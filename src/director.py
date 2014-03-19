# -*- encoding: utf-8 -*-
#wehe
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
        self.quiere_salir_escena = False
        self.quiere_cambiar_escena = None
        self.quiere_apilar_escena = None
        self.pilaEscenas=[]
        # Reloj
        self.reloj = pygame.time.Clock()

    def ejecutar(self):

        # Si la escena es de juego, la ejecutamos como un bucle
        if isinstance(self.escena, EscenaPygame):
          
            while not self.salir_programa:
                tiempo_pasado = 0
                self.salir_escena = False;
                # El bucle del juego, las acciones que se realicen se harán en cada escena
                while not self.salir_escena:
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
                    
                    #Comprobamos si quiere abandonar la escena
                    if(self.quiere_salir_escena):
                        self.ejecutarSalirEscena()
                        
                    
                        
                    #Comprobamos si quiere cambiar de escena
                    if(self.quiere_apilar_escena != None):
                        self.ejecutarApilarEscena()
                #Comprobamos si quiere cambiar de escena
                if(self.quiere_cambiar_escena != None):
                    self.ejecutarCambiarEscena()
                if self.escena == None:
                    self.salir_programa = True
            
            # Si hemos salido del bucle, finalizamos pygame
            pygame.quit()
            
        # Si no, si la escena es de animacion con pyglet, la ejecutamos de esa manera
        elif isinstance(self.escena, EscenaPyglet):
            # Registramos que se actualice segun la frecuencia de frames por segundo
            pyglet.clock.schedule_interval(self.escena.update, 1/float(FPS))

            # Ejecutamos la aplicacion de pyglet
            pyglet.app.run()
        else:
            self.escena = None
            raise Exception('No se que tipo de escena es')
        
        # Al final se devuelve si se quiere salir del programa, ademas de salir de la escena
        return self.salir_programa

    def cambiarEscena(self, escena):
        if self.escena == None:
            self.escena = escena
            self.salir_escena = False
            self.salir_programa = False
        else:
                 # Si es una escena de pyglet
            if isinstance(self.escena, EscenaPyglet):
                self.escena.close()
                # Indicamos que la función programada no se vuelva a llamar
                # De no ser así, se llamará la próxima vez que se invocle el bucle de pyglet
                pyglet.clock.unschedule(self.escena.update)
                # Salimos del bucle de pyglet
                pyglet.app.exit()
                self.escena = escena
                self.ejecutar()
            else:
                self.quiere_cambiar_escena = escena
                self.salir_escena = True
        
    def ejecutarCambiarEscena(self):  
        self.escena = self.quiere_cambiar_escena
        self.quiere_cambiar_escena = None

    def apilarEscena(self, escena):
        # Si es una escena de pyglet
        if isinstance(self.escena, EscenaPyglet):
            #self.escena.close()
            self.escena.hide()
            # Indicamos que la función programada no se vuelva a llamar
            # De no ser así, se llamará la próxima vez que se invocle el bucle de pyglet
            pyglet.clock.unschedule(self.escena.update)
            # Salimos del bucle de pyglet
            pyglet.app.exit()
            self.pilaEscenas.append(self.escena)
            self.escena = escena
            self.ejecutar()
        else:
            self.quiere_apilar_escena = escena
        
    def ejecutarApilarEscena(self):
        self.salir_escena = True
        self.pilaEscenas.append(self.escena)
        self.escena = self.quiere_apilar_escena
        self.quiere_apilar_escena = None

    def salirEscena(self):
        # Si es una escena de pyglet
        if isinstance(self.escena, EscenaPyglet):
            self.escena.close();
            # Indicamos que la función programada no se vuelva a llamar
            # De no ser así, se llamará la próxima vez que se invocle el bucle de pyglet
            pyglet.clock.unschedule(self.escena.update)
            # Salimos del bucle de pyglet
            pyglet.app.exit()
            if(len(self.pilaEscenas)!=0):
                self.escena = self.pilaEscenas.pop()
                self.escena.show()
                self.ejecutar()
        else:
            self.quiere_salir_escena = True
        
    def ejecutarSalirEscena(self):
        self.quiere_salir_escena = False
        if(len(self.pilaEscenas)==0):
            self.salir_escena = True
            self.escena = None
        else:
            self.escena = self.pilaEscenas.pop()

    def salirPrograma(self):
        self.salirEscena()
        self.salir_programa = True
