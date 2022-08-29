// importamos el archivo store, es en donde guardamos los mensajes del componente
const store = require('./store');

// funcion para agregar mensajes
function addMessage(user, message){
  // retorna una nueva promesa, como cualquier promesa necesita un resolve y un reject
  return new Promise((resolve, reject) =>{
    // si no hay usuario o no hay mensaje
    if(!user || !message){
      // regresamos un reject
      console.error('[messageController] No hay usuario o mensaje')
      return reject('Datos incorrectos')
    }
    // creamos un objeto llamado fullMessage que utiliza el archivo network del componente
    // este objeto contiene un usuario, un mensaje y una fecha de creación
    const fullMessage={
      user: user,
      message: message,
      date: new Date()
    }
    // usando la funcion add del archivo store le pasamos este nuevo objeto fullMessage
    // console.log(fullMessage)
    store.add(fullMessage)
    // resolvemos con fullmessage
    resolve(fullMessage)
  })
}

function getMessage(filterUser){
  return new Promise((resolve, reject) => {
    resolve(store.list(filterUser))
  })
}

function patchMessage(id, message){
  return new Promise(async (resolve, reject) => {
    if(!id || !message) {
      reject('Invalid data')
      return false
    }
    const result = await store.update(id, message)
    resolve(result)
    
  })
}

function deleteMessage(id){
  return new Promise(async (resolve, reject) => {
    if(!id){
      reject('Invalid id')
      return false
    }
    const deleted = await store.remove(id)
    resolve(deleted)
  })
}

module.exports = {
  addMessage,
  getMessage,
  patchMessage,
  deleteMessage
}