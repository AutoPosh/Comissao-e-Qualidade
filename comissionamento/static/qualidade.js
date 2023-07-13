const botao = document.querySelector(".img-logo");

botao.addEventListener("click", function () {
  location.href = "/homepage";
});

// Função para lidar com o clique no botão "Finalizar"
function handleAvaliarButton(event) {
  const divId = event.target.dataset.id;

  const divElement = event.target.closest('.data-values');
  const etapaElement = divElement.querySelector('.etapa-data');
  const servicoElement = divElement.querySelector('.servico-data');

  const etapa = etapaElement.textContent.trim();
  const servico = servicoElement.textContent.trim();

  enviarSolicitacaoAPI(divId, "Avaliar", etapa, servico);
}

// Função para enviar a solicitação para sua API
function enviarSolicitacaoAPI(divId, acao, etapa, servico) {
  // Faça a solicitação para sua rota da API com o ID da div e a ação
  // Você pode usar o objeto XMLHttpRequest ou a função fetch para fazer a solicitação AJAX
  // Por exemplo, usando fetch:

  fetch(`/qualidade/init_avaliacao?id=${divId}&acao=${acao}&etapa=${etapa}&servico=${servico}`, {
    method: 'POST',
    // Se houver necessidade de passar algum cabeçalho ou corpo na solicitação, você pode adicionar aqui
  })
}

// Obtenha uma lista de todos os botões de reiniciar, pausar e finalizar
const avaliarButtons = document.getElementsByClassName('btn-avaliar');

// Adicione um event listener para cada botão
for (const button of avaliarButtons) {
  button.addEventListener('click', handleAvaliarButton);
}