##import pygame
##
##pygame.init()
##pygame.display.set_mode((800,480))
##screen = pygame.display.get_surface()
##while True:
##    img = pygame.image.load('/media/pi/88DB-D77C/photos/singles/eeb0890f-38ef-433a-a828-d068c41c43f5-photo-1491475916.png')
##    screen.blit(img, (0,0))
##
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import pygame.camera
import cv2
import uuid
import numpy as np
import sys
from PIL import Image
import time as time
import os, sys
import uuid


DEVICE = '/dev/video0'
SIZE =  (640,480)
BATCH_SIZE = 4
TIME_BETWEEN_PHOTOS = -2
photos_dir = '/media/pi/88DB-D77C/photos'
single_photos_dir = '/media/pi/88DB-D77C/photos/singles'
vertical_photos_dir = '/media/pi/88DB-D77C/photos/vertical'
horizontal_photos_dir = '/media/pi/88DB-D77C/photos/horizontal'

class App:
    start_time = 0
    now_time = 0
    batch_id = None
    has_started = False
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
 
    def on_init(self):
        pygame.init()
        pygame.camera.init()
        pygame.display.set_caption('photo booth')
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
    ##        #SET VARIABLES
    ##        self.start_time = int(time.time())
    ##        self.batch_id = uuid.uuid4()
 
    def on_event(self, event):
        properties = event.__dict__
        key = properties.get('key')
        #print properties
        if key == 27:
            self._running = False
        if key == 13:
            self.start_time=int(time.time())
            self.batch_id = uuid.uuid4()
            self.has_started = True
            #pygame.image.save(screen, FILENAME)
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
    def captureimage(self, frame):
        name = '{0}/{1}-photo-{2}.png'.format(single_photos_dir,self.batch_id, self.now_time)
        print 'taking photo {0}'.format(name)
        print frame.get_alpha()
        frame.set_alpha(1)
        pygame.image.save(frame, name)
    def captureimage_string(self, imgstring):
        name = '{0}/{1}-photo-{2}.png'.format(single_photos_dir,self.batch_id, self.now_time)
        print 'taking photo {0}'.format(name)
        imgconverted = np.asarray(imgstring)
        cv2.imwrite(name, imgconverted)
        
    def stichphotos(self):
        photos = os.listdir( single_photos_dir )
        matching = []
        for photo in photos:
            if photo.startswith(str(self.batch_id)):
                matching.append('{0}/{1}'.format(single_photos_dir,photo))
                                
        number = len(matching)
        if (number== 0):
            return
        print 'stiching photos there are: {0}'.format(number)
        print 'photos taken:'
        for image_name in matching:
            print image_name
        
        imgs    = [ Image.open(i) for i in matching ]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

        # save that beautiful picture
        imgs_comb = Image.fromarray( imgs_comb)
        horizontal_image_name =  '{0}/Horizontal-{1}.jpg'.format(horizontal_photos_dir,self.now_time)
        imgs_comb.save(horizontal_image_name)
        print 'saved horiztonal image: {0}'.format(horizontal_image_name)

        # for a vertical stacking it is simple: use vstack
        imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        imgs_comb = Image.fromarray( imgs_comb)
        vertical_image_name = '{0}/Vertical-{1}.jpg'.format(vertical_photos_dir, self.now_time)
        imgs_comb.save(vertical_image_name)
        print 'saved vertical image: {0}'.format(vertical_image_name)
        
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        display = pygame.display.set_mode(SIZE, 0)
        camera = pygame.camera.Camera(DEVICE, SIZE)
        
        camera.start()
        screen = pygame.surface.Surface(SIZE, 0, display)
        num_of_photos = 4
        
        while( self._running ):
            self.now_time= int(time.time())
            screen = camera.get_image(screen)
            display.blit(screen, (0,0))
            pygame.display.flip()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            if ((  (self.start_time - self.now_time) == TIME_BETWEEN_PHOTOS) and (self.has_started) and (num_of_photos > 0)): 
                self.captureimage(screen) #raise event for this
                #self.captureimage_string(camera.get_raw())
                if (num_of_photos == 1): #we have taken the last photo of the batch
                    self.stichphotos() #put the photos together
                    print 'processed batch:{0} press enter to start next batch'.format(self.batch_id)
                    self.has_started = False #we are not taking a photos to set this false
                    self.batch_id = None # remove batch_id
                    num_of_photos = 4 #set the number of photos back to default
                else:
                    num_of_photos=num_of_photos-1 #we are still taking photos so just decrement by 1
                    self.start_time=self.now_time #always override the start time when we are taking photos
           
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
