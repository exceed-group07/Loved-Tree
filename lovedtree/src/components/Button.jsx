import "../styles/Mode_BT.css"
import {useState, useEffect} from 'react'
import FetchData from "../api/Fetchdata"

function ModeBT() {
    const [status, setStatus] = useState(0)
    useEffect(() => {
        FetchData().then(result => setStatus(result.result[0].mode))
        
    }, [status])

    const handleOptionChange = (e) => {
    }
    return (
        <div class="autoBT">
            <fieldset id="switch" class="radio">
                <input name="switch" id="auto" value="1" type="radio" onChange={handleOptionChange} defaultChecked={status === 1}></input>
                <label for="auto">AUTO</label>
                <input name="switch" id="manual" value="0" type="radio" onChange={handleOptionChange} defaultChecked={status === 0}></input>
                <label for="manual">MANUAL</label>
            </fieldset>
        </div>
    )
}

export default ModeBT