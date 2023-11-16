import json, random

addresses = ["10.35.70.4", "10.35.70.46"]

networks = ["weather", "soil", 'irrigation', 'livestock', 'crop']

sensorList = [['temperature', 'humidity', 'wind_speed', 'rain_gauge', 'solar_radiation', 'evapotranspiration', 'atmospheric_gas', 'barometric_pressure'], # weatherSensorList
['moisture', 'erosion', 'salinity', 'texture', 'temperature', 'organic_matter_content', 'pH'], # soilSensorList
['moisture', 'flow_rate', 'pressure', 'quality', 'pump_status', 'pH', 'evapotranspiration', 'turbidity'], # irrigationSensorList
['temperature', 'RFID_Tag', 'heart_rate_monitor', 'milk_production', 'consumption_meter', 'proximity_meters', 'feed_intake', 'activity_monitor'], # livestockSensorList
['temperature', 'humidity', 'oxygen_level', 'ethylene_gas', 'carbon_dioxide', 'moisture_content', 'rain_gauge']] # cropSensorList

nodeNeighborList = ["weather","soil","irrigation","livestock","crop"]

json_array = []

port = 33001

def get_addr(sensor_no=0):
    return {
                "listen port": port,
                "send port": port+1,
                "address": addresses[sensor_no//3]
            }

def getNodeAddr(nodeName):
    return f'/{nodeName}s/{nodeName}1'


nodeNames = [getNodeAddr(nodeNeighborList[i]) for i in range(len(nodeNeighborList))]



for i in range(len(nodeNeighborList)):
    nodeName = getNodeAddr(nodeNeighborList[i])
    json_array.append({nodeName : [
        get_addr(i), 
        {
                "neighbors": [getNodeAddr(random.choice(nodeNeighborList)) for _ in range(random.randint(1,3))]
            }
            ]})
    for j in range(len(sensorList)):
        json_array.append({f'{nodeName}/{sensorList[i][j]}' : [
        get_addr(i), 
        {
                "neighbors": nodeName
            }
            ]})


# for diver in Divers:
#     diver_name = "/" + Networks[0] + "/" + diver
#     json_array.append({diver_name : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]},{"neighbors" : DiverNeighborList[neighbor_itertator]}]})
#     listen_port += 2
#     send_port += 2
#     neighbor_itertator +=1
#     for sensor in DiverSensors:
#         json_array.append({"/" + Networks[0] + "/" + diver + "/" + sensor : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]},{"neighbors" : [diver_name]}]})
#         listen_port += 2
#         send_port += 2

# neighbor_itertator = 0
# for scientist in Scientists:
#     scientist_name = "/" + Networks[1] + "/" + scientist
#     json_array.append({scientist_name : [{"listen port": listen_port,"send port": send_port,"address": Addresses[1]},{"neighbors" : ScientistNeighborList[neighbor_itertator]}]})
#     listen_port += 2
#     send_port += 2
#     for sensor in ScientistSensors:
#         json_array.append({"/" + Networks[1] + "/" + scientist + "/" + sensor : [{"listen port": listen_port,"send port": send_port,"address": Addresses[1]},{"neighbors" : [scientist_name]}]})
#         listen_port += 2
#         send_port += 2



with open('interfaces.json', 'w') as f:
  json.dump(json_array, f, indent=4)
