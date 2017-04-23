import ConfigParser

import facebook

CONFIG_PARSER = ConfigParser.RawConfigParser()
CONFIG_FILE_PATH = r'../keys.txt'
CONFIG_PARSER.read(CONFIG_FILE_PATH)

def post_to_facebook(image_to_post):
    '''reads from config the access_token and album id and posts image to FB'''
    graph = facebook.GraphAPI(
        access_token=CONFIG_PARSER.get('facebook', 'access_token_photo_booth'),
        version='2.7')
        #image=open(CONFIG_PARSER.get('facebook', 'test_photo'), 'rb')
    graph.put_photo(
        image=open(image_to_post, 'rb'),
        album_path=CONFIG_PARSER.get('facebook', 'test_album_id') + "/photos")
