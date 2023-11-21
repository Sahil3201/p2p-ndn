from UDPNode1 import p2p_node
from router import Router
import argparse

class Base():
    def __init__(self, id):
        self.data=id+"_data"

    def update(self):
        pass


if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Node Interface', type=str)
    args = parser.parse_args()

    if args.name is None:
        print("Please specify node name")
        exit(1)

    router = Router(args.name)
    interface = Base(args.name)
    node = p2p_node(args.name,router,interface)
    node.run()
