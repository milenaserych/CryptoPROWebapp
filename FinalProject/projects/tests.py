from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Lesson, Project

class AdminButtonVisibilityTestCase(TestCase):
    def setUp(self):
        # Create a regular user
        self.regular_user = User.objects.create_user(username='regularuser', password='Serych123')

        # Create a superuser/admin
        self.superuser = User.objects.create_superuser(username='admin', password='Superuser123')

        # URL for the projects page
        self.projects_url = reverse('projects:projects')

    def test_add_module_button_visibility(self):
        # Regular user does not have access to this button
        self.client.login(username='regularuser', password='Serych123')
        response = self.client.get(self.projects_url)
        self.assertNotContains(response, 'Add Module')

        # Admin does have access to this button
        self.client.login(username='admin', password='Superuser123')
        response=self.client.get(self.projects_url)
        self.assertContains(response, 'Add Module')


class ProjectCreationTestCase(TestCase):
    def setUp(self):
        # Create a superuser/admin
        self.superuser = User.objects.create_superuser(username='admin', password='Superuser123')

        # URL for creating a project
        self.create_project_url = reverse('projects:create-project')

    def test_project_creation(self):

        self.client.login(username='admin', password='Superuser123')

        # Data for creating a project
        project_data = {
            'title': 'Test Project',
            'description': 'This is a test project.'
        }

        # Post request to create a project
        response = self.client.post(self.create_project_url, project_data)

        # Check if the project was created successfully
        self.assertEqual(response.status_code, 302) # Should redirect back to the projects page after successful creation

        #Check if the project appears on the projects page
        projects_page_url = reverse('projects:projects')
        response = self.client.get(projects_page_url)
        self.assertContains(response, 'Test Project')


class UpdateProjectTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        
        # Create a project
        self.project = Project.objects.create(title='Test Project', description='This is a test project.')

    def test_update_project(self):
        # Log in as the superuser
        self.client.login(username='admin', password='adminpassword')
        
        # Define updated data for the project
        updated_data = {
            'title': 'Updated Test Project',
            'description': 'This is the updated test project description.'
        }
        
        # Make a POST request to update the project
        response = self.client.post(reverse('projects:update-project', args=[self.project.pk]), updated_data, follow=True)
        
        # Assert that the project is updated successfully
        self.assertEqual(response.status_code, 200)
        
        # Check if the project is updated in the database
        updated_project = Project.objects.get(pk=self.project.pk)
        self.assertEqual(updated_project.title, 'Updated Test Project')
        self.assertEqual(updated_project.description, 'This is the updated test project description.')

class DeleteProjectTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        
        # Create a project
        self.project = Project.objects.create(title='Test Project', description='This is a test project.')

    def test_delete_project(self):
        # Log in as the superuser
        self.client.login(username='admin', password='adminpassword')
        
        # Make a POST request to delete the project
        response = self.client.post(reverse('projects:delete-project', args=[self.project.pk]), follow=True)
        
        # Assert that the project is deleted successfully
        self.assertEqual(response.status_code, 200)
        
        # Check if the project is deleted from the database
        project_exists = Project.objects.filter(pk=self.project.pk).exists()
        self.assertFalse(project_exists)

class LessonCreationTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(username='superuser', password='testpassword')
        
        # Create a project
        self.project = Project.objects.create(title='Test Project', description='This is a test project.')
        
        # URL for creating a lesson
        self.create_lesson_url = reverse('projects:create-lesson')
        
    def test_lesson_creation(self):
        # Log in as the superuser
        self.client.login(username='superuser', password='testpassword')
        
        # Data for creating a lesson
        lesson_data = {
            'project': self.project.id,
            'title': 'Test Lesson',
            'content': 'This is a test lesson content.',
            'number': 1  # Assuming lessons are numbered sequentially
        }
        
        # Post request to create a lesson
        response = self.client.post(self.create_lesson_url, lesson_data)
        
        # Check if the lesson was created successfully
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        
        # Check if the lesson exists in the database
        lesson_exists = Lesson.objects.filter(title='Test Lesson').exists()
        self.assertTrue(lesson_exists)  # Check if the lesson exists in the database