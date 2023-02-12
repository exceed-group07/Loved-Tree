import { useEffect, useState, useRef } from "react";
import FetchData from "../api/Fetchdata";
import "../styles/Status.css"


function Intensitystatus() {
    const [light, setLight] = useState(0)

    useEffect(() => {
        FetchData().then(result => setLight(result.result[0].status_intensity))
    })

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
      
            FetchData().then(result => setLight(result)) 
            
            
        
      }, 3000);


    return (
        <div className="intensity-div">
            <div>
                {light === 0 ? "Normal status" : light === 1 ? "Too dark" : "Too bright"}
            </div>
        </div>
    )
}

export default Intensitystatus