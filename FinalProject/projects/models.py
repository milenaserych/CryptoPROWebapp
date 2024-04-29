from django.db import models
import uuid
# Create your models here.



class Project(models.Model):
    title = models.CharField(max_length=200)
    number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    number = models.IntegerField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, related_name='lessons', on_delete=models.CASCADE, default='8fd8d246-8b97-439b-8291-9f85fb156483')

    def __str__(self):
        return self.title
    
    def get_sections(self):
        return self.sections.all()

class LessonSection(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    ordered_list = models.TextField(null=True, blank=True)
    term_definition = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='lesson_images/', default="profiles/defaultprofile.jpeg")

    def __str__(self):
        return self.title
    
    def get_ordered_list_as_list(self):
        if self.ordered_list:
            return self.ordered_list.splitlines()
        return []
