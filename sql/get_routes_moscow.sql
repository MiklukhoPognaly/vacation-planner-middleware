Select distinct
  c.city_code as arrival_iata
  ,d.name_translations as name
  ,e.rus_name as counry_name
  ,e.world_part
  ,e.location
  ,d.sea_vacation
  ,d.ski_vacation
from public.routes as a
inner join
public.iata_mapping as b
on a.departure_airport_iata = b.code
inner join public.iata_mapping as c
on a.arrival_airport_iata = c.code
inner join public.cities d
on d.code = c.city_code
inner join public.countries e
on d.country_code = e.iata_2
where b.city_code = 'MOW';