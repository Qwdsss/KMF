from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, RegistrationStep1Form, RegistrationStep2Form, RegistrationStep3Form, RegistrationStep4Form
from KMF_app.models import CustomUser
import logging


logger = logging.getLogger(__name__)

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register_step1.html', {'form': form})


# Функция отображения главной страницы
def home(request):
    # Получаем имя пользователя, если он аутентифицирован
    user_name = request.user.name if request.user.is_authenticated else None

    # Обработка выхода пользователя
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)

    return render(request, 'home.html', {'user_name': user_name})


# Шаг 1 регистрации: ввод email и номера телефона
def register_step1(request):
    if request.method == 'POST':
        form = RegistrationStep1Form(request.POST)
        if form.is_valid():
            # Сохраняем данные в сессии
            request.session['registration_data'] = {
                'email': form.cleaned_data['email'],
                'phone_number': form.cleaned_data['phone_number'],
            }
            return redirect('register_step2')
    else:
        form = RegistrationStep1Form()
    return render(request, 'registration/register_step1.html', {'form': form})


# Шаг 2 регистрации: ввод кода из SMS
def register_step2(request):
    if request.method == 'POST':
        form = RegistrationStep2Form(request.POST)
        if form.is_valid():
            # Проверка введенного SMS кода
            if form.cleaned_data['sms_code'] == '123456':
                return redirect('register_step3')
            else:
                form.add_error('sms_code', 'Invalid SMS code. Please try again.')

    else:
        form = RegistrationStep2Form()

    return render(request, 'registration/register_step2.html', {'form': form})


# Шаг 3 регистрации: ввод имени, типа бизнеса и пола
def register_step3(request):
    if request.method == 'POST':
        form = RegistrationStep3Form(request.POST)
        if form.is_valid():
            # Обновляем данные в сессии
            registration_data = request.session.get('registration_data', {})
            registration_data.update({
                'name': form.cleaned_data.get('name'),
                'business_type': form.cleaned_data.get('business_type'),
                'gender': form.cleaned_data.get('gender'),
            })
            print(form.cleaned_data)
            request.session['registration_data'] = registration_data
            return redirect('register_step4')
    else:
        form = RegistrationStep3Form()

    return render(request, 'registration/register_step3.html', {'form': form})


# Шаг 4 регистрации: ввод пароля
def register_step4(request):
    # Выводим данные из сессии в консоль (для отладки)
    if 'registration_data' in request.session:
        print(request.session['registration_data'])

    if request.method == 'POST':
        form = RegistrationStep4Form(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            confirm_password = form.cleaned_data['password2']

            # Создаем пользователя и аутентифицируем его
            if password == confirm_password:
                user = CustomUser.objects.create_user(
                    username=request.session['registration_data']['email'],
                    email=request.session['registration_data']['email'],
                    password=password,
                    phone_number=request.session['registration_data']['phone_number'],
                    name=request.session['registration_data'].get('name'),
                    business_type=request.session['registration_data'].get('business_type'),
                    gender=request.session['registration_data'].get('gender')
                )

                login(request, user)
                # Сохраняем данные в сессии перед удалением
                registration_data = request.session.pop('registration_data', None)
                # Проверяем сохраненные данные
                print('Data after creating user:', registration_data)

                return redirect('home')
            else:
                form.add_error('password2', 'Passwords do not match.')
    else:
        form = RegistrationStep4Form()

    return render(request, 'registration/register_step4.html', {'form': form})


# Вход пользователя
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
