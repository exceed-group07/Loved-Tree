import { useEffect, useState } from "react"
import "../styles/ColorBT.css"
import FetchData from "../api/Fetchdata"

function ColorBT() {
    const [status, setStatus] = useState("")
 useEffect(() => {
        FetchData().then(result => setStatus(result.result[0].color))

    }, [status])
    return (
        <fieldset id="colorBT" class="colorBT">
            <input name="colorBT" id="red" type="radio" defaultChecked={status === "#ff0000"}></input>
            <label for="red"></label>
            <input name="colorBT" id="green" type="radio" defaultChecked={status === "#78eb65"}></input>
            <label for="green"></label>
            <input name="colorBT" id="blue" type="radio" defaultChecked={status === "#2b56fb"}></input>
            <label for="blue"></label>
        </fieldset>
    )
}

export default ColorBT