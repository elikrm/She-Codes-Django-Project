# Generated by Django 3.0.8 on 2020-08-22 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_newsstory_story_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsstory',
            name='story_img',
        ),
    ]
