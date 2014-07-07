# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions
from picassoft.utils.feincms_translation import TranslatedFeinCMSInline

from .content.models import ImageContent, RestructuredContent, HtmlContent, News, InfoPage, GalleryPage
from .blocks.models import TextBlock

# Have to place FeinCMS registers here, because translations.py is imported when models are imported,
# which are imported in FeinCMS registers. Thus translations are imported before models are registered.

ImageContent.feincms_item_editor_inline = TranslatedFeinCMSInline
RestructuredContent.feincms_item_editor_inline = TranslatedFeinCMSInline
HtmlContent.feincms_item_editor_inline = TranslatedFeinCMSInline

def register_model(model_class, model_fields):
    class ModelTranslationOptions(TranslationOptions):
        fields = model_fields

    translator.register(model_class, ModelTranslationOptions)

def register_content_model(model_class, model_fields=('title', 'text'), register_text=True, register_html=False):
    model_class.register_regions(('main', _("Main content area")),)
    ModelRestructuredContent = model_class.create_content_type(RestructuredContent, class_name=model_class.__name__ + 'Text') if register_text else None
    ModelHtmlContent = model_class.create_content_type(HtmlContent, class_name=model_class.__name__ + 'Html') if register_html else None
    ModelImageContent = model_class.create_content_type(ImageContent, class_name=model_class.__name__ + 'Image')

    register_model(model_class, model_fields)

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

register_content_model(News)
register_content_model(InfoPage)
register_content_model(GalleryPage, register_text=False)

register_model(TextBlock, ('text',))
