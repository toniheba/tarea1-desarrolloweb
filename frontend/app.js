const API_URL = "/estudiantes";
const btn_guardar = document.getElementById("btnguardar");
const formulario = document.getElementById("formulario");
const tabla = document.getElementById("tabla_estudiantes");


async function getEstudiantesPaginado(skip=0, limit=10){
    tabla.innerHTML = ""
    const response = await fetch(`${API_URL}?skip=${skip}&limit=${limit}`);
    if (response.ok){
        const data = await response.json();
        const estudiantes = data.detail
        estudiantes.forEach(estudiante => {
            const tr = document.createElement("tr")
            tr.innerHTML = `
                <td> ${estudiante.matricula || ""} </td>
                <td> ${estudiante.nombre || ""} </td>
                <td> ${estudiante.apellido || ""} </td>
                <td> ${estudiante.genero || ""} </td>
                <td> ${estudiante.direccion || ""} </td>
                <td> ${estudiante.telefono || ""} </td>
            `;
            tabla.appendChild(tr);
        });

        let paginacion = documento.getElementById("paginacion");
        if (!paginacion){
            paginancion = document.createElement("div");
            paginancion.id = "paginacion";
            tabla.parentElement.appendChild(paginacion);
        }
        paginacion.innerHTML=`
            <button ${!data.previus ? "disable" : ""} id="back_btn">Anterior</button>
            <span>${skip + 1} - ${Math.min(skip+limit, data.count)} de ${data.count}</span>
            <button ${!data.next ? "disable" : ""} id="next_btn">Siguiente</button>
        `;

        if(data.previus){
            document.getElementById("back_btn").onclick = () =>{
                const url = new URL(data.previus);
                getEstudiantesPaginado(Numbre(url.searchParams.get("skip")), Number(url.searchParams.get("limit")))
            };
        }

        if(data.next){
            document.getElementById("next_btn").onclick = () =>{
                const url = new URL(data.next);
                getEstudiantesPaginado(Numbre(url.searchParams.get("skip")), Number(url.searchParams.get("limit")))
            };
        }


    }
}

btn_guardar.onclick = async (event) => {
    event.preventDefault();
    const estudiante = {
        matricula: document.getElementById("matricula")?.value || "",
        nombre: document.getElementById("nombre")?.value || "",
        apellidos: document.getElementById("apellidos")?.value || "",
        genero: document.getElementById("genero")?.value || "",
        direccion: document.getElementById("direccion")?.value || "",
        telefono: document.getElementById("telefono")?.value || ""
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
    getEstudiantesPaginado();
}

getEstudiantesPaginado();
