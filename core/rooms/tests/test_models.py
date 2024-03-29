from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import QuestRoom, Message, RoomCode

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
        self.assertEqual(self.user.created_rooms.count(), 1)
        self.assertEqual(user2.created_rooms.count(), 1)
        

class MessageModelTests(TestCase):
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
        
    def test_message(self):
        message = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Test Message'
        )
        self.assertEqual(message.room, self.room)
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.content, 'Test Message')
        self.assertLessEqual(message.created_at, timezone.now())
        
    def test_latest_messages(self):
        message = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Test Message 1'
        )
        message2 = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Test Message 2'
        )
        latest_messages = Message.latest_messages.get_latest_messages(self.room.id)
        self.assertEqual(latest_messages.count(), 2)
        self.assertEqual(latest_messages[0], message2)
        self.assertEqual(latest_messages[1], message)
        self.assertEqual(latest_messages[0].content, 'Test Message 2')
        self.assertEqual(latest_messages[1].content, 'Test Message 1')


class RoomCodeModelTests(TestCase):
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
        
    def test_room_code(self):
        room_code = RoomCode.objects.create(
            code='TESTCODE',
            room=self.room,
            generated_by=self.user
        )
        self.assertEqual(room_code.code, 'TESTCODE')
        self.assertEqual(room_code.room, self.room)
        self.assertEqual(room_code.generated_by, self.user)
        self.assertLessEqual(room_code.created_at, timezone.now())
        
    def test_room_code_is_valid(self):
        room_code = RoomCode.objects.create(
            code='TESTCODE',
            room=self.room,
            generated_by=self.user
        )
        self.assertTrue(room_code.is_valid())
        
    def test_room_code_is_invalid(self):
        room_code = RoomCode.objects.create(
            code='TESTCODE',
            room=self.room,
            generated_by=self.user
        )
        room_code.created_at = timezone.now() - timezone.timedelta(days=11)
        room_code.save()
        self.assertFalse(room_code.is_valid())
        
    def test_room_code_unique(self):
        room_code = RoomCode.objects.create(
            code='TESTCODE',
            room=self.room,
            generated_by=self.user
        )
        with self.assertRaises(Exception):
            room_code2 = RoomCode.objects.create(
                code='TESTCODE',
                room=self.room,
                generated_by=self.user
            )
            
    def test_room_code_unique(self):
        room_code = RoomCode.objects.create(
            code='TESTCODE',
            room=self.room,
            generated_by=self.user
        )
        room_code2 = RoomCode.objects.create(
            code='TESTCODE2',
            room=self.room,
            generated_by=self.user
        )
        self.assertEqual(self.room.codes.count(), 2)
        self.assertEqual(self.room.codes.first(), room_code)
        self.assertEqual(self.room.codes.last(), room_code2)
        self.assertEqual(self.room.codes.first().code, 'TESTCODE')
        self.assertEqual(self.room.codes.last().code, 'TESTCODE2')