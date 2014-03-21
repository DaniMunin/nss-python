# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from item import *
from personajes import *
from pygame.locals import *
from cellarScene import *
# from testItem import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

OPT_KEYS = {pygame.K_1 : 1,
               pygame.K_2 : 2,
               pygame.K_3: 3,
               pygame.K_4 : 4}

class FaseInvestigacion(EscenaPygame):
    def __init__(self, director, jugador1):
        # Primero invocamos al constructor de la clase padre
        EscenaPygame.__init__(self, director)

        
        pygame.display.set_caption("Fase")
        pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        """Initialize things; create a Player; create a Level."""
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.player = jugador1
        fondo = pygame.image.load("../res/maps/mapa2.png")
        #cambiar el rect.copy para poner posicion inicial
        posInicialMapa = self.screen_rect.copy()
        posInicialMapa.topleft = (posInicialMapa.topleft[0]-100,posInicialMapa.topleft[1]+100)
        self.level = Level(fondo, posInicialMapa, self.player)
        self.grupoJugadores = pygame.sprite.Group(jugador1)
        self.dialogo = 6
        self.opcion = False
        self.optEl = 0
        self.eventoT = True
        self.activarEv = False
        self.accion = False
        self.inventario = False
        self.mostrar = True
        self.primerDia = True
        self.numRes = 0
        self.accionO = None
        self.accionT = None
        self.accionR = None
        self.accionResult = None
        self.text = Text()
        self.bolio = NoJugador("../res/Sprites/bolio2.png","../res/BolioCoordJugador.txt", (244,1990), 1, "dialogoEspeonza.xml", (184,134,11))
        self.espeonza = NoJugador("../res/Sprites/esperanza2.png","../res/EspeonzaCoordJugador.txt", (223,1748), 1, "dialogoEspeonza.xml", (199,21,133))
        self.charles = NoJugador("../res/Sprites/charles.png","../res/CharlesCoordJugador.txt", (156,1564), 1.5, "dialogoEspeonza.xml", (200,20,20))
        self.cervero = NoJugador("../res/Sprites/scien2.png","../res/ScienceCoordJugador.txt", (993,1984), 1, "dialogoEspeonza.xml", (50,205,50))
        self.rateos = NoJugador("../res/Sprites/rateos2.png","../res/RateosCoordJugador.txt", (831,1504), 1, "dialogoEspeonza.xml", (100,100,100))
        self.poli = NoJugador("../res/Sprites/poli.png","../res/PoliCoordJugador.txt", (586,1400), 1.5, "dialogoEspeonza.xml", (0,0,255))
        self.grupoNPC = pygame.sprite.Group( self.poli, self.rateos, self.cervero, self.charles, self.espeonza, self.bolio )

        self.ball = Item(10, "pokeball.xml")
        self.ball.rect.center = (630,1780)
        self.grupoObj = pygame.sprite.Group(self.ball)
        
        self.level.mask.draw(self.ball.mask, (self.ball.rect.center[0]-5, self.ball.rect.center[1]-5))
        self.level.mask.draw(self.poli.mask, (self.poli.rect.center[0]-16, self.poli.rect.center[1]-30))
        self.level.mask.draw(self.espeonza.mask, (self.espeonza.rect.center[0]-20, self.espeonza.rect.center[1]-30))
        self.level.mask.draw(self.charles.mask, (self.charles.rect.center[0]-20, self.charles.rect.center[1]-30))
        self.level.mask.draw(self.cervero.mask, (self.cervero.rect.center[0]-20, self.cervero.rect.center[1]-30))
        self.level.mask.draw(self.rateos.mask, (self.rateos.rect.center[0]-16, self.rateos.rect.center[1]-30))
        self.level.mask.draw(self.bolio.mask, (self.bolio.rect.center[0]-20, self.bolio.rect.center[1]-30))
        
                
    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se actualizan los jugadores con los movimientos a realizar
    #  Se actualiza la posicion del sol y el color del cielo
    #  Se mueven los enemigos como sea conveniente
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se actualiza el scroll del decorado y los objetos en el
    def update(self, tiempo):
#         self.screen.fill(pygame.Color("black"))
        if (self.accion):
            self.tiempoDial += tiempo
            if ~self.primerDia:
                self.accionT, self.accionR, self.accionResult = self.continuarAccion(self.accionO, self.numRes) 
        elif (self.inventario):
            if self.optEl != 0:
                self.inventario = False
                if not self.mostrar:
                    self.primerDia = True
                    self.numRes = 0
                    self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoObj)
                    self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO, self.player.objetos[self.optEl - 1])
                self.optEl = 0
        else:   
            self.level.update(self.keys)
#         print self.rateos.rect
#         print self.player.rect
#         print self.poli.rect
#         print self.espeonza.rect
#         print self.cervero.rect
        
#         else:
#             self.level.draw(self.screen, texto)
    
    def dibujar(self):        
        s = self.level.draw(self.screen)
        s.blit(self.ball.image, self.ball.rect)
        s.blit(self.poli.image, self.poli.posicion)
        s.blit(self.espeonza.image, self.espeonza.posicion)
        self.player.draw(s)
        s.blit(self.bolio.image, self.bolio.posicion)
        s.blit(self.charles.image, self.charles.posicion)
        s.blit(self.cervero.image, self.cervero.posicion)
        s.blit(self.rateos.image, self.rateos.posicion)
        
        if self.accion:
            self.interact(self.tiempoDial, s)
            
        if self.inventario:
            self.mostrarInv(s)
            
        self.screen.blit(s, (0,0), self.level.viewport)

    def evento(self, event):
        # Indicamos la acciÃ³n a realizar segun la tecla pulsada para cada jugador
        self.keys = pygame.key.get_pressed()
        if self.opcion:
            for key in OPT_KEYS:
                if self.keys[key]:
                    self.optEl = OPT_KEYS[key]
                    self.opcion = False
                    if self.accionR != None and self.accionR != []:
                        self.numRes = self.accionR[self.optEl - 1][1]
                        self.optEl = 0
                        self.tiempoDial = 0
        #Interactuar con npc/objeto sin utilizar nada
        if self.keys[K_SPACE] and (not self.accion) and (not self.inventario):
            if (pygame.sprite.spritecollideany(self.player, self.grupoNPC) != None):
                self.primerDia = True
                self.numRes = 0
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoNPC)
                self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
            if (pygame.sprite.spritecollideany(self.player, self.grupoObj) != None):
                self.primerDia = True
                self.numRes = 0
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoObj)
                self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
        #Abrir el inventario
        if self.keys[K_i] and ~self.accion and ~self.inventario:
            #Interactuar con npc/objeto utilizando un objeto
            if (pygame.sprite.spritecollideany(self.player, self.grupoObj) != None):
                self.mostrar = False
            else: 
                self.mostrar = True
            self.inventario = True
        #Cerrar el inventario en caso de estar solo mostrandolo
        if self.inventario and self.mostrar:
            if self.keys[K_u]:
                self.optEl = 1
        #Esto de aqui no deberÃ­a funcionar asÃ­, si no que deberÃ­a cerrar el programa sin mÃ¡s, no llevarnos a la fase siguiente
        if event.type == pygame.QUIT:
             print "Hola"
             escenaSig = CellarScene(self.director, self.player)
             self.director.cambiarEscena(escenaSig)
            
    def interact(self, tiempo, surface):
        if tiempo < 1000:
            self.text.render(surface,self.accionT, self.accionO.color, (self.accionO.rect.topleft[0], self.accionO.rect.topleft[1]))
        elif len(self.accionR) == 1:
            if tiempo < 2000:
                self.text.render(surface,self.accionR[0][0], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1]))
                self.numRes = self.accionR[0][1] 
        elif len(self.accionR) == 0:
            #Objetos recibidos
            if self.accionResult[0] != "None":
                self.player.objetos.append(self.accionResult[0])
            #Nuevo estado del objeto/npc
            self.accionO.cambiarEstado(None, int(self.accionResult[3]))
            #Eventos generados
            if self.accionResult[2] != "None":
                pass
            #Movimiento de algun personaje
            if self.accionResult[1] != "None":
                pass
            self.accion = False
        elif self.optEl == 0:
            self.tiempoDial = 2000
            self.opcion = True
            j = len(self.accionR)
            for i in range(len(self.accionR)):
                self.text.render(surface,self.accionR[i][0], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - j*30))
                j -= 1
        else:
            self.primerDia = False
    
    #Muestra el inventario hasta pulsar la tecla u o seleccionar un objeto
    def mostrarInv(self, surface):
        if self.optEl == 0:
            self.tiempoDial = 2000
            self.opcion = True
            j = len(self.player.objetos)
            self.text.render(surface,"Inventario:", (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - (j+1)*30))
            for i in range(len(self.player.objetos)):
                self.text.render(surface,self.player.objetos[i], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - j*30))
                j -= 1
            
    def empezarAccion(self, objeto, usar = None):
        #recuperar texto xml
        self.accion = True
        self.tiempoDial = 0
        self.primerDia = True
        texto,respuesta,resultado = objeto.continuar(0,usar)
        return texto,respuesta,resultado
    
    def continuarAccion(self, objeto, respuesta):
        #recuperar texto xml
        texto,respuesta,resultado = objeto.continuar(respuesta)
        return texto,respuesta,resultado
    
    
class Level(object):
    """
A class for our map. Maps in this implementation are one image; not
tile based. This makes collision detection simpler but can have performance
implications.
"""
    def __init__(self, map_image, viewport, player):
        """
Takes an image from which to make a mask, a viewport rect, and a
player instance.
"""
        self.image = map_image
#         self.image =pygame.image.load("../res/maps/primerinteriormask.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA*4, ALTO_PANTALLA*4))
        mascara = pygame.image.load("../res/maps/mascaramapa.png").convert_alpha()        
        mascara = pygame.transform.scale(mascara, (ANCHO_PANTALLA*4, ALTO_PANTALLA*4))
        self.mask = pygame.mask.from_surface(mascara)
        self.rect = self.image.get_rect()
        self.player = player
#         self.player.rect.center = self.rect.center
        #posicion inicial
        self.player.rect.center = (630,1480)
        self.viewport = viewport
        

    def update(self, keys):
        """
Updates the player and then adjust the viewport with respect to the
player's new position.
"""
        self.player.update(self.mask, keys)
        self.update_viewport()
#         print self.player.rect
#         print self.poli.rect
        
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