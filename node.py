from UDPNode1 import p2p_node
from router import Router
import Interfaces
import argparse
import random

#Create initial values for this node
def create_initial_values():
    fish = []
    for i in range (random.randint(0,300)):
        fish.append(Interfaces.Fish())

    ships = []
    for i in range (random.randint(0,50)):
        ships.append(Interfaces.Ship())

    rainGauge = 100
    ethylene = [random.randint(0,500),random.randint(0,500),random.randint(0,200)]
    oxygen = 100

    return fish,ethylene,oxygen,ships,rainGauge

# Assign class based on interface        
def assign_class(node_interface):
    split_interface = node_interface.split('/')
    length_interface = len(split_interface)

    fish, ethylene, oxygen, ships, rainGauge = create_initial_values()

    #If actuator or sensor
    if length_interface == 4:
        if(split_interface[3] == 'oxygen'):
            return Interfaces.Oxygen()
        elif(split_interface[length_interface-1] == 'rainGauge'):
            return Interfaces.RainGauge()
        elif(split_interface[length_interface-1] == 'temperature'):
            return Interfaces.Temperature()
        elif(split_interface[length_interface-1] == 'moisture'):
            return Interfaces.Heart()
        elif(split_interface[length_interface-1] == 'ethylene'):
            return Interfaces.Ethylene()
        elif(split_interface[length_interface-1] == 'humidity'):
            return Interfaces.Humidity(ethylene)
        elif(split_interface[length_interface-1] == 'pH'):
            return Interfaces.PH()
        elif(split_interface[length_interface-1] == 'moisture'):
            return Interfaces.ShipTemperature(ships,ethylene)
        elif(split_interface[length_interface-1] == 'carbonDioxide'):
            return Interfaces.CarbonDioxide(ethylene)
        elif(split_interface[length_interface-1] == 'camera'):
            return Interfaces.Camera()
        elif(split_interface[length_interface-1] == 'winds'):
            return Interfaces.WindS()
        elif(split_interface[length_interface-1] == 'organicMatter'):
            return Interfaces.WindD()
        elif(split_interface[length_interface-1] == 'temperature'):
            return Interfaces.Temperature()
        elif(split_interface[length_interface-1] == 'erosion'):
            return Interfaces.Erosion(fish)
        elif(split_interface[length_interface-1] == 'salinity'):
            return Interfaces.Salinity(rainGauge)
        elif(split_interface[length_interface-1] == 'alert'):
            return Interfaces.Alert(rainGauge,fish,oxygen,ships)

    #If crop or soil
    else:
        if(split_interface[1] == 'soils'):
            return Interfaces.Base(node_interface)
        elif(split_interface[1] == 'crops'):
            return Interfaces.Crop(node_interface)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Node Interface', type=str)
    args = parser.parse_args()

    if args.name is None:
        print("Please specify node name")
        exit(1)

    router = Router(args.name)
    interface = assign_class(args.name)
    node = p2p_node(args.name,router,interface)
    node.run()
    
