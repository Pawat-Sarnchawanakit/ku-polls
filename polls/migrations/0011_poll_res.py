# Generated by Django 5.1 on 2024-08-24 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_alter_poll_creator_alter_response_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='res',
            field=models.IntegerField(default=0),
        ),
    ]