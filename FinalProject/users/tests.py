from django.test import TestCase
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from users.models import Profile
from django.urls import reverse

class UserRegistrationTest(TestCase):
    # Test Case to check that registration can be successfull with correct input data
    def test_user_registration_success(self):
        data = {
            'first_name': 'Ben', 
            'email': 'ben@gmail.com', 
            'username': 'Ben', 
            'password1': 'Serych123', 
            'password2': 'Serych123'
        }
        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())
        # Simulate a user registration request with valid data
        response = self.client.post(reverse('register'), data)
        
        # Assert that the registration was successful (HTTP status code 302 for redirect)
        self.assertEqual(response.status_code, 302)
        
        # Assert that the user was created in the database
        self.assertTrue(User.objects.filter(username='Ben').exists())

    #Test Case that registration will not be successful with no username
    def test_user_registration_no_username(self):
        data = {
            'first_name': 'Ben', 
            'email': 'ben@gmail.com', 
            'username': '', 
            'password1': 'Serych123', 
            'password2': 'Serych123'
        }
        response = self.client.post(reverse('register'), data)

        # Assert that the registration failed (HTTP status code 200 for success)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the user was not created in the database
        self.assertFalse(User.objects.filter(username='').exists())

    #Test Case that registration will not be successful with non-matching passwords
    def test_user_registration_passwords_not_match(self):
        data = {
            'first_name': 'Ben', 
            'email': 'ben@gmail.com', 
            'username': 'Ben', 
            'password1': 'Serych123', 
            'password2': 'Serych456'
        }
        response = self.client.post(reverse('register'), data)

        # Assert that the registration failed (HTTP status code 200 for success)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the user was not created in the database
        self.assertFalse(User.objects.filter(username='Ben').exists())


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='Serych123')

    # Test case to check that user can be authenticated with the correct data
    def test_user_login_success(self):
        data = {
            'username': 'testuser', 
            'password': 'Serych123' 
        }

        response = self.client.post(reverse('login'), data, follow=True)
        #Assert that login was successful
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_login_invalid_data(self):
        data = {
            'username': 'testuser',
            'password': 'Incorrect123'
        }
        response = self.client.post(reverse('login'), data, follow=True)
        #Assert that login failed and user was not authenticated
        self.assertFalse(response.context['user'].is_authenticated)

    # Test case to check that user can log out
    def test_user_logout(self):
        # Log in the user before logging out
        self.client.login(username='testuser', password='Serych123')
        
        # Perform logout
        response = self.client.get(reverse('logout'), follow=True)
        
        # Assert that the user is logged out
        self.assertFalse(response.context['user'].is_authenticated)


class UserProfileCreationTest(TestCase):
    def test_profile_creation_on_registration(self):
        data = {
            'first_name': 'Milena', 
            'email': 'milena@gmail.com', 
            'username': 'milena_ser', 
            'password1': 'Serych123', 
            'password2': 'Serych123'
        }
        response = self.client.post(reverse('register'), data, follow=True)
        # Check if the user's profile was created
        user = User.objects.get(username='milena_ser')
        self.assertTrue(Profile.objects.filter(user=user).exists())
