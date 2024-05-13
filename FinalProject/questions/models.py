from django.db import models
from quizes.models import Quiz
from projects.models import Lesson
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answer_set.all() 


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"
    

class IncorrectQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.user.username}, Quiz: {self.quiz.name}, Question: {self.question.text}"