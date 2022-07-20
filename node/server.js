
const express = require('express');
const bodyParser = require('body-parser');
const router = express.Router()

var app = express();
app.use(bodyParser.json())
app.use(router)

router.get('/message', (req, res) =>{
  console.log(req.header)
  res.header({
    "customHeader": "Nuestro valor"
  })
  res.send('Hola desde get')
})

router.post('/message', (req, res) =>{
  res.status(201).send({
    "error": "",
    "body": "creado correctamente"
  })
})

router.delete('/message', (req, res) =>{
  console.log(req.body)
  console.log(req.query)
  res.send('mensaje ' + req.body.text + ' borrado exitosamente')
})


app.listen(3000)
console.log('la app esta escuchando en el http://localhost:3000')
