import random

N_CARTAS = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
N_PALOS = [0, 1, 2, 3]

class Mazo():
    # 40 cartas
    def __init__(self):
        self.cartas = []
        for palo in N_PALOS:
            for numero in N_CARTAS:
                carta = Carta(numero, palo)
                self.cartas.append(carta)

        random.shuffle(self.cartas)

    def agarrar(self):
        return self.cartas.pop()

class Carta():
    def __init__(self, numero, palo):
        palos = ['espada', 'basto', 'oro', 'copa']
        self.numero = numero
        self.npalo = palo
        self.palo = palos[palo]
        self.imagen = f'img/{self.npalo}_{self.numero}.jpg'
        self.valor = self._rankear()

    def mostrar(self):
        return f'{self.numero} de {self.palo}'

    def _rankear(self):
        if self.numero != 1 and self.numero != 7:
            basicas = {
                        2: 9,
                        3: 10,
                        4: 1,
                        5: 2,
                        6: 3,
                        10: 5,
                        11: 6,
                        12: 7
                    }
            return basicas[self.numero]

        if self.numero == 1:
            if self.npalo == 1: # ancho de basto
                return 13
            elif self.npalo == 0: # ancho es espada
                return 14
            else:
                return 8

        if self.numero == 7:
            if self.npalo == 0: # 7 de espada
                return 13
            elif self.npalo == 2: # 7 es oro
                return 14
            else:
                return 4

class Jugador():
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0
        self.mano = []
        self.cartas_jugadas = []
        self.primera = False
        self.modificador_truco = 1

    def agarrar_carta(self, carta):
        self.mano.append(carta)

    def mostrar_mano(self):
        if len(self.mano) <= 0:
            return'No tengo cartas'
        else:
            print(f'Mano de {self.nombre}')
            i = 0
            for carta in self.mano:
                i += 1
                print(f'Carta {i}: {carta.mostrar()}')

    def jugar_carta(self):
        self.mostrar_mano()
        opt = int(input('Cual carta queres jugar? '))

        while opt < 1 or opt > len(self.mano):
            print('Error al elegirr la carta')
            opt = int(input('Elegí bien! '))
        self.carta_jugada = self.mano.pop(opt - 1)
