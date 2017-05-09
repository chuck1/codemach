# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 00:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheet_id', models.CharField(max_length=256)),
                ('user_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sheet_user_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]