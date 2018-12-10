from django import forms
from django.core.exceptions import ValidationError


class FilterForm(forms.Form):
    vendor = forms.CharField(required=False)
    vulner = forms.CharField(required=False)
