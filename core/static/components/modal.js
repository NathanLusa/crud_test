$(document).ready(function () {
    // Evento disparado quando o modal é totalmente exibido
    $(".modal").on("shown.bs.modal", function (e) {
        console.log("aqui", e);

        // Buscar a div com a class modal-body
        var modalBody = $(this).find(".modal-body");
        // Pegar o data attribute com nome data-url-body
        var url = modalBody.data("url-body");

        // Fazer uma requisição AJAX para o endereço
        $.ajax({
            url: url,
            method: "GET",
            success: function (response) {
                // Adicionar o HTML retornado dentro da modal-body
                console.log(response);
                // modalBody.html(response.body || JSON.stringify(response));
                modalBody.html(response);

                document_ready_form();
            },
            error: function () {
                modalBody.html("Erro ao carregar o conteúdo.");
            },
        });
    });
});
