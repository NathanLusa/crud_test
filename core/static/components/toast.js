function showToast(text, color) {
    const toastLiveExample = document.getElementById("liveToast");
    const toastBody = $(".toast-body");
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);

    toastBody.html(text);
    $(toastBootstrap._element).find("#toast-color").removeClass("bg-primary");
    $(toastBootstrap._element).find("#toast-color").removeClass("bg-danger");
    $(toastBootstrap._element).find("#toast-color").removeClass("bg-success");
    $(toastBootstrap._element).find("#toast-color").addClass(color);

    toastBootstrap.show();
}
