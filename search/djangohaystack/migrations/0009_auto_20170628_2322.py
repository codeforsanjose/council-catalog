# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-28 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangohaystack', '0008_auto_20170628_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('ip_address', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Note',
        ),
    ]