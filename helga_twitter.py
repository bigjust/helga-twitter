import tweepy

from twisted.internet import reactor

from helga.plugins import command


@command('t')
def twitter(client, channel, nick, message, cmd, args):
    return 'yo!'
