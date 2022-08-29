
// importamos el archivo model
const Model = require("./model")

// funcion para agregar mensajes, recibe el mensaje de controller del componente
function addMessage(message){
//   list.push(message)
// la variable myMessage es un nuevo modelo creado con lo que tenga message
    const myMessage = new Model(message)
    // guardamos myMessage en la dataBase
    myMessage.save()
}

async function getMessage(filterUser){
    let filter ={}
    if(filterUser !== null){
        filter = { user:  filterUser}
    }
    const messages = await Model.find(filter)
    return messages
}

async function patchMessage(id, message) {
     const foundMessage = await Model.findOne({
        _id: id
     })
     foundMessage.message =message
     const newMessage = await foundMessage.save()
     return newMessage
}

async function deleteMessage(id) {
     await Model.deleteOne({
        _id: id
    })
}

module.exports ={
    add: addMessage,
    list: getMessage,
  update: patchMessage,
  remove: deleteMessage
  // delete:
}