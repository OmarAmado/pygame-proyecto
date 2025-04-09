import pygame, sys
from pygame.locals import *
import random

pygame.init()
reloj=pygame.time.Clock()
WIDTH, HEIGHT = 640, 480
pantalla=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Serpiente')
font_path=pygame.font.match_font('Arial')
fuente=pygame.font.Font(font_path,32)

def cargar_imagenes():
    pared=pygame.image.load('pared.png')
    fruta=pygame.image.load('fruta.png')
    serpiente=pygame.image.load('serpiente.png')
    return {'pared':pared,'fruta':fruta,
           'serpiente':serpiente}

def cargar_mapa(ruta):
    archivo=open(ruta,'r')
    contenido=archivo.readlines()
    archivo.close()
    return contenido

class DatosJuego:
    def __init__(self):
        self.vidas=3
        self.estas_muerto=False
        self.bloques=[]
        self.tick=300
        self.velocidad=250
        self.frame=0
        self.nivel=1
        self.cuenta_frutas=0
        self.segmentos=1        
        fx=random.randint(1,38)
        fy=random.randint(1,28)
        self.fruta=Posicion(fx,fy)
        self.bloques.append(Posicion(20,15))
        self.bloques.append(Posicion(19,15))
        self.direccion=0
    
class Posicion:
    def __init__(self,x,y):
        self.x=x
        self.y=y

def dibujar_texto_juego_terminado(pantalla):
    texto1=fuente.render('Juego Terminado',
                        True,
                        (255,255,255))
    texto2=fuente.render('Espacio para jugar o cierra la ventana',
                        True,
                        (255,255,255))
    cx=pantalla.get_width()/2
    cy=pantalla.get_height()/2
    texto1_area=texto1.get_rect(centerx=cx,
                                top=cy-48)
    texto2_area=texto2.get_rect(centerx=cx,
                                top=cy)
    pantalla.blit(texto1,texto1_area)
    pantalla.blit(texto2,texto2_area)
    
def dibujar_paredes(pantalla,imagen,mapa):
    fila=0
    for linea in mapa:
        col=0
        for letra in linea:
            if letra=='1':
                imagen_area=imagen.get_rect()
                imagen_area.top=fila*16
                imagen_area.left=col*16
                pantalla.blit(imagen,imagen_area)
            col+=1
        fila+=1

def dibujar_datos(pantalla,datos):
    texto=f'Vidas = {datos.vidas}, Nivel = {datos.nivel}'
    texto=fuente.render(texto,True,(255,255,255))
    texto_area=texto.get_rect(centerx=pantalla.get_width()/2,
                             top=32)
    pantalla.blit(texto,texto_area)
    
def dibujar_serpiente(pantalla,imagen,datos):
    inicio=True
    for bloque in datos.bloques:
        dest=(bloque.x*16,bloque.y*16,16,16)
        if inicio:
            inicio=False
            fuente=(((datos.direccion*2)+
                     (datos.frame))*16,
                    0,16,16)
        else:
            fuente=(8*16,0,16,16)
        pantalla.blit(imagen,dest,fuente)

def actualizar_juego(datos,tiempo):
    datos.tick-=tiempo
    cabeza=datos.bloques[0]
    if datos.tick<0:
        datos.tick+=datos.velocidad
        datos.frame+=1
        datos.frame%=2
        if datos.direccion==0:
            mov=(1,0)
        elif datos.direccion==1:
            mov=(-1,0)
        elif datos.direccion==2:
            mov=(0,-1)
        else:
            mov=(0,1)
        nueva_pos=Posicion(cabeza.x+mov[0],
                          cabeza.y+mov[1])
        for bloque in datos.bloques:
            temp=Posicion(bloque.x,bloque.y)
            bloque.x=nueva_pos.x
            bloque.y=nueva_pos.y
            nueva_pos=Posicion(temp.x,temp.y)
    
    teclas=pygame.key.get_pressed()
    if teclas[K_RIGHT] and datos.direccion!=1:
        datos.direccion=0
    elif teclas[K_LEFT] and datos.direccion!=0:
        datos.direccion=1
    elif teclas[K_UP] and datos.direccion!=3:
        datos.direccion=2
    elif teclas[K_DOWN] and datos.direccion!=2:
        datos.direccion=3
    
    if (cabeza.x==datos.fruta.x and cabeza.y==datos.fruta.y):
        ultimo_indice=len(datos.bloques)-1
        for i in range(datos.segmentos):
            nueva_cola=Posicion(
            datos.bloques[ultimo_indice].x,
            datos.bloques[ultimo_indice].y)
            datos.bloques.append(nueva_cola)
        fx=random.randint(1,38)
        fy=random.randint(1,28)
        datos.fruta=Posicion(fx,fy)
        datos.cuenta_frutas+=1
        if datos.cuenta_frutas==3:
            datos.cuenta_frutas=0
            datos.velocidad-=25
            datos.nivel+=1
            datos.segmentos*=2
            if datos.segmentos>64:
                datos.segmentos=64
            if datos.velocidad<100:
                datos.velocidad=100

def cabeza_golpea_pared(mapa,datos):
    fila=0
    for linea in mapa:
        col=0
        for letra in linea:
            if letra=='1':
                if datos.bloques[0].x==col and \
                   datos.bloques[0].y==fila:
                    return True
            col+=1
        fila+=1
    return False

def cabeza_golpea_cuerpo(datos):
    cabeza=datos.bloques[0]
    for i in range(1,len(datos.bloques)):
        bloque=datos.bloques[i]
        if cabeza.x==bloque.x and cabeza.y==bloque.y:
            return True
    return False
          
def perder_vida(datos):
    datos.vidas-=1
    datos.bloques[:]=[]
    datos.direccion=0
    datos.bloques.append(Posicion(20,15))
    datos.bloques.append(Posicion(19,15))
    
def posicion_fruta(datos):
    fx=random.randint(1,38)
    fy=random.randint(1,28)
    colision=True
    while colision:
        colision=False
        for bloque in datos.bloques:
            if bloque.x==fx and bloque.y==fy:
                fx=random.randint(1,38)
                fy=random.randint(1,28)
                colision=True
                continue
    datos.fruta=Posicion(fx,fy)
    
imagenes=cargar_imagenes()
imagenes['fruta'].set_colorkey((255,0,255))
mapa=cargar_mapa('mapa.txt')
datos=DatosJuego()
quitar_juego=False
estas_jugando=False
while not quitar_juego:
    if estas_jugando:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
        fruta_area=imagenes['fruta'].get_rect()
        fruta_area.top=datos.fruta.y*16
        fruta_area.left=datos.fruta.x*16
        
        actualizar_juego(datos,reloj.get_time())
        
        colision=cabeza_golpea_pared(mapa,datos) \
            or cabeza_golpea_cuerpo(datos)
        
        if colision:
            perder_vida(datos)
            posicion_fruta(datos)
        
        estas_jugando=datos.vidas>0
        if estas_jugando:
            pantalla.fill((0,0,0))
            pantalla.blit(imagenes['fruta'],
                         fruta_area)
            dibujar_paredes(pantalla,
                           imagenes['pared'],
                           mapa)
            dibujar_datos(pantalla,datos)
            dibujar_serpiente(pantalla,
                             imagenes['serpiente'],
                             datos)
    else:
        teclas=pygame.key.get_pressed()
        #python --version
        #ls
        #clear
        #dir
        #history
        #cd ..
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        
        if teclas[K_SPACE]:
            estas_jugando=True
            datos=None
            datos=DatosJuego()
        
        dibujar_texto_juego_terminado(pantalla)
        
    pygame.display.update()
    reloj.tick(30)