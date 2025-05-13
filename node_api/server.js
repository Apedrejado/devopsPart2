const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.get('/get-from-python', async (req, res) => {
    try {
        const response = await axios.get('http://python_api:5000/users');
 const dataWithSource = {
    ...response.data,  
    source: 'node_api' 
};

res.json(dataWithSource); 
    } catch (error) {
        console.error('Erro ao chamar a API Python:', error);
        res.status(500).send('Erro ao chamar a API Python');
    }
});

app.listen(port, () => {
    console.log(`Servidor Node.js rodando na porta ${port}`);
});
