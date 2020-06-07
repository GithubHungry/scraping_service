from django import forms

from .models import City, Language


class SearchForm(forms.Form):
    """Form for searching vacancies."""
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Vacancy city')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='Vacancy language')
