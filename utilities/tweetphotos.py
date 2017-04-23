import ConfigParser

import twitter

CONFIG = ConfigParser.RawConfigParser()
CONFIG_FILE_PATH = r'../keys.txt'
CONFIG.read(CONFIG_FILE_PATH)

def post_to_twitter(text, image):
    print text
    print image
    api = twitter.Api(consumer_key=CONFIG.get('keys', 'consumer_key'),
                      consumer_secret=CONFIG.get('keys', 'consumer_secret'),
                      access_token_key=CONFIG.get('keys', 'access_token'),
                      access_token_secret=CONFIG.get('keys', 'access_secret'))
    user = api.VerifyCredentials()
    #print(user)



    #statuses = api.GetUserTimeline(screen_name=user)
    #print statuses

    #status = api.PostUpdate(text, image)
    #print status.text


#post_to_twitter('hey alex','/media/pi/88DB-D77C/photos/horizontal/Horizontal-1491905533.jpg')
