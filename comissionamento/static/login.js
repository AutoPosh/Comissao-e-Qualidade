/*document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('formulario');
    const senhaInput = document.getElementById('senha');
    const confirmaSenhaInput = document.getElementById('confirma-senha');

    form.addEventListener('submit', function (event) {
        if (senhaInput.value !== confirmaSenhaInput.value) {
            // Senhas não correspondem
            event.preventDefault(); // Impede o envio do formulário

            // Estiliza o campo de senha e confirmação de senha
            senhaInput.style.borderColor = 'red';
            confirmaSenhaInput.style.borderColor = 'red';

            // Exibe um alerta informando que as senhas não correspondem
            alert('As senhas digitadas não correspondem.');
        }
    });
});*/

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('formulario');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const passwordField = document.getElementById('password-field');
        const password = passwordField.value;

        const response = await fetch('http://192.168.1.147:5000/authenticate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `password=${encodeURIComponent(password)}`,
        });

        if (response.ok) {
            const data = await response.text();
            console.log(data);
        } else {
            console.error('Erro na solicitação:', response.status);
        }
    });
});
