# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IrcChannel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('channel', models.TextField()),
                ('key', models.TextField(null=True, blank=True)),
                ('log_nicknames', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='IrcNetwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('network', models.TextField()),
                ('nick', models.TextField()),
                ('altnick', models.TextField()),
                ('nickserv_user', models.TextField(null=True, blank=True)),
                ('nickserv_password', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IrcServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostorip', models.TextField()),
                ('port', models.PositiveIntegerField()),
                ('password', models.TextField(null=True, blank=True)),
                ('network', models.ForeignKey(to='tykurllog.IrcNetwork')),
            ],
        ),
        migrations.CreateModel(
            name='LoggedUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('nick', models.TextField(null=True, blank=True)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('channel', models.ForeignKey(to='tykurllog.IrcChannel')),
            ],
        ),
        migrations.AddField(
            model_name='ircchannel',
            name='network',
            field=models.ForeignKey(to='tykurllog.IrcNetwork'),
        ),
    ]
