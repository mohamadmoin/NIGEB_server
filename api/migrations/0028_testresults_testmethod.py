# Generated by Django 4.0.5 on 2024-08-19 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_samples_phone_number_samples_sample_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresults',
            name='testMethod',
            field=models.CharField(default='', max_length=50),
        ),
    ]
