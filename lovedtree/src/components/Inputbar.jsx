import rh from "../icons/rh.png"
import temp from "../icons/temp.png"
import sm from "../icons/sm.png"
import "../styles/InputBar.css"
import { useState } from "react"
import axios from "axios"
const URL = "http://group7.exceed19.online"
function IPBar(props) {
    const {opposite} = props
    const [inputs, setInputs] = useState({
        temperature: "",
        rh: "",
        soilMoisture: "",
    });

    const handleInputChange = (event) => {
        setInputs({
            ...inputs,
            [event.target.name]: event.target.value,
        });
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(inputs);
        axios.put(URL+"/set_temp_auto?tree_id=0&temp="+inputs.temperature)
            .then(res => {
                console.log(res);
                console.log(res.data);
            })
            axios.put(URL+"/set_humid_air?tree_id=0&humid_air="+inputs.rh)
            .then(res => {
                console.log(res);
                console.log(res.data);
            })

            axios.put(URL+"/set_humid_soil?tree_id=0&humid_soil="+inputs.soilMoisture)
            .then(res => {
                console.log(res);
                console.log(res.data);
            })
            event.target[0].value = ""
            event.target[1].value = ""
            event.target[2].value = ""
    }

    return (
        <form class="auto-def" onSubmit={handleSubmit}>
            <div class="grid-container1">
                <div class="item11"><img src={temp} /></div>
                <div class="item21">
                    <input type="number"
                        min="16"
                        step="1"
                        max="40"
                        class="input"
                        placeholder="Input here"
                        name="temperature"
                        onChange={handleInputChange} 
                        disabled={opposite}/></div>
                <div class="item31">Degree celsius</div>
            </div>
            <div class="grid-container1">
                <div class="item11"><img src={rh} /></div>
                <div class="item21"><input type="number" min="0" step="1" max="100" class="input" placeholder="Input here"
                    name="rh"
                    onChange={handleInputChange}
                    disabled={opposite}></input></div>
                <div class="item31">Percent RH</div>
            </div>
            <div class="grid-container1">
                <div class="item11"><img src={sm} /></div>
                <div class="item21"><input type="number" min="0" step="1" max="9" class="input" placeholder="Input here"
                    name="soilMoisture"
                    onChange={handleInputChange}
                    disabled={opposite}>
                    </input></div>
                <div class="item31">Soil moisture</div>
            </div>
            <div class="subBT">
                <button type="submit">SUBMIT</button>
            </div>
        </form>
    )
}

export default IPBar