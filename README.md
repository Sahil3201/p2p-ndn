# p2p Name-Defined Network

This repository is a group project for the TCD module CS7NS1: Scalable Computing. Our aim is to create a peer-to-peer (p2p) name-defined network designed for communication across multiple Raspberry Pi devices. The project is exemplified with an agriculture mission emulation.

## Group 4 NDN Run Instructions

To run our two name-defined networks on independent Raspberry Pi's, follow these instructions:

### Setup:

1. To start, you have to specify your ip address of the Raspberry Pi's in the interfaces.json file. Simply search and replace every instance of "10.35.70.46" with the ip address of your 1st pi and replace every instance of "10.35.70.4" with the ip address of your 2nd pi.

### On Pi 1:

1. Cd into the project folder.
1. Run the command: `source .tmux/centralNode`
   - This starts the Central Node authority network which managed the RSA public keys of devices.
1. Run the command: `source .tmux/ndn-soils`
   - This starts the Soil network.

### On Pi 2:

1. Cd into the project folder.
2. Run the command: `source .tmux/ndn-crops`
   - This starts the Crop network.

### On either or both Pi(s):

1. Run the command: `tmux attach` on both pi.
   - This allows you to interface with the nodes in the network.
2. To see a list of selectable nodes, press `Ctrl+b` and then `w`.
3. Select a node (e.g. '/crops/crop2') with the arrow keys and press enter to use the node's terminal.
4. The node's command line prompts to 'Ask the network for information:'.
   - Type in some data name (e.g. /soils/soil3/moisture') from the list of data names at the end of this document. If an invalid name is typed, the data won’t send.
5. Wait for the data to return. You can track the routing by switching to other nodes.
6. To exit tmux, press `Ctrl+b` and then `d`.
7. To kill the network and all running ports, enter the command: `tmux kill-server`

### Network Structure

The network is divided into two types of devices - nodes and sensors.

- Sensors are devices with three-level names, such as */soils/soil4/temperature*.
- Nodes are devices with two-level names, such as */soils/soil4*.

Nodes with two-level names can access data from every other sensor or node. If an attempt is made to get data from sensors away from its node network, it will fail to retrieve the data. However, nodes can retrieve data from all sensors in the entire network of networks.

#### Network graph
The network nodes are connected in the following manner:

![Network Graph](https://github.com/Sahil3201/p2p-ndn/blob/minimal/network%20architecture/Network%20Graph.png)

The Crops nodes have the following device sensors:

<img src="https://github.com/Sahil3201/p2p-ndn/blob/minimal/network%20architecture/Crops%20Device%20Graph.png" alt="Crops Device Graph" style="width:1000px;"/>

The Soils nodes have the following device sensors:

<img src="https://github.com/Sahil3201/p2p-ndn/blob/minimal/network%20architecture/Soils%20Device%20Graph.png" alt="Soils Device Graph" style="width:1000px;"/>

### List of Data Names
#### List of Names of Nodes
"/crops/crop1",
"/crops/crop2",
"/crops/crop3",
"/crops/crop4",
"/crops/crop5",
"/soils/soil1",
"/soils/soil2",
"/soils/soil3",
"/soils/soil4",
"/soils/soil5"

#### List of Names of Sensors
"/crops/crop1/humidity",
"/crops/crop1/oxygen",
"/crops/crop1/ethylene",
"/crops/crop1/carbonDioxide",
"/crops/crop1/temperature",
"/crops/crop1/moisture",
"/crops/crop1/rainGauge",
"/crops/crop1/camera",
"/crops/crop2/humidity",
"/crops/crop2/oxygen",
"/crops/crop2/ethylene",
"/crops/crop2/carbonDioxide",
"/crops/crop2/temperature",
"/crops/crop2/moisture",
"/crops/crop2/rainGauge",
"/crops/crop2/camera",
"/crops/crop3/humidity",
"/crops/crop3/oxygen",
"/crops/crop3/ethylene",
"/crops/crop3/carbonDioxide",
"/crops/crop3/temperature",
"/crops/crop3/moisture",
"/crops/crop3/rainGauge",
"/crops/crop3/camera",
"/crops/crop4/humidity",
"/crops/crop4/oxygen",
"/crops/crop4/ethylene",
"/crops/crop4/carbonDioxide",
"/crops/crop4/temperature",
"/crops/crop4/moisture",
"/crops/crop4/rainGauge",
"/crops/crop4/camera",
"/crops/crop5/humidity",
"/crops/crop5/oxygen",
"/crops/crop5/ethylene",
"/crops/crop5/carbonDioxide",
"/crops/crop5/temperature",
"/crops/crop5/moisture",
"/crops/crop5/rainGauge",
"/crops/crop5/camera",
"/soils/soil1/moisture",
"/soils/soil1/erosion",
"/soils/soil1/salinity",
"/soils/soil1/winds",
"/soils/soil1/organicMatter",
"/soils/soil1/temperature",
"/soils/soil1/pH",
"/soils/soil1/alert",
"/soils/soil2/moisture",
"/soils/soil2/erosion",
"/soils/soil2/salinity",
"/soils/soil2/winds",
"/soils/soil2/organicMatter",
"/soils/soil2/temperature",
"/soils/soil2/pH",
"/soils/soil2/alert",
"/soils/soil3/moisture",
"/soils/soil3/erosion",
"/soils/soil3/salinity",
"/soils/soil3/winds",
"/soils/soil3/organicMatter",
"/soils/soil3/temperature",
"/soils/soil3/pH",
"/soils/soil3/alert",
"/soils/soil4/moisture",
"/soils/soil4/erosion",
"/soils/soil4/salinity",
"/soils/soil4/winds",
"/soils/soil4/organicMatter",
"/soils/soil4/temperature",
"/soils/soil4/pH",
"/soils/soil4/alert",
"/soils/soil5/moisture",
"/soils/soil5/erosion",
"/soils/soil5/salinity",
"/soils/soil5/winds",
"/soils/soil5/organicMatter",
"/soils/soil5/temperature",
"/soils/soil5/pH",
"/soils/soil5/alert"


Feel free to explore and contribute to our p2p name-defined network project!