import json
import smokesignal
import tweepy

from twisted.internet import reactor

from helga import settings, log
from helga.plugins import Command, ResponseNotReady

CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', False)
CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', False)
ACCESS_TOKEN = getattr(settings, 'TWITTER_ACCESS_TOKEN', False)
ACCESS_TOKEN_SECRET = getattr(settings, 'TWITTER_ACCESS_SECRET', False)

logger = log.getLogger(__name__)


def get_client():

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return api

def tweet(client, channel, status):

    twitter = get_client()

    try:
        status_obj = twitter.update_status(status)
    except tweepy.error.TweepError as error:
        client.msg(
            channel,
            u'error: {}'.format(str(error))
        )
        return

    client.msg(
        channel,
        'https://twitter.com/{}/status/{}'.format(
            status_obj.author.screen_name,
            status_obj.id,
        ),
    )


class HelgaStreamListener(tweepy.StreamListener):

    def __init__(self, *args, **kwargs):

        self.client = kwargs.pop('client')
        self.channel = kwargs.pop('channel')

        super(HelgaStreamListener, self).__init__(*args, **kwargs)

    def on_status(self, status):

        if status.text.startswith('RT'):
            return

        self.client.msg(self.channel, u'@{}: {}'.format(
            status.user.screen_name,
            status.text
        ))


class TwitterPlugin(Command):

    command = 'twitter'
    help = 'Be Social. Usage: twitter [tweet|follow|unfollow] <status>|<screen_name>'

    def run(self, client, channel, nick, message, cmd, args):

        if args:

            twitter = get_client()
            subcmd = args[0]

            if subcmd == 'tweet':

                if len(args) < 2:
                    return 'usage: twitter tweet <text...>'

                reactor.callLater(0, tweet, client, channel, ' '.join(args[1:]))

                raise ResponseNotReady

            if subcmd == 'follow':

                if len(args) < 2:
                    return 'usage: twitter follow <username>'

                username = args[1]
                twitter.create_friendship(
                    screen_name=username,
                    follow=True
                )

                return 'Done!'

            if subcmd == 'unfollow':

                if len(args) < 2:
                    return 'usage: twitter unfollow <username>'

                twitter.destroy_friendship(
                    screen_name=args[1],
                )

                return 'Done!'

@smokesignal.on('join')
def init_twitter_stream(client, channel):

    required_settings = [
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    ]

    if not all(required_settings):
        logger.info('missing or more of required Twitter authentication settings. Please see README.')
        return

    twitter = get_client()

    myStream = tweepy.Stream(
        auth = twitter.auth,
        listener = HelgaStreamListener(
            client=client,
            channel=channel
        )
    )

    myStream.userstream(async=True)

    logger.debug('twitter stream listener initialized.')
