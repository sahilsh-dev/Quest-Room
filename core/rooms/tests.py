from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from .models import QuestRoom

User = get_user_model()

class HomeViewTests(TestCase):
    def test_unauthenticated_user_can_view_home(self):
        response = self.client.get(reverse('rooms:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_redirects_authenticated_user(self):
        self.user = User.objects.create_user('test', 'test')
        self.client.force_login(self.user)
        response = self.client.get(reverse('rooms:home'))
        self.assertRedirects(response, reverse('rooms:view_rooms'))
        
    
class ViewRoomsViewTests(TestCase):
    def test_authenticated_user_can_view_rooms(self):
        self.user = User.objects.create_user('test', 'test')
        self.client.force_login(self.user)
        response = self.client.get(reverse('rooms:view_rooms'))
        self.assertEqual(response.status_code, 200)

    def test_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('rooms:view_rooms'))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('rooms:view_rooms')}")
    

class CreateRoomViewTests(TestCase):
    def test_authenticated_user_can_view_create_room(self):
        self.user = User.objects.create_user('test', 'test')
        self.client.force_login(self.user)
        response = self.client.get(reverse('rooms:create_room'))
        self.assertEqual(response.status_code, 200)
        
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('rooms:create_room'))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('rooms:create_room')}")
        
    def test_authenticated_user_can_create_room(self):
        self.user = User.objects.create_user('test', 'test')
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('rooms:create_room'), {
                'name': 'Test Room', 
                'description': 'Test Description', 
                'expire_days': 10, 
                'room_type': QuestRoom.RoomType.LEETCODE, 
                'daily_required_points': 1
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.rooms.count(), 1)
        self.assertEqual(self.user.rooms.first().name, 'Test Room')
        self.assertEqual(self.user.rooms.first().description, 'Test Description')
        self.assertEqual(self.user.rooms.first().expire_days, 10)
        self.assertEqual(self.user.rooms.first().head, self.user)
        self.assertEqual(self.user.rooms.first().daily_required_points, 1)
        self.assertLessEqual(
            self.user.rooms.first().expires_at, 
            timezone.now() + timezone.timedelta(days=10)
        )
        
    def test_invalid_form_submission(self):
        self.user = User.objects.create_user('test', 'test')
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('rooms:create_room'), {
                'name': 'Test Room', 
                'description': 'Test Description', 
                'expire_days': 0, 
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.rooms.count(), 0)
    

class QuestRoomModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test')

    def test_creator_is_head(self):
        room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            head=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.assertEqual(room.head, self.user)
        
    def test_room_expires_at(self):
        room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            head=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.assertLessEqual(room.expires_at, timezone.now() + timezone.timedelta(days=10))
        
    def test_room_members(self):
        room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            head=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.assertEqual(room.members.count(), 0)
        room.members.add(self.user)
        self.assertEqual(room.members.count(), 1)
        self.assertEqual(room.members.first(), self.user)
        room.members.remove(self.user)
        self.assertEqual(room.members.count(), 0)
        
    def test_room_type(self):
        room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            head=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.assertEqual(room.room_type, QuestRoom.RoomType.LEETCODE)
        