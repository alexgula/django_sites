# coding=utf-8
from django.utils.translation import ugettext_lazy as _

POSITION_LEFT = 'left'
POSITION_RIGHT = 'right'

POSITION_CHOICES = (
    (POSITION_LEFT, _("Left")),
    (POSITION_RIGHT, _("Right")),
)

IMAGESIZE_270 = '270'
IMAGESIZE_570 = '570'
IMAGESIZE_870 = '870'

IMAGESIZE_CHOICES = (
    (IMAGESIZE_270, _("One Column (270px)")),
    (IMAGESIZE_570, _("Two Column (570px)")),
    (IMAGESIZE_870, _("One Column (870px)")),
)