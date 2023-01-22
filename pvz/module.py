import numpy as np
from data_source import Zombie,Plants
from typing import List
def get_hp_down(zombie:Zombie, plants:List[Plants],time:float,dist:float,plant_pos:List[float])->float:
    ans = 0
    for plant in plants:
        if plant.only_hurt_metal and zombie.metal:
            ans += plant.damage
            zombie.metal = 0
            continue
        if time/plant.damage_interval == int(time/plant.damage_interval) and plant.damage_distance[0]<dist-plant_pos[plants.index(plant)]<plant.damage_distance[1]:
            ans += plant.damage
    return ans