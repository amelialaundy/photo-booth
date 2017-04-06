import cv2
import numpy as np
import sys
from PIL import Image
import time as time
import  multiprocessing as mp
import os, sys
import uuid
photos_dir = '/media/pi/88DB-D77C/photos'
single_photos_dir = '/media/pi/88DB-D77C/photos/singles'
vertical_photos_dir = '/media/pi/88DB-D77C/photos/vertical'
horizontal_photos_dir = '/media/pi/88DB-D77C/photos/horizontal'
photo_batch_size = 4
time_between_photos = -1

def captureimage(frame, batch_id):
    name = '{0}/{1}-photo-{2}.png'.format(single_photos_dir,batch_id, int(time.time()))
    print 'taking photo {0}'.format(name)
    #img = Image.fromarray(frame)
    #img.save(name)
    cv2.imwrite(name, frame)

def stichphotos(batch_id):

    photos = os.listdir( single_photos_dir )
    matching = []
    for photo in photos:
        if photo.startswith(str(batch_id)):
            matching.append('{0}/{1}'.format(single_photos_dir,photo))
                            
    number = len(matching)
    if (number== 0):
        return
    print 'stiching photos there are: {0}'.format(number)
    print 'photos taken:'
    for image_name in matching:
        print image_name
    
    imgs    = [ Image.open(i) for i in matching ]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

    # save that beautiful picture
    imgs_comb = Image.fromarray( imgs_comb)
    horizontal_image_name =  '{0}/Horizontal-{1}.jpg'.format(horizontal_photos_dir,int(time.time()))
    imgs_comb.save(horizontal_image_name)
    print 'saved horiztonal image: {0}'.format(horizontal_image_name)

    # for a vertical stacking it is simple: use vstack
    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    imgs_comb = Image.fromarray( imgs_comb)
    vertical_image_name = '{0}/Vertical-{1}.jpg'.format(vertical_photos_dir, int(time.time()))
    imgs_comb.save(vertical_image_name)
    print 'saved vertical image: {0}'.format(horizontal_image_name)

#kick off the window opening
def start():

    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    has_started = False
        
    start_time = int(time.time())
    batch_id = uuid.uuid4()
    num_of_photos = photo_batch_size
    while vc.isOpened():
        
        grab, frame = vc.read()
        cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
        now_time= int(time.time())

        if key == 27: # exit on ESC
            stichphotos(batch_id)
            break
        if key == 10: #enter key to start batch
            has_started = True
            start_time=now_time
            batch_id = uuid.uuid4()
            print 'starting batch: {0} at time: {1}'.format(batch_id, now_time)
##        if key == 116: #t start againt a new batch
##            has_started = False
##            stichphotos(batch_id)
##            
##            batch_id = None 
##            num_of_photos = photo_batch_size
            

        if (start_time - now_time == time_between_photos) and (has_started) and (num_of_photos > 0):
            captureimage(frame, batch_id)
            if (num_of_photos == 1): #we have taken the last photo of the batch
                stichphotos(batch_id) #put the photos together
                print 'processed batch:{0} press enter to start next batch'.format(batch_id)
                has_started = False #we are not taking a photos to set this false
                batch_id = None # remove batch_id
                num_of_photos = photo_batch_size #set the number of photos back to default
            else:
                num_of_photos=num_of_photos-1 #we are still taking photos so just decrement by 1
                start_time=now_time #always override the start time when we are taking photos

    cv2.destroyWindow("preview")


start()
