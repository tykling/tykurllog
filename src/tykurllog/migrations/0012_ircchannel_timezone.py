# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0011_ircchannel_announce_urlrepeats'),
    ]

    operations = [
        migrations.AddField(
            model_name='ircchannel',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(blank=True, null=True),
        ),
    ]
