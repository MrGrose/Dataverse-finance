# Generated by Django 5.2.1 on 2025-05-13 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presenter',
            name='title',
        ),
    ]
