from .forms import UrlSearchForm
from haystack.generic_views import SearchView


class UrlSearchView(SearchView):
    template_name = 'search.html'
    form_class = UrlSearchForm

search = UrlSearchView.as_view()


