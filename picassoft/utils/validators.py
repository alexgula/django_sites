# coding=utf-8
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_percent(value):
    if value < -100 or value > 100:
        raise ValidationError(u"{0} {1}".format(value, _("is not a percent number (must be between -100 and 100)")))

def validate_bounds(name, value, lower_bound, upper_bound):
    if value <= lower_bound or value > upper_bound:
        raise ValidationError(u"{0} ({1}) {2} ({3}; {4}]".format(name, value, _("is out of bounds"), lower_bound, upper_bound))
