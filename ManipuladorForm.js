document.getElementById('Formulario').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir o envio padrão do formulário

    var cidade = document.getElementById('cidade').value; // Pegar o valor do campo de cidade

    fetch('http://localhost:3000/consultar-transportadora', { // URL do servidor
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cidade: cidade }) // Enviar dados como JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Logar a resposta no console para diagnóstico
        if (data.transportadora) {
            document.getElementById('primeira').textContent = 'Primeira Transportadora: ' + data.transportadora;
            // Se houver uma segunda transportadora, atualize-a aqui também
            // document.getElementById('segunda').textContent = 'Segunda Transportadora: ' + data.segundaTransportadora;
        } else {
            // Altere esse valor para o que você quiser exibir quando não houver dados
            document.getElementById('primeira').textContent = 'Nenhuma transportadora encontrada';
            alert('Nenhuma transportadora encontrada para a cidade especificada.');
        }
    })
    .catch(error => {
        console.error('Erro ao fazer a requisição:', error);
        alert('Erro ao conectar com o servidor.');
    });
});