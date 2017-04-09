
import time as time
import uuid

import cv2
import numpy as np

#import zope.event.classhandler
import stitch as stitch
import zope.event
from PIL import Image

SIZE = (640, 480)
SINGLE_PHOTOS_DIR = '/media/pi/88DB-D77C/photos/singles'
PHOTO_BATCH_SIZE = 4
TIME_BETWEEN_PHOTOS = -2
PHOTO_TAKEN = 'photo_taken'


class App:
    """main"""
    start_time = 0
    now_time = 0
    batch_id = None
    is_processing = False
    video_capture = None
    num_of_photos = PHOTO_BATCH_SIZE

    def __init__(self):
        self._running = True

    def on_init(self):
        """called on startup"""
        zope.event.subscribers.append(self.on_enter)
        zope.event.subscribers.append(self.on_exit)
        #zope.event.classhandler.handler(np.ndarray, self.captureimage)
        zope.event.subscribers.append(self.captureimage)
        zope.event.subscribers.append(self.after_image_capture)
        cv2.namedWindow("preview")
        self.video_capture = cv2.VideoCapture(0)
        self._running = True
        # one_image = cv2.resize(cv2.imread('./1.jpg'), (800, 600))
        # two_image = cv2.resize(cv2.imread('./2.jpg'), (800, 600))
        # three_image = cv2.resize(cv2.imread('./3.jpg'), (800, 600))
        # white_image = cv2.resize(cv2.imread('./flash.png'), (800, 600))

    def time_reached(self):
        """works out if we have passed the alotted time between each photo being taken"""
        return (self.start_time - self.now_time) == TIME_BETWEEN_PHOTOS

    def should_take_photo(self):
        """logic for taking photo"""
        return self.time_reached() and (self.is_processing) and (self.num_of_photos > 0)

    def on_enter(self, event):
        """handles enter key being pushed, starts the batch processing"""
        if isinstance(event, int):
            if event == 10:  # enter key to start batch
                self.is_processing = True
                self.start_time = self.now_time
                self.batch_id = uuid.uuid4()
                # show count down images?
                print 'starting batch: {0} at time: {1}'.format(self.batch_id, self.now_time)

    def on_exit(self, event):
        """closes the program is exit is hit"""
        if isinstance(event, int):
            if event == 27:  # exit on ESC
                stitch.stitch_photos(self.batch_id)
                self._running = False

    def on_loop(self):
        """loop"""
        self.now_time = int(time.time())
        #if self.should_take_photo():
        frame = self.video_capture.read()[1]
        zope.event.notify(frame)  # take photo
            #self.after_image_capture()
        #else:
         #   pass

    def after_image_capture(self, event):
        """handles event photo_taken and increments the photo count"""
        if isinstance(event, str) and event == PHOTO_TAKEN: #make sure it is a string
            if self.num_of_photos == 1:  # we have taken the last photo of the batch
                stitch.stitch_photos(self.batch_id)  # put the photos together
                print 'processed batch:{0} press enter to start next batch'.format(self.batch_id)
                self.is_processing = False  # we are not taking a photos to set this false
                self.batch_id = None  # remove batch_id
                # set the number of photos back to default
                self.num_of_photos = PHOTO_BATCH_SIZE
            else:
                # we are still taking photos so just decrement by 1
                self.num_of_photos = self.num_of_photos - 1
                # always override the start time when we are taking photos
                self.start_time = self.now_time

    def on_render(self):
        """render?"""
        pass

    def on_cleanup(self):
        """close the program"""
        self._running = False
        cv2.destroyWindow("preview")

    def captureimage(self, event):
        """write the current frame to disk"""
        if isinstance(event, np.ndarray) and self.should_take_photo():
            name = '{0}/{1}-photo-{2}.png'.format(
                SINGLE_PHOTOS_DIR, self.batch_id, int(time.time()))
            print 'taking photo {0}'.format(name)
            cv2.imwrite(name, event)
            zope.event.notify(PHOTO_TAKEN)

    def on_execute(self):
        """first thing to be called"""
        if self.on_init() is False:
            self._running = False

        while self.video_capture.isOpened() and self._running:
            frame = self.video_capture.read()[1]
            cv2.imshow("preview", frame)
            key = cv2.waitKey(20)
            zope.event.notify(key)
            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    App().on_execute()
