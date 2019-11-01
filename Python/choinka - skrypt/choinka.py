import msvcrt as ms
from colorama import init
from termcolor import colored
init()
wysokosc = input('Wprowadź wysokość choinki (5-40): ')
try:
    choinka = int(wysokosc)
    z = choinka - 1
    x = 1
    if 4 < choinka < 41:
        print('\n Proszę bardzo: \n')
        for i in range(choinka):
            print(colored(' ' * z + '*' * x + ' ' * z, 'green'))
            x += 2
            z -= 1
        if choinka > 9:
            for w in range(2):
                print(colored(' ' * (choinka - 3) + '*' * 5, 'red'))
        else:
                print(colored(' ' * (choinka - 2) + '*' * 3, 'red'))
    else:
        print(colored('Podano wartość spoza wymaganego przedziału!', 'red'))
except ValueError:
    print(colored('Nie podano liczby całkowitej z podanego przedziału!', 'red'))
finally:
    print('\n made by Patryk Kerlin :)')
    print(colored('\n Press any key to exit...', 'yellow'))
    while True:
        if ms.kbhit():
            break