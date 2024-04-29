from django.contrib import admin

# Register your models here.
from .models import Project, Lesson, LessonSection


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'project')

@admin.register(LessonSection)
class LessonSectionAdmin(admin.ModelAdmin):
    pass