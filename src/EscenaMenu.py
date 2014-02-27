# -*- encoding: utf-8 -*-

import pyglet
from pygame.locals import *
from personajes import load_image
from escena import *


class EscenaMenu(EscenaPyglet, pyglet.window.Window):

    def __init__(self, director):

        # Constructores de las clases padres
        EscenaPyglet.__init__(self, director)
        pyglet.window.Window.__init__(self, ANCHO_PANTALLA, ALTO_PANTALLA)

        # La imagen de fondo
        self.imagen = pyglet.image.load('../res/sprites/fondo.png')
        self.imagen = pyglet.sprite.Sprite(self.imagen)
        self.imagen.scale = float(ANCHO_PANTALLA) / self.imagen.width
        self.imagen.set_position(0, (ALTO_PANTALLA - self.imagen.height)/2)

        # Los botones
        self.botonJugar = pyglet.sprite.Sprite(pyglet.image.load('../res/sprites/botonJugar.png'))
        self.botonSalir = pyglet.sprite.Sprite(pyglet.image.load('../res/sprites/botonSalir.png'))
        self.botonJugar.scale = 0.4
        self.botonSalir.scale = 0.4
        self.botonJugar.set_position(550, 90)
        self.botonSalir.set_position(630, 90)

        # Creamos el batch de las animaciones
        self.batch = pyglet.graphics.Batch()

    # El evento relativo a la pulsacion de una tecla
    def on_key_press(self, symbol, modifiers):
        # Si se pulsa Escape, se sale del programa
        if symbol == pyglet.window.key.ESCAPE:
            self.director.salirPrograma()


    # el evento que se ejecuta cada vez que hay que dibujar la pantalla
    def on_draw(self):
        # Si la ventana esta visible
        if self.visible:
            # Borramos lo que hay en pantalla
            self.clear()
            # Dibujamos la pantalla
            self.imagen.draw()
            # Dibujamos los botones
            self.botonJugar.draw()
            self.botonSalir.draw()
            # Ponemos las animaciones
            self.batch.draw()

    # Si intentan cerrar esta ventana, saldremos del programa
    def on_close(self):
        self.director.salirPrograma()

    # El evento relativo al clic del raton
    def on_mouse_press(self, x, y, button, modifiers):
        # Si se pulsa el boton izquierdo
        if(pyglet.window.mouse.LEFT == button):
            # Miramos a ver en que boton se ha pulsado, y se hace la accion correspondiente
            if  (x>=self.botonJugar.x) and (x<=(self.botonJugar.x + self.botonJugar.width)) and (y>=self.botonJugar.y) and (y<=(self.botonJugar.y + self.botonJugar.height)):
                self.director.salirEscena()
            elif  (x>=self.botonSalir.x) and (x<=(self.botonSalir.x + self.botonSalir.width)) and (y>=self.botonSalir.y) and (y<=(self.botonSalir.y + self.botonSalir.height)):
                self.director.salirPrograma()
    
    def update(self, *args):
        return