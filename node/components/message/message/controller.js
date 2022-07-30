const store = require('./store');

function addMessage(user, message){
  return new Promise((resolve, reject) =>{
    if(!user || !message){
      console.error('[messageController] No hay usuario o mensaje')
      return reject('Datos incorrectos')
    }
    const fullMessage={
      user: user,
      message: message,
      date: new Date()
    }
    // console.log(fullMessage)
    store.add(fullMessage)
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