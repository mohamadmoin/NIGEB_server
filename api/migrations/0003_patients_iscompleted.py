# Generated by Django 4.0.5 on 2023-06-03 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_patients_usercreatorname'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='iscompleted',
            field=models.BooleanField(default=False),
        ),
    ]
