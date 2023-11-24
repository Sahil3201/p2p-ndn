from UDPNode1 import p2p_node
from router import Router
import argparse
import interfaces

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Node Interface', type=str)
    args = parser.parse_args()

    if args.name is None:
        print("Please specify node name")
        exit(1)

    if args.name == 'centralNode':
        node = CentralNode('centralNode')
    else:
        router = Router(args.name)
        interface = interfaces.Base(args.name)
        node = p2p_node(args.name,router,interface)
        node.run()
