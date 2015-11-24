# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0009_auto_20151122_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggedurl',
            name='repeats',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
