from django import forms


class FilterForm(forms.Form):
    vendor = forms.CharField(required=False)
    vulner = forms.CharField(required=False)
