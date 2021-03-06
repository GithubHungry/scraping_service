import jsonfield
from django.db import models


# Create your models here.

def default_urls():
    return {'trudbox': '', 'work': ''}


class City(models.Model):
    name = models.CharField('City name', max_length=225, unique=True)
    slug = models.SlugField('City slug', max_length=225, blank=True, unique=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField('Language name', max_length=225, unique=True)
    slug = models.SlugField('Language slug', max_length=225, blank=True, unique=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField('Vacancy title', max_length=250)
    company = models.CharField('Vacancy company', max_length=250)
    description = models.TextField('Vacancy description')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Vacancy city', related_name='vacancies')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Vacancy language')
    timestamp = models.DateField(auto_now_add=True)
    url = models.URLField('Vacancy url', unique=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Url city')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='Url language')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language',)

    def __str__(self):
        return '{0} - {1}'.format(self.city, self.language)


class Error(models.Model):
    data = jsonfield.JSONField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp)
