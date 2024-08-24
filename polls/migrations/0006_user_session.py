# Generated by Django 5.1 on 2024-08-20 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_poll_image_poll_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('password_hash', models.BinaryField(max_length=64)),
                ('password_salt', models.BinaryField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('accessed', models.DateTimeField(auto_now_add=True)),
                ('session', models.CharField(editable=False, max_length=48, primary_key=True, serialize=False, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.user')),
            ],
        ),
    ]
