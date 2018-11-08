from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<user_pk>/', views.view_profile, name='view_profile'),
    path('<user_pk>/edit/', views.edit_profile, name='edit_profile')
]
