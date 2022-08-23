
const store = require('./store')

function addEnterprise(name){
  if(!name){
    return Promise.reject('invalid name')
  }
  const enterprise = {
    name,
  }
  return store.addEnterprise(enterprise)
}

function getEnterprise(){
  return new Promise((resolve, reject) => {
    resolve(store.list())
  })
}

module.exports = {
  addEnterprise,
  getEnterprise
}