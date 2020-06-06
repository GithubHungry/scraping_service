from django.shortcuts import render
from .models import Vacancy


# Create your views here.
def index(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'scraping/index.html', {'object_list': vacancies})
