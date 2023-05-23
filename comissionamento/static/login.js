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

    // Função para gerar um device_id único
    function generateDeviceId() {
        if (typeof uuidv4 !== 'undefined') {
            return uuidv4();
        } else {
            console.error('Erro: A biblioteca UUID não está carregada.');
            return null;
        }
    }

    const form = document.getElementById('formulario');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const passwordField = document.getElementById('password-field');
        const password = passwordField.value;

        const device_id = generateDeviceId();

        const response = await fetch(`http://192.168.0.34:5000/authenticate/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `password=${encodeURIComponent(password)}`,
        });

        if (response.ok) {
            const data = await response.text();
            console.log(data);
            window.location.href = '/index'
        } else {
            console.error('Erro na solicitação:', response.status);
        }
    });
});
