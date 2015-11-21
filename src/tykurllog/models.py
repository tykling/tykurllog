from django.db import models
from django import forms
from django.core.urlresolvers import reverse


class IrcNetwork(models.Model):
    network = models.TextField()
    nick = models.TextField()
    altnick = models.TextField()
    nickserv_user = models.TextField(null=True, blank=True)
    nickserv_password = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.network)


class IrcServer(models.Model):
    network = models.ForeignKey('tykurllog.IrcNetwork', related_name="servers")
    hostorip = models.TextField()
    port = models.PositiveIntegerField()
    tls = models.BooleanField(default=True)
    password = models.TextField(null=True, blank=True)


class IrcChannel(models.Model):
    network = models.ForeignKey('tykurllog.IrcNetwork', related_name="channels")
    channel = models.TextField()
    key = models.TextField(null=True, blank=True)
    log_nicknames = models.BooleanField(default=True)


class LoggedUrl(models.Model):
    channel = models.ForeignKey('tykurllog.IrcChannel', related_name="urls")
    url = models.TextField()
    nick = models.TextField(null=True, blank=True)
    when = models.DateTimeField(auto_now_add=True)

