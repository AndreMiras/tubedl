# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('videodl', '0004_auto_20150301_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='downloadlink',
            name='id',
        ),
        migrations.AlterField(
            model_name='downloadlink',
            name='audio_path',
            field=models.CharField(max_length=255, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='downloadlink',
            name='title',
            field=models.CharField(max_length=255, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='downloadlink',
            name='uuid',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
        ),
        migrations.AlterField(
            model_name='downloadlink',
            name='video_path',
            field=models.CharField(max_length=255, blank=True, default=''),
        ),
    ]
