from django import forms
from haystack.forms import SearchForm
from .models import IrcChannel, LoggedUrl
import datetime

class UrlSearchForm(SearchForm):
    start_date = forms.DateField(input_formats=['%Y%m%d'], required=False, widget=forms.DateInput(attrs={'class': 'datepicker'}), help_text='Show urls logged no earlier than this date. Format: YYYYMMDD')
    end_date = forms.DateField(input_formats=['%Y%m%d'], required=False, widget=forms.DateInput(attrs={'class': 'datepicker'}), help_text='Show urls logged no later than this date. Format: YYYYMMDD')
    usermask = forms.CharField(required=False)
    channel = forms.ModelChoiceField(required=False, queryset=IrcChannel.objects.all(), empty_label=None)
    
    def __init__(self, *args, **kwargs):
        super(UrlSearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].help_text = 'Show only URLs containing this text'

    def no_query_found(self):
        #return self.searchqueryset.all()
        return LoggedUrl.objects.all()

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(UrlSearchForm, self).search()
        
        # Filter usermask if relevant
        if self.cleaned_data['usermask']:
            print("filtering %s results by usermask %s" % (sqs.count(), self.cleaned_data['usermask']))
            sqs = sqs.filter(mask__contains=self.cleaned_data['usermask'])
        

        # Filter start_date if requested
        if self.cleaned_data['start_date']:
            print("filtering %s results by start_date %s" % (sqs.count(), self.cleaned_data['start_date']))
            sqs = sqs.filter(when__gte=self.cleaned_data['start_date'])
        
        # Filter end_date if requested
        if self.cleaned_data['end_date']:
            # add timestamp to end_date to include the whole end_date day,
            # because datefields are compared as 0am on the given date, 
            # which is what we want for start_date but not for end_date)
            end_time = datetime.datetime.combine(self.cleaned_data['end_date'], datetime.time.max)
            print("filtering %s results by end_date %s" % (sqs.count(), self.cleaned_data['end_date']))
            sqs = sqs.filter(when__lte=end_time)

        # Filter channel if relevant
        if self.cleaned_data['channel']:
            print("filtering %s results by channel %s" % (sqs.count(), self.cleaned_data['channel']))
            sqs = sqs.filter(channel=self.cleaned_data['channel'])

        return sqs

