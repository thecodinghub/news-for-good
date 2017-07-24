# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20170724_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_html',
            field=models.TextField(default='There', editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.Post'),
        ),
    ]
