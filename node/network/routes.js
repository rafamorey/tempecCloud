const express = require('express');

// llamo al archivo message/networks, que contiene la logica de negocio del componente message
const message =require('../components/message/message/networks')

// creamos las rutas a utilizar, para eso le pasamos el end point que va a recibir y el archivo a ejecutar
const routes = function(server) {
  server.use('/message', message)
  server.use('/user', message)
  server.use('/device', message)
}

// exportamos la variable routes
module.exports = routes