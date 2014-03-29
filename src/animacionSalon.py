# -*- encoding: utf-8 -*-

import pyglet
from escena import *
import random
from faseInvestigacion import *
from xml.dom import minidom

VELOCIDAD_BADASS = 30 # Pixels por segundo




# -------------------------------------------------
# Clase para las animaciones que solo ocurriran una vez
#  (sin bucles)

class AnimacionSalon(EscenaPyglet, pyglet.window.Window):
    
    
    def __init__(self, director):
        # Constructores de las clases padres
        EscenaPyglet.__init__(self, director)
        pyglet.window.Window.__init__(self, ANCHO_PANTALLA, ALTO_PANTALLA)
        
        pyglet.resource.path = ['.', '../res', '../res/maps', '../res/Sounds', '../res/Sprites']
        pyglet.resource.reindex()

         #carga del fichero de textos
        self.fullname = os.path.join('', "../res/Dialogos/animacionSalon.xml")
        # La imagen de fondo
        self.imagen = pyglet.image.load('../res/maps/primerinterior.png')
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
#         self.lluviaSon = pyglet.resource.media('rain.wav', streaming=False)
        self.rayoSon = pyglet.resource.media('thunderS.wav', streaming=False)
        self.puertaSon = pyglet.resource.media('door.wav', streaming=False)
        self.focoSon = pyglet.resource.media('foco.wav', streaming=False)
        self.luzSon = pyglet.resource.media('lightSwitch.wav', streaming=False)
        self.suspSon = pyglet.resource.media('suspense.wav', streaming=False)
        self.playerP = self.puertaSon.play()
        self.playerR = self.rayoSon.play()
        self.playerR.pause() 
        self.playerF = self.focoSon.play()
        self.playerF.pause() 
        self.playerI = self.luzSon.play()
        self.playerI.pause()
        self.playerM = self.suspSon.play()
        self.playerM.pause()

   
        poli = pyglet.resource.image('poli.png')
        self.poli = pyglet.sprite.Sprite(poli, batch=self.batch, group=self.grupoMedio)
        self.poli.set_position(ANCHO_PANTALLA/2,2.7*ALTO_PANTALLA/4)
        self.poli.scale = 1.3
        
        fanuel = pyglet.resource.image('fanuel.png')
        self.fanuel = pyglet.sprite.Sprite(fanuel, batch=self.batch, group=self.grupoMedio)
        self.fanuel.set_position(ANCHO_PANTALLA/3,2.25*ALTO_PANTALLA/4)
        self.fanuel.scale = 0.5
        
        
        bolio = pyglet.resource.image('bolioQ.png')
        self.bolio = pyglet.sprite.Sprite(bolio, batch=self.batch, group=self.grupoMedio)
        self.bolio.set_position(ANCHO_PANTALLA/6,ALTO_PANTALLA/12)
        self.bolio.scale = 0.9
        
        
        charles = pyglet.resource.image('charlesQ.png')
        self.charles = pyglet.sprite.Sprite(charles, batch=self.batch, group=self.grupoMedio)
        self.charles.set_position(ANCHO_PANTALLA/7,ALTO_PANTALLA/1.9)
        self.charles.scale = 1.3
        
        
        esperanza = pyglet.resource.image('esperanzaQ.png')
        self.esperanza = pyglet.sprite.Sprite(esperanza, batch=self.batch, group=self.grupoMedio)
        self.esperanza.set_position(ANCHO_PANTALLA/5,ALTO_PANTALLA/3)
        self.esperanza.scale = 0.9
        
        
        rateos = pyglet.resource.image('rateosQ.png')
        self.rateos = pyglet.sprite.Sprite(rateos, batch=self.batch, group=self.grupoMedio)
        self.rateos.set_position(3*ANCHO_PANTALLA/4,ALTO_PANTALLA/1.75)
        self.rateos.scale = 0.8
        
        self.animacionCervero = [
            pyglet.image.AnimationFrame(pyglet.resource.image('scienQ.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('scienQE.png'), 2.5),
            pyglet.image.AnimationFrame(pyglet.resource.image('scienQL.png'), 0.5),
            pyglet.image.AnimationFrame(pyglet.resource.image('scienQL.png', flip_x=True), 0.5) ]
        self.cervero = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionCervero), batch=self.batch, group=self.grupoMedio)
        self.cervero.set_position(3.5*ANCHO_PANTALLA/4,ALTO_PANTALLA/12)
        self.cervero.scale = 0.9

        # La animacion del corredor: hay que leerlo de la hoja de Sprite

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
        numImagenes = [6, 6, 6, 1]
        pfile=open('../res/BadassCoordJugador.txt','r')
        datos=pfile.read()
        pfile.close()
        datos = datos.split()
        BadassIzdaFrames = []
        espaldasFrames = []
        for coord in range(6):
            BadassIzdaFrames.append(pyglet.image.AnimationFrame(hoja.get_region(int(datos[24 + coord*4]), hoja.height-int(datos[24 + coord*4 + 1])-int(datos[24 + coord*4 + 3]), int(datos[24 + coord*4 + 2]), int(datos[24 + coord*4 + 3])), 0.1))
        for coord in range(6):
            espaldasFrames.append(pyglet.image.AnimationFrame(hoja.get_region(int(datos[coord*4]), hoja.height-int(datos[coord*4 + 1])-int(datos[coord*4 + 3]), int(datos[coord*4 + 2]), int(datos[coord*4 + 3])), 0.1))
        # A partir de los frames, se crea la animacion
        self.animacionIzda = pyglet.sprite.Sprite(pyglet.image.Animation(BadassIzdaFrames), batch=self.batch, group=self.grupoMedio)
        self.animacionIzda.set_position(2.5*ANCHO_PANTALLA/4,ALTO_PANTALLA/1.75)
        self.animacionIzda.scale = 1
        # Se podria, igual que las anteriores, no haberla creado, sino haberlo hecho
        #  cuando fuese necesario que apareciera, pero en este caso se crea aqui y se
        #  pone como invisible hasta cuandos ea necesario que aparezca
        self.animacionIzda.visible = True
        # A partir de los frames, se crea la animacion
        self.animacionEspaldas = pyglet.sprite.Sprite(pyglet.image.Animation(espaldasFrames), batch=self.batch, group=self.grupoMedio)
        self.animacionEspaldas.set_position(ANCHO_PANTALLA/2 + self.animacionEspaldas.width,ALTO_PANTALLA/1.75)
        self.animacionEspaldas.scale = 1
        # Se podria, igual que las anteriores, no haberla creado, sino haberlo hecho
        #  cuando fuese necesario que apareciera, pero en este caso se crea aqui y se
        #  pone como invisible hasta cuandos ea necesario que aparezca
        self.animacionEspaldas.visible = False
        self.animacionBadassQ = [
            pyglet.image.AnimationFrame(pyglet.resource.image('badassQL.png'), 3),
            pyglet.image.AnimationFrame(pyglet.resource.image('badassQLL.png'), 4.5),
            pyglet.image.AnimationFrame(pyglet.resource.image('badassQ.png'), 0.5),
            pyglet.image.AnimationFrame(pyglet.resource.image('badassQL.png', flip_x=True), 0.5) ]
        self.badassQ = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionBadassQ), batch=self.batch, group=self.grupoMedio)
        self.badassQ.set_position(ANCHO_PANTALLA/2 + self.badassQ.width,2.5*ALTO_PANTALLA/4)
        self.badassQ.scale = 1
        self.badassQ.visible = False
        self.quieto = False
        badassF = pyglet.resource.image('badassF.png')
        self.badassF = pyglet.sprite.Sprite(badassF, batch=self.batch, group=self.grupoMedio)
        self.badassF.set_position(ANCHO_PANTALLA/2 + self.badassQ.width,2.5*ALTO_PANTALLA/4)
        self.badassF.visible = False
        self.text = pyglet.text.Label('Empecemos entonces...',
                      font_name='X-Files', 
                      font_size=26, color=(255, 255, 255, 255),
                      x=ANCHO_PANTALLA/4 + 26, y=ALTO_PANTALLA-26, batch = self.batch,
                      anchor_x='center', anchor_y='center',
                      group = self.grupoDelante)
        self.text.draw()
        self.tiempo = 0
        foco = pyglet.resource.image('foco.png')
        self.foco = pyglet.sprite.Sprite(foco, batch=self.batch, group=self.grupoDelante)
        self.foco.scale = 1
        self.foco.visible = False
#         self.animacionFondoR = [
#             pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorR.png'), 1),
#             pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorO.png'), 1.5),
#             pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorN.png'), 9.5) ]
#         self.animacionFondoR = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionFondoR), batch=self.batch, group=self.grupoMedio)
#         self.animacionFondoR.scale = float(ANCHO_PANTALLA) / 704
#         self.animacionFondoR.visible = False

        self.animacionFondoR = [
            pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorR.png'), 0.5),
            pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorO.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorN.png'), 5.5) ]
        self.animacionFondoR = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionFondoR), batch=self.batch, group=self.grupoMedio)
        self.animacionFondoR.scale = float(ANCHO_PANTALLA) / 704
        self.animacionFondoR.visible = False

        self.animacionFondoF = [
            pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorR.png'), 2),
            pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorN.png'), 29.5) ]
        self.animacionFondoF = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionFondoF), batch=self.batch, group=self.grupoDelante)
        self.animacionFondoF.scale = float(ANCHO_PANTALLA) / 704
        self.animacionFondoF.visible = False

        self.animacionPuntos = [
            pyglet.image.AnimationFrame(pyglet.resource.image('punto1.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('punto2.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('punto3.png'), 1),
            pyglet.image.AnimationFrame(pyglet.resource.image('punto4.png'), 5) ]
        self.animacionPuntos1 = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPuntos), batch=self.batch, group=self.grupoMedio)
        self.animacionPuntos1.set_position(self.badassQ.x, self.badassQ.y + 60)
        self.animacionPuntos1.visible = False
        self.animacionPuntos2 = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPuntos), batch=self.batch, group=self.grupoMedio)
        self.animacionPuntos2.set_position(self.poli.x, self.poli.y + 40)
        self.animacionPuntos2.visible = False
        self.animacionPuntos3 = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPuntos), batch=self.batch, group=self.grupoMedio)
        self.animacionPuntos3.set_position(self.cervero.x, self.cervero.y + 60)
        self.animacionPuntos3.visible = False
        self.animacionPuntos4 = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPuntos), batch=self.batch, group=self.grupoMedio)
        self.animacionPuntos4.set_position(self.bolio.x, self.bolio.y + 60)
        self.animacionPuntos4.visible = False
        self.animacionPuntos5 = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPuntos), batch=self.batch, group=self.grupoMedio)
        self.animacionPuntos5.set_position(self.esperanza.x, self.esperanza.y + 60)
        self.animacionPuntos5.visible = False
        self.animacionPuntos6 = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPuntos), batch=self.batch, group=self.grupoMedio)
        self.animacionPuntos6.set_position(self.rateos.x, self.rateos.y + 60)
        self.animacionPuntos6.visible = False
        portada = pyglet.resource.image('portada.png')
        self.portada = pyglet.sprite.Sprite(portada, batch=self.batch, group=self.grupoDelante)
        self.portada.set_position(0,0)
        self.portada.visible = False
        self.tiempoTrans = 0

    # El metodo para eliminar una animacion determinada
    def eliminarAnimacion(self, tiempo, animacion):
        animacion.delete()
        
        
        # Metodo que hace aparecer una animacion de humo en el cielo
#     def aparecerRayo(self, tiempo):
#         #=======================================================================
#         animacionRayo = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionRayoFrames), batch=self.batch, group=self.grupoDetras)
#         # La escalamos un factor aleatorio para dar sensacion de profundidad
#         animacionRayo.scale = 1
#         animacionRayo.rotation = 45
#         # Decimos que aparezca en un sitio aleatorio del cielo
#         animacionRayo.set_position(random.uniform(20, ANCHO_PANTALLA-20), random.uniform(20, ALTO_PANTALLA-20))
# 
#         self.rayoSon.play()
#         # Programamos que se elimine la animacion cuando termine
#         pyglet.clock.schedule_once(self.eliminarAnimacion, animacionRayo.image.get_duration(), animacionRayo)
#         #=======================================================================
    
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
        self.salirEscena()


    # El evento relativo al clic del raton
    def on_mouse_press(self, x, y, button, modifiers):
        # Si se pulsa el boton izquierdo
        if (pyglet.window.mouse.LEFT == button):
            self.salirEscena()
        return

    def salirEscena(self):
        jugador1 = Jugador()
        escenaSig = FaseInvestigacion(self.director, jugador1)
        self.director.cambiarEscena(escenaSig)

    def close(self):
        # Restablecemos la duracion de cada frame del tanque
#         for frame in self.tanque.image.frames:
#             frame.duration = 0.05
        self.playerP.pause()
        self.playerR.pause() 
        self.playerF.pause() 
        self.playerI.pause()
        self.playerM.pause()
        pyglet.window.Window.close(self);


    # El evento que sera llamado periodicamente
    def update(self, tiempo):
        # Y si la animacion del protagonista caminando a la izda es visible, la movemos hacia la izquierda
        if self.animacionIzda.visible:
            self.animacionIzda.x -= tiempo*VELOCIDAD_BADASS
            # Ademas, si llega al centro cambiamos la animación
            if (self.animacionIzda.x<(ANCHO_PANTALLA/2 + self.badassQ.width))&(self.animacionIzda.x>(ANCHO_PANTALLA/2 + self.badassQ.width)-5):
                self.animacionIzda.visible = False
                self.animacionEspaldas.visible = True
                
        if self.animacionEspaldas.visible:
            self.animacionEspaldas.y += tiempo*VELOCIDAD_BADASS
            if self.animacionEspaldas.y>2.5*ALTO_PANTALLA/4:
                self.animacionEspaldas.visible = False
                self.badassQ.visible = True
                self.quieto = True
        
        #Cuando el personaje se para, empezamos a mostrar los dialogos
        if self.quieto:
#             self.text.delete()

            if self.tiempoTrans < 4:   
                self.text.delete()
                xmldoc = minidom.parse(self.fullname)
                self.textList = xmldoc.getElementsByTagName('phrase') 
                self.text = pyglet.text.Label(self.textList[0].attributes['content'].value,
                      font_name='X-Files', multiline=True,
                      font_size=16, color=(0, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                      x=self.poli.x, y=self.poli.y + 80, batch = self.batch,
                      anchor_x='center', anchor_y='center',
                      group = self.grupoDelante)
                self.text.draw()   
            else:  
                if self.tiempoTrans < 8: 
                    self.text.delete()
                    self.text = pyglet.text.Label(self.textList[1].attributes['content'].value,
                          font_name='X-Files', multiline=True,
                          font_size=16, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                          x=self.badassQ.x, y=self.badassQ.y+120, batch = self.batch,
                          anchor_x='center', anchor_y='center',
                          group = self.grupoDelante)
                    self.text.draw()
                else: 
                    if self.tiempoTrans < 25: 
                        self.text.delete()
                        self.text = pyglet.text.Label(self.textList[2].attributes['content'].value+"\n"+self.textList[3].attributes['content'].value+"\n"+self.textList[4].attributes['content'].value,
                              font_name='X-Files', multiline=True,
                              font_size=16, color=(0, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                              x=self.poli.x, y=self.poli.y + 120, batch = self.batch,
                              anchor_x='center', anchor_y='center',
                              group = self.grupoDelante)
                        self.text.draw()
                        if self.tiempoTrans > 21:
                            self.text.delete()
                            self.foco.visible = True
                            self.foco.set_position(-980 + self.badassQ.x,-1015 + self.badassQ.y + 10)
                            self.text = pyglet.text.Label(self.textList[5].attributes['content'].value,
                              font_name='X-Files', multiline=True,
                              font_size=16, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                              x=self.badassQ.x, y=self.badassQ.y+120, batch = self.batch,
                              anchor_x='center', anchor_y='center',
                              group = self.grupoDelante)
                            self.text.draw()
                    else: 
                        if self.tiempoTrans < 28: 
                            self.foco.visible = False
                            self.text.delete()
                            self.text = pyglet.text.Label(self.textList[6].attributes['content'].value,
                                  font_name='X-Files', multiline=True,
                                  font_size=16, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                                  x=self.badassQ.x, y=self.badassQ.y+120, batch = self.batch,
                                  anchor_x='center', anchor_y='center',
                                  group = self.grupoDelante)
                            self.text.draw()
                        else: 
                            if self.tiempoTrans < 38: 
                                self.text.delete()
                                self.text = pyglet.text.Label(self.textList[7].attributes['content'].value,
                                      font_name='X-Files', multiline=True,
                                      font_size=16, color=(0, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                                      x=self.poli.x, y=self.poli.y + 120, batch = self.batch,
                                      anchor_x='center', anchor_y='center',
                                      group = self.grupoDelante)
                                self.text.draw()
                            else: 
                                if self.tiempoTrans < 48: 
                                    self.foco.set_position(-980 + ANCHO_PANTALLA/6,-1015 + ALTO_PANTALLA/12)
                                    self.foco.visible = True
                                    if self.tiempoTrans > 38 and self.tiempoTrans < 38.05:
                                                    self.playerF = self.focoSon.play()
                                    self.text.delete()
                                    self.text = pyglet.text.Label(self.textList[8].attributes['content'].value,
                                          font_name='X-Files', multiline=True,
                                          font_size=16, color=(0, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                                          x=self.poli.x, y=self.poli.y + 80, batch = self.batch,
                                          anchor_x='center', anchor_y='center',
                                          group = self.grupoDelante)
                                    self.text.draw()
                                else: 
                                    if self.tiempoTrans < 58: 
                                        self.foco.set_position(-980 + ANCHO_PANTALLA/5,-1015 + ALTO_PANTALLA/3)
                                        if self.tiempoTrans > 48 and self.tiempoTrans < 48.05:
                                                    self.playerF = self.focoSon.play()
                                        self.text.delete()
                                        self.text = pyglet.text.Label(self.textList[9].attributes['content'].value,
                                              font_name='X-Files', multiline=True,
                                              font_size=16, color=(0, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                                              x=self.poli.x, y=self.poli.y + 80, batch = self.batch,
                                              anchor_x='center', anchor_y='center',
                                              group = self.grupoDelante)
                                        self.text.draw()
                                    else: 
                                        if self.tiempoTrans < 80: 
                                            if self.tiempoTrans < 68: 
                                                self.foco.set_position(-980 + ANCHO_PANTALLA/7,-1015 + ALTO_PANTALLA/1.9)
                                                if self.tiempoTrans > 58 and self.tiempoTrans < 58.05:
                                                    self.playerF = self.focoSon.play()
                                                self.text.delete()
                                                self.text = pyglet.text.Label(self.textList[10].attributes['content'].value,
                                                      font_name='X-Files', multiline=True,
                                                      font_size=16, color=(0, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                                                      x=self.poli.x, y=self.poli.y + 80, batch = self.batch,
                                                      anchor_x='center', anchor_y='center',
                                                      group = self.grupoDelante)
                                                self.text.draw()
                                            else:
                                                if self.tiempoTrans < 73:
                                                    self.text.delete()
                                                    self.foco.visible = False
                                #                                                     self.text.delete()
                                                    if self.tiempoTrans > 68 and self.tiempoTrans < 68.05:
                                                        self.playerR = self.rayoSon.play()
                                                    self.animacionFondoR.visible = True
                                                else:
                                                    self.animacionFondoR.visible = False
                                                    if self.tiempoTrans > 73 and self.tiempoTrans < 73.05:
                                                        self.playerI = self.luzSon.play()
                                                    self.text.delete()
                                                    self.text = pyglet.text.Label(self.textList[11].attributes['content'].value,
                                                          font_name='X-Files', multiline=True,
                                                          font_size=16, color=(255, 0, 0, 255), width = ANCHO_PANTALLA/3, 
                                                          x=self.charles.x+40, y=self.charles.y + 80, batch = self.batch,
                                                          anchor_x='center', anchor_y='center',
                                                          group = self.grupoDelante)
                                                    self.text.draw()
                                                    self.animacionPuntos1.visible = True
                                                    self.animacionPuntos2.visible = True
                                                    self.animacionPuntos3.visible = True
                                                    self.animacionPuntos4.visible = True
                                                    self.animacionPuntos5.visible = True
                                                    self.animacionPuntos6.visible = True
                                        else: 
                                            if self.tiempoTrans < 90: 
                                                self.animacionPuntos1.visible = False
                                                self.animacionPuntos2.visible = False
                                                self.animacionPuntos3.visible = False
                                                self.animacionPuntos4.visible = False
                                                self.animacionPuntos5.visible = False
                                                self.animacionPuntos6.visible = False
                                                self.foco.visible = True
                                                self.foco.set_position(-980 + 3*ANCHO_PANTALLA/4,-1015 + ALTO_PANTALLA/1.75)
                                                if self.tiempoTrans > 80 and self.tiempoTrans < 80.05:
                                                    self.playerF = self.focoSon.play()
                                                self.text.delete()
                                                self.text = pyglet.text.Label(self.textList[12].attributes['content'].value,
                                                      font_name='X-Files', multiline=True,
                                                      font_size=16, color=(0, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                                                      x=self.poli.x, y=self.poli.y + 60, batch = self.batch,
                                                      anchor_x='center', anchor_y='center',
                                                      group = self.grupoDelante)
                                                self.text.draw()
                                            else: 
                                                if self.tiempoTrans < 100: 
                                                    self.foco.set_position(-980 + 3.5*ANCHO_PANTALLA/4,-1015 + ALTO_PANTALLA/12)
                                                    if self.tiempoTrans > 90 and self.tiempoTrans < 90.05:
                                                        self.playerF = self.focoSon.play()
                                                    self.text.delete()
                                                    self.text = pyglet.text.Label(self.textList[13].attributes['content'].value,
                                                          font_name='X-Files', multiline=True,
                                                          font_size=16, color=(0, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                                                          x=self.poli.x, y=self.poli.y + 40, batch = self.batch,
                                                          anchor_x='center', anchor_y='center',
                                                          group = self.grupoDelante)
                                                    self.text.draw()
                                                
                                                else: 
                                                    if self.tiempoTrans < 105: 
                                                        self.foco.visible = False
                                                        self.badassF.visible = True
                                                        self.badassQ.visible = False
                                                        self.text.delete()
                                                        self.text = pyglet.text.Label(self.textList[14].attributes['content'].value,
                                                              font_name='X-Files', multiline=True,
                                                              font_size=16, color=(255, 255, 255, 255), width = ANCHO_PANTALLA/1.5, 
                                                              x=self.badassF.x + 150, y=self.badassF.y+120, batch = self.batch,
                                                              anchor_x='center', anchor_y='center',
                                                              group = self.grupoDelante)
                                                        self.text.draw()
                                                    else:  
                                                        if self.tiempoTrans < 110: 
                                                            self.text.delete()
                                                            if self.tiempoTrans > 105 and self.tiempoTrans < 105.04:
                                                                self.playerR = self.rayoSon.play()
                            #                                 self.animacionFondoR = [
                            #                                     pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorR.png'), 2),
                            #                                     pyglet.image.AnimationFrame(pyglet.resource.image('primerinteriorN.png'), 29.5) ]
                            #                                 self.animacionFondoR = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionFondoR), batch=self.batch, group=self.grupoDelante)
                            #                                 self.animacionFondoR.scale = float(ANCHO_PANTALLA) / 704
                                                            self.animacionFondoF.visible = True
                                                        else: 
                                                            if self.tiempoTrans < 110.05 and self.tiempoTrans > 110: 
                                                                self.playerM = self.suspSon.play()
                                                            else: 
                                                                if self.tiempoTrans > 114 and self.tiempoTrans < 116: 
                                                                    self.animacionFondoF.visible = False
                                                                    self.portada.visible = True
                                                                else: 
                                                                    if self.tiempoTrans < 125 and self.tiempoTrans > 119: 
                                                                        self.text.delete()
                                                                        self.text = pyglet.text.Label(self.textList[15].attributes['content'].value,
                                                                              font_name='X-Files', multiline=True,
                                                                              font_size=16, color=(255, 0, 0, 255), width = ANCHO_PANTALLA/3, 
                                                                              x=self.charles.x+40, y=self.charles.y + 80, batch = self.batch,
                                                                              anchor_x='center', anchor_y='center',
                                                                              group = self.grupoDelante)
                                                                        self.text.draw()
                                                                    elif self.tiempoTrans > 125: 
                                                                        self.salirEscena()
            self.tiempoTrans += tiempo
#             print self.tiempoTrans

