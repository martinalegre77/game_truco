import os
import time

from class_truco import Jugador, Mazo

# crear el mazo
mazo = Mazo()

# ver el mazo completo
# for carta in mazo.cartas:
#   carta.mostrar()

jugador1 = Jugador('Pipi')
jugador2 = Jugador('Martin')

# Game Loop
while True:
    # borrar pantalla
    os.system('clear')
    # Tanteador
    print(f'{jugador1.nombre} tiene {jugador1.puntos} puntos')
    print(f'{jugador2.nombre} tiene {jugador2.puntos} puntos')
    print()

    # repartir cartas
    jugador1.mano = []
    jugador2.mano = []

    for _ in range(3):
        jugador1.agarrar_carta(mazo.agarrar())
        jugador2.agarrar_carta(mazo.agarrar())

    ganador = False
    ronda = 1

    jugador1.primera = False
    jugador2.primera = False

    while ronda <= 3 and ganador == False:
        print(f'Ronda {ronda}')

        jugador1.jugar_carta()
        print(f'{jugador1.nombre} juega {jugador1.carta_jugada.mostrar()}')
        time.sleep(2)
        print()

        jugador2.jugar_carta()
        print(f'{jugador2.nombre} juega {jugador2.carta_jugada.mostrar()}')
        time.sleep(2)
        print()
        print()

        # comparar
        if jugador1.carta_jugada.valor > jugador2.carta_jugada.valor:
            print(f'{jugador1.nombre} gana el turno')
            if jugador1.primera:
                print(f'Ganó {jugador1.nombre}!')
                jugador1.puntos +=1
                ganador = True
                # Dar puntos
            else:
                jugador2.primera = True

        elif jugador1.carta_jugada.valor < jugador2.carta_jugada.valor:
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

