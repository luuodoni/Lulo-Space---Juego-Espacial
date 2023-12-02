import pygame
import random
import math
from pygame import mixer

# import io

# Iniciamos pygame.
pygame.init()

# Tamaño de pantalla.
pantalla = pygame.display.set_mode((800, 600))

# Funcion para ser ejecutable, la fuente.
'''def fuente_bytes(fuente):
    with open(fuente, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)'''

# Titulo e icono juego.
pygame.display.set_caption('LuloSpaceX')
icono = pygame.image.load('ovni icono.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.png')

# Jugador variables.
nave_img = pygame.image.load('astronave.png')
nave_x = 368
nave_y = 536
nave_movi_x = 0
nave_movi_y = 0

# Musica y efectos del juego.
mixer.music.load('musica fondo.mp3')
mixer.music.play(-1)

# Enemigo variables.
enemigo_img = []
enemigo_x = []
enemigo_y = []
enemigo_movi_x = []
enemigo_movi_y = []
cantidad_enemigos = 10

for e in range(cantidad_enemigos):
    enemigo_img.append(pygame.image.load('extraterrestre.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_movi_x.append(1)
    enemigo_movi_y.append(50)

# Jugador bala.
balas = []
bala_img = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_movi_x = 0
bala_movi_y = 3
bala_visible = False

# Puntaje.
puntaje = 0
# fuente_como_bytes = fuente_bytes('FreeSansBold.ttf')
fuente_puntaje = pygame.font.Font('FreeSansBold.ttf', 32)
puntaje_x = 10
puntaje_y = 10


# Mostrar puntaje.
def mostrar_puntaje(x, y):
    texto = fuente_puntaje.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Movimiento del jugador.
def jugador(x, y):
    pantalla.blit(nave_img, (x, y))


# Movimiento del jugador.
def enemigo(x, y, ene):
    pantalla.blit(enemigo_img[ene], (x, y))


# Movimiento de bala.
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(bala_img, (x + 16, y + 10))


# Detectar colisiones.
def colisiones(x1, x2, y1, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distancia < 27:
        return True
    else:
        return False


# Texto final del juego.
fuente_final = pygame.font.Font('FreeSansBold.ttf', 60)


def texto_final():
    mi_fuente_final = fuente_final.render('GAME OVER WACHIN', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (100, 200))


cerrar = True
# Loop del juego.
while cerrar:

    # Imagen fondo.
    pantalla.blit(fondo, (0, 0))

    # Evento en el juego.
    for evento in pygame.event.get():

        # Boton de cerrar juego.
        if evento.type == pygame.QUIT:
            cerrar = False

        # Boton de teclas.
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                nave_movi_x = -0.5
            if evento.key == pygame.K_RIGHT:
                nave_movi_x = 0.5
            if evento.key == pygame.K_x:
                sonido_bala = mixer.Sound('disparo musica.mp3')
                sonido_bala.play()
                nueva_bala = {
                    "x": nave_x,
                    "y": nave_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)

        # Soltar botones
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                nave_movi_x = 0

    # Modificar ubicacion jugador:
    nave_x += nave_movi_x

    # Mantener dentro de bordes a nave.
    if nave_x <= 0:
        nave_x = 0
    elif nave_x >= 736:
        nave_x = 736

    jugador(nave_x, nave_y)

    # Modificar ubicacion enemigo:
    for e in range(cantidad_enemigos):

        # Fin del juego.
        if enemigo_y[e] > 600:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_movi_x[e]

        # Colision.
        for bala in balas:
            colision_bala_enemigo = colisiones(enemigo_x[e], bala["x"], enemigo_y[e], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("explosion.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

        # Mantener dentro de bordes a enemigo.
        if enemigo_x[e] <= 0:
            enemigo_movi_x[e] = 0.2
            enemigo_y[e] += enemigo_movi_y[e]
        elif enemigo_x[e] >= 736:
            enemigo_movi_x[e] = -0.2
            enemigo_y[e] += enemigo_movi_y[e]

        # Mostrar puntaje.
        mostrar_puntaje(puntaje_x, puntaje_y)

    # Movimiento bala.
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(bala_img, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(bala_img, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    # Actualiza pantalla.
    pygame.display.update()
