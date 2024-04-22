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
        console.log(data); // Tratar a resposta aqui
        // Aqui você pode atualizar o DOM ou mostrar alguma mensagem baseada na resposta
    })
    .catch(error => console.error('Erro ao fazer a requisição:', error));
});
