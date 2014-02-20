# -*- encoding: utf-8 -*-

# Modulos
import pygame, pyglet
import sys
from escena import *
from pygame.locals import *

FPS = 60

class Director():

    def __init__(self):
        # Escena actual
        self.escena = None
        # Flag que nos indica cuando quieren salir de la escena o del programa
        self.salir_escena = False
        self.salir_programa = False
        # Reloj
        self.reloj = pygame.time.Clock()

    def ejecutar(self):

        # Si la escena es de juego, la ejecutamos como un bucle
        if isinstance(self.escena, EscenaPygame):

            tiempo_pasado = 0
            
            # El bucle del juego, las acciones que se realicen se harán en cada escena
            while not self.salir_escena and not self.salir_programa:

                # Sincronizar el juego a un determinado fps
                tiempo_pasado = self.reloj.tick(FPS)
            
                # Para cada evento
                for event in pygame.event.get():

                    # Si se sale del programa
                    if event.type == pygame.QUIT:
                        self.salirPrograma()

                    # Realizamos los eventos
                    self.escena.evento(event)

                # Actualiza la escena y nos dice si hay que terminar
                self.escena.update(tiempo_pasado)

                # Se dibuja en pantalla
                self.escena.dibujar()
                pygame.display.flip()

            # Si hemos salido del bucle, finalizamos pygame
            pygame.quit()


        # Si no, si la escena es de animacion con pyglet, la ejecutamos de esa manera
        elif isinstance(self.escena, EscenaPyglet):
            # Registramos que se actualice segun la frecuencia de frames por segundo
            pyglet.clock.schedule_interval(self.escena.update, 1/float(FPS))

            # Ejecutamos la aplicacion de pyglet
            pyglet.app.run()

            # Cuando hayamos terminado la animacion con pyglet, cerramos la ventana
            self.escena.close()
        else:
            raise Exception('No se que tipo de escena es')
        
        # Al final se devuelve si se quiere salir del programa, ademas de salir de la escena
        return self.salir_programa

    def cambiarEscena(self, escena):
        self.salir_escena = False
        self.salir_programa = False
        self.escena = escena

    def salirEscena(self):
        # Si es una escena de pyglet
        if isinstance(self.escena, EscenaPyglet):
            # Indicamos que la función programada no se vuelva a llamar
            # De no ser así, se llamará la próxima vez que se invocle el bucle de pyglet
            pyglet.clock.unschedule(self.escena.update)
            # Salimos del bucle de pyglet
            pyglet.app.exit()
        self.salir_escena = True

    def salirPrograma(self):
        self.salirEscena()
        self.salir_programa = True
