import os
import sys
from PIL import Image
import time as time
import numpy as np
import tweetphotos
import facebookphotos

PHOTOS_DIR = '/media/pi/88DB-D77C/photos'
SINGLE_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/singles'
VERTICAL_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/vertical'
HORIZONTAL_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/horizontal'
SHARK_DIR = '/media/pi/88DB-D77C/photos/sharky'
SHARK_IMAGE = '/media/pi/88DB-D77C/photos/stretch-shark.png'
SAVE_HORIZONTAL = False
POST_TWITTER = False
POST_TO_FB = True

def get_photo_batch(batch_id):
    '''finds the photos in the directory that belong to this batch_id'''
    photos = os.listdir(SINGLE_PHOTOS_DIR)
    matching = []
    for photo in photos:
        if photo.startswith(str(batch_id)):
            matching.append('{0}/{1}'.format(SINGLE_PHOTOS_DIR, photo))
    return matching

def stitch_photos(batch_id):
    """saves a vertical and a horiztonal image of all of the images in the batch"""
    #get the photos from this batch
    matching = get_photo_batch(batch_id)

    number = len(matching)
    if number == 0:
        return
    print 'stiching photos there are: {0}'.format(number)

    imgs = [Image.open(i) for i in matching]
    # pick the image which is the smallest, and resize the others to match it
    # (can be arbitrary image shape here)
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

    if SAVE_HORIZONTAL:
        make_horizontal(min_shape, imgs)
    vertical_image = make_vertical(min_shape, imgs)
    shark_image = add_shark_border(vertical_image)
    if POST_TWITTER:
        tweetphotos.post_to_twitter('works on my machine', shark_image)
    if POST_TO_FB:
        facebookphotos.post_to_facebook(vertical_image)

def add_shark_border(photo):
    '''creates blank larger image, pastes photo onto it in middle, then overlays the shark border'''
    original_photo_size = photo.size
    shark_im = Image.open(SHARK_IMAGE)
    new_size = (900, 1700)
    #create a new blank black image
    photo_with_blank_border = Image.new("RGB", new_size)  #blank image same size as shark border

    location_to_paste_x = (photo_with_blank_border.size[0]-original_photo_size[0])/2
    location_to_paste_y = (photo_with_blank_border.size[1]-original_photo_size[1])/2
    #paste the photo in middle of it
    photo_with_blank_border.paste(
        photo,
        (location_to_paste_x, location_to_paste_y))

    #this is the magic, put the shark border over the top
    photo_with_blank_border.paste(shark_im, (0, 0), shark_im)
    image_name = '{0}/sharky-{1}.jpg'.format(
        SHARK_DIR, int(time.time()))
    photo_with_blank_border.save(image_name)
    print 'saved sharky image: {0}'.format(image_name)
    return photo_with_blank_border

def make_horizontal(min_shape, imgs):
    '''makes an array of the images into a wide image then saves'''
    # resize the images to be the same size
    image_array = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

    horizontal_image = Image.fromarray(image_array)
    horizontal_image_name = '{0}/Horizontal-{1}.jpg'.format(
        HORIZONTAL_PHOTOS_DIR, int(time.time()))
    horizontal_image.save(horizontal_image_name)
    print 'saved horiztonal image: {0}'.format(horizontal_image_name)
    return horizontal_image

def make_vertical(min_shape, imgs):
    '''stacks the images vertically then saves'''
    imgs_stack = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
    vertical_image = Image.fromarray(imgs_stack)
    vertical_image_name = '{0}/Vertical-{1}.jpg'.format(
        VERTICAL_PHOTOS_DIR, int(time.time()))
    vertical_image.save(vertical_image_name)
    print 'saved vertical image: {0}'.format(vertical_image_name)
    return vertical_image
