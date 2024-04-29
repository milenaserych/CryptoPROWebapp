import os
import chardet
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Lesson
from quizes.models import Quiz
from users.models import Profile
from .forms import ProjectForm, LessonForm, LessonSectionForm
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt



def projects(request):
    projects = Project.objects.all()
    try:
        profile_obj = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile_obj = None
    context = {
        'projects' : projects,
        'profile' : profile_obj,
    }
    return render(request, 'projects/projects.html', context)


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    lessons = Lesson.objects.filter(project=projectObj).order_by('number').all()
    lessons_ids = list(lessons.values_list('id', flat=True))
    quiz = Quiz.objects.filter(project=projectObj)
    try:
        profile_obj = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile_obj = None
    print("Lessons: ", lessons)
    context = {
        'project':projectObj,
        'lessons':lessons,
        'quiz':quiz,
        'lessons_ids':lessons_ids,
        'profile':profile_obj,
    }
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects:projects')
    context = {
        'form':form,
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:projects')
    context = {
        'form':form,
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects:projects')
    context = {
        'object':project,
    }
    return render(request, 'projects/delete_template.html', context)

@login_required(login_url="login")
def createLesson(request):
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST)
        section_formset = formset_factory(LessonSectionForm, extra=int(request.POST.get('section_count', 1)))(request.POST, request.FILES, prefix='sections')

        if lesson_form.is_valid() and all(form.is_valid() for form in section_formset):
            lesson = lesson_form.save()

            for form in section_formset:
                section = form.save(commit=False)
                section.lesson = lesson
                section.save()

            return redirect('projects:projects')  # Redirect to the project details page or another appropriate page
    else:
        lesson_form = LessonForm()
        section_formset = formset_factory(LessonSectionForm, extra=1)(prefix='sections')

    context = {
        'lesson_form': lesson_form,
        'section_formset': section_formset,
    }

    return render(request, 'projects/create_lesson.html', context)


@csrf_exempt
def update_current_module(request):
    if request.method == 'POST':
        module_title = request.POST.get('module_title', '')
        try:
            profile_obj = Profile.objects.get(user=request.user)
            project = Project.objects.get(title=module_title)
            current_module_number = project.number
            modules_completed = profile_obj.modules_completed
            print("Current_module_number: ", current_module_number)
            print("Modules_completed: ", modules_completed)

            if current_module_number >= modules_completed:
                profile_obj.current_module = module_title
                profile_obj.modules_completed = current_module_number
                print("Current module was just changed in the back end! Changed to: ", profile_obj.current_module)
                print("Modules Completed: ", profile_obj.modules_completed)
                profile_obj.save()
                return JsonResponse({'success': True})
            else:
                print("You already completed that module, just decided to go over it again!")
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})