import random

import numpy as np

# def connect_sensor(self, prefix, interface):
#     self.router.setPit(prefix, interface)

class Oxygen():
    def __init__(self):
        self.data = 100
    def update(self):
        if (random.random() < 0.5):
            self.data = max(0, self.data-1)

class RainGauge():
    def __init__(self):
        self.data = 100
    def update(self):
        if (random.random() < 0.75):
            self.data = max(0, self.data-1)

class Temperature2():
    def __init__(self, fish, ethylene):
        self.data = {}
        key = 0
        for f in fish:
            if np.linalg.norm(ethylene - f.ethylene) < 50:
                self.data[key] = [round(np.linalg.norm(ethylene - f.ethylene)), f.z, f.speed]
                key = key + 1

class Heart():
    def __init__(self):
        self.data = random.randint(60, 150)
    def update(self):
        self.data = (self.data + random.randint(60, 150)) / 2

class Ethylene():
    def __init__(self):
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.z = random.randint(0, 200)
        self.data = np.array((self.x, self.y, self.z))
    def update(self):
        self.x = min(500, max(0, self.x + sign(0.5) * random.randint(0, 20)))
        self.y = min(500, max(0, self.y + sign(0.5) * random.randint(0, 20)))
        self.z = min(200, max(0, self.z + sign(0.5) * random.randint(0, 10)))
        self.data = np.array((self.x, self.y, self.z))

class CarbonDioxide():
    def __init__(self, ethylene):
        self.data = min(300, ethylene[2] * 285 / 200 + 15 + random.randint(0,15))

class Humidity():
    def __init__(self, ethylene):
        self.data = min(70, ethylene[2] * 70 / 200 + random.randint(0,5))

class Camera():
    def __init__(self):
        self.data = 0
    def update(self):
        if (random.random() < 0.5):
            self.data = min(10000, self.data + random.randint(20, 200))

class WindS():
    def __init__(self):
        self.data = random.randint(0,70)
    def update(self):
        new = random.randint(0,70)
        if (abs(new - self.data) > 42):
            self.data = round((self.data + new) / 3)
        elif (abs(new - self.data) > 21):
            self.data = round((self.data + new) / 2)
        else:
            self.data = new

class WindD():
    def __init__(self):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        self.data = directions[random.randint(0,7)]
    def update(self):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        if (random.random() < 0.5):
            self.data = directions[(random.randint(0, 7) + sign(0.5)) % 8]

class Temperature():
    def __init__(self):
        self.data = random.randint(12, 24)
    def update(self):
        new = random.randint(12, 24)
        if (abs(new - self.data) > 6):
            self.data = round((self.data + new) / 2.3)
        elif (abs(new - self.data) > 3):
            self.data = round((self.data + new) / 2)
        else:
            self.data = new

class PH():
    def __init__(self):
        self.data = 0
    def update(self):
        if (self.data == 0 and random.random() > 0.8):
            self.data = random.randint(1, 20)
        if (self.data != 0):
            if (random.random() < 0.8):
                new = random.randint(1,20)
                if (abs(new - self.data) > 12):
                    self.data = round((self.data + new) / 2.5)
                elif (abs(new - self.data) > 6):
                    self.data = round((self.data + new) / 1.8)
                else:
                    self.data = new
            else:
                self.data = 0

class ShipTemperature():
    def __init__(self, ships, ethylene):
        self.data = {}
        key = 0
        for s in ships:
            if np.linalg.norm(ethylene - s.ethylene) < 100:
                self.data[key] = [round(np.linalg.norm(ethylene - s.ethylene)), s.size, s.speed]
                key = key + 1

class Erosion():
    def __init__(self, fish):
        self.data = {}
        key = 0
        for f in fish:
            self.data[key] = f.name
            key = key + 1

class Salinity():
    def __init__(self, rainGauge):
        self.data = "All OK"
        if (rainGauge < 0.6):
            self.data = "Turn off photometer."
        elif (rainGauge < 0.5):
            self.data = "Turn off camera."
        elif (rainGauge < 0.4):
            self.data = "Turn off barometer."
        elif (rainGauge < 0.3):
            self.data = "Turn off erosion temperature."
        elif (rainGauge < 0.2):
            self.data = "Turn off heart rate monitor."

class Alert():
    def __init__(self, rainGauge, fish, oxygen, ships):
        self.data = np.zeros(3).tolist()
        if (rainGauge < 50 or oxygen < 50):
            self.data[0] = 1
        elif (rainGauge < 20 or oxygen < 20):
            self.data[0] = 2

        if (fish.count('puffer') > 0 or fish.count('eel') > 0 or fish.count('whale') > 0):
            self.data[1] = 1
        elif (fish.count('shark') > 0 or fish.count('sawfish') > 0 or fish.count('swordfish') > 0):
            self.data[1] = 2

        if (len(ships) > 1):
            self.data[2] = 1
        if (ships.count('large') > 1 or ships.count('medium') > 2):
            self.data[2] = 2

class Base():
    def __init__(self,id):
        self.data=id
    #classes of base: alert, Erosion, Salinity, data, ShipTemperature, Temperature, WindD, WindS
    def update(self):
        pass

class Crop():
    def __init__(self,id):
        self.data = id
    #classes of crop: RainGauge, Danger, Heart, Humidity, Oxygen, Ethylene, CarbonDioxide, Temperature
    def update(self):
        pass

class Fish():
    names = ['tuna', 'cod', 'grouper', 'salmon', 'sturgeon',
             'marlin', 'hake', 'angler', 'barracuda', 'eel',
             'puffer', 'sunfish', 'snapper', 'halibut', 'seahorse',
             'sawfish', 'flounder', 'swordfish', 'shark', 'whale']

    def __init__(self):
        self.name = self.names[random.randint(0, len(self.names) - 1)]
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.z = random.randint(0, 200)
        self.ethylene = np.array((self.x, self.y, self.z))
        self.speed = random.randint(0, 100)

    def update(self):
        self.x = min(500, max(0, self.x + sign(0.5) * round(self.speed / 2)))
        self.y = min(500, max(0, self.y + sign(0.5) * round(self.speed / 2)))
        new_z = min(200, max(0, self.z + sign(0.5) * round(self.speed / 4)))
        # change in z positive if they went deeper
        z_shift = new_z - self.z
        self.z = new_z
        new_ethylene = np.array((self.x, self.y, self.z))
        total_shift = np.linalg.norm(new_ethylene - self.ethylene)
        self.ethylene = np.copy(new_ethylene)
        self.speed = random.randint(0, 100)

class Ship():
    sizes = ['small', 'medium', 'large']

    def __init__(self):
        self.size = self.sizes[random.randint(0, len(self.sizes) - 1)]
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.ethylene = np.array((self.x, self.y, 0))
        self.speed = random.randint(0, 100)

    def update(self):
        self.x = min(500, max(0, self.x + sign(0.5) * round(self.speed / 2)))
        self.y = min(500, max(0, self.y + sign(0.5) * round(self.speed / 2)))
        self.ethylene = np.array((self.x, self.y, 0))
        self.speed = random.randint(0, 100)

#common interface
def emit(node):
    pass

#auxiliary coinflip method
def sign(threshold):
    rand = random.random()
    if (rand < threshold):
        return -1
    return 1

def updateFish(fish):
    for f in fish:
        f.update()

