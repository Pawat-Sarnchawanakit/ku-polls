# Generated by Django 5.1 on 2024-08-21 08:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_limit_poll_allow'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='submitter',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
    ]
