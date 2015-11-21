# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0003_auto_20151121_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ircnetwork',
            old_name='network',
            new_name='name',
        ),
    ]
