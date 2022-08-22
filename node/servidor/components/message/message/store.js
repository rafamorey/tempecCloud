const Model = require("./model")

function addMessage(message){
//   list.push(message)
    const myMessage = new Model(message)
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