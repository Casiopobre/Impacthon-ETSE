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

//Rutas post
app.post("/getRecetas", getRecetas);
app.post("/authPWD", autorizacionPWD);
app.post("/authToken", autorizacionToken);
app.post("/createActMedico", crearCuentaMedico);
app.post("/createAct", crearCuenta);
app.post("/insertarRecetas", insertarRecetas);

//-------------  FUNCIONES  -------------
//Funciones get

//Funciones post
function autorizacionPWD(request, response) {
  dni = request.body.dni;
  passwd = request.body.passwd;
  if (dni && passwd) {
    conexion.query(
      "SELECT * FROM Usuario WHERE dni = ? ",
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
            id = results[0].id;
            if (await bcrypt.compare(passwd, results[0].passwd)) {
              let tokenLogin = generateAccessToken(id);
              response.json({
                correcto: 1,
                tokenLogin: tokenLogin,
                id: results[0].id,
                tipoUsuario: results[0].tipoUsuario,
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
  let tokenLogin = request.body.tokenLogin;
  if (tokenLogin) {
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
              "SELECT * FROM Usuario WHERE id = ? ",
              [idPaciente],
              async function (error, results, fields) {
                if (error) {
                  console.log(error);
                  response.json({
                    correcto: 0,
                    mensaje: error.message,
                  });
                } else {
                  if (results.length > 0) {
                    id = results[0].id;
                    let tokenLogin = generateAccessToken(id);
                    response.json({
                      correcto: 1,
                      tokenLogin: tokenLogin,
                      id: results[0].id,
                      tipoUsuario: results[0].tipoUsuario
                    });
                  }
                }
              }
            );
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

  // Aqui hay que añadir una comprobacion de que el usuario no exista ya
  // ni en paciente ni en medico, con DNI, supongo que valdrá

  if (dni && passwd && edad && nombre && apellido1 && apellido2 && num_tlf) {
    conexion.query(
      "INSERT into Usuario (dni,edad,nombre,apellido1,apellido2,passwd,num_tlf,tipo_usuario) values(?,?,?,?,?,?,?,?)",
      [
        dni,
        edad,
        nombre,
        apellido1,
        apellido2,
        encryptedPasswd,
        num_tlf,
        "paciente",
      ],
      async function (error) {
        if (error) {
          response.json({
            correcto: 0,
            mensaje: error.message,
          });
        } else {
          response.json({
            correcto: 1,
            mensaje: "Cuenta creada",
            token: token,
          });
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

async function crearCuentaMedico(request, response) {
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  if (tokenLogin) {
    jwt.verify(
      token,
      process.env.ACCESS_TOKEN_SECRET,
      function (err, token_data) {
        if (err || token_data != id) {
          response.json({
            correcto: 0,
          });
        } else {
          conexion.query(
            "SELECT * FROM Usuario WHERE id = ? ",
            [id],
            async function (error, results, fields) {
              if (error) {
                console.log(error);
                response.json({
                  correcto: 0,
                  mensaje: error.message,
                });
              } else {
                if (results > 0) {
                  dni = request.body.dni;
                  passwd = request.body.passwd;
                  edad = request.body.edad;
                  nombre = request.body.nombre;
                  apellido1 = request.body.apellido1;
                  apellido2 = request.body.apellido2;
                  num_tlf = request.body.num_tlf;
                  let encryptedPasswd = await bcrypt.hash(passwd, saltRounds);

                  if (
                    dni &&
                    passwd &&
                    edad &&
                    nombre &&
                    apellido1 &&
                    apellido2 &&
                    num_tlf
                  ) {
                    conexion.query(
                      "INSERT into Usuario (dni,edad,nombre,apellido1,apellido2,passwd,num_tlf,tipo_usuario) values(?,?,?,?,?,?,?,?)",
                      [
                        dni,
                        edad,
                        nombre,
                        apellido1,
                        apellido2,
                        encryptedPasswd,
                        num_tlf,
                        "paciente",
                      ],
                      async function (error) {
                        if (error) {
                          response.json({
                            correcto: 0,
                            mensaje: error.message,
                          });
                        } else {
                          conexion.query(
                            "SELECT * FROM Usuario WHERE dni = ? ",
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
                                    "INSERT into CodigoQR (token,paciente,uso) values(?,?,?)",
                                    [token, id, "login"],
                                    async function (error) {
                                      if (error) {
                                        console.log(error);
                                        response.json({
                                          correcto: 0,
                                          mensaje: "Error al crear el token",
                                        });
                                      } else {
                                        response.json({
                                          correcto: 1,
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
                } else {
                  response.json({
                    correcto: 0,
                    mensaje: "No tienes permisos para esa accion",
                  });
                }
              }
            }
          );
        }
      }
    );
  }
}

function getRecetas(request, response) {
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  if (tokenLogin) {
    jwt.verify(
      token,
      process.env.ACCESS_TOKEN_SECRET,
      function (err, token_data) {
        if (err || token_data != id) {
          response.json({
            correcto: 0,
          });
        } else {
          conexion.query(
            "SELECT * FROM Receta WHERE id_paciente = ? ",
            [id],
            async function (error, results, fields) {
              if (error) {
                console.log(error);
                response.json({
                  correcto: 0,
                  mensaje: error.message,
                });
              } else {
                if (results.length > 0) {
                  let recetas;
                  for (const recetaNum in results) {
                    conexion.query(
                      "SELECT nombre FROM Medicamento WHERE id = ? ",
                      [recetaNum.id],
                      async function (error, resultsMed, fields) {
                        if (error) {
                        } else {
                          recetas[recetaNum] = {
                            nombre: resultsMed[0],
                            fechaEmision: results[recetaNum].fecha_emision,
                            fechaFin: results[recetaNum].fecha_fin,
                            dosificacion: results[recetaNum].dosificacion,
                            intervalosDosificacion:
                              results[recetaNum].intervalos_dosificacion,
                          };
                          jsonRespuesta = {
                            correcto: 1,
                            recetas: recetas,
                          };
                          response.json(jsonRespuesta);
                        }
                      }
                    );
                  }
                }
                response.json({
                  correcto: 0,
                  mensaje: "Este paciente no tiene recetas",
                });
              }
            }
          );
        }
      }
    );
  }
}

function insertarRecetas(request, response) {
  let tokenLogin = request.body.tokenLogin;
  if (tokenLogin) {
    wt.verify(
      token,
      process.env.ACCESS_TOKEN_SECRET,
      function (err, token_data) {
        if (err || token_data != id) {
          response.json({
            correcto: 0,
          });
        } else {
          arrayRecetas = request.body.recetas;
          for (const numReceta in arrayRecetas) {
            receta = arrayRecetas[numReceta];
            conexion.query(
              "INSERT into Receta (id_paciente,id_medicamento,fecha_emision,fecha_fin,dosificacion,intervalos_dosificacion) values(?,?,?,?,?,?)",
              [
                receta.idPaciente,
                receta.idMedicamento,
                receta.fechaEmision,
                receta.fechaFin,
                receta.dosificacion,
                receta.intervalosDosificacion,
              ],
              async function (error) {
                if (error) {
                  response.json({
                    correcto: 0,
                    mensaje: error.message,
                  });
                }
              }
            );
          }
          response.json({
            correcto: 1,
            mensaje: "Recetas insertadas correctamente",
          });
        }
      }
    );
  }
}

// app.del('/', function(req, res) {
//   res.json({ mensaje: 'Método delete' })
// })

// iniciamos nuestro servidor
app.listen(port);
console.log("API escuchando en el puerto " + port);
