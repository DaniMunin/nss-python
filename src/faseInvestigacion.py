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
        self.text = Text()
        self.bolio = NoJugador("../res/Sprites/bolio2.png","../res/BolioCoordJugador.txt", (244,1990))
        self.espeonza = NoJugador("../res/Sprites/esperanza2.png","../res/EspeonzaCoordJugador.txt", (223,1748))
        self.charles = NoJugador("../res/Sprites/charles.png","../res/CharlesCoordJugador.txt", (156,1564))
        self.cervero = NoJugador("../res/Sprites/scien2.png","../res/ScienceCoordJugador.txt", (993,1984))
        self.rateos = NoJugador("../res/Sprites/rateos2.png","../res/RateosCoordJugador.txt", (831,1504))
        self.poli = NoJugador("../res/Sprites/poli.png","../res/PoliCoordJugador.txt", (586,1400))
#         self.bolio.posicion = (244,1990)
#         self.espeonza.posicion = (223,1748)
#         self.charles.posicion = (156,1564)
#         self.cervero.posicion = (993,1984)
#         self.rateos.posicion = (831,1504)
#         self.poli.posicion = (586,1387)

        self.ball = Item(10)
        self.ball.rect.center = (630,1480)
        
                
    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se actualizan los jugadores con los movimientos a realizar
    #  Se actualiza la posicion del sol y el color del cielo
    #  Se mueven los enemigos como sea conveniente
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se actualiza el scroll del decorado y los objetos en el
    def update(self, tiempo):
#         self.screen.fill(pygame.Color("black"))
        if (self.dialogo == 6):
            #Evento activado
            if self.activarEv:
                self.tiempoEv += tiempo
            #Juego normal
            else:
                self.level.update(self.keys)
                #Detecto dialogo (colision con personaje y pulsar espacio)
                if (pygame.sprite.collide_mask(self.player, self.poli) != None) and (self.keys[pygame.K_SPACE]):
                    self.dialogo = 0
                    self.tiempoDial = 0
                #Detecto evento ( posicion determinada y el trigger de eventos activado)
                if (pygame.sprite.collide_mask(self.player, self.rateos) != None) and (self.eventoT):
                    self.activarEv = True
                    self.tiempoEv = 0
        #             sonido = pygame.mixer.Sound("../res/Sounds/foco.wav")
        #             canal = sonido.play()
        # Dialogo activado
        else:
            self.tiempoDial += tiempo    
#         print self.rateos.rect
        print self.player.rect
        print self.poli.rect
#         print self.espeonza.rect
#         print self.cervero.rect
        
#         else:
#             self.level.draw(self.screen, texto)
    
    def dibujar(self):        
#         self.text.render(self.screen, "Se acabs el tiempo!", (0,0,255), (self.player.rect.topleft[0], self.player.rect.topleft[1] -30))
        s = self.level.draw(self.screen)
        s.blit(self.poli.image, self.poli.posicion)
        self.player.draw(s)
        s.blit(self.bolio.image, self.bolio.posicion)
        s.blit(self.espeonza.image, self.espeonza.posicion)
        s.blit(self.charles.image, self.charles.posicion)
        s.blit(self.cervero.image, self.cervero.posicion)
        s.blit(self.rateos.image, self.rateos.posicion)
#         self.text.render(s, "Se acabs el tiempo!", (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] -30))
        if self.activarEv:
            self.eventDraw(0,self.tiempoEv, s)
        if (self.dialogo != 6):
            self.interact(self.dialogo, self.tiempoDial, s)
        
        
        s.blit(self.ball.image, self.ball.rect)
        
        
#         self.text.render(s, "Se acabff el tiempo!", (0,255,255), (self.level.poli.rect.topleft[0], self.level.poli.rect.topleft[1] -30))
        self.screen.blit(s, (0,0), self.level.viewport)
#         self.grupoJugadores.draw(self.screen)
        
#         self.screen.blit(self.image, self.rect, self.rectSubimagen)
        
#         self.grupoJugadores.draw(self.screen)

    def evento(self, event):
        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        self.keys = pygame.key.get_pressed()
        if self.opcion:
            for key in OPT_KEYS:
                if self.keys[key]:
                    self.optEl = OPT_KEYS[key]
                    self.opcion = False
        #Esto de aqui no debería funcionar así, si no que debería cerrar el programa sin más, no llevarnos a la fase siguiente
        if event.type == pygame.QUIT:
             print "Hola"
             escenaSig = CellarScene(self.director, self.player)
             self.director.cambiarEscena(escenaSig)
            
    def interact(self, npc, tiempo, surface):
        # 0 = poli, 1= bolio, 2=rateos, 3 = espeonza, 4 = charles, 5 = cervero
        if npc == 0:
            if tiempo < 1000:
                self.text.render(surface,"Hola", (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] -30))
            elif tiempo < 2000:
                self.text.render(surface,"Hola", (0,255,255), (self.poli.rect.topleft[0], self.poli.rect.topleft[1] -30))
            elif self.optEl == 0:
                self.tiempoDial = 2000
                self.opcion = True
                print tiempo, self.opcion
                self.text.render(surface,"Elige una opcion: \n 1) Opción 1 \n 2) Opción 2 \n 3) Opción 3 \n 3) Opción 3 \n", (0,255,255), (self.poli.rect.topleft[0], self.poli.rect.topleft[1] -30))
            elif tiempo < 4000:
                if self.optEl == 1:
                    self.text.render(surface,"Elegida opcion 1", (0,255,255), (self.poli.rect.topleft[0], self.poli.rect.topleft[1] -30))
                elif self.optEl == 2:
                    self.text.render(surface,"Elegida opcion 2", (0,255,255), (self.poli.rect.topleft[0], self.poli.rect.topleft[1] -30))
                    self.eventoT = True
                elif self.optEl == 3:
                    self.text.render(surface,"Elegida opcion 3", (0,255,255), (self.poli.rect.topleft[0], self.poli.rect.topleft[1] -30))
                elif self.optEl == 4:
                    self.text.render(surface,"Elegida opcion 4", (0,255,255), (self.poli.rect.topleft[0], self.poli.rect.topleft[1] -30))
                else:
                    self.text.render(surface,"Se acabó el tiempo!", (0,255,255), (self.poli.rect.topleft[0], self.poli.rect.topleft[1] -30))
            else:
                self.optEl = 0
                self.dialogo = 6
                return None
        elif npc == 1:
            pass
        elif npc == 2:
            pass
        elif npc == 3:
            pass
        elif npc == 4:
            pass
        elif npc == 5:
            pass
        return 1
        
    def eventDraw(self, num, tiempo, surface):
        if num == 0:
            if tiempo < 1000:
                self.text.render(surface,"Hola", (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] -30))
            elif tiempo < 2000:
                self.text.render(surface,"Hola", (0,255,255), (self.rateos.rect.topleft[0], self.rateos.rect.topleft[1] -30))
#             elif self.optEl == 0:
#                 self.tiempoDial = 2000
#                 print tiempo, self.opcion
#                 self.text.render(surface,"Elige una opcion: \n 1) Opción 1 \n 2) Opción 2 \n 3) Opción 3 \n 3) Opción 3 \n", (0,255,255), (self.rateos.rect.topleft[0], self.rateos.rect.topleft[1] -30))
            elif tiempo < 4000:
                if self.optEl == 1:
                    self.text.render(surface,"Elegida opcion 1", (0,255,255), (self.rateos.rect.topleft[0], self.rateos.rect.topleft[1] -30))
                elif self.optEl == 2:
                    self.text.render(surface,"Elegida opcion 2", (0,255,255), (self.rateos.rect.topleft[0], self.rateos.rect.topleft[1] -30))
                elif self.optEl == 3:
                    self.text.render(surface,"Elegida opcion 3", (0,255,255), (self.rateos.rect.topleft[0], self.rateos.rect.topleft[1] -30))
                elif self.optEl == 4:
                    self.text.render(surface,"Elegida opcion 4", (0,255,255), (self.rateos.rect.topleft[0], self.rateos.rect.topleft[1] -30))
                else:
                    self.text.render(surface,"Se acabó el tiempo!", (0,255,255), (self.rateos.rect.topleft[0], self.rateos.rect.topleft[1] -30))
            else:
                self.eventoT = False
                self.activarEv = False
                return None
        elif num == 1:
            pass
        elif num == 2:
            pass
        elif num == 3:
            pass
        elif num == 4:
            pass
        elif num == 5:
            pass
        return 1
    
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
        
        
#         self.ball = testItem()
#         self.ball.rect.center = (630,1480)
#         self.image.blit(self.ball.image, self.ball.rect)

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
#         self.new_image.blit(self.poli.image, self.poli.posicion)
#         self.player.draw(self.new_image)
# #         self.poli.update(self.mask,2, 10)
#         self.new_image.blit(self.bolio.image, self.bolio.posicion)
#         self.new_image.blit(self.espeonza.image, self.espeonza.posicion)
#         self.new_image.blit(self.charles.image, self.charles.posicion)
#         self.new_image.blit(self.cervero.image, self.cervero.posicion)
#         self.new_image.blit(self.rateos.image, self.rateos.posicion)
#         if texto != None:
#             self.text.render(self.new_image, texto[0], texto[1], texto[2])
#         surface.fill((50,255,50))
#         surface.blit(self.new_image, (0,0), self.viewport)
#         self.text.render(surface, texto[0], texto[1], texto[2])
        return self.new_image
    
    
class Text:
    def __init__(self, FontName = '../res/XFILES.ttf', FontSize = 30):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize
 
    def render(self, surface, text, color, pos):
        text = unicode(text, "UTF-8")
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color, (255,255,255)), (x, y))
            y += self.size 