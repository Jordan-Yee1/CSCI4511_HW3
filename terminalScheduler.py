##surely this assignment Ive been putting off wont cause me lengthy pain and suffering
import json
import sys


#References:
#https://www.w3schools.com/python/python_json.asp Referenced for json parsong technique
#https://www.digitalocean.com/community/tutorials/python-str-repr-functions Referenced proper printing using __str__ and __repr__


class Aircraft:
    def __init__(self, id, arrival, cargo):
        self.id = id
        self.arrival = arrival
        self.departure = -1
        self.cargo = cargo
        self.hangar = None

    def setHangar(self, hangar):
        if hangar.aircraft is not None:
            return False
        self.hangar = hangar
        
    def setDeparture(self, time):
        self.departure = time

    def getCargo(self):
        return self.cargo
    
    def __str__(self):
        return f'Aircraft id : {self.id} | Arrival Time : {self.arrival} | Cargo : {self.cargo}'  
    
    def __repr__(self):
        return self.__str__()



class Hangar:
    def __init__(self, id):
        self.id = id
        self.aircraft:Aircraft = None
        self.pallets = 0
        self.trucks:Truck = []
        self.forklifts:Forklifts = []

    def addPlane(self, aircraft:Aircraft):
        self.aircraft = aircraft

    def addTruck(self, truck):
        self.trucks.append(truck)
    
    def setPallet(self, pallets):
        if pallets < 0:
            return False
        self.pallets = pallets
    
    def addForklift(self, Forklift):
        self.forklifts.append(Forklift)


    def getPallets(self):
        return self.pallets

    def __str__(self):
        return f'Hangar id : {self.id} | Aircraft : {self.aircraft} | Pallets : {self.pallets} | Trucks : {self.trucks}'  
    
    def __repr__(self):
        return self.__str__()

class Forklifts:
    def __init__(self, id,):
        self.id = id
        self.schedule = []

    def addUnload(self, hangar:Hangar, time):
        newJob = {
            "Hangar": hangar.id,   #ID of hangar
            "Time": time,       #time in format
            "Job": "Unload"          
            }
        
        self.schedule.append(newJob)
        return newJob

    def addLoad(self, hangar:Hangar, time):
        newJob = {
            "Hangar": hangar.id,
            "Time": time,       #time in format
            "Job": "load"          
            }

        self.schedule.append(newJob)

    #Is the forklift not scheduled for a job during a block of time
    #Ex: Has job 800 for unload (takes 20 mins) and checking for 820 for load (5mins)
    # if 800+20 = 820  > startTime conflict found
    # also check upper bound 
    def isFree(self, start, duration):
        if len(self.schedule) == 0:
            return True
        
        for job in self.schedule:
            lastTime = job["Time"]
            lastDuration = -1
            if job["Job"] == "Unload":
                lastDuration = 20
            else:
                lastDuration = 5
            lastJob = lastTime + lastDuration
            if lastJob > start:
                return False

    
    def __str__(self):
        return f'Forklift id : {self.id} | Schedule : {self.schedule}\n' 
    
    def __repr__(self):
        return self.__str__()


class Truck:
    def __init__(self, id, Time):
        self.id = id
        self.time = Time        #The time for arrival of truck (ignore naming conventions, this code is a bomb waiting for the wrong variable name to be changed then everything blows up)
        self.Hangar = None
        self.job = None #Will be a dict for the schedule function, trucks can only have one job once one has been assigned

    def addLoad(self, hangar:Hangar, arrivalTime, departureTime):
        newJob = {
            "Hangar": hangar.id,
            "Arrival": arrivalTime,
            "Departure": departureTime
        }
        self.job = newJob
        return newJob
    
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
        
        #Init hangar objects
        metaHangars = []
        for hangar in MetaData.Hangars:
            metaHangars.append(Hangar(hangar))
        self.hangars = metaHangars
       
        #Init Fork objects
        metaFork = []
        for Fork in MetaData.forklifts:
            metaFork.append(Forklifts(Fork))
        self.forklifts = metaFork
    
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
                aircraft.setHangar(hangar)
                aircraft.departure = aircraft.arrival + 20*aircraft.cargo
                
                new_aircraft = {aircraft.id : {
                    "Hangar": aircraft.hangar,
                    "Arrival": aircraft.arrival,
                    "Departure": aircraft.departure}}
                
                self.schedule["aircraft"][aircraft.id] = new_aircraft

                return True
        print("No hangars possible")
        return False

    #Unloading the forklift assumes that there is a plane in the hanger, if there is not, return False
    def unloadForklift(self, hangar:Hangar):
        if hangar.aircraft is None:
            print(f"No Aircraft{hangar}")
            return False
        for forklift in self.forklifts:
            if len(forklift.schedule) == 0:
                #Both adds the new job to the schedule here and the individual fork lift schedule
                self.schedule["forklifts"][forklift.id] = forklift.addUnload(hangar, hangar.aircraft.arrival)
                return True
        return False #No fork lifts found sutiable
    
    def loadForklift(self, hangar:Hangar):
        if len(hangar.trucks) == 0:
            print(f"No Truck{hangar}")
            return False
        for forklift in self.Forklifts:
            lastJob = forklift.schedule[len(forklift.schedule) - 1]["Job"] 
            if lastJob == "Unload":
                #Will add if the lat job was an unload. Because unloads take 20 mins it will schedule the unload for 20 mins after
                self.schedule["forklifts"][forklift.id] = forklift.addLoad(hangar, lastJob["Time"] + 20)
                return True 
        return False #No fork lifts
        
    def scheduleTruck(self, truck:Truck):
        for hangar in self.hangars:
            if len(hangar.trucks) == 0 and hangar.pallets>0: #WIll naively go to first hangar available with pallets
                hangar.addTruck(truck.id)
                earliestArrival = max(self.start, truck.time)

                departureTime = -1
                for forklift in self.forklifts:

                #Departure time will be the timing of having a fork lift be able to load onto the truck
                self.schedule["trucks"][truck.id] = truck.addLoad(hangar, earliestArrival, departureTime)
                return True
        return False




    #Can be run to do a full scan of the hangars/planes/trucks/forklifts to see if any constraints are being violated
    def checkConstrain(self):
        #First check locational constraints, like is there a forklift scheduled multiple times
        #This only refers to individual objects meaning that it doesnt necessarily check for overlaps (yet)

        #Second check for time constrains (inviduals), is an object scheduled for something either before or after start/stop?

        #Third check for timeoverlap constrains, meaning that two or more objects cannot be in one place at a time.
        #This is different from the previous checks in that it will be comparing multiple objects against each other

        #Fourth is functional constraints, a forklift cant unload a plane that has no more pallets for example
        
        return False
    




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