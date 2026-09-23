from django import forms

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')
        widgets = {
            'avatar': forms.ClearableFileInput(
                attrs={'accept': 'image/*'},
            ),
            'bio': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Tell us about yourself',
                },
            ),
        }