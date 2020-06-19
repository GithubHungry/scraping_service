from django import forms

from .models import City, Language, Vacancy


class SearchForm(forms.Form):
    """Form for searching vacancies."""
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Vacancy city')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='Vacancy language')


class VacancyForm(forms.ModelForm):
    """Form for customize vacancies form."""
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Vacancy city')
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='Vacancy language')
    url = forms.CharField(label='URL', widget=forms.URLInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    company = forms.CharField(label='Company', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancy
        fields = '__all__'
