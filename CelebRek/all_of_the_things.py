#!/Users/andrewrubino/anaconda2/bin/python

from __future__ import print_function

import glob
import os
import tweepy
import json
import wget
import boto3

from datetime import datetime, timedelta
from tweepy import OAuthHandler

# set env vars and local vars
hour = (datetime.now() - timedelta(minutes=10)).strftime('%H')
today = (datetime.now() - timedelta(minutes=10)).strftime('%Y-%m-%d')
# hour = (datetime.now() - timedelta(hours=1)).strftime('%H')
# today = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d')
# hour = '16'
# today = '2018-12-03'
tweet_dir = os.environ.get('tweet_dir')
pics = os.environ.get('pics')
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_secret = os.environ.get('access_secret')


def create_filename(tweet_dir, today, hour):
    return tweet_dir + today + '/logs_' + hour + '.json'

def create_download_output_folder(pics, today):
    return pics + today + '/'

def create_picture_folder(output_folder):
  if not os.path.exists(output_folder):
    os.mkdir(output_folder)

def read_hourly_json(filename):
    """Read in json by hour"""
    tweets = []
    for line in open(filename, 'r'):
        try:
            tweets.append(json.loads(line))
        except ValueError:
            continue
    return tweets

def get_media_files(tweets, today, hour, output_folder):
    """obtain the full path for the images"""
    media_file = ""
    tweet_id = ""
    create_picture_folder(output_folder)

    for tweet in tweets:
        if tweet.get('delete') != None:
            continue
        if not tweet['retweeted'] and 'RT @' not in tweet['text'] and not tweet['in_reply_to_status_id']:
            media = tweet.get('entities').get('media', [])
            if len(media) > 0:
                # media_files.append(media[0]['media_url'])
                media_file += media[0]['media_url']
                # tweet_ids.append(tweet['id'])
                tweet_id += tweet['id_str']
    return media_file, tweet_id

def download_media_files(media_file, output_folder):
    """Download the images"""
    # for media_file in media_files:
    if os.path.isfile(os.path.join(output_folder, media_file.split('/')[-1].encode())) == False:
        wget.download(media_file, out = output_folder)
    else:
        pass

def recognize_photo(output_folder, photo):
    rec_dict = {'Names': [], 'Confidence': []}

    directory = output_folder + photo
    with open(directory, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})

    for celebrity in response['CelebrityFaces']:
        rec_dict['Names'].append(celebrity['Name'].encode('utf-8'))
        rec_dict['Confidence'].append(celebrity['MatchConfidence'])
    return rec_dict
      
def generate_message(_dict):
    i = 0
    tweet = ""
    subjects = len(_dict['Confidence'])
    categories = {'100%': [], '99%': [], 'almost sure': [], 'maybe': [], 'not sure': []}
    if _dict['Confidence'] == []:
        tweet +=  "I don't recognize anyone in this photo."
    else:
        while i < len(_dict['Confidence']):
            if _dict['Confidence'][i] == 100:
                categories['100%'].append(_dict['Names'][i])
            if _dict['Confidence'][i] == 99.:
                categories['99%'].append(_dict['Names'][i])
            if _dict['Confidence'][i] < 99. and _dict['Confidence'][i] >= 90.:
                categories['almost sure'].append(_dict['Names'][i])
            if _dict['Confidence'][i] < 90. and _dict['Confidence'][i] >= 70.:
                categories['maybe'].append(_dict['Names'][i])
            if _dict['Confidence'][i] < 70.:
                categories['not sure'].append(_dict['Names'][i])
            i += 1

        ## START HERE: print(*categories['maybe'], sep=' and ')
        for k,v in categories.items():
            if v != []:
                if k == '100%':
                    tweet += "I'm 100% confident I see " + ' and '.join(categories[k]) + '.\n'
                if k == '99%':
                    tweet += "I'm 99% sure that's " + ' and '.join(categories[k]) + '.\n'
                if k == 'almost sure':
                    tweet += "There's a good chance that's " + ' and '.join(categories[k]) + '.\n'
                if k == 'maybe': 
                    tweet += ' and '.join(categories[k]) + " might be in this picture.\n"
                if k == 'not sure':
                    tweet += "I think that's " + ' and '.join(categories[k]) + '.\n'
    return tweet

def main(today, hour, pics, tweet_dir, consumer_key, consumer_secret, access_token, access_secret):
    filename = create_filename(tweet_dir, today, hour)
    output_folder = create_download_output_folder(pics, today)
    list_of_files = glob.glob(output_folder + '*')
    tweets = read_hourly_json(filename)
    media_file, tweet_id = get_media_files(tweets, today, hour, output_folder)
    if media_file == "":
        print("No pic downloaded")
        pass
    elif media_file != "":
        if output_folder + media_file.split('/')[-1].encode() in list_of_files:
            pass
        else:
            pic = media_file.split('/')[-1].encode()
            # print(pic)
            download_media_files(media_file, output_folder)
            rec_dict = recognize_photo(output_folder, pic)
            print(rec_dict)
            message = generate_message(rec_dict)
            if message == "I don't recognize anyone in this photo.":
                pass
            else:   
                auth = OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_secret)
                api = tweepy.API(auth)
                api.update_status(status="@RottenTomatoes {}".format(message),
                                  in_reply_to_status_id="{}".format(tweet_id))

# execute
if __name__=='__main__':
    client = boto3.client('rekognition')
    main(today, hour, pics, tweet_dir, consumer_key, consumer_secret, access_token, access_secret)
    # print(tweet_dir)
    # print("this is a test")
    # filename = create_filename(tweet_dir, today, hour)
    # print(filename)
