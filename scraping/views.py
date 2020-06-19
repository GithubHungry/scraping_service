from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Vacancy
from .forms import SearchForm, VacancyForm


# Create your views here.
def index(request):
    form = SearchForm()

    return render(request, 'scraping/index.html', {'form': form})


# def list_view(request):
#     form = SearchForm()
#     city = request.GET.get('city')
#     language = request.GET.get('language')
#     page_obj = []
#     context = {'city': city, 'language': language, 'form': form}
#
#     if city or language:
#         _filter = {}
#         if city:
#             _filter['city__slug'] = city
#         if language:
#             _filter['language__slug'] = language
#
#         vacancies = Vacancy.objects.filter(**_filter)
#         paginator = Paginator(vacancies, 10)  # Show 25 contacts per page.
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#     context['object_list'] = page_obj
#
#     return render(request, 'scraping/list.html', context)


# def v_detail(request, pk=None):
# vac = Vacancy.objects.get(pk=pk)
# vac = get_object_or_404(Vacancy, pk=pk)
# return render(request, 'scraping/detail.html', {'object': vac})


class VacancyDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraping/detail.html'
    context_object_name = 'object'


class VacancyList(ListView):
    model = Vacancy
    template_name = 'scraping/list.html'
    form = SearchForm()
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        vacancies = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            vacancies = Vacancy.objects.filter(**_filter)
        return vacancies


class VacancyCreate(CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('index')


class VacancyUpdate(UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('index')
