
import cv2
import uuid
import numpy as np
import sys
from PIL import Image
import time as time
import os
import zope.event
#import zope.event.classhandler
import stitch as stitch

SIZE = (640, 480)
SINGLE_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/singles'
PHOTO_BATCH_SIZE = 4
TIME_BETWEEN_PHOTOS = -2


class App:
    start_time = 0
    now_time = 0
    batch_id = None
    has_started = False
    vc = None
    num_of_photos = PHOTO_BATCH_SIZE

    def __init__(self):
        self._running = True

    def on_init(self):
        zope.event.subscribers.append(self.on_enter)
        zope.event.subscribers.append(self.on_exit)
        #zope.event.classhandler.handler(np.ndarray, self.captureimage)
        zope.event.subscribers.append(self.captureimage)
        cv2.namedWindow("preview")
        self.vc = cv2.VideoCapture(0)
        self._running = True
        # one_image = cv2.resize(cv2.imread('./1.jpg'), (800, 600))
        # two_image = cv2.resize(cv2.imread('./2.jpg'), (800, 600))
        # three_image = cv2.resize(cv2.imread('./3.jpg'), (800, 600))
        # white_image = cv2.resize(cv2.imread('./flash.png'), (800, 600))

    def take_photo(self):
        return ((self.start_time - self.now_time) == TIME_BETWEEN_PHOTOS) and (self.has_started) and (self.num_of_photos > 0)
    def on_enter(self, event):
        if type(event) is int:
            if event == 10:  # enter key to start batch
                self.has_started = True
                self.start_time = self.now_time
                self.batch_id = uuid.uuid4()
                #show count down images?
                print 'starting batch: {0} at time: {1}'.format(self.batch_id, self.now_time)

    def on_exit(self, event):
        if type(event) is int:
            if event == 27:  # exit on ESC
                stitch.stitch_photos(self.batch_id)
                self._running = False

    def on_loop(self):
        self.now_time = int(time.time())
        if self.take_photo():
            grab, frame = self.vc.read()
            zope.event.notify(frame) #take photo
            self.after_image_capture()
        else:
            pass

    def after_image_capture(self):
        if (self.num_of_photos == 1):  # we have taken the last photo of the batch
            stitch.stitch_photos(self.batch_id)  # put the photos together
            print 'processed batch:{0} press enter to start next batch'.format(self.batch_id)
            self.has_started = False  # we are not taking a photos to set this false
            self.batch_id = None  # remove batch_id
            self.num_of_photos = PHOTO_BATCH_SIZE  # set the number of photos back to default
        else:
            # we are still taking photos so just decrement by 1
            self.num_of_photos = self.num_of_photos - 1
            # always override the start time when we are taking photos
            self.start_time = self.now_time
    def on_render(self):
        pass

    def on_cleanup(self):
        self._running = False
        cv2.destroyWindow("preview")

    def captureimage(self, event):
        if type(event) is np.ndarray:
            print type(event) is np.ndarray
            name = '{0}/{1}-photo-{2}.png'.format(
                SINGLE_PHOTOS_DIR, self.batch_id, int(time.time()))
            print 'taking photo {0}'.format(name)
            cv2.imwrite(name, event)
        
    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self.vc.isOpened() and self._running:
            grab, frame = self.vc.read()
            cv2.imshow("preview", frame)
            key = cv2.waitKey(20)
            zope.event.notify(key)
            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
