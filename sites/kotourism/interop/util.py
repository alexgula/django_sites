# coding=utf-8
from picassoft.utils.http import post_xml_file


def reconstruct_slugs():
    from ..places.models import Place
    from .data_import import make_slug

    for place in Place.objects.filter(interop_code__isnull=False).exclude(interop_code=u''):
        slug = make_slug(place.name, place.interop_code)
        if slug != place.slug:
            place.slug = slug
            place.save()


if __name__ == '__main__':
    r = post_xml_file('http://localhost:8001/uk/interop/upload/',
                      r'E:/Picassoft/Projects/Django/sites/kotourism/tmp/turizm.xml', 'interop', 'loponeda39')
    print(r.status_code)
    print(r.content)
