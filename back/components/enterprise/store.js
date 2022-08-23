const Model = require('./model');

function addEnterprise(enterprise){
  const myEnterprise = new Model(enterprise)
  return myEnterprise.save() 
}

async function getEnterprise(){
  const enterprises = await Model.find(filter)
  return enterprises
}

module.exports = {
  addEnterprise,
  getEnterprise
}