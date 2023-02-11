import spray from "../icons/spray.png"
import watering from "../icons/watering.png"
import "../styles/watering.css"

function Watering() {
    return (
        <div>
            <div class="circle1"><img src={spray} /></div>
            <div class="circle2"><img src={watering} /></div>
            <div class="DWbt">
                <fieldset id="DW" class="radio">
                    <input name="DW" id="dry" type="radio"></input>
                    <label for="dry">DRY</label>
                    <input name="DW" id="normal" type="radio"></input>
                    <label for="normal">NORMAL</label>
                </fieldset>
            </div>
        </div>
    )
}

export default Watering