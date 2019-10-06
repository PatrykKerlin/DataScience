create table kierowcy (id_kierowcy integer primary key, imie varchar(50) not null,
nazwisko varchar(50) not null, srednia_ocena integer);

create table samochody (id_samochody integer primary key, nr_rejestracyjny varchar(7) not null,
przebieg integer not null, data_przegladu date not null, ilosc_miejsc integer not null,
marka varchar(50) not null, model varchar(50) not null);

create table oceny (id_oceny integer primary key, id_przejazdy integer not null, ocena integer not null,
komentarz varchar(500));

create table przejazdy (id_przejazdy integer primary key, id_kierowcy integer not null,
id_samochody integer not null, czas integer not null, dystans integer not null, koszt float(2) not null,
napiwek float(2), id_oceny integer, foreign key (id_oceny) references oceny,
foreign key (id_kierowcy) references kierowcy, foreign key (id_samochody) references samochody);

insert into kierowcy (id_kierowcy, imie, nazwisko, srednia_ocena)
values (1, 'Sylwester', 'Stalone', 9);

insert into kierowcy (id_kierowcy, imie, nazwisko, srednia_ocena)
values (2, 'Dolph', 'Lundgren', 7);

insert into kierowcy (id_kierowcy, imie, nazwisko, srednia_ocena)
values (3, 'Jason', 'Statham', 8);

insert into samochody (id_samochody, nr_rejestracyjny, przebieg, data_przegladu, ilosc_miejsc, marka, model)
values (1, 'GDA1234', 25000, '2018-11-12', 5, 'Mercedes', 'E320');

insert into samochody (id_samochody, nr_rejestracyjny, przebieg, data_przegladu, ilosc_miejsc, marka, model)
values (2, 'GBY4321', 123000, '2019-02-15', 5, 'Volkswagen', 'Passat');

insert into samochody (id_samochody, nr_rejestracyjny, przebieg, data_przegladu, ilosc_miejsc, marka, model)
values (3, 'WGM8546', 45000, '2018-08-01', 9, 'Renault', 'Trafic');

insert into samochody (id_samochody, nr_rejestracyjny, przebieg, data_przegladu, ilosc_miejsc, marka, model)
values (4, 'GD789XY', 85000, '2018-12-16', 5, 'Audi', 'A6');

insert into samochody (id_samochody, nr_rejestracyjny, przebieg, data_przegladu, ilosc_miejsc, marka, model)
values (5, 'GSP548Z', 12000, '2019-02-02', 5, 'Toyota', 'Prius');

insert into oceny (id_oceny, id_przejazdy, ocena, komentarz)
values (1, 1, 7, 'Miły kierowca, tanio :)');

insert into oceny (id_oceny, id_przejazdy, ocena, komentarz)
values (2, 2, 9, 'Wszystko OK');

insert into oceny (id_oceny, id_przejazdy, ocena)
values (3, 4, 8);

insert into przejazdy (id_przejazdy, id_kierowcy, id_samochody, czas, dystans, koszt, napiwek, id_oceny)
values (1, 1, 2, 23, 15, 30.50, 5, 1);

insert into przejazdy (id_przejazdy, id_kierowcy, id_samochody, czas, dystans, koszt)
values (2, 2, 1, 12, 4, 10.00);

insert into przejazdy (id_przejazdy, id_kierowcy, id_samochody, czas, dystans, koszt, id_oceny)
values (3, 3, 3, 35, 20, 52.35, 2);

insert into przejazdy (id_przejazdy, id_kierowcy, id_samochody, czas, dystans, koszt, napiwek, id_oceny)
values (4, 2, 5, 27, 14, 33.30, 2.50, 3);

alter table oceny add foreign key (id_przejazdy) REFERENCES przejazdy

