function get_lookup_item(lookup_id, item) {
    return `<li class="list-group-item lookup-item" 
                data-lookup="${lookup_id}"
                data-value="${item.value}"
                ${Object.keys(item.attrs)
                    .map((key) => `data-${key}="${item.attrs[key]}"`)
                    .join("")}>${item.desc}</li>`;
}

function lookup_list_hide(lookup_list, clear = true) {
    lookup_list.innerHTML = clear ? "" : lookup_list.innerHTML;
    lookup_list.style.display = "none";
}

function lookup_focus_out(event) {
    // console.log(event);
    const lookup_list = document.getElementById(this.id + "-list");
    lookup_list_hide(lookup_list, false);
}

function lookup_item_onclick(event) {
    const selected_item = $(event.target);
    const lookup_id = "#" + selected_item.data("lookup");
    const label = selected_item.data("value") + " - " + selected_item.text();

    $(lookup_id).attr("data-selected-id", selected_item.data("value"));
    $(lookup_id).val(label);
}

function navigate_items(key, items) {
    let currentIndex = items.index(items.filter(".lookup-item-highlight"));
    items.removeClass("lookup-item-highlight");

    if (key === 40) {
        // Down arrow
        currentIndex = (currentIndex + 1) % items.length;
    } else if (key === 38) {
        // Up arrow
        currentIndex = (currentIndex - 1 + items.length) % items.length;
    }

    items.eq(currentIndex).addClass("lookup-item-highlight");
}

function lookup_keyup(event) {
    const lookup = this;
    const input_value = this.value;
    const lookup_list = document.getElementById(this.id + "-list");
    const items = $(lookup_list).find(".lookup-item");
    const selectedItem = document.getElementsByClassName("lookup-item-highlight");

    if (event.which === 38 || event.which === 40) {
        navigate_items(event.which, items);
        return;
    }

    if (event.which === 13 && selectedItem.length > 0) {
        $(selectedItem[0]).trigger("mousedown");
        lookup_list_hide(lookup_list, false);
        return;
    }

    if (event.which === 13 || input_value.length >= 3) {
        const endpoint = $(this).data("lookup-url");

        let params = {};
        if (input_value != "") {
            params["find"] = input_value;
        }

        $.get(endpoint, params, function (data) {
            lookup_list_hide(lookup_list);
            $(lookup).removeAttr("data-selected-id");
            data.forEach((item) => (lookup_list.innerHTML += get_lookup_item(lookup.id, item)));
            lookup_list.style.display = data.length > 0 ? "block" : "none";

            $(".lookup-item").on("mousedown", lookup_item_onclick);
        }).fail(function (error) {
            console.error("Error:", error);
            $(lookup).removeAttr("data-selected-id");
            lookup_list_hide(lookup_list);
        });
    } else {
        $(lookup).removeAttr("data-selected-id");
        lookup_list_hide(lookup_list);
    }
}

$(document).ready(function () {
    $("input[data-lookup-url]").keyup(lookup_keyup);
    $("input[data-lookup-url]").blur(lookup_focus_out);
    $("input[data-lookup-url]").focus((event) => $(event.target).select());
});
