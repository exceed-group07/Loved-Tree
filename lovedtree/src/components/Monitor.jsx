import {useState, useEffect} from 'react'
import "../styles/Monitor.css"
import rh from "../icons/rh.png"
import temp from "../icons/temp.png"
import sm from "../icons/sm.png"
import FetchData from "../api/Fetchdata"

function Monitors() {
    // const [data, setData] = useState({result:[{temp_now:0}]})
    const [data,setData] = useState([])
    useEffect(() => {
        FetchData().then(result => setData(result)) 
        
        
    }, [])

    return (
        <div className="monitor">
            <div className="DC">
                <div className="grid-container">
                    <div className="item1">{data?.result?.[0]?.temp_now}</div>
                    <div className="item2">℃</div>
                    <div className="item3"><img src={temp}/></div>
                    <div className="item4">temperature</div>
                </div>
                <div className="grid-container">
                    <div className="item1">{data?.result?.[0]?.humid_soil_now}</div>
                    <div className="item2">%RH</div>
                    <div className="item3"><img src={rh} /></div>
                    <div className="item4">relative humidity</div>
                </div>
                <div className="grid-container">
                    <div className="item1">1</div>
                    <div className="item2">LVL</div>
                    <div className="item3"><img src={sm} /></div>
                    <div className="item4">soil moisture</div>
                </div>
            </div>
        </div>
    )

}

export default Monitors