# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0010_loggedurl_repeats'),
    ]

    operations = [
        migrations.AddField(
            model_name='ircchannel',
            name='announce_urlrepeats',
            field=models.BooleanField(default=True),
        ),
    ]
