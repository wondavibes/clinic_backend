from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("book/", views.book_slot, name="book_slot"),
    path("success/", views.booking_success, name="booking_success"),
    path("login/", views.custom_login, name="custom_login"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("booking_history/", views.booking_history, name="booking_history"),
    path("", views.register, name="Home"),
    path("logout/", views.custom_login, name="logout"),
    path(
        "cancel_booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"
    ),
    path("view_booking/<int:booking_id>/", views.view_booking, name="view_booking"),
]

# The above code defines the URL patterns for the clinic API.
