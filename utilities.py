from cities import City, CityCollection
from pathlib import Path
import csv
from typing import Dict, List, Tuple
from dataclasses import dataclass

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

    
    for i in range(len(city_list)):
        attendee=attendee_list[i]
        country=country_list[i]
        cityname=city_list[i]
        lat=lat_list[i]
        lon=lon_list[i]
        a: List[str,str,int,float,float]=[cityname,country,attendee,lat,lon]
        
       
       
    return a
file_path=Path("attendee_locations.csv")
print(file_path)
print(read_attendees_file("/Users/gengjiahao/Desktop/attendee_locations.csv"))
            