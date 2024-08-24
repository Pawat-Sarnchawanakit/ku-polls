# Generated by Django 5.1 on 2024-08-20 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_response_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='image',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='poll',
            name='name',
            field=models.CharField(default='Unnamed Poll', max_length=100),
        ),
    ]