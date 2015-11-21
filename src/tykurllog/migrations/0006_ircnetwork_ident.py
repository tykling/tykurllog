# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0005_remove_ircnetwork_altnick'),
    ]

    operations = [
        migrations.AddField(
            model_name='ircnetwork',
            name='ident',
            field=models.TextField(blank=True),
        ),
    ]
