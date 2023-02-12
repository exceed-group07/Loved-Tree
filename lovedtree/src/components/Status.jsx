import { useEffect, useState } from "react";
import FetchData from "../api/Fetchdata";
import "../styles/Status.css"


function Intensitystatus() {
    const [light, setLight] = useState(0)

    useEffect(() => {
        FetchData().then(result => setLight(result.result[0].status_intensity))
    })


    return (
        <div className="intensity-div">
            <div>
                {light == 0 ? "Normal status" : light == 1 ? "Too dark" : "Too bright"}
            </div>
        </div>
    )
}

export default Intensitystatus