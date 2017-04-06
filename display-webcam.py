import cv2
import numpy as np
import sys
from PIL import Image
import time as time
import  multiprocessing as mp
photonum=1

def captureimage(photonum, frame):
     name = './photos/photo-{0}.png'.format(photonum)
     print 'taking photo {0}'.format(name)
     #img = Image.fromarray(frame)
     #img.save(name)
     cv2.imwrite(name, frame)

def stichphotos():
    print 'stiching photos there are: {0}'.format(photonum-1)
    if photonum-1 == 0:
        return
    list_im = []
    for x in range(1, photonum):
        list_im.append('./photos/photo-{0}.png'.format(x))
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

def takephotos(vc):
     num = 1
     print num
     print 'starting inner while'
     global photonum
     start_time = int(time.time())
     while num < 5:
          now_time= int(time.time())
          rval, photoframe = vc.read()
          print 'inside inner while'
          test = cv2.imshow("preview", photoframe)
          print test
          if start_time - now_time == -1:
               print type(photoframe)
               captureimage(photonum,photoframe)
               cv2.imshow("preview", photoframe)
               start_time=now_time
               num = num+1
               photonum = photonum + 1


     
#kick off the window opening
def start():
     cv2.namedWindow("preview")
     vc = cv2.VideoCapture(0)

     if vc.isOpened(): # try to get the first frame
         grab, frame = vc.read()
     else:
         grab = False
     pool = mp.Pool()
     while vc.isOpened():
         cv2.imshow("preview", frame)
         grab, frame = vc.read()
         key = cv2.waitKey(20)
         if key == 27: # exit on ESC
             stichphotos()
             break
         if key == 10: #enter key
               #captureimage(photonum,frame)
               #photonum = photonum + 1
             pool.apply_async(takephotos(vc))
         if key == 116: #t
             stichphotos()
             print 'restarting next batch'
             global photonum
             photonum=1
             
     cv2.destroyWindow("preview, enter to take, t to start again")


start()




