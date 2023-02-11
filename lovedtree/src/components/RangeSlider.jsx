import React, { useState } from "react";
import "../styles/RangeSlider.css";
const RangeSlider = () => {
    const [value, setValue] = useState(50);

    return (
        <div>
            <input
                type="range"
                min="0"
                max="100"
                value={value}
                onChange={(event) => setValue(event.target.value)}
                className='slider'
            />
        </div>
    );
};

export default RangeSlider;