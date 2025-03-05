# Generated by Django 4.0.5 on 2024-07-17 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0020_samples_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersDetaileds',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_id', models.CharField(default='', max_length=100)),
                ('userCreatorId', models.CharField(default='--', max_length=100)),
                ('name', models.CharField(default='', max_length=50)),
                ('user_Main_Img', models.FileField(blank=True, null=True, upload_to='files/')),
                ('image_loc', models.CharField(default='', max_length=50)),
                ('other_1', models.CharField(default='', max_length=50)),
                ('other_2', models.CharField(default='', max_length=50)),
                ('other_3', models.CharField(default='', max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
