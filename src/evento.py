import pygame, sys, os
from pygame.locals import *
from xml.dom import minidom

class Evento(pygame.sprite.Sprite):
    
    def __init__(self, posicion, nombre, xml = None, activo = 0, pasado = False ):
        pygame.sprite.Sprite.__init__(self);
        #Tratamiento de dialogos XML
        if xml != None:
            self.fullname = os.path.join('', "../res/Dialogos/"+xml)
            xmldoc = minidom.parse(self.fullname)
            self.itemlist = xmldoc.getElementsByTagName('dialog') 
        self.activo = activo
        self.pasado = pasado
        self.image = pygame.image.load("../res/Sprites/ball.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.posicion = posicion
        self.rect = self.image.get_rect() 
        self.rect.center = self.posicion
        self.color = (0,0,0)
        self.nombre = nombre
        
    def onEvent(self):
        pass
    
    def cambiarEstado(self, object=None, estado=None):
        self.pasado = True
        return True
    
class EventoDesaparicion(Evento):
    
    def __init__(self, posicion, nombre, sprite, grupo, mascara):
        Evento.__init__(self, posicion, nombre)
        self.sprite = sprite
        self.grupo = grupo
        self.mascara = mascara

    def onEvent(self):
        self.grupo.remove(self.sprite)
        self.mascara.erase(self.sprite.mask, (self.sprite.rect.center[0]-20, self.sprite.rect.center[1]-30))
        
class EventoAparicion(Evento):
    
    def __init__(self, posicion, nombre, xml, sprite, grupo, mascara):
        Evento.__init__(self, posicion, nombre, xml)
        self.sprite = sprite
        self.grupo = grupo
        self.mascara = mascara

    def onEvent(self):
        self.grupo.add(self.sprite)
        self.mascara.draw(self.sprite.mask, (self.sprite.rect.center[0]-20, self.sprite.rect.center[1]-30))
        
    def continuar(self, respuesta, object = None):
        phrase_list = self.itemlist[0].getElementsByTagName("phrase")
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
    