import pygame, sys, os
from pygame.locals import *
from xml.dom import minidom
from animacionFinalMalo import *
from cellarScene import *


class Evento(pygame.sprite.Sprite):
    
    def __init__(self, posicion, nombre, xml = None, activo = 0, pasado = False ):
        pygame.sprite.Sprite.__init__(self);
        #Tratamiento de dialogos XML
        if xml != None:
            self.fullname = os.path.join('', "../res/Dialogos/"+xml)
            xmldoc = minidom.parse(self.fullname)
            self.itemlist = xmldoc.getElementsByTagName('dialog') 
        self.estado = 0
        self.image = pygame.image.load("../res/Sprites/sprite_invisible.png")
        self.mask = pygame.mask.from_surface(pygame.image.load("../res/Sprites/maskEventGen.png"))
        self.mask.fill()
        self.posicion = posicion
        self.rect = self.image.get_rect() 
        self.rect.center = self.posicion
        self.color = (0,0,0)
        self.nombre = nombre
        
    def onEvent(self):
        pass
    
    def cambiarEstado(self, object=None, estado=None):
        if estado != None:
            if estado == -1:
                for item in self.itemlist:
                    if item.attributes['id'].value == "final":
                        self.estado = self.itemlist.index(item)
            else:
                self.estado = estado
        return True
        
    def continuar(self, respuesta, object = None):
        print "respuesta - "
        print respuesta
        print len(self.itemlist)
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
    
class EventoDesaparicion(Evento):
    
    def __init__(self, posicion, nombre, xml, sprite, grupo, mascara):
        Evento.__init__(self, posicion, nombre,xml)
        self.sprite = sprite
        self.grupo = grupo
        self.mascara = mascara

    def onEvent(self):
        self.grupo.remove(self.sprite)
        self.mascara.erase(self.sprite.mask, (self.sprite.rect.center[0]-20, self.sprite.rect.center[1]-30))
        
class EventoAparicion(Evento):
    
    def __init__(self, posicion, nombre, xml, sprite, grupo, mascara , drawMask = True):
        Evento.__init__(self, posicion, nombre, xml)
        self.sprite = sprite
        self.grupo = grupo
        self.mascara = mascara
        self.drawMask = drawMask

    def onEvent(self):
        self.grupo.add(self.sprite)
        if self.drawMask :
            self.mascara.draw(self.sprite.mask, (self.sprite.rect.center[0]-20, self.sprite.rect.center[1]-30))
 
class EventoActivaItems(Evento):
    
    def __init__(self, posicion, nombre, itemsActivados, grupo, sonido = None):
        Evento.__init__(self, posicion, nombre, "evPista.xml")
        self.itemsActivados = itemsActivados
        self.grupo = grupo
        self.sonido = sonido
        
    def onEvent(self):
        if self.sonido != None:
            canal = self.sonido.play()
        for i in self.itemsActivados:
            self.grupo.add(i)
            
class EventoCambioEstado(Evento):
    
    def __init__(self, posicion, nombre, objeto, estadoN, xml, sonido = None):
        Evento.__init__(self, posicion, nombre, xml)
        self.objeto = objeto
        self.estadoN = estadoN
        self.sonido = sonido
        
    def onEvent(self):
        if self.sonido != None:
            canal = self.sonido.play()
        self.objeto.cambiarEstado(None,self.estadoN)          
  
class EventoFinal(Evento):
    
    def __init__(self, posicion, nombre, fase):
        Evento.__init__(self, posicion, nombre, "evVacio.xml")
        self.fase = fase
        
    def onEvent(self):
        if self.nombre == "MuerteCafe":
            self.fase.finFase(EscenaAnimacionFinalMalo(self.fase.director, "../res/Dialogos/animacionFinalMaloCafe.xml"))
        elif self.nombre == "FinalBolio":
            self.fase.finFase(EscenaAnimacionFinalMalo(self.fase.director, "../res/Dialogos/animacionFinalMaloBolio.xml"))
        elif self.nombre == "FinalChema":
            self.fase.finFase(EscenaAnimacionFinalMalo(self.fase.director, "../res/Dialogos/animacionFinalMaloChema.xml"))
        elif self.nombre == "FinalEspeonza":
            self.fase.finFase(EscenaAnimacionFinalMalo(self.fase.director, "../res/Dialogos/animacionFinalMaloEspeonza.xml"))
        elif self.nombre == "FinalCervero":
            self.fase.finFase(EscenaAnimacionFinalMalo(self.fase.director, "../res/Dialogos/animacionFinalMaloCervero.xml"))
        elif self.nombre == "FinalCharles":
            self.fase.finFase(EscenaAnimacionFinalMalo(self.fase.director, "../res/Dialogos/animacionFinalMaloCharles.xml"))
        elif self.nombre == "FinalTodos":
            self.fase.finFase(CellarScene(self.fase.director, self.fase.player))
        
        
class EventoCulpable(Evento):
    
    def __init__(self, posicion, nombre, culpable, culpables, poli, eventosAct, eventoN, sonido, inventario, objeto=None):
        Evento.__init__(self, posicion, nombre, "evCulp.xml")
        self.culpable = culpable
        self.culpables = culpables
        self.poli = poli
        self.eventosAct = eventosAct
        self.eventoN = eventoN
        self.sonido = sonido
        self.objeto = objeto
        self.inventario = inventario
        
    def onEvent(self):
        canal = self.sonido.play()
        if self.culpable == "Bolio":
            if "Chema" in self.culpables:
                self.poli.cambiarEstado(None, 3)
                self.eventosAct.append(self.eventoN)
            else:
                self.poli.cambiarEstado(None, 1)
        elif self.culpable == "Chema":
            if "Bolio" in self.culpables:
                self.poli.cambiarEstado(None, 3)
                self.eventosAct.append(self.eventoN)
            else:
                self.poli.cambiarEstado(None, 2)
        elif self.culpable == "Espeonza":
            self.poli.cambiarEstado(None, 4)
            self.eventosAct.append(self.eventoN)
        elif self.culpable == "Cervero":
            self.poli.cambiarEstado(None, 5)
            self.eventosAct.append(self.eventoN)
        elif self.culpable == "Charles":
            self.poli.cambiarEstado(None, 6)
        self.culpables.append(self.culpable)
        if self.objeto != None:
            if self.objeto in self.inventario:
                self.inventario.remove(self.objeto) 
            
                 