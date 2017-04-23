import os
import sys
from PIL import Image
import time as time
import numpy as np
import tweetphotos
import facebookphotos
PHOTOS_DIR = '/media/pi/88DB-D77C/photos'
BLANK_IMAGE = '/media/pi/88DB-D77C/photos/blank_photo.png'
SHARK_IMAGE = '/media/pi/88DB-D77C/photos/stretch-shark.png'


class Stitch(object):
    '''stiches given photos together based on batch id'''
    save_horizontal = False
    post_to_twitter = False
    post_to_fb = False

    def __init__(self):
        self.single_photos_dir = '{0}/singles'.format(PHOTOS_DIR)
        self.vertical_photos_dir = '{0}/vertical'.format(PHOTOS_DIR)
        self.horizontal_photos_dir = '{0}/horizontal'.format(PHOTOS_DIR)
        self.shark_dir = '{0}/sharky'.format(PHOTOS_DIR)
        self.shark_image = Image.open(SHARK_IMAGE)
        self.base_image = Image.open(BLANK_IMAGE)



    def stitch_photos(self, batch_id):
        """saves a vertical and a horiztonal image of all of the images in the batch"""
        #get the photos from this batch
        matching = self.__get_photo_batch(batch_id)
        if len(matching) == 0:
            return

        imgs = [Image.open(i) for i in matching]
        # pick the image which is the smallest, and resize the others to match it
        # (can be arbitrary image shape here)
        min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

        if self.save_horizontal:
            self.__make_horizontal(min_shape, imgs)
        vertical_image_path = self.__make_vertical(min_shape, imgs)
        shark_image_path = self.__add_shark_border(vertical_image_path)
        self.__share(shark_image_path)

    def __add_shark_border(self, photo):
        '''creates blank image, pastes photo onto it in middle, then overlays the shark border'''
        photo = Image.open(photo)
        background = self.base_image.copy()

        paste_location = self.__get_paste_location(background.size, photo.size)
        #paste the photo in middle of it
        background.paste(photo, paste_location)

        #this is the magic, put the shark border over the top
        background.paste(self.shark_image, (0, 0), self.shark_image)
        sharkified_image = self.__get_shark_image_name()
        background.save(sharkified_image)
        print 'saved sharky image: {0}'.format(sharkified_image)
        return sharkified_image

    def __make_horizontal(self, min_shape, imgs):
        '''makes an array of the images into a wide image then saves'''
        # resize the images to be the same size
        image_array = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

        horizontal_image = Image.fromarray(image_array)
        horizontal_image_name = self.__get_horizontal_image_name()
        horizontal_image.save(horizontal_image_name)
        print 'saved horiztonal image: {0}'.format(horizontal_image_name)
        return horizontal_image

    def __make_vertical(self, min_shape, imgs):
        '''stacks the images vertically then saves'''
        imgs_stack = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
        vertical_image = Image.fromarray(imgs_stack)
        vertical_image_name = self.__get_vertical_image_name()
        vertical_image.save(vertical_image_name)
        print 'saved vertical image: {0}'.format(vertical_image_name)
        return vertical_image_name

    def __get_photo_batch(self, batch_id):
        '''finds the photos in the directory that belong to this batch_id'''
        photos = os.listdir(self.single_photos_dir)
        matching = []
        for photo in photos:
            if photo.startswith(str(batch_id)):
                matching.append('{0}/{1}'.format(self.single_photos_dir, photo))
        return matching

    def __get_paste_location(self, backgound_size, image_to_paste_size):
        location_to_paste_x = (backgound_size[0]-image_to_paste_size[0])/2
        location_to_paste_y = (backgound_size[1]-image_to_paste_size[1])/2
        return (location_to_paste_x, location_to_paste_y)

    def __get_horizontal_image_name(self):
        return '{0}/Horizontal-{1}.jpg'.format(self.horizontal_photos_dir, int(time.time()))

    def __get_vertical_image_name(self):
        return '{0}/Vertical-{1}.jpg'.format(self.vertical_photos_dir, int(time.time()))

    def __get_shark_image_name(self):
        return '{0}/sharky-{1}.jpg'.format(self.shark_dir, int(time.time()))

    def __share(self, image_path):
        if self.post_to_twitter:
            tweetphotos.post_to_twitter('works on my machine', image_path)
        if self.post_to_fb:
            facebookphotos.post_to_facebook(image_path)
