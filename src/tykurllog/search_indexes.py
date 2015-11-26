from haystack import indexes
from .models import LoggedUrl


class LoggedUrlIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(model_attr='url', document=True)
    when = indexes.DateTimeField(model_attr='when')
    usermask = indexes.EdgeNgramField(model_attr='usermask')
    channel = indexes.CharField(model_attr='channel')

    def get_model(self):
        return LoggedUrl

