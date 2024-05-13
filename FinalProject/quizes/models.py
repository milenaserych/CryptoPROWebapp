from django.db import models
from projects.models import Project

# Create your models here.

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard')
)

class Quiz(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='quizzes', default='8fd8d246-8b97-439b-8291-9f85fb156483')
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    max_points = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    def get_questions(self):
        return self.question_set.all()[:self.number_of_questions]
    
    def calculate_max_score(self):
        if self.difficulty == 'easy':
            return self.max_points
        elif self.difficulty == 'medium':
            return self.max_points * 2
        elif self.difficulty == 'hard':
            return self.max_points * 3
        
    def save(self, *args, **kwargs):
        # Calculate and set max_score before saving the object
        self.max_score = self.calculate_max_score()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Quizes'