# Generated by Django 5.1.5 on 2025-01-23 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachment',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='sample',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='sampletest',
            options={'ordering': ['id']},
        ),
    ]
