
const store = require('./store')

function addEnterprise(req){
  // console.log(req.body)
  if(!req.body){
    return Promise.reject('invalid data')
  }
  const enterprise = {
    "name": req.body.name,
    "password": req.body.password,
    "email": req.body.email,
    "phone": req.body.phone,
    "idUsers": req.body.idUsers
  }
  return store.addEnterprise(enterprise)
}

// function addPassword(password){
//   if(!password){
//     return Promise.reject('invalid password')
//   }
//   const pass = {
//     password
//   }
//   return store.addPassword(pass)
// }

function getEnterprise(){
  return new Promise((resolve, reject) => {
    resolve(store.getEnterprise())
  })
}

module.exports = {
  addEnterprise,
  // addPassword,
  getEnterprise
}