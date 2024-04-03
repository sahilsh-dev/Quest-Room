from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from ..models import QuestRoom, Message, RoomCode

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
    def setUp(self):
        self.user = User.objects.create_user('test', 'test')
    
    def test_authenticated_user_can_view_create_room(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rooms:create_room'))
        self.assertEqual(response.status_code, 200)
        
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('rooms:create_room'))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('rooms:create_room')}")
        
    def test_authenticated_user_can_create_room(self):
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
        self.assertEqual(self.user.created_rooms.count(), 1)
        self.assertEqual(self.user.created_rooms.first().name, 'Test Room')
        self.assertEqual(self.user.created_rooms.first().description, 'Test Description')
        self.assertEqual(self.user.created_rooms.first().expire_days, 10)
        self.assertEqual(self.user.created_rooms.first().created_by, self.user)
        self.assertEqual(self.user.created_rooms.first().daily_required_points, 1)
        self.assertLessEqual(
            self.user.created_rooms.first().expires_at, 
            timezone.now() + timezone.timedelta(days=10)
        )
        
    def test_invalid_form_submission(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('rooms:create_room'), {
                'name': 'Test Room', 
                'description': 'Test Description', 
                'expire_days': 0, 
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.created_rooms.count(), 0)
        
    def test_user_cannot_create_same_name_room(self):
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
        self.assertEqual(self.user.created_rooms.count(), 1)
        response = self.client.post(
            reverse('rooms:create_room'), {
                'name': 'Test Room', 
                'description': 'Test Description', 
                'expire_days': 10, 
                'room_type': QuestRoom.RoomType.LEETCODE, 
                'daily_required_points': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.created_rooms.count(), 1)
    
    def test_rooom_owner_is_added_to_members(self):
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
        self.assertEqual(self.user.created_rooms.count(), 1)
        self.assertEqual(self.user.created_rooms.first().members.count(), 1)
        self.assertEqual(self.user.created_rooms.first().members.first(), self.user)
    
    def test_room_owner_is_added_to_admins(self):
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
        room = QuestRoom.objects.get(name='Test Room')
        self.assertEqual(room.admins.count(), 1)
        self.assertEqual(room.admins.first(), self.user)
        

class RoomDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test')
        self.room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            created_by=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.room.members.add(self.user)
        
    def test_authenticated_user_can_view_room_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rooms:room_detail', args=[self.room.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(reverse('rooms:room_detail', args=[self.room.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('rooms:room_detail', args=[self.room.id])}")
        
    def test_room_does_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rooms:room_detail', args=[self.room.id + 1]))
        self.assertEqual(response.status_code, 404)
    
    def test_room_messages(self):
        self.client.force_login(self.user)
        message = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Test Message'
        )
        response = self.client.get(reverse('rooms:room_detail', args=[self.room.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['room'], self.room)
        self.assertEqual(response.context['latest_messages'].count(), 1)
        self.assertEqual(response.context['latest_messages'][0].room_id, self.room.id)
        
    def test_multiple_room_messages(self):
        self.client.force_login(self.user)
        message1 = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Test Message 1'
        )
        message2 = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Test Message 2'
        )
        response = self.client.get(reverse('rooms:room_detail', args=[self.room.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['room'], self.room)
        self.assertEqual(response.context['latest_messages'].count(), 2)
        self.assertEqual(response.context['latest_messages'][0].room_id, self.room.id)
        self.assertEqual(response.context['latest_messages'][1].room_id, self.room.id)

    def test_non_member_cannot_view_room(self):
        user2 = User.objects.create_user('test2', 'test2')
        self.client.force_login(user2)
        response = self.client.get(reverse('rooms:room_detail', args=[self.room.id]))
        self.assertEqual(response.status_code, 403)


class GenerateRoomCodeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test')
        self.room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            created_by=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.room.members.add(self.user)
        self.room.admins.add(self.user)

    def test_authenticated_user_can_generate_room_code(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('rooms:generate_room_code', args=[self.room.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RoomCode.objects.count(), 1)
        self.assertEqual(RoomCode.objects.first().room, self.room)
        self.assertEqual(RoomCode.objects.first().generated_by, self.user)
        self.assertTrue(RoomCode.objects.first().is_valid())
        self.assertEqual(len(RoomCode.objects.first().code), settings.ROOM_INVITE_CODE_LENGTH)
        
    def test_redirects_unauthenticated_user(self):
        response = self.client.post(reverse('rooms:generate_room_code', args=[self.room.id]))
        self.assertRedirects(
            response, 
            f"{reverse('users:login')}?next={reverse('rooms:generate_room_code', args=[self.room.id])}"
        )

    def test_non_admins_are_redirected(self):
        user2 = User.objects.create_user('test2', 'test2')
        self.client.force_login(user2)
        response = self.client.post(reverse('rooms:generate_room_code', args=[self.room.id]))
        self.assertEqual(response.status_code, 302)


class JoinRoomViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test')
        self.room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            created_by=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.room.members.add(self.user)
        self.room.admins.add(self.user)
        self.room_code = RoomCode.objects.create(room=self.room, code='TESTCODE', generated_by=self.user)
        self.url = reverse('rooms:join_room')

    def test_join_room_not_logged_in(self):
        response = self.client.post(self.url, {'room_code': 'TESTCODE'})
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_join_room_invalid_code(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {'room_code': 'INVALIDCODE'})
        self.assertEqual(response.status_code, 302)  # Redirects to 'rooms:view_rooms'

    def test_join_room_success(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {'room_code': 'TESTCODE'})
        self.assertEqual(response.status_code, 302)  # Redirects to 'rooms:room_detail'
        self.assertTrue(self.room.members.filter(id=self.user.id).exists())
