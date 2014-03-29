import pygame, sys, os
from pygame.locals import *
from xml.dom import minidom

class Item(pygame.sprite.Sprite):
    
    def __init__(self, id, xml,imagen, pos):
        self.itemId = id
        pygame.sprite.Sprite.__init__(self)
        fullname = os.path.join('', imagen)
        self.image = pygame.image.load(fullname)
        if id == 11:
            self.image = pygame.transform.scale(self.image, (int(80), int(80)))
        self.rect = self.image.get_rect() 
        self.rect.center = pos
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        #Tratamiento de dialogos XML
        self.fullname = os.path.join('', "../res/Dialogos/"+xml)
        xmldoc = minidom.parse(self.fullname)
        self.itemlist = xmldoc.getElementsByTagName('dialog') 
#         phrase_list = itemlist[0].getElementsByTagName("phrase")
        self.obj=[]
        for item in self.itemlist:
            self.obj.append(item.attributes['obj'].value)
        self.color = (0,0,0)
        self.estado = 0

    def onUse(self):
        return self.itemId
    
#     def onUse(self, object):
#         if object != None:
#             print object
#         phrase_list = self.itemlist[self.estado].getElementsByTagName("phrase")
#         phrase = phrase_list[0].attributes['content'].value
#         response_list=[];
#         for response in phrase_list[0].getElementsByTagName("response"):
#             response_list.append((response.attributes["content"].value, int(response.attributes["next"].value)))
#         result_list=[]
#         if(len(response_list)==0):
#             results=phrase_list[respuesta].getElementsByTagName("result")
#             result_list.append(results[0].attributes["obj"].value)
#             result_list.append(results[0].attributes["move"].value)
#             result_list.append(results[0].attributes["event"].value)
#         return phrase, response_list, result_list
    
    def continuar(self, respuesta, object = None):
        if object != None and self.itemlist[self.estado].attributes['id'].value != "final":
            self.cambiarEstado(object)
        phrase_list = self.itemlist[self.estado].getElementsByTagName("phrase")
        phrase = phrase_list[respuesta].attributes['content'].value
        response_list=[];
        for response in phrase_list[respuesta].getElementsByTagName("response"):
            response_list.append((response.attributes["content"].value, int(response.attributes["next"].value)))
        result_list=[]
        if(len(response_list)==0):
            results=phrase_list[respuesta].getElementsByTagName("result")
            result_list.append(results[0].attributes["obj"].value)
            result_list.append(results[0].attributes["move"].value)
            result_list.append(results[0].attributes["event"].value)
            result_list.append(results[0].attributes["state"].value)
        return phrase, response_list, result_list
    
    def cambiarEstado(self, object=None, estado=None):
        if object != None:
            if object in self.obj:
                self.estado = self.obj.index(object)
            else:
                self.estado = len(self.obj)-1-self.estado
        if estado != None:
            if estado == -1:
                for item in self.itemlist:
                    if item.attributes['id'].value == "final":
                        self.estado = self.itemlist.index(item)
            else:
                self.estado = estado
        return False
    
class ItemVisible(Item):   
    def __init__(self, id, xml, imagen, pos): 
        Item.__init__(self, id, xml,imagen, pos);
        self.mask = pygame.mask.from_surface(self.image)
        if id == 11:
            self.mask.fill()

class ItemInvisible(Item): 
    def __init__(self, id, xml, pos):
        Item.__init__(self,id,xml, "../res/Sprites/sprite_invisible.png", pos);
        self.mask = pygame.mask.from_surface(pygame.image.load(os.path.join('', "../res/Sprites/sprite_invisible.png")))
        self.mask.fill()
        