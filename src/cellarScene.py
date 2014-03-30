# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
from FinalScene import *
from item import *
from evento import *

OPT_KEYS = {pygame.K_1 : 1,
               pygame.K_2 : 2,
               pygame.K_3 : 3,
               pygame.K_4 : 4,
               pygame.K_5 : 5,
               pygame.K_6 : 6,
               pygame.K_7 : 7,
               pygame.K_8 : 8,
               pygame.K_9 : 9,
               pygame.K_0 : 10}
OPT_KEYS_PUZZLE = {pygame.K_1 : 0,
               pygame.K_2 : 1,
               pygame.K_3 : 2,
               pygame.K_4 : 3,
               pygame.K_5 : 4,
               pygame.K_6 : 5,
               pygame.K_7 : 6,
               pygame.K_8 : 7,
               pygame.K_9 : 8,
               pygame.K_0 : 9}
TIEMPODIALOGO = 10000
class CellarScene(EscenaPygame):
    def __init__(self, director, jugador1):

        EscenaPygame.__init__(self, director)
       
        pygame.display.set_caption("Cellar")
        pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        """Initialize things; create a Player; create a Level."""
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.player = jugador1
        self.player.speed = 7
        self.player.objetos = []
        fondo = pygame.image.load("../res/maps/first.png")
        self.level = Level(fondo, self.screen_rect.copy(), self.player,"../res/maps/FirstCellarRoomMask.png", (500,400))
        self.grupoJugadores = pygame.sprite.Group(jugador1)
        self.hojas =[]
        self.pared =[]
        
        self.dialogo = 6
        self.opcion = False
        self.optEl = 0
        self.eventoT = True
        self.activarEv = False
        self.accion = False
        self.inventario = False
        self.mostrar = True
        
        self.cambiarDia = False
        self.numRes = 0
        self.eventoAct = False
        
        self.accionO = None
        self.accionT = None
        self.accionR = []
        self.accionResult = None
        
        self.text = Text()
        self.eventos = []
        self.eventosActivos = []
        
        #Bloque de colocación de items
        self.libro0 = Item(10, "libroCellar.xml",  "../res/Sprites/libroinvisible.png", (743, 268))
        self.libro0.cambiarEstado(None, 0)
        self.libro1 = Item(10, "libroCellar.xml",  "../res/Sprites/libroinvisible.png", (743, 130))
        self.libro1.cambiarEstado(None, 1)
        self.libro2 = Item(10, "libroCellar.xml",  "../res/Sprites/libroinvisible.png", (743, 200))
        self.libro2.cambiarEstado(None, 2)
        self.pizarra = Item(10, "pizarraCellar.xml",  "../res/Sprites/pizarrainvisible.png", (350, 54))
        self.jarron = Item(10, "jarronCellar.xml",  "../res/Sprites/libroinvisible.png", (236, 74))
        self.puerta = Item(10, "puertaCellar.xml",  "../res/Sprites/cellarSceneDoor.png", (136, 141))
        self.puerta.cambiarEstado(None, 2)
        self.puertaEntrada = Item(10, "puertaCellar.xml",  "../res/Sprites/libroinvisible.png", (521, 471))
        self.libreria = Item(10, "estanteriaCellar.xml",  "../res/Sprites/libroinvisible.png", (68, 77))
        self.grupoObj = pygame.sprite.Group(self.libro0,self.libro1,self.libro2, self.pizarra, self.jarron, self.puerta, self.libreria, self.puertaEntrada)
        self.puzzleAct = False
        self.puzzleFin = False
        self.opcionPuz = False
        
        self.eventoInicial = EventoCambioEstado((236, 74),"evInicial", self.puerta, 2, "evCellar.xml", None)
        self.eventosActivos.append(self.eventoInicial)
        
        self.eventoFinalScene = EventoFinal((0,0), "FinalScene", self)
        self.eventos.append(self.eventoFinalScene)
        
        #Cargamos la música        
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load("../res/Sounds/fear.ogg")
        pygame.mixer.music.play(-1)
        
    def update(self, tiempo):
        if (self.accion):
            self.tiempoDial += tiempo
#             print self.tiempoDial
#             print self.cambiarDia
            if self.cambiarDia:
#                 print self.numRes
                self.accionT, self.accionR, self.accionResult = self.continuarAccion(self.accionO, self.numRes) 
                self.cambiarDia = False
                self.tiempoDial = 0
        elif (self.inventario):
            if self.optEl != 0:
                self.inventario = False
                if not self.mostrar:
                    self.cambiarDia = False
                    self.numRes = 0
                    self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO, self.player.objetos[self.optEl - 1])
                self.optEl = 0
        elif (self.puzzleAct):
            if self.puzzleFin:
                self.puzzleAct = False
                self.puzzleFin = False
                self.numRes = 0
                self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO, self.player.objetos[self.optEl - 1])
#         elif (self.eventoAct):
#             self.accionT, self.accionR, self.accionResult = self.continuarAccion(self.accionO, self.numRes) 
        else:   
            self.level.update(self.keys)
    
        
    def dibujar(self):
        s = self.level.draw(self.screen)
        self.grupoObj.draw(s)
        self.grupoJugadores.draw(s)
        if self.accion:
           self.interact(self.tiempoDial, s)   
        if self.inventario:
            self.mostrarInv(s)
        if self.puzzleAct:
            self.puzzle(s)
        
        self.screen.blit(s, (0,0), self.level.viewport)

    def evento(self, event):
        # Indicamos la acciÃ³n a realizar segun la tecla pulsada para cada jugador
        self.keys = pygame.key.get_pressed()
        if self.opcion:
            for key in OPT_KEYS:
                if self.keys[key]:
                    if (self.accionR == [] and len(self.player.objetos) >= OPT_KEYS[key]):
                        self.optEl = OPT_KEYS[key]
                        self.opcion = False
                    elif OPT_KEYS[key] <= len(self.accionR):
                        self.optEl = OPT_KEYS[key]
                        self.opcion = False
                        if self.accionR != None and self.accionR != []:
                            self.numRes = self.accionR[self.optEl - 1][1]
                            self.optEl = 0
                            self.cambiarDia = True
                            
        if self.opcionPuz:
            if len(self.hojas) == 0:
                self.comprobarPuzzle(self.pared)
                self.opcionPuz = False
                self.puzzleFin = True
            for key in OPT_KEYS_PUZZLE:
                if self.keys[key] and len(self.hojas) > OPT_KEYS_PUZZLE[key]:
                    hoja = self.hojas.pop(int(OPT_KEYS_PUZZLE[key]))
                    self.pared.append(hoja)
#                     if (self.accionR == [] and len(self.player.objetos) >= OPT_KEYS[key]):
#                         self.optEl = OPT_KEYS[key]
#                         self.opcion = False
#                     elif OPT_KEYS[key] <= len(self.accionR):
#                         self.optEl = OPT_KEYS[key]
#                         self.opcion = False
#                         if self.accionR != None and self.accionR != []:
#                             self.numRes = self.accionR[self.optEl - 1][1]
#                             self.optEl = 0
#                             self.cambiarDia = True
        #Interactuar con npc/objeto sin utilizar nada
        if self.keys[K_SPACE] and (not self.accion) and (not self.inventario):
            if (pygame.sprite.spritecollideany(self.player, self.grupoObj) != None):
                self.cambiarDia = False
                self.numRes = 0
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoObj)
                self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
        #Abrir el inventario
        if (self.keys[K_i]) and (not self.accion) and (not self.inventario):
            #Interactuar con npc/objeto utilizando un objeto
#             if (pygame.sprite.spritecollideany(self.player, self.grupoObj) != None):
#                 self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoObj)
#                 self.mostrar = False
#             else: 
            self.mostrar = True
            self.inventario = True
        #Cerrar el inventario en caso de estar solo mostrandolo
        if self.inventario and self.mostrar:
            if self.keys[K_u]:
                self.optEl = 1
            
        if self.keys[K_q] and self.accion:
            if self.tiempoDial > TIEMPODIALOGO:
                self.tiempoDial = TIEMPODIALOGO*2
            else:
                self.tiempoDial = TIEMPODIALOGO
        if self.keys[K_h]  :  
            self.player.objetos.append("esoasdlngrgudfpabsdiuasdpo")
            self.player.objetos.append("emergycbjkqworghbfxgcpsefñjak")
            self.hojas.append("esoasdlngrgudfpabsdiuasdpo")
            self.hojas.append("emergycbjkqworghbfxgcpsefñjak")
            self.player.objetos.append("nknpvwkfbopfwowbfldfowb")
            self.player.objetos.append("aefbjiophzqgmifzrt")
            self.hojas.append("nknpvwkfbopfwowbfldfowb")
            self.hojas.append("aefbjiophzqgmifzrt")
            self.player.objetos.append("sopqzydhhjennqmn")
            self.player.objetos.append("fiuyhnmbvewqdghnbvgyu")
            self.hojas.append("sopqzydhhjennqmn")
            self.hojas.append("fiuyhnmbvewqdghnbvgyu")
            self.player.objetos.append("cpojgkwgmwotrbmzasdkplwn")
            self.hojas.append("cpojgkwgmwotrbmzasdkplwn")
            self.puerta.cambiarEstado(None,4)
#             PRUEBAS EVENTOS....
        ########################################
        #Captar eventos
        if (len(self.eventosActivos) != 0) and (not self.accion):
            for ev in self.eventosActivos:
#                 print self.player.rect.topleft
#                 print ev.posicion
                if pygame.sprite.collide_mask(self.player, ev):
                    ev.onEvent()
                    self.cambiarDia = False
                    self.numRes = 0
                    self.tiempoDial = 0
                    self.accionO = ev
                    self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
        #Esto de aqui no deberÃ­a funcionar asÃ­, si no que deberÃ­a cerrar el programa sin mÃ¡s, no llevarnos a la fase siguiente
        if event.type == pygame.QUIT or (self.keys[K_t] and self.keys[K_r]):
             escenaSig = FinalScene(self.director, self.player)
             self.director.cambiarEscena(escenaSig)
            
            
    def interact(self, tiempo, surface):
        if tiempo < TIEMPODIALOGO:
            self.text.render(surface,self.accionT, self.accionO.color, (self.accionO.rect.topleft[0], self.accionO.rect.topleft[1]), self.screen_rect[3])
        elif len(self.accionR) == 1 and tiempo < TIEMPODIALOGO*2:
            self.text.render(surface,self.accionR[0][0], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1]), self.screen_rect[3])
            self.numRes = self.accionR[0][1] 
        elif len(self.accionR) == 0:
            #Objetos recibidos
            if self.accionResult[0] != "None":
                if(self.accionResult[0]=="hoja1"):
                    self.player.cogerObjeto("esoasdlngrgudfpabsdiuasdpo")
                    self.player.cogerObjeto("emergycbjkqworghbfxgcpsefñjak")
                    self.hojas.append("esoasdlngrgudfpabsdiuasdpo")
                    self.hojas.append("emergycbjkqworghbfxgcpsefñjak")
                elif(self.accionResult[0]=="hoja2"):
                    self.player.cogerObjeto("nknpvwkfbopfwowbfldfowb")
                    self.player.cogerObjeto("aefbjiophzqgmifzrt")
                    self.hojas.append("nknpvwkfbopfwowbfldfowb")
                    self.hojas.append("aefbjiophzqgmifzrt")
                elif(self.accionResult[0]=="hoja3"):
                    self.player.cogerObjeto("sopqzydhhjennqmn")
                    self.player.cogerObjeto("fiuyhnmbvewqdghnbvgyu")
                    self.hojas.append("sopqzydhhjennqmn")
                    self.hojas.append("fiuyhnmbvewqdghnbvgyu")
                elif(self.accionResult[0]=="hoja4"):
                    self.player.cogerObjeto("cpojgkwgmwotrbmzasdkplwn")
                    self.hojas.append("cpojgkwgmwotrbmzasdkplwn")
                else:
                    self.player.cogerObjeto(self.accionResult[0])
                if(len(self.hojas)==7):
                    self.puerta.cambiarEstado(None,4)
            #Nuevo estado del objeto/npc
            elimEvento = self.accionO.cambiarEstado(None, int(self.accionResult[3]))
            if elimEvento:
                self.eventosActivos.remove(self.accionO)
            #Eventos generados
            if self.accionResult[2] != "None":
                if (self.accionResult[2] == "puzzle"):
#                     self.puzzle(self.level.draw(self.screen))
                    self.puzzleAct = True
                else:
                    for e in self.eventos:
                        if e.nombre==self.accionResult[2]:
                            self.eventosActivos.append(e)
                            self.eventos.remove(e)
            #Movimiento de algun personaje
            if self.accionResult[1] != "None":
                pass
            self.accion = False
        elif len(self.accionR) > 1 and self.optEl == 0:
            self.tiempoDial = TIEMPODIALOGO*2
            self.opcion = True
            j = len(self.accionR)
            for i in range(len(self.accionR)):
                self.text.render(surface,self.accionR[i][0], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - j*30), self.screen_rect[3])
                j -= 1
        else:
            self.cambiarDia = True            
    def empezarAccion(self, objeto, usar = None):
        #recuperar texto xml
        self.accion = True
        self.tiempoDial = 0
        self.primerDia = True
        texto,respuesta,resultado = objeto.continuar(0,None)
        return texto,respuesta,resultado
    
    def continuarAccion(self, objeto, respuesta):
        #recuperar texto xml
        texto,respuesta,resultado = objeto.continuar(respuesta)
        return texto,respuesta,resultado
    
    def puzzle2(self, surface):
        pygame.font.init()
        self.font = pygame.font.Font('../res/XFILES.ttf', 30)
        x = 743
        y = 268
        texto = ""
        for i in self.hojas:
            texto= texto+i+"%"
        print texto
        self.text.render(surface, texto, (0,0,0), (x,y), self.screen_rect[3])
        
    def comprobarPuzzle(self, pared):
        self.opcion = False
        self.puerta.cambiarEstado(None,4)
        for h in range(0,7):
            if h == 0:
                hojaAct = "nknpvwkfbopfwowbfldfowb"
            elif h== 1:
                hojaAct = "emergycbjkqworghbfxgcpsefñjak"
            elif h== 2:
                hojaAct = "sopqzydhhjennqmn"
            elif h== 3:
                hojaAct = "cpojgkwgmwotrbmzasdkplwn"
            elif h== 4:
                hojaAct = "aefbjiophzqgmifzrt"
            elif h== 5:
                hojaAct = "fiuyhnmbvewqdghnbvgyu"
            elif h== 6:
                hojaAct = "esoasdlngrgudfpabsdiuasdpo"
            else:
                hojaAct = "nknpvwkfbopfwowbfldfowb"
            if self.pared != [] and self.pared.pop(0)[0] == hojaAct[0]:
                pass
            else:
                self.hojas.append("esoasdlngrgudfpabsdiuasdpo")
                self.hojas.append("emergycbjkqworghbfxgcpsefñjak")
                self.hojas.append("nknpvwkfbopfwowbfldfowb")
                self.hojas.append("aefbjiophzqgmifzrt")
                self.hojas.append("sopqzydhhjennqmn")
                self.hojas.append("fiuyhnmbvewqdghnbvgyu")
                self.hojas.append("cpojgkwgmwotrbmzasdkplwn")
                self.pared = []
                return None
        self.eventosActivos.append(self.eventoFinalScene)
            
    
    def puzzle(self, surface):
        if self.optEl == 0:
            self.tiempoDial = TIEMPODIALOGO*2
            self.opcionPuz = True
            j = len(self.hojas) - 4
            self.text.render(surface,"Hojas", (0,0,0), (50, 20), self.screen_rect[3])
            for i in range(len(self.hojas)):
                self.text.render(surface,self.hojas[i], (0,0,0), (50, 200 - j*30), self.screen_rect[3])
                j -= 1
            j = len(self.pared) - 4
            self.text.render(surface,"Pared", (0,0,0), (750, 20), self.screen_rect[3])
            for i in range(len(self.pared)):
                self.text.render(surface,self.pared[i], (0,0,0), (750, 200 - j*30), self.screen_rect[3])
                j -= 1

    #Muestra el inventario hasta pulsar la tecla u o seleccionar un objeto
    def mostrarInv(self, surface):
        if self.optEl == 0:
            self.tiempoDial = TIEMPODIALOGO*2
            if not self.mostrar:
                self.opcion = True
            j = len(self.player.objetos) - 4
            self.text.render(surface,"Inventario:", (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - (j+1)*30), self.screen_rect[3])
            for i in range(len(self.player.objetos)):
                self.text.render(surface,self.player.objetos[i], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - j*30), self.screen_rect[3])
                j -= 1
    
    def finFase(self, final):
        if final == "FinalScene":
            escenaSig = FinalScene(self.director, self.player)
            self.director.cambiarEscena(escenaSig)
        else:
            self.director.cambiarEscena(final)
    
class Level(object):
    """
A class for our map. Maps in this implementation are one image; not
tile based. This makes collision detection simpler but can have performance
implications.
"""
    def __init__(self, map_image, viewport, player, mascara, playerCenter):
        """
Takes an image from which to make a mask, a viewport rect, and a
player instance.
"""
        self.image = map_image
#         self.image =pygame.image.load("../res/maps/primerinteriormask.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA, ALTO_PANTALLA))
        mascara = pygame.image.load(mascara).convert_alpha()        
        mascara = pygame.transform.scale(mascara, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.mask = pygame.mask.from_surface(mascara)
        self.rect = self.image.get_rect()
        self.player = player
#         self.player.rect.center = self.rect.center
        #posicion inicial
        self.player.rect.center = playerCenter
        self.viewport = viewport

    def update(self, keys):
        """
Updates the player and then adjust the viewport with respect to the
player's new position.
"""
        self.player.update(self.mask, keys)
        self.update_viewport()

    def update_viewport(self):
        """
The viewport will stay centered on the player unless the player
approaches the edge of the map.
"""
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rect)

    def draw(self, surface):
        """
Blit actors onto a copy of the map image; then blit the viewport
portion of that map onto the display surface.
"""
        #new_image = self.image.copy()
        #self.player.draw(new_image)
        #surface.fill((50,255,50))
        #surface.blit(new_image, (0,0), self.viewport)
        self.new_image = self.image.copy()
        return self.new_image

class Text:
    def __init__(self, FontName = '../res/XFILES.ttf', FontSize = 20):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize
 
    def render(self, surface, text, color, pos, ancho):
#         text = unicode(text, "UTF-8")
        x, y = pos
        numLin = len(text.split("%"))
        for i in text.split("%"):
            if((x-self.font.size(i)[0]/2)<0):
                posx = 0
            elif((x+self.font.size(i)[0]/2)>ancho):
                posx = x - self.font.size(i)[0]
            else:
                posx =x-self.font.size(i)[0]/2
            
            if(( y - numLin*self.font.size(i)[1])<0):
                posy = 0
                y= numLin*self.font.size(i)[1]
            else:
                posy = y- numLin*self.font.size(i)[1]
                
            surface.blit(self.font.render(i, 1, color, (255,255,255)), (posx, posy))
            y += self.size   
