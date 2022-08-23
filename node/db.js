// mongodb+srv://tebanRaf:Mr178910@cluster0.xtjrswc.mongodb.net/?retryWrites=true&w=majority
// indicamos que vamos a utilizar mongoose
const db = require('mongoose')
// le indicamos a la base de datos que si va a utilizar algun formato de promesa, use la que tiene nativa mongoose
db.Promise = global.Promise
// 'mongodb+srv://tebanRaf:Mr178910@cluster0.xtjrswc.mongodb.net/?retryWrites=true&w=majority'
// funcion para conectarse con la data base, necesita una url
// esta funcion es exportada, e importada en server.js, en donde se le pasa la url
async function connect(url) {
     await db.connect(url , {
    useNewUrlParser: true,
})
console.log('db conectada con exito')
}

module.exports = connect