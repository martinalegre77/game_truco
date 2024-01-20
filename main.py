import os
import time
from class_truco import Jugador, Mazo
import pygame

# Const
GAME_DELTA_TIME = 1 # tiempo de espera en seg entre momentos
SCREEN_RESOLUTION = (1000, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Init
pygame.init()
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')

mazo = Mazo()

jugador1 = Jugador('Pipi')
jugador2 = Jugador('Martin')

# Titulo de la ventana
pygame.display.set_caption('TRUCO')

def draw_text(surf, msg, size, color, x_text, y_text):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(
        msg, 
        True, 
        color
    )
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x_text, y_text)
    surf.blit(text_surface, text_rect)

def end_game():
    pygame.quit()
    quit()

def draw_ganador(msg, carta_jug1, carta_jug2):
    # limpiar pantalla
    screen.fill(BLACK)
    draw_text(
            screen,
            msg,
            25,
            WHITE,
            SCREEN_RESOLUTION[0] / 2,
            SCREEN_RESOLUTION[1] / 2 + 100
            )
    img_carta = pygame.image.load(carta_jug1.imagen)
    x_carta = SCREEN_RESOLUTION[0] / 2 - 200
    y_carta = SCREEN_RESOLUTION[1] / 2 - 50
    screen.blit(img_carta, (x_carta, y_carta))

    img_carta = pygame.image.load(carta_jug2.imagen)
    x_carta = SCREEN_RESOLUTION[0] / 2 + 100
    y_carta = SCREEN_RESOLUTION[1] / 2 - 50
    screen.blit(img_carta, (x_carta, y_carta))

    pygame.display.update()

def cantar_truco(jugador, other, truco=0):
    cantando = True 

    cantos = ['Truco', 'Retruco', 'Vale 4']

    if truco > 0:
        menu = ['Aceptar']
        menu.append(cantos[truco])
        menu.append('Rechazar')
    else:
        menu = [cantos[truco]]
        menu.append('Salir')

    opt = 0

    while cantando:
        # limpiar pantalla
        screen.fill(BLACK)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                end_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    end_game()

                if event.key == pygame.K_RIGHT:
                    opt += 1
                    if opt > len(menu) - 1:
                        opt = 0

                if event.key == pygame.K_LEFT:
                    opt -= 1
                    if opt < 0:
                        opt = len(menu) - 1

                if event.key == pygame.K_SPACE:
                    if opt == 0 and truco > 0:
                        truco += 1
                        jugador.modificador_truco = truco
                        other.modificador_truco = truco
                        cantando = False
                    elif opt == len(menu) - 1:
                        if truco > 0:
                            other.modificador_truco = truco
                            cantando = False
                            raise Exception('Not implemented')
                        else:
                            cantando = False
                    else:
                        draw_text(
                            screen,
                            f'{jugador.nombre} canta {menu[opt]}',
                            25,
                            WHITE,
                            SCREEN_RESOLUTION[0] / 2,
                            10
                            )
                        cantar_truco(other, jugador, truco+1)
                        cantando = False

        for i, palabra in enumerate(menu):
            x_palabra = SCREEN_RESOLUTION[0] / 2 - 20 + i * 40
            if opt == i:
                y_palabra = SCREEN_RESOLUTION[1] - 75
            else:
                y_palabra = SCREEN_RESOLUTION[1] - 25
            draw_text(
                        screen,
                        f'{palabra}',
                        25,
                        WHITE,
                        x_palabra,
                        y_palabra
                        ) 
        pygame.display.update()

def jugar_carta_scene(ronda, jugador, other):

    eligiendo = True
    opt = 0

    while eligiendo:
        # limpiar pantalla
        screen.fill(BLACK)

        marcador = f'Ronda {ronda} - {jugador.nombre} {jugador.puntos} | {other.nombre} {other.puntos}'

        if jugador.modificador_truco > 1:
            marcador = f'{marcador} | Estamos en TRUCO'

        draw_text(
            screen,
            marcador,
            20,
            WHITE,
            SCREEN_RESOLUTION[0] / 4,
            0
        ) 

        draw_text(
            screen,
            f'{jugador.nombre}',
            20,
            WHITE,
            SCREEN_RESOLUTION[0] / 2,
            SCREEN_RESOLUTION[1] - 25
        ) 

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                end_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    end_game()

                if event.key == pygame.K_RIGHT:
                    opt += 1
                    if opt > len(jugador.mano) - 1:
                        opt = 0

                if event.key == pygame.K_LEFT:
                    opt -= 1
                    if opt < 0:
                        opt = len(jugador.mano) - 1

                if event.key == pygame.K_SPACE:
                    jugador.cartas_jugadas.append(jugador.mano.pop(opt))
                    eligiendo = False

                if event.key == pygame.K_t:
                    # preguntar si ya se cantó truco
                    cantar_truco(jugador, other)

        if other.cartas_jugadas:
            for i, carta in enumerate(other.cartas_jugadas):
                img_carta = pygame.image.load(carta.imagen)
                x_carta = SCREEN_RESOLUTION[0] / 2 - 100 + i * 65
                y_carta = SCREEN_RESOLUTION[1] / 4 - 120
                screen.blit(img_carta, (x_carta, y_carta))

        if jugador.cartas_jugadas:
            for i, carta in enumerate(jugador.cartas_jugadas):
                img_carta = pygame.image.load(carta.imagen)
                x_carta = SCREEN_RESOLUTION[0] / 2 - 100 + i * 65
                y_carta = SCREEN_RESOLUTION[1] / 4 + 50
                screen.blit(img_carta, (x_carta, y_carta))

            # pygame.display.update()

        # dibujar cartas
        for i, carta in enumerate(jugador.mano):
            img_carta = pygame.image.load(carta.imagen)
            x_carta = SCREEN_RESOLUTION[0] / 2 - 100 + i * 65
            if i == opt:
                y_carta = SCREEN_RESOLUTION[1] - 250
            else:
                y_carta = SCREEN_RESOLUTION[1] - 200
            screen.blit(img_carta, (x_carta, y_carta))

        pygame.display.update()

# Game Loop
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            end_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                end_game()

    # repartir cartas
    jugador1.mano = []
    jugador2.mano = []

    jugador1.cartas_jugadas = []
    jugador2.cartas_jugadas = []

    jugador1.modificador_truco = 1
    jugador2.modificador_truco = 1


    for _ in range(3):
        jugador1.agarrar_carta(mazo.agarrar())
        jugador2.agarrar_carta(mazo.agarrar())

    ganador = False
    ronda = 1

    jugador1.primera = False
    jugador2.primera = False

    while ronda <= 3 and ganador == False:

        jugar_carta_scene(ronda, jugador1 , jugador2)

        jugar_carta_scene(ronda, jugador2, jugador1)
        
        
        # comparar
        if jugador1.cartas_jugadas[ronda-1].valor == jugador2.cartas_jugadas[ronda-1].valor:
            # parda la mejor
            # el que gana segunda gana
            if jugador1.primera:
                msg = f'{jugador1.nombre} gana la ronda'
                draw_ganador(msg, jugador1.cartas_jugadas[ronda-1], jugador2.cartas_jugadas[ronda-1])
                # Dar puntos
                jugador1.puntos +=1 * jugador1.modificador_truco
                ganador = True
            elif jugador2.primera:
                jaux = jugador2
                jugador2 = jugador1
                jugador1 = jaux
                f'{jugador1.nombre} gana la ronda'
                draw_ganador(msg, jugador1.cartas_jugadas[ronda-1], jugador2.cartas_jugadas[ronda-1])
                # Dar puntos
                jugador1.puntos +=1 * jugador1.modificador_truco
                ganador = True
            else:
                jugador1.primera = True
                jugador2.primera = True

                msg = 'Empate! Parda la mejor'
                draw_ganador(msg, jugador1.cartas_jugadas[ronda-1], jugador2.cartas_jugadas[ronda-1]) 
        else:
            # Si gana jugador2 pasa a ser el primero la prox ronda
            if jugador1.cartas_jugadas[ronda-1].valor < jugador2.cartas_jugadas[ronda-1].valor:
                jaux = jugador2
                jugador2 = jugador1
                jugador1 = jaux

            if jugador1.primera:
                msg = f'{jugador1.nombre} gana la ronda'
                draw_ganador(msg, jugador1.cartas_jugadas[ronda-1], jugador2.cartas_jugadas[ronda-1])
                ganador = True
                # Dar puntos
                jugador1.puntos +=1 * jugador1.modificador_truco
            else:
                jugador1.primera = True
                msg = f'La carta de {jugador1.nombre} gana'
                draw_ganador(msg, jugador1.cartas_jugadas[ronda-1], jugador2.cartas_jugadas[ronda-1])

        time.sleep(2)
        ronda += 1