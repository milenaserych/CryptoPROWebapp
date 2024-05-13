from django.shortcuts import render
from results.models import Result, Leaderboard
from users.models import Profile
from django.contrib.auth.models import User


def update_leaderboard(user):
    try:
        profile = Profile.objects.get(user=user)
        total_points = profile.points_of_progress

        leaderboard, created = Leaderboard.objects.get_or_create(user=user)
        leaderboard.score_of_progress = total_points
        leaderboard.save()

        print(f"Leaderboard updated successfully for {user.username}. Total points: {total_points}")
    except Exception as e:
        print(f"An error occurred while updating leaderboard: {e}")


def leaderboard(request):
    # Retrieve leaderboard data (example: top 10 highest scores)
    leaderboard_data = Leaderboard.objects.order_by('-score_of_progress')[:10]
    return render(request, 'quizes/leaderboard.html', {'leaderboard_data': leaderboard_data})

