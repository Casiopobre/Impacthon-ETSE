//Importación de paquetes
var express = require("express");
var bodyParser = require("body-parser");
var app = express();
const bcrypt = require("bcrypt");
const maketoken = require("./functions.js");
const generateAccessToken = require("./generarTokenAuth.js");
const mysql = require("mysql");
require("dotenv").config();

//Variables generales
const saltRounds = 10;

//Puerto del servidor
var port = process.env.PORT || 8080;
app.use(express.json());

//Conexion base de datos
conexion = mysql.createPool({
  host: process.env.HOST,
  user: process.env.USER,
  password: process.env.PASSWORD,
  database: process.env.DATABASE,
  port: 3306,
  typeCast: function castField(field, useDefaultTypeCasting) {
    if (field.type === "BIT" && field.length === 1) {
      var bytes = field.buffer();
      return bytes[0] === 1;
    }
    return useDefaultTypeCasting();
  },
});

//-------------  RUTAS  -------------

//Rutas get
app.get("/getRecetas", getRecetas);

//Rutas post
app.post("/authPWD", autorizacionPWD);
app.post("/authToken", autorizacionToken);
app.post("/create-act", crearCuenta);

//-------------  FUNCIONES  -------------
//Funciones get
function getRecetas(request, response) {
  let tokenLogin=document.body.tokenLogin
  if(tokenLogin){
    jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, function (err, token_data) {
      if (err) {
          response.json({
            correcto: 0
          })
      } else {
        jsonRespuesta = {
          recetas: [
            {
              nombre: "Paracetamol",
              inicio: "16/03/2025",
              fin: "21/03/2025",
              dosis: 7,
              intervalos: 8,
            },
            {
              nombre: "Ibuprofeno",
              inicio: "12/03/2025",
              fin: "17/03/2025",
              dosis: 4,
              intervalos: 12,
            },
          ],
        };
        response.json(jsonRespuesta);
      }})
  }
  
  
}
//Funciones post
function autorizacionPWD(request, response) {
  dni = request.body.dni;
  passwd = request.body.passwd;
  if (dni && passwd) {
    conexion.query(
      "SELECT * FROM Paciente WHERE dni = ? ",
      [dni],
      async function (error, results, fields) {
        if (error) {
          console.log(error);
          response.json({
            correcto: 0,
            mensaje: error.message,
          });
        } else {
          if (results.length > 0) {
            if (await bcrypt.compare(passwd, results[0].passwd)) {
              let tokenLogin = generateAccessToken(dni)
              response.json({
                "tokenLogin": tokenLogin
            });
            }
          }
        }
      }
    );

    jsonRespuesta = {
      usuario: dni,
      contraseña: passwd,
      token: makeid(8),
    };
    response.json(jsonRespuesta);
  }
}

function autorizacionToken(request, response) {
  let tokenLogin=document.body.tokenLogin
  if(tokenLogin){
    conexion.query(
      "SELECT * FROM CodigoQR WHERE token = ? ",
      [tokenLogin],
      async function (error, results, fields) {
        if (error) {
          console.log(error);
          response.json({
            correcto: 0,
            mensaje: error.message,
          });
        } else {
          if (results.length > 0) {
            idPaciente = results[0].paciente;
            conexion.query(
              "SELECT * FROM Paciente WHERE id = ? ",
              [idPaciente],
              async function (error, results, fields) {
                if (error) {
                  console.log(error);
                  response.json({
                    correcto: 0,
                    mensaje: error.message,
                  });
                }else{
                  if (results.length > 0) {
                  dni=results[0].dni
                  let tokenLogin = generateAccessToken(dni)
                  response.json({
                    "tokenLogin": tokenLogin
                  });
                }
                } 
              })
            
          }
        }
      }
    );

  }


}

async function crearCuenta(request, response) {
  dni = request.body.dni;
  passwd = request.body.passwd;
  edad = request.body.edad;
  nombre = request.body.nombre;
  apellido1 = request.body.apellido1;
  apellido2 = request.body.apellido2;
  num_tlf = request.body.num_tlf;
  let encryptedPasswd = await bcrypt.hash(passwd, saltRounds);

  if (dni && passwd && edad && nombre && apellido1 && apellido2 && num_tlf) {
    conexion.query(
      "INSERT into Paciente (dni,edad,nombre,apellido1,apellido2,passwd,num_tlf) values(?,?,?,?,?,?,?)",
      [dni, edad, nombre, apellido1, apellido2, encryptedPasswd, num_tlf],
      async function (error) {
        if (error) {
          response.json({
            correcto: 0,
            mensaje: error.message,
          });
        } else {
          conexion.query(
            "SELECT * FROM Paciente WHERE dni = ? ",
            [dni],
            async function (error, results, fields) {
              // Si ocurre algún error lanzamos el error
              if (error) {
                console.log(error);
                response.json({
                  correcto: 0,
                  mensaje: "Error al crear el token",
                });
              } else {
                if (results.length > 0) {
                  id = results[0].id;
                  token = maketoken(10);
                  conexion.query(
                    "INSERT into CodigoQR (token,paciente) values(?,?)",
                    [token, id],
                    async function (error) {
                      if (error) {
                        console.log(error);
                        response.json({
                          correcto: 0,
                          mensaje: "Error al crear el token",
                        });
                      } else {
                        response.json({
                          correcto: 0,
                          mensaje: "Cuenta creada",
                          token: token,
                        });
                      }
                    }
                  );
                }
              }
            }
          );
        }
      }
    );
  } else {
    response.json({
      correcto: 0,
      mensaje: "Faltan campos",
    });
  }
}

// app.del('/', function(req, res) {
//   res.json({ mensaje: 'Método delete' })
// })

// iniciamos nuestro servidor
app.listen(port);
console.log("API escuchando en el puerto " + port);
