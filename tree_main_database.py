from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pymongo import MongoClient
from pydantic import BaseModel

from dotenv import load_dotenv
import os
import urllib

load_dotenv('.env')
user = os.getenv('usernames')
password = urllib.parse.quote(os.getenv('password'))

DATABASE_NAME = "exceed07"
COLLECTION_NAME = "LOVED-TREE"

MONGO_DB_URL = f"mongodb://{user}:{urllib.parse.quote(password)}@mongo.exceed19.online:8443/?authMechanism=DEFAULT"
MONGO_DB_PORT = 8443

client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}")
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

HOW_MANY_TREE = 1

class Tree(BaseModel):
    tree_id: int # which tree
    mode: int # 0 = manual, 1 = auto
    temp_manual: int # 0 - 100 celcius
    temp_auto: int # 0 - 100 celcius
    humid_soil: int ######################################33
    humid_air: int # 0 - 100 % ## air humidity
    color: int # 0 = "red", 1 = "green", 2 = "blue" ## color of RGB
    intensity: int # 0 - 100 ## RGB light intensity
    temp_now: int # 0 - 100 celcius
    humid_soil_now: int ####################################
    humid_air_now: int # 0 - 100 % ## air humidity
    intensity_now: int #
    status_temp:int # 0 = OFF, 1 = decrese_temp, 2 = increase_temp
    status_water:bool # False = OFF, TTrue = ON ## humidifier
    status_dehumid:bool # False = OFF, True = ON ## dehumid_humidifier
    status_humid: bool # False = OFF, 
    status_intensity: int

app = FastAPI()

origins = ["*"]# allow everyone
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

all_tree = []

def update_status():
    for i in collection.find({}):
        x = dict(i)  
        if x["mode"] == 0:
            if x["temp_now"] - x["temp_manual"] > 3:
                x["status_temp"] = 1
            elif x["temp_now"] - x["temp_manual"] < -3:
                x["status_temp"] = 2
            else:
                x["status_temp"] = 0
            collection.update_one({"tree_id": x["tree_id"]}, {"$set": {"status_temp": x["status_temp"]}})
            return

        if x["temp_now"] - x["temp_auto"] > 3:
            x["status_temp"] = 1
        elif x["temp_now"] - x["temp_auto"] < -3:
            x["status_temp"] = 2
        else:
            x["status_temp"] = 0
        
        if x["humid_air_now"] - x["humid_air"] > 5:
            x["status_humid"] = False
            x["status_dehumid"] = True
        elif x["humid_air_now"] - x["humid_air"] < -5:
            x["status_humid"] = True
            x["status_dehumid"] = False
        else:
            x["status_humid"] = False
            x["status_dehumid"] = False

        if x["humid_soil_now"] - x["humid_soil"] > 0:
            x["status_water"] = True
        else:
            x["status_water"] = False

        if x["intensity_now"] - x["intensity"] > 20:
            x["status_intensity"] = 2
        elif x["intensity_now"] - x["intensity"] < -20:
            x["status_intensity"] = 1
        else:
            x["status_intensity"] = 0

        collection.update_one({"tree_id": x["tree_id"]}, {"$set": { "status_temp": x["status_temp"], 
                                                                    "status_humid": x["status_humid"],
                                                                    "status_dehumid": x["status_humid"],
                                                                    "status_water": x["status_water"],
                                                                    "status_intensity": x["status_intensity"]}})

def init():
    for i in range(HOW_MANY_TREE):
        collection.insert_one({
        "tree_id": i,
        "mode": 1,
        "temp_manual": 25,
        "temp_auto": 25,
        "humid_soil": 5,
        "humid_air": 50,
        "color": 0,
        "intensity": 100,
        "temp_now": 25,
        "humid_soil_now": 50,
        "humid_air_now": 50,
        "intensity_now": 0,
        "status_temp": 100,
        "status_water": False,
        "status_humid": False,
        "status_dehumid": False,
        "status_intensity": 0
    })

collection.delete_many({})
init()

@app.get("/front")
def send_status_front():
    update_status()
    all = []
    for i in collection.find({}, {"_id": 0}):
        all.append(dict(i))
    return {"result": all}

@app.get("/hardware")
def send_status_hardware():
    update_status()
    all = []
    for i in collection.find({}, {"_id": 0}):
        x = dict(i)
        all.append({"tree_id": x["tree_id"], "status_temp": x["status_temp"], "status_water": int(x["status_water"]), "status_humid": int(x["status_humid"]), 
                    "status_dehumid": int(x["status_dehumid"]), "intensity": x["intensity"], "color": x["color"], "status_intensity": x["status_intensity"]})
    return all[0]
    #return {"result": all}

@app.put("/hardware_update")    
def get_hardware_status(tree_id = Body(), temp_now = Body(), humid_soil_now = Body(), humid_air_now = Body(), intensity_now = Body()):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")

    x = collection.find_one({"tree_id": tree_id}, {"_id": 0})
    if x == None:
        raise HTTPException(status_code=400, detail = f"Dont have this {tree_id} tree_id")
    x = dict(x)

    if(humid_soil_now >= 4000):
        x["humid_soil_now"] = 0
    elif humid_soil_now == 0:
        x["humid_soil_now"] = 9
    else:
        x["humid_soil_now"] = int((4000-humid_soil_now)//400)

    collection.update_one({"tree_id": tree_id}, {"$set": {  "temp_now": temp_now, 
                                                            "humid_soil_now": x["humid_soil_now"], ####### x.humid_soil_now 0-9 higher is wetter#
                                                            "humid_air_now": humid_air_now, 
                                                            "intensity_now": intensity_now}})
    return {"msg": "Update Complete"}

@app.put("/set_mode")
def set_mode(tree_id: int, mode: Union[int, None] = None):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")

    x = dict(collection.find_one({"tree_id": tree_id}, {"_id": 0}))
    if mode is None:
        if x["mode"] == 0:
            x["mode"] = 1
        else:
            x["mode"] = 0
    elif mode in range(2):
        x["mode"] = mode
    else:
        raise HTTPException(status_code=400, detail = "mode only have 0(manaul) or 1(auto)")
    
    collection.update_one({"tree_id": tree_id}, {"$set": {"mode": x["mode"]}})
    return {"msg": "Changed Mode"}

@app.put("/set_intensity")
def set_intensity(tree_id: int, intensity: int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    collection.update_one({"tree_id": tree_id}, {"$set": {"intensity": intensity}})
    return {"msg": "Changed intensity"}

@app.put("/set_color")
def set_color(tree_id: int, color:int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    collection.update_one({"tree_id": tree_id}, {"$set": {"color": color}})
    return {"msg": "set color"}

@app.put("/set_temp_manual")
def set_temp(tree_id: int, temp:int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")

    x = dict(collection.find_one({"tree_id": tree_id}, {"_id": 0}))
    if (x["mode"] == 1):
        raise HTTPException(status_code=400, detail = "cant set temp_manual in auto mode")
    collection.update_one({"tree_id": tree_id}, {"$set": {"temp_manual": temp}})
    return {"msg": "set temp_manual"}

@app.put("/set_temp_auto")
def set_AC(tree_id: int, temp: int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")

    x = dict(collection.find_one({"tree_id": tree_id}, {"_id": 0}))
    if (x["mode"] == 0):
        raise HTTPException(status_code=400, detail = "cant set temp_auto in manual mode")
    collection.update_one({"tree_id": tree_id}, {"$set": {"temp_auto": temp}})
    return {"msg": "set temp_auto"}

@app.put("/set_humid_soil")
def set_humid_soil(tree_id: int, humid_soil:int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")

    x = dict(collection.find_one({"tree_id": tree_id}, {"_id": 0}))
    if (x["mode"] == 0):
        raise HTTPException(status_code=400, detail = "cant set humid_soil in manual mode")
    collection.update_one({"tree_id": tree_id}, {"$set": {"humid_soil": humid_soil}})
    return {"msg": "set humid_soil"}

@app.put("/set_humid_air")
def set_humid_air(tree_id: int, humid_air:int):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")

    x = dict(collection.find_one({"tree_id": tree_id}, {"_id": 0}))
    if (x["mode"] == 0):
        raise HTTPException(status_code=400, detail = "cant set humid_air in manual mode")
    collection.update_one({"tree_id": tree_id}, {"$set": {"humid_air": humid_air}})
    return {"msg": "set humid_air"}

@app.put("/water")
def water(tree_id:int, status: Union[bool, None] = None):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    
    x = dict(collection.find_one({"tree_id": tree_id}, {"_id": 0}))
    if (x["mode"] == 1):
        raise HTTPException(status_code=400, detail = "cant manually water in auto mode")
    if status is None:
        if x["status_water"] == False:
            x["status_water"] = True
        else:
            x["status_water"] = False
    else:
        x["status_water"] = status

    collection.update_one({"tree_id": tree_id}, {"$set": {"status_water": x["status_water"]}})

    if x["status_water"]:
        return {"msg": "WATER ON"}
    return {"msg": "WATER OFF"}

@app.put("/humidnify")
def humidnify_air(tree_id:int, status: Union[bool, None] = None):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")

    x = dict(collection.find_one({"tree_id": tree_id}))
    if (x["mode"] == 1):
        raise HTTPException(status_code=400, detail = "cant humidify in auto mode")
    if status is None:
        if x["status_humid"] == False:
            x["status_humid"] = True
        else:
            x["status_humid"] = False
    else:
        x["status_humid"] = status

    collection.update_one({"tree_id": tree_id}, {"$set": {"status_humid": x["status_humid"]}})

    if x["status_humid"]:
        return {"msg": "HUMIDIFIER ON"}
    return {"msg": "HUMIDIFIER OFF"}

@app.put("/dehumidify")
def dehumidify(tree_id: int, status: Union[bool, None] = None):
    if tree_id not in range(HOW_MANY_TREE):
        raise HTTPException(status_code=400, detail = f"Only Have {HOW_MANY_TREE} tree(s)")
    
    x = dict(collection.find_one({"tree_id": tree_id}, {"_id": 0}))
    if (x["mode"] == 1):
        raise HTTPException(status_code=400, detail = "cant dehumidify in auto mode")
    if status is None:
        if x["status_dehumid"] == False:
            x["status_dehumid"] = True
        else:
            x["status_dehumid"] = False
    else:
        x["status_dehumid"] = status

    collection.update_one({"tree_id": tree_id}, {"$set": {"status_dehumid": x["status_dehumid"]}})

    if x["status_dehumid"]:
        return {"msg": "DEHUMIDIFIER ON"}
    return {"msg": "DEHUMIDIFIER OFF"}