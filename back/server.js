
const express = require('express')
const bodyParser = require('body-parser')
const db = require('./db')
const router = require('./network/routes')
const secret = require('./secret')

db(apiKey)
var app = express()
app.use(bodyParser.json())

router(app)

// app.use('/app', express.static('public'))

const port = 3002
app.listen(port)
console.log(`el servidor esta escuchando en el puerto ${port}`)



