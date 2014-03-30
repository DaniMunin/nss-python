# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
from item import *
from evento import *

OPT_KEYS = {pygame.K_1 : 1,
               pygame.K_2 : 2,
               pygame.K_3 : 3,
               pygame.K_4 : 4,
               pygame.K_5 : 5,
               pygame.K_6 : 6,
               pygame.K_7 : 7,
               pygame.K_8 : 8,
               pygame.K_9 : 9,
               pygame.K_0 : 10}
TIEMPODIALOGO = 10000

class FinalScene(EscenaPygame):
    def __init__(self, director, jugador1):

        EscenaPygame.__init__(self, director)
       
        pygame.display.set_caption("FinalScene")
        pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        """Initialize things; create a Player; create a Level."""
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.player = jugador1
        fondo = pygame.image.load("../res/maps/finalMap.png")
        self.level = Level(fondo, self.screen_rect.copy(), self.player, "../res/maps/FinalMapMask.png", (416,986))
        self.grupoJugadores = pygame.sprite.Group(jugador1)
        
        self.charlesD = NoJugador("../res/Sprites/ryuk.png","../res/RyukCoordJugador.txt", (410,614), 1, "dialogoCharlesD.xml", (200,20,20))
        self.grupoEnemigos = pygame.sprite.Group(self.charlesD)
        
        self.charles = ItemVisible(10, "altar1.xml", "../res/Sprites/CharlesT.png", (410, 614))
        self.altar1 = ItemVisible(10, "altar1.xml", "../res/Sprites/altar.png", (412, 283))
        self.altar2 = ItemVisible(10, "altar2.xml", "../res/Sprites/altar.png", (294, 739))
        self.altar3 = ItemVisible(10, "altar3.xml", "../res/Sprites/altar.png", (532, 739))
        self.altar4 = ItemVisible(10, "altar4.xml", "../res/Sprites/altar.png", (203, 459))
        self.altar5 = ItemVisible(10, "altar5.xml", "../res/Sprites/altar.png", (623, 459))
        self.grupoObj = pygame.sprite.Group(self.altar1, self.altar2, self.altar3, self.altar4, self.altar5)
        
        self.accion= False
        self.optEl = 0
        self.cambiarDia = False
        self.numRes = 0
        self.opcion = False
        self.eventoAct = False
        self.muerto=False
        
        self.accionO = None
        self.accionT = None
        self.accionR = []
        self.accionResult = None
        
        self.text = Text()
        self.eventos = []
        self.eventosActivos = []
        self.tiempoDial = 0
        
        self.eventoInicial = EventoCambioEstado((400, 939),"evInicial", self.altar1, 0, "evFinalScene.xml", None)
        self.eventosActivos.append(self.eventoInicial)
        
        self.eventoAltar1 = EventoCambioEstado((412, 283),"eventoAltar1", self.altar2, 1, "eventoAltar1.xml", None)
        self.eventoAltar2 = EventoCambioEstado((294, 739),"eventoAltar2", self.altar3, 1, "eventoAltar2.xml", None)
        self.eventoAltar3 = EventoCambioEstado((532, 739),"eventoAltar3", self.altar4, 1, "eventoAltar3.xml", None)
        self.eventoAltar4 = EventoCambioEstado((203, 459),"eventoAltar4", self.altar5, 1, "eventoAltar4.xml", None)
        self.eventoAltar5 = EventoDesaparicion((623, 459),"eventoAltar5", "eventoAltar5.xml", self.charlesD, self.grupoEnemigos, self.level.mask)
        self.eventoCharlesAp = EventoAparicion((623, 459),"CharlesAp", "CharlesAp.xml", self.charles, self.grupoObj,self.level.mask, False)
        self.finBueno = EventoFinal((623, 459), "FinalJuego", self)
        
        self.eventos.append(self.eventoAltar1)
        self.eventos.append(self.eventoAltar2)
        self.eventos.append(self.eventoAltar3)
        self.eventos.append(self.eventoAltar4)
        self.eventos.append(self.eventoAltar5)
        self.eventos.append(self.eventoCharlesAp)
        self.eventos.append(self.finBueno)
        
        
                
    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se actualizan los jugadores con los movimientos a realizar
    #  Se actualiza la posicion del sol y el color del cielo
    #  Se mueven los enemigos como sea conveniente
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se actualiza el scroll del decorado y los objetos en el
    def update(self, tiempo):
        if (self.accion):
            self.tiempoDial += tiempo
#             print self.tiempoDial
#             print self.cambiarDia
            if self.cambiarDia:
#                 print self.numRes
                self.accionT, self.accionR, self.accionResult = self.continuarAccion(self.accionO, self.numRes) 
                self.cambiarDia = False
                self.tiempoDial = 0
        else:   
            self.level.update(self.keys)
            dir, cant = self.charlesD.mover_malox(self.player)
            if cant != 0:
                self.charlesD.update(self.level.mask, dir,cant)
            dir, cant = self.charlesD.mover_maloy(self.player)
            if cant != 0:
                self.charlesD.update(self.level.mask, dir,cant)
#             print self.player.rect
#             print "npc"
#             print self.charlesD.rect
            if pygame.sprite.spritecollideany(self.player, self.grupoEnemigos) != None and not self.muerto:
#                 self.director.salirEscena()
#                 print "muerto"
                self.muerto=True
                self.accion = True
                self.cambiarDia = False
                self.numRes = 0
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoEnemigos)
                self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
        
    def dibujar(self):
        s = self.level.draw(self.screen)
        self.grupoObj.draw(s)
        if self.charlesD in self.grupoEnemigos:
            s.blit(self.charlesD.image, self.charlesD.posicion)
        self.grupoJugadores.draw(s)
        if self.accion:
           self.interact(self.tiempoDial, s)
        
        self.screen.blit(s, (0,0), self.level.viewport)

    def evento(self, event):
        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        
        self.keys = pygame.key.get_pressed()
        # Indicamos la acciÃ³n a realizar segun la tecla pulsada para cada jugador
        self.keys = pygame.key.get_pressed()
        if self.opcion:
            for key in OPT_KEYS:
                if self.keys[key]:
                    if (self.accionR == [] and len(self.player.objetos) >= OPT_KEYS[key]):
                        self.optEl = OPT_KEYS[key]
                        self.opcion = False
                    elif OPT_KEYS[key] <= len(self.accionR):
                        self.optEl = OPT_KEYS[key]
                        self.opcion = False
                        if self.accionR != None and self.accionR != []:
                            self.numRes = self.accionR[self.optEl - 1][1]
                            self.optEl = 0
                            self.cambiarDia = True
        #Interactuar con npc/objeto sin utilizar nada
        if self.keys[K_SPACE] and (not self.accion):
            if (pygame.sprite.spritecollideany(self.player, self.grupoObj) != None):
                self.cambiarDia = False
                self.numRes = 0
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoObj)
                self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
        if (len(self.eventosActivos) != 0) and (not self.accion):
            for ev in self.eventosActivos:
#                 print self.player.rect.topleft
#                 print ev.posicion
                if pygame.sprite.collide_mask(self.player, ev):
                    ev.onEvent()
                    self.cambiarDia = False
                    self.numRes = 0
                    self.tiempoDial = 0
                    self.accionO = ev
                    self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
        if self.keys[K_q] and self.accion:
            if self.tiempoDial > TIEMPODIALOGO:
                self.tiempoDial = TIEMPODIALOGO*2
            else:
                self.tiempoDial = TIEMPODIALOGO
        #Esto de aqui no deberÃ­a funcionar asÃ­, si no que deberÃ­a cerrar el programa sin mÃ¡s, no llevarnos a la fase siguiente
        if event.type == pygame.QUIT or (self.keys[K_t] and self.keys[K_r]):
             escenaSig = CellarScene(self.director, self.player)
             self.director.cambiarEscena(escenaSig)   
              
    def interact(self, tiempo, surface):
        if tiempo < TIEMPODIALOGO:
            self.text.render(surface,self.accionT, self.accionO.color, (self.accionO.rect.topleft[0], self.accionO.rect.topleft[1]))
        elif len(self.accionR) == 1 and tiempo < TIEMPODIALOGO*2:
            self.text.render(surface,self.accionR[0][0], (0,0,0), (self.accionO.rect.topleft[0], self.accionO.rect.topleft[1]))
            self.numRes = self.accionR[0][1] 
        elif len(self.accionR) == 0:
            #Objetos recibidos
            if self.accionResult[0] != "None":
                self.player.cogerObjeto(self.accionResult[0])
            #Nuevo estado del objeto/npc
            elimEvento = self.accionO.cambiarEstado(None, int(self.accionResult[3]))
            if elimEvento:
                self.eventosActivos.remove(self.accionO)
            #Eventos generados
            if self.accionResult[2] != "None":
                if self.accionResult[2] == "eventoRein":
                    self.reiniciarAltares()
                if self.accionResult[2] == "faseRein":
                    self.reiniciarFase()
                if self.accionResult[2] == "GameOver":
                    self.director.salirEscena()
                for e in self.eventos:
                    if e.nombre==self.accionResult[2]:
                        self.eventosActivos.append(e)
                        self.eventos.remove(e)
            #Movimiento de algun personaje
            if self.accionResult[1] != "None":
                pass
            self.accion = False
        elif len(self.accionR) > 1 and self.optEl == 0:
            self.tiempoDial = TIEMPODIALOGO*2
            self.opcion = True
            j = len(self.accionR)
            for i in range(len(self.accionR)):
                self.text.render(surface,self.accionR[i][0], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - j*30))
                j -= 1
        else:
            self.cambiarDia = True 
            
    def empezarAccion(self, objeto, usar = None):
        #recuperar texto xml
        self.accion = True
        self.tiempoDial = 0
        self.primerDia = True
        texto,respuesta,resultado = objeto.continuar(0,None)
        return texto,respuesta,resultado
    
    def continuarAccion(self, objeto, respuesta):
        #recuperar texto xml
        texto,respuesta,resultado = objeto.continuar(respuesta)
        return texto,respuesta,resultado
    
    def reiniciarAltares(self):
        self.charlesD.speed += 1
        self.altar1.estado = 0
        self.altar2.estado = 0
        self.altar3.estado = 0
        self.altar4.estado = 0
        self.altar5.estado = 0
        if not self.eventoAltar1 in self.eventos:
            self.eventos.append(self.eventoAltar1)
        if not self.eventoAltar2 in self.eventos:
            self.eventos.append(self.eventoAltar2)
        if not self.eventoAltar3 in self.eventos:
            self.eventos.append(self.eventoAltar3)
        if not self.eventoAltar4 in self.eventos:
            self.eventos.append(self.eventoAltar4)
        if not self.eventoAltar5 in self.eventos:
            self.eventos.append(self.eventoAltar5)
        
    def reiniciarFase(self):
        self.reiniciarAltares()
        self.charlesD.speed = 1
        self.muerto=False
        self.player.rect.center = (416,986)
        self.charlesD.posicion = (410,614)
        self.charlesD.rect = Rect(410,614,35,75)
        
    def finFase(self, final):
        print"fin"
        escenaSig = FinalScene(self.director, self.player)
        self.director.cambiarEscena(escenaSig)
    
class Level(object):
    """
A class for our map. Maps in this implementation are one image; not
tile based. This makes collision detection simpler but can have performance
implications.
"""
    def __init__(self, map_image, viewport, player, mascara, playerCenter):
        """
Takes an image from which to make a mask, a viewport rect, and a
player instance.
"""
        self.image = map_image
#         self.image =pygame.image.load("../res/maps/primerinteriormask.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA, ALTO_PANTALLA*2))
        mascara = pygame.image.load(mascara).convert_alpha()        
        mascara = pygame.transform.scale(mascara, (ANCHO_PANTALLA, ALTO_PANTALLA*2))
        self.mask = pygame.mask.from_surface(mascara)
        self.rect = self.image.get_rect()
        self.player = player
#         self.player.rect.center = self.rect.center
        #posicion inicial
        self.player.rect.center = playerCenter
        self.viewport = viewport

    def update(self, keys):
        """
Updates the player and then adjust the viewport with respect to the
player's new position.
"""
        self.player.update(self.mask, keys)
        self.update_viewport()

    def update_viewport(self):
        """
The viewport will stay centered on the player unless the player
approaches the edge of the map.
"""
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rect)

    def draw(self, surface):
        """
Blit actors onto a copy of the map image; then blit the viewport
portion of that map onto the display surface.
"""
        #new_image = self.image.copy()
        #self.player.draw(new_image)
        #surface.fill((50,255,50))
        #surface.blit(new_image, (0,0), self.viewport)
        self.new_image = self.image.copy()
        return self.new_image
    
class Text:
    def __init__(self, FontName = '../res/XFILES.ttf', FontSize = 20):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize
 
    def render(self, surface, text, color, pos):
#         text = unicode(text, "UTF-8")
        x, y = pos
        numLin = len(text.split("%"))
        for i in text.split("%"):
            surface.blit(self.font.render(i, 1, color, (255,255,255)), (x - self.font.size(i)[0]/2, y - numLin*self.font.size(i)[1]))
            y += self.size 
    