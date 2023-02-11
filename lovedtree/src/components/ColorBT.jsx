import { useEffect, useState } from "react"
import "../styles/ColorBT.css"
import FetchData from "../api/Fetchdata"
import axios from "axios"

function ColorBT() {
    const [status, setStatus] = useState()
    const [finish,setFinish] = useState(false)
    
    useEffect(() => {
        FetchData().then(result => {setStatus(result.result[0].color)
        setFinish(true)})

    }, [status])

    const handleOptionChange = (e) => {
        const newColor= e.target.value;
        axios.put('http://group7.exceed19.online/set_color', null, {
            params: {
                tree_id: 0,
                color : newColor
            }
        }).then(response => {
            setStatus(newColor);
        }).catch(error => {
            console.error(error);
        });
    };
    return (
        <fieldset id="colorBT" class="colorBT">
            {finish&&<div>

            <input name="colorBT" value={0} id="red" type="radio" defaultChecked={status === 0} onChange={handleOptionChange}></input>
            <label for="red"></label>
            <input name="colorBT" value={1} id="green" type="radio" defaultChecked={status === 1} onChange={handleOptionChange}></input>
            <label for="green"></label>
            <input name="colorBT" value={2} id="blue" type="radio" defaultChecked={status === 2} onChange={handleOptionChange}></input>
            <label for="blue"></label>
            </div>
            }
        </fieldset>
    )
}

export default ColorBT