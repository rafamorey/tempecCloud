const { MongoClient } = require("mongodb");
const uri =
"mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri);
async function run() {
  try {
    const database = client.db('Tempec_Cloud');
    const enterprises = database.collection('Enterprises');
    const historial = database.collection('Historial');
    const condi = {};
    const query = historial.find(condi).project({ _id: 0, _temperatura_interior:1 });
    await query.forEach(console.dir)
  } finally {
    await client.close();
  }
}
run().catch(console.dir);