# Generated by Django 3.0.8 on 2020-07-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_remove_userstasks_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstasks',
            name='task_status',
            field=models.CharField(default='unsolved', max_length=60),
        ),
    ]
