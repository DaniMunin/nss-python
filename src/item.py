import pygame, sys, os
from pygame.locals import *

class Item(pygame.sprite.Sprite):
    
    def __init__(self, id):
        self.itemId = id
        pygame.sprite.Sprite.__init__(self)
        fullname = os.path.join('', "../res/Sprites/ball.png")
        self.image =pygame.image.load(fullname)
        self.rect = self.image.get_rect() 
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        fullname = os.path.join('', "../res/Sprites/ballmask.png")
        self.mask = pygame.mask.from_surface(pygame.image.load(fullname))

    def onUse(self):
        return self.itemId