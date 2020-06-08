import os
import sys

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from django.db import DatabaseError
import scraping.work
from scraping.models import Vacancy, City, Language

city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()
jobs = scraping.work.work()
for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass
