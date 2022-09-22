const updateCustomerUrl = 'https://mintic-bancoproj-g1.herokuapp.com/update/';
//const updateCustomerUrl = ' http://127.0.0.1:8000/update/';

const userId = sessionStorage.getItem('clientId');

function validar_nombre_apellido(val) {
    const letters = /^[A-Z a-zÁÉÍÓÚáéíóúñ]+$/;
    if (val.match(letters))
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

    const firstName = document.actualizar.firstName.value.trim();
    const lastName = document.actualizar.lastName.value.trim();
    const email = document.actualizar.email.value.trim();
    const password = document.actualizar.password.value;

    let result = true
    if (firstName) {
        result = validar_nombre_apellido(firstName);
        if (!result) {
            alert('Nombre no válido');
            return;
        }
    }
    if (lastName) {
        result = validar_nombre_apellido(lastName);
        if (!result) {
            alert('Apellido no válido');
            return;
        }
    }
    if (password) {
        result = validar_contrasena(password);
        if (!result) {
            alert('Contraseña no válida. Deben ser al menos 5 caracteres');
            return;
        }
    }

    const customer = {}

    if (firstName)
        customer.firstName = firstName;
    if (lastName)
        customer.lastName = lastName;
    if (email)
        customer.email = email;
    if (password)
        customer.password = password;

    console.log(customer);

    const dataToSend = JSON.stringify(customer);
    sendData(dataToSend);
}

function sendData(data) {
    accessToken = sessionStorage.getItem('accessToken');

    fetch(updateCustomerUrl + userId, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + accessToken
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
            alert('Datos actualizados');
            goBack();
        })
        .catch(err => {
            console.log("Error: " + err);
            alert('Error al actualizar datos');
            goBack();
        });
}

function goBack() {
    window.location.href = './cliente.html?id=' + userId;
}

function showOldData() {
    const oldFName = sessionStorage.getItem('fname');
    const oldLName = sessionStorage.getItem('lname');
    const oldEmail = sessionStorage.getItem('email');

    document.actualizar.firstName.placeholder = oldFName;
    document.actualizar.lastName.placeholder = oldLName;
    document.actualizar.email.placeholder = oldEmail;
}

// ---------------------------------

document.actualizar.addEventListener('submit', collectData);
document.addEventListener('DOMContentLoaded', showOldData);