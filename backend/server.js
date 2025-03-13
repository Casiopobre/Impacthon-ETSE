//Importación de paquetes
var express = require("express");
var bodyParser = require("body-parser");
var app = express();
const bcrypt = require("bcrypt");
const maketoken = require("./functions.js");
const generateAccessToken = require("./generarTokenAuth.js");
const mysql = require("mysql");
const jwt = require("jsonwebtoken")
require("dotenv").config();

//Variables generales
const saltRounds = 10;

//Puerto del servidor
var port = process.env.PORT || 8080;
app.use(express.json());

//Conexion base de datos
conexion = mysql.createConnection({
  host: process.env.HOST,
  user: 'root',
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

function checkTokenJWT(token, id) {
    returnValue=0
  if (token) {
   
    jwt.verify(
      token,
      process.env.ACCESS_TOKEN_SECRET,
      function (err, token_data) {
        if (err || token_data != id) {
          returnValue=1;
        } else {
        returnValue=0;
        }
      }
    );
  }
  return returnValue
}

//-------------  RUTAS  -------------

//Rutas get

//Rutas post
app.post("/getTipoUsuario",getTipoUsuario);
app.post("/getRecetas", getRecetas);
app.post("/authPWD", autorizacionPWD);
app.post("/authToken", autorizacionToken);
app.post("/crearTokenEditar", crearTokenEditar);
app.post("/getIdToken", getIdToken);
app.post("/getDatosUsuario", getDatosUsuario);
app.post("/createActMedico", crearCuentaMedico);
app.post("/createAct", crearCuenta);
app.post("/insertarRecetas", insertarRecetas);
app.post("/insertarSintomas", insertarSintomas);

//-------------  FUNCIONES  -------------
//Funciones get

//Funciones post
function autorizacionPWD(request, response) {
  console.log("PersonaLogeada")
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
              console.log({
                correcto: 1,
                tokenLogin: tokenLogin,
                id: results[0].id,
                tipoUsuario: results[0].tipo,
              })
              response.json({
                correcto: 1,
                tokenLogin: tokenLogin,
                id: results[0].id,
                tipoUsuario: results[0].tipo,
              });
            }
          }
        }
      }
    );
  }else{
  response.json({
            correcto: 0,
            mensaje: "Faltan campos",
          });
    
  }
}

function autorizacionToken(request, response) {
  let tokenLogin = request.body.tokenLogin;
  if (tokenLogin) {
    conexion.query(
      "SELECT * FROM codigoQR WHERE token = ? ",
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
                      tipoUsuario: results[0].tipoUsuario,
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


function getIdToken(request, response) {
  let token = request.body.token;
  if (token) {
    conexion.query(
      "SELECT * FROM codigoQR WHERE token = ? ",
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
                    response.json({
                      correcto: 1,
                      id: results[0].id,
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
  fecha = request.body.fecha;
  nombreCompleto = request.body.nombreCompleto;
  num_tlf = request.body.num_tlf;
  let encryptedPasswd = await bcrypt.hash(passwd, saltRounds);

  // Aqui hay que añadir una comprobacion de que el usuario no exista ya
  // ni en paciente ni en medico, con DNI, supongo que valdrá

  if (dni && passwd && fecha && nombreCompleto && num_tlf) {
    conexion.query(
      "INSERT into Usuario (dni,fecha_nac,nombre_completo,passwd,num_tlf,tipo) values(?,?,?,?,?,?)",
      [dni, fecha, nombreCompleto, encryptedPasswd, num_tlf, "paciente"],
      async function (error) {
        if (error) {
          response.json({
            correcto: 0,
            mensaje: error.message,
          });
        } else {
          response.json({
            correcto: 1,
            mensaje: "Cuenta creada"
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
  if (checkTokenJWT(tokenLogin, id)) {
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
          if (results > 0 && (results[0].tipo="medico")) {
            dni = request.body.dni;
            passwd = request.body.passwd;
            fecha = request.body.fecha;
            nombreCompleto = request.body.nombreCompleto;
            num_tlf = request.body.num_tlf;
            let encryptedPasswd = await bcrypt.hash(passwd, saltRounds);

            if (dni && passwd && edad && nombreCompleto && num_tlf) {
              conexion.query(
                "INSERT into Usuario (dni,fecha_nac,nombre_completo,passwd,num_tlf,tipo) values(?,?,?,?,?,?)",
                [
                  dni,
                  fecha,
                  nombreCompleto,
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
                              "INSERT into codigoQR (token,paciente,uso) values(?,?,?)",
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
  } else {
    response.json({
      correcto: 0,
    });
  }
}

function getDatosUsuario(request,response){
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  let idPaciente = request.body.idPaciente;

  if (!tokenLogin || !checkTokenJWT(tokenLogin, id)) {
    return response.json({ correcto: 0 });
  }

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
        console.log(results[0].tipo))
        if (results > 0 && (results[0].tipo="medico")) {
          conexion.query(
            "SELECT * FROM Usuario WHERE id = ? ",
            [idPaciente],
            async function (error, results, fields) {
              if (error) {
                console.log(error);
                response.json({
                  correcto: 0,
                  mensaje: "Error",
                });
              } else {
                console.log(results)
                if (results > 0) {
                  response.json({
                    correcto: 1,
                    nombre: results[0].nombre_completo,
                    dni:results[0].dni,
                    fechaNacimiento:results[0].fecha_nac,
                    email:results[0].email,
                    numTlf:results[0].num_tlf
                  });
                  
                }else{
                  response.json({
                    correcto: 0,
                    mensaje: "no hay resultados",
                  });
                }
               
              }
            }
          );
          
        }else{
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
                console.log(results)
                if (results > 0) {
                  response.json({
                    correcto: 1,
                    nombre: results[0].nombre_completo,
                    dni:results[0].dni,
                    fechaNacimiento:results[0].fecha_nac,
                    email:results[0].email,
                    numTlf:results[0].num_tlf
                  });
                  
                }else{
                  response.json({
                    correcto: 0,
                    mensaje: "no hay resultados",
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

function crearTokenEditar(request, response){
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  if (!tokenLogin || !checkTokenJWT(tokenLogin, id)) {
    return response.json({ correcto: 0 });
  }
  token = maketoken(10);
  conexion.query(
    "INSERT into codigoQR (token,paciente,uso) values(?,?,?)",
    [token, id, "editar"],
    async function (error) {
      if (error) {
        console.log(error);
        response.json({
          correcto: 0,
          mensaje: error.message,
        });
      } else {
        response.json({
          correcto: 1,
          mensaje: "Token creado",
          token: token,
        });
      }
    }
  );
}

function crearTokenEditar(request, response){
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  if (!tokenLogin || !checkTokenJWT(tokenLogin, id)) {
    return response.json({ correcto: 0 });
  }
  token = maketoken(10);
  conexion.query(
    "INSERT into codigoQR (token,paciente,uso) values(?,?,?)",
    [token, id, "editar"],
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
          mensaje: "Token creado",
          token: token,
        });
      }
    }
  );
}

function getRecetas(request, response) {
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  let idPaciente = request.body.idPaciente;

  
  if (!tokenLogin || !checkTokenJWT(tokenLogin, id)) {
    return response.json({ correcto: 0 });
  }

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
        if (results > 0 && (results[0].tipo="medico")) {
          conexion.query(
            "SELECT * FROM Receta WHERE id_paciente = ?",
            [idPaciente],
            async function (error, results, fields) {
              if (error) {
                console.log(error);
                return response.json({
                  correcto: 0,
                  mensaje: error.message,
                });
              }
        
              if (results.length === 0) {
                return response.json({
                  correcto: 0,
                  mensaje: "Este paciente no tiene recetas",
                });
              }
        
              try {
                const recetas = await Promise.all(results.map(async (receta) => {
                  const [medicamento] = await new Promise((resolve, reject) => {
                    conexion.query(
                      "SELECT nombre FROM Medicamento WHERE id = ?",
                      [receta.id_medicamento],
                      (error, resultsMed) => {
                        if (error) reject(error);
                        else resolve(resultsMed);
                      }
                    );
                  });
        
                  return {
                    nombre: medicamento ? medicamento.nombre : 'Desconocido',
                    fechaEmision: receta.fecha_emision,
                    fechaFin: receta.fecha_fin,
                    dosificacion: receta.dosificacion,
                    intervalosDosificacion: receta.intervalos_dosificacion,
                  };
                }));
        
                response.json({
                  correcto: 1,
                  recetas: recetas,
                });
              } catch (err) {
                console.error(err);
                response.json({
                  correcto: 0,
                  mensaje: "Error al procesar las recetas",
                });
              }
            }
          );
        }else{
          conexion.query(
            "SELECT * FROM Receta WHERE id_paciente = ?",
            [id],
            async function (error, results, fields) {
              if (error) {
                console.log(error);
                return response.json({
                  correcto: 0,
                  mensaje: error.message,
                });
              }
        
              if (results.length === 0) {
                return response.json({
                  correcto: 0,
                  mensaje: "Este paciente no tiene recetas",
                });
              }
        
              try {
                const recetas = await Promise.all(results.map(async (receta) => {
                  const [medicamento] = await new Promise((resolve, reject) => {
                    conexion.query(
                      "SELECT nombre FROM Medicamento WHERE id = ?",
                      [receta.id_medicamento],
                      (error, resultsMed) => {
                        if (error) reject(error);
                        else resolve(resultsMed);
                      }
                    );
                  });
        
                  return {
                    nombre: medicamento ? medicamento.nombre : 'Desconocido',
                    fechaEmision: receta.fecha_emision,
                    fechaFin: receta.fecha_fin,
                    dosificacion: receta.dosificacion,
                    intervalosDosificacion: receta.intervalos_dosificacion,
                  };
                }));
        
                response.json({
                  correcto: 1,
                  recetas: recetas,
                });
              } catch (err) {
                console.error(err);
                response.json({
                  correcto: 0,
                  mensaje: "Error al procesar las recetas",
                });
              }
            }
          );
        }}})




  
}


function insertarRecetas(request, response) {
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  if (tokenLogin) {
    console.log(checkTokenJWT(tokenLogin,id))
    if(checkTokenJWT(tokenLogin,id)==1){
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
    }else{
      response.json({
        correcto: 0,
        mensaje:"No va"
      });
    }
  }
}

function insertarSintomas(request, response) {
  /*    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_paciente` BIGINT UNSIGNED NOT NULL,
    `fecha` DATE NOT NULL,
    `sintomas` TEXT NOT NULL, */
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  let fecha= request.body.fecha;
  let sintomas = request.body.sintomas;
  if (tokenLogin) {
    if(checkTokenJWT(tokenLogin,id)){
      console.log("Enter")
      conexion.query(
        "INSERT into Sintomatologia (id_paciente,fecha,sintomas) values(?,?,?)",
        [
          id,
          fecha,
          sintomas
        ],
        async function (error) {
          if (error) {
            response.json({
              correcto: 0,
              mensaje: error.message,
            });
          }else{
            response.json({
              correcto: 1,
              mensaje: "Insertado con exito",
            });
          }
        }
      );
    

    }
  }
}



function getTipoUsuario(request,response){
  let tokenLogin = request.body.tokenLogin;
  let id = request.body.id;
  
  if (!tokenLogin || !checkTokenJWT(tokenLogin, id)) {
    return response.json({ correcto: 0 });
  }

  conexion.query(
    "SELECT * FROM Usuario WHERE id = ?",
    [id],
    async function (error, results, fields) {
      if (error) {
        console.log(error);
        return response.json({
          correcto: 0,
          mensaje: error.message,
        });
      }
      if (results.length > 0) {
          console.log(results[0])
          return response.json({
            correcto: 1,
            tipoUsuario: results[0].tipo
          });
      }else{
        return response.json({
          correcto: 0,
          mensaje: "Este paciente no existe",
        });
      }})
}

// app.del('/', function(req, res) {
//   res.json({ mensaje: 'Método delete' })
// })

// iniciamos nuestro servidor
app.listen(port);
console.log("API escuchando en el puerto " + port);
