const express = require('express');
var cors = require('cors');
const app = express();
app.use(cors());
const port = process.env.PORT || 5000;

app.listen(port, ()=> console.log(`Listening on port ${port}`));

app.post('/', (req, res)=>{
    res.send({express: 'YOUR EXPRESS BACKEND IS CONNECTED TO REACT'})
})