from haystack import indexes
from .models import LoggedUrl


class LoggedUrlIndex(indexes.SearchIndex, indexes.Indexable):
    # use template even though we only have one field, 
    # because special characters like / seem to be indexed wrongly when not using template
    #text = indexes.EdgeNgramField(model_attr='url', document=True)
    text = indexes.EdgeNgramField(document=True, use_template=True)
    when = indexes.DateTimeField(model_attr='when')
    usermask = indexes.EdgeNgramField(model_attr='usermask')
    channel = indexes.CharField(model_attr='channel')

    def get_model(self):
        return LoggedUrl

