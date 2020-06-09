import os
import sys

from django.contrib.auth import get_user_model

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from django.db import DatabaseError
import scraping.work
from scraping.models import Vacancy, City, Language, Url

User = get_user_model()

urls = ('http://trudbox.by/minsk?whatQuery=python',)


def get_info():
    qs = User.objects.filter(is_subscribed=True).values()
    info_list = set((q['city_id'], q['language_id']) for q in qs)
    return info_list


def get_urls(_info):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _info:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dict[pair]
        urls.append(tmp)
    return urls


q = get_info()
u = get_urls(q)

city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()
jobs = scraping.work.work(urls[0])
for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass
