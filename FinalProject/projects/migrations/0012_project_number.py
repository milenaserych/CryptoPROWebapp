# Generated by Django 4.2 on 2024-04-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_lesson_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
