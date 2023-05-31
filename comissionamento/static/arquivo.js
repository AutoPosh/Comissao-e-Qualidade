            // Função para filtrar os itens da tabela por nome e idade
            function filterTable() {
                var nameFilterInput = document.getElementById("nameFilterInput");
                var nameFilterValue = nameFilterInput.value.toUpperCase();
                var ageFilterInput = document.getElementById("ageFilterInput");
                var ageFilterValue = ageFilterInput.value.toUpperCase();
                var table = document.querySelector(".table-container table");
                var rows = table.getElementsByTagName("tr");

                for (var i = 1; i < rows.length; i++) {
                    var cells = rows[i].getElementsByTagName("td");
                    var nameCellValue = cells[0].textContent || cells[0].innerText;
                    var ageCellValue = cells[1].textContent || cells[1].innerText;
                    var display = true;

                    if (nameFilterValue && nameCellValue.toUpperCase().indexOf(nameFilterValue) === -1) {
                        display = false;
                    }

                    if (ageFilterValue && ageCellValue.toUpperCase().indexOf(ageFilterValue) === -1) {
                        display = false;
                    }

                    rows[i].style.display = display ? "" : "none";
                }
            }

            // Função para filtrar os itens da tabela por data de nascimento
            function filterTableByDate() {
                var dateFilterStart = document.getElementById("dateFilterStart").value;
                var dateFilterEnd = document.getElementById("dateFilterEnd").value;
                var table = document.querySelector(".table-container table");
                var rows = table.getElementsByTagName("tr");

                var startDate = new Date(dateFilterStart);
                var endDate = new Date(dateFilterEnd);

                for (var i = 1; i < rows.length; i++) {
                    var cells = rows[i].getElementsByTagName("td");
                    var dateCellValue = cells[2].textContent || cells[2].innerText;
                    var birthDate = new Date(dateCellValue);
                    var display = true;

                    if (dateFilterStart && birthDate < startDate) {
                        display = false;
                    }

                    if (dateFilterEnd && birthDate > endDate) {
                        display = false;
                    }

                    rows[i].style.display = display ? "" : "none";
                }
            }


            // Função para ordenar a tabela por ordem alfabética
            function sortTable() {
                var table = document.querySelector(".table-container table");
                var rows = Array.from(table.getElementsByTagName("tr")).slice(1); // Ignora a primeira linha (cabeçalho)

                rows.sort(function (a, b) {
                    var nameA = a.getElementsByTagName("td")[0].textContent || a.getElementsByTagName("td")[0].innerText;
                    var nameB = b.getElementsByTagName("td")[0].textContent || b.getElementsByTagName("td")[0].innerText;

                    return nameA.localeCompare(nameB);
                });

                rows.forEach(function (row) {
                    table.appendChild(row);
                });
            }

            // Adiciona os ouvintes de eventos aos elementos
            document.getElementById("nameFilterInput").addEventListener("keyup", filterTable);
            document.getElementById("ageFilterInput").addEventListener("keyup", filterTable);
            document.getElementById("dateFilterStart").addEventListener("change", filterTableByDate);
            document.getElementById("dateFilterEnd").addEventListener("change", filterTableByDate);
            document.getElementById("sortButton").addEventListener("click", sortTable);
