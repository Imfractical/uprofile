"""users app URL configuration"""

from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<user_pk>/', views.profile, name='profile'),
]
