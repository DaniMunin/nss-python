# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from item import *
from personajes import *
from pygame.locals import *
from cellarScene import *
from evento import *
# from testItem import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

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
TIEMPODIALOGO = 1000

class FaseInvestigacion(EscenaPygame):
    def __init__(self, director, jugador1):
        # Primero invocamos al constructor de la clase padre
        EscenaPygame.__init__(self, director)

        
        pygame.display.set_caption("Fase")
        pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        """Initialize things; create a Player; create a Level."""
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
#         self.clock = pygame.time.Clock()
#         self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.player = jugador1
        self.grupoJugador = pygame.sprite.Group( self.player)
        fondo = pygame.image.load("../res/maps/mapa2.png")
        #cambiar el rect.copy para poner posicion inicial
        posInicialMapa = self.screen_rect.copy()
        posInicialMapa.topleft = (posInicialMapa.topleft[0]-100,posInicialMapa.topleft[1]+100)
        self.level = Level(fondo, posInicialMapa, self.player)
        self.grupoJugadores = pygame.sprite.Group(jugador1)
        
        self.secretoSon = pygame.mixer.Sound("../res/Sounds/secret.wav")
        
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
        
        self.bolio = NoJugador("../res/Sprites/bolio2.png","../res/BolioCoordJugador.txt", (244,2000), 1, "dialogoBolio.xml", (184,134,11))
        self.espeonza = NoJugador("../res/Sprites/esperanza2.png","../res/EspeonzaCoordJugador.txt", (223,1748), 1, "dialogoEspeonza.xml", (199,21,133))
        self.charles = NoJugador("../res/Sprites/charles.png","../res/CharlesCoordJugador.txt", (190,1514), 1.5, "dialogoCharles.xml", (200,20,20))
        self.cervero = NoJugador("../res/Sprites/scien2.png","../res/ScienceCoordJugador.txt", (993,1984), 1, "dialogoCervero.xml", (50,205,50))
        self.rateos = NoJugador("../res/Sprites/rateos2.png","../res/RateosCoordJugador.txt", (831,1504), 1, "dialogoRateos.xml", (100,100,100))
        self.poli = NoJugador("../res/Sprites/poli.png","../res/PoliCoordJugador.txt", (586,1400), 1.5, "dialogoPoli.xml", (0,0,255))
        self.poliEstorbo1 = NoJugador("../res/Sprites/poli_rudeQE.png", "../res/PoliEstorboCoordJugador.txt", (1695, 1670), 1.5, "dialogoPoliEstorbo.xml", (0,0,0))
        self.poliEstorbo3 = NoJugador("../res/Sprites/poli_rudeQ.png", "../res/PoliEstorboCoordJugador.txt", (2460, 1240), 1.5, "dialogoPoliEstorbo.xml", (0,0,0))
        self.poliEstorbo2 = NoJugador("../res/Sprites/poli_rudeQL.png", "../res/PoliEstorboCoordJugador.txt", (2039, 1560), 1.5, "dialogoPoliEstorbo.xml", (0,0,0))

        self.grupoNPC = pygame.sprite.Group( self.poli, self.rateos, self.cervero, self.charles, self.espeonza, self.bolio, self.poliEstorbo1, self.poliEstorbo2, self.poliEstorbo3 )
        self.grupoNPCDetras = pygame.sprite.Group( self.poli, self.charles, self.espeonza, self.cervero, self.poliEstorbo2, self.poliEstorbo3)
        self.grupoNPCDelante = pygame.sprite.Group( self.rateos, self.bolio, self.poliEstorbo1 )

        self.chim1 = ItemInvisible(10, "pokeball.xml", (756,1446))
        self.armarioBarIzda = ItemInvisible(10, "armarioBarIzda.xml", (2607, 799))
        self.mesaCircBar = ItemInvisible(10, "mesaCircBar.xml", (2940, 1117))
        self.chimCuadro = ItemInvisible(10, "chimCuadro.xml", (3051, 1505))
        self.relojCuadro = ItemInvisible(10, "relojCuadro.xml", (2792, 1505))
        self.Cuadro = ItemInvisible(10, "Cuadro.xml", (2925, 1505))
        self.armarioHabIzda = ItemInvisible(10, "ArmarioHabIzda.xml", (1247, 673))
        self.relojEntrada = ItemInvisible(10, "relojEntrada.xml", (1788, 2173))
        self.llave = ItemVisible(10, "llave.xml", "../res/Sprites/key.png", (1712, 2283))
        self.armarioHabDcha = ItemInvisible(10, "armarioHabDcha.xml", (1303, 673))
        self.CamaHab = ItemInvisible(10, "camaHab.xml", (1142, 739))
        self.bibDchaComedor = ItemInvisible(10, "bibDchaComedor.xml", (2715, 177))
        self.sillaComedor = ItemInvisible(10, "sillaComedor.xml", (2306, 332))
        self.relojEntradaArriba = ItemInvisible(10, "relojEntradaArriba.xml", (1863, 1342))
        self.mesaNormBar = ItemInvisible(10, "mesaNormBar.xml", (2707, 1006))
        self.fanuel = ItemVisible(11, "fanuel.xml", "../res/Sprites/fanuel.png", (426,1540))
        self.grupoObj = pygame.sprite.Group(self.chim1, self.Cuadro, self.mesaNormBar, self.relojEntradaArriba, self.fanuel)
        
        self.level.mask.draw(self.poli.mask, (self.poli.rect.center[0]-16, self.poli.rect.center[1]-30))
        self.level.mask.draw(self.espeonza.mask, (self.espeonza.rect.center[0]-20, self.espeonza.rect.center[1]-30))
        self.level.mask.draw(self.charles.mask, (self.charles.rect.center[0]-20, self.charles.rect.center[1]-30))
        self.level.mask.draw(self.cervero.mask, (self.cervero.rect.center[0]-20, self.cervero.rect.center[1]-30))
        self.level.mask.draw(self.rateos.mask, (self.rateos.rect.center[0]-16, self.rateos.rect.center[1]-30))
        self.level.mask.draw(self.bolio.mask, (self.bolio.rect.center[0]-20, self.bolio.rect.center[1]-30))
#         self.level.mask.draw(self.poliEstorbo1.mask, (self.poliEstorbo1.rect.center[0]-20, self.poliEstorbo1.rect.center[1]-30))
#         self.level.mask.draw(self.poliEstorbo2.mask, (self.poliEstorbo2.rect.center[0]-20, self.poliEstorbo2.rect.center[1]-30))
#         self.level.mask.draw(self.poliEstorbo3.mask, (self.poliEstorbo3.rect.center[0]-20, self.poliEstorbo3.rect.center[1]-30))
        self.level.mask.draw(self.fanuel.mask, (self.fanuel.rect.center[0]-35, self.fanuel.rect.center[1]-35))
        
        self.evPrueba = EventoAparicion((586,1600),"evPrueba", "dialogoEventoPrueba.xml", self.espeonza, self.grupoNPCDetras,self.level.mask)
        
        self.culpables = []
        self.eventos = []
        self.eventosActivos = []
        self.eventos.append(self.evPrueba)
#         self.eventosActivos.append(evPrueba)
        self.eventoEstorbo1Des = EventoDesaparicion((545,1610),"estorbo1Des", "estorboDes.xml", self.poliEstorbo1, self.grupoNPCDelante,self.level.mask)
        self.eventoEstorbo2Des = EventoDesaparicion((545,1610),"estorbo2Des", "estorboDes.xml", self.poliEstorbo2, self.grupoNPCDetras,self.level.mask)
        self.eventoEstorbo3Des = EventoDesaparicion((545,1610),"estorbo3Des", "estorboDes.xml", self.poliEstorbo3, self.grupoNPCDetras,self.level.mask)
        
        #Eventos para descubrir a Bolio
        self.eventoDormitorioAct = EventoActivaItems((100,1314),"DormitorioAct", list([self.armarioHabDcha, self.CamaHab]), self.grupoObj, self.secretoSon)
        self.eventoCulpableBolio = EventoCulpable((100,1314),"CulpableBolio", "Bolio", self.culpables,self.poli,self.eventosActivos, self.eventoEstorbo1Des, self.secretoSon, self.player.objetos, "Linterna")
        
        self.eventos.append(self.eventoDormitorioAct)
        self.eventos.append(self.eventoCulpableBolio)
        ####################################
        
        #Eventos para descubrir a Rateos
        self.eventoComedorAct = EventoActivaItems((100,1314),"ComedorAct", list([self.bibDchaComedor, self.sillaComedor]), self.grupoObj, self.secretoSon)
        self.eventoPeriodicoCom = EventoCambioEstado((2197, 149),"PeriodicoCom", self.bibDchaComedor, 1, "evDesc.xml", self.secretoSon)
        self.eventoCulpableChema = EventoCulpable((100,1314),"CulpableChema", "Chema", self.culpables,self.poli,self.eventosActivos, self.eventoEstorbo1Des, self.secretoSon, self.player.objetos, None)
        
        self.eventos.append(self.eventoComedorAct)
        self.eventos.append(self.eventoPeriodicoCom)
        self.eventos.append(self.eventoCulpableChema)
        ####################################

        
        #Eventos para descubrir a Espeonza
        self.eventoRelojEntrada = EventoActivaItems((100,1314), "RelojEntrada", list([self.relojEntrada, self.armarioHabIzda]) , self.grupoObj, self.secretoSon)
        self.eventoLlaveEntrada = EventoAparicion((1553, 2020), "LlaveEntrada", "evVacio2.xml", self.llave, self.grupoObj, self.level.mask)
        self.eventoDesLlaveEntrada = EventoDesaparicion((1679, 2216), "desaparecerLlave", "evVacio.xml", self.llave, self.grupoObj, self.level.mask)
        self.eventoCulpableEspeonza = EventoCulpable((100,1314),"CulpableEspeonza", "Espeonza", self.culpables,self.poli,self.eventosActivos, self.eventoEstorbo2Des, self.secretoSon, self.player.objetos, "LlaveArmario")
        
        self.eventos.append(self.eventoRelojEntrada)
        self.eventos.append(self.eventoLlaveEntrada)
        self.eventos.append(self.eventoDesLlaveEntrada)
        self.eventos.append(self.eventoCulpableEspeonza)
        
        #Eventos para descubrir a Cervero
        self.eventoHabCuadro = EventoActivaItems((100,1314),"HabCuadro", list([self.relojCuadro, self.chimCuadro]), self.grupoObj, self.secretoSon)
        self.eventoAbreCuadro = EventoCambioEstado((2947, 1448),"abreCuadro", self.Cuadro, 1, "evAbrir.xml", self.secretoSon)
        self.eventoCulpableCervero = EventoCulpable((100,1314),"CulpableCervero", "Cervero", self.culpables,self.poli,self.eventosActivos, self.eventoEstorbo3Des, self.secretoSon, self.player.objetos, "BarraMetal")
        
        self.eventos.append(self.eventoHabCuadro)
        self.eventos.append(self.eventoAbreCuadro)
        self.eventos.append(self.eventoCulpableCervero)
        ####################################
        
        #Eventos para descubrir a Charles
        self.eventoBar = EventoActivaItems((100,1314),"Bar", list([self.armarioBarIzda, self.mesaCircBar]), self.grupoObj, self.secretoSon)
        self.fantasma = NoJugador("../res/Sprites/poli_rudeQ.png","../res/PoliEstorboCoordJugador.txt", (2713,892), 1.5, "dialogoPoliEstorbo.xml", (0,0,255))
        self.eventoFantasmaAp = EventoAparicion((2706,774),"fantasmaAp", "fantasmaAp.xml", self.fantasma, self.grupoNPCDelante,self.level.mask)
        self.eventoBadassDes = EventoDesaparicion((2706,774),"badassDes", "badassDes.xml", self.player, self.grupoJugador,self.level.mask)
        self.eventoBadassAp = EventoAparicion((2706,774),"badassAp", "badassAp.xml", self.player, self.grupoJugador,self.level.mask, False)
        self.eventoFantasmaDes = EventoDesaparicion((2706,774),"fantasmaDes", "fantasmaDes.xml", self.fantasma, self.grupoNPCDelante,self.level.mask)
        self.eventoCulpableCharles = EventoCulpable((100,1314),"CulpableCharles", "Charles", self.culpables,self.poli,self.eventosActivos, None, self.secretoSon, self.player.objetos, "LlaveBar")
        
        self.eventos.append(self.eventoBar)
        self.eventos.append(self.eventoFantasmaAp)
        self.eventos.append(self.eventoFantasmaDes)
        self.eventos.append(self.eventoBadassDes)
        self.eventos.append(self.eventoBadassAp)
        self.eventos.append(self.eventoCulpableCharles)
        ####################################
        
        #Eventos de finales diferentes
        self.eventoMuerteCafe = EventoFinal((2597, 864), "MuerteCafe", self)
        self.eventoFinalBolio = EventoFinal((100,1314), "FinalBolio", self)
        self.eventoFinalChema = EventoFinal((100,1314), "FinalChema", self)
        self.eventoFinalEspeonza = EventoFinal((100,1314), "FinalEspeonza", self)
        self.eventoFinalCervero = EventoFinal((100,1314), "FinalCervero", self)
        self.eventoFinalCharles = EventoFinal((100,1314), "FinalCharles", self)
        self.eventoFinalTodos = EventoFinal((100,1314), "FinalTodos", self)
        
        self.eventos.append(self.eventoMuerteCafe)
        self.eventos.append(self.eventoFinalBolio)
        self.eventos.append(self.eventoFinalChema)
        self.eventos.append(self.eventoFinalEspeonza)
        self.eventos.append(self.eventoFinalCervero)
        self.eventos.append(self.eventoFinalCharles)
        self.eventos.append(self.eventoFinalTodos)
        ####################################
        
        
                
    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se actualizan los jugadores con los movimientos a realizar
    #  Se actualiza la posicion del sol y el color del cielo
    #  Se mueven los enemigos como sea conveniente
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se actualiza el scroll del decorado y los objetos en el
    def update(self, tiempo):
#         self.screen.fill(pygame.Color("black"))
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
#         elif (self.eventoAct):
#             self.accionT, self.accionR, self.accionResult = self.continuarAccion(self.accionO, self.numRes) 
        else:   
            self.level.update(self.keys)
            print self.player.rect
#         print self.rateos.rect
#         print self.player.rect
#         print self.poli.rect
#         print self.espeonza.rect
#         print self.cervero.rect
        
#         else:
#             self.level.draw(self.screen, texto)
    
    def dibujar(self):        
        s = self.level.draw(self.screen)
        self.grupoNPCDetras.draw(s)
        self.grupoObj.draw(s)
#         s.blit(self.poli.image, self.poli.posicion)
#         s.blit(self.espeonza.image, self.espeonza.posicion)
#         s.blit(self.charles.image, self.charles.posicion)
        self.grupoJugador.draw(s)
        self.grupoNPCDelante.draw(s)
#         s.blit(self.bolio.image, self.bolio.posicion)
#         s.blit(self.cervero.image, self.cervero.posicion)
#         s.blit(self.rateos.image, self.rateos.posicion)
        
        if self.accion:
            self.interact(self.tiempoDial, s)
            
        if self.inventario:
            self.mostrarInv(s)
            
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
        #Interactuar con npc/objeto sin utilizar nada
        if self.keys[K_SPACE] and (not self.accion) and (not self.inventario):
            if (pygame.sprite.spritecollideany(self.player, self.grupoNPCDetras) != None) or (pygame.sprite.spritecollideany(self.player, self.grupoNPCDelante) != None):
                self.cambiarDia = False
                self.numRes = 0
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoNPC)
                self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
            if (pygame.sprite.spritecollideany(self.player, self.grupoObj) != None):
                self.cambiarDia = False
                self.numRes = 0
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoObj)
                self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
        #Abrir el inventario
        if (self.keys[K_i]) and (not self.accion) and (not self.inventario):
            #Interactuar con npc/objeto utilizando un objeto
            if (pygame.sprite.spritecollideany(self.player, self.grupoObj) != None):
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoObj)
                self.mostrar = False
            elif (pygame.sprite.spritecollideany(self.player, self.grupoNPCDetras) != None) or (pygame.sprite.spritecollideany(self.player, self.grupoNPCDelante) != None):
                self.accionO = pygame.sprite.spritecollideany(self.player, self.grupoNPC)
                self.mostrar = False
            else: 
                self.mostrar = True
            self.inventario = True
        #Cerrar el inventario en caso de estar solo mostrandolo
        if self.inventario and self.mostrar:
            if self.keys[K_u]:
                self.optEl = 1
            
        if self.keys[K_q] and self.accion:
            self.tiempoDial = TIEMPODIALOGO
#             PRUEBAS EVENTOS....
        if self.keys[K_d]:
            evPrueba = EventoDesaparicion((586,1700), "", None, self.espeonza, self.grupoNPCDetras,self.level.mask)
            evPrueba.onEvent()
        if self.keys[K_a]:
            evPrueba = EventoAparicion((586,1600), "", "dialogoEventoPrueba.xml", self.espeonza, self.grupoNPCDetras,self.level.mask)
            evPrueba.onEvent()
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
                    self.accionO.rect = self.player.rect
                    self.accionT, self.accionR, self.accionResult = self.empezarAccion(self.accionO)
        if (self.keys[K_r] and self.keys[K_e]):
            self.player.cogerObjeto("Tarjeta de credito")
            self.player.cogerObjeto("Saco de Cafe")
            self.player.cogerObjeto("Periodico financiero")
            self.player.cogerObjeto("Ropa")
            self.player.cogerObjeto("Libro satanico")
        if (self.keys[K_p] and self.keys[K_f]):
             #print "Hola"
            escenaSig = EscenaAnimacionFinalMalo(self.director, "../res/Dialogos/animacionFinalMaloCafe.xml")
            self.director.cambiarEscena(escenaSig)
        #Esto de aqui no deberÃ­a funcionar asÃ­, si no que deberÃ­a cerrar el programa sin mÃ¡s, no llevarnos a la fase siguiente
        if event.type == pygame.QUIT or (self.keys[K_t] and self.keys[K_r]):
             #print "Hola"
             escenaSig = CellarScene(self.director, self.player)
             self.director.cambiarEscena(escenaSig)
            
    def interact(self, tiempo, surface):
        if tiempo < TIEMPODIALOGO:
            self.text.render(surface,self.accionT, self.accionO.color, (self.accionO.rect.topleft[0], self.accionO.rect.topleft[1]))
        elif len(self.accionR) == 1 and tiempo < TIEMPODIALOGO*2:
            self.text.render(surface,self.accionR[0][0], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1]))
            self.numRes = self.accionR[0][1] 
        elif len(self.accionR) == 0:
            #Objetos recibidos
            if self.accionResult[0] != "None":
                self.player.objetos.append(self.accionResult[0])
            #Nuevo estado del objeto/npc
            elimEvento = self.accionO.cambiarEstado(None, int(self.accionResult[3]))
            if elimEvento:
                self.eventosActivos.remove(self.accionO)
            #Eventos generados
            if self.accionResult[2] != "None":
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
                self.text.render(surface,self.accionR[i][0], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - j*30))
                j -= 1
        else:
            self.cambiarDia = True
    
    #Muestra el inventario hasta pulsar la tecla u o seleccionar un objeto
    def mostrarInv(self, surface):
        if self.optEl == 0:
            self.tiempoDial = TIEMPODIALOGO*2
            if not self.mostrar:
                self.opcion = True
            j = len(self.player.objetos) - 4
            self.text.render(surface,"Inventario:", (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - (j+1)*30))
            for i in range(len(self.player.objetos)):
                self.text.render(surface,self.player.objetos[i], (0,0,0), (self.player.rect.topleft[0], self.player.rect.topleft[1] - j*30))
                j -= 1
            
    def empezarAccion(self, objeto, usar = None):
        #recuperar texto xml
        self.accion = True
        self.tiempoDial = 0
        self.primerDia = True
        texto,respuesta,resultado = objeto.continuar(0,usar)
        return texto,respuesta,resultado
    
    def continuarAccion(self, objeto, respuesta):
        #recuperar texto xml
        texto,respuesta,resultado = objeto.continuar(respuesta)
        return texto,respuesta,resultado
    
    def finFase(self, final):
        self.director.cambiarEscena(final)
    
    
class Level(object):
    """
A class for our map. Maps in this implementation are one image; not
tile based. This makes collision detection simpler but can have performance
implications.
"""
    def __init__(self, map_image, viewport, player):
        """
Takes an image from which to make a mask, a viewport rect, and a
player instance.
"""
        self.image = map_image
#         self.image =pygame.image.load("../res/maps/primerinteriormask.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA*4, ALTO_PANTALLA*4))
        mascara = pygame.image.load("../res/maps/mascaramapa.png").convert_alpha()        
        mascara = pygame.transform.scale(mascara, (ANCHO_PANTALLA*4, ALTO_PANTALLA*4))
        self.mask = pygame.mask.from_surface(mascara)
        self.rect = self.image.get_rect()
        self.player = player
#         self.player.rect.center = self.rect.center
        #posicion inicial
        self.player.rect.center = (630,1480)
        self.viewport = viewport
        

    def update(self, keys):
        """
Updates the player and then adjust the viewport with respect to the
player's new position.
"""
        self.player.update(self.mask, keys)
        self.update_viewport()
#         print self.player.rect
#         print self.poli.rect
        
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
        self.new_image = self.image.copy()
        return self.new_image
    
    
class Text:
    def __init__(self, FontName = '../res/XFILES.ttf', FontSize = 20):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize
 
    def render(self, surface, text, color, pos):
#         text = unicode(text, "UTF-8")
        x, y = pos
        numLin = len(text.split("%"))
        for i in text.split("%"):
            surface.blit(self.font.render(i, 1, color, (255,255,255)), (x - self.font.size(i)[0]/2, y - numLin*self.font.size(i)[1]))
            y += self.size 