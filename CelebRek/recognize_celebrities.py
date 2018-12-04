import boto3
import json

# if __name__ == "__main__":
#     photo = 'bpanther.jpg'
    
#     client = boto3.client('rekognition')


#     with open(photo, 'rb') as image:
#         response = client.recognize_celebrities(Image={'Bytes': image.read()})
#         print(response)

#     print('Detected faces for ' + photo)
#     for celebrity in response['CelebrityFaces']:
#         print 'Confidence: ' + str(celebrity['MatchConfidence'])
#         print 'Name: ' + celebrity['Name']
#         print 'Id: ' + celebrity['Id']
#         print 'Position:'
#         print '   Left: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Height'])
#         print '   Top: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Top'])
#         print 'Info'
#         for url in celebrity['Urls']:
#             print '   ' + url
#         print

client = boto3.client('rekognition')

def download_pic():
    # write data to file only for tweetspics that returned a pic.
    with open('data/data.json', 'w') as outfile:
        for tweet in tweets:
            if tweet._json.get('entities').get('media') == None:
                continue
            json.dump(tweet._json, outfile)
            outfile.write('\n')

    # obtain the full path for the images
    media_files = set()
    for status in tweets:
        media = status.entities.get('media', [])
        if len(media) > 0:
            media_files.add(media[0]['media_url'])

    print(media_files)
    # Download the images
    for media_file in media_files:
        wget.download(media_file, './pics/')

# TO DO: assign vars depending on number of celebs recognized in pic
# OR store all the kv's in a dict!!
def recognize_photo(photo):
    rec_dict = {'Names': [], 'Confidence': []}

    with open(photo, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})
        # print(json.dumps(response))

    print('Detected faces for ' + photo)
    for celebrity in response['CelebrityFaces']:
        print('Confidence: ' + str(celebrity['MatchConfidence']))
        print('Name: ' + celebrity['Name'])
        print('Id: ' + celebrity['Id'])
        print('Position:')
        print('   Left: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Height']))
        print('   Top: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Top']))
        print('Info')
        for url in celebrity['Urls']:
            print('   ' + url)
        rec_dict['Names'].append(celebrity['Name'].encode('utf-8'))
        rec_dict['Confidence'].append(celebrity['MatchConfidence'])
        print('Length of the dict is {}'.format(len(response['CelebrityFaces'])))
    print(rec_dict)
    return rec_dict
        
def generate_message(_dict):
    i = 0
    while i < len(_dict['Confidence']):
        if _dict['Confidence'][i] == 100.:
            print("I'm 100% confident that this is {}".format(_dict['Names'][i]))
        if _dict['Confidence'][i] < 100.:
            if _dict['Confidence'][i] >= 90.:
                print("There's a good chance that this is {}".format(_dict['Names'][i]))
            if _dict['Confidence'][i] < 90.:
                if _dict['Confidence'][i] >= 70.:
                    print("This is likely a picture of {}".format(_dict['Names'][i]))
                if _dict['Confidence'][i] < 70.:
                    print("I'm not sure who this is, but I think it's {}".format(_dict['Names'][i]))
            else:
                print("There's a problem here.")
        i += 1

rec_dict = recognize_photo('notsure.jpg')
generate_message(rec_dict)


    # {"prob": 95.0, "description": "almost certainly"},
    # {"prob": 90.0, "description": "highly likely"}, 
    # {"prob": 80.0, "description": "good chance"}, 
    # {"prob": 70.0, "description": "likely"},
    # {"prob": 60.0, "description": "possible"}, 
    # {"prob": 20.0, "description": "unlikely"}, 
    # {"prob": 0.0, "description": "highly unlikely"}

