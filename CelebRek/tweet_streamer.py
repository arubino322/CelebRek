#!/Users/andrewrubino/anaconda2/bin/python

import time
import datetime
import os
import json
import wget
import tweepy

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# set env vars
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_secret = os.environ.get('access_secret')
tweet_dir = os.environ.get('tweet_dir')

class listener(StreamListener):

    def on_data(self, data):
        try:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            hour = datetime.datetime.now().strftime('%H')
            # if not data['retweeted'] and 'RT @' not in data['text']:
            print(data)
            if not os.path.exists(os.path.join(tweet_dir, today)):
                os.mkdir(os.path.join(tweet_dir, today))
            # media = data.get('entities').get('media', [])
            # if len(media) > 0:
            saveFile = open('/Users/andrewrubino/Code/CelebRek/data/{0}/logs_{1}.json'.format(today, hour), 'a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
            return True
        except BaseException, e:
            print('failed ondata,',str(e))
            time.sleep(5)

    def on_error(self, status):
        print(status)

try:
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(follow=['20108560']) # account_id for @RottenTomatoes account
except BaseException, e:
    print 'failed authorization,',str(e)
