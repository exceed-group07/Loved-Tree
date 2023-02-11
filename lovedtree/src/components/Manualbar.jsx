import "../styles/InputBar.css"
import temp from "../icons/temp.png"

function Manualbar() {
    return (
        <div>
            <div class="grid-container1">
                <div class="item11"><img src={temp} /></div>
                <div class="item21"><input type="number" min="16" step="1" max="40" class="input" placeholder="Input here"></input></div>
                <div class="item31">degree celsius</div>
            </div>
            <div class="subBT"><p>SUBMIT</p></div>
        </div>
    )
}

export default Manualbar