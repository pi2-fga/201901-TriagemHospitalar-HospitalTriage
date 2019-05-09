from django import forms
from django.forms.widgets import NumberInput


class RangeInput(NumberInput):
    input_type = 'range'


class TextForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class SelectForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class ScaleForm(forms.Form):
    number = forms.IntegerField(widget=RangeInput, min_value=0, max_value=10)
