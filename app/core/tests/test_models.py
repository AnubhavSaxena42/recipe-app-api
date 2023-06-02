""""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email_succesful(self):
        """Test creating user with an email is succesful"""

        email = "test@example.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""

        sample_emails = [
            ["test1@examplE.com","test1@example.com"],
            ["Test2@eXAMPLE.com","Test2@example.com"],
            ["test3@example.com","test3@example.com"],
        ]

        for email,expected in sample_emails:
            user=get_user_model().objects.create_user(
                email=email,
                password="sample123"
            )
            self.assertEqual(user.email,expected)


    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','password123')


    def test_create_superuser(self):
        """Test creating a super user"""

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)