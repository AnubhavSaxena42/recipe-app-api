"""
Tests for the user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

"""The reverse function is used to get the url of the view by name"""
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

"""Helper function: To create a user in the database"""
def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        """Set up before the tests run"""
        """Client object to make requests"""
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is succesful"""
        """Payload Dummy data to post for user creation"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'testname'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        """This check is pretty self explanatory, checking if api ran succesfully"""
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])

        """This checks that the password of the created user is equal to the payload pass(validation object created)"""
        self.assertTrue(user.check_password(payload['password']))

        """To check that the password key is not present inside the response returned as user returned should
         never contain the hashed password"""
        self.assertNotIn('password', res.data)


    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'testuser'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short_error(self):
        """Test an error is returned if password is less than 5 characters"""

        payload = {
            'email': 'test@example.com',
            'password': 'test',
            'name': 'testuser'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email= payload['email']
        ).exists()

        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """Generates token for valid credentials"""

        user_details = {
            'name': 'testname',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        create_user(**user_details)

        payload = {
           'email': user_details['email'],
           'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_invalid_credentials(self):
        """Test create token if credentials are invalid"""

        user_details = {
            'name': 'testname',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': 'incorrectpassword'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_empty_password(self):
        """Tests create token API when a blank password is provided"""

        payload = {
            'email': 'test@example.com',
            'password': ''
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for the me endpoint."""

        res = self.client.get(ME_URL,)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(email="test@example.com",password="testpass123",name="testname")
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)


    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test post is not allowed for the me endpoint"""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user"""

        payload = {'name': 'Updated name','password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name,payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)



