from typing import Dict, List, Tuple
from typing import Any
from pathlib import Path
import math
import matplotlib.pyplot as plt
 
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
    
    def distance_to(self, other: 'City') -> float: #一个城市到另一个城市的距离
        
        lat1=self.lat
        lon1=self.lon
        lat2=other.lat
        lon2=other.lon
        R=6371
        distance=2*R*math.asin(math.sqrt(math.sin((lat2-lat1)/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2))
        return distance
    
    def co2_to(self, other: 'City') -> float:#一个城市到另一个城市排放的CO2
       
        if self.distance_to(other)<=1000:
            co2=0.2**self.attendee*self.distance_to(other)
        elif self.distance_to(other)>1000 and self.distance_to(other)<=8000:
            co2=0.25*self.attendee*self.distance_to(other)
        else:
            co2=0.3*self.attendee*self.distance_to(other)
        return co2
        
class CityCollection:
    def __init__(self,list_of_cities:"list"):
        self.cities=list_of_cities
    
    def countries(self) -> List[str]:#所有国家的列表，不能有重复
        countries_set = []
        for c in self.cities:
            c=c.country
            if not c in countries_set:
                countries_set.append(c)
        return countries_set

    def total_attendees(self) -> int:#所有国家的所有参会者的总数
        total=0
        for c in self.cities:
            total+=c.attendee
        return total

    def total_distance_travel_to(self, city: City) -> float:#所有地方飞到主办地(苏黎世)的距离总和
        total_distance_travel_to=0
        for c in self.cities:
            total_distance_travel_to+=c.distance_to(city)
        return total_distance_travel_to

    def travel_by_country(self, city: City) -> Dict[str, float]:#每个国家飞到主办地(苏黎世)的距离和
        sum={}
        for c in self.cities:  
            travel_by_country={}    
            travel_by_country[c.country]=c.distance_to(city)
            if c.country in sum.keys():
                sum[c.country]+=c.distance_to(city)
            else:
                sum[c.country]=c.distance_to(city)
        return sum
    
    def total_co2(self, city: City) -> float:#所有地方飞到主办地(苏黎世)排放的CO2总和
        total_co2=0
        for c in self.cities:
            total_co2+=c.co2_to(city)
        return total_co2

    def co2_by_country(self, city: City) -> Dict[str, float]:#每个国家排放的CO2总和
        sum={}
        for c in self.cities:
            co2_by_country={}
            co2_by_country[c.country]=c.co2_to(city)
            if c.country in sum.keys():
                sum[c.country]+=c.co2_to(city)
            else:
                sum[c.country]=c.co2_to(city)
        return sum

    def summary(self, city: City):
        totalco2=int(self.total_co2(city))
        citynumber=len(self.cities)
        attendeesnumber=self.total_attendees()
        print("Host city: {} ({})".format(city.cityname,city.country))
        print("Total CO2: {} tones".format(totalco2))
        print("Total attendee travelling to {} from {} different cities: {}".format(city.cityname,citynumber,attendeesnumber))
        
    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        result=[]
        for c in self.cities:
            result.append((c.cityname,self.total_co2(c)))
        result=sorted(result,key=lambda x:x[:][1])   
        return result
    
    def plot_top_emitters(self, city: City, n: int, save: bool):
        sum=self.co2_by_country(city)
        sum=sorted(sum.items(),key=lambda item:item[1],reverse=True)
        CO2_emission=[]
        top_country=[]
        for i in range(len(sum)):   
            top_country.append(sum[i][0])
            CO2_emission.append(sum[i][1])
        plt.bar(range(len(CO2_emission)),CO2_emission,tick_label=top_country)
        plt.title("Total emissions from each country",fontsize=15)
        plt.show()
        return sum

