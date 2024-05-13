from django.db import models
from quizes.models import Quiz
from users.models import Profile
from django.contrib.auth.models import User

# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def calculate_points_of_progress(self):
        # Check if the user passed the quiz
        if hasattr(self.user, 'profile'):
            if self.score >= self.quiz.required_score_to_pass:
                # Calculate the user's points_of_progress based on user's result
                points_earned = round(self.score * self.quiz.calculate_max_score()/100)
                print("Points earned: ", points_earned)

                # Get the user's results for the quiz
                results = Result.objects.filter(user=self.user, quiz=self.quiz).exclude(pk=self.pk).order_by('-score')
                print("Results length: ", len(results))
                if len(results) == 0:
                    # Update the user's points_of_progress for the first attempt
                    self.user.profile.points_of_progress += points_earned
                    self.user.profile.save()
                    print("Updated points_of_progress for the first attempt.")
                else:
                    # Get the best result (excluding the current one)
                    best_result = results.first()
                    print("Best result: ", best_result)
                    # Check if the best result is less than the maximum possible score
                    if self.score > best_result.score:
                        # Calculate the difference between the current result and the best result
                        difference = round((self.score - best_result.score) * self.quiz.calculate_max_score()/100)
                        print("Difference: ", difference)
                        # Update the user's points_of_progress
                        self.user.profile.points_of_progress += difference
                        self.user.profile.save()
                        print("Updated points_of_progress based on improvement.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Calculate and update points_of_progress after saving the results
        self.calculate_points_of_progress()

    def __str__(self):
        return f"Result {self.pk} - User: {self.user.username}, Score: {self.score}"
    

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score_of_progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score_of_progress}"
    