// indicamos que vamos a utilizar express
const express = require('express');
// empezamos a utilizar el convertidor de body de express
const bodyParser = require('body-parser');
// llamamos al archivo que conecta con la base de datos
const db = require("./db")
// llamamos al archivo que tiene las routas
const router = require('./network/routes')

// url de base de datos
db('mongodb+srv://tebanRaf:Mr178910@cluster0.xtjrswc.mongodb.net/?retryWrites=true&w=majority')
//inicializamos express
var app = express();
// usamos el convertidor de body para pasarlo a json
app.use(bodyParser.json())

// indicamos al router que utilice app
router(app)

// al recibir este endpoint regresamos el archivo estatico guardado en public, el archivo debe de llamarse index.html
app.use('/app',express.static('public'))

// el puerto de escucha es el 3000
app.listen(3000)
console.log('la app esta escuchando en el http://localhost:3000')
