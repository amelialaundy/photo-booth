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

DEVICE = '/dev/video0'
SIZE =  (640,480)
class App:
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
 
    def on_event(self, event):
        properties = event.__dict__
        key = properties.get('key')
        #rint properties
        if key == 27:
            self._running = False
        #if key == 13:
            #img = pygame.image.load('/media/pi/88DB-D77C/photos/singles/eeb0890f-38ef-433a-a828-d068c41c43f5-photo-1491475916.png')
            #print img
            #self._display_surf.blit(img,(0,0))
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        display = pygame.display.set_mode(SIZE, 0)
        camera = pygame.camera.Camera(DEVICE, SIZE)
        camera.start()
        screen = pygame.surface.Surface(SIZE, 0, display)
        while( self._running ):
            print 'while'
            screen = camera.get_image(screen)
            display.blit(screen, (0,0))
            pygame.display.flip()
            #img = pygame.image.load(frame)
            #print img
            #self._display_surf.blit(img,(0,0))
            for event in pygame.event.get():
                print 'forloop'
                self.on_event(event)
            self.on_loop()
            print 'on loop'
            self.on_render()
            print 'on render'
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
