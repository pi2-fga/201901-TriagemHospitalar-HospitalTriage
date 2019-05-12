from django import forms


class TextForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True,
                              widget=forms.Textarea)


class BooleanForm(forms.Form):
    boolean = forms.BooleanField(required=True)
