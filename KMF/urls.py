from django.contrib import admin
from django.urls import path
from KMF_app.views import home, login_view, register_step1, register_step2, register_step3, register_step4

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/step1/', register_step1, name='register_step1'),
    path('register/step2/', register_step2, name='register_step2'),
    path('register/step3/', register_step3, name='register_step3'),
    path('register/step4/', register_step4, name='register_step4'),
]