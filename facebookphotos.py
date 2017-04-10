import facebook
import ConfigParser

configParser = ConfigParser.RawConfigParser()   
configFilePath = r'../keys.txt'
configParser.read(configFilePath)

graph = facebook.GraphAPI(access_token=configParser.get('facebook', 'access_token_photo_booth'), version='2.7')
graph.put_photo(image=open("/media/pi/88DB-D77C/photos/vertical/Vertical-1491810510.jpg", 'rb'), album_path='151959131998755' + "/photos")
