# coding=utf-8
import csv
from decimal import Decimal
from django.contrib.auth.models import User
from .models import CustomerProfile
from ..catalog.models import default_price_type, get_price_type_dict

def read_csv(filename, delimiter=';', quotechar='\"'):
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            yield row

user_map = {
    'u_login': 'username',
    'u_name': 'first_name',
    'u_lastname': 'last_name',
    'u_email': 'email',
    'u_password': ('password', lambda v: u'md5$${}'.format(v)),
}

profile_map = {
    'u_patronymic': 'father_name',
    'u_id1c': 'code1c',
    'u_name1c': 'username1c',
    'u_mobile': 'phone',
    'u_city': 'city',
    'u_adres': 'address',
    'u_delivery': 'delivery',
    'u_group': 'price_type',
    'u_discount': ('discount', lambda v: Decimal(v) if v else Decimal(0)),
}

def convert_value(map, key, value, target):
    if map.has_key(key):
        map_key = map[key]
        value = unicode(value, encoding='utf8')
        if isinstance(map_key, tuple):
            map_key, convertor = map_key
            value = convertor(value)
        target[map_key] = value

def map_row(row):
    user, profile = {}, {}
    for key, value in row.iteritems():
        convert_value(user_map, key, value, user)
        convert_value(profile_map, key, value, profile)
    return user, profile

def load_users(filename):
    price_types = get_price_type_dict()
    default = default_price_type()
    loaded = skipped = inserted = 0
    for row in read_csv(filename):
        loaded += 1
        user_dict, profile_dict = map_row(row)
        try:
            User.objects.get(username=user_dict['username'])
            skipped += 1
        except User.DoesNotExist:
            user = User.objects.create(**user_dict)
            profile_dict['user'] = user
            if profile_dict['price_type']:
                profile_dict['price_type'] = price_types.get(profile_dict['price_type'], default)
            else:
                profile_dict['price_type'] = default
            CustomerProfile.objects.create(**profile_dict)
            inserted += 1
    return loaded, skipped, inserted
