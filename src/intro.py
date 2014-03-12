# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - 50

MINIMO_Y_JUGADOR = 50
MAXIMO_Y_JUGADOR = ALTO_PANTALLA - 50

class Intro(EscenaPygame):
    def __init__(self, director, jugador1):

        # Primero invocamos al constructor de la clase padre
        EscenaPygame.__init__(self, director)

        # Inicializamos la pantalla y el modo grafico
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Al diablo el cafe")


        self.jugador1 = jugador1
        self.grupoJugadores = pygame.sprite.Group(jugador1)
        
#         jugador1.establecerPosicion(ANCHO_PANTALLA/2, ALTO_PANTALLA*6/7)
#         self.jugador1.establecerPosicion(ANCHO_PANTALLA*5/7, ALTO_PANTALLA*6)
#         self.jugador1.establecerPosicion(ANCHO_PANTALLA*5/7, ALTO_PANTALLA*13/2)
        self.jugador1.establecerPosicion(ANCHO_PANTALLA*0.8, ALTO_PANTALLA*7/3)
        self.jugador1.numPostura = QUIETO
        
        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Cargamos el decorado
        self.image = load_image('../res/maps/mapa2.png', -1)
#         self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA, ALTO_PANTALLA))
#         self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA*2, ALTO_PANTALLA))
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA*4, ALTO_PANTALLA*4))
        self.rect = self.image.get_rect()
        self.rect.bottom = ALTO_PANTALLA*4
        # Que parte del decorado estamos visualizando
        self.posicionx = 0
        self.posiciony = 0
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.topleft = (self.posicionx, self.posiciony)
        
        
        self.imagemask = Colisiones("../res/maps/maskmap.png")
        
        print self.image.get_size()
        print self.imagemask.mask.get_size()
        print self.jugador1.posicionx
        print self.jugador1.posiciony
        
#         self.mask = pygame.mask.from_surface(self.imagemask)
#         self.mask.rect = self.imagemask.get_rect()
        
#         self.mask = Colisiones("../res/maps/maskmap.png")
#         self.grupoMascaras = pygame.sprite.Group(self.mask)
        
#         mask = load_image('../res/maps/maskmap.png', -1)
#         self.mascaraPrueba = pygame.mask.from_surface(mask)
#         self.image

    def posicionesInicioJugadores(self):
        return self.inicioJugador1
    
    
    
    # Desplaza todo el decorado y los objetos (plataformas, enemigos) que hay en el en el eje x
    def desplazarDecoradox(self, desplazamiento, jugadorAMover):
        # Desplazamos el jugador a mover hacia el lado contrario
        jugadorAMover.posicionx -= desplazamiento
        jugadorAMover.rect.left = jugadorAMover.posicionx
        # La imagen que se muestra hacia ese lado
        self.posicionx += desplazamiento*2
        
        # Actualizamos cual es la parte de la imagen del decorado que se muestra en pantalla
        self.rectSubimagen.left = self.posicionx
        
        # Desplaza todo el decorado y los objetos (plataformas, enemigos) que hay en el eje y
    def desplazarDecoradoy(self, desplazamiento, jugadorAMover):
        # Desplazamos el jugador a mover hacia el lado contrario
        jugadorAMover.posiciony -= desplazamiento
        jugadorAMover.rect.top = jugadorAMover.posiciony
        # La imagen que se muestra hacia ese lado
        self.posiciony += desplazamiento*2
        
        # Actualizamos cual es la parte de la imagen del decorado que se muestra en pantalla
        self.rectSubimagen.topleft = (self.posicionx, self.posiciony)
    
    def actualizarScroll(self, jugador1):
        
        if (jugador1.posicionx<MINIMO_X_JUGADOR):
            desplazamiento = MINIMO_X_JUGADOR - jugador1.posicionx
            jugador1.posicionx = MINIMO_X_JUGADOR

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.posicionx <= 0:
                self.posicionx = 0

            # Si se puede hacer scroll a la izquierda
            else:
                # Desplazamos todo el decorado a la izquierda
                self.desplazarDecoradox(-desplazamiento, jugador1)

        # Si el jugador quiere moverse mas a la derecha
        if (jugador1.posicionx>MAXIMO_X_JUGADOR):
            desplazamiento = jugador1.posicionx - MAXIMO_X_JUGADOR
            jugador1.posicionx = MAXIMO_X_JUGADOR
 
            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.posicionx + ANCHO_PANTALLA >= self.image.get_rect().right:
                self.posicionx = self.image.get_rect().right - ANCHO_PANTALLA
 
            # Si se puede hacer scroll a la derecha
            else:
                # Desplazamos todo el decorado a la derecha
                self.desplazarDecoradox(desplazamiento, jugador1)
        
        
        # Si el jugador de la izquierda quiere moverse mas hacia arriba
        if (jugador1.posiciony<MINIMO_Y_JUGADOR):
            desplazamiento = MINIMO_Y_JUGADOR - jugador1.posiciony
            jugador1.posiciony = MINIMO_Y_JUGADOR

            # Si el escenario ya está arriba del todo, no lo movemos mas
            if self.posiciony <= 0:
                self.posiciony = 0

            # Si se puede hacer scroll hacia arriba
            else:
                # Desplazamos todo el decorado hacia arriba
                self.desplazarDecoradoy(-desplazamiento, jugador1)

        # Si el jugador de la derecha quiere moverse mas hacia abajo
        if (jugador1.posiciony>MAXIMO_Y_JUGADOR):
            desplazamiento = jugador1.posiciony - MAXIMO_Y_JUGADOR
            jugador1.posiciony = MAXIMO_Y_JUGADOR
 
            # Si el escenario ya está abajo del todo, no lo movemos mas
            if self.posiciony + ALTO_PANTALLA >= self.image.get_rect().right:
                self.posiciony = self.image.get_rect().right - ALTO_PANTALLA
 
            # Si se puede hacer scroll abajo
            else:
                # Desplazamos todo el decorado a la derecha, incluyendo el jugador que este en la izquierda
                self.desplazarDecoradoy(desplazamiento, jugador1)
                
    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se actualizan los jugadores con los movimientos a realizar
    #  Se actualiza la posicion del sol y el color del cielo
    #  Se mueven los enemigos como sea conveniente
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se actualiza el scroll del decorado y los objetos en el
    def update(self, tiempo):
        
            if(pygame.sprite.collide_mask(self.imagemask, self.jugador1)==None):
               self.grupoJugadores.update(tiempo)
#                print pygame.sprite.collide_mask(self.imagemask, self.jugador1)
               print "uhahsd"
               print (int(self.jugador1.posicionx))
               print (int(self.jugador1.posiciony))
#                print self.imagemask.mask.get_at((int(self.jugador1.posicionx), int(self.jugador1.posiciony)))
            else: print "Algoooooo"   
            self.actualizarScroll(self.jugador1)
        
    def dibujar(self):
        
        self.grupoJugadores.draw(self.pantalla)
        
        self.pantalla.blit(self.image, self.rect, self.rectSubimagen)
        
        self.grupoJugadores.draw(self.pantalla)

    def evento(self, event):
        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

    
    #Clase que crea la mascara para las colisiones
class Colisiones(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image, -1)
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA*4, ALTO_PANTALLA*4))
        self.rect = self.image.get_rect()
        self.rect.bottom = ALTO_PANTALLA*4
        self.mask=pygame.mask.from_surface(self.image)
        self.posicionx = 0
        self.posiciony = 0
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.topleft = (self.posicionx, self.posiciony)
    def update(self):
        pass
    