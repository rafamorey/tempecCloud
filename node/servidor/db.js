// mongodb+srv://tebanRaf:Mr178910@cluster0.xtjrswc.mongodb.net/?retryWrites=true&w=majority
const db = require('mongoose')
db.Promise = global.Promise
// 'mongodb+srv://tebanRaf:Mr178910@cluster0.xtjrswc.mongodb.net/?retryWrites=true&w=majority'
async function connect(url) {
     await db.connect(url , {
    useNewUrlParser: true,
})
console.log('db conectada con exito')
}

module.exports = connect