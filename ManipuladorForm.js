document.getElementById('Formulario').addEventListener('submit', function(event) {
    event.preventDefault();

    var cidade = document.getElementById('cidade').value;

    fetch('https://your-backend-url.com/consultar-transportadora', { // Altere para a URL de produção
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cidade: cidade })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.transportadora) {
            document.getElementById('primeira').textContent = 'Primeira Transportadora: ' + data.transportadora;
        } else {
            document.getElementById('primeira').textContent = 'Nenhuma transportadora encontrada';
            alert('Nenhuma transportadora encontrada para a cidade especificada.');
        }
    })
    .catch(error => {
        console.error('Erro ao fazer a requisição:', error);
        alert('Erro ao conectar com o servidor.');
    });
});