
// indicamos que vamos a utilizar express
const express = require('express')
// vamos a utilizar el router de express
const router = express.Router()
// importo el archivo de response
const response = require('../../../network/response')
// importo el archivo controlador, del componente
const controller = require('./controller')

// cuando nos venga un get, 
router.get('/', (req, res) =>{
    // funcion para filtrar el mensaje y saber de que usuario es,
  const filterMessage = req.query.user || null

    // funcion para obtener los mensajes, recibe el usuario filtrado
  controller.getMessage(filterMessage)

    // si el usuario existe, ejecutamos el archivo response con la funcion success y pasamos la req, la respuesta, la lista de mensajes y un estatus 200 de ok
    .then((messageList) => {
      response.success(req, res, messageList, 200)
    })
    // en caso de existir un error lo capturamos con catch y respondemos con archivo response y la funcion error con la req, respuesta, el texto error innesperado, status 500 y el e = error encontrado
    .catch(e => {
      response.error(req, res, "unexpected Error", 500, e)
    })
})

// usamos el router de express, cuando nos venga una peticion post
router.post('/', (req, res) => {

  // funcion para agreagar mensajes, el usuario viene en user dentro del body de la peticion, y el mensaje en message dentro del body de la peticion
  controller.addMessage(req.body.user, req.body.message)
  // console.log(req.body.user)
  // si todo esta ok, respondemos success con la peticion, la respuesta, el mensaje y status 201 de creado con exito
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