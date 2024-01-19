from typing import Any    #wasdas
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from cities_light.models import Country, City
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    birthdate = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date', 'format': 'dd-mm-yyyy'}),
    help_text="Format: TT-MM-JJJJ"
    )
    
    # die funktion muss "clean_"irgendwas heißen, weil isvalid bei einem formaufruf immer schaut,
    # ob ea eine clean_ method gibt, um daten zu bereinigen
    def clean_birthdate(self): 
        birthdate = self.cleaned_data.get('birthdate')
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if age < 18:
            raise forms.ValidationError("Wir (unter 18 Jahre alt) müssen draußen bleiben!")

        return birthdate

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('name', 'country', 'city', 'birthdate',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'z.B. icke@kikke.ma'}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'country', 'city']
    

class UpdateProfileForm(forms.ModelForm):
    # countries = Country.objects.all()
    # COUNTRIES = []
    # for c in countries:
    #     COUNTRIES.append((c.id, c))

    # cities = City.objects.all()
    # CITIES = []
    # for c in cities:
    #     CITIES.append((c.id, c.name))


    GENDER_CHOICES = [
        ('female', 'weiblich'),
        ('male', 'männlich'),
        ('divers', 'divers'),
    ]
    
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'z.B. 25'}), min_value=12, max_value=110, required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'placeholder': 'z.B. Berlin'}))
    # country = forms.ChoiceField(choices=COUNTRIES, widget=forms.Select(attrs={'class': 'form-control'}))
    # city = forms.ChoiceField(choices=CITIES, widget=forms.Select(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'z.B. Hi, ich muss mal..'}))
    interests = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'z.B. Halligalli, Semmeln, Löten'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'age', 'gender', 'location', 'bio', 'interests',]



