function handleActionClick(e) {
    e.preventDefault(); // Prevent the default action
    var action = $(this).data("action");
    var href = $(this).attr("href");

    switch (action) {
        case "view":
        case "edit":
            window.location.href = href;
            break;
        case "delete":
            confirmAndDelete(href);
            break;
        default:
            console.warn("Unknown action:", action);
    }
}

function confirmAndDelete(href) {
    Swal.fire({
        title: "Tem certeza?",
        text: "Você tem certeza que deseja excluir esse item?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sim, exclua!",
        cancelButtonText: "Canelar",
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: href,
                type: "DELETE",
                success: function (result) {
                    Swal.fire("Excluído!", "Item excluído com sucesso", "success").then((result) =>
                        window.location.reload()
                    );
                },
                error: function (xhr, status, error) {
                    console.error("Erro deletando item:", error);
                    Swal.fire("Erro!", "Erro deletendo item: " + error, "error");
                },
            });
        }
    });
}

function formatValue(value, arg) {
    switch (arg) {
        case "currency":
            return `R$ ${
                value ? value.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : "0,00"
            }`;
        case "data":
            return value ? new Date(value).toLocaleDateString("pt-BR") : "";
        case "datetime":
            return value ? new Date(value).toLocaleString("pt-BR") : "";
        case "decimal":
            return `R$ ${
                value ? value.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : "0,00"
            }`;
        case "time":
            return value ? new Date(value).toLocaleTimeString("pt-BR") : "";
        case "integer":
            return value ? value : 0;
        case "percent":
            return `${
                value ? value.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : "0,00"
            } %`;
        case "boolean":
            return `<input class="form-check-input" type="checkbox" ${value ? "checked" : ""} onclick="return false;">`;
        default:
            return value;
    }
}

function get_action_button(item, action, url) {
    switch (action) {
        case "edit":
            return `<a href="${url}/${item.id}" class="btn btn-primary btn-sm action" data-action="${action}"><i class="fas fa-edit"></i></a>`;
        case "delete":
            return `<a href="${url}/${item.id}" class="btn btn-danger btn-sm action" data-action="${action}"><i class="fas fa-trash"></i></a>`;
        default:
            return "";
    }
}

async function get_lookup_value(endpoint, id, traducao) {
    const _endpoint = endpoint + id;
    try {
        const data = await $.get(_endpoint);
        return traducao ? data[traducao] : data.name;
    } catch (error) {
        console.error("Error:", error);
        return "";
    }
}

async function handleTableData(table, data) {
    table.find("tbody").empty();
    for (const item of data) {
        var row = "<tr>";
        for (const th of table.find("thead th")) {
            const fieldName = $(th).data("field");
            const format_type = $(th).data("format");
            const lookup_url = $(th).data("lookup-url");
            const lookup_traducao = $(th).data("lookup-traducao");
            if (item.hasOwnProperty(fieldName)) {
                if (lookup_url) {
                    const lookup_value = await get_lookup_value(lookup_url, item[fieldName], lookup_traducao);
                    row += "<td>" + lookup_value + "</td>";
                } else {
                    row += "<td>" + formatValue(item[fieldName], format_type) + "</td>";
                }
            } else if (fieldName == "actions") {
                const action_list = $(th).data("actions");
                if (action_list) {
                    row += "<td>";
                    action_list
                        .split(";")
                        .filter((action) => action)
                        .forEach((action) => {
                            const action_url = action != "delete" ? table.data("form-url") : table.data("api-url");
                            row += get_action_button(item, action, action_url);
                        });
                    row += "</td>";
                }
            } else {
                row += "<td></td>";
                console.log('Campo "' + fieldName + '" não encontrado no JSON.');
            }
        }
        row += "</tr>";
        table.find("tbody").append(row);
    }
}

function loadTableData(table) {
    const url = table.data("table-url");
    $.ajax({
        url: url,
        method: "GET",
        success: function (data) {
            console.log(data);
            handleTableData(table, data["data"]);
        },
        error: function (err) {
            console.error("Erro ao carregar dados da tabela:", err);
            showToast("Erro ao carregar dados da tabela: " + err, "bg-danger");
        },
    });
}

$(document).ready(function () {
    $("table[data-table-url]").each(function () {
        loadTableData($(this));
    });

    $("body").on("click", ".action", handleActionClick);
});
