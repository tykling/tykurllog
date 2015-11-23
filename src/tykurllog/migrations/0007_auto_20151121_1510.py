# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0006_ircnetwork_ident'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loggedurl',
            old_name='nick',
            new_name='mask',
        ),
    ]
