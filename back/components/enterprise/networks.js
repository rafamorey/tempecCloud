const express = require('express')
const router = express.Router()
const response = require('../../network/response')
const controller = require('./controller')

router.get('/', (req,res) => {
  controller.getEnterprise()
  .then((enterprises) =>{
    response.success(req, res, enterprises, 200)
  })
  .catch(err => {
    response.error(req,res, 'internal error', 500, err)
  })
})

router.post('/', (req,res) =>{
  controller.addEnterprise(req)
    .then(data => {
      response.success(req,res,data,201)
    })
    .catch(err => {
      response.error(req,res, 'internal error', 500, err)
    })
})


module.exports = router
