import os
import time
from class_truco import Jugador, Mazo
import pygame

# Const
GAME_DELTA_TIME = 1 # tiempo de espera en seg entre momentos
SCREEN_RESOLUTION = (1000, 620)
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

def jugar_carta_scene(jugador, other):

    eligiendo = True
    opt = 0

    while eligiendo:
        # limpiar pantalla
        screen.fill(BLACK)
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

        if other.cartas_jugadas:
            for i, carta in enumerate(other.cartas_jugadas):
                img_carta = pygame.image.load(carta.imagen)
                x_carta = SCREEN_RESOLUTION[0] / 2 - 100 + i * 65
                y_carta = SCREEN_RESOLUTION[1] / 4 - 160
                screen.blit(img_carta, (x_carta, y_carta))

            pygame.display.update()

        # dibujar cartas
        for i, carta in enumerate(jugador.mano):
            img_carta = pygame.image.load(carta.imagen)
            x_carta = SCREEN_RESOLUTION[0] / 2 - 100 + i * 65
            if i == opt:
                y_carta = SCREEN_RESOLUTION[1] - 250
            else:
                y_carta = SCREEN_RESOLUTION[1] - 160
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


    for _ in range(3):
        jugador1.agarrar_carta(mazo.agarrar())
        jugador2.agarrar_carta(mazo.agarrar())

    ganador = False
    ronda = 1

    jugador1.primera = False
    jugador2.primera = False

    while ronda <= 3 and ganador == False:

        jugar_carta_scene(jugador1 , jugador2)

        jugar_carta_scene(jugador2, jugador1)
        
        
        # comparar
        if jugador1.cartas_jugadas[ronda-1].valor > jugador2.cartas_jugadas[ronda-1].valor:
            print(f'{jugador1.nombre} gana el turno')
            if jugador1.primera:
                print(f'Ganó {jugador1.nombre}!')
                jugador1.puntos +=1
                ganador = True
                # Dar puntos
            else:
                jugador2.primera = True

        elif jugador1.cartas_jugadas[ronda-1].valor < jugador2.cartas_jugadas[ronda-1].valor:
            print(f'{jugador2.nombre} gana el turno')
            print()
            print()
            jaux = jugador2
            jugador2 = jugador1
            jugador1 = jaux

            if jugador1.primera:
                print(f'Ganó {jugador1.nombre}!')
                jugador1.puntos +=1
                ganador = True
                # Dar puntos
            else:
                jugador1.primera = True


        else:
            print(f'Empardados')

        time.sleep(2)
        ronda += 1


# pipi.mostrar_mano()
# print()
# yo.mostrar_mano()

