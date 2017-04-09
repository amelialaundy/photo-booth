import os
import sys
from PIL import Image
import time as time
import numpy as np
PHOTOS_DIR = '/media/pi/88DB-D77C/photos'
SINGLE_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/singles'
VERTICAL_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/vertical'
HORIZONTAL_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/horizontal'

def stitch_photos(batch_id):
    photos = os.listdir(SINGLE_PHOTOS_DIR)
    matching = []
    for photo in photos:
        if photo.startswith(str(batch_id)):
            matching.append('{0}/{1}'.format(SINGLE_PHOTOS_DIR, photo))

    number = len(matching)
    if number == 0:
        return
    print 'stiching photos there are: {0}'.format(number)
    print 'photos taken:'
    for image_name in matching:
        print image_name

    imgs = [Image.open(i) for i in matching]
    # pick the image which is the smallest, and resize the others to match it
    # (can be arbitrary image shape here)
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

    # save that beautiful picture
    imgs_comb = Image.fromarray(imgs_comb)
    horizontal_image_name = '{0}/Horizontal-{1}.jpg'.format(
        HORIZONTAL_PHOTOS_DIR, int(time.time()))
    imgs_comb.save(horizontal_image_name)
    print 'saved horiztonal image: {0}'.format(horizontal_image_name)

    # for a vertical stacking it is simple: use vstack
    imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
    imgs_comb = Image.fromarray(imgs_comb)
    vertical_image_name = '{0}/Vertical-{1}.jpg'.format(
        VERTICAL_PHOTOS_DIR, int(time.time()))
    imgs_comb.save(vertical_image_name)
    print 'saved vertical image: {0}'.format(horizontal_image_name)


# if __name__ == "__main__":
#     dostuff()
