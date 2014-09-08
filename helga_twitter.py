from twisted.internet import reactor

from helga.plugins import command
from helga.util.twitter import get_api


@command('twitter')
def twitter(client, channel, nick, message, cmd, args):
    return
