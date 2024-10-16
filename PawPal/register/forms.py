from django import forms
from .models import CustomUser, Caretaker

class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'user_type']
        widgets = {
            'password': forms.PasswordInput(),
        }

    USER_TYPES = [
        ('owner', 'Pet Owner'),
        ('caretaker', 'Pet Caretaker'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'border-2 border-black w-96  bg-textfield px-2 py-1 rounded-md'})