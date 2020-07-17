import decimal

def generator():
    lista = []
    start = 2
    stop = 5.5
    while start <= stop:
        lista.append(decimal.Decimal(start))
        start += 0.5
    print(lista)

generator()