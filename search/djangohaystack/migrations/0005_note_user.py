# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-28 00:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('djangohaystack', '0004_auto_20170628_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]