import random 
import pickle
from vehicle import Vehicle
from allVariables import *
from misc import *
from car import Car
def nextGeneration() :
    calculateFitness()
    for i in range(total) :
        newVehicle = pickOne()
        newCar = Car(newVehicle)
        cars.append(newCar)
    group.add(cars)
    del savedVehicles[:]
def pickOne(): 
    index = 0 
    r = random.random()
    while r > 0 :
        r = r - savedVehicles[index].fitness
        index += 1
    index -= 1 
    theChoosenOne = savedVehicles[index]
    child = Vehicle(theChoosenOne.brain)
    child.mutate()
    return child
def calculateFitness() : 
    sum = 0
    for vehicle in savedVehicles : 
        sum += vehicle.score
    for vehicle in savedVehicles : 
        vehicle.fitness = vehicle.score / sum
def saveVehicle(fitVehicle) : 
    with open('ML/VehiclesDriving/vehicleCar1.obj' , 'wb') as f : 
        pickle.dump(fitVehicle , f)
def loadVehicle() : 
    with open('ML/VehiclesDriving/vehicleCar.obj' , 'rb') as f : 
        fitVehicle = pickle.load(f)
    return fitVehicle
def runFittestVehicle() : 
    fitVehicle = loadVehicle()
    cars.append(Car(fitVehicle))
    group.add(cars)