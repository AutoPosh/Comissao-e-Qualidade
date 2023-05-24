/* function logoClick() {
    location.href = 'http://192.168.0.34:5000'
}

//Ao clicar nos ids svc, qualidade, consulta, painel o site deve redirecionar para a página correspondente

document.addEventListener("DOMContentLoaded", function() {
    const svc = document.getElementById('svc');
    const qualidade = document.getElementById('qualidade');
    const consulta = document.getElementById('consulta');
    const painel = document.getElementById('painel');
  
    svc.addEventListener('click', function() {
        window.location.href = '/service'; // Redirecionar para a página '/service'
    });
  
    qualidade.addEventListener('click', function() {
        window.location.href = '/qualidade'; // Redirecionar para a página '/qualidade'
    });
  
    consulta.addEventListener('click', function() {
        window.location.href = '/consulta'; // Redirecionar para a página '/consulta'
    });
  
    painel.addEventListener('click', function() {
        window.location.href = '/adm'; // Redirecionar para a página '/painel'
    });
  }); */
  



/*document.addEventListener("DOMContentLoaded", function () {
    const contentDiv = document.getElementById("content");
    contentDiv.style.transition = "opacity 0.3s";

    function loadPage(url) {
        contentDiv.style.opacity = "0";
        if (url === "/") {
            location.href = "http://192.168.1.147:5000";
            return;
        }
        fetch(url)
            .then(response => response.text())
            .then(html => {
                setTimeout(() => {
                    contentDiv.innerHTML = html;
                    contentDiv.style.opacity = "1";
                }, 300); // Aguarda 300ms antes de exibir o conteúdo com opacidade 1
            });
    }

    // Atualizar o conteúdo da página quando um link for clicado
    document.querySelectorAll("nav a").forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            const url = this.getAttribute("href");
            loadPage(url);
            history.pushState(null, null, url);
        });
    });

    // Atualizar o conteúdo da página ao navegar usando o botão voltar/avançar do navegador
    window.addEventListener("popstate", function () {
        contentDiv.style.opacity = "0";
        setTimeout(() => {
            loadPage(location.pathname);
        }, 300); // Aguarda 300ms antes de carregar a nova página com opacidade 1
    });
});*/