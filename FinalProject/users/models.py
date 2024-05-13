from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from projects.models import Project
from questions.models import IncorrectQuestion
import uuid


class Profile(models.Model):
    #Create one-to-one relationship between the user Profile and prebuilt Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default="profiles/defaultprofile.jpeg")
    created = models.DateTimeField(auto_now_add=True)
    points_of_progress = models.IntegerField(default=0)
    current_module = models.CharField(max_length=200, blank=True, null=True)
    current_quiz = models.CharField(max_length=200, blank=True, null=True)
    modules_completed = models.IntegerField(default=0)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.user.username}"
    
    def get_incorrect_questions(self):
        incorrect_questions = IncorrectQuestion.objects.filter(user=self.user)
        return incorrect_questions
    
    def get_most_frequent_incorrect_questions(self, num_questions=2):
        incorrect_questions = self.get_incorrect_questions()
        print("Incorrect questions: ", incorrect_questions)
        most_frequent_questions = (
            incorrect_questions
            .values('question__text', 'question__lesson__title')
            .annotate(frequency=Count('question'))
            .order_by('-frequency')[:num_questions]
        )
        return most_frequent_questions
    
    def save(self, *args, **kwargs):
        if not self.name and self.user:
            self.name = self.user.first_name
        super().save(*args, **kwargs)




