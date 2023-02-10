from fastapi import FastAPI, Body, HTTPException
from typing import Union, Optional
from pydantic import BaseModel

HOW_MANY_TREE = 1

class Tree:
    def __init__(   self, tree_id: int, mode: int, temp_manual : int, temp_auto: int, humid_soil: int, humid_air: int, color: str, intensity: int,
                    temp_now: int, humid_soil_now: int, humid_air_now: int, 
                    status_temp: int,intensity_now:int, status_water:bool, status_water_air:bool, status_dehumid: bool):
        self.tree_id = tree_id # which tree
        self.mode = mode # 0 = manual, 1 = auto
        self.temp_manual = temp_manual # 0 - 100 celcius
        self.temp_auto = temp_auto # 0 - 100 celcius
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
    temp = Tree(i, 1, 25, 25, 0, 0, "#ffffff", 0, 0, 0, 0, 0, 0, False, False, False)
    all_tree.append(temp)

app = FastAPI()

def update_status():
    for i in all_tree:
        if i.mode == 0:
            if i.temp_now - i.temp_manual > 5:
                i.status_temp = 1
            else:
                i.status_temp = 2
            return

        if i.temp_now - i.temp_auto > 5:
            i.status_temp = 1
        elif i.temp_now - i.temp_auto < 5:
            i.status_temp = 2
        else:
            i.status_temp = 0
        
        if i.humid_air_now - i.humid_air > 5:
            i.status_humid = False
            i.status_dehumid = True
        elif i.humid_air_now - i.humid_air < 5:
            i.status_humid = True
            i.status_dehumid = False
        else:
            i.status_humid = False
            i.status_dehumid = False

        
        if i.humid_soil_now - i.humid_soil >= 5:
            i.status_water = False
        else:
            i.status_water = True


@app.get("/front")
def send_status():
    update_status()
    all = []
    for i in all_tree:
        all.append({"tree_id": i.tree_id, "mode": i.mode, "temp_manual" : i.temp_manual, "temp_auto" : i.temp_auto, "humid_soil": i.humid_soil, "humid_air": i.humid_air, "color": i.color, "intensity": i.intensity,
                    "temp_now": i.temp_now, "humid_soil_now": i.humid_soil, "humid_air_now": i.humid_air_now, 
                    "intensity_now": i.intensity_now, "status_temp": i.status_temp, "status_water": i.status_water, "status_humid": i.status_humid, "status_dehumid": i.status_dehumid})
    return {"result": all}

@app.get("/hardware")
def send_status():
    update_status()
    all = []
    for i in all_tree:
        all.append({"tree_id": i.tree_id,"status_temp": i.status_temp, "status_water":i.status_water, "status_humid":i.status_humid, "status_dehumid": i.status_dehumid})
    return {"result": all}

@app.put("/hardware_update")
def get_hardware_status(tree_id: int, temp_now: int, humid_soil_now: int, humid_air_now: int, intensity_now: int):
    all_tree[tree_id].temp_now = temp_now
    all_tree[tree_id].humid_soil_now = humid_soil_now
    all_tree[tree_id].humid_air_now = humid_air_now
    all_tree[tree_id].intensity_now = intensity_now

    return {"msg": "Update Complete"}


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

@app.put("/set_color") ## wait color from frontend
def set_color(tree_id: int, color:str):
    all_tree[tree_id].color = color
    return {"msg": "set color"}

@app.put("/set_temp_manual")
def set_temp(tree_id: int, temp:int):
    if (all_tree[tree_id].mode == 1):
        raise HTTPException(status_code=400, detail = "cant set temp_manual in auto mode")
    all_tree[tree_id].temp_manual = temp
    return {"msg": "set temp_manual"}

@app.put("/set_temp_auto")
def set_AC(tree_id: int, temp: int):
    if (all_tree[tree_id].mode == 0):
        raise HTTPException(status_code=400, detail = "cant set temp_auto in manual mode")
    all_tree[tree_id].temp_auto = temp
    return {"msg": "set temp_auto"}

@app.put("/set_humid_soil")
def set_humid_soil(tree_id: int, humid_soil:int):
    if (all_tree[tree_id].mode == 0):
        raise HTTPException(status_code=400, detail = "cant set humid_soil in manual mode")
    all_tree[tree_id].humid_soil = humid_soil
    return {"msg": "set humid_soil"}

@app.put("/set_humid_air")
def set_humid_air(tree_id: int, humid_air:int):
    if (all_tree[tree_id].mode == 0):
        raise HTTPException(status_code=400, detail = "cant set humid_air in manual mode")
    all_tree[tree_id].humid_air = humid_air
    return {"msg": "set humid_air"}

@app.put("/water")
def water(tree_id:int, status: bool):
    if (all_tree[tree_id].mode == 1):
        raise HTTPException(status_code=400, detail = "cant manually water in auto mode")
    all_tree[tree_id].status_water = status
    return {"msg": "OK"}

@app.put("/humidnify")
def humidnify_air(tree_id:int, status: bool):
    if (all_tree[tree_id].mode == 1):
        raise HTTPException(status_code=400, detail = "cant humidify in auto mode")
    all_tree[tree_id].status_humid = status
    return {"msg": "OK"}

@app.put("/dehumidify")
def dehumidify(tree_id: int, status: bool):
    if (all_tree[tree_id].mode == 1):
        raise HTTPException(status_code=400, detail = "cant dehumidify in auto mode")
    all_tree[tree_id].status_dehumid = status
    return {"msg": "OK"}
