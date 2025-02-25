from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import Food_Entry
from django.core.validators import MinValueValidator , MaxValueValidator


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password',
                                                              'type': 'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'
                                                              , 'type': 'password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password',
                                                             'type': 'password'}))


class WeightLogForm(forms.Form):
    weight = forms.IntegerField(
        label="Weight (kg)",
        validators=[
            MinValueValidator(1, message="Weight must be a positive integer."),
            MaxValueValidator(999, message="Weight cannot exceed 999 kg.")  # Adjust the max value as needed
        ],
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter your weight in kg',
            'class': 'form-control',
            'maxlength': '3'  # Limits input length at the HTML level
        })
    )


class DateInput(forms.DateInput):
    input_type = 'date'

class FoodForm(forms.Form):
    date = forms.DateField(widget=DateInput, initial=timezone.now) #^[a-zA-Z0-9]([\w .]*[a-zA-Z0-9])+$
    description = forms.CharField(label="Description", max_length=31, validators=[RegexValidator('^[\w .,()+-]+$', message='Description must be alphanumeric', code='invalid_desc')])
    calories = forms.IntegerField(label="Calories")

class FoodFormTheSecond(forms.Form):
    date = forms.DateField(widget=DateInput, initial=timezone.now)
    description = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(FoodFormTheSecond, self).__init__(*args, **kwargs)
        self.fields['description'].choices = Food_Entry.objects.filter(user=self.request.user).order_by('description').values_list("description", "description").distinct()

