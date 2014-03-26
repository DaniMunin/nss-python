# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *

class CellarScene(EscenaPygame):
    def __init__(self, director, jugador1):

        EscenaPygame.__init__(self, director)
       
        pygame.display.set_caption("Cellar")
        pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        """Initialize things; create a Player; create a Level."""
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.player = jugador1
        fondo = pygame.image.load("../res/maps/firstWithDoor.png")
        self.level = Level(fondo, self.screen_rect.copy(), self.player)
        self.grupoJugadores = pygame.sprite.Group(jugador1)
                
    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se actualizan los jugadores con los movimientos a realizar
    #  Se actualiza la posicion del sol y el color del cielo
    #  Se mueven los enemigos como sea conveniente
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se actualiza el scroll del decorado y los objetos en el
    def update(self, tiempo):
        
        self.screen.fill(pygame.Color("black"))
        self.level.update(self.keys)
        self.level.draw(self.screen)
        
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
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA, ALTO_PANTALLA))
        mascara = pygame.image.load("../res/maps/FirstCellarRoomMask.png").convert_alpha()        
        mascara = pygame.transform.scale(mascara, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.mask = pygame.mask.from_surface(mascara)
        self.rect = self.image.get_rect()
        self.player = player
#         self.player.rect.center = self.rect.center
        #posicion inicial
        self.player.rect.center = (500,400)
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
        new_image = self.image.copy()
        self.player.draw(new_image)
        surface.fill((50,255,50))
        surface.blit(new_image, (0,0), self.viewport)
    