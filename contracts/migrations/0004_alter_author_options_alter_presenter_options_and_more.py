# Generated by Django 5.2.1 on 2025-05-13 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_manager_options_alter_person_options_and_more'),
        ('contracts', '0003_alter_accrual_options_alter_author_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Авторский', 'verbose_name_plural': '_Авторские'},
        ),
        migrations.AlterModelOptions(
            name='presenter',
            options={'verbose_name': 'Ведущий', 'verbose_name_plural': '_Ведущие'},
        ),
        migrations.RemoveField(
            model_name='contract',
            name='id',
        ),
        migrations.AlterField(
            model_name='author',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.person', verbose_name='Преподаватель'),
        ),
        migrations.AlterField(
            model_name='author',
            name='reward_percent',
            field=models.DecimalField(decimal_places=1, max_digits=8, verbose_name='Процент'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='contract_nunber',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='presenter',
            name='presenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.person', verbose_name='Ведущий'),
        ),
    ]
