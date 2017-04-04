import cv2
import numpy as np
import sys
from PIL import Image
import time as time
foldernum = 1
photonum=1

def captureimage(folder, photo, frame):
     name = './photos/{0}photo-{1}.png'.format(folder,photo)
     print 'taking photo {0}'.format(name)
     cv2.imwrite(name, frame)

def stichphotos():
    print 'stiching photos there are: {0}'.format(photonum-1)
    if photonum-1 == 0:
        return
    list_im = []
    for x in range(1, photonum):
        list_im.append('./photos/{0}photo-{1}.png'.format(1, x))
    print list_im
    imgs    = [ Image.open(i) for i in list_im ]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

    # save that beautiful picture
    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.save( './photos/Horizontal-{}.jpg'.format(int(time.time())) )    

    # for a vertical stacking it is simple: use vstack
    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.save( './photos/Vertical-{}.jpg'.format(int(time.time())) )

 
#kick off the window opening
cv2.namedWindow("preview, enter to take, t to start again")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview, enter to take, t to start again", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        stichphotos()
        break
    if key == 10:
        captureimage(foldernum,photonum,frame)
        photonum = photonum + 1
    if key == 116: #t
        stichphotos()
        print 'restarting next batch'
        foldernum = foldernum +1
        photonum=1

cv2.destroyWindow("preview, enter to take, t to start again") 
