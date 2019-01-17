import ConfigParser

import facebook

import requests

import base64

CONFIG_PARSER = ConfigParser.RawConfigParser()
CONFIG_FILE_PATH = r'/home/pi/Projects/photo-booth/utilities/keys.txt'
CONFIG_PARSER.read(CONFIG_FILE_PATH)
ALBUM_ID = CONFIG_PARSER.get('imgur', 'album_id')
CLIENT_ID = CONFIG_PARSER.get('imgur', 'client_id')

def post_to_facebook(image_to_post):
    '''reads from config the access_token and album id and posts image to FB'''
    print CONFIG_PARSER.sections()
    image = open(image_to_post, 'rb')
    url = 'https://api.imgur.com/3/image'
    body = {'image': base64.b64encode(image.read()), 'album': ALBUM_ID}
    headers = {'Authorization': 'Client-ID {0}'.format(CLIENT_ID)}
    res = requests.post(
        url,
        headers = headers,
        data = body
    )
    print res.text
    
##    
##    graph = facebook.GraphAPI(
##        access_token=CONFIG_PARSER.get('facebook', 'access_token_photo_booth'),
##        version='3.1')
##        #image=open(CONFIG_PARSER.get( 'facebook', 'test_photo'), 'rb')
##    graph.put_photo(
##        image=open(image_to_post, 'rb'),
##        album_path=CONFIG_PARSER.get('facebook', 'test_album_id') + "/photos")

