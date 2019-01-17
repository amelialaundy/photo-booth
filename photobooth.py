import sys

sys.path.append('/home/pi/Projects/photo-booth/utilities')
import threading
import time as time
import uuid

import cv2
import numpy as np

#import zope.event.classhandler
from stitch import Stitch
import zope.event
from PIL import Image

SIZE = (640, 480)
SINGLE_PHOTOS_DIR = '/media/pi/88DB-D77C1/photos/singles'
PHOTO_BATCH_SIZE = 3
TIME_BETWEEN_PHOTOS = 5
PHOTO_TAKEN = 'photo_taken'

ADELE_PHOTO = '/media/pi/88DB-D77C1/photos/adele-polaroid-resized.png'

class App:
    """main"""
    start_time = 0
    now_time = 0
    batch_id = None
    is_processing = False
    video_capture = None
    num_of_photos = PHOTO_BATCH_SIZE
    count_down_images = None
    adele_image = None

    def __init__(self):
        self._running = True
        cv2.imread('./1.jpg')
        one_image = cv2.resize(cv2.imread('./1.jpg'), SIZE)
        two_image = cv2.resize(cv2.imread('./2.jpg'), SIZE)
        three_image = cv2.resize(cv2.imread('./3.jpg'), SIZE)
        self.adele_image = cv2.resize(cv2.imread('./Splash.png'), SIZE)
        self.count_down_images = {'1': one_image, '2': two_image, '3': three_image}
         
    def on_init(self):
        """called on startup"""
        zope.event.subscribers.append(self.on_enter)
        zope.event.subscribers.append(self.on_exit)
        zope.event.subscribers.append(self.captureimage)
        zope.event.subscribers.append(self.after_image_capture)
        cv2.namedWindow("preview")
        self.video_capture = cv2.VideoCapture(0)
        self._running = True


    def time_reached(self):
        """works out if we have passed the alotted time between each photo being taken"""
        return self.seconds_until_next_photo() == 0

    def should_take_photo(self):
        """logic for taking photo"""
        return self.time_reached() and (self.is_processing) and (self.num_of_photos > 0)

    def on_enter(self, event):
        
        """handles enter key event, starts the batch processing"""
        if isinstance(event, int):
            if event == 10:  # enter key to start batch
                self.is_processing = True
                self.start_time = self.now_time
                self.batch_id = uuid.uuid4()
                print 'starting batch: {0} at time: {1}'.format(self.batch_id, self.now_time)

    def on_exit(self, event):
        """handles esc key event,exit program"""
        if isinstance(event, int) and event == 27:
            stitch.stitch_photos(self.batch_id) # exit on ESC
            self._running = False

    def captureimage(self, event):
        """handles frame event, write the current frame to disk"""
        if isinstance(event, np.ndarray) and self.should_take_photo():
            name = '{0}/{1}-photo-{2}.png'.format(
                SINGLE_PHOTOS_DIR, self.batch_id, int(time.time()))
            print 'taking photo {0}'.format(name)
            cv2.imwrite(name, event)
            zope.event.notify(PHOTO_TAKEN)

    def after_image_capture(self, event):
        """handles event photo_taken and increments the photo count"""
        if isinstance(event, str) and event == PHOTO_TAKEN: #make sure it is a string
            if self.num_of_photos == 1:  # we have taken the last photo of the batch
                #start the stitching in a new thread
                thread = threading.Thread(target=Stitch.stitch_photos, args=(Stitch(), self.batch_id,))
                thread.daemon = True                            # Daemonize thread
                thread.start()
                print 'processed batch:{0} press enter to start next batch'.format(self.batch_id)
                self.is_processing = False  # we are not taking a photos to set this false
                self.batch_id = None  # remove batch_id
                self.num_of_photos = PHOTO_BATCH_SIZE # set the number of photos back to default
            else:
                # we are still taking photos so just decrement by 1
                self.num_of_photos = self.num_of_photos - 1
                #set start time back to now
                self.start_time = self.now_time

    def on_loop(self):
        """loop, raises the current frame as an event"""
        self.now_time = int(time.time())
        zope.event.notify(self.video_capture.read()[1])  # take photo

    def on_render(self):
        """render?"""
        pass

    def on_cleanup(self):
        """close the program"""
        self._running = False
        cv2.destroyWindow("preview")

    def seconds_until_next_photo(self):
        """seconds left until next photo"""
        time_between_start_of_batch_and_now = (self.now_time - self.start_time)
        return TIME_BETWEEN_PHOTOS - time_between_start_of_batch_and_now

    def get_current_image(self):
        """returns either an overlay with countdown or just the current frame"""
        seconds_until_next_photo = self.seconds_until_next_photo()
        #print 'seconds_until_next_photo = {0}'.format(seconds_until_next_photo)
        if not self.is_processing:
            return self.adele_image
        if str(seconds_until_next_photo) in self.count_down_images:
            return cv2.addWeighted(self.count_down_images[str(seconds_until_next_photo)], 0.5, self.video_capture.read()[1], 0.5, 0.0)
        else:
            return self.video_capture.read()[1]

    def on_execute(self):
        """first thing to be called"""
        if self.on_init() is False:
            self._running = False
        while self.video_capture.isOpened() and self._running:
            cv2.imshow("preview", self.get_current_image()) #1 display the current frame
            key = cv2.waitKey(20) #2 wait for key input after 20 ms
            zope.event.notify(key) #3 notify any subscribers to a key event
            self.on_loop() #4 run the loop (this will trigger images being taken or batching)
            self.on_render() #?

        self.on_cleanup()


if __name__ == "__main__":
    App().on_execute()
