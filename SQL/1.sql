select min(price)
from sacramentorealestatetransactions

select max(price)
from sacramentorealestatetransactions

select count(*)
from sacramentorealestatetransactions
where lower(type) like 'residential'

select avg(price)
from sacramentorealestatetransactions
where lower(city) like 'sacramento'

select max(sq__ft)
from sacramentorealestatetransactions
where lower(city) like 'rio linda'

