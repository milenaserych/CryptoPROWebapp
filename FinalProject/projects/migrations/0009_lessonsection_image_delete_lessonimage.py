# Generated by Django 4.2 on 2024-02-05 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_lesson_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonsection',
            name='image',
            field=models.ImageField(default='profiles/defaultprofile.jpeg', upload_to='lesson_images/'),
        ),
        migrations.DeleteModel(
            name='LessonImage',
        ),
    ]
