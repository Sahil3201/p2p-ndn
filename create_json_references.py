import json, random

Addresses = ["10.35.70.4", "10.35.70.46"]

Networks = ["crops", "soils"]

Crops = ["crop1","crop2","crop3","crop4","crop5"]
CropNeighborList = [["/crops/crop3","/crops/crop4","/soils/soil1"], ["/crops/crop4","/crops/crop5","/soils/soil1","/soils/soil4"], ["/crops/crop1"], ["/crops/crop1","/crops/crop2"], ["/crops/crop2","/soils/soil2"]]

Soils = ["soil1", "soil2", "soil3","soil4","soil5"]

CropSensors = ["humidity", "oxygen", "ethylene", "carbonDioxide", "temperature", "moisture", "rainGauge", "camera"]

SoilSensors = ["moisture", "erosion", "salinity", "winds", "organicMatter", "temperature", "pH", "alert"]
SoilNeighborList = [["/soils/soil3","/soils/soil4","/crops/crop1","/crops/crop2"], ["/soils/soil3","/crops/crop2","/crops/crop5"],["/soils/soil1","/soils/soil2","/soils/soil4","/soils/soil5"], ["/soils/soil3"]]


listen_port = 33001
send_port = 33002
neighbor_itertator = 0
for crop in Crops:
    crop_name = "/" + Networks[0] + "/" + crop
    json_array.append({crop_name : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]},{"neighbors" : CropNeighborList[neighbor_itertator]}]})
    listen_port += 2
    send_port += 2
    neighbor_itertator +=1
    for sensor in CropSensors:
        json_array.append({"/" + Networks[0] + "/" + crop + "/" + sensor : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]},{"neighbors" : [crop_name]}]})
        listen_port += 2
        send_port += 2

neighbor_itertator = 0
for soil in Soils:
    soil_name = "/" + Networks[1] + "/" + soil
    json_array.append({soil_name : [{"listen port": listen_port,"send port": send_port,"address": Addresses[1]},{"neighbors" : SoilNeighborList[neighbor_itertator]}]})
    listen_port += 2
    send_port += 2
    for sensor in SoilSensors:
        json_array.append({"/" + Networks[1] + "/" + soil + "/" + sensor : [{"listen port": listen_port,"send port": send_port,"address": Addresses[1]},{"neighbors" : [soil_name]}]})
        listen_port += 2
        send_port += 2


with open('interfaces.json', 'w') as f:
  json.dump(json_array, f, indent=4)
