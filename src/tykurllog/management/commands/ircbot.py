from django.core.management.base import BaseCommand
from django.utils import timezone
from tykurllog.models import IrcNetwork, LoggedUrl
import asyncio, irc3, random, yurl


class Command(BaseCommand):
    args = 'none'
    help = 'Run IRC bots'

    def handle(self, *args, **options):
        ### get asyncio loop
        loop = asyncio.get_event_loop()

        ### loop through networks, spawn bots as needed
        for ircnetwork in IrcNetwork.objects.filter(active=True):
            self.stdout.write('Processing IRC network %s...' % ircnetwork)
            if ircnetwork.servers.filter(active=True).count==0:
                self.stdout.write('IRC network %s has no active servers, skipping' % ircnetwork.name)
                continue
            if ircnetwork.channels.filter(active=True).count==0:
                self.stdout.write('IRC network %s has no active channels, skipping' % ircnetwork.name)
                continue
        
            server = random.choice(ircnetwork.servers.filter(active=True))
            self.stdout.write('Picked server %s:%s (%s) for IRC network %s...' % (server.hostorip, server.port, 'with TLS' if server.tls else 'no TLS', ircnetwork.name))
            config = {
                'autojoins': [channel.channel for channel in ircnetwork.channels.filter(active=True)],
                'host': server.hostorip,
                'port': server.port,
                'ssl': server.tls,
                'includes': [
                    'irc3.plugins.core',
                    __name__,
                ],
                'loop': loop,
                'nick': ircnetwork.nick,
                'realname': ircnetwork.ident if ircnetwork.ident else 'tykurllog',
                'userinfo': ircnetwork.realname if ircnetwork.realname else 'tykurllog - https://github.com/tykling/tykurllog',
                'network': ircnetwork,
            }

            self.stdout.write('Starting bot for network %s...' % ircnetwork.name)
            irc3.IrcBot(**config).run(forever=False)

        ### done
        self.stdout.write('Done spawning bots, entering loop...')
        loop.run_forever()

@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self.network = bot.config['network']

    @irc3.event(irc3.rfc.PRIVMSG)
    def check_for_url(bot, **kwargs):
        ### check if this is a message to a channel
        if kwargs['target'] not in [channel.channel for channel in bot.network.channels.filter(active=True)]:
            return
        
        ### get the current time
        messagetime = timezone.now()

        ### check if each word in this message is a URL
        for word in kwargs['data'].split(" "):
            ### since almost all strings can be a valid URL, 
            ### we identify the URLs we want by looking for the protocol seperator :// 
            if '://' in word:
                ### use urlparse to validate/cleanup the URL
                try:
                    url = yurl.URL(word).validate()
                except yurl.InvalidHost: ### do we need to catch other exceptions here?
                    ### invalid url, not saving
                    return
                
                ### check if this url has been spammed on this channel before
                try:
                    dburl = LoggedUrl.objects.get(
                        channel=bot.network.channels.get(channel=kwargs['target']),
                        url=url.as_string(),
                    )
                    
                    ### this url has been spammed to this channel before, increase number of repeats
                    dburl.repeats += 1
                    dburl.save()
                    
                    ### announce url repeat to channel if enabled
                    if bot.network.channels.get(channel=kwargs['target']).announce_urlrepeats:
                        if dburl.repeats==1:
                            bot.privmsg(kwargs['target'], '%s, that url was first spammed in %s on %s by %s.' % (kwargs['usermask'].split("!")[0], kwargs['target'], dburl.when, dburl.usermask.split("!")[0]))
                        else:
                            bot.privmsg(kwargs['target'], '%s, that url has been repeated %s times since it was first spammed in %s on %s by %s' % (kwargs['usermask'].split("!")[0], dburl.repeats, kwargs['target'], dburl.when, dburl.usermask.split("!")[0]))
                except LoggedUrl.DoesNotExist:
                    ### save new url (for this channel at least) to db
                    loggedurl = LoggedUrl.objects.create(
                        channel=bot.network.channels.get(channel=kwargs['target']),
                        url=url.as_string(),
                        usermask=kwargs['mask'] if bot.network.channels.get(channel=kwargs['target']).log_nicknames else None,
                        when=messagetime,
                    )

