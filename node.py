from UDPNode1 import p2p_node
from router import Router
import Interfaces
import argparse
import random

# Assign class based on interface        
def assign_class(node_interface):
    split_interface = node_interface.split('/')
    length_interface = len(split_interface)

    # If sensor
    if length_interface == 4:
        sensor_name = split_interface[length_interface-1 ]
        if(sensor_name in ['temperature']):
            return Interfaces.RangeIntSensor(20, 30)
        elif(sensor_name in ['ph']):
            return Interfaces.RangeSensor(1, 13)
        # Percent values
        elif(sensor_name in ['humidity', 'windSpeed']):
            return Interfaces.RangeSensor(1, 99)
        else:
            return Interfaces.RangeSensor(1, 99)

    # If node
    else:
        return Interfaces.Node(node_interface)

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
    
