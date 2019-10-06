-- Ćwiczenie sql na bazie danych airHelp. Napisać zapytanie, które pokaże:

-- a. ilość wniosków dla których kwota rekompensaty na pasażera była większa niż 400
-- i mniejsza niż 500;

select count(id) as ilosc_wnioskow
from wnioski
where kwota_rekompensaty/liczba_pasazerow > 400
and kwota_rekompensaty/liczba_pasazerow < 500;

-- b. procent wniosków posiadających analizę operatora;

select 100 * count(ao.id)/count(w.id)::numeric as procent_wnioskow
from wnioski w
left join analiza_operatora ao on w.id = id_wniosku;

-- c. maksymalną wartość rekompensaty dla wniosków, których status analizy prawnej
-- jest zaakceptowany.

select max(kwota_rekompensaty) as maksymalna_wartosc
from wnioski w
left join analiza_prawna ap on w.id = id_wniosku
where lower(status) like 'zaakcept%';