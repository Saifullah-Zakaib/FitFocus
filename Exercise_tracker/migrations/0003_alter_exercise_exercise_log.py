# Generated by Django 5.1.3 on 2024-11-26 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exercise_tracker', '0002_alter_exercise_exercise_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='exercise_log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exlog_app.exerciselog'),
        ),
    ]
