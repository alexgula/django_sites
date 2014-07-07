# coding=utf-8
from haystack import indexes
from .models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, model_attr='get_text_translations')
    url = indexes.CharField(model_attr='get_nonlocal_url')
    name = indexes.CharField(model_attr='get_name_translations')
    type = indexes.CharField(model_attr='get_type_translations')
    desc = indexes.CharField(model_attr='get_desc_translations')

    def get_model(self):
        return Event

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)
