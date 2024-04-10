from django.urls import path
from . import views

app_name = 'rooms'
urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.view_rooms, name='view_rooms'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/join/', views.join_room, name='join_room'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/code/', views.generate_roomcode, name='generate_room_code'),
    path('rooms/<int:room_id>/make_admin/', views.make_room_member_admin, name='make_room_member_admin'),
    path('rooms/<int:room_id>/remove_member/', views.remove_room_member, name='remove_room_member'),
    path('rooms/<int:room_id>/update_score/', views.update_room_score, name='update_room_score'),
    path('rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),
]
