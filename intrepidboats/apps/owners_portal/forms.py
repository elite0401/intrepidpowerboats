from django import forms

from intrepidboats.apps.common.models import ExtraUserData
from .models import SharedPicture


class SharedPictureForm(forms.ModelForm):
    class Meta:
        model = SharedPicture
        fields = ['comment', 'is_public', 'image', ]
        widgets = {
            'is_public': forms.RadioSelect
        }


class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = ExtraUserData
        fields = ['profile_picture', 'gallery_header']

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
