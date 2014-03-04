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

VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo


MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - 100

class Intro(EscenaPygame):
    def __init__(self, director, jugador1):

        # Primero invocamos al constructor de la clase padre
        EscenaPygame.__init__(self, director)

        # Inicializamos la pantalla y el modo grafico
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Al diablo el cafe")


        self.jugador1 = jugador1
        self.grupoJugadores = pygame.sprite.Group(jugador1)
        
        jugador1.establecerPosicion(100, 100)
        
        jugador1.numPostura = QUIETO
        
        plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
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
        self.image = load_image('../res/maps/primerinterior.png', -1)
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA, ALTO_PANTALLA))

        self.rect = self.image.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # Creamos el fondo
        #self.sol = Fondo('../res/maps/gransalon.png')

        # Que parte del decorado estamos visualizando
        self.posicionx = 0
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = self.posicionx

        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo
        plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
        # La plataforma del techo del edificio
        plataformaCasa = Plataforma(pygame.Rect(870, 417, 200, 10))
        # y el grupo con las mismas
        self.grupoPlataformas = pygame.sprite.Group( plataformaSuelo, plataformaCasa )

    def posicionesInicioJugadores(self):
        return self.inicioJugador1
    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se actualizan los jugadores con los movimientos a realizar
    #  Se actualiza la posicion del sol y el color del cielo
    #  Se mueven los enemigos como sea conveniente
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se actualiza el scroll del decorado y los objetos en el
    def update(self, tiempo):
        
        self.grupoJugadores.update(self.grupoPlataformas, tiempo)
        
        
        # Actualizamos la posicion del sol y el color del cielo
        #self.sol.update(tiempo)
        print("updatevacio")

        
    def dibujar(self):
        # Ponemos primero el sol y cielo
        #self.sol.dibujar(self.pantalla)
        # Después la imagen de fondo
        self.grupoJugadores.draw(self.pantalla)
        self.pantalla.blit(self.image, self.rect, self.rectSubimagen)

    def evento(self, event):
        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

# -------------------------------------------------
# Clase Plataforma

class Plataforma(pygame.sprite.Sprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self);
        # Rectangulo con las coordenadas que ocupara
        self.rect = rectangulo
        # Posicion en el eje x (en el eje y no hace falta, no hay scroll vertical)
        self.posx = self.rect.left

        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = None


    def update(self,desplazamiento):
        self.posx += desplazamiento
        self.rect.left = self.posx


# -------------------------------------------------
# Clase Fondo

class Fondo(pygame.sprite.Sprite):
    def __init__(self,nombreImagen):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self);

        self.image = load_image(nombreImagen,-1)
        self.image = pygame.transform.scale(self.image, (300, 200))

        self.rect = self.image.get_rect()
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        self.posicionx += VELOCIDAD_SOL * tiempo
        if (self.posicionx - self.rect.width >= ANCHO_PANTALLA):
            self.posicionx = 0
        self.rect.right = self.posicionx
        # Calculamos el color del cielo
        if self.posicionx >= ((self.rect.width + ANCHO_PANTALLA) / 2):
            ratio = 2 * ((self.rect.width + ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + ANCHO_PANTALLA)
        else:
            ratio = 2 * self.posicionx / (self.rect.width + ANCHO_PANTALLA)
        self.colorCielo = (100*ratio, 200*ratio, 255)
        
    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        # Y ponemos el sol
        pantalla.blit(self.image, self.rect)

