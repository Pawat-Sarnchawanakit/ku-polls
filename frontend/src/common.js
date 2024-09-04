export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function log_out() {
    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", getCookie("csrftoken"));
    fetch(window.location.protocol + "//" + window.location.host + "/accounts/logout/", {
        method: 'POST',
        redirect: 'follow',
        body: formData
    }).then(response => {
        if (response.redirected)
            window.location.href = response.url;
    });
}

export function login() {
    window.location.href = window.location.protocol + "//" + window.location.host + "/accounts/login/?next=" + window.location.pathname
}