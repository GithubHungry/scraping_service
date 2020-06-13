from django.shortcuts import render
from django.core.paginator import Paginator

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
    page_obj = []
    context = {'city': city, 'language': language, 'form': form}

    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        vacancies = Vacancy.objects.filter(**_filter)
        paginator = Paginator(vacancies, 10)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj

    return render(request, 'scraping/list.html', context)
