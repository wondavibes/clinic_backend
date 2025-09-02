from . import views
from django.urls import path


urlpatterns = [
    path('book/', views.book_slot, name='book_slot'),
    path('success/', views.booking_success, name='booking_success'),
    path('login/', views.custom_login, name='custom_login'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('booking_history/', views.booking_history, name='booking_history')
]

# The above code defines the URL patterns for the clinic API.