//Importación de paquetes
var express = require('express')
var bodyParser = require('body-parser')
var app = express()
const bcrypt = require('bcrypt')
const makeid = require("./functions.js")
const mysql = require("mysql");               
require("dotenv").config();



//Puerto del servidor
var port = process.env.PORT || 8080  
app.use(express.json());


//Conexion base de datos
conexion = mysql.createPool({
  host: process.env.HOST,
  user: process.env.USER,
  password: process.env.PASSWORD,
  database: process.env.DATABASE,
  port: 3306,
  typeCast: function castField(field, useDefaultTypeCasting) {
      if ((field.type === "BIT") && (field.length === 1)) {
          var bytes = field.buffer();
          return (bytes[0] === 1);
      }
      return (useDefaultTypeCasting());
  }
});



//-------------  RUTAS  -------------

//Rutas get
app.get('/calendario', calendario)

//Rutas post
app.post('/auth', autorizacion)
app.post('/create-act',crearCuenta)




//-------------  FUNCIONES  -------------
//Funciones get
function calendario(request,response){
  jsonRespuesta = {
    recetas:[
      {nombre:'Paracetamol',inicio:'16/03/2025',fin:'21/03/2025',dosis:7,intervalos:8},
      {nombre:'Ibuprofeno',inicio:'12/03/2025',fin:'17/03/2025',dosis:4,intervalos:12}
    ]

  }
  response.json(jsonRespuesta) 
}
//Funciones post
function autorizacion(request, response) {
  dni=request.body.dni
  passwd=request.body.passwd
  // conexion.query('SELECT * FROM Paciente WHERE dni = ? ', [dni], async function (error, results, fields) {
  //   // Si ocurre algún error lanzamos el error
  //   if (error) throw error;
  //   // Comprobamos si la consulta devolvió algún usuario
  //   if (results.length > 0) {
  //       if (await bcrypt.compare(passwd, results[0].passwd)) {
  //           console.log(results[0])
  //               token
  //               response.cookie('auth', {
  //                   "token": makeid(5),
  //                   "username": username,
  //                   "id": results[0].Id
  //               });
  //           }
  //       }})
  jsonRespuesta={
    usuario:dni,contraseña:passwd,token:makeid(8)
  }
  response.json(jsonRespuesta)   
}

function crearCuenta(request,response){

}


// app.del('/', function(req, res) {
//   res.json({ mensaje: 'Método delete' })  
// })

// iniciamos nuestro servidor
app.listen(port)
console.log('API escuchando en el puerto ' + port)