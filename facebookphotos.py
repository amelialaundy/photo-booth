import facebook
import ConfigParser

configParser = ConfigParser.RawConfigParser()   
configFilePath = r'../keys.txt'
configParser.read(configFilePath)

graph = facebook.GraphAPI(access_token=configParser.get('facebook', 'access_token_photo_booth'), version='2.7')
graph.put_photo(image=open(configParser.get('facebook', 'test_photo'), 'rb'), album_path=configParser.get('facebook', 'test_album_id') + "/photos")
