# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions
from picassoft.utils.feincms_translation import TranslatedFeinCMSInline

from content.models import News, Portfolio, Certificate, StaticPage, ImageContent, RestructuredContent, FileContent


# Have to place FeinCMS registers here, because translations.py is imported when models are imported,
# which are imported in FeinCMS registers. Thus translations are imported before models are registered.


#def register_model(model_class, *model_fields):
    #class ModelTranslationOptions(TranslationOptions):
    #    fields = model_fields

    #translator.register(model_class, ModelTranslationOptions)


def register_content_type(model_class, content_model_class, *content_model_fields):
    ModelContent = model_class.create_content_type(content_model_class,
                                                   class_name=model_class.__name__ + content_model_class.__name__)
    #ModelContent.feincms_item_editor_inline = TranslatedFeinCMSInline
    #register_model(ModelContent, *content_model_fields)


def register_content_model(model_class, *model_fields):
    model_class.register_templates({
        'key': 'standard',
        'title': _("Standard template"),
        'path': '{model}_detail_standard.html',
        'regions': (
            ('main', _("Content")),
        ),
    })

    register_content_type(model_class, ImageContent, 'caption')
    register_content_type(model_class, RestructuredContent, 'text')
    register_content_type(model_class, FileContent, 'caption')

    #register_model(model_class, *model_fields)


register_content_model(News, 'title', 'desc')
register_content_model(Portfolio, 'title', 'desc')
register_content_model(StaticPage, 'title', 'desc')
register_content_model(Certificate, 'title', 'desc')
