# coding=utf-8
from xml.etree.ElementTree import ElementTree
import re
from kotourism.places.models import Place, PlaceType

tag_names = {
    u"ЮридичнаНазва": 'name',
    u"Адреса": 'address',
    u"Телефон": 'phone',
    u"РежимРоботи": 'timetable',
    u"Сайт": 'url',
    u"Экспозиции": 'exposition',
    u"Транспорт": 'transport',
}

lang_names = {
    u"У": 'uk',
    u"Р": 'ru',
    u"А": 'en',
}

conversion = {
    u'а': u'a',
    u'б': u'b',
    u'в': u'v',
    u'г': u'g',
    u'д': u'd',
    u'е': u'e',
    u'є': u'je',
    u'ё': u'e',
    u'ж': u'zh',
    u'з': u'z',
    u'і': u'i',
    u'ї': u'ji',
    u'и': u'i',
    u'й': u'j',
    u'к': u'k',
    u'л': u'l',
    u'м': u'm',
    u'н': u'n',
    u'о': u'o',
    u'п': u'p',
    u'р': u'r',
    u'с': u's',
    u'т': u't',
    u'у': u'u',
    u'ф': u'f',
    u'х': u'h',
    u'ц': u'c',
    u'ч': u'ch',
    u'ш': u'sh',
    u'щ': u'sch',
    u'ь': u'',
    u'ы': u'y',
    u'э': u'e',
    u'ю': u'ju',
    u'я': u'ja',
}

dash_re = re.compile(u" +")

def cyr2lat(s):
    s = s.lower()
    retval = []
    for c in s:
        if c.isalnum():
            default = c
        else:
            default = u" "
        c = conversion.get(c, default)
        retval.append(c)
    retval = u"".join(retval)
    retval = dash_re.sub(u" ", retval).strip().replace(u" ", u"-")
    return retval

place_re = re.compile(u" +")

def prep_text(text):
    res = place_re.sub(u" ", text).strip()
    return res if res != u"-" else u""

def make_slug(name, code):
    slug = cyr2lat(name.lower())[:40]
    code = unicode(code) # base64.b32encode(unicode(code)).rstrip('=').lower() # Some obscure encoding
    return u"-".join([slug, code])

def gen_place(node):
    place = dict(interop_code=prep_text(node.attrib[u"Код"]))
    for attrib in node:
        if attrib.text:
            lang_name = attrib.attrib.get(u"Мова", None)
            lang_code = lang_names[lang_name] if lang_name else None

            property_name = tag_names[attrib.tag]
            if lang_code:
                property_name = u"{}_{}".format(property_name, lang_code)

            place[property_name] = prep_text(attrib.text)
    if len(place['name_uk']) == 0:
        place['name_uk'] = place['interop_code']
    return place

def update_place(model, values):
    changed = False
    for code, value in values.iteritems():
        if hasattr(model, code) and getattr(model, code) != value:
            setattr(model, code, value)
            changed = True
    return changed

def load_places(place_type, places):
    place_queryset = Place.objects.filter(type=place_type)
    place_cache = dict()
    for place_model in place_queryset:
        place_cache[place_model.interop_code] = place_model
    for place_dict in places:
        interop_code = place_dict['interop_code']
        place_dict['slug'] = make_slug(place_dict['name_en'], interop_code)
        place_model = place_cache.get(interop_code, Place(type=place_type))
        if update_place(place_model, place_dict):
            place_model.save()

def load_place_types(place_type_dict):
    place_type_queryset = PlaceType.objects.all()
    for place_type in place_type_queryset:
        place_dict = place_type_dict.get(place_type.name_uk, None)
        if place_dict:
            load_places(place_type, place_dict)

def load(data):
    tree = ElementTree()
    root = tree.parse(data)

    head = dict(date=root.attrib[u"Дата"], time=root.attrib[u"Время"])
    tree_res = dict(head=head, types=dict())

    for place_cat in root:
        for place_type in place_cat:
            name = place_type.attrib[u"Назва"]
            places = []
            for place in place_type:
                places.append(gen_place(place))
            tree_res['types'][name] = places

    load_place_types(tree_res['types'])
