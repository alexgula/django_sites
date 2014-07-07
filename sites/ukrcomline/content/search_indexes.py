# coding=utf-8
from haystack import indexes
from .models import News, Portfolio, StaticPage


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, model_attr='get_text')
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField(model_attr='title')
    desc = indexes.CharField(model_attr='desc')

    def get_model(self):
        return News

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)


class PortfolioIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, model_attr='get_text')
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField(model_attr='title')
    desc = indexes.CharField(model_attr='desc')

    def get_model(self):
        return Portfolio

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)


class StaticPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, model_attr='get_text')
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField(model_attr='title')
    desc = indexes.CharField(model_attr='desc')

    def get_model(self):
        return StaticPage

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)
