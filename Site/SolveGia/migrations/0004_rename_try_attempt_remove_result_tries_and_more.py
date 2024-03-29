# Generated by Django 4.2.5 on 2023-09-17 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SolveGia', '0003_remove_task_category_category_amount_of_type_numbers_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Try',
            new_name='Attempt',
        ),
        migrations.RemoveField(
            model_name='result',
            name='tries',
        ),
        migrations.RemoveField(
            model_name='task',
            name='type_number',
        ),
        migrations.AddField(
            model_name='result',
            name='attempts',
            field=models.ManyToManyField(related_name='toattempts', to='SolveGia.attempt'),
        ),
    ]
