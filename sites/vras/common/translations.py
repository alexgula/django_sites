# coding=utf-8
from modeltranslation.translator import translator, TranslationOptions

from content.models import News, StaticPage
from catalog.models import Category


def register_model(model_class, *model_fields):
    class ModelTranslationOptions(TranslationOptions):
        fields = model_fields

    translator.register(model_class, ModelTranslationOptions)


register_model(News, 'title', 'desc')
register_model(StaticPage, 'title', 'desc')
register_model(Category, 'title', 'desc')
