from UDPNode1 import p2p_node
from router import Router
import argparse
import interfaces
from centralNode import CentralNode

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
        interface = interfaces.Base(args.name)
        node = p2p_node(args.name,router,interface)
        node.run()
