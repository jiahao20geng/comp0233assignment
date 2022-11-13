from typing import Dict, List, Tuple
from dataclasses import dataclass
from typing import Any
from pathlib import Path

@dataclass
class City:
    def __init__(self,cityname:"str",country:"str",attendee:"int",lat:"float",lon:"float") ->"City":
        if type(cityname)!=str:
            raise TypeError("the city name must be a String!")
        if type(country)!=str:
            raise TypeError("the country must be a String!")
        if type(attendee)!=int:
            raise TypeError("the number of attendee must be integer!")
        if type(lat)!=float:
            raise TypeError("the latitude must be a decimal number!")
        if type(lon)!=float:
            raise TypeError("the longitude must be a decimal number!")
        if attendee<=0:
            raise ValueError("the number of attendee must be a positive integer!")
        if lat<-90 or lat>90:
            raise ValueError("latitude must be restricted to the -90 to 90 ranges")
        if lon<-180 or lon>180:
            raise ValueError("the longitude must be restricted to the -180 to 180 ranges")
        
        self.cityname=cityname
        self.country=country
        self.attendee=attendee
        self.lat=lat
        self.lon=lon
        
    
    def distance_to(self, other: 'City') -> float:
        raise NotImplementedError
    
    def co2_to(self, other: 'City') -> float:
        raise NotImplementedError



@dataclass
class CityCollection:
    city: Any

    def countries(self) -> List[str]:
        raise NotImplementedError

    def total_attendees(self) -> int:
        raise NotImplementedError

    def total_distance_travel_to(self, city: City) -> float:
        raise NotImplementedError

    def travel_by_country(self, city: City) -> Dict[str, float]:
        raise NotImplementedError

    def total_co2(self, city: City) -> float:
        raise NotImplementedError

    def co2_by_country(self, city: City) -> Dict[str, float]:
        raise NotImplementedError

    def summary(self, city: City):
        raise NotImplementedError

    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        raise NotImplementedError

    def plot_top_emitters(self, city: City, n: int, save: bool):
        raise NotImplementedError


