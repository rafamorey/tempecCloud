const express = require('express')
const router = express.Router()
const response = require('../../../network/response')
const controller = require('./controller')

router.get('/', (req, res) =>{
  controller.getMessage()
    .then((messageList) => {
      response.success(req, res, messageList, 200)
    })
    .catch(e => {
      response.error(req, res, "unexpected Error", 500, e)
    })
})

router.post('/', (req, res) =>{
  controller.addMessage(req.body.user, req.body.message)
    .then((fullMessage) => {
      response.success(req,res, fullMessage, 201)
    })
    .catch(e => {
      response.error(req,res,'Informacion Invalida', 400, 'Es una simulacion')
    })  
})

router.delete('/message', (req, res) =>{
  console.log(req.body)
  console.log(req.query)
  res.send('mensaje ' + req.body.text + ' borrado exitosamente')
})

module.exports = router