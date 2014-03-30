# -*- coding: utf-8 -*-
# Importar modulos
import director
from director import *
from EscenaMenu import *
from animacion import *




class AplicacionJuego():

    def __init__(self):
        # Creamos el director
        self.director = Director()

    
    def ejecutar(self):
            # Creamos la escena con la pantalla inicial
            escena = EscenaMenu(self.director)
            # Le decimos al director en que escena estamos
            self.director.cambiarEscena(escena)
            # Y ejecutamos el bucle
            salir_programa = self.director.ejecutar()
            if (salir_programa):
                # Si ademas de salir de la escena, se quiere salir del programa, se finaliza
                sys.exit()


if __name__ == '__main__':
    juego = AplicacionJuego()
    juego.ejecutar()

