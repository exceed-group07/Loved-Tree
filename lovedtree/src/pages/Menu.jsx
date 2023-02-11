import Manualbar from "../components/Manualbar"
import IPBar from "../components/Inputbar"
import ModeBT from "../components/Button"
import Monitors from "../components/Monitor"
import ColorBT from "../components/ColorBT"
import Watering from "../components/watering"
import "../styles/Mode_BT.css"
import "../styles/Menu.css"
import RangeSlider from "../components/RangeSlider"
function Menu() {

    return (
        <div>
            <Monitors></Monitors>
            <br></br>
            <div class="control-panel">
                <div>
                    <ModeBT></ModeBT>
                </div>
                <div class="color-select">
                    <ColorBT></ColorBT>
                </div>
                <div><RangeSlider /></div>
            </div>
            <div class="lower">
                <IPBar />
                <div class="line"></div>
                <Watering />
                <div className="man-temp">
                    <Manualbar />
                </div>
            </div>
        </div>
    )

}

export default Menu