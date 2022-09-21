const getCustomerUrl = 'https://mintic-bancoproj-g1.herokuapp.com/read/';
//const getCustomerUrl = ' http://127.0.0.1:8000/read/';

function getCustomer() {
  const parsedUrl = new URL(window.location.href);
  //console.log(parsedUrl);
  const id = parsedUrl.searchParams.get("id");
  //console.log(id);
  const accessToken = sessionStorage.getItem('accessToken')
  const refreshToken = sessionStorage.getItem('refreshToken')
  console.log('Acá va: ' + accessToken)
  console.log('Acá va: ' + refreshToken)

  fetch(getCustomerUrl + id, {
    headers: {
      "Authorization": "Bearer " + accessToken
    }
  })
    .then(response => {
      if (response.ok || response.status == 400) {
        return response.text()
      } else {
        throw new Error(response.status)
      }
    })
    .then(data => {
      console.log(data);
      if (data.includes("No existe un usuario con ese documento")) {
        handleError(data);
      }
      const customer = JSON.parse(data);
      handleCustomer(customer);
    })
    .catch(err => {
      console.log("Error: " + err);
      handleError();
    });
}

function handleCustomer(customer) {
  const accDivs = [];
  customer.accounts.forEach((acc) => {
    const accDiv = `
      <h4>Número de cuenta: ${acc.number}</h4>
      <h4>Saldo: ${acc.balance}</h4>`;
    accDivs.push(accDiv);
  });
  const custDiv = document.createElement("div");
  custDiv.innerHTML =
    `<h3>Nombre: ${customer.firstName}</h3>
    <h3>Apellido: ${customer.lastName}</h3>
    <h3>Cédula: ${customer.id}</h3>
    <h3>Cuentas:</h3>`;
  accDivs.forEach(accDiv => custDiv.innerHTML += accDiv);

  document.getElementById("cargando").remove();
  const info = document.getElementById("info-customers");
  info.appendChild(custDiv);
}

function handleError(err) {
  document.getElementById("cargando").remove();
  const message = document.createElement("p");
  if (err) {
    message.innerHTML = err;
  } else {
    message.innerHTML = "No se pudo cargar la información. Intente luego.";
  }
  const info = document.getElementById("info-customers");
  info.appendChild(message);
}

// ---------------------------------

document.addEventListener("DOMContentLoaded", getCustomer);