from fastapi import FastAPI, Body, HTTPException
from typing import Union
import requests

HOW_MANY_TREE = 2

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

app = FastAPI()

def update_status():
    for tree in all_tree:
        tree:Tree         
        if tree.mode == 0:
            if tree.temp_now - tree.temp_manual > 5:
                tree.status_temp = 1
            elif tree.temp_now - tree.temp_manual < -5:
                tree.status_temp = 2
            else:
                tree.status_temp = 0
            return

        if tree.temp_now - tree.temp_auto > 5:
            tree.status_temp = 1
        elif tree.temp_now - tree.temp_auto < -5:
            tree.status_temp = 2
        else:
            tree.status_temp = 0
        
        if tree.humid_air_now - tree.humid_air > 5:
            tree.status_humid = False
            tree.status_dehumid = True
        elif tree.humid_air_now - tree.humid_air < -5:
            tree.status_humid = True
            tree.status_dehumid = False
        else:
            tree.status_humid = False
            tree.status_dehumid = False

        
        if tree.humid_soil_now - tree.humid_soil > 5:
            tree.status_water = False
        elif tree.humid_soil_now - tree.humid_soil < -5:
            tree.status_water = True
        else:
            tree.status_water = False


for i in range(HOW_MANY_TREE):
    temp = Tree(i, 1, 25, 25, 50, 50, "#ffffff", 100, 25, 50, 50, 0, 100, False, False, False)
    all_tree.append(temp)

@app.get("/")
def welcome():
    return "<html><title>Loved Tree</title><head></head><body><h1>😭😭😭😭Welcome😭😭😭😭</h1><div>😭😭😭😭Welcome😭😭😭😭</div></body></html>"

@app.get("/front")
def send_status_front():
    update_status()
    all = []
    for tree in all_tree:
        tree:Tree
        all.append({"tree_id": tree.tree_id, "mode": tree.mode, "temp_manual" : tree.temp_manual, "temp_auto" : tree.temp_auto, "humid_soil": tree.humid_soil, "humid_air": tree.humid_air, "color": tree.color, "intensity": tree.intensity,
                    "temp_now": tree.temp_now, "humid_soil_now": tree.humid_soil_now, "humid_air_now": tree.humid_air_now, 
                    "intensity_now": tree.intensity_now, "status_temp": tree.status_temp, "status_water": tree.status_water, "status_humid": tree.status_humid, "status_dehumid": tree.status_dehumid})
    return {"result": all}

@app.get("/hardware")
def send_status_hardware():
    update_status()
    all = []
    for tree in all_tree:
        tree:Tree
        all.append({"tree_id": tree.tree_id,"status_temp": tree.status_temp, "status_water":tree.status_water, "status_humid":tree.status_humid, "status_dehumid": tree.status_dehumid})
    return {"result": all}

@app.put("/hardware_update")    
def get_hardware_status(tree_id: int, temp_now: int, humid_soil_now: int, humid_air_now: int, intensity_now: int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    x.temp_now = temp_now
    x.humid_soil_now = humid_soil_now
    x.humid_air_now = humid_air_now
    x.intensity_now = intensity_now

    return {"msg": "Update Complete"}


@app.put("/set_mode")
def set_mode(tree_id: int, mode: Union[int, None] = None):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    if mode is None:
        if x.mode == 0:
            x.mode = 1
        else:
            x.mode = 0
    elif mode in range(2):
        x.mode = mode
    else:
        raise HTTPException(status_code=400, detail = "mode only have 0(manaul) or 1(auto)")
    return {"msg": "Changed Mode"}

@app.put("/set_intensity")
def set_intensity(tree_id: int, intensity: int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    x.intensity = intensity
    return {"msg": "Changed intensity"}

@app.put("/set_color") ## wait color from frontend
def set_color(tree_id: int, color:str):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    x.color = color
    return {"msg": "set color"}

@app.put("/set_temp_manual")
def set_temp(tree_id: int, temp:int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    if (x.mode == 1):
        raise HTTPException(status_code=400, detail = "cant set temp_manual in auto mode")
    x.temp_manual = temp
    return {"msg": "set temp_manual"}

@app.put("/set_temp_auto")
def set_AC(tree_id: int, temp: int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    if (x.mode == 0):
        raise HTTPException(status_code=400, detail = "cant set temp_auto in manual mode")
    x.temp_auto = temp
    return {"msg": "set temp_auto"}

@app.put("/set_humid_soil")
def set_humid_soil(tree_id: int, humid_soil:int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    if (x.mode == 0):
        raise HTTPException(status_code=400, detail = "cant set humid_soil in manual mode")
    x.humid_soil = humid_soil
    return {"msg": "set humid_soil"}

@app.put("/set_humid_air")
def set_humid_air(tree_id: int, humid_air:int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    if (x.mode == 0):
        raise HTTPException(status_code=400, detail = "cant set humid_air in manual mode")
    x.humid_air = humid_air
    return {"msg": "set humid_air"}

@app.put("/water")
def water(tree_id:int, status: Union[bool, None] = None):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    if (x.mode == 1):
        raise HTTPException(status_code=400, detail = "cant manually water in auto mode")
    if status is None:
        if x.status_water == False:
            x.status_water = True
        else:
            x.status_water = False
    else:
        x.status_water = status

    if x.status_water:
        return {"msg": "WATER ON"}
    return {"msg": "WATER OFF"}

@app.put("/humidnify")
def humidnify_air(tree_id:int, status: Union[bool, None] = None):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    if (x.mode == 1):
        raise HTTPException(status_code=400, detail = "cant humidify in auto mode")
    if status is None:
        if x.status_humid == False:
            x.status_humid = True
        else:
            x.status_humid = False
    else:
        x.status_humid = status

    if x.status_humid:
        return {"msg": "HUMIDIFIER ON"}
    return {"msg": "HUMIDIFIER OFF"}

@app.put("/dehumidify")
def dehumidify(tree_id: int, status: Union[bool, None] = None):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    x = all_tree[tree_id]
    x: Tree
    if (x.mode == 1):
        raise HTTPException(status_code=400, detail = "cant dehumidify in auto mode")
    if status is None:
        if x.status_dehumid == False:
            x.status_dehumid = True
        else:
            x.status_dehumid = False
    else:
        x.status_dehumid = status

    if x.status_dehumid:
        return {"msg": "DEHUMIDIFIER ON"}
    return {"msg": "DEHUMIDIFIER OFF"}

#@app.put("/disco")
#def disco():
    #for ai in range() :
    #x = requests.get("http://group7.exceed19.online/front")
    #return (x.json)

@app.get("/rachata")
def emoji():
    for i in range(100):
        print("😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭")
    return "😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭"

            

        


