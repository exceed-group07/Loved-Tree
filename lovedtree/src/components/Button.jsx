import "../styles/Mode_BT.css"
import {useState, useEffect} from 'react'
import FetchData from "../api/Fetchdata"
import axios from "axios"




function ModeBT(props) {
    const [status, setStatus] = useState(0)
    const {button}  = props
    
   
    useEffect(() => { 
        FetchData().then(result => setStatus(result.result[0].mode))
    }, [status])

    const handleOptionChange = (e) => {
        const newStatus = e.target.value; 
        axios.put('http://group7.exceed19.online/set_mode', null, {
            params: {
                tree_id: 0,
                mode: newStatus
            }
        }).then(response => {
          setStatus(newStatus);
          button(newStatus)
        }).catch(error => {
          console.error(error);
        });
      };

    return (
        <div class="autoBT">
            <fieldset id="switch" class="radio">
                <input name="switch" id="auto" value={1} type="radio" onChange={handleOptionChange} defaultChecked={status === 1}></input>
                <label for="auto">AUTO</label>
                <input name="switch" id="manual" value={0} type="radio" onChange={handleOptionChange} defaultChecked={status === 0}></input>
                <label for="manual">MANUAL</label>
            </fieldset>
        </div>
    )
}

export default ModeBT