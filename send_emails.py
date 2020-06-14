import os
import sys
import django
import datetime
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()

from scraping.models import Vacancy, Error
from scraping_service.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()

subject = '[noreply] Vacancy site notification [{}]'.format(today)
text_content = '[noreply] Vacancy site notification [{}]'.format(today)
from_email = EMAIL_HOST_USER
empty = '<h2> There are no actual vacancies today</h2>'

User = get_user_model()

qs = User.objects.filter(is_subscribed=True).values('city', 'language', 'email')
users_dict = {}
for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])
if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])

    qs = Vacancy.objects.filter(**params, timestamp=today).values()

    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)

    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(timestamp=today)
if qs.exists():
    error = qs.first()
    data = error.data
    content = ''
    for i in data:
        content += '<p><a href="{0}"> Error: {1} </a></p>'.format(i['url'], i['title'])

    subject = 'Scraping errors {0}'.format(today)
    text_content = 'Scraping errors {0}'.format(today)
    to = ADMIN_USER

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    msg.send()
