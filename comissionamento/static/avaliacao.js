// Obtendo o botão "Salvar"
var btnSalvar = document.querySelector('.btn-save');

// Adicionando um evento de clique ao botão "Salvar"
btnSalvar.addEventListener('click', function () {
    // Obtendo todas as perguntas
    var perguntas = document.querySelectorAll('.perguntas');

    // Variáveis para armazenar a contagem
    var simCount = 0;
    var naoCount = 0;
    var total = 0;

    // Iterando sobre as perguntas
    perguntas.forEach(function (pergunta) {
        // Obtendo os radio buttons da pergunta atual
        var radios = pergunta.querySelectorAll('input[type="radio"]');

        // Verificando se algum radio button está marcado
        var algumMarcado = false;

        // Verificando cada radio button da pergunta atual
        radios.forEach(function (radio) {
            if (radio.checked) {
                algumMarcado = true;

                // Verificando qual opção foi marcada
                if (radio.classList.contains('s')) {
                    simCount++;
                } else if (radio.classList.contains('n')) {
                    naoCount++;
                }
            }
        });

        // Incrementando o total somente se algum radio button estiver marcado na pergunta
        if (algumMarcado) {
            total++;
        }
    });

    // Exibindo o alerta com os valores contados
    console.log('SIM: ' + simCount + ' VALOR\nNÃO: ' + naoCount + ' VALOR\nTOTAL: ' + total + ' VALOR');
    let notaAvaliacao = simCount / (simCount + naoCount)
    // Arredondando a nota para 2 casas decimais
    notaAvaliacao = notaAvaliacao.toFixed(2);
    let id = document.getElementById('id').textContent
    let etapa = document.getElementById('etapa').textContent
    alert(`O id é ${id}. A nota: ${notaAvaliacao}\nA etapa: ${etapa}`)
    dados = {
        id: id,
        nota: notaAvaliacao,
        etapa: etapa
    }
    // Enviar a solicitação para a rota "avaliacao" usando o método fetch
    fetch('/premiacao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
        .then(response => response.json())
        .then(result => {
            console.log('Resposta da API:', result.message);
            // Faça algo com a resposta da API
        })
        .catch(error => {
            // Lidar com erros (opcional)
            console.error(error);
        });
});
