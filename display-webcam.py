import cv2
import numpy as np

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
        photonum = 1

for x in range(1, photonum):
    print(x)
    
img1 = cv2.imread('./photos/{0}photo-{1}.png'.format(foldernum, photonum))
img2 = cv2.imread('./photos/{0}photo-{1}.png'.format(foldernum-1, photonum-1))
img2 = cv2.imread('./photos/{0}photo-{1}.png'.format(foldernum-2, photonum-2))
img2 = cv2.imread('./photos/{0}photo-{1}.png'.format(foldernum-1, photonum-1))
vis = np.concatenate((img1, img2, img3, im4), axis=1)
cv2.imwrite('/photos/out.png', vis)
        
cv2.destroyWindow("preview") 
