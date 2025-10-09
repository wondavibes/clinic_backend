from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Booking, AppointmentSlot
from django.contrib.auth.decorators import login_required
from .forms import BookingForm, LoginForm
from django.conf import settings
from django.db import transaction
from .forms import CustomUserCreationForm

"""@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            booking.slot.is_available = False
            booking.slot.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'core/book_appointment.html', {'form': form})"""


# Create your views here.
def booking_success(request):
    return render(request, "core/booking_success.html")


@login_required
def user_dashboard(request):
    # get the next booking
    next_booking = (
        Booking.objects.filter(user=request.user, slot__date__gte=timezone.now().date())
        .order_by("slot__date", "slot__start_time")
        .first()
    )
    if next_booking:
        return render(
            request, "core/user_dashboard.html", {"next_booking": next_booking}
        )
    else:
        return render(request, "core/user_dashboard.html")


def custom_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # try backend that accepts email first, then fall back to username
            user = authenticate(request, email=email, password=password)
            if user is None:
                user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_dashboard")
            form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, "core/login.html", {"form": form})


@login_required
def book_slot(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            selected_slot = form.cleaned_data["slot"]
            user = request.user
            today = timezone.now().date()

            if not selected_slot.is_available:
                form.add_error(None, "Selected slot is no longer available.")
            else:
                # check if user already booked this exact slot
                if Booking.objects.filter(user=user, slot=selected_slot).exists():
                    form.add_error(None, "You have already booked that slot.")
                else:
                    bookings_today = Booking.objects.filter(
                        user=user, slot__date=today
                    ).count()
                    if bookings_today >= getattr(settings, "MAX_BOOKINGS_PER_DAY", 3):
                        form.add_error(
                            None, "You've reached your booking limit for today."
                        )
                    else:
                        # prevent race conditions by locking the slot row
                        with transaction.atomic():
                            slot = AppointmentSlot.objects.select_for_update().get(
                                pk=selected_slot.pk
                            )
                            if not slot.is_available:
                                form.add_error(
                                    None, "Selected slot was taken just now."
                                )
                            else:
                                booking = form.save(commit=False)
                                booking.user = user
                                booking.save()
                                slot.is_available = False
                                slot.save()
                                return redirect("booking_success")
        # fall through to re-render form with validation errors
    else:
        form = BookingForm()

    return render(request, "core/book_appointment.html", {"form": form})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-booked_at")
    return render(request, "core/booking_history.html", {"bookings": bookings})


def register(request):
    # if request.user.is_authenticated:
    # return redirect('user_dashboard')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("custom_login")
    else:
        form = CustomUserCreationForm()

    return render(request, "core/register.html", {"form": form})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == "Upcoming":
        booking.status = "Cancelled"
        booking.slot.is_available = True
        booking.slot.save()
        booking.save()
        messages.success(request, "Your appointment has been cancelled successfully.")
    else:
        messages.error(request, "Only upcoming bookings can be cancelled.")
    return redirect("booking_history")


@login_required
def view_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "core/view_booking.html", {"booking": booking})
