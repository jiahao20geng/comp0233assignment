from cities import City, CityCollection
from pathlib import Path
import csv
from typing import Dict, List, Tuple

def read_attendees_file(filepath: Path) -> CityCollection:
    attendee_list=[]
    country_list=[]
    city_list=[]
    lat_list=[]
    lon_list=[]
    
    with open(filepath,"r")as file:
        csvreader=csv.reader(file)
        for coloum in csvreader:
            attendee_list.append(coloum[0])
            country_list.append(coloum[1])
            city_list.append(coloum[3])
            lat_list.append(coloum[4])
            lon_list.append(coloum[5])
    attendee_list=attendee_list[1:]
    country_list=country_list[1:]
    city_list=city_list[1:]
    lat_list=lat_list[1:]
    lon_list=lon_list[1:]
    
    attendee_list=list(map(int,attendee_list))#covert str to int
    lat_list=list(map(float,lat_list))#convert str to float
    lon_list=list(map(float,lon_list))
 
    citylist=[]
  
    for i in range(len(city_list)):
        attendee=attendee_list[i]
        country=country_list[i]
        cityname=city_list[i]
        lat=lat_list[i]
        lon=lon_list[i]
        city=City(cityname,country,attendee,lat,lon)
        citylist.append(city)
      
    return CityCollection(citylist)


file_path=Path("attendee_locations.csv")

collection=CityCollection(file_path)
file=read_attendees_file(file_path)






