
const mongoose = require('mongoose')
const Schema = mongoose.Schema

const mySchema = new Schema({
  id: String,
  name: String,
  password:String,
  email: String,
  phone: String,
  idUsers:Array
})

const model = mongoose.model('Enterprise', mySchema)

module.exports = model