# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions
from picassoft.utils.feincms_translation import TranslatedFeinCMSInline

from .events.models import Event
from .places.models import Region, PlaceType, Place, Track
from .slideshow.models import Slide
from .content.models import ImageContent, RestructuredContent, FileContent
from .exhibit.models import Exhibit, ExhibitSection, ExhibitMap, ExhibitPartner
from .photocontest.models import Contest

# Have to place FeinCMS registers here, because translations.py is imported when models are imported,
# which are imported in FeinCMS registers. Thus translations are imported before models are registered.

FEINCMS_TEMPLATES = {
    'default': [
        {
            'key': 'standart',
            'title': _("Standard template"),
            'path': '{model}_detail_standart.html',
            'regions': (
                ('main', _("Main content area")),
                ('sideleft', _("Sidebar left")),
                ('sideright', _("Sidebar right")),
            ),
        }, {
            'key': '2col',
            'title': _("Two columns"),
            'path': '{model}_detail_2col.html',
            'regions': (
                ('main', _("Column one")),
                ('side', _("Column two")),
            ),
        }
    ],
}

RestructuredContent.feincms_item_editor_inline = TranslatedFeinCMSInline

def register_model(model_class, model_fields):
    class ModelTranslationOptions(TranslationOptions):
        fields = model_fields

    translator.register(model_class, ModelTranslationOptions)

def register_content_model(model_class, model_fields, register_file):
    model_class.register_templates(*FEINCMS_TEMPLATES['default'])

    ModelRestructuredContent = model_class.create_content_type(RestructuredContent, class_name='RestructuredContent')
    model_class.create_content_type(ImageContent, class_name='ImageContent')
    if register_file: model_class.create_content_type(FileContent, class_name='FileContent')

    register_model(model_class, model_fields)

    class ModelRestructuredContentTranslationOptions(TranslationOptions):
        fields = 'text',

    translator.register(ModelRestructuredContent, ModelRestructuredContentTranslationOptions)


register_content_model(Event, ('name', 'desc', 'place', 'organizer', ), True)
register_content_model(Region, ('name', 'desc', ), False)

register_model(Slide, ('name', 'desc', ))
register_model(PlaceType, ('name', ))
register_model(Place, ('name', 'address', 'phone', 'timetable', 'exposition', 'transport', 'desc', ))
register_model(Track, ('name', 'track', ))
register_model(Exhibit, ('name', 'desc', ))
register_model(ExhibitSection, ('name', 'desc', ))
register_model(ExhibitMap, ('name', 'desc', ))
register_model(ExhibitPartner, ('name', ))
register_model(Contest, ('name', ))
