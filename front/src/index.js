console.log('hola')

// url del backend
const api_url = 'http://localhost:3002/enterprise'


async function login() {
    
    const res = await fetch(api_url)
    const data = await res.json()
    console.log('access')
    console.log(data)
    
    if(res.status !== 200){
        console.log('error de conexion')
    }else {
        return data
    }
}

const signInButton = document.getElementById('signInButton')
signInButton.onclick = login