##surely this assignment Ive been putting off wont cause me lengthy pain and suffering
import json
import sys


#References:
#https://www.w3schools.com/python/python_json.asp Referenced for json parsong technique
#https://www.digitalocean.com/community/tutorials/python-str-repr-functions Referenced proper printing using __str__ and __repr__

'''
Variables:
Arrivals/Aircraft
Hangars
Forklifts
Trucks

{
    "aircraft": {
        "The Aircraft": {
            "Hangar": "The Hangar",
            "Arrival": 800,
            "Departure": 820
        }
    },
    "trucks": {
        "The Truck": {
            "Hangar": "The Hangar",
            "Arrival": 820,
            "Departure": 825
        }
    },
    "forklifts": {
        "The Forklift": [
            {
                "Hangar": "The Hangar",
                "Time": 800,
                "Job": "Unload"
            },
            {
                "Hangar": "The Hangar",
                "Time": 825,
                "Job": "Load"
            }
        ]
    }
}

'''


class Aircraft:
    def __init__(self, id, arrival, cargo):
        self.id = id
        self.arrival = arrival
        self.departure = -1
        self.cargo = cargo

    def setDeparture(self, time):
        self.departure = time

    def __str__(self):
        return f'Aircraft id : {self.id} | Arrival Time : {self.arrival} | Cargo : {self.cargo}'  
    
    def __repr__(self):
        return self.__str__()



class Hangar:
    def __init__(self, id):
        self.id = id
        self.aircraft = None
        self.pallets = 0
        self.trucks = []
        self.forklifts = []

    def addPlane(self, aircraft):
        self.aircraft = aircraft

    def addTruck(self, truck):
        self.trucks.append(truck)

    
    def addForklift(self, Forklift):
        self.forklifts.append(Forklift)

    def __str__(self):
        return f'Hangar id : {self.id} | Aircraft : {self.aircraft} | Pallets : {self.pallets} | Trucks : {self.trucks}'  
    
    def __repr__(self):
        return self.__str__()

class Forklifts:
    def __init__(self, id,):
        self.id = id
        self.schedule = []

    def add_job(self, hangar, time, job):
        newJob = {
            "Hangar": hangar,   #ID of hangar
            "Time": time,       #time in format
            "Job": job          #Either load or unload
            }
        
        self.schedule.append(newJob)
    
    def __str__(self):
        return f'Forklift id : {self.id} | Schedule : {self.schedule}\n' 
    
    def __repr__(self):
        return self.__str__()


class Truck:
    def __init__(self, id, Time):
        self.id = id
        self.time = Time      
        self.Hangar = None
    
    def __str__(self):
        return f'Truck id : {self.id} | Arrival Time : {self.time} | Hangar : {self.Hangar}'  
    
    def __repr__(self):
        return self.__str__()


#There can only be one Meta per instance
class Meta:
    def __init__(self, start, stop, Hangars, forklifts):
        self.start = start
        self.stop = stop
        self.Hangars = Hangars
        self.forklifts = forklifts
    

    def __str__(self):
        return f'Meta Start: {self.start} | Stop Time : {self.stop} | Hangars : {self.Hangars}, Forklifts : {self.forklifts}'  
    
    def __repr__(self):
        return self.__str__()
   
#I think it passes it in as a dict in a dict, dictception???
class Parser: 
    def parseAircraft(self, jsonData):
        data = json.loads(jsonData)
        ret_aircraft = []
        for aircraft, values in data.items():
            new_aircraft = Aircraft(aircraft, values['Time'], values['Cargo'])
            ret_aircraft.append(new_aircraft)
        return ret_aircraft
    
    def parseMeta(self, jsonData):
        data = json.loads(jsonData)
        ret_data = Meta(
            start = data['Start Time'],
            stop = data['Stop Time'],
            Hangars = data['Hangars'],
            forklifts = data['Forklifts']
        )
        return ret_data
    
    def parseTrucks(self, jsonData):
        data = json.loads(jsonData)
        ret_truck = []
        for truck, values, in data.items():
            new_truck = Truck(truck, values)
            ret_truck.append(new_truck)
        return ret_truck
    

class state:
    def __init__(self, MetaData: Meta):
        self.start = MetaData.start
        self.stop = MetaData.stop
        self.hangars = MetaData.Hangars
        self.forklifts = MetaData.forklifts
        self.trucks = []  
        self.schedule = {
            "aircraft": {},
            "trucks": {},
            "forklifts": {}
        } 

    def scheduleAircraft(self, aircraft:Aircraft):
        #Assign aircraft to hangers, for now do not worry about other vehicles
        for hangar in self.hangars:
            if hangar.Aircraft is None:
                hangar.Aircraft = aircraft
                aircraft.departure = aircraft.arrival + 20




    
def read_file(filename):
    with open(filename, "r") as file:
        return file.read()
    

# terminalScheduler.py META_PATH AIRCRAFT_PATH TRUCKS_PATH SCHEDULE_PATH
# python terminalScheduler.py ./tests/test1_passes/meta.json ./tests/test1_passes/aircraft.json ./tests/test1_passes/trucks.json ./
def main():
    parse = Parser()


    meta = read_file(sys.argv[1])
    print(parse.parseMeta(meta))


    aircrafts = read_file(sys.argv[2])
    print(parse.parseAircraft(aircrafts))


    trucks = read_file(sys.argv[3])
    print(parse.parseTrucks(trucks))

    #In this order
    #Aircraft > Forklift > Truck
    #AND ALSO OUTPUT FILE SOMEWHERE 
    #WRITE TO SCHEDULE PATH OR SMTHN
    schedule_path = sys.argv[4]

if __name__ == "__main__":
    main()  