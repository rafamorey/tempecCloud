const express = require('express')

const enterprise = require('../components/enterprise/networks')

const routes = function(server){
  server.use('/enterprise', enterprise)
  server.use('/user', enterprise)
  server.use('/device', enterprise)
}

module.exports = routes