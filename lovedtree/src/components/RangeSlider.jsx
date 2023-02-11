import React, { useState, useEffect } from "react";
import "../styles/RangeSlider.css";
import FetchData from "../api/Fetchdata";
import axios from "axios";
const RangeSlider = () => {
    const [value, setValue] = useState(50);
    var t
    useEffect(() => {
        FetchData().then(result => setValue(result.result[0].intensity))

    }, [])



    const handleOptionChange = (e) => {
        setValue(e.target.value);
        const newIntensity = e.target.value;
        axios.put('http://group7.exceed19.online/set_intensity', null, {
            params: {
                tree_id: 0,
                intensity : newIntensity
            }
        }).then(response => {
            console.log(newIntensity)
            setValue(e.target.value);
        }).catch(error => {
            console.error(error);
        });
    };
    return (
        <div>
            <input
                type="range"
                min="0"
                step="5"
                max="100"
                value={value}
                onChange={handleOptionChange}
                className='slider'
                
            />
        </div>
    );
};

export default RangeSlider;