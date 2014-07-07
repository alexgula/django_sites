# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions
from picassoft.utils.feincms_translation import TranslatedFeinCMSInline

from content.models import  ImageContent, RestructuredContent, HtmlContent
from news.models import News
from library.models import Author, Work, Publisher
from page.models import Page

# Have to place FeinCMS registers here, because translations.py is imported when models are imported,
# which are imported in FeinCMS registers. Thus translations are imported before models are registered.

def register_model(model_class, model_fields):
    class ModelTranslationOptions(TranslationOptions):
        fields = model_fields

    translator.register(model_class, ModelTranslationOptions)

def register_content_model(model_class, model_fields, translate=False, register_text=True, register_html=False):
    model_class.register_regions(('main', _("Main content area")),)
    ModelRestructuredContent = model_class.create_content_type(RestructuredContent, class_name=model_class.__name__ + 'Text') if register_text else None
    ModelHtmlContent = model_class.create_content_type(HtmlContent, class_name=model_class.__name__ + 'Html') if register_html else None
    ModelImageContent = model_class.create_content_type(ImageContent, class_name=model_class.__name__ + 'Image')

    if translate:
        register_model(model_class, model_fields)

        ModelRestructuredContent.feincms_item_editor_inline = TranslatedFeinCMSInline
        ModelHtmlContent.feincms_item_editor_inline = TranslatedFeinCMSInline
        ModelImageContent.feincms_item_editor_inline = TranslatedFeinCMSInline

        if register_text:
            class ModelRestructuredContentTranslationOptions(TranslationOptions):
                fields = 'text',

            translator.register(ModelRestructuredContent, ModelRestructuredContentTranslationOptions)

        if register_html:
            class ModelHtmlContentTranslationOptions(TranslationOptions):
                fields = 'text',

            translator.register(ModelHtmlContent, ModelHtmlContentTranslationOptions)

        class ModelImageContentTranslationOptions(TranslationOptions):
            fields = 'caption',

        translator.register(ModelImageContent, ModelImageContentTranslationOptions)

register_content_model(Work, ())

register_content_model(Page, ('title',), translate=True, register_html=True)

register_model(News, ('title', 'text',))

register_model(Author, ('first_name', 'family_name',))
register_model(Publisher, ('name',))
