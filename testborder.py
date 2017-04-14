##import cv2
##import numpy as np
##
##print " Press r to replicate the border with a random color "
##print " Press c to replicate the border "
##print " Press Esc to exit "
##
##img = cv2.imread('/media/pi/88DB-D77C/photos/vertical/Vertical-1491810510.jpg')
##rows,cols = img.shape[:2]
##
##dst = img.copy()
##
##top = int (0.05*rows)
##bottom = int (0.05*rows)
##
##left = int (0.05*cols)
##right = int (0.05*cols)
##
##while(True):
##    
##    cv2.imshow('border',dst)
##    k = cv2.waitKey(500)
##    
##    if k==27:
##        break
##    elif k == ord('c'):
##        value = np.random.randint(0,255,(3,)).tolist()
##        print type(value)
##        dst = cv2.copyMakeBorder(img,top,bottom,left,right,cv2.BORDER_CONSTANT,value = value)
##    elif k == ord('r'):
##        dst = cv2.copyMakeBorder(img,top,bottom,left,right,cv2.BORDER_REPLICATE)
##
##cv2.destroyAllWindows()

from PIL import Image

photos = Image.open('/media/pi/88DB-D77C/photos/vertical/Vertical-1491810510.png')
original_photo_size = photos.size
print 'original_photo_size {}'.format(original_photo_size)

shark_im = Image.open('/home/pi/projects/photo-booth/stretch-shark.png')
original_shark_im_size = shark_im.size
print 'original_shark_im_size {}'.format(original_shark_im_size)

shark_size = shark_im.size
print 'new shark im size {}'.format(shark_im.size)



new_size = (900, 1700)
photo_with_blank_border = Image.new("RGB", new_size)   ## luckily, this is already black!

photo_with_blank_border.paste(photos, ((photo_with_blank_border.size[0]-original_photo_size[0])/2,
                      (photo_with_blank_border.size[1]-original_photo_size[1])/2))
photo_with_blank_border.save('./photo_with_blank_border1.png')


new_photo_with_blank_border_size = photo_with_blank_border.size #photo with a black border around it

photo_with_blank_border.paste(shark_im, (0,0),shark_im) #this is the magic



photos.paste(shark_im, ((shark_size[0]+original_photo_size[0])/2,
                      (shark_size[1]+original_photo_size[1])/2))

shark_im.paste(photos, ((shark_size[0]-original_photo_size[0])/2,
                      (shark_size[1]-original_photo_size[1])/2))
#return cv2.addWeighted(self.count_down_images[str(seconds_until_next_photo)], 0.5, self.video_capture.read()[1], 0.5, 0.0)

photos.save('./old_im.png')
shark_im.save('./shark_im.png')
photo_with_blank_border.save('./photo_with_blank_border.png') #this works
