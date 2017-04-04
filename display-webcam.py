import cv2
import numpy as np
import sys
from PIL import Image
import time as time

# testing
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
foldernum = 1
photonum=1
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    if key == 10:
        name = './photos/{0}photo-{1}.png'.format(foldernum,photonum)
        print 'taking photo {0}'.format(name)
        #borderimg = cv2.rectangle(frame,(384,0),(510,128),(0,255,0),2)
        cv2.imwrite(name, frame)
        photonum = photonum + 1
    if key == 116: #t
        print 'restarting'
        img1 = cv2.imread('./photos/1photo-1.png')
        img2 = cv2.imread('./photos/1photo-2.png')
        vis = np.concatenate((img1, img2), axis=0)
        cv2.imwrite('./photos/out.png', vis)
        foldernum = foldernum +1
        photonum = photonum + 1

imagesarr = []
for x in range(1, photonum-1):
    print('hi',x)
    imagesarr.append(cv2.imread('./photos/{0}photo-{1}.png'.format(1, x)))


imagenames = []
for x in range(1, photonum-1):
    print('hi',x)
    imagenames.append('./photos/{0}photo-{1}.png'.format(1, x))
  
##img1 = cv2.imread('./photos/{0}photo-{1}.png'.format(foldernum, photonum))
##img2 = cv2.imread('./photos/{0}photo-{1}.png'.format(foldernum-1, photonum-1))
##img2 = cv2.imread('./photos/{0}photo-{1}.png'.format(foldernum-2, photonum-2))
##img2 = cv2.imread('./photos/{0}photo-{1}.png'.format(foldernum-1, photonum-1))
##vis = np.concatenate((images[0],images[1],images[2]), axis=1)

##cv2.imwrite('/photos/out.png', vis)
## works horixontally
##images = map(Image.open, imagenames)
##widths, heights = zip(*(i.size for i in images))
##
##total_width = max(widths)
##max_height = sum(heights)
##
##new_im = Image.new('RGB', (total_width, max_height))
##
##x_offset = 0
##for im in images:
##  new_im.paste(im, (x_offset,0))
##  x_offset += im.size[0]
##
##new_im.save('./photos/test.jpg')        

list_im = imagenames
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
cv2.destroyWindow("preview") 
