# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0007_auto_20151121_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loggedurl',
            old_name='mask',
            new_name='usermask',
        ),
    ]
