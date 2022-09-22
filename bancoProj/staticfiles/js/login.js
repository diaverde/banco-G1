const loginUrl = 'https://mintic-bancoproj-g1.herokuapp.com/login';
//const loginUrl = ' http://127.0.0.1:8000/login';

function collectData(evt) {
    evt.preventDefault();

    const email = document.login.email.value.trim();
    const password = document.login.password.value;

    const customer = {
        email: email,
        password: password
    }
    console.log(customer);
    const dataToSend = JSON.stringify(customer);
    sendData(dataToSend);
}

function sendData(data) {
    fetch(loginUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: data
    })
        .then(response => {
            if (response.ok || response.status == 401) {
                return response.text()
            } else {
                throw new Error(response.status)
            }
        })
        .then(data => {
            console.log(data);
            if (data.includes("Credenciales inválidas"))
                handleError(data)
            else
                handleSuccess(JSON.parse(data));
        })
        .catch(err => {
            console.log("Error: " + err);
            handleError();
        });
}

function handleSuccess(data) {
    document.getElementById("formData").remove();
    const message = document.createElement("p");
    message.innerHTML = "Ingreso exitoso. Accediendo a su información...";
    const info = document.getElementById("info");
    info.appendChild(message);
    //console.log(data.access)
    //console.log(data.refresh)
    sessionStorage.setItem('accessToken', data.access)
    sessionStorage.setItem('refreshToken', data.refresh)
    sessionStorage.setItem('clientId', data.id)
    window.location.href = './cliente.html?id=' + data.id;
}

function handleError(err) {
    document.getElementById("formData").remove();
    const message = document.createElement("p");
    if (err)
        message.innerHTML = err;
    else
        message.innerHTML = "No se pudo ingresar. Intente luego.";
    const info = document.getElementById("info");
    info.appendChild(message);
}

// ---------------------------------

document.login.addEventListener('submit', collectData);