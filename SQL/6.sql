-- Należy wczytać plik xpdusd_d.csv zawierający notowania palladium od 2016 roku.

-- - należy wyliczyć średnie ceny zamknięcia w agregacji miesięcznej, ponadto wyliczyć z tych cen wartości MoM.
-- - Wygenerować daty od 2016 roku do końca 2019 w interwałach miesięcnych.
-- - dla miesięcy dla których nie mamy danych będziemy wyliczali predykcję średnich cen miesięczych:

-- należy wyliczyć średnią wartość MoM - będzię to nasz współczynniki trendu, czyli wartość procentowa o jaką średnio zmienia się cena w stosunku do poprzedniego miesiąca.
-- Wartość ceny dla kolejnych miesięcy będzie zmieniać się zgodnie z współczynnikiem trendu.
-- Przykład:
-- 1000 = cena z ostatniego miesiąca
-- 0.1 = wspołczynnik trendu

-- 1_cena_predykowana = 1000 + 1000 * 0.1
-- 2_cena_predykowana =  1_cen_predykowana + 1_cena_predykowana * 0.1
-- itd...

with avg_pal as (
    select to_char(data, 'yyyy-mm') as yyyy_mm,
           avg(zamkniecie) as avg_zamkniecie
    from xpdusd_d
    group by 1
    order by 1
),
    avg_pal_mom as (
    select *,
           lag(avg_zamkniecie) over () as lag,
           (avg_zamkniecie - lag(avg_zamkniecie) over ())
               / lag(avg_zamkniecie) over () as mom
    from avg_pal
),
    nowe_daty as (
    select to_char(generate_series('2016-01-01', '2019-12-31',
        interval '1 month')::date, 'yyyy-mm') as daty
),
    avg_mom as (
    select avg(mom) as sr_mom
    from avg_pal_mom
),
    nnn as (
    select daty,
           row_number() over (order by daty) as n
    from nowe_daty
    where (select max(yyyy_mm) from avg_pal) < daty
),
    ost_cena_zamk as (
    select to_char(data, 'yyyy-mm'),
           avg(zamkniecie) as ost_avg_cena
    from xpdusd_d
    group by 1
    order by 1 desc
    limit 1
),
    pred as (
    select nn.daty as yyyy_mm, nn.n, ocz.ost_avg_cena, am.sr_mom,
           (ocz.ost_avg_cena * (1 + am.sr_mom) ^ nn.n) as avg_zamkniecie
    from nnn nn, ost_cena_zamk ocz, avg_mom am
)
    select yyyy_mm as data, round(avg_zamkniecie, 2) as srednia_cena_zamkniecia
    from avg_pal
    union all
    select yyyy_mm as data, round(avg_zamkniecie, 2) as srednia_cena_zamkniecia
    from pred;
