
const express = require('express');

var app = express();

app.use('/', (req, res)=>
  res.send('Hola')
)

app.listen(3000)
console.log('la app esta escuchando en el http://localhost:3000')
