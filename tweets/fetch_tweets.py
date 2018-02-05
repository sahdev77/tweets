from tweepy import Stream
from tweets.tweets_listner import TweetsDataListener
from settings import twitter_config

class Tweety(object):
    def __init__(self, listener=TweetsDataListener()):
        self.listener = listener
        self.__auth__ = None

    def __authenticate__(self):
        from tweepy import OAuthHandler
        if self.__auth__ is None:
            self.__auth__ = OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
            self.__auth__.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
        return self.__auth__ is not None

    def __streamer__(self):
        is_authenticated = self.__authenticate__()
        if is_authenticated:
            return Stream(self.__auth__, self.listener,timeout=300)
        return None

    def filter(self, keywords,woeid,async=True):
        self.__authenticate__()
        import tweepy
        if not keywords:
            api = tweepy.API(self.__auth__)
            stream_api = api.trends_place(woeid) # tweets for india only
            keywords = []
            for trend in stream_api[0]["trends"]:
                try:
                    keywords.append(str(trend["name"]))
                except:
                    pass
        streamer = self.__streamer__()
        try:
            print "[STREAM] Started stream using keywords", keywords
            streamer.filter(track=keywords,async=async)
        except Exception as ex:
            print "[STREAM] Stream stopped! Reconnecting to twitter stream, keywords", keywords
            print ex.message, ex.args
            self.filter(keywords=keywords, async=async)

    def get_woied(self):
        self.__authenticate__()
        import tweepy
        api = tweepy.API(self.__auth__)
        places = api.trends_available()
        return places
