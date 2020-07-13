# Generated by Django 3.0.8 on 2020-07-03 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField(max_length=500)),
                ('answer', models.CharField(max_length=60)),
                ('level', models.PositiveIntegerField()),
                ('url', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TasksCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Userstasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_status', models.CharField(default='unsolved', max_length=12)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.Tasks')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsersCategoryLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_progress', models.PositiveIntegerField(default=0)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.TasksCategory')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tasks',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.TasksCategory'),
        ),
    ]
