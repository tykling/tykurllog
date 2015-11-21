from django.core.management.base import BaseCommand
from django.utils import timezone
from tykurllog.models import IrcNetwork, LoggedURL
import asyncio, irc3, random
from urllib import parse


class Command(BaseCommand):
    args = 'none'
    help = 'Run IRC bots'

    def handle(self, *args, **options):
        ### get asyncio loop
        loop = asyncio.get_event_loop()

        ### loop through networks, spawn bots as needed
        for ircnetwork in IrcNetwork.objects.all():
            self.stdout.write('Processing IRC network %s...' % ircnetwork)
            if ircnetwork.servers.count==0:
                self.stdout.write('IRC network %s has no servers, skipping' % ircnetwork.network)
                continue
            if ircnetwork.channels.count==0:
                self.stdout.write('IRC network %s has no channels, skipping' % ircnetwork.network)
                continue
        
            server = random.choice(ircnetwork.servers.all())
            self.stdout.write('Picked server %s:%s (%s) for IRC network %s...' % (server.hostorip, server.port, 'with TLS' if server.tls else 'no TLS', ircnetwork.network))
            config = {
                'autojoins': [channel.channel for channel in ircnetwork.channels.all()],
                'host': server.hostorip,
                'port': server.port,
                'ssl': server.tls,
                'timeout': 10,
                'includes': [
                    'irc3.plugins.core',
                    __name__,
                ],
                'loop': loop,
                'nick': ircnetwork.nick,
                'network': ircnetwork,
            }

            self.stdout.write('Starting bot for network %s...' % ircnetwork.network)
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
        if kwargs['target'] not in [channel.channel for channel in bot.network.channels.all()]:
            return
        
        ### check if this message contains a URL
        for word in kwargs['data']:
            ### since almost all strings can be a valid URL, 
            ### we identify URLs by looking for the protocol seperator :// 
            if '://' in word:
                ### use urlparse to validate/cleanup the URL
                result = parse(word)
                url = result.geturl()

                ### save to db
                loggedurl = LoggedUrl.objects.create(
                    channel=kwargs['target'],
                    url=url,
                    nick=kwargs['mask'] if bot.network.channels.get(channel=kwargs['target']).log_nicknames else None,
                    when=timezone.now(),
                )
                ### debug output
                self.bot.privmsg(kwargs['target'], 'url %s saved to db!' % url)

