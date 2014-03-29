# -*- encoding: utf-8 -*-

import pyglet
from escena import *
import random
from animacionSalon import *
from xml.dom import minidom
import os

# Funcion auxiliar que crea una animacion a partir de una imagen que contiene la animacion
#  dividida en filas y columnas
def crearFramesAnimacion(nombreImagen, filas, columnas):
    # Cargamos la secuencia de imagenes del archivo
    secuenciaImagenes = pyglet.image.ImageGrid(pyglet.image.load(nombreImagen), filas, columnas)
    # Creamos la secuencia de frames
    secuenciaFrames = []
    # Para cada fila, del final al principio
    for fila in range(filas, 0, -1):
        end = fila * columnas
        start = end - (columnas -1) -1
        # Para cada imagen de la fila
        for imagen in secuenciaImagenes[start:end:1]:
            # Creamos un frame con esa imagen, indicandole que tendra una duracion de 0.5 segundos
            frame = pyglet.image.AnimationFrame(imagen, 0.1)
            #  y la anadimos a la secuencia de frames
            secuenciaFrames.append(frame)

    # Devolvemos la secuencia de frames
    return secuenciaFrames




# -------------------------------------------------
# Clase para las animaciones que solo ocurriran una vez
#  (sin bucles)

class EscenaAnimacionFinalMalo(EscenaPyglet, pyglet.window.Window):
    
    
    def __init__(self, director, xml):
        # Constructores de las clases padres
        EscenaPyglet.__init__(self, director)
        self.window = pyglet.window.Window.__init__(self, ANCHO_PANTALLA, ALTO_PANTALLA)
        
        pyglet.resource.path = ['.', '../res', '../res/maps', '../res/Sounds', '../res/Sprites']
        pyglet.resource.reindex()

        #carga del fichero de textos
        self.fullname = os.path.join('', xml)
        # La imagen de fondo
        self.imagen = pyglet.resource.image('finalmaloescena.png')
        self.imagen = pyglet.sprite.Sprite(self.imagen)
        self.imagen.set_position(100, -120)
#         self.imagen.scale = float(ANCHO_PANTALLA) / self.imagen.width

        self.tiempoTrans = 0
        # Las animaciones que habra en esta escena
        # No se crean aqui las animaciones en si, porque se empiezan a reproducir cuando se crean
        # Lo que se hace es cargar los frames de disco para que cuando se creen ya esten en memoria
        
        

        # Creamos el batch de las animaciones
        self.batch = pyglet.graphics.Batch()
        # Y los grupos para ponerlas por pantalla
        self.grupoDetras =  pyglet.graphics.OrderedGroup(0)
        self.grupoMedio =   pyglet.graphics.OrderedGroup(1)
        self.grupoDelante = pyglet.graphics.OrderedGroup(2)

        pyglet.font.add_file('../res/XFILES.TTF')
        xfiles = pyglet.font.load('X-Files')
        self.lluviaSon = pyglet.resource.media('rain.wav', streaming=False)
        self.rayoSon = pyglet.resource.media("thunder.wav", streaming=False)
        self.hangSon = pyglet.resource.media("hanging.wav", streaming=False)
        self.playerR = self.rayoSon.play()
        self.playerL = self.lluviaSon.play()
        self.playerH = self.hangSon.play()
        self.playerL.stop()


        # La animacion de la lluvia: creamos los frames
        #=======================================================================
        self.animacionHangBadass = [
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass1.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass2.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass3.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass2.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass1.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass2.png', flip_x=True), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass3.png', flip_x=True), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass2.png', flip_x=True), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('hangBadass1.png'), 1)]
        #=======================================================================
        self.animacionHangBadass = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionHangBadass), batch=self.batch, group=self.grupoDetras)
        self.animacionHangBadass.scale = 2
        # Decimos que aparezca en un sitio aleatorio del cielo
        self.animacionHangBadass.set_position(333, 200)
        
        
        # Esta animacion aparecera cada tiempo determinado
        #=======================================================================
        pyglet.clock.schedule_interval(self.aparecerRayo, 20.5)
        pyglet.clock.schedule_interval(self.sonidoLluvia, 6.0)
        pyglet.clock.schedule_interval(self.sonidoSoga, 6.0)
        #=======================================================================
        
        xmldoc = minidom.parse(self.fullname)
        self.textList = xmldoc.getElementsByTagName('phrase') 
        self.text = pyglet.text.Label(self.textList[0].attributes['content'].value,
                      font_name='X-Files', multiline=True,
                      font_size=26, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/2 - 20, 
                      x=ANCHO_PANTALLA/4, y=ALTO_PANTALLA/2, batch = self.batch,
                      anchor_x='center', anchor_y='center',
                      group = self.grupoDelante)
        self.text.draw()

    # El metodo para eliminar una animacion determinada
    def eliminarAnimacion(self, tiempo, animacion):
        animacion.delete()
        
        
        # Metodo que hace sonar un rayo
    def aparecerRayo(self, tiempo):
        #=======================================================================
        self.playerR = self.rayoSon.play()
        
        #=======================================================================
        
        # Metodo que hace aparecer una animacion de badass
    def aparecerHBad(self, tiempo):
        #=======================================================================
        animacionHangBadass = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionHangBadass), batch=self.batch, group=self.grupoDetras)
        # La escalamos un factor aleatorio para dar sensacion de profundidad
        animacionHangBadass.scale = 2
        # Decimos que aparezca en un sitio aleatorio del cielo
        animacionHangBadass.set_position(350, 250)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionHangBadass.image.get_duration(), animacionHangBadass)
        #=======================================================================
         
    # Metodo para hacer aparecer el sonido de lluvia
    def sonidoLluvia(self, tiempo):
        self.playerL = self.lluviaSon.play()

    # Metodo para hacer aparecer el sonido de la soga
    def sonidoSoga(self, tiempo):
        self.playerH = self.hangSon.play()

    # El evento relativo a la pulsacion de una tecla
    def on_key_press(self, symbol, modifiers):
        # Si se pulsa Escape, se sale del programa
        if symbol == pyglet.window.key.ESCAPE:
            self.director.salirEscena()


    # el evento que se ejecuta cada vez que hay que dibujar la pantalla
    def on_draw(self):
        # Si la ventana esta visible
        if self.visible:
            # Borramos lo que hay en pantalla
            self.clear()
            # Dibujamos la imagen
            if self.imagen!=None:
                self.imagen.draw()
            # Y, para cada animacion, la dibujamos
            # Para hacer esto, le decimos al batch que se dibuje
            self.batch.draw()


    # Si intentan cerrar esta ventana, saldremos de la escena
    def on_close(self):
        pyglet.clock.unschedule(self.aparecerRayo)
        pyglet.clock.unschedule(self.aparecerLluvia)
        pyglet.clock.unschedule(self.sonidoLluvia)
        self.director.salirEscena()


    # El evento relativo al clic del raton
    def on_mouse_press(self, x, y, button, modifiers):
        # Si se pulsa el boton izquierdo
        if (pyglet.window.mouse.LEFT == button):
            self.salirEscena()
        return

    def salirEscena(self):
        escenaSig = AnimacionSalon(self.director)
        self.director.cambiarEscena(escenaSig)    
        
    def close(self):
        # Restablecemos la duracion de cada frame del tanque
#         for frame in self.tanque.image.frames:
#             frame.duration = 0.05
#         pyglet.window.Window.dispatch_events()
        self.fin = True
        pyglet.clock.unschedule(self.aparecerRayo)
        pyglet.clock.unschedule(self.sonidoLluvia)
        pyglet.clock.unschedule(self.sonidoSoga)
        self.playerL.pause()
        self.playerR.pause()
        self.playerH.pause()
#         self.player.stop()
#         stop = time()+6
#         while time() < stop:
#             print"ll"
        pyglet.window.Window.close(self);


    # El evento que sera llamado periodicamente
    def update(self, tiempo):
        if self.tiempoTrans < 10 and self.tiempoTrans > 5: 
            self.text.delete()
            self.text = pyglet.text.Label(self.textList[1].attributes['content'].value,
                  font_name='X-Files', multiline=True,
                  font_size=26, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/2 - 20, 
                  x=ANCHO_PANTALLA/4, y=ALTO_PANTALLA/2, batch = self.batch,
                  anchor_x='center', anchor_y='center',
                  group = self.grupoDelante)
            self.text.draw()
        elif self.tiempoTrans < 15 and self.tiempoTrans > 10:  
                self.text.delete()
                self.text = pyglet.text.Label(self.textList[2].attributes['content'].value,
                      font_name='X-Files', multiline=True,
                      font_size=26, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/2 - 20, 
                      x=ANCHO_PANTALLA/4, y=ALTO_PANTALLA/2, batch = self.batch,
                      anchor_x='center', anchor_y='center',
                      group = self.grupoDelante)
                self.text.draw()
        elif self.tiempoTrans > 20: 
                self.salirEscena()
#             self.tiempo += 1
#             print self.tiempo
        self.tiempoTrans += tiempo
        print self.tiempoTrans


