# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0012_ircchannel_timezone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ircchannel',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(),
        ),
    ]
