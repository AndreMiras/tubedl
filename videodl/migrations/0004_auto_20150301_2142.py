# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videodl', '0003_downloadlink_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloadlink',
            name='url',
            field=models.URLField(max_length=255),
            preserve_default=True,
        ),
    ]
