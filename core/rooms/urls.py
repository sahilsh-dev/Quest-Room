from django.urls import path
from . import views

app_name = 'rooms'
urlpatterns = [
    path('', views.home, name='home'),
]