from django import forms


class FilterForm(forms.Form):
    vendor = forms.CharField(required=False, label='Vendor')
    vulner = forms.CharField(required=False, label='Vulner')
