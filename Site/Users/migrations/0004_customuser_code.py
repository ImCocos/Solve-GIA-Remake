# Generated by Django 4.2.5 on 2023-09-22 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_customuser_failed_customuser_solved'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
