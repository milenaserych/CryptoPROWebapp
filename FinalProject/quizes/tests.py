from django.test import TestCase
from django.urls import reverse
from .models import Quiz
from questions.models import Question, Answer
from projects.models import Project, Lesson
from django.contrib.auth.models import User



class QuizCreationTestCase(TestCase):
    def setUp(self):

        # Create a superuser/admin
        self.superuser = User.objects.create_superuser(username='admin', password='Superuser123')

         # Create a project
        self.project = Project.objects.create(title='Test Project', description='This is a test project.')


    def test_create_quiz(self):
        quiz_data = {
            'project': self.project.id,
            'name': 'Test Quiz',
            'topic': 'Test Topic',
            'number_of_questions': 3,
            'time': 10,
            'required_score_to_pass': 70,
            'difficulty': 'easy',
        }
        self.client.login(username='admin', password='Superuser123')
        #Test creating a quiz
        response = self.client.post(reverse('quizes:create-quiz'), quiz_data, follow=True)
        # Check if redirecting after successful quiz creation
        self.assertEqual(response.status_code, 200)
        
        
        # Check if quiz is created
        quiz_exists = Quiz.objects.filter(name='Test Quiz').exists()
        self.assertTrue(quiz_exists)

    
