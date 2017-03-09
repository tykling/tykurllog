from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from timezone_field import TimeZoneField
from django.conf import settings


class IrcNetwork(models.Model):
    name = models.TextField()
    nick = models.TextField()
    ident = models.TextField(blank=True)
    realname = models.TextField(blank=True)
    nickserv_user = models.TextField(null=True, blank=True)
    nickserv_password = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s <%s>' % (self.name, self.nick)


class IrcServer(models.Model):
    network = models.ForeignKey('tykurllog.IrcNetwork', related_name="servers")
    hostorip = models.TextField()
    port = models.PositiveIntegerField()
    tls = models.BooleanField(default=True)
    password = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s: %s port %s, tls: %s' % (self.network.name, self.hostorip, self.port, self.tls)


class IrcChannel(models.Model):
    network = models.ForeignKey('tykurllog.IrcNetwork', related_name="channels")
    channel = models.TextField()
    key = models.TextField(null=True, blank=True)
    log_nicknames = models.BooleanField(default=True)
    announce_urlrepeats = models.BooleanField(default=True)
    timezone = TimeZoneField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s (%s)' % (self.network.name, self.channel, 'active' if self.active else 'not active')


class LoggedUrl(models.Model):
    channel = models.ForeignKey('tykurllog.IrcChannel', related_name="urls")
    url = models.URLField(max_length=500)
    usermask = models.TextField(null=True, blank=True)
    when = models.DateTimeField(auto_now_add=True)
    repeats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s spammed on %s by %s on %s' % (self.url, self.channel, self.usermask, self.when)

    class Meta:
        ordering = ['-when']
        unique_together=('channel', 'url')


