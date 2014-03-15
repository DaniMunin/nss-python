# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
# from testItem import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------


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
                
    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se actualizan los jugadores con los movimientos a realizar
    #  Se actualiza la posicion del sol y el color del cielo
    #  Se mueven los enemigos como sea conveniente
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se actualiza el scroll del decorado y los objetos en el
    def update(self, tiempo):
        self.screen.fill(pygame.Color("black"))
        texto = None
        if (pygame.sprite.collide_mask(self.player, self.level.poli) != None) and (self.keys[pygame.K_SPACE]):
            self.dialogo = 0
            self.tiempoDial = 0
        if (self.dialogo != 6):
            texto = self.interact(self.dialogo, self.tiempoDial)
            self.tiempoDial += tiempo
        else:
            self.level.update(self.keys)
        self.level.draw(self.screen, texto)
        
    
    def interact(self, npc, tiempo):
        # 0 = poli, 1= bolio, 2=rateos, 3 = espeonza, 4 = charles, 5 = cervero
        if npc == 0:
            if tiempo < 1000:
                return 1
            else:
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
        
    def dibujar(self):
        pass
#         self.grupoJugadores.draw(self.screen)
        
#         self.screen.blit(self.image, self.rect, self.rectSubimagen)
        
#         self.grupoJugadores.draw(self.screen)

    def evento(self, event):
        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        
        self.keys = pygame.key.get_pressed()
            
    
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
        self.bolio = NoJugador("../res/Sprites/badassSprites.png","../res/BadassCoordJugador.txt")
        self.espeonza = NoJugador("../res/Sprites/badassSprites.png","../res/BadassCoordJugador.txt")
        self.charles = NoJugador("../res/Sprites/badassSprites.png","../res/BadassCoordJugador.txt")
        self.cervero = NoJugador("../res/Sprites/badassSprites.png","../res/BadassCoordJugador.txt")
        self.rateos = NoJugador("../res/Sprites/badassSprites.png","../res/BadassCoordJugador.txt")
        self.poli = NoJugador("../res/Sprites/badassSprites.png","../res/BadassCoordJugador.txt")
        self.bolio.posicion = (244,1990)
        self.espeonza.posicion = (223,1748)
        self.charles.posicion = (156,1564)
        self.cervero.posicion = (993,1984)
        self.rateos.posicion = (831,1504)
        self.poli.posicion = (586,1387)
        self.rect = self.image.get_rect()
        self.player = player
#         self.player.rect.center = self.rect.center
        #posicion inicial
        self.player.rect.center = (630,1480)
        self.viewport = viewport
        self.text = Text()
        
        
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
        print self.player.rect
        print self.poli.rect
        
    def update_viewport(self):
        """
The viewport will stay centered on the player unless the player
approaches the edge of the map.
"""
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rect)

    def draw(self, surface, text):
        """
Blit actors onto a copy of the map image; then blit the viewport
portion of that map onto the display surface.
"""
        new_image = self.image.copy()
        new_image.blit(self.poli.image, self.poli.posicion)
        self.player.draw(new_image)
#         self.poli.update(self.mask,2, 10)
        new_image.blit(self.bolio.image, self.bolio.posicion)
        new_image.blit(self.espeonza.image, self.espeonza.posicion)
        new_image.blit(self.charles.image, self.charles.posicion)
        new_image.blit(self.cervero.image, self.cervero.posicion)
        new_image.blit(self.rateos.image, self.rateos.posicion)
        if text != None:
            self.text.render(new_image, "Hello!", (255,255,255), (self.player.rect.topleft[0], self.player.rect.topleft[1] -30))
        surface.fill((50,255,50))
        surface.blit(new_image, (0,0), self.viewport)
    
    
class Text:
    def __init__(self, FontName = None, FontSize = 30):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize
 
    def render(self, surface, text, color, pos):
        text = unicode(text, "UTF-8")
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color, (0,0,255)), (x, y))
            y += self.size 