const botao = document.querySelector(".img-logo");

botao.addEventListener("click", function () {
  location.href = "/homepage";
});


// Selecionar todos os botões "Avaliar"
const buttons = document.querySelectorAll('.btn-avaliar');

// Adicionar um evento de clique a cada botão
buttons.forEach(button => {
  button.addEventListener('click', () => {
    // Obter o ID da div correspondente
    const id = button.dataset.id;

    // Obter os dados da div correspondente
    const osData = document.getElementById(id).querySelector('.os-data').textContent;
    const servicoData = document.getElementById(id).querySelector('.servico-data').textContent;
    const etapaData = document.getElementById(id).querySelector('.etapa-data').textContent;
    const statusServico = document.getElementById(id).querySelector('.status-servico').textContent;


    // Criar o objeto de dados a ser enviado na solicitação
    const data = {
      id: id,
      osData: osData,
      servicoData: servicoData,
      statusServico: statusServico,
      etapaData: etapaData
    };

    // Enviar a solicitação para a rota "avaliacao" usando o método fetch
    fetch('/avaliacao', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(() => {
        // Redirecionar o navegador para a rota "avaliacao"
       window.location.href = `/avaliacao?id=${id}&osData=${osData}&servicoData=${servicoData}&etapaData=${etapaData}`;
      })
      .catch(error => {
        // Lidar com erros (opcional)
        console.error(error);
      });
  });
});

/*
// Função para lidar com o clique no botão "Avaliar"
function handleAvaliarButton(event) {
  const divId = event.target.dataset.id;

  const divElement = event.target.closest('.data-values');
  const etapaElement = divElement.querySelector('.etapa-data');
  const servicoElement = divElement.querySelector('.servico-data');

  const etapa = etapaElement.textContent.trim();
  const servico = servicoElement.textContent.trim();

  enviarSolicitacaoAPI(divId, "Avaliar", etapa, servico);
}

function enviarSolicitacaoAPI(divId, acao, etapa, servico) {
  var url = "/avaliar"; // Substitua pela URL correta da sua API Flask

  var data = {
    divId: divId,
    acao: acao,
    etapa: etapa,
    servico: servico
  };

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .catch(function (error) {
      console.log("Erro na solicitação:", error.message);
    });
}


// Obtenha uma lista de todos os botões de reiniciar, pausar e finalizar
const avaliarButtons = document.getElementsByClassName('btn-avaliar');

// Adicione um event listener para cada botão
for (const button of avaliarButtons) {
  button.addEventListener('click', handleAvaliarButton);
}*/