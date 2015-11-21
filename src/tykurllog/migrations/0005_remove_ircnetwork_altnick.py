# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0004_auto_20151121_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ircnetwork',
            name='altnick',
        ),
    ]
