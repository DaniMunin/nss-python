import pygame, sys, os
from pygame.locals import *
from xml.dom import minidom

class Item(pygame.sprite.Sprite):
    
    def __init__(self, id, xml):
        #Cargamos los dialogos del item
        self.fullname = os.path.join('', "../res/Dialogos/"+xml)
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
        xmldoc = minidom.parse(fullname)
        itemlist = xmldoc.getElementsByTagName('phrase') 
        print len(itemlist)
        print itemlist[0].attributes['content'].value
        child_list = itemlist[0].getElementsByTagName("response")
        print child_list[0].attributes['content'].value
        #for s in itemlist :
        #    print s.attributes['content'].value
        #itemlist = xmldoc.getElementsByTagName('response')
        #for s in itemlist :
        #    print s.attributes['content'].value