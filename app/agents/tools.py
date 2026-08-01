from app.models.models import Habit, JobOffer

from app.services.scraper import buscar_ofertas_remotive

from app.services.services import marcar_completado_hoy



def tool_crear_habito(nombre: str, descripcion: str = None, db=None, usuario=None):
    """Crea un nuevo hábito para el usuario autenticado."""
    nuevo = Habit(nombre=nombre, descripcion=descripcion, usuario_id=usuario.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return f"✅ Hábito '{nombre}' creado con éxito."

def tool_completar_habito(nombre: str, db=None, usuario=None):
    """Marca un hábito como completado HOY (busca por nombre exacto)."""

    habito = db.query(Habit).filter(
        Habit.nombre == nombre,
        Habit.usuario_id == usuario.id
    ).first()

    if not habito:
        return f"❌ No encontré el hábito '{nombre}'."

    marcar_completado_hoy(db, habito.id)

    return f"✅ Hábito '{nombre}' completado hoy."

def tool_eliminar_habito(nombre: str, db=None, usuario=None):
    """Elimina un hábito (busca por nombre exacto)."""
    habito = db.query(Habit).filter(Habit.nombre == nombre, Habit.usuario_id == usuario.id).first()
    if not habito:
        return f"❌ No encontré el hábito '{nombre}'."
    db.delete(habito)
    db.commit()
    return f"🗑️ Hábito '{nombre}' eliminado."

def tool_scrapear_ofertas(palabra: str, db=None, usuario=None):
    """Busca ofertas reales en Remotive y las guarda en PostgreSQL."""

    ofertas = buscar_ofertas_remotive(
        palabra,
        max_ofertas=5
    )

    if not ofertas:
        return f"No encontré ofertas para {palabra}"

    if "error" in ofertas[0]:
        return ofertas[0]["error"]

    nuevas_guardadas = 0
    resultado = ""

    for i, oferta in enumerate(ofertas, 1):

        resultado += f"""
    {i}. {oferta['titulo']}
    Empresa: {oferta['empresa']}
    Categoría: {oferta['categoria']}
    Salario: {oferta['salario']}
    Tags: {oferta['tags']}
    Link: {oferta['enlace']}

    """

        existe = db.query(JobOffer).filter(
            JobOffer.enlace == oferta["enlace"],
            JobOffer.usuario_id == usuario.id
        ).first()

        if existe:
            continue

        nueva_oferta = JobOffer(
            titulo=oferta["titulo"],
            empresa=oferta["empresa"],
            categoria=oferta["categoria"],
            salario=oferta["salario"],
            tags=oferta["tags"],
            enlace=oferta["enlace"],
            usuario_id=usuario.id
        )

        db.add(nueva_oferta)
        nuevas_guardadas += 1

    db.commit()

    nombre_habito = f"Revisar ofertas de {palabra}"

    existe = db.query(Habit).filter(
        Habit.nombre == nombre_habito,
        Habit.usuario_id == usuario.id
    ).first()

    if not existe:
        tool_crear_habito(
            nombre=nombre_habito,
            descripcion=f"{len(ofertas)} ofertas encontradas en Remotive",
            db=db,
            usuario=usuario
        )

    return (
        f"🔎 Encontradas: {len(ofertas)}\n"
        f"💾 Nuevas guardadas: {nuevas_guardadas}\n\n"
        + resultado
    )

def tool_consultar_documento(
    consulta: str,
    db=None,
    usuario=None,
):
    """
    Consulta los documentos del usuario usando el RAG.
    """

    from app.services.rag_service import answer_query

    return answer_query(
        consulta=consulta,
        usuario_id=usuario.id,
    )

TOOLS_MAP = {
    "crear_habito": tool_crear_habito,
    "completar_habito": tool_completar_habito,
    "eliminar_habito": tool_eliminar_habito,
    "scrapear_ofertas": tool_scrapear_ofertas,
    "consultar_documento": tool_consultar_documento,
}

