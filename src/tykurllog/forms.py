from django import forms
from django.utils import timezone
from .models import IrcChannel, LoggedUrl
import datetime

class UrlSearchForm(forms.Form):
    q = forms.CharField(help_text = 'Show only URLs containing this text', required=False)
    start_date = forms.DateField(input_formats=['%Y%m%d'], required=False, widget=forms.DateInput(attrs={'class': 'datepicker'}), help_text='Show urls logged no earlier than this date. Format: YYYYMMDD')
    end_date = forms.DateField(input_formats=['%Y%m%d'], required=False, widget=forms.DateInput(attrs={'class': 'datepicker'}), help_text='Show urls logged no later than this date. Format: YYYYMMDD')
    usermask = forms.CharField(required=False)
    channel = forms.ModelChoiceField(required=False, queryset=IrcChannel.objects.all())

