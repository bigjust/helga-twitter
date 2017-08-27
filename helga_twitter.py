import tweepy

from twisted.internet import reactor

from helga import settings
from helga.plugins import Command

CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = getattr(settings, 'TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = getattr(settings, 'TWITTER_ACCESS_SECRET')


class HelgaStreamListener(tweepy.StreamListener):

    def __init__(self, *args, **kwargs):

        self.client = kwargs.pop('client')
        self.channel = kwargs.pop('channel')

        super(HelgaStreamListener, self).__init__(*args, **kwargs)

    def on_status(self, status):
        self.client.msg(self.channel, u'@{}: {}'.format(
            status.user.screen_name,
            status.text
        ))


class TwitterPlugin(Command):

    command = 'twitter'

    def run(self, client, channel, nick, message, cmd, args):

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        myStream = tweepy.Stream(
            auth = api.auth,
            listener = HelgaStreamListener(
                client=client,
                channel=channel
            )
        )

        myStream.userstream(async=True)

        return 'Initialized Twitter listener...'
