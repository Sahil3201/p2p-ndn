import random

import numpy as np

# def connect_sensor(self, prefix, interface):
#     self.router.setPit(prefix, interface)

class PercentSensor():
    def __init__(self):
        self.data = random.randint(0,100)

    def update(self):
        self.data = random.randint(0,100)


class RangeIntSensor(minVal, maxVal):
    def __init__(self):
        self.data = random.randint(minVal, maxVal)
    def update(self):
        self.data = random.randint(minVal, maxVal)


class RangeSensor(minVal, maxVal):
    def __init__(self):
        self.data = random.randint(minVal, maxVal)
    def update(self):
        self.data = random.randint(minVal, maxVal)



class Node():
    def __init__(self,id):
        self.data=id
    def update(self):
        pass



