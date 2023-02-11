import Manualbar from "../components/Manualbar"
import IPBar from "../components/Inputbar"
import ModeBT from "../components/Button"
import Monitors from "../components/Monitor"
import ColorBT from "../components/ColorBT"
import Watering from "../components/watering"
import "../styles/Mode_BT.css"
import "../styles/Menu.css"
import RangeSlider from "../components/RangeSlider"
import { useEffect, useState } from "react"
import FetchData from "../api/Fetchdata"

// 
function Menu() {
    const [data, setData] = useState([])
    const [button, setButton] = useState(true)
    const [humid, setHumid] = useState(true)
    const [water, setWater] = useState(true)
    const [sprinkle, setSprinkle] = useState(true)


    

    useEffect( () => {
        FetchData().then(result => {setData(result)
            result.result.mode == 1 ? setButton(false) : setButton(true) 
            setHumid(result.result.status_dehumid)
            })
    },[])


    const input = (val) => {
        val == 1 ? setButton(false) : setButton(true)
    }

    const status = (bool) => {

        bool == "dry" ? setHumid(true) : setHumid(false)
        console.log(humid)
    }

    const plants = (waters) => {
        waters ? setWater(true) : setWater(false)
    }

    const tree = (w) => {
        w ? setSprinkle(true) : setSprinkle(false)
    }

   
    


    

    return (
        <div>
            <Monitors></Monitors>
            <br></br>
            <div class="control-panel">
                <div>
                    <ModeBT button={input}></ModeBT>
                </div>
                <div class="color-select">
                    <ColorBT></ColorBT>
                </div>
                <div><RangeSlider /></div>
            </div>
            <div className="lower">
                <div className={button ? "disabled" : null}>
                <IPBar opposite={button}/>
                </div>
               
                <div class="line"></div>
                <div className={button ? null : "disabled"}>
                <Watering status={button} humid={humid} st={status} plant={plants} tree={tree} water_status={water} sprinkle_status={sprinkle}/>
                </div>
                
                <div className={`man-temp ${button ? null : "disabled"}`} >
                    <Manualbar manual={button} />
                </div>
            </div>
        </div>
    )

}

export default Menu