
from PIL import Image

photos = Image.open('/media/pi/88DB-D77C/photos/vertical/Vertical-1491810510.png')
original_photo_size = photos.size
print 'original_photo_size {}'.format(original_photo_size)

shark_im = Image.open('/media/pi/88DB-D77C/photos/resized_shark_im.png')
#shark_im.resize()
original_shark_im_size = shark_im.size
print original_shark_im_size
print 'original_shark_im_size {}'.format(original_shark_im_size)

new_shark = shark_im.resize((900, 1800))
print new_shark.size
new_shark.save('./stretch-shark.png')
shark_size = shark_im.size
print 'new shark im size {}'.format(shark_im.size)



new_size = (900, 1700)
photo_with_blank_border = Image.new("RGB", new_size)   ## luckily, this is already black!

photo_with_blank_border.paste(photos, ((photo_with_blank_border.size[0]-original_photo_size[0])/2,
                      (photo_with_blank_border.size[1]-original_photo_size[1])/2))
#photo_with_blank_border.save('./photo_with_blank_border1.png')
