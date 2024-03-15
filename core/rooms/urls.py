from django.urls import path
from . import views

app_name = 'rooms'
urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.view_rooms, name='view_rooms'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/<int:room_id>/', views.view_room, name='view_room'),
]