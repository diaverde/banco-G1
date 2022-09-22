const getCustomersUrl = 'https://mintic-bancoproj-g1.herokuapp.com/read';
//const getCustomersUrl = ' http://127.0.0.1:8000/read';

let customers = [];

function getCustomers() {
  fetch(getCustomersUrl)
    .then(response => {
      if (response.ok) {
        return response.text()
      } else {
        throw new Error(response.status)
      }
    })
    .then(data => {
      console.log(data);
      customers = JSON.parse(data);
      handleCustomers();
    })
    .catch(err => {
      console.log("Error: " + err);
      handleError();
    });
}

function handleCustomers() {
  const divs = [];
  customers.forEach((cust) => {
    const div = document.createElement("div");
    div.innerHTML =
      `<h3>Nombre: ${cust.firstName}</h3>
      <h3>Apellido: ${cust.lastName}</h3>
      <h3>Cédula: ${cust.id}</h3>`;
    divs.push(div);
  });
  document.getElementById("cargando").remove();
  const info = document.getElementById("info-customers");
  divs.forEach(div => info.appendChild(div));
}

function handleError() {
  document.getElementById("cargando").remove();
  const message = document.createElement("p");
  message.innerHTML = "No se pudo cargar la información. Intente luego.";
  const info = document.getElementById("info-customers");
  info.appendChild(message);
}

// ---------------------------------

document.addEventListener("DOMContentLoaded", getCustomers);