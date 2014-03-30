# -*- encoding: utf-8 -*-

import pyglet
from escena import *
import random
from animacionSalon import *
from xml.dom import minidom

VELOCIDAD_IZDA = 50 # Pixels por segundo
VELOCIDAD_ARRIBA = 30 # Pixels por segundo

class EscenaAnimacion(EscenaPyglet, pyglet.window.Window):
    
    
    def __init__(self, director):
        # Constructores de las clases padres
        EscenaPyglet.__init__(self, director)
        self.window = pyglet.window.Window.__init__(self, ANCHO_PANTALLA, ALTO_PANTALLA)
        
        pyglet.resource.path = ['.', '../res', '../res/maps', '../res/Sounds', '../res/Sprites']
        pyglet.resource.reindex()

        #carga del fichero de textos
        self.fullname = os.path.join('', "../res/Dialogos/escenaAnimacion.xml")
        # La imagen de fondo
        self.imagen = pyglet.image.load('../res/maps/entrada.jpg')
        self.imagen = pyglet.sprite.Sprite(self.imagen)
        self.imagen.scale = float(ANCHO_PANTALLA) / self.imagen.width

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
        self.playerR = self.rayoSon.play()
        self.playerL = self.lluviaSon.play()
        self.playerL.stop()
        

        # La animacion del rayo
        #=======================================================================
        self.animacionRayoFrames = [
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0001.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0002.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0003.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0004.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0005.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0006.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0007.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0008.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0009.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/bolt_strike_0010.png'), None),
            ]
#         self.animacionRayoFrames.scale = 1
#         self.animacionRayoFrames.rotation = 90

        # Esta animacion aparecera en el segundo determinado
        #=======================================================================
        pyglet.clock.schedule_interval(self.aparecerRayo, 2.5)
        #=======================================================================
        
        
        
        # La animacion de la lluvia: creamos los frames
        #=======================================================================
        self.animacionLluviaFrames = [
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain0.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain1.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain2.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain3.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain4.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain5.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain6.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain7.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain8.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain9.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain10.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain1.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain1.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain3.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain4.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain5.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain6.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain7.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain8.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain9.png'), 0.1),
            pyglet.image.AnimationFrame(pyglet.image.load('../res/Sprites/rain10.png'), 0.1)]
        #=======================================================================
        # Registramos para que llueva siempre en la escena
        pyglet.clock.schedule_once(self.aparecerLluvia, 0.1)
        pyglet.clock.schedule_interval(self.aparecerLluvia, 2.0)
        pyglet.clock.schedule_once(self.sonidoLluvia, 0)
        pyglet.clock.schedule_interval(self.sonidoLluvia, 6.0)
    
        # La animacion del protagonista: hay que leerlo de la hoja de Sprite

        # Leemos la hoja del Sprite del fichero
        hoja = pyglet.image.load('../res/Sprites/badass.png')

        # Introducimos manualmente el valor del canal alpha:
        #  Aquellos pixels cuyo RGB sea igual al pixel de la posicion (0, 0) no se veran
        rawimage = hoja.get_image_data()
        format = 'RGBA'
        pitch = rawimage.width * len(format)
        pixels = rawimage.get_data(format, pitch)
        pixels = list( pixels )
        r = pixels[0]
        g = pixels[1]
        b = pixels[2]
        for i in range(0, len(pixels), 4):
            if (pixels[i]==r) and (pixels[i+1]==g) and (pixels[i+2]==b):
                pixels[i+3] = str(chr(0))
            else:
                pixels[i+3] = str(chr(255))
        hoja.set_data('RGBA', pitch, "".join(pixels))

        # Leemos las coordenadas de un archivo de texto
        numImagenes = [6, 6, 6]
        pfile=open('../res/BadassCoordJugador.txt','r')
        datos=pfile.read()
        pfile.close()
        datos = datos.split()
        izdaFrames = []
        espaldasFrames = []
        for coord in range(6):
            izdaFrames.append(pyglet.image.AnimationFrame(hoja.get_region(int(datos[24 + coord*4]), hoja.height-int(datos[24 + coord*4 + 1])-int(datos[24 + coord*4 + 3]), int(datos[24 + coord*4 + 2]), int(datos[24 + coord*4 + 3])), 0.1))
        for coord in range(6):
            espaldasFrames.append(pyglet.image.AnimationFrame(hoja.get_region(int(datos[coord*4]), hoja.height-int(datos[coord*4 + 1])-int(datos[coord*4 + 3]), int(datos[coord*4 + 2]), int(datos[coord*4 + 3])), 0.1))
        # A partir de los frames, se crea la animacion
        self.animacionIzda = pyglet.sprite.Sprite(pyglet.image.Animation(izdaFrames), batch=self.batch, group=self.grupoDetras)
        self.animacionIzda.set_position(700,40)
        self.animacionIzda.scale = 1
        self.animacionIzda.visible = True
        # A partir de los frames, se crea la animacion
        self.animacionEspaldas = pyglet.sprite.Sprite(pyglet.image.Animation(espaldasFrames), batch=self.batch, group=self.grupoDetras)
        self.animacionEspaldas.set_position(ANCHO_PANTALLA/2-20,40)
        self.animacionEspaldas.scale = 1
        # Se podria, igual que las anteriores, no haberla creado, sino haberlo hecho
        #  cuando fuese necesario que apareciera, pero en este caso se crea aqui y se
        #  pone como invisible hasta cuandos ea necesario que aparezca
        self.animacionEspaldas.visible = False
        
        xmldoc = minidom.parse(self.fullname)
        self.textList = xmldoc.getElementsByTagName('phrase') 
        self.text = pyglet.text.Label(str(self.textList[0].attributes['content'].value)+"\n"+self.textList[1].attributes['content'].value+"\n"+self.textList[2].attributes['content'].value+"\n",
                      font_name='X-Files', multiline=True,
                      font_size=26, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/2 - 20, 
                      x=ANCHO_PANTALLA/4, y=ALTO_PANTALLA/2, batch = self.batch,
                      anchor_x='center', anchor_y='center',
                      group = self.grupoDelante)
        self.text.draw()



    # Metodo que hace moverse el mapa
    def moverMapa(self, tiempo):
        #=======================================================================
        self.imagen.set_position(self.imagen.x, self.imagen.y -7)
        #=======================================================================

    # El metodo para eliminar una animacion determinada
    def eliminarAnimacion(self, tiempo, animacion):
        animacion.delete()
        
        
        # Metodo que hace aparecer una animacion de rayo en el cielo
    def aparecerRayo(self, tiempo):
        #=======================================================================
        animacionRayo = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionRayoFrames), batch=self.batch, group=self.grupoDetras)
        animacionRayo.scale = 1
        animacionRayo.rotation = 45
        # Decimos que aparezca en un sitio aleatorio del cielo
        animacionRayo.set_position(random.uniform(20, ANCHO_PANTALLA-20), random.uniform(20, ALTO_PANTALLA-20))

        self.playerR = self.rayoSon.play()
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionRayo.image.get_duration(), animacionRayo)
        
        #=======================================================================
        

    # Metodo para hacer aparecer la lluvia por toda la pantalla
    def aparecerLluvia(self, tiempo):
        # Creamos la animacion de la lluvia
        #=======================================================================
        animacionLluvia = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia.scale = 1
        animacionLluvia.set_position(0, 0)
        animacionLluvia2 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia2.scale = 1
        animacionLluvia2.set_position(animacionLluvia.width, animacionLluvia.height-5)
         
        animacionLluvia3 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia3.scale = 1
        animacionLluvia3.set_position(animacionLluvia.width, 0)
         
        animacionLluvia4 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia4.scale = 1
        animacionLluvia4.set_position(0, animacionLluvia.height-5)
         
        animacionLluvia5 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia5.scale = 1
        animacionLluvia5.set_position(2*animacionLluvia.width, 0)
         
        animacionLluvia6 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia6.scale = 1
        animacionLluvia6.set_position(0, 2*(animacionLluvia.height-5))
         
        animacionLluvia7 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia7.scale = 1
        animacionLluvia7.set_position(2*animacionLluvia.width, 2*(animacionLluvia.height-5))
         
        animacionLluvia8 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia8.scale = 1
        animacionLluvia8.set_position(2*animacionLluvia.width, animacionLluvia.height-5)
         
        animacionLluvia9 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia9.scale = 1
        animacionLluvia9.set_position(animacionLluvia.width, 2*(animacionLluvia.height-5))
        
        
        animacionLluvia10 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia10.scale = 1
        animacionLluvia10.set_position(3*animacionLluvia.width, 0)
         
        animacionLluvia11 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia11.scale = 1
        animacionLluvia11.set_position(3*animacionLluvia.width, animacionLluvia.height-5)
         
        animacionLluvia12 = pyglet.sprite.Sprite(pyglet.image.Animation( self.animacionLluviaFrames ), batch=self.batch, group=self.grupoDelante)
#         animacionLluvia.scale = 3.5
        animacionLluvia12.scale = 1
        animacionLluvia12.set_position(3*animacionLluvia.width, 2*(animacionLluvia.height-5))
        
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia.image.get_duration(), animacionLluvia)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia2.image.get_duration(), animacionLluvia2)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia3.image.get_duration(), animacionLluvia3)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia4.image.get_duration(), animacionLluvia4)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia5.image.get_duration(), animacionLluvia5)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia6.image.get_duration(), animacionLluvia6)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia7.image.get_duration(), animacionLluvia7)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia8.image.get_duration(), animacionLluvia8)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia9.image.get_duration(), animacionLluvia9)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia10.image.get_duration(), animacionLluvia10)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia11.image.get_duration(), animacionLluvia11)
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLluvia12.image.get_duration(), animacionLluvia12)
        
        #=======================================================================
        
    # Metodo para hacer aparecer el sonido de lluvia
    def sonidoLluvia(self, tiempo):
        self.playerL = self.lluviaSon.play()

    
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
        pyglet.clock.unschedule(self.aparecerLluvia)
        pyglet.clock.unschedule(self.sonidoLluvia)
        self.playerL.pause()
        self.playerR.pause()
#         self.player.stop()
#         stop = time()+6
#         while time() < stop:
#             print"ll"
        pyglet.window.Window.close(self);


    # El evento que sera llamado periodicamente
    def update(self, tiempo):
        # Y si la animacion de la izquierdar es visible, la movemos
        if self.animacionIzda.visible:
            self.animacionIzda.x -= tiempo*VELOCIDAD_IZDA
            # Ademas, si llega al centro cambiamos la animación
            if (self.animacionIzda.x<(ANCHO_PANTALLA/2-20))&(self.animacionIzda.x>(ANCHO_PANTALLA/2)-25):
                self.text.delete()
                self.text = pyglet.text.Label(self.textList[3].attributes['content'].value,
                      font_name='X-Files', multiline=True,
                      font_size=26, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/2 - 50, 
                      x=ANCHO_PANTALLA/4, y=ALTO_PANTALLA/2, batch = self.batch,
                      anchor_x='center', anchor_y='center',
                      group = self.grupoDelante)
                self.text.draw()
                self.text2 = pyglet.text.Label(self.textList[4].attributes['content'].value,
                      font_name='X-Files', multiline=True,
                      font_size=26, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/2 - 50, 
                      x=3.1*ANCHO_PANTALLA/4, y=ALTO_PANTALLA/2, batch = self.batch,
                      anchor_x='center', anchor_y='center',
                      group = self.grupoDelante)
                self.text2.draw()
                pyglet.clock.schedule_interval(self.moverMapa, 0.5)
                self.animacionIzda.visible = False
                self.animacionEspaldas.visible = True
        if self.animacionEspaldas.visible:
            self.animacionEspaldas.y += tiempo*VELOCIDAD_ARRIBA
            if (self.animacionEspaldas.y>(ALTO_PANTALLA/2))&(self.animacionEspaldas.y<(ALTO_PANTALLA/2)+5):
                self.text.delete()
                self.text2.delete()
                self.text = pyglet.text.Label(self.textList[5].attributes['content'].value,
                      font_name='X-Files', multiline=True,
                      font_size=26, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/2 - 50, 
                      x=3.1*ANCHO_PANTALLA/4, y=ALTO_PANTALLA/2, batch = self.batch,
                      anchor_x='center', anchor_y='center',
                      group = self.grupoDelante)
                self.text.draw()
            if self.animacionEspaldas.y>450:
                self.text.delete()
                self.salirEscena()


