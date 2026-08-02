[35mapp/agents/tools.py[m[36m:[mfrom app.models.models import [1;31mHabit[m, JobOffer
[35mapp/agents/tools.py[m[36m:[m    nuevo = [1;31mHabit[m(nombre=nombre, descripcion=descripcion, usuario_id=usuario.id)
[35mapp/agents/tools.py[m[36m:[m    habito = db.query([1;31mHabit[m).filter(
[35mapp/agents/tools.py[m[36m:[m        [1;31mHabit[m.nombre == nombre,
[35mapp/agents/tools.py[m[36m:[m        [1;31mHabit[m.usuario_id == usuario.id
[35mapp/agents/tools.py[m[36m:[m    habito = db.query([1;31mHabit[m).filter([1;31mHabit[m.nombre == nombre, [1;31mHabit[m.usuario_id == usuario.id).first()
[35mapp/agents/tools.py[m[36m:[m    existe = db.query([1;31mHabit[m).filter(
[35mapp/agents/tools.py[m[36m:[m        [1;31mHabit[m.nombre == nombre_habito,
[35mapp/agents/tools.py[m[36m:[m        [1;31mHabit[m.usuario_id == usuario.id
[35mapp/schemas/schemas.py[m[36m:[mclass [1;31mHabit[mCreate(BaseModel):
[35mapp/schemas/schemas.py[m[36m:[mclass [1;31mHabit[mUpdate(BaseModel):
[35mapp/schemas/schemas.py[m[36m:[mclass [1;31mHabit[mResponse(BaseModel):
[35mapp/services/services.py[m[36m:[mfrom app.models.models import [1;31mHabit[m, Registro
[35mapp/services/services.py[m[36m:[mdef obtener_estadisticas_habito(habito: [1;31mHabit[m) -> tuple[int, int]:
[35mapp/services/services.py[m[36m:[m    habito = db.query([1;31mHabit[m).filter(
[35mapp/services/services.py[m[36m:[m        [1;31mHabit[m.id == habito_id
[35mtemplates/index.html[m[36m:[m                <p class="display-4" id="total[1;31mHabit[mos">0</p>
[35mtemplates/index.html[m[36m:[m            <form id="new[1;31mHabit[mForm" class="row g-3 mb-4">
[35mtemplates/index.html[m[36m:[m<div class="modal fade" id="edit[1;31mHabit[mModal" tabindex="-1">
[35mtemplates/index.html[m[36m:[m                <input type="hidden" id="edit[1;31mHabit[mId">
[35mtemplates/index.html[m[36m:[m                        id="edit[1;31mHabit[mName">
[35mtemplates/index.html[m[36m:[m                        id="edit[1;31mHabit[mDescription">
[35mtemplates/index.html[m[36m:[m                    id="saveEdit[1;31mHabit[m">
[35mtemplates/index.html[m[36m:[m        const new[1;31mHabit[mForm = document.getElementById('new[1;31mHabit[mForm');
[35mtemplates/index.html[m[36m:[m        function show[1;31mHabit[mMessage(msg, type = 'success') {
[35mtemplates/index.html[m[36m:[m        async function cargar[1;31mHabit[mos() {
[35mtemplates/index.html[m[36m:[m        render[1;31mHabit[mos(habitos);
[35mtemplates/index.html[m[36m:[m        show[1;31mHabit[mMessage(
[35mtemplates/index.html[m[36m:[m            document.getElementById('total[1;31mHabit[mos').textContent = data.total_habitos || 0;
[35mtemplates/index.html[m[36m:[mfunction render[1;31mHabit[mos(habitos) {
[35mtemplates/index.html[m[36m:[m            await eliminar[1;31mHabit[mo(btn.dataset.id);
[35mtemplates/index.html[m[36m:[m        document.getElementById('edit[1;31mHabit[mId').value = btn.dataset.id;
[35mtemplates/index.html[m[36m:[m        document.getElementById('edit[1;31mHabit[mName').value = btn.dataset.nombre;
[35mtemplates/index.html[m[36m:[m        document.getElementById('edit[1;31mHabit[mDescription').value = btn.dataset.descripcion;
[35mtemplates/index.html[m[36m:[m            document.getElementById('edit[1;31mHabit[mModal')
[35mtemplates/index.html[m[36m:[m        show[1;31mHabit[mMessage(data.message);
[35mtemplates/index.html[m[36m:[m        cargar[1;31mHabit[mos();
[35mtemplates/index.html[m[36m:[m        show[1;31mHabit[mMessage(
[35mtemplates/index.html[m[36m:[m    show[1;31mHabit[mMessage(
[35mtemplates/index.html[m[36m:[masync function editar[1;31mHabit[mo(id, nombre, descripcion) {
[35mtemplates/index.html[m[36m:[m        show[1;31mHabit[mMessage("Hábito actualizado");
[35mtemplates/index.html[m[36m:[m        cargar[1;31mHabit[mos();
[35mtemplates/index.html[m[36m:[m        show[1;31mHabit[mMessage(
[35mtemplates/index.html[m[36m:[m    show[1;31mHabit[mMessage("Error editando hábito", "danger");
[35mtemplates/index.html[m[36m:[mdocument.getElementById('saveEdit[1;31mHabit[m')
[35mtemplates/index.html[m[36m:[m    const id = document.getElementById('edit[1;31mHabit[mId').value;
[35mtemplates/index.html[m[36m:[m    const nombre = document.getElementById('edit[1;31mHabit[mName').value.trim();
[35mtemplates/index.html[m[36m:[m    const descripcion = document.getElementById('edit[1;31mHabit[mDescription').value.trim();
[35mtemplates/index.html[m[36m:[m        show[1;31mHabit[mMessage('El nombre es obligatorio', 'warning');
[35mtemplates/index.html[m[36m:[m    await editar[1;31mHabit[mo(id, nombre, descripcion);
[35mtemplates/index.html[m[36m:[m        document.getElementById('edit[1;31mHabit[mModal')
[35mtemplates/index.html[m[36m:[m        async function eliminar[1;31mHabit[mo(id) {
[35mtemplates/index.html[m[36m:[m                 show[1;31mHabit[mMessage(data.message);
[35mtemplates/index.html[m[36m:[m                 cargar[1;31mHabit[mos();
[35mtemplates/index.html[m[36m:[m                show[1;31mHabit[mMessage(
[35mtemplates/index.html[m[36m:[m    show[1;31mHabit[mMessage(
[35mtemplates/index.html[m[36m:[m        new[1;31mHabit[mForm.addEventListener('submit', async (e) => {
[35mtemplates/index.html[m[36m:[m                show[1;31mHabit[mMessage('El nombre es obligatorio', 'warning');
[35mtemplates/index.html[m[36m:[m                    show[1;31mHabit[mMessage(`Hábito "${nuevo.nombre}" añadido`);
[35mtemplates/index.html[m[36m:[m                    new[1;31mHabit[mForm.reset();
[35mtemplates/index.html[m[36m:[m                    cargar[1;31mHabit[mos();
[35mtemplates/index.html[m[36m:[m                    show[1;31mHabit[mMessage(error.detail || 'Error al crear hábito', 'danger');
[35mtemplates/index.html[m[36m:[m                show[1;31mHabit[mMessage('Error al crear el hábito', 'danger');
[35mtemplates/index.html[m[36m:[m                    cargar[1;31mHabit[mos();
[35mtemplates/index.html[m[36m:[m        cargar[1;31mHabit[mos();
[35mtemplates/index.html[m[36m:[m                    await cargar[1;31mHabit[mos();
