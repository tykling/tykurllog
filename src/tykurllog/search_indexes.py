from haystack import indexes
from .models import LoggedUrl


class LoggedUrlIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='url', document=True)
    when = indexes.DateTimeField(model_attr='when')
    usermask = indexes.CharField(model_attr='usermask')
    channel = indexes.CharField(model_attr='channel')

    def get_model(self):
        return LoggedUrl

