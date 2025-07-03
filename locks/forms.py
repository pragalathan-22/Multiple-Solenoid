from django import forms
from .models import LockCommand

class LockCommandForm(forms.ModelForm):
    class Meta:
        model = LockCommand
        fields = '__all__'
