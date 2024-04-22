// sheetsAPI.js
const { google } = require('googleapis');

exports.getDataFromSheet = async function (cidade) {
    const auth = new google.auth.GoogleAuth({
        keyFile: 'credentials.json', // o caminho para suas credenciais
        scopes: 'https://www.googleapis.com/auth/spreadsheets.readonly',
    });

    const sheets = google.sheets({version: 'v4', auth});
    const spreadsheetId = '1FQOiNWM1ChoaLKK5a-26PvZDUo_iI993'; // Seu ID de Planilha
    const range = 'Sua_Aba!D:K'; // Ajuste a range conforme necessário

    try {
        const response = await sheets.spreadsheets.values.get({
            spreadsheetId: spreadsheetId,
            range: range,
        });
        const rows = response.data.values;
        const filteredRows = rows.filter(row => row[0].toLowerCase() === cidade.toLowerCase());
        return filteredRows;
    } catch (err) {
        console.error('Erro ao acessar o Google Sheets', err);
        throw err;
    }
};
