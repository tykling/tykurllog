# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ircserver',
            name='tls',
            field=models.BooleanField(default=True),
        ),
    ]
