const URL= "http://group7.exceed19.online/"

export default async function FetchData() {
    try {
        const response = await fetch(URL)
        const result = await response.json()
        return result
    }catch(err) {
        console.log(err)
    }
}