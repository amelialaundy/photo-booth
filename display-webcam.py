import cv2
import time
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
    if key == 1048603: # exit on ESC
        break
    if key == 1048586:
        name = './photos/{0}photo-{1}.png'.format(foldernum,photonum)
        print 'taking photo {0}'.format(name)
        #borderimg = cv2.rectangle(frame,(384,0),(510,128),(0,255,0),2)
        cv2.imwrite(name,frame)
        photonum = photonum + 1
    if key == 1048675:
        print 'restarting'
        foldernum = foldernum +1
        photonum = 1
        
cv2.destroyWindow("preview") 
