# 1. Stwórz swoją klasę, która zawiera co najmniej 1 atrybut co najmniej jedną metodę
# metodę __init__. Stwórz 2 obiekty tej klasy.
# 2. stwórz klasę "dziecko" dla klasy z poprzedniego zadania, która będzie zawierać co
# najmniej 1 atrybut i nadpisze metodę z poprzedniej klasy. Stwórz 2 obiekty tej klasy.
# 3. W swojej klasie "rodzica" stwórz metodę, która zmieni atrybut obiektu tej klasy i
# zapisze starą wartość tego atrybutu do listy. Zmień kilka razy ten atrybut obiektu
# Twojej klasy i wyświetl historię zmian.
# 4. Napisz iterator po atrybutach obiektu Twojej klasy (niech wyświetla wartość każdego
# atrybutu w konsoli)

class MarvelHeroes:
    team = 'Avengers'
    oldheroes = []

    def __init__(self, name, alias):
        self.name = name
        self.alias = alias

    def herodata(self):
        print(self.name, 'also known as', self.alias, 'is part of the', MarvelHeroes.team, 'team')

    def newheroes(self):
        self.oldheroes.append(self.name+' aka '+self.alias)
        self.name = input('Type in new name: ')
        self.alias = input('Type in new alias: ')
        print(self.name, 'also known as', self.alias, 'is part of the', MarvelHeroes.team, 'team (after change)')


class NewMarvelHeroes(MarvelHeroes):
    universe = 'Earth 616'

    def herodata(self):
        print(self.name, 'also known as', self.alias, 'is part of the', MarvelHeroes.team, 'team an lives in the',
              NewMarvelHeroes.universe)


def heroes():
    ironman = MarvelHeroes('Anthony Stark', 'Iron Man')
    hawkeye = MarvelHeroes('Clinton Barton', 'Hawkeye')
    spiderman = NewMarvelHeroes('Peter Parker', 'Spider-Man')
    antman = NewMarvelHeroes('Scott Lang', 'Ant-Man')
    ironman.herodata()
    hawkeye.herodata()
    spiderman.herodata()
    antman.herodata()
    ironman.newheroes()
    hawkeye.newheroes()


if __name__ == "__main__":
    heroes()

print('Team before change:', MarvelHeroes.oldheroes)

for attr, val in MarvelHeroes.__dict__.items():
    if not attr.startswith('__'):
        print(attr, ":", val)
