
exports.success = function(req, res, enterprise, status){
  res.status(status).send({
    error:"",
    body: enterprise
  })
}

exports.error = function(req, res, enterprise, status, details){
  console.log('response error' + details)
  res.status(status || 500).send({
    error:enterprise,
    body: ""
  })
}