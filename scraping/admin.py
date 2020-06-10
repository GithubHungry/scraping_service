from django.contrib import admin

from .models import City, Language, Vacancy, Url, Error


# Register your models here.

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # auto generate slug for City


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # auto generate slug for Language


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    pass


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    pass


admin.site.site_title = "Jobs scraper"
admin.site.site_header = "Jobs scraper"
