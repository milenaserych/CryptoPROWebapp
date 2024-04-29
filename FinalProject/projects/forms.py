from django.forms import ModelForm
from .models import Project, Lesson, LessonSection

# Generate a form to add new Projects to the db based on the current Project model
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image','description']

class LessonSectionForm(ModelForm):
    class Meta:
        model = LessonSection
        fields = ['title', 'content', 'ordered_list', 'term_definition', 'image']

class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['project', 'title', 'content', 'number'] 
