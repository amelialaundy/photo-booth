import twitter
import ConfigParser

configParser = ConfigParser.RawConfigParser()   
configFilePath = r'../keys.txt'
configParser.read(configFilePath)

api = twitter.Api(consumer_key=configParser.get('keys', 'consumer_key'),
                      consumer_secret=configParser.get('keys', 'consumer_secret'),
                      access_token_key=configParser.get('keys', 'access_token'),
                      access_token_secret=configParser.get('keys', 'access_secret'))
user = api.VerifyCredentials()
print(user)



statuses = api.GetUserTimeline(screen_name=user)
print statuses

status = api.PostUpdate('testing')
print status.text
