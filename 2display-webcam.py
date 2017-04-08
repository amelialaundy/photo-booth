import os
import sys
import time as time
import uuid

import cv2
import numpy as np

from PIL import Image

PHOTOS_DIR = '/media/pi/88DB-D77C/photos'
SINGLE_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/singles'
VERTICAL_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/vertical'
HORIZONTAL_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/horizontal'
PHOTO_BATCH_SIZE = 4
TIME_BETWEEN_PHOTOS = -1


def captureimage(frame, batch_id):
    name = '{0}/{1}-photo-{2}.png'.format(SINGLE_PHOTOS_DIR, batch_id, int(time.time()))
    print 'taking photo {0}'.format(name)
    #img = Image.fromarray(frame)
    # img.save(name)
    cv2.imwrite(name, frame)


def stichphotos(batch_id):

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

# kick off the window opening


def start():

    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    has_started = False

    start_time = int(time.time())
    batch_id = uuid.uuid4()
    num_of_photos = PHOTO_BATCH_SIZE
    one_image = cv2.resize(cv2.imread('./1.jpg'), (800, 600))
    two_image = cv2.resize(cv2.imread('./2.jpg'), (800, 600))
    three_image = cv2.resize(cv2.imread('./3.jpg'), (800, 600))
    white_image = cv2.resize(cv2.imread('./whiteflash.png'), (800, 600))
    while vc.isOpened():

        grab, frame = vc.read()
        cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
        now_time = int(time.time())

        if key == 27:  # exit on ESC
            stichphotos(batch_id)
            break
        if key == 10:  # enter key to start batch
            has_started = True
            start_time = now_time
            batch_id = uuid.uuid4()
            cv2.imshow("preview", three_image)
            cv2.waitKey(400)
            cv2.imshow("preview", two_image)
            cv2.waitKey(400)
            cv2.imshow("preview", one_image)
            cv2.waitKey(20)
            print 'starting batch: {0} at time: {1}'.format(batch_id, now_time)

        if (start_time - now_time == TIME_BETWEEN_PHOTOS) and (has_started) and (num_of_photos > 0):
            cv2.imshow("preview", white_image)
            cv2.waitKey(20)
            captureimage(frame, batch_id)
            if num_of_photos == 1:  # we have taken the last photo of the batch
                stichphotos(batch_id)  # put the photos together
                print 'processed batch:{0} press enter to start next batch'.format(batch_id)
                has_started = False  # we are not taking a photos to set this false
                batch_id = None  # remove batch_id
                num_of_photos = PHOTO_BATCH_SIZE  # set the number of photos back to default
            else:
                # we are still taking photos so just decrement by 1
                num_of_photos = num_of_photos - 1
                start_time = now_time  # always override the start time when we are taking photos

    cv2.destroyWindow("preview")


start()
