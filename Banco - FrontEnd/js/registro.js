//const newCustomerUrl = 'https://mintic-bancoproj-g1.herokuapp.com/new';
const newCustomerUrl = ' http://127.0.0.1:8000/new';

function validar_nombre_apellido(val) {
    const letters = /^[A-Z a-zÁÉÍÓÚáéíóúñ]+$/;
    if (val.match(letters))
        return true;
    else
        return false;
}

function validar_cedula(val) {
    if (Number(val) > 1000)
        return true;
    else
        return false;
}

function validar_contrasena(val) {
    if (val.length >= 5)
        return true;
    else
        return false;
}

function collectData(evt) {
    evt.preventDefault();

    const id = document.registro.id.value;
    const firstName = document.registro.firstName.value.trim();
    const lastName = document.registro.lastName.value.trim();
    const email = document.registro.email.value.trim();
    const password = document.registro.password.value;

    let result = validar_nombre_apellido(firstName);
    if (!result) {
        alert('Nombre no válido');
        return;
    }
    result = validar_nombre_apellido(lastName);
    if (!result) {
        alert('Apellido no válido');
        return;
    }
    result = validar_cedula(id);
    if (!result) {
        alert('Cédula no válida');
        return;
    }
    result = validar_contrasena(password);
    if (!result) {
        alert('Contraseña no válida. Deben ser al menos 5 caracteres');
        return;
    }

    const customer = {
        id: id,
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password
    }
    console.log(customer);
    /*
    alert(`Usuario registrado con los siguientes datos:
        ${customer.firstName} ${customer.lastName} ${customer.id}`);
    */

    const dataToSend = JSON.stringify(customer);
    sendData(dataToSend);
}

function sendData(data) {
    fetch(newCustomerUrl, {
        method: "POST",
        headers: {
            "Content-Type": "text/json"
        },
        body: data
    })
        .then(response => {
            if (response.ok) {
                return response.text()
            } else {
                throw new Error(response.status)
            }
        })
        .then(data => {
            console.log(data);
            handleSuccess();
        })
        .catch(err => {
            console.log("Error: " + err);
            handleError();
        });
}

function handleSuccess() {
    document.getElementById("formData").remove();
    const message = document.createElement("p");
    message.innerHTML = "Cliente creado exitosamente.";
    const info = document.getElementById("info");
    info.appendChild(message);
}

function handleError() {
    document.getElementById("formData").remove();
    const message = document.createElement("p");
    message.innerHTML = "No se pudo crear el cliente. Intente luego.";
    const info = document.getElementById("info");
    info.appendChild(message);
}

// ---------------------------------

document.registro.addEventListener('submit', collectData);