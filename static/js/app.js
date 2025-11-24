/* ============================================================
   🛡 VALIDACIÓN DEL FORMULARIO
============================================================ */

function validarFormulario(nombre, correo, telefono) {
    if (nombre.trim().length < 3) {
        alert("El nombre debe tener mínimo 3 caracteres.");
        return false;
    }

    const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!correoRegex.test(correo)) {
        alert("Correo electrónico inválido.");
        return false;
    }

    if (telefono && isNaN(telefono)) {
        alert("El teléfono debe contener solo números.");
        return false;
    }

    return true;
}


/* ============================================================
   📝 FORMULARIO – contacto.html
============================================================ */

const form = document.getElementById("formContacto");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value.trim();
        const correo = document.getElementById("correo").value.trim();
        const telefono = document.getElementById("telefono").value.trim();

        if (!validarFormulario(nombre, correo, telefono)) return;

        // =============================
        // 📤 Enviar datos al backend
        // =============================
        try {
            const response = await fetch("/guardar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nombre, correo, telefono })
            });

            const data = await response.json();

            if (!response.ok) {
                alert("❌ " + data.error);
                return;
            }

            alert("✅ " + data.mensaje);
            form.reset();

        } catch (error) {
            console.error("Error enviando datos:", error);
            alert("❌ Error de conexión con el servidor.");
        }
    });
}


/* ============================================================
   📋 LISTA – lista.html
============================================================ */

const tabla = document.getElementById("tablaContactos");

if (tabla) {
    async function cargarContactos() {
        try {
            const res = await fetch("/api/contactos");
            const data = await res.json();

            if (!res.ok) {
                tabla.innerHTML = `
                    <tr><td colspan="5" class="p-3 text-center text-red-500">
                        Error cargando datos
                    </td></tr>
                `;
                return;
            }

            if (data.length === 0) {
                tabla.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center p-3 text-gray-500">
                            No hay contactos registrados.
                        </td>
                    </tr>
                `;
                return;
            }

            data.forEach(c => {
                const fila = document.createElement("tr");
                fila.classList.add("border-b");

                fila.innerHTML = `
                    <td class="p-2">${c.nombre}</td>
                    <td class="p-2">${c.correoElectronico}</td>
                    <td class="p-2">${c.telefono}</td>
                    <td class="p-2">${c.fechaRegistro}</td>
                `;

                tabla.appendChild(fila);
            });

        } catch (error) {
            console.error("Error:", error);
            tabla.innerHTML = `
                <tr>
                    <td colspan="5" class="p-3 text-center text-red-500">
                        Error conectando al servidor.
                    </td>
                </tr>
            `;
        }
    }

    cargarContactos();
}
