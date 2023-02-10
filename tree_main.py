from fastapi import FastAPI, Body
from typing import Union, Optional
from pydantic import BaseModel

HOW_MANY_TREE = 1

class Tree:
    def __init__(   self, tree_id: int, mode: int, temp : int, humid_soil: int, humid_air: int, color: str, intensity: int,
                    temp_now: int, humid_soil_now: int, humid_air_now: int, 
                    status_temp: int,intensity_now:int, status_water:bool, status_water_air:bool, status_dehumid: bool):
        self.tree_id = tree_id # which tree
        self.mode = mode # 0 = manual, 1 = auto
        self.temp = temp # 0 - 100 celcius
        self.humid_soil = humid_soil # 0 - 100 % ## soil humidity
        self.humid_air = humid_air # 0 - 100 % ## air humidity
        self.color = color # "red", "green", "blue" ## color of RGB
        self.intensity = intensity # 0 - 100 ## RGB light intensity

        self.temp_now = temp_now # 0 - 100 celcius
        self.humid_soil_now = humid_soil_now # 0 - 100 % ## soil humidity
        self.humid_air_now = humid_air_now # 0 - 100 % ## air humidity
        self.intensity_now = intensity_now # 

        self.status_temp = status_temp # 0 = OFF, 1 = decrese_temp, 2 = increase_temp
        self.status_water = status_water # False = OFF, True = ON ## tree water
        self.status_humid = status_water_air # False = OFF, True = ON ## humidifier
        self.status_dehumid = status_dehumid # False = OFF, True = ON ## dehumid_humidifier
        

all_tree = []
for i in range(HOW_MANY_TREE):
    temp = Tree(i, 0, 25, 0, 0, "#ffffff", 0, 0, 0, 0, 0, 0, False, False, False)
    all_tree.append(temp)

app = FastAPI()

@app.get("/front")
def send_status(tree_id: int):
    all = []
    for i in all_tree:
        all.append({"tree_id": all_tree[tree_id].tree_id, "mode": all_tree[tree_id].mode, "temp" : all_tree[tree_id].temp, "humid_soil": all_tree[tree_id].humid_soil, "humid_air": all_tree[tree_id].humid_air, "color": all_tree[tree_id].color, "intensity": all_tree[tree_id].intensity,
                    "temp_now": all_tree[tree_id].temp_now, "humid_soil_now": all_tree[tree_id].humid_soil, "humid_air_now": all_tree[tree_id].humid_air_now, 
                    "intensity_now": all_tree[tree_id].intensity_now, "status_temp": all_tree[tree_id].status_temp, "status_water":all_tree[tree_id].status_water, "status_humid":all_tree[tree_id].status_humid, "status_dehumid": all_tree[tree_id].status_dehumid})
    return {"result": all}

@app.get("/hardware")
def send_status(tree_id: int):
    all = []
    for i in all_tree:
        all.append({"tree_id": all_tree[tree_id].tree_id,"status_temp": all_tree[tree_id].status_temp, "status_water":all_tree[tree_id].status_water, "status_humid":all_tree[tree_id].status_humid, "status_dehumid": all_tree[tree_id].status_dehumid})
    return {"result": all}

@app.put("/hardware_update")
def get_hardware_status(tree_id: int, temp_now: int, humid_soil_now: int, humid_air_now: int, intensity_now: int):
    all_tree[tree_id].temp_now = temp_now
    all_tree[tree_id].humid_soil_now = humid_soil_now
    return {"msg": "OK"}

@app.put("/set_mode")
def set_mode(tree_id: int, mode: Union[int, None] = None):
    if mode is None:
        if all_tree[tree_id].mode == 0:
            all_tree[tree_id].mode = 1
        else:
            all_tree[tree_id].mode = 0
    else:
        all_tree[tree_id].mode = mode
    return {"msg": "Changed Mode"}

@app.put("/set_intensity")
def set_intensity(tree_id: int, intensity: int):
    all_tree[tree_id].intensity = intensity
    return {"msg": "Changed intensity"}

@app.put("/set_temp")
def set_temp(tree_id: int, temp:int):
    all_tree[tree_id].temp = temp
    return {"msg": "set temp"}

@app.put("/set_color")
def set_color(tree_id: int, color:str):
    all_tree[tree_id].color = color
    return {"msg": "set color"}

@app.put("/set_humid_soil")
def set_humid_soil(tree_id: int, humid_soil:int):
    all_tree[tree_id].temp = humid_soil
    return {"msg": "set humid_soil"}

@app.put("/set_humid_air")
def set_humid_air(tree_id: int, humid_air:int):
    all_tree[tree_id].temp = humid_air
    return {"msg": "set humid_air"}


@app.put("/water")
def water(tree_id:int, status: bool):
    all_tree[tree_id].status_water = status
    return {"msg": "OK"}

@app.put("/humidnify")
def humidnify_air(tree_id:int, status: bool):
    all_tree[tree_id].status_humid = status
    return {"msg": "OK"}

@app.put("/dehumidify")
def dehumidify(tree_id: int, status: bool):
    all_tree[tree_id].status_dehumid = status
    return {"msg": "OK"}

@app.put("/AC")
def set_AC(tree_id: int, status: int):
    all_tree[tree_id].temp = status
    return {"msg": "OK"}