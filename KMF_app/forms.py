# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('phone_number', 'name', 'business_type', 'gender')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Ваша логика валидации для номера телефона
        if not phone_number.isnumeric():
            raise ValidationError("Phone number should contain only digits.")
        return phone_number

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Ваша логика валидации для имени
        if len(name) < 3:
            raise ValidationError("Name should be at least 3 characters long.")
        return name

    def clean_business_type(self):
        business_type = self.cleaned_data.get('business_type')
        # Ваша логика валидации для типа бизнеса
        return business_type

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        # Ваша логика валидации для пола
        return gender

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.name = self.cleaned_data['name']
        user.business_type = self.cleaned_data['business_type']
        user.gender = self.cleaned_data['gender']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'] = forms.EmailField(label='Email', required=True)


class RegistrationStep1Form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number']


class RegistrationStep2Form(forms.Form):
    sms_code = forms.CharField(max_length=6, required=True, help_text="Enter the code from SMS")


class RegistrationStep3Form(forms.ModelForm):
    GENDER_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),
    )
    BUSINESS_TYPE_CHOICES = (
        ('opt', 'Оптовый'),
        ('biz', 'Бизнес'),
        ('log', 'Логистика'),
    )
    business_type = forms.ChoiceField(
        choices=BUSINESS_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'business_type', 'gender']


class RegistrationStep4Form(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['password1', 'password2']