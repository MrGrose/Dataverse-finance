# Generated by Django 5.2.1 on 2025-05-14 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0014_alter_contract_created_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contract',
            unique_together=set(),
        ),
    ]
