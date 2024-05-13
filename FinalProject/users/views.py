from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from .models import Profile
from .forms import CustomUserCreationForm, UpdateProfile, ProfilePictureForm
from results.views import update_leaderboard

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('projects:projects')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Check that this user exists
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) # Create the session for the user in the db and in browser's cookies
            return redirect('projects:projects')
        else:
            messages.error(request, 'Username OR Password does not exist')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request, 'User was successfully logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()

            login(request, user)

            update_leaderboard(request.user) 
            return redirect('projects:projects')
        
        
        else:
            messages.error(request, 'An error has occurred during registration.')
        
    context = {
        'page':page,
        'form':form,
    }
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles' : profiles,
    }
    return render(request, 'users/profiles.html', context)

# def userProfile(request, pk):
#     try:
#         profile = Profile.objects.get(id=pk)
#     except Profile.DoesNotExist:
#         raise Http404("Profile not found")
#     return render(request, 'users/user-profile.html', {'profile': profile})

@login_required
def userProfile(request):
    profile = get_object_or_404(Profile, user=request.user)
    most_frequent_questions = profile.get_most_frequent_incorrect_questions()

    lessons_for_revision_set = set()
    for question in most_frequent_questions:
        if 'question__lesson__title' in question and question['question__lesson__title']:
            lessons_for_revision_set.add(question['question__lesson__title'])

    lessons_for_revision = list(lessons_for_revision_set)

    print("Lessons for revision: ", lessons_for_revision)
    return render(request, 'users/user-profile.html', {'profile': profile, 'lessons_for_revision':lessons_for_revision})


@login_required
def adminUserProfile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    most_frequent_questions = profile.get_most_frequent_incorrect_questions()
    lessons_for_revision = [
        question['question__lesson__title']
        for question in most_frequent_questions
        if 'question__lesson__title' in question and question['question__lesson__title']
    ]
    print("Lessons for revision: ", lessons_for_revision)
    return render(request, 'users/user-profile.html', {'profile': profile, 'lessons_for_revision':lessons_for_revision})


# @csrf_exempt  # This decorator is used to exempt CSRF protection for simplicity. Use appropriate CSRF protection in production.
# @login_required  # This decorator ensures that the user is logged in to update their profile picture.
# def update_user(request):
#     profile = Profile.objects.get(id=request.user.profile.id)
#     form = ProfilePictureForm(instance=profile)
#     if request.method == 'POST':
#         form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect('user-profile')  # Redirect to profile page after successful update
#     else:
#         form = ProfilePictureForm(instance=profile)

#     context = {
#         'form': form,
#     }
#     return render(request, 'users/user-profile.html', context)

@login_required
def update_user(request):
    current_user = Profile.objects.get(id=request.user.profile.id)
    print("Current User: ", current_user)
    form = UpdateProfile(request.POST or None, request.FILES or None, instance=current_user)
    if form.is_valid():
        form.save()
        return redirect('user-profile')
    return render(request, "users/update_user.html", {'form': form})