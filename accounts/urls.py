from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/<int:user_pk>', views.profile, name='profile'),
]
