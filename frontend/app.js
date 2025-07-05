const API_URL = "http://127.0.0.1:8000/estudiantes/";
const btn_guardar = document.getElementById("btnguardar")
const formulario = document.getElementById("formulario")

btn_guardar.onclick = async (event) => {
    event.preventDefault();
    const estudiante = {
        matricula: document.getElementById("matricula").value,
        nombre: document.getElementById("nombre").value,
        apellidos: document.getElementById("apellidos").value,
        genero: document.getElementById("genero").value,
        direccion: document.getElementById("direccion").value,
        telefono: document.getElementById("telefono").value
       };
       console.log(estudiante)
       //REQUEST - solicitud, enviar datos (generalmente desde el front)
       //RESPONSE - respuesta, obtener datos(generalmente desde el back)
       await fetch(
        API_URL, 
        {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(estudiante)
       }
    )
    .then(response => response.json())
    .then(response => console.log(response))
    .catch(err => console.error(err));
    formulario.reset();
}