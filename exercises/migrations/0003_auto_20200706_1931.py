# Generated by Django 3.0.8 on 2020-07-06 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_auto_20200703_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='task_id',
        ),
        migrations.RemoveField(
            model_name='taskscategory',
            name='category_id',
        ),
    ]
