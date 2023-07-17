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
    let notaAvaliacao = (simCount / (simCount + naoCount)) * 100
    // Arredondando a nota para 2 casas decimais
    notaAvaliacao = notaAvaliacao.toFixed(2);
    alert(notaAvaliacao)
});
