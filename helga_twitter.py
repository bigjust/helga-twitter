import smokesignal
import tweepy

from twisted.internet import reactor

from helga import settings, log
from helga.plugins import Command

CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = getattr(settings, 'TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = getattr(settings, 'TWITTER_ACCESS_SECRET')

logger = log.getLogger(__name__)


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

        if args and args[0] in ['tweet', 'follow']:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)

            subcmd = args[0]

            if subcmd == 'tweet':

                if len(args) < 2:
                    return 'usage: twitter tweet <text...>'

                status = api.update_status(' '.join(args[1:]))
                return 'https://twitter.com/{}/status/{}'.format(
                    status.author.screen_name,
                    status.id,
                )

            if subcmd == 'follow':

                if len(args) < 2:
                    return 'usage: twitter follow <username>'

                username = args[1]
                api.create_friendship(
                    screen_name=username,
                    follow=True
                )

                return 'Done!'


@smokesignal.on('join')
def init_twitter_stream(client, channel):

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
