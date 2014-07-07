# coding=utf-8
import json
from StringIO import StringIO # cStringIO cannot work with Unicode!
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils import translation


def get_first(d, *args):
    """Get first item from the dictionary, that is not None, using one of the keys provided.
    The last argument is default value."""
    for key in args[:-1]:
        if key in d:
            return d[key]
    return args[-1]


class TranslatedUnicode(object):

    def __init__(self, data=None):
        if isinstance(data, basestring):
            self.data = json.loads(data)
        else:
            self.data = data
        if self.data is None:
            self.data = []

    def __unicode__(self):
        """Pack text chunks into one string.

        Each chunk can be either string (or any convertible object) or the following dictionary:
        {
            'LANGUAGE_CODE_1': "text_1",
            'LANGUAGE_CODE_2': "text_2",
            ...
        }.
        """
        result = []
        for chunk in self.data:
            if isinstance(chunk, dict):
                chunk_dict = {}
                for lang_code, text in chunk.iteritems():
                    if text:
                        chunk_dict[lang_code.upper()] = force_unicode(text)
                result.append(chunk_dict)
            else:
                result.append(force_unicode(chunk))
        return json.dumps(result, ensure_ascii=False)

    def translate(self, lang_code=None):
        """Filters out from the text only parts in the specified language and parts with unspecified language.

        >>>t = TranslatedUnicode(u'["ABC", {"RU": "KLM", "UK": "EFG"}, "XYZ"]')
        >>>t.translate('uk')
        'ABCEFGXYZ'
        >>>t.translate('ru')
        'ABCKLMXYZ'
        """
        if lang_code is None:
            lang_code = translation.get_language()
        result = StringIO()
        for chunk in self.data:
            if isinstance(chunk, dict):
                result.write(get_first(chunk, lang_code.upper(), settings.LANGUAGE_CODE.upper(), u""))
            else:
                result.write(chunk)
        return force_unicode(result.getvalue())

    def add(self, other):
        self.data.extend(other.data)

    def add_text(self, text):
        self.data.append(force_unicode(text))

    def add_field_translations(self, obj, field_name):
        result = {}
        for lang in settings.LANGUAGES:
            lang_code = lang[0]
            value = getattr(obj, '{}_{}'.format(field_name, lang_code))
            if value:
                result[lang_code] = value
        self.data.append(result)

    def add_content_translations(self, obj):
        for region in obj.content._fetch_regions().itervalues():
            for content in region:
                translations = content.get_text_translations()
                if translations:
                    self.data.extend(translations.data)

    def add_text_translations(self, text, context=None):
        chunk = {}
        for lang in settings.LANGUAGES:
            translation.activate(lang[0])
            value = u""
            if context:
                value = translation.pgettext(context, text)
            if not context or not value:
                value = translation.ugettext(text)
            if value:
                chunk[lang[0]] = value
        self.data.append(chunk)
