// Função para formatar o CPF ou CNPJ
function formatCPForCNPJ(input) {
    var value = input.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    var formattedValue = '';

    if (value.length <= 11) {
        // Formata como CPF (ex: 123.456.789-01)
        formattedValue = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    } else {
        // Formata como CNPJ (ex: 12.345.678/0001-90)
        formattedValue = value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
    }

    input.value = formattedValue;
}

window.addEventListener('DOMContentLoaded', function () {
    var cpfField = document.getElementById('cpf-field');
    cpfField.addEventListener('input', function () {
        formatCPForCNPJ(this);
    });
});

function openModal() {
    var modal = document.getElementById('success-modal');
    if (modal) {
        var myInput = document.getElementById('myInput');

        modal.addEventListener('shown.bs.modal', function () {
            myInput.focus();
        });

        var modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();
    } else {
        console.error("O elemento com ID 'success-modal' não foi encontrado.");
    }
}
