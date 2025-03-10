# Generated by Django 5.1.5 on 2025-01-28 09:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_definitions', '0002_alter_testinfo_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteTestGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tests', models.ManyToManyField(blank=True, to='tests_definitions.testinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_test_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['group_name'],
                'unique_together': {('user', 'group_name')},
            },
        ),
    ]
