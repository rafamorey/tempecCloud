
const express = require('express');
const bodyParser = require('body-parser');
const db = require("./public/db")

const router = require('./network/routes')

db('mongodb+srv://tebanRaf:Mr178910@cluster0.xtjrswc.mongodb.net/?retryWrites=true&w=majority')
var app = express();
app.use(bodyParser.json())
// app.use(router)

router(app)

app.use('/app',express.static('public'))




app.listen(3000)
console.log('la app esta escuchando en el http://localhost:3000')
