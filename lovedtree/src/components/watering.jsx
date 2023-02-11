import spray from "../icons/spray.png"
import watering from "../icons/watering.png"
import "../styles/watering.css"
import {useState, useEffect} from 'react'

import axios from "axios"

function Watering(props) {
    const {status, humid, st, plant,tree,water_status,sprinkle_status} = props
    const [water, setWaters] = useState({
        status: Boolean
    })
    const [humids, setHumid] = useState({
        status_dehumid : Boolean
    })
    

    const handleOptionChange = (e) => {
        const newHumid = e.target.value; 
        let status_test = false
        if (newHumid === 'dry'){
            status_test = true
        }
        axios.put('http://group7.exceed19.online/dehumidify', null, {
            params: {
                tree_id: 0,
                status: status_test
            }
        }).then(response => {
          setHumid(newHumid);
          st(newHumid)
          console.log(newHumid)
        }).catch(error => {
          console.error(error);
        });
      };

      const handleStatusChange = (e) => {
        const newWater = !water_status; 
        axios.put('http://group7.exceed19.online/humidnify', null, {
            params: {
                tree_id: 0,
                status : newWater
            }
        }).then(response => {
          plant(newWater)
          console.log(newWater)
        }).catch(error => {
          console.error(error);
        });
      };

      const handleStatusChange2 = (e) => {
        const newSprinkle = !sprinkle_status; 
        axios.put('http://group7.exceed19.online/water', null, {
            params: {
                tree_id: 0,
                status : newSprinkle
            }
        }).then(response => {
          tree(newSprinkle)
          console.log(newSprinkle)
        }).catch(error => {
          console.error(error);
        });
      };

      
    return (
        <div>
            <div onClick={handleStatusChange} class="circle1" style={{background: water_status ? "#2B56FB" : "#FFFFFF"}}><img src={spray} /></div>
            <div onClick={handleStatusChange2} class ="circle2" style={{background: sprinkle_status ? "#2B56FB" : "#FFFFFF"}}><img src={watering} /></div>
            <div class="DWbt">
                <fieldset id="DW" class="radio">
                    <input name="DW" id="dry" type="radio" disabled={!status}  defaultChecked={humid} onChange={handleOptionChange} value='dry'></input>
                    <label for="dry">DRY</label>
                    <input name="DW" id="normal" type="radio" disabled={!status} defaultChecked={!humid} onChange={handleOptionChange} value='normal'></input>
                    <label for="normal">NORMAL</label>
                </fieldset>
            </div>
        </div>
    )
}

export default Watering