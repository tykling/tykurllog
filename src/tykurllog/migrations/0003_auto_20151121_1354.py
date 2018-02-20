# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tykurllog', '0002_ircserver_tls'),
    ]

    operations = [
        migrations.AddField(
            model_name='ircnetwork',
            name='realname',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='ircchannel',
            name='network',
            field=models.ForeignKey(related_name='channels', to='tykurllog.IrcNetwork', on_delete=models.PROTECT),
        ),
        migrations.AlterField(
            model_name='ircserver',
            name='network',
            field=models.ForeignKey(related_name='servers', to='tykurllog.IrcNetwork', on_delete=models.PROTECT),
        ),
        migrations.AlterField(
            model_name='loggedurl',
            name='channel',
            field=models.ForeignKey(related_name='urls', to='tykurllog.IrcChannel', on_delete=models.PROTECT),
        ),
    ]
