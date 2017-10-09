from django import forms


class OptionalEquipmentForm(forms.Form):
    equipment = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    email_intrepid_also = forms.BooleanField(required=False)
