# Generated by Django 4.2.5 on 2023-09-22 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_status_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status',
            old_name='number',
            new_name='weight',
        ),
    ]
