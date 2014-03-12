# -*- encoding: utf-8 -*-

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Escena:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def evento(self, *args):
        raise NotImplemented("Tiene que implementar el metodo evento.")

    def dibujar(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
    
    def hide(self):
        raise NotImplemented("Tienes q implementar el método ocultar.")

class EscenaPygame(Escena):

    def __init__(self, director):
        Escena.__init__(self, director)


class EscenaPyglet(Escena):

    def __init__(self, director):
        Escena.__init__(self, director)
