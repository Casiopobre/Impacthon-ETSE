//Importación de paquetes
var express = require('express')
var app = express()
const mysql = require("mysql");               
require("dotenv").config();


//Puerto del servidor
var port = process.env.PORT || 8080  



//-------------  RUTAS  -------------

//Rutas get
app.get('/calendario', calendario)

//Rutas post
app.post('/auth', autorizacion)




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
  response.json({ mensaje: 'Método post' })   
}


// app.del('/', function(req, res) {
//   res.json({ mensaje: 'Método delete' })  
// })

// iniciamos nuestro servidor
app.listen(port)
console.log('API escuchando en el puerto ' + port)