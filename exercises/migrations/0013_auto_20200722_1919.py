# Generated by Django 3.0.8 on 2020-07-22 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0012_category_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='about',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
    ]
