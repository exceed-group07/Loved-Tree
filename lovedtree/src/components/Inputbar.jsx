import rh from "../icons/rh.png"
import temp from "../icons/temp.png"
import sm from "../icons/sm.png"
import "../styles/InputBar.css"

function IPBar() {
    return (
        <div class="auto-def">
            <div class="grid-container1">
                <div class="item11"><img src={temp} /></div>
                <div class="item21"><input type="number" min="16" step="1" max="40" class="input"></input></div>
                <div class="item31">degree celsius</div>
            </div>
            <div class="grid-container1">
                <div class="item11"><img src={rh} /></div>
                <div class="item21"><input type="number" min="0" step="1" max="100" class="input"></input></div>
                <div class="item31">percent RH</div>
            </div>
            <div class="grid-container1">
                <div class="item11"><img src={sm} /></div>
                <div class="item21"><input type="number" min="0" step="1" max="100" class="input"></input></div>
                <div class="item31">soil moisture</div>
            </div>
            <div class="subBT"><p>SUBMIT</p></div>
        </div>
    )
}

export default IPBar