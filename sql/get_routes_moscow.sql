Select
    a.arrival_city_iata
    ,b.name_translations as arrival_city_name
    from
        (
            Select distinct
            b.city_code as departure_city_iata
            ,c.city_code as arrival_city_iata
            from public.routes as a
            inner join
            public.iata_mapping as b
            on a.departure_airport_iata = b.code
            inner join public.iata_mapping as c
            on a.arrival_airport_iata = c.code
            where b.city_code = 'MOW'
         ) a
    inner join
    public.cities b
    on a.arrival_city_iata = b.code
    inner join public.cities c
    on a.departure_city_iata = c.code