from django.shortcuts import render

from .models import Vacancy
from .forms import SearchForm


# Create your views here.
def index(request):
    form = SearchForm()

    return render(request, 'scraping/index.html', {'form': form})


def list_view(request):
    form = SearchForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    vacancies = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        vacancies = Vacancy.objects.filter(**_filter)

    return render(request, 'scraping/list.html', {'object_list': vacancies, 'form': form})

