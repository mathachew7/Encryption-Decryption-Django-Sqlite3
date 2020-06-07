from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('encrypt.html', views.encrypt, name='encrypt'),
    path('decrypt.html', views.decrypt, name='decrypt'),
    path('profile.html', views.profile, name='profile'),
    path('login.html', views.login, name='login'),
    path('register.html', views.register, name='register'),
    path('logout', views.logout, name="logout")
]
