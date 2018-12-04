import os
import tweepy
from tweepy import OAuthHandler
 
consumer_key = 'F5izqDeBYHyS2qZ2o82kKD8X9'
consumer_secret = 'EE8j05uFeDE3LlVmnnZPzGF8vfqwivecQOdNTcYHEEHAHyYLVF'
access_token = '607964367-08jXSUsWf1sWBpf4gg0jbiL8SVcYnrhKvjqghqNQ'
access_secret = 'hKsSxmzJphL1brmRIPQqkpFIBW6OHp09ESLikxXKPbgrU'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

# Read our own timeline (i.e. our Twitter homepage) with:

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)