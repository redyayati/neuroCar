import pickle 
from vehicle import Vehicle
from misc import *
def loadVehicle() : 
    with open('ML/VehiclesDriving/vehicleCar.obj' , 'rb') as f : 
        fitVehicle = pickle.load(f)

veh = loadVehicle()
print(dir(veh))
for att in dir(veh) : 
    print(att,getattr(veh,att))