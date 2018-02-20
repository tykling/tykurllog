from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import UrlSearchForm
from .models import LoggedUrl


class UrlSearchView(FormMixin, ListView):
    model = LoggedUrl
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        # get the form
        form = UrlSearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data.get('q'):
                # First, get the results filtered by the q term
                results = LoggedUrl.objects.filter(url__contains=form.cleaned_data.get('q')).order_by('-when')
            else:
                # Workaround to return all results when there is no searchword (instead of returning 0 results)
                results = LoggedUrl.objects.all().order_by('-when')

            # Filter channel if requested
            if form.cleaned_data['channel']:
                print("filtering %s results by channel %s" % (sqs.count(), form.cleaned_data['channel']))
                results = results.filter(channel=form.cleaned_data['channel'])

            # Filter usermask if requested
            if form.cleaned_data['usermask']:
                print("filtering %s results by usermask %s" % (sqs.count(), form.cleaned_data['usermask']))
                results = results.filter(usermask__icontains=form.cleaned_data['usermask'])


            # Filter start_date if requested
            if form.cleaned_data['start_date']:
                print("filtering %s results by start_date %s" % (sqs.count(), form.cleaned_data['start_date']))
                results = results.filter(when__gte=form.cleaned_data['start_date'])

            # Filter end_date if requested
            if form.cleaned_data['end_date']:
                # add timestamp to end_date to include the whole end_date day,
                # because datefields are compared as 0am on the given date, 
                # which is what we want for start_date but not for end_date)
                end_time = datetime.datetime.combine(form.cleaned_data['end_date'], datetime.time.max)
                print("filtering %s results by end_date %s" % (sqs.count(), form.cleaned_data['end_date']))
                results = results.filter(when__lte=end_time)
        else:
            results = None

        # get ready to return the result
        if results:
            # return to the search page with the results
            paginator = Paginator(results, 100) # Show 100 results per page
            resultpage = paginator.get_page(request.GET.get('page'))
        else:
            resultpage = None

        return render(
            request=self.request,
            template_name='search.html',
            context={
                'results': resultpage,
                'form': form,
            }
        )

