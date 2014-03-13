# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4

#Posturas
SPRITE_QUIETO = 3
SPRITE_ANDANDO = 1
SPRITE_SUBIENDO = 0
SPRITE_BAJANDO = 2

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 1 / VELOCIDAD_JUGADOR


# -------------------------------------------------
# -------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------
# -------------------------------------------------

# El colorkey es es color que indicara la transparencia
#  Si no se usa, no habra transparencia
#  Si se especifica -1, el color de transparencia sera el del pixel (0,0)
#  Si se especifica un color, ese sera la transparencia
def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
#     image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            print colorkey
        image.set_colorkey(colorkey, RLEACCEL)
        print image.get_at((0,0))
    return image

# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# Clases Personaje

class Personaje(pygame.sprite.Sprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Posicion que ocupa el personaje
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion,location):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self);
        # Se carga la hoja
        
        self.hoja = load_image(archivoImagen,-1)
#         self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = ARRIBA

        # Leemos las coordenadas de un archivo de texto
        fullname = os.path.join('', archivoCoordenadas)
        pfile=open(fullname,'r')
        datos=pfile.read()
        pfile.close()
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 4):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;
        
        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

                # La posicion x e y que ocupa
        self.posicionx = 0
        self.posiciony = 0
        self.rect.left = 0
        self.rect.bottom = 0

        # Las velocidades de caminar y salto
        self.velocidad = velocidad
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura(0,0)
        self.mask = pygame.mask.from_surface(load_image("../res/Sprites/badassmask.png"))
        self.rect = self.image.get_rect(center=location)


    def establecerPosicion(self, posicionx, posiciony):
        self.posicionx = posicionx
        self.posiciony = posiciony
        self.rect.left = self.posicionx
        self.rect.bottom = self.posiciony

    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
            self.movimiento = movimiento


    def actualizarPostura(self, x, y):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if x<0:
                self.numPostura = SPRITE_ANDANDO
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif x>0:
                self.numPostura = SPRITE_ANDANDO
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)
            
            elif y>0:
                self.numPostura = SPRITE_BAJANDO
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            elif y<0:
                self.numPostura = SPRITE_SUBIENDO
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
                
            else:
                self.numPostura = SPRITE_QUIETO

    def movimientoHorizontal(self, incrementox):
        # Esta mirando hacia ese lado
        self.mirando = self.movimiento
        # Actualizamos la posicion
        self.posicionx += incrementox
        self.rect.left = self.posicionx
        self.numPostura = SPRITE_ANDANDO
                
    def movimientoVertical(self, incrementoy):
        # Esta mirando hacia ese lado
        self.mirando = self.movimiento
        # Actualizamos la posicion
        self.posiciony += incrementoy
        self.rect.bottom = self.posiciony
        if (incrementoy<0):
            self.numPostura = SPRITE_SUBIENDO
        else:
            self.numPostura = SPRITE_BAJANDO
            
    def check_collisions(self, move, level_mask):
        """
Call collision_detail for the x and y components of our movement vector.
"""
        x_change = self.collision_detail(move, level_mask, 0)
        self.rect.move_ip((x_change,0))
        y_change = self.collision_detail(move, level_mask, 1)
        self.rect.move_ip((0,y_change))
        return ( x_change, y_change)

    def collision_detail(self, move, level_mask, index):
        """
Check for collision and if found decrement vector by single pixels
until clear.
"""
        test_offset = list(self.rect.topleft)
        test_offset[index] += move[index]
        while level_mask.overlap_area(self.mask, test_offset):
            move[index] += (1 if move[index]<0 else -1)
            test_offset = list(self.rect.topleft)
            test_offset[index] += move[index]
        return move[index]

    def update(self, tiempo, level_mask):
        # Si vamos a la izquierda
        if self.movimiento == IZQUIERDA:
            # Realizamos ese movimiento a la izquierda
            self.movimientoHorizontal(-self.velocidad*tiempo)
                
        # Si vamos a la derecha
        elif self.movimiento == DERECHA:
            # Realizamos ese movimiento a la derecha
            self.movimientoHorizontal( self.velocidad*tiempo)

        # Si estamos saltando
        elif self.movimiento == ARRIBA:
            self.movimientoVertical( -self.velocidad*tiempo)

        # Si estamos saltando
        elif self.movimiento == ABAJO:
            self.movimientoVertical( self.velocidad*tiempo)
            
        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
                self.numPostura = SPRITE_QUIETO

        # Actualizamos la imagen a mostrar
        x,y = self.check_collisions(move, level_mask)
        self.actualizarPostura(x, y)
        return
    
    def draw(self, surface):
        """Basic draw function."""
        surface.blit(self.image, self.rect)



# -------------------------------------------------
# Clase Jugador
DIRECT_DICT = {pygame.K_UP : ( 0,-1),
               pygame.K_DOWN : ( 0, 1),
               pygame.K_RIGHT: ( 1, 0),
               pygame.K_LEFT : (-1, 0)}
class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'../res/Sprites/badassSprites.png','../res/BadassCoordJugador.txt', [6, 6, 6, 1], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR,(0,0));
        self.speed = 7

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        move = [0, 0]
#         print "l"
        for key in DIRECT_DICT:
#             print teclasPulsadas[arriba]
            if teclasPulsadas[key]:
                for i in (0, 1):
                    move[i] += DIRECT_DICT[key][i]*self.speed
        return move

    def update(self, level_mask, keys):
        move = self.mover(keys, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        x,y = self.check_collisions(move, level_mask)
        self.actualizarPostura(x, y)
        
# -------------------------------------------------
# Clase NoJugador
DIRECT_DICT = {pygame.K_UP : ( 0,-1),
               pygame.K_DOWN : ( 0, 1),
               pygame.K_RIGHT: ( 1, 0),
               pygame.K_LEFT : (-1, 0)}
class NoJugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self, imagen, coordenadas):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'../res/Sprites/badassSprites.png','../res/BadassCoordJugador.txt', [6, 6, 6, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR,(0,0));
        self.speed = 7

    def mover(self, direccion):
        if direccion == 0:
            move = (0,self.speed)
        elif direccion == 1:
            move = (self.speed,0)
        elif direccion == 2:
            move = (0,-self.speed)
        elif direccion == 3:
            move = (-self.speed,0)
        return move

    def update(self, level_mask, direccion):
        move = self.mover(direccion)
        x,y = self.check_collisions(move, level_mask)
        self.actualizarPostura(x, y)
