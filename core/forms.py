from django import forms
from .models import Booking, AppointmentSlot
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Clinic

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['slot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the initial slot (if any) from the instance
        if self.instance.pk:  # Check if it's an existing instance (update)
            initial_slot = self.instance.slot
            # Create a queryset that includes the initial slot, even if it's not available
            queryset = AppointmentSlot.objects.filter(pk=initial_slot.pk) | AppointmentSlot.objects.filter(is_available=True) # Combine the querysets
            self.fields['slot'].queryset = queryset.distinct() # Ensure no duplicates
        else:
            # If it's a new form, just show available slots
            self.fields['slot'].queryset = AppointmentSlot.objects.filter(is_available=True)
        self.fields['slot'].empty_label = "Select an available slot"

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    clinic = forms.ModelChoiceField(
    queryset = Clinic.objects.all(),
    empty_label = "Select your clinic",
    required=True
)
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'clinic', 'phone_number')
        labels = {
            'email': 'Email Address',
            'full_name': 'Full Name',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
            }
        help_texts = {
            'email' : "We'll never share your email"
        }