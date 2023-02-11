import {useState, useEffect, useRef} from 'react'
import "../styles/Monitor.css"
import rh from "../icons/rh.png"
import temp from "../icons/temp.png"
import sm from "../icons/sm.png"
import FetchData from "../api/Fetchdata"

function Monitors() {
    const [data,setData] = useState([])
    useEffect(() => {
        FetchData().then(result => setData(result)) 
        
        
    }, [])
    
    function useInterval(callback, delay) {
        const savedCallback = useRef();
    
        // Remember the latest callback.
        useEffect(() => {
          savedCallback.current = callback;
        }, [callback]);
    
        // Set up the interval.
        useEffect(() => {
          function tick() {
            savedCallback.current();
          }
          if (delay !== null) {
            let id = setInterval(tick, delay);
            return () => clearInterval(id);
          }
        }, [delay]);
      }
      useInterval(() => {
      
            FetchData().then(result => setData(result)) 
            
            
        
      }, 3000);

    return (
        <div className="monitor">
            <div className="DC">
                <div className="grid-container">
                    <div className="item1">{data?.result?.[0]?.temp_now}</div>
                    <div className="item2">℃</div>
                    <div className="item3"><img src={temp}/></div>
                    <div className="item4">Temperature</div>
                </div>
                <div className="grid-container">
                    <div className="item1">{data?.result?.[0]?.humid_air_now}</div>
                    <div className="item2">%RH</div>
                    <div className="item3"><img src={rh} /></div>
                    <div className="item4">Relative humidity</div>
                </div>
                <div className="grid-container">
                    <div className="item1">{data?.result?.[0].humid_soil_now}</div>
                    <div className="item2">LVL</div>
                    <div className="item3"><img src={sm} /></div>
                    <div className="item4">Soil moisture</div>
                </div>
            </div>
        </div>
    )

}

export default Monitors