
const express = require('express');
const bodyParser = require('body-parser');

const response = require('./response')
const router = express.Router()

var app = express();
app.use(bodyParser.json())
app.use(router)

router.get('/message', (req, res) =>{
  console.log(req.header)
  res.header({
    "customHeader": "Nuestro valor"
  })
  // res.send('Hola desde get')
  response.success(req, res, 'Lista de mensajes', 200)
})

router.post('/message', (req, res) =>{
  if(req.query.error == "ok"){
    response.error(req, res, 'Error simulado', 400)
  }else{
    response.success(req,res,'Creado correctamente',201)
  }
})

router.delete('/message', (req, res) =>{
  console.log(req.body)
  console.log(req.query)
  res.send('mensaje ' + req.body.text + ' borrado exitosamente')
})

app.use('/app',express.static('public'))

app.listen(3000)
console.log('la app esta escuchando en el http://localhost:3000')
