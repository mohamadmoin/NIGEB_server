# Generated by Django 4.0.5 on 2024-08-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_filetables_use_case_alter_testinfos_normal_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='samples',
            name='history_file_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
