##surely this assignment Ive been putting off wont cause me lengthy pain and suffering
import json
import sys


#References:
#https://www.w3schools.com/python/python_json.asp Referenced for json parsong technique
#https://www.digitalocean.com/community/tutorials/python-str-repr-functions Referenced proper printing using __str__ and __repr__

'''
Variables:
Arrivals/Aircraft
Hangers
Forklifts
Trucks


'''


class Aircraft:
    def __init__(self, id, arrival, cargo):
        self.id = id
        self.arrival = arrival
        self.cargo = cargo

    def __str__(self):
        return f'\nAircraft id : {self.id} | Arrival Time : {self.arrival} | Cargo : {self.cargo}'  
    
    def __repr__(self):
        return self.__str__()



class Hanger:
    def __init__(self, id, Aircraft, Truck, pallets):
        self.id = id
        self.aircraft = Aircraft
        self.pallets = pallets

class Forklifts:
    def __init__(self, id, Aircraft, Hanger, Pallet, Truck):
        self.id = id
        self.aircraft = Aircraft
        self.hanger = Hanger
        self.pallet = Pallet
        self.truck = Truck

class Truck:
    def __init__(self, id, Forklifts, Hanger):
        self.id = id
        self.forklifts = Forklifts
        self.hanger = Hanger


class Meta:
    def __init__(self, start, stop, hangers, forklifts)
        self.start = start
        self.stop = stop
        self.hangers = hangers
        self.forklifts = forklifts
   
    
    
#I think it passes it in as a dict in a dict, dictception???
class Parser:
    
    def parseAircraft(self, jsonData):
        data = json.loads(jsonData)
        print(data)
        ret_aircraft = []
        for aircraft, values in data.items():
            new_aircraft = Aircraft(aircraft, values['Time'], values['Cargo'])
            ret_aircraft.append(new_aircraft)
        return ret_aircraft
    
    def parseMeta(self, jsonData):
        data = json.loads(jsonData)
        ret_data = {
            "start": data['StartT Time'],
            "stop" : data['Stop Time'],
            ""

        }

    
def read_file(filename):
    with open(filename, "r") as file:
        return file.read()
    

# terminalScheduler.py META_PATH AIRCRAFT_PATH TRUCKS_PATH SCHEDULE_PATH
def main():
    parse = Parser()

    meta = read_file(sys.argv[1])
    print(parse.parseMeta(meta))


    aircrafts = read_file(sys.argv[2])
    print(parse.parseAircraft(aircrafts))


    trucks = read_file(sys.argv[3])
    print(parse.parseTrucks(trucks))

    #AND ALSO OUTPUT FILE SOMEWHERE 
    #WRITE TO SCHEDULE PATH OR SMTHN
    schedule_path = sys.argv[4]

if __name__ == "__main__":
    main()  