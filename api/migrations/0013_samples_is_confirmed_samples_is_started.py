# Generated by Django 4.0.5 on 2024-06-14 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_rename_idid_testinfos_id_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='samples',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='samples',
            name='is_started',
            field=models.BooleanField(default=False),
        ),
    ]
