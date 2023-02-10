import "../styles/Mode_BT.css"

function ModeBT() {

    const handleOptionChange = (e) => {
    }
    return (
        <div class="autoBT">
            <fieldset id="switch" class="radio">
                <input name="switch" id="auto" type="radio" onChange={handleOptionChange}></input>
                <label for="auto">AUTO</label>
                <input name="switch" id="manual" type="radio" onChange={handleOptionChange}></input>
                <label for="manual">MANUAL</label>
            </fieldset>
        </div>
    )
}

export default ModeBT