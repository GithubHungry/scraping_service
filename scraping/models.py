from django.db import models


# Create your models here.

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
