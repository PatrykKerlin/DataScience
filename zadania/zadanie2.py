import random

def roznice():
    lista = []
    wejscie = []
    wyjscie = []
    n = 10
    for x in range(n):
        lista.append(x + 1)
        wejscie.append(x + 1)

    for y in range(random.randrange(1, len(wejscie))):
        toRemove = random.choice(wejscie)
        wejscie.remove(toRemove)

    wyjscie = list(set(lista) - set(wejscie))
    print('1-n:', lista)
    print('wejście: {}, {}'.format(wejscie, n))
    print('wyjście:', wyjscie)

roznice()