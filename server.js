// server.js
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.json());

const { getDataFromSheet } = require('./sheetsAPI');

app.post('/consultar-transportadora', async (req, res) => {
    const cidade = req.body.cidade;
    try {
        const dados = await getDataFromSheet(cidade);
        const melhorTransportadora = encontrarMelhorTransportadora(dados);
        res.send({ transportadora: melhorTransportadora });
    } catch (error) {
        res.status(500).send("Erro ao processar a solicitação");
    }
});

function encontrarMelhorTransportadora(dados) {
    let melhorTempo = Infinity;
    let melhorTransportadora = '';
    dados.forEach(row => {
        const tempo = Number(row[2]); // Ajuste o índice conforme a localização da coluna de tempo
        if (tempo < melhorTempo) {
            melhorTempo = tempo;
            melhorTransportadora = row[1]; // Ajuste o índice conforme a localização da coluna de nome da transportadora
        }
    });
    return melhorTransportadora;
}

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
