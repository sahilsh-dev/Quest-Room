from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import QuestRoom

User = get_user_model()


class QuestRoomModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test')

    def test_creator_is_created_by(self):
        room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            created_by=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.assertEqual(room.created_by, self.user)
        
    def test_room_expires_at(self):
        room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            created_by=self.user,
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
            created_by=self.user,
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
            created_by=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.assertEqual(room.room_type, QuestRoom.RoomType.LEETCODE)
        
    def test_user_cannot_create_same_name_room(self):
        room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            created_by=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        with self.assertRaises(Exception):
            room2 = QuestRoom.objects.create(
                name='Test Room', 
                description='Test Description', 
                expire_days=10, 
                room_type=QuestRoom.RoomType.LEETCODE, 
                daily_required_points=1,
                created_by=self.user,
                expires_at = timezone.now() + timezone.timedelta(days=10)
            )
            
    def test_diff_user_can_create_same_name_room(self):
        room = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            created_by=self.user,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        user2 = User.objects.create_user('test2', 'test2')
        room2 = QuestRoom.objects.create(
            name='Test Room', 
            description='Test Description', 
            expire_days=10, 
            room_type=QuestRoom.RoomType.LEETCODE, 
            daily_required_points=1,
            created_by=user2,
            expires_at = timezone.now() + timezone.timedelta(days=10)
        )
        self.assertEqual(self.user.rooms.count(), 1)
        self.assertEqual(user2.rooms.count(), 1)
        