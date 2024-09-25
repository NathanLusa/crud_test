function handleFormSubmit(event) {
    event.preventDefault();
    var formData = $(this).serializeArray();
    var data = serializeFormData(formData, $(this));

    console.log(data);

    showOverlay();

    $.ajax({
        url: $(this).attr("action"),
        method: $(this).attr("method"),
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
            console.log("Sucesso:", response);
            Swal.fire({
                title: "Success",
                text: "Form submitted successfully",
                icon: "success",
                confirmButtonText: "OK",
                confirmButtonColor: "#3085d6",
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = "/";
                }
            });
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Erro:", textStatus, errorThrown);
            Swal.fire({
                title: "Error",
                // text: jqXHR.responseJSON.detail,
                text: errorThrown,
                icon: "error",
                confirmButtonText: "OK",
                confirmButtonColor: "#d33",
            });
        },
        complete: function () {
            hideOverlay();
        },
    });
}

function serializeFormData(formData, form) {
    var data = {};

    // Convert form data to JSON object
    $.each(formData, function (index, item) {
        data[item.name] = item.value;
    });

    // Include checkbox values
    form.find('input[type="checkbox"]').each(function () {
        data[this.name] = this.checked;
    });

    // Incluir valores de inputs com atributo data-selected-id
    form.find("input[data-selected-id]").each(function () {
        data[this.name] = $(this).attr("data-selected-id");
    });

    return data;
}

function document_ready_form() {
    $("form[data-post-type]").on("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            return false;
        }
    });

    $("form[data-post-type]").on("submit", handleFormSubmit);
}

$(document).ready(function () {
    document_ready_form();
});
