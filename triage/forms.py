from django import forms
from django.utils.translation import ugettext_lazy as _


class TextForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True,
                              widget=forms.Textarea)


BOOL_CHOICES = ((_('Sim'), _('Sim')), (_('Não'), _('Não')))


class BooleanForm(forms.Form):
    boolean = forms.ChoiceField(required=True, choices=BOOL_CHOICES,
                                widget=forms.RadioSelect)
