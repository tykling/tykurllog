# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0008_auto_20151122_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='ircchannel',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ircnetwork',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ircserver',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
