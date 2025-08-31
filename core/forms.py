from django import forms
from .models import Booking, AppointmentSlot

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