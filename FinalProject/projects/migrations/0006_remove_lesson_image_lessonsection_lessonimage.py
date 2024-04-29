# Generated by Django 4.2 on 2024-01-26 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_lesson_remove_project_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='image',
        ),
        migrations.CreateModel(
            name='LessonSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(blank=True, null=True)),
                ('ordered_list', models.TextField(blank=True, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='projects.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='LessonImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='lesson_images/')),
                ('lesson_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='projects.lessonsection')),
            ],
        ),
    ]