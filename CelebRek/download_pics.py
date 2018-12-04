import os
import tweepy
from tweepy import OAuthHandler
import json
import wget

from datetime import datetime
 
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_secret = os.environ.get('access_secret')

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

tweets = api.user_timeline(screen_name='RottenTomatoes',
                           count=25, include_rts=False,
                           exclude_replies=True)
last_id = tweets[-1].id
 
# collect tweets
while tweets < 25:
    more_tweets = api.user_timeline(screen_name='RottenTomatoes',
                                    count=10,
                                    include_rts=False,
                                    exclude_replies=True,
                                    max_id=last_id-1)
    # There are no more tweets
    if len(more_tweets) == 0:
        break
    else:
        last_id = more_tweets[-1].id-1
        tweets = tweets + more_tweets

# write data to file only for tweetspics that returned a pic.
with open('data/data.json', 'w') as outfile:
    for tweet in tweets:
        if tweet._json.get('entities').get('media') == None:
            continue
        json.dump(tweet._json, outfile)
        outfile.write('\n')

def download_images(status, num_tweets, output_folder):
  create_folder(output_folder)
  downloaded = 0

  for tweet_status in status:

    if(downloaded >= num_tweets):
      break

    for media_url in tweet_media_urls(tweet_status):
      # Only download if there is not a picture with the same name in the folder already
      file_name = os.path.split(media_url)[1]
      if not os.path.exists(os.path.join(output_folder, file_name)):
        wget.download(media_url +":orig", out=output_folder+'/'+file_name)
        downloaded += 1

# hour = datetime.now().strftime('%H')
# today = datetime.now().strftime('%Y-%m-%d')
# filename = 'logs_' + hour + '.json'

# def read_hourly_json(filename):
#     """Read in json by hour"""
#     tweets = []
#     for line in open(filename, 'r'):
#         try:
#             tweets.append(json.loads(line))
#         except ValueError:
#             continue
#     return tweets

# """obtain the full path for the images"""
# tweets = read_hourly_json('../data/2018-08-15/logs_03.json')
# media_files = set()
# for tweet in tweets:
#     media = tweet.get('entities').get('media', [])
#     if len(media) > 0:
#         media_files.add(media[0]['media_url'])

# print(media_files)
# # Download the images
# for media_file in media_files:
#     wget.download(media_file, '../pics/')
