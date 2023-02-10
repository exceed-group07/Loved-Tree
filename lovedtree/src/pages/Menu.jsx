import { useState,useEffect } from "react"
import IPBar from "../components/Inputbar"
import ModeBT from "../components/Button"
import Monitors from "../components/Monitor"
import "../styles/Mode_BT.css"
import "../styles/Menu.css"
function Menu() {
    



    

    
    return (
        <div>
            <Monitors></Monitors>
            <br></br>
            <div class="control-panel">
                <div>
                    <ModeBT></ModeBT>
                </div>
                <div class="color-select"></div>
            </div>
            <div class="lower">
                <IPBar />
                <div class="line"></div>
            </div>
        </div>
    )

}

export default Menu