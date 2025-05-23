# Generated by Django 5.2.1 on 2025-05-13 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0009_alter_contract_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='contract_nunber',
            new_name='contract_number',
        ),
        migrations.AlterUniqueTogether(
            name='contract',
            unique_together={('contract_number',)},
        ),
    ]
