# Generated by Django 4.0.5 on 2024-07-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_usersdetaileds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdetaileds',
            name='user_Main_Img',
            field=models.FileField(blank=True, null=True, upload_to='profiles/'),
        ),
    ]
