import pygame, sys, os
from pygame.locals import *

class Item(pygame.sprite.Sprite):
    
    def __init__(self, id):
        self.itemId = id
        pygame.sprite.Sprite.__init__(self)
        fullname = os.path.join('', "../res/Sprites/ball.png")
        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect() 
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.mask = pygame.mask.from_surface(pygame.image.load(fullname))
        self.color = (0,0,0)

    def onUse(self):
        return self.itemId
    
    def onUse(self, object):
        phrase_list = itemlist[self.estado].getElementsByTagName("phrase")
        phrase = phrase_list[0].attributes['content'].value
        response_list=[];
        for response in phrase_list[0].getElementsByTagName("response"):
            response_list.append(response.attributes["content"].value, int(response.attributes["next"].value))
        result_list=[]
        if(len(response_list)==0):
            results=phrase_list[respuesta].getElementsByTagName("result")
            result_list.append(results[0].attributes["obj"].value)
            result_list.append(results[0].attributes["move"].value)
            result_list.append(results[0].attributes["event"].value)
        return phrase, response_list, result_list
    
    def continuar(self, respuesta):
        phrase_list = itemlist[self.estado].getElementsByTagName("phrase")
        phrase = phrase_list[respuesta].attributes['content'].value
        response_list=[];
        for response in phrase_list[respuesta].getElementsByTagName("response"):
            response_list.append(response.attributes["content"].value, int(response.attributes["next"].value))
        result_list=[]
        if(len(response_list)==0):
            results=phrase_list[respuesta].getElementsByTagName("result")
            result_list.append(results[0].attributes["obj"].value)
            result_list.append(results[0].attributes["move"].value)
            result_list.append(results[0].attributes["event"].value)
        return phrase, response_list, result_list