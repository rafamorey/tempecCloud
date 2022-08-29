// indico que voy a utilizar mongoose
const mongoose = require('mongoose')

// voy a utilizar el Schema de mongoose
const Schema = mongoose.Schema

// my schema es una nueva instancia se Schema
// el cual incluye un usuario que es un string
// el mensaje debe ser obligatorio
// y una fecha
const mySchema = new Schema({
    user: String,
    message: {
        type: String,
        required: true,
    },
    date: Date
})

// le pasamos el esquema con el que queremos que se cree nuestro mensaje a mongoose.model
const model = mongoose.model('Message', mySchema)

// exportamos este modelo
module.exports = model;