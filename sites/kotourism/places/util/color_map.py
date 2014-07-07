from PIL import Image
from picassoft.utils.templatetags.markup import restructuredtext
from ..models import Region

def pixel_to_hex(pixel):
    """Encode (R,G,B,A) tuple to RRGGBB hex value.

    Doesn't support 'P' palette mode currently."""
    return "{0:02x}{1:02x}{2:02x}".format(*pixel)

def normalize_color(color):
    color = color.strip()
    if color.startswith("#"):
        color = color[1:]
    return color.lower()

def build_region_ids():
    region_map = dict()
    for region in Region.objects.all():
        color = normalize_color(region.map_color)
        if color and region_map.has_key(color):
            raise KeyError("Duplicate color {} for regions".format(color))
        region_map[color] = region
    return region_map

def build_color_data(file_name):
    im = Image.open(file_name)
    region_map = build_region_ids()

    def region_for_color(pixel):
        region = region_map.get(pixel_to_hex(pixel), None)
        return region.map_id if region is not None else 0
    color_map = [region_for_color(p) for p in im.getdata()]

    region_map_repr = dict()
    for region in region_map.values():
        icon = region.icon.url if region.icon else ""
        desc = restructuredtext(region.desc)
        url = region.get_absolute_url()
        region_map_repr[region.map_id] = dict(name=region.name, icon=icon, desc=desc, url=url)

    return dict(color_map=color_map, size=im.size, region_map=region_map_repr)
