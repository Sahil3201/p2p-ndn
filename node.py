from UDPNode1 import p2p_node
from router import Router
import argparse
import interfaces
from centralNode import CentralNode

def get_random_texts(name='', prefix=''):
    return [f'{prefix} All {name} systems normal.', f'{prefix} {name} system needs attention!']

def assign_class(name):
    name_list = name.split('/')
    if(len(name_list)==3 and name_list[1] in ['crops', 'soils']):
        return interfaces.RandomText(name, get_random_texts(name_list[-1]))
    elif (name_list[-1] in ['humidity', 'salinity', 'erosion', 'moisture', 'oxygen', 'ethylene', 'carbonDioxide']):
        return interfaces.ValueRange(name, 1, 99, '%')
    elif (name_list[-1] in ['temperature']):
        return interfaces.ValueRange(name, 10, 30, ' C')
    elif (name_list[-1] in ['rainGauge']):
        return interfaces.ValueRange(name, 10, 250, ' mm')
    elif (name_list[-1] in ['pH']):
        return interfaces.ValueRange(name, 2, 13)
    elif (name_list[-1] in ['winds']):
        return interfaces.ValueRange(name, 1, 30)
    elif (name_list[-1] in ['organicMatter']):
        return interfaces.ValueRange(name, 2, 100, ' ppm')
    elif (name_list[-1] in ['camera']):
        return interfaces.TrueFalse(name)
    elif (name_list[-1] in ['alert']):
        return interfaces.RandomText(name, get_random_texts(name_list[-2], "ALERT:"))
    else:
        print('Assigning base class')
        return interfaces.Base(name)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Node Interface', type=str)
    args = parser.parse_args()

    if args.name is None:
        print("Please specify node name")
        exit(1)

    if args.name.find('centralNodes')!=-1:
        node = CentralNode(args.name)
        node.run()
    else:
        router = Router(args.name)
        interface = assign_class(args.name)
        node = p2p_node(args.name,router,interface)
        node.run()
