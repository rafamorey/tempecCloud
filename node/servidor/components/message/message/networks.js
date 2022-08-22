const express = require('express')
const router = express.Router()
const response = require('../../../network/response')
const controller = require('./controller')

router.get('/', (req, res) =>{
  const filterMessage = req.query.user || null

  controller.getMessage(filterMessage)
    .then((messageList) => {
      response.success(req, res, messageList, 200)
    })
    .catch(e => {
      response.error(req, res, "unexpected Error", 500, e)
    })
})

router.post('/', (req, res) => {
  controller.addMessage(req.body.user, req.body.message)
  // console.log(req.body.user)
    .then((fullMessage) => {
      response.success(req,res, fullMessage, 201)
    })
    .catch(e => {
      response.error(req,res,'Informacion Invalida', 400, 'Es una simulacion')
    })  
})

router.delete('/:id', (req, res) => {
  controller.deleteMessage(req.params.id,)
    .then((id) => {
      response.success(req,res, `Usuario ${req.params.id} eliminado`, 200)
    })
    .catch(e => {
      response.error(req, res, "unexpected error", 500, e)
    })
})

router.patch('/:id', (req, res) => {
  controller.patchMessage( req.params.id, req.body.message)
    .then((data) => {
      response.success(req, res, data, 200)
    })
    .catch(e => {
      response.error(req, res, "unexpected error", 500, e)
    })
  // console.log(req.params.id)

} )
module.exports = router