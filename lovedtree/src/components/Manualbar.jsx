import "../styles/InputBar.css"
import temp from "../icons/temp.png"
import { useState } from "react";
import axios from "axios";
function Manualbar(props) {
    const { manual } = props
    const [inputs, setInputs] = useState({
        temperature: "",
    });

    const handleInputChange = (event) => {
        setInputs({
            ...inputs,
            [event.target.name]: event.target.value,
        });
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(event.target.value)
        console.log(inputs);
        axios.put(URL+"/set_temp_manual?tree_id=0&temp="+inputs.temperature)
            .then(res => {
                console.log(res);
                console.log(res.data);
            })
        event.target[0].value = ""
    }

    return (
        <div>
            <form class="grid-container1" onSubmit={handleSubmit}>
                <div class="item11"><img src={temp} /></div>
                <div class="item21"><input type="number" min="16" step="1" max="40" class="input" placeholder="Input here" 
                name='temperature'
                onChange={handleInputChange} disabled={!manual}></input></div>
                <div class="item31">degree celsius</div>
            <div class="subBT2">
                <button type="submit" disabled={!manual}>SUBMIT</button>
            </div>
            </form>
        </div>
    )
}

export default Manualbar