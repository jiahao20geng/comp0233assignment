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
    
    #the distance from one city to another
    def distance_to(self, other: 'City') -> float: 
        
        lat1=self.lat
        lon1=self.lon
        lat2=other.lat
        lon2=other.lon
        R=6371
        distance=2*R*math.asin(math.sqrt(math.sin((lat2*math.pi/180-lat1*math.pi/180)/2)**2+math.cos(lat1*math.pi/180)*math.cos(lat2*math.pi/180)*(math.sin((lon2*math.pi/180-lon1*math.pi/180)/2)**2)))
        return distance
    
    #the total CO2 emitted by all the attendees from one city to another
    def co2_to(self,other:'City') -> float:
        if self.distance_to(other)<=1000:
            co2=0.2*self.attendee*self.distance_to(other)
        if self.distance_to(other)>1000 and self.distance_to(other)<=8000:
            co2=0.25*self.attendee*self.distance_to(other)
        if self.distance_to(other)>8000:
            co2=0.3*self.attendee*self.distance_to(other)
        return co2
        
class CityCollection:
    def __init__(self,list_of_cities:"list"):
        self.cities=list_of_cities
    
    #define the list of total counties and no repeat countries
    def countries(self) -> List[str]:
        countries_set = []
        for c in self.cities:
            c=c.country
            if not c in countries_set:
                countries_set.append(c)
        return countries_set
    
    #define the total attendees from all the countries
    def total_attendees(self) -> int:
        total=0
        for c in self.cities:
            total+=c.attendee
        return total
    
    #define the total distance from one city to the host city
    def total_distance_travel_to(self, city: City) -> float:
        total_distance_travel_to=0
        for c in self.cities:
            total_distance_travel_to+=c.distance_to(city)
        return total_distance_travel_to
    
    #define the total distance of every country
    def travel_by_country(self, city: City) -> Dict[str, float]:
        sum={}
        for c in self.cities:  
            travel_by_country={}    
            travel_by_country[c.country]=c.distance_to(city)
            if c.country in sum.keys():
                sum[c.country]+=c.distance_to(city)
            else:
                sum[c.country]=c.distance_to(city)
        return sum
    
    #define the total CO2 emitted by all the cities
    def total_co2(self, city: City) -> float:#所有地方飞到主办地(苏黎世)排放的CO2总和
        total_co2=0
        for c in self.cities:
            total_co2+=c.co2_to(city)
        return total_co2
    
    #define the CO2 emitted by each country
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
        if n<len(top_country):
            top_country=top_country[:n]
            top_country.append("Everywhere else")
            CO2_emission2=CO2_emission[:n]
            a=CO2_emission[n:]
            total=0.0
            for i in range(len(a)):
               total+=a[i]
            CO2_emission2.append(total)
        else:
            CO2_emission2=CO2_emission
                                
        plt.bar(range(len(CO2_emission2)),CO2_emission2,tick_label=top_country)
        plt.title("Total emissions from each country",fontsize=15)
        file_name=city.cityname.lower().replace(" ","_")
        if save:
            plt.savefig('./{}.jpg'.format(file_name))
        else:
            plt.show()
        return file_name
