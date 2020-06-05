from django.contrib import admin

from .models import City, Language


# Register your models here.

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # auto generate slug for City


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # auto generate slug for Language


admin.site.site_title = "Jobs scraper"
admin.site.site_header = "Jobs scraper"
