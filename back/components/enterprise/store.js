const Model = require('./model');

function addEnterprise(enterprise){
  const myEnterprise = new Model(enterprise)
  return myEnterprise.save() 
}

function addPassword(pass){
  const myEnterprise = new Model(pass)
  return myEnterprise.save() 
}

async function getEnterprise(){
  const enterprises = await Model.find()
  return enterprises
}

module.exports = {
  addEnterprise,
  addPassword,
  getEnterprise
}