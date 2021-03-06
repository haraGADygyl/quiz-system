# Generated by Django 4.0.3 on 2022-04-02 10:05

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="interests",
            field=models.ManyToManyField(
                related_name="interested_students", to="main.subject"
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="quizzes",
            field=models.ManyToManyField(to="main.quiz"),
        ),
    ]
