# Generated by Django 4.2 on 2024-01-26 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_lessonsection_term_definition'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='project',
            field=models.ForeignKey(default='8fd8d246-8b97-439b-8291-9f85fb156483', on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='projects.project'),
        ),
    ]