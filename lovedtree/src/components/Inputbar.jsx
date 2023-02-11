import rh from "../icons/rh.png"
import temp from "../icons/temp.png"
import sm from "../icons/sm.png"
import "../styles/InputBar.css"

function IPBar() {
    return (
        <div class="auto-def">
            <div class="grid-container1">
                <div class="item11"><img src={temp} /></div>
                <div class="item21"><input type="number" min="16" step="1" max="40" class="input" placeholder="Input here"></input></div>
                <div class="item31">Degree celsius</div>
            </div>
            <div class="grid-container1">
                <div class="item11"><img src={rh} /></div> 
                <div class="item21"><input type="number" min="0" step="1" max="100" class="input" placeholder="Input here"></input></div>
                <div class="item31">Percent RH</div>
            </div>
            <div class="grid-container1">
                <div class="item11"><img src={sm} /></div>
                <div class="item21"><input type="number" min="0" step="1" max="9" class="input" placeholder="Input here"></input></div>
                <div class="item31">Soil moisture</div>
            </div>
            <div class="subBT"><p>SUBMIT</p></div>
        </div>
    )
}

export default IPBar