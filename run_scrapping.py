from django.contrib.auth import get_user_model
from django.db import DatabaseError
import os
import sys
import time
import asyncio

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

jobs, errors = [], []


def get_info():
    qs = User.objects.filter(is_subscribed=True).values()
    info_list = set((q['city_id'], q['language_id']) for q in qs)
    return info_list


def get_urls(_info):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _info:
        if pair in url_dict:
            tmp = dict()
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dict[pair]
            urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value  # Unpack
    job, err = await loop.run_in_executor(None, func, url, city, language)  # Start worker
    errors.extend(err)  # Add results into list
    jobs.extend(job)


info = get_info()
url_list = get_urls(info)

start = time.time()

loop = asyncio.get_event_loop()  # Create loop
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language']) for data in url_list for func, key in
             parsers]  # Create tasks list (pack)
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])  # Give args for workers

# for data in url_list:
#
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()  # close loop

print(time.time()-start)

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    err = Error(date=errors).save()
