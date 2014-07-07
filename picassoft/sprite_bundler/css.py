# coding=utf-8
import re


_CSS_REGEXP = re.compile(r'[^a-zA-Z\-_0-9]')
_CSS_ELEMENT_TEMPLATE = """
.{selector} {{
    display: block;
    width: {width};
    height: {height};
    background: {background};
}}
"""


def _format_size(size, unit='px'):
    if size == 0:
        return '0'
    else:
        return '{}{}'.format(size, unit)


def _format_background(url, x, y):
    return 'url("{}") {} {}'.format(url, _format_size(x), _format_size(y))


def _clear_css_name(name):
    name = name.replace(' ', '-').replace('.', '-')
    return _CSS_REGEXP.sub('', name)


def _format_css_name(template, filename, fileext):
    filename = _clear_css_name(filename)
    fileext = _clear_css_name(fileext)
    return template.format(name=filename, ext=fileext)


def _generate_css_element(box, cssname_format, url, height_divider=1, height_shift=0, css_modifier=""):
    return _CSS_ELEMENT_TEMPLATE.format(
        selector=_format_css_name(cssname_format, box.filename, box.fileext) + css_modifier,
        width=_format_size(box.width),
        height=_format_size(box.height / height_divider),
        background=_format_background(url, -box.x, -box.y - height_shift * box.height / height_divider))


def generate_css(url, cssname_format, areas):
    for area in areas:
        for box in area.boxes():
            if box.hover:
                yield _generate_css_element(box, cssname_format, url, 2, 0)
                yield _generate_css_element(box, cssname_format, url, 2, 1, ":hover")
            else:
                yield _generate_css_element(box, cssname_format, url)
