# coding=utf-8
from haystack import indexes
from .models import Category, Product


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, model_attr='get_text')
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField(model_attr='title')
    desc = indexes.CharField(model_attr='desc')
    logo = indexes.CharField(model_attr='logo')

    def get_model(self):
        return Category

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, model_attr='get_text')
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField(model_attr='title')
    desc = indexes.CharField(model_attr='desc')
    logo = indexes.CharField(model_attr='logo')

    def get_model(self):
        return Product

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)
