-- Należy wczytać plik athlete_events.csv, zawierający zawodników startujących w igrzyskach olimpijskich. (źródło: kaggle.com)

-- W wielu przykadkach brakuje informacji o wzroście i wadze zawodników, dane te będzie trzeba uzupełnić.
-- Dane te należy uzulełnić wartością mediany wagi lub wzrostu zawodników tej samej płci, konkurencji sportowej (pole sport) i roku igrzysk.
-- Jeżeli w danym przecięciu płeć-sport-rok jest mniej niż połowa zawodników z kompletnymi danymi wzrostu i wagi,
-- wtedy należy z naszego zbioru usunąć wszystkich zawodników tego przecięcia.
-- Tak samo nalezy usunąć takie przecięcia, w których jest mniej niż 10 zawodników z kompletnymi danymi.

-- Dla tak oczyszczonego zboiru nalezy jeszcze dodać pole bmi wyliczone wg wzoru: waga [kg]/ wzrost [m] ^2.
-- Taki zbiór danych należy wyeksportować do pliku csv - w drugiej części zadania będziemy go wczytywać w Tableu.

-- Ponadto należly wyliczyć średnie bmi w przecięciach płeć-sport-rok.
-- Następnie utworzyć zapytanie w którym orzymamy sporty dla kobiet oraz mężczyzn, które charakteryzują się największą zmiennością na przestrzeni lat.
-- Czyli takie, które mają największe odchylenie standardowe z średnich rocznych wartości.

select * into TEMP athlete_events_backup from athlete_events;

UPDATE athlete_events
SET weight = nullif(weight,'NA')
where weight = 'NA';

UPDATE athlete_events
SET height = nullif(height,'NA')
where height = 'NA';

select *
from athlete_events;

with dane_licznosc as (
    select sex,
           sport,
           season,
           year,
           count(distinct (id))                                  as licznosc,
           percentile_disc(0.5) within group ( order by height ) as mediana_wzrost,
           percentile_disc(0.5) within group ( order by weight ) as mediana_waga
    from athlete_events
    where lower(height) is not null
      and lower(weight) is not null
    group by 1, 2, 3, 4
    having count(distinct (id)) >= 10
    order by 1, 2, 3
),
dane_licz_ogol as (
    select sex,
           sport,
           season,
           year,
           count(distinct(id)) as licznosc_ogolna
    from athlete_events
    group by 1, 2, 3, 4
    order by 1, 2, 3
),
dane_filtr as (
    select dl.sex,
           dl.sport,
           dl.season,
           dl.year,
           dl.licznosc,
           dog.licznosc_ogolna,
           100 * (dl.licznosc / dog.licznosc_ogolna::numeric) as licznosc_procent
    from dane_licznosc dl
             join dane_licz_ogol dog on dl.sex = dog.sex
        and dl.sport = dog.sport
        and dl.year = dog.year
    where 100 * (dl.licznosc / dog.licznosc_ogolna::numeric) >= 50
    order by 1, 2, 3
),
dane_do_uzupelnienia as (
    select distinct(ae.id),
                   df.sex    as plec,
                   df.sport,
                   df.season as sezon,
                   df.year   as rok,
                   ae.height as wzrost_z_na,
                   ae.weight as waga_z_na,
                   dl.mediana_wzrost,
                   dl.mediana_waga
    from dane_filtr df
             join athlete_events ae on df.sex = ae.sex
        and df.sport = ae.sport
        and df.year = ae.year
             join dane_licznosc dl on df.sex = dl.sex
        and df.sport = dl.sport
        and df.year = dl.year
    order by 1, 2, 3
),
dane_uzupelnione as (
    select plec,
           sport,
           sezon,
           rok,
           (case
               when waga_z_na is null then mediana_waga
               when waga_z_na is not null then waga_z_na
               end)::numeric as waga,
           (case
               when wzrost_z_na is null then mediana_wzrost
               when wzrost_z_na is not null then wzrost_z_na
               end)::numeric as wzrost
    from dane_do_uzupelnienia
    order by 1, 2, 3
),
dane_bmi as (
    select *,
           (waga / power((wzrost / 100), 2)) as bmi
    from dane_uzupelnione
),
dane_bmi_avg as (
    select *, avg(bmi) over (partition by plec, sport, rok) as bmi_avg
    from dane_bmi
),
dane_bmi_stddev as (
    select *, round(stddev(bmi_avg) over (partition by plec, sport), 5) as bmi_stddev
    from dane_bmi_avg
)
select distinct(sport), sezon, plec, rok, round(bmi_avg,2) as bmi_avg,
     bmi_stddev as stddev,
     max(bmi_stddev) over (partition by plec) as max_stddev
from dane_bmi_stddev
order by 2, 1, 3;



