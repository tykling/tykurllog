from django.core.management.base import BaseCommand
from tykurllog.models import IrcNetwork
import asyncio, irc3, random

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
                'network': ircnetwork,
            }

            self.stdout.write('Starting bot for network %s...' % ircnetwork.network)
            irc3.IrcBot(nick=ircnetwork.nick, network=ircnetwork, **config).run(forever=False)

        ### done
        self.stdout.write('Done spawning bots, entering loop...')
        loop.run_forever()

@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self.network = bot.config['network']

    @irc3.event(rfc.PRIVMSG)
    def check_for_url(bot, **kwargs):
        ### check if this is a message to a channel
        if kwargs['target'] not in [channel.channel for channel in bot.network.channels.all()]:
            return
        
        print("got message %s on channel %s" % (kwargs['data'], kwargs['target']))
        ### check if this message contains a URL

