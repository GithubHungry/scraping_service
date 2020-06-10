from django.contrib.auth import get_user_model
from django.db import DatabaseError
import os
import sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.parsers import *
from scraping.models import City, Vacancy, Language, Error, Url

User = get_user_model()

parsers = (
    (trudbox, 'trudbox'),
    (work, 'work'),
)


def get_info():
    qs = User.objects.filter(is_subscribed=True).values()
    info_list = set((q['city_id'], q['language_id']) for q in qs)
    return info_list


def get_urls(_info):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _info:
        tmp = dict()
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dict[pair]
        urls.append(tmp)
    return urls


info = get_info()
url_list = get_urls(info)

jobs, errors = [], []

for data in url_list:

    for func, key in parsers:
        url = data['url_data'][key]
        j, e = func(url, city=data['city'], language=data['language'])
        jobs += j
        errors += e

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    err = Error(date=errors).save()
