from django.test import TestCase
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserSerializer

class UserRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'nurl8n@example.com',
            'first_name': 'random',
            'last_name': 'random',
            'password': 'zaq'
        }
        self.invalid_data = {
            'email': '',
            'first_name': 'nurl8n',
            'last_name': 'random',
            'password': '123'
        }
        self.existing_user = CustomUser.objects.create(
            email='iwillbesenior@gmail.com',
            first_name='oneday',
            last_name='or',
            password='dayone'
        )

    def test_valid_data(self):
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, self.valid_data)

    def test_missing_email(self):
        serializer = UserRegistrationSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('error', serializer.errors)
        self.assertEqual(serializer.errors['error'], "Email not found")

    def test_existing_email(self):
        data = self.valid_data.copy()
        data['email'] = 'existing@example.com'
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('error', serializer.errors)
        self.assertEqual(serializer.errors['error'], "Email already exists")

    def test_create_user(self):
        serializer = UserRegistrationSerializer(data=self.valid_data)
        serializer.is_valid()
        user = serializer.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertTrue(user.check_password(self.valid_data['password']))
