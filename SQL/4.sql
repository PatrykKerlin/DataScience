-- Ile wniosków pochodzi z nie zakłóconej podróży?

select count(w.id) as liczba_wnioskow
from wnioski w
left join podroze p on w.id = p.id_wniosku
left join szczegoly_podrozy sp on p.id = sp.id_podrozy
where czy_zaklocony = false;

-- W którym roku było najwięcej wniosków w języku polskim?

select date_part('year', data_utworzenia) as rok, count(id) as liczba_wnisokow
from wnioski
where jezyk = 'pl'
group by 1
order by 2 desc
limit 1;

-- Które wnioski podczas analizy nie wykazały zaistnienia strajku oraz dobrej pogody?

select id_wniosku
from analizy_wnioskow
where brak_strajku = 'true'
and pogoda_ok = 'false';

-- Wyświetl dane o zmianie ilości analiz prawnych z roku na rok(year over year).

select date_part('year', data_rozpoczecia) as rok,
       count(id) as liczba_wnioskow,
       lag(count(id)) over () as poprzednio,
       round((count(id) - lag(count(id)) over ()) / lag(count(id)::numeric) over (),2) as zmiana
from analiza_prawna
group by 1;

-- Podaj medianę i kwartyle (Q1 i Q3) procentu opłaty za usługę wniosków z analizą prawną.

select
       percentile_disc(0.5) within group (order by oplata_za_usluge_prawnicza_procent) as mediana,
       percentile_disc(0.25) within group (order by oplata_za_usluge_prawnicza_procent) as q1,
       percentile_disc(0.75) within group (order by oplata_za_usluge_prawnicza_procent) as q3
from wnioski;

-- Jaka jest korelacja między kwotą rekompensaty oryginalnej i kwotą rekompensaty, dla języka?

select jezyk, corr(kwota_rekompensaty, kwota_rekompensaty_oryginalna) as korelacja
from wnioski
group by 1
order by 2 desc;








-- Dla każdego wniosku dla, którego nastąpiła rekompensata ale nie było informacji o źródle
-- polecenia przyporządkuj dokładnie 1 wniosek podobny, który:
-- -> jest z tego samego rodzaju konta (tabela szczegoly_rekompensat) oraz jest wypłacony z
--    tego samego powodu,
-- -> ma informację o źródle polecenia i został utworzony wcześniej niż porównywany wniosek
-- -> ma kwotę rekompensaty identyczną, bądź możliwie jak najbardziej podobną. W przypadku
--    równych kwot kilku wniosków podobnych, wybrać ten, który został złożony w najmniejszym
--    odstępie czasowym od porównywanego wniosku

with wnioski_glowne as (
       select w.id,
              w.data_utworzenia,
              w.stan_wniosku,
              w.zrodlo_polecenia,
              sr.konto,
              w.powod_operatora,
              w.kwota_rekompensaty
       from wnioski w
                   join rekompensaty r on w.id = r.id_wniosku
                   join szczegoly_rekompensat sr on r.id = sr.id_rekompensaty
       where w.zrodlo_polecenia is null
         and lower(w.stan_wniosku) like 'wypl%'
),
     wnioski_podobne as (
            select w.id,
                   w.data_utworzenia,
                   w.stan_wniosku,
                   w.zrodlo_polecenia,
                   sr.konto,
                   w.powod_operatora,
                   w.kwota_rekompensaty
            from wnioski w
                        join rekompensaty r on w.id = r.id_wniosku
                        join szczegoly_rekompensat sr on r.id = sr.id_rekompensaty
            where w.zrodlo_polecenia is not null
              and lower(w.stan_wniosku) like 'wypl%'
     ),
     wnioski_razem as (
            select row_number() over (partition by wg.id
              order by abs(wp.kwota_rekompensaty - wg.kwota_rekompensaty),
                wg.data_utworzenia - wp.data_utworzenia) as numer,
                   wg.id                                              as id_glowny,
                   wp.id                                              as id_podobny,
                   wg.kwota_rekompensaty                              as kwota_glowna,
                   wp.kwota_rekompensaty                              as kwota_podobna,
                   abs(wp.kwota_rekompensaty - wg.kwota_rekompensaty) as kwota_roznica,
                   wg.data_utworzenia                                 as data_glowna,
                   wp.data_utworzenia                                 as data_podobna,
                   wg.data_utworzenia - wp.data_utworzenia            as data_roznica,
                   wg.zrodlo_polecenia                                as zrodlo_glowne,
                   wp.zrodlo_polecenia                                as zrodlo_podobne
            from wnioski_glowne wg
              join wnioski_podobne wp on wg.powod_operatora = wp.powod_operatora
            where wg.konto = wp.konto
              and wg.powod_operatora = wp.powod_operatora
              and wp.data_utworzenia < wg.data_utworzenia
     ),

-- Wylistować id wniosku i jego kwotę rekompensaty, id wniosku podobnego oraz źródło
-- wniosku podobnego. Ponadto z powyższego zestawienia zrobić podsumowanie z liczbą i
-- średnią kwotą wniosków ze względu na źródło wniosku podobnego.
-- UWAGA: Dla części wniosków nie znajdziemy żadnego wniosku podobnego, spełniającego
-- powyższe wymagania.

     lista_wnioskow as (
            select id_glowny as id_wniosku_glownego,
                   kwota_glowna as rekompensata_wniosku_glownego,
                   id_podobny as id_wniosku_podobnego,
                   zrodlo_podobne as zrodlo_polecenia_wniosku_podobnego
            from wnioski_razem
            where numer = 1
     )
select zrodlo_polecenia_wniosku_podobnego,
       count(1) as liczba_wnioskow,
       avg(rekompensata_wniosku_glownego)
from lista_wnioskow
group by 1;