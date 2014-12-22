# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videodl', '0002_auto_20141221_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='downloadlink',
            name='title',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
