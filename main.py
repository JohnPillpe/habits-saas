from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import get_db, Base, engine
from models import Habit
from schemas import HabitCreate, HabitResponse
from services import habit_to_response, marcar_completado_hoy


app = FastAPI(title="Seguimiento de Hábitos")
Base.metadata.create_all(bind=engine)


@app.get("/habits", response_model=list[HabitResponse])
def listar_habitos(db: Session = Depends(get_db)):
    habitos = db.query(Habit).order_by(Habit.creado_en.desc()).all()
    return [habit_to_response(habito) for habito in habitos]


@app.post("/habits", response_model=HabitResponse, status_code=201)
def crear_habito(habito: HabitCreate, db: Session = Depends(get_db)):
    nombre = habito.nombre.strip()

    if not nombre:
        raise HTTPException(
            status_code=400,
            detail="El nombre es obligatorio"
        )

    nuevo = Habit(
        nombre=nombre,
        descripcion=habito.descripcion.strip()
        if habito.descripcion else None,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return habit_to_response(nuevo)


@app.post("/habits/{habito_id}/complete", response_model=HabitResponse)
def completar_habito_hoy(
    habito_id: int,
    db: Session = Depends(get_db)
):
    habito = db.query(Habit).filter(Habit.id == habito_id).first()

    if not habito:
        raise HTTPException(
            status_code=404,
            detail="Hábito no encontrado"
        )

    marcar_completado_hoy(db, habito_id)

    db.refresh(habito)

    return habit_to_response(habito)


@app.get("/", response_class=HTMLResponse)
def pagina_principal():
    return HTMLResponse(content=HTML_PAGE)
    
HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Seguimiento de Hábitos</title>

    <link 
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" 
        rel="stylesheet"
    >

    <style>
        body {
            background-color: #f8f9fa;
        }

        .streak-badge {
            min-width: 3rem;
        }
    </style>
</head>


<body>

<div class="container py-5">

    <h1 class="mb-4">
        Seguimiento de Hábitos
    </h1>


    <div id="alert-container"></div>


    <div class="card mb-4">

        <div class="card-header">
            Nuevo hábito
        </div>


        <div class="card-body">

            <form id="form-nuevo-habito" class="row g-3">

                <div class="col-md-5">

                    <input 
                        id="nombre"
                        class="form-control"
                        placeholder="Nombre del hábito"
                        required
                    >

                </div>


                <div class="col-md-5">

                    <input 
                        id="descripcion"
                        class="form-control"
                        placeholder="Descripción"
                    >

                </div>


                <div class="col-md-2">

                    <button class="btn btn-primary w-100">
                        Añadir
                    </button>

                </div>

            </form>

        </div>

    </div>



    <div class="card">

        <div class="card-header">
            Mis hábitos
        </div>


        <div class="table-responsive">

            <table class="table table-hover mb-0">


                <thead class="table-light">

                    <tr>

                        <th>
                            Hábito
                        </th>

                        <th class="text-center">
                            Racha
                        </th>

                        <th class="text-center">
                            Total días
                        </th>


                        <th class="text-center">
                            Último registro
                        </th>


                        <th>
                            Acción
                        </th>


                    </tr>

                </thead>


                <tbody id="tabla-habitos">

                </tbody>


            </table>

        </div>

    </div>


</div>
<script>

const alertContainer = document.getElementById("alert-container");
const tablaHabitos = document.getElementById("tabla-habitos");
const formNuevoHabito = document.getElementById("form-nuevo-habito");



function mostrarAlerta(mensaje, tipo="success") {

    alertContainer.innerHTML = `
        <div class="alert alert-${tipo} alert-dismissible fade show">
            ${mensaje}

            <button 
                type="button" 
                class="btn-close" 
                data-bs-dismiss="alert">
            </button>

        </div>
    `;

}



function escaparHtml(texto) {

    const div = document.createElement("div");

    div.textContent = texto ?? "";

    return div.innerHTML;

}




async function cargarHabitos() {


    const respuesta = await fetch("/habits");


    const habitos = await respuesta.json();


    tablaHabitos.innerHTML = habitos.map(h => `


        <tr>


            <td>

                <strong>
                    ${escaparHtml(h.nombre)}
                </strong>


                <br>

                <small class="text-muted">
                    ${h.descripcion ?? ""}
                </small>


            </td>



            <td class="text-center">

                <span class="badge bg-warning">

                    ${h.racha_actual}

                </span>


            </td>



            <td class="text-center">

                <span class="badge bg-info">

                    ${h.total_completados}

                </span>

            </td>



            <td class="text-center">

                ${h.ultimo_registro ?? "Nunca"}

            </td>



            <td>


                <button
                    class="btn btn-success btn-sm"
                    onclick="completarHabito(${h.id})">

                    Completar hoy

                </button>


            </td>


        </tr>


    `).join("");

}




async function completarHabito(id) {


    const respuesta = await fetch(
        `/habits/${id}/complete`,
        {
            method:"POST"
        }
    );


    const habito = await respuesta.json();


    mostrarAlerta(
        `"${habito.nombre}" completado correctamente`
    );


    cargarHabitos();


}




formNuevoHabito.addEventListener(
"submit",
async function(e){


    e.preventDefault();


    const nombre =
        document.getElementById("nombre").value;


    const descripcion =
        document.getElementById("descripcion").value;



    await fetch(
        "/habits",
        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },


            body:JSON.stringify({

                nombre:nombre,

                descripcion:descripcion

            })

        }
    );


    formNuevoHabito.reset();


    mostrarAlerta(
        "Hábito creado correctamente"
    );


    cargarHabitos();


});



cargarHabitos();


</script>


<script 
src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js">
</script>


</body>

</html>

"""