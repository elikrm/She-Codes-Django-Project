from django.urls import path, include
from .views import CreateAccountView, ViewProfile
from . import views

app_name = 'users'

urlpatterns = [
path('create-account/', CreateAccountView.as_view(),name='createAccount'),
path('profile-view/', views.ViewProfile.as_view(),name='Profile')
] 
