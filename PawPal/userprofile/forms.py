from django import forms
from .models import User

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'border-2 border-black w-96  bg-textfield px-2 py-1 rounded-md'})