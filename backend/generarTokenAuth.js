const jwt = require("jsonwebtoken")

function generateAccessToken (dni) {
return jwt.sign({name:user}, process.env.ACCESS_TOKEN_SECRET, {expiresIn: "43800m"})
}
module.exports=generateAccessToken