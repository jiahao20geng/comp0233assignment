import pytest
from pytest import raises,approx
from cities import City, CityCollection

#Class City

#attendee must be a positive number
with raises(ValueError):
    City('Zurich', 'Switzerland', -10, 47.22, 8.33)

with raises(ValueError):
    City('Zurich', 'Switzerland', 0, 47.22, 8.33)

#latitude should be restricted to -90 to 90
with raises(ValueError):
    zurich = City('Zurich', 'Switzerland', 52, -100.0, 8.33)

with raises(ValueError):
    zurich = City('Zurich', 'Switzerland', 52, 100.0, 8.33)

#longitude should be restricted to -180 to 180
with raises(ValueError):
    zurich = City('Zurich', 'Switzerland', 52, 47.22, -200.0)

with raises(ValueError):
    zurich = City('Zurich', 'Switzerland', 52, 47.22, 200.0)

#  the name and country should be passed as strings 
with raises(TypeError):
    zurich = City(3232323, 'Switzerland', 52, 47.22, 8.33)

with raises(TypeError):
    zurich = City('Zurich', False, 52, 47.22, 8.33)
    
with raises(TypeError):
    zurich = City(100.00, 'Switzerland', 52, 47.22, 8.33)

#number of attendees as an integer
with raises(TypeError):
    zurich = City('Zurich', 'Switzerland', 52.0, 47.22, 8.33)

with raises(TypeError):
    zurich = City('Zurich', 'Switzerland', '52.0', 47.22, 8.33)

#latitude and longitude as decimal numbers(in degrees)
with raises(TypeError):
    zurich = City('Zurich', 'Switzerland', 52, 47, 8.33)

with raises(TypeError):
    zurich = City('Zurich', 'Switzerland', 52, 47.22, 8)

with raises(TypeError):
    zurich = City('Zurich', 'Switzerland', 52, '47.22', 8.33)

with raises(TypeError):
    zurich = City('Zurich', 'Switzerland', 52, 47.22, '8.33')

#Class CityCollection

#Define cities
zurich = City('Zurich', 'Switzerland', 52, 47.22, 8.33)
san_francisco = City('San Francisco', 'United States', 71, 37.77, -122.41)
greenwich = City('Greenwich', 'United Kingdom', 15, 51.48, 0.0)
beijing=City('Beijing','China',950,39.91,116.39)
shanghai=City('Shanghai','China',96,31.23,121.47)
hongkong=City('Hong Kong','China',6,22.35,114.18)

#method distance_to
assert zurich.distance_to(san_francisco) == san_francisco.distance_to(zurich)
assert greenwich.distance_to(beijing) == beijing.distance_to(greenwich)
assert shanghai.distance_to(hongkong) == hongkong.distance_to(shanghai)

assert zurich.distance_to(san_francisco) == 9374.706927199608
assert greenwich.distance_to(beijing) == 8135.444186791611
assert shanghai.distance_to(hongkong) == 1223.3505954866278

#method co2_to
assert zurich.co2_to(san_francisco) == approx(9374.706927199608*0.3*52,1e-7)
assert greenwich.co2_to(beijing) == approx(8135.444186791611*0.3*15,1e-7)
assert shanghai.co2_to(hongkong) == approx(1223.3505954866278*0.25*96,1e-7)

list_of_cities=[zurich,san_francisco,greenwich,beijing,shanghai,hongkong]
city_collection=CityCollection(list_of_cities)

#method countries
assert city_collection.countries()==['Switzerland','United States','United Kingdom','China']

#method total_attendees
assert city_collection.total_attendees()==1190

host_city=zurich
#method total_distance_travel_to
zrh_distance=zurich.distance_to(zurich)
sfo_distance=san_francisco.distance_to(zurich)
gwc_distance=greenwich.distance_to(zurich)
bj_distance=beijing.distance_to(zurich)
sh_distance=shanghai.distance_to(zurich)
hk_distance=hongkong.distance_to(zurich)

assert city_collection.total_distance_travel_to(zurich)==sfo_distance+gwc_distance+bj_distance+sh_distance+hk_distance

#method travel_by_country
dictionary={'Switzerland':zrh_distance,'United States':sfo_distance,'United Kingdom':gwc_distance,'China':bj_distance+sh_distance+hk_distance}

assert city_collection.travel_by_country(zurich)==dictionary

#method total_co2
zrh_co2=zurich.co2_to(zurich)
sfo_co2=san_francisco.co2_to(zurich)
gwc_co2=greenwich.co2_to(zurich)
bj_co2=beijing.co2_to(zurich)
sh_co2=shanghai.co2_to(zurich)
hk_co2=hongkong.co2_to(zurich)

assert city_collection.total_co2(zurich)==zrh_co2+sfo_co2+gwc_co2+bj_co2+sh_co2+hk_co2

#method co2_by_country
co2_dictionary={'Switzerland':zrh_co2,'United States':sfo_co2,'United Kingdom':gwc_co2,'China':bj_co2+sh_co2+hk_co2}

assert city_collection.co2_by_country(zurich)==co2_dictionary

#method sorted_by_emissions
emission=[('Zurich',city_collection.total_co2(zurich)),('San Francisco',city_collection.total_co2(san_francisco)),('Greenwich',city_collection.total_co2(greenwich)),('Beijing',city_collection.total_co2(beijing)),('Shanghai',city_collection.total_co2(shanghai)),('Hong Kong',city_collection.total_co2(hongkong))]
emission.sort(key=lambda a:a[1])

assert city_collection.sorted_by_emissions()==emission