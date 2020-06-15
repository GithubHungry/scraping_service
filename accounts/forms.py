from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Wrong email, user does not exist!')
            if not check_password(password, qs[0].password):
                raise ValueError('Wrong password!')
            user = authenticate(email=email, password=password)
            if not user:
                raise ValueError('This account is not active!')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Enter email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Enter pass', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_2 = forms.CharField(label='Repeat pass', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)  # password as a default

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError('Passwords not equal!')
        return data['password_2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Vacancy city')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=True,
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='Vacancy language')
    is_subscribed = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='is_subscribed')

    class Meta:
        model = User
        fields = ('city', 'language', 'is_subscribed')


class ContactForm(forms.Form):
    pass
