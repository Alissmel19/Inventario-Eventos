
"use strict";

/* =========================================================
   CONFIGURACIÓN Y ESTADO
========================================================= */

let conceptos = [];
let paqueteSeleccionado = null;

const paquetes = window.PAQUETES_BERAKA || {
    "1": {
        nombre: "Evento privado premium",
        descripcion: "Menú VIP y servicios exclusivos."
    },
    "2": {
        nombre: "Evento corporativo",
        descripcion: "Consumo y servicios para eventos corporativos."
    },
    "3": {
        nombre: "Evento por consumo",
        descripcion: "Se cobra según los conceptos seleccionados."
    },
    "4": {
        nombre: "Evento privado estándar",
        descripcion: "Paquete estándar de $21.50 por persona."
    }
};

function dinero(valor) {
    return "$" + (Number(valor) || 0).toFixed(2);
}

function obtenerValor(id) {
    return document.getElementById(id)?.value?.trim() || "";
}

function obtenerPersonas() {
    return Math.max(
        1,
        parseInt(obtenerValor("personas"), 10) || 1
    );
}

/* =========================================================
   SELECCIÓN DE PAQUETE
========================================================= */

function seleccionarPaquete(id) {
    id = String(id);

    if (!paquetes[id]) {
        console.warn("Paquete no reconocido:", id);
        return;
    }

    if (
        paqueteSeleccionado &&
        paqueteSeleccionado !== id &&
        conceptos.length > 0
    ) {
        if (!confirm(
            "Cambiar de paquete eliminará los conceptos agregados. ¿Continuar?"
        )) {
            const anterior = document.querySelector(
                'input[name="paquete"]:checked'
            );

            if (anterior) {
                anterior.checked = false;
            }

            const radioAnterior = document.querySelector(
                `input[name="paquete"][value="${paqueteSeleccionado}"]`
            );

            if (radioAnterior) radioAnterior.checked = true;

            return;
        }

        conceptos = [];
    }

    paqueteSeleccionado = id;

    const info = document.getElementById("packageInfo");

    if (info) {
        info.replaceChildren();

        const titulo = document.createElement("strong");
        titulo.textContent = paquetes[id].nombre;

        const descripcion = document.createElement("p");
        descripcion.textContent = paquetes[id].descripcion;

        info.append(titulo, descripcion);
    }

    const busqueda = document.getElementById("buscarConcepto");
    const categoria = document.getElementById("categoryFilter");

    if (busqueda) busqueda.value = "";
    if (categoria) categoria.value = "todas";

    // Mostrar y filtrar catálogo y opcionales.
    filtrarCatalogo();
    filtrarServicios();

    // La propina se muestra para los paquetes por consumo.
    actualizarVisibilidadPropina();

    renderizarConceptos();
}

/* =========================================================
   CATÁLOGO: PLATILLOS, BEBIDAS Y SERVICIOS
========================================================= */

function esPremium(elemento) {
    const tipo = (elemento.dataset.tipo || "").toLowerCase();
    const nombre = (elemento.dataset.nombre || "").toLowerCase();

    return tipo.includes("premium") ||
           nombre.includes("premium");
}

function esPlatilloEstandar(elemento) {
    const nombre = (
        elemento.dataset.nombre ||
        elemento.querySelector("h3")?.textContent ||
        ""
    ).trim().toLowerCase();

    return [
        "pollo a la cordon bleu",
        "pechuga en salsa de hongos",
        "pechuga de pollo en salsa de hongos",
        "pechuga de pollo en salsa de hongos de la casa"
    ].includes(nombre);
}

function filtrarCatalogo() {
    const texto = obtenerValor("buscarConcepto").toLowerCase();

    const categoria =
        document.getElementById("categoryFilter")?.value || "todas";

    document.querySelectorAll(".catalog-item").forEach(elemento => {
        const nombre = (
            elemento.dataset.nombre ||
            elemento.textContent ||
            ""
        ).toLowerCase();

        const tipo = (
            elemento.dataset.tipo || ""
        ).trim();

        let permitido = true;

        if (paqueteSeleccionado === "1") {
            permitido = esPremium(elemento);
        } else if (["2", "3"].includes(paqueteSeleccionado)) {
            permitido = !esPremium(elemento);
        } else if (paqueteSeleccionado === "4") {
            permitido = esPlatilloEstandar(elemento);
        }

        const coincideTexto = nombre.includes(texto);

        const coincideCategoria =
            categoria === "todas" || tipo === categoria;

        elemento.style.display =
            permitido && coincideTexto && coincideCategoria
                ? ""
                : "none";
    });
}

/* =========================================================
   SERVICIOS OPCIONALES
========================================================= */

function filtrarServicios() {
    document.querySelectorAll(".variable-card").forEach(elemento => {
        // No ocultamos los opcionales al seleccionar un paquete.
        elemento.style.display = "";
    });
}

/* =========================================================
   AGREGAR CONCEPTOS
========================================================= */

function agregarConcepto(nombre, tipo, precio, unidad) {
    if (!paqueteSeleccionado) {
        alert("Primero selecciona un paquete.");
        return;
    }

    const precioNumero = Number(precio);

    if (!Number.isFinite(precioNumero) || precioNumero < 0) {
        alert("El precio del concepto no es válido.");
        return;
    }

    const personas = obtenerPersonas();

    conceptos.push({
        nombre: String(nombre),
        tipo: String(tipo || ""),
        precio: precioNumero,
        unidad: String(unidad || "unidad"),
        cantidad: unidad === "persona" ? personas : 1
    });

    renderizarConceptos();
}

function agregarVariable(nombre, precio, unidad) {
    if (!paqueteSeleccionado) {
        alert("Primero selecciona un paquete.");
        return;
    }

    const precioNumero = Number(precio);

    if (!Number.isFinite(precioNumero) || precioNumero < 0) {
        alert("El precio del servicio opcional no es válido.");
        return;
    }

    const personas = obtenerPersonas();

    conceptos.push({
        nombre: String(nombre),
        tipo: "Servicio opcional",
        precio: precioNumero,
        unidad: String(unidad || "evento"),
        cantidad: unidad === "persona" ? personas : 1
    });

    renderizarConceptos();
}

/* =========================================================
   EDITAR Y ELIMINAR CONCEPTOS
========================================================= */

function cambiarPrecio(index, valor) {
    if (!conceptos[index]) return;

    const precio = Number(valor);

    if (!Number.isFinite(precio) || precio < 0) {
        alert("Ingresa un precio válido.");
        renderizarConceptos();
        return;
    }

    conceptos[index].precio = precio;
    renderizarConceptos();
}

function cambiarCantidad(index, valor) {
    if (!conceptos[index]) return;

    const cantidad = Number.parseFloat(valor);

    if (!Number.isFinite(cantidad) || cantidad <= 0) {
        alert("La cantidad debe ser mayor que cero.");
        renderizarConceptos();
        return;
    }

    conceptos[index].cantidad = cantidad;
    renderizarConceptos();
}

function eliminarConcepto(index) {
    conceptos.splice(index, 1);
    renderizarConceptos();
}

function actualizarPersonas() {
    const personas = obtenerPersonas();

    conceptos.forEach(concepto => {
        if (concepto.unidad === "persona") {
            concepto.cantidad = personas;
        }
    });

    renderizarConceptos();
}

/* =========================================================
   CONSTRUIR TABLA DE COTIZACIÓN
========================================================= */

function crearCelda(texto) {
    const celda = document.createElement("td");
    celda.textContent = texto;
    return celda;
}

function crearEntrada(valor, minimo, alCambiar) {
    const entrada = document.createElement("input");

    entrada.type = "number";
    entrada.value = valor;
    entrada.min = minimo;
    entrada.step = "0.01";
    entrada.className = "cotizacion-editable";

    entrada.addEventListener("change", () => {
        alCambiar(entrada.value);
    });

    return entrada;
}

function renderizarConceptos() {
    const tbody = document.getElementById("cotizacionBody");
    const vacio = document.getElementById("emptyMessage");

    if (!tbody || !vacio) return;

    tbody.replaceChildren();

    vacio.style.display = conceptos.length ? "none" : "block";

    conceptos.forEach((concepto, index) => {
        const fila = document.createElement("tr");

        const celdaNombre = document.createElement("td");

        const nombre = document.createElement("strong");
        nombre.textContent = concepto.nombre;

        const tipo = document.createElement("small");
        tipo.textContent = concepto.tipo;

        celdaNombre.append(nombre, document.createElement("br"), tipo);

        const celdaCantidad = document.createElement("td");

        celdaCantidad.appendChild(
            crearEntrada(
                concepto.cantidad,
                "0.01",
                valor => cambiarCantidad(index, valor)
            )
        );

        const celdaUnidad = crearCelda(concepto.unidad);

        const celdaPrecio = document.createElement("td");

        celdaPrecio.appendChild(
            crearEntrada(
                concepto.precio.toFixed(2),
                "0",
                valor => cambiarPrecio(index, valor)
            )
        );

        const celdaTotal = document.createElement("td");

        const total = document.createElement("strong");
        total.textContent = dinero(
            concepto.precio * concepto.cantidad
        );

        celdaTotal.appendChild(total);

        const celdaEliminar = document.createElement("td");

        const boton = document.createElement("button");
        boton.type = "button";
        boton.className = "delete-btn";
        boton.textContent = "Eliminar";
        boton.addEventListener("click", () => eliminarConcepto(index));

        celdaEliminar.appendChild(boton);

        fila.append(
            celdaNombre,
            celdaCantidad,
            celdaUnidad,
            celdaPrecio,
            celdaTotal,
            celdaEliminar
        );

        tbody.appendChild(fila);
    });

    calcularTotales();
}

/* =========================================================
   CÁLCULOS
========================================================= */

function actualizarVisibilidadPropina() {
    const mostrar = ["2", "3"].includes(paqueteSeleccionado);

    const filaPropina = document.getElementById("filaPropina");
    const filaMonto = document.getElementById("filaMontoPropina");
    const campoPropina = document.getElementById("propina");

    if (filaPropina) {
        filaPropina.style.display = mostrar ? "" : "none";
    }

    if (filaMonto) {
        filaMonto.style.display = mostrar ? "" : "none";
    }

    if (campoPropina && mostrar && campoPropina.value === "") {
        campoPropina.value = "10";
    }
}

function calcularTotales() {
    let subtotal = conceptos.reduce((suma, concepto) => {
        return suma + concepto.precio * concepto.cantidad;
    }, 0);

    // Paquete estándar: tarifa fija de $21.50 por invitado.
    if (paqueteSeleccionado === "4") {
        subtotal = 21.50 * obtenerPersonas();
    }

    const descuento = Math.max(
        0,
        Number(obtenerValor("descuento")) || 0
    );

    const base = Math.max(0, subtotal - descuento);

    const porcentajePropina =
        ["2", "3"].includes(paqueteSeleccionado)
            ? Math.max(0, Number(obtenerValor("propina")) || 0)
            : 0;

    const propina = base * porcentajePropina / 100;
    const total = base + propina;

    function actualizar(id, valor) {
        const elemento = document.getElementById(id);

        if (elemento) {
            elemento.textContent = dinero(valor);
        }
    }

    actualizar("subtotal", subtotal);
    actualizar("baseImponible", base);
    actualizar("montoPropina", propina);
    actualizar("total", total);
    actualizar("costoPersona", total / obtenerPersonas());

    return {
        subtotal,
        descuento: Math.min(descuento, subtotal),
        base,
        porcentajePropina,
        propina,
        total
    };
}

/* =========================================================
   CSRF DE DJANGO
========================================================= */

function obtenerCookie(nombre) {
    const prefijo = nombre + "=";

    const cookie = document.cookie
        .split(";")
        .map(c => c.trim())
        .find(c => c.startsWith(prefijo));

    return cookie
        ? decodeURIComponent(cookie.substring(prefijo.length))
        : "";
}

/* =========================================================
   GUARDAR COTIZACIÓN EN DJANGO
========================================================= */

async function generarCotizacion() {
    const cliente = obtenerValor("cliente");
    const tipoEvento = obtenerValor("tipoEvento");
    const fecha = obtenerValor("fechaEvento");
    const lugar = obtenerValor("lugarEvento");
    const personas = obtenerPersonas();

    if (!paqueteSeleccionado) {
        alert("Selecciona un paquete.");
        return;
    }

    if (!cliente || !tipoEvento || !fecha || !lugar) {
        alert("Completa el cliente, tipo de evento, fecha y lugar.");
        return;
    }

    if (!conceptos.length && paqueteSeleccionado !== "4") {
        alert("Agrega al menos un concepto a la cotización.");
        return;
    }

    const totales = calcularTotales();

    const radioPaquete = document.querySelector(
        'input[name="paquete"]:checked'
    );

    const boton = document.querySelector(
        'button[onclick="generarCotizacion()"]'
    );

    const payload = {
        cliente,
        telefono: obtenerValor("telefono"),
        correo: obtenerValor("correo"),
        tipo_evento: tipoEvento,
        fecha_evento: fecha,
        hora_inicio: obtenerValor("horaInicio"),
        hora_fin: obtenerValor("horaFin"),
        personas,
        lugar,
        direccion: obtenerValor("direccionEvento"),
        observaciones: obtenerValor("observaciones"),
        paquete_id: paqueteSeleccionado,
        paquete_nombre:
            radioPaquete?.dataset.nombre ||
            paquetes[paqueteSeleccionado]?.nombre ||
            "",
        conceptos: conceptos.map(concepto => ({
            nombre: concepto.nombre,
            tipo: concepto.tipo,
            precio: Number(concepto.precio),
            unidad: concepto.unidad,
            cantidad: Number(concepto.cantidad)
        })),
        subtotal: totales.subtotal,
        descuento: totales.descuento,
        porcentaje_propina: totales.porcentajePropina,
        monto_propina: totales.propina,
        total: totales.total,
        forma_pago: obtenerValor("formaPago"),
        anticipo: obtenerValor("anticipo"),
        vigencia: obtenerValor("vigencia"),
        fecha_limite: obtenerValor("fechaLimite"),
        condiciones: obtenerValor("condiciones")
    };

    try {
        if (boton) {
            boton.disabled = true;
            boton.textContent = "Guardando...";
        }

        const respuesta = await fetch(window.location.href, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": obtenerCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify(payload)
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok || !resultado.ok) {
            throw new Error(
                resultado.error || "No se pudo guardar la cotización."
            );
        }

        alert(
            "¡Cotización guardada correctamente!\n\n" +
            "Número: " + resultado.numero_cotizacion +
            "\nTotal: " + dinero(resultado.total)
        );

        window.location.href = "/eventos/";

    } catch (error) {
        console.error("Error guardando cotización:", error);
        alert("No se pudo guardar la cotización:\n" + error.message);

    } finally {
        if (boton) {
            boton.disabled = false;
            boton.textContent = "Generar cotización";
        }
    }
}

/* =========================================================
   INICIALIZACIÓN
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    // El catálogo y los servicios opcionales aparecen al cargar.
    filtrarCatalogo();
    filtrarServicios();
    actualizarVisibilidadPropina();
    renderizarConceptos();

    // Recalcular si se modifica el descuento o la propina.
    document.getElementById("descuento")
        ?.addEventListener("input", calcularTotales);

    document.getElementById("propina")
        ?.addEventListener("input", calcularTotales);

    document.getElementById("personas")
        ?.addEventListener("change", actualizarPersonas);

    // Seleccionar el paquete marcado, si existe.
    const seleccionado = document.querySelector(
        'input[name="paquete"]:checked'
    );

    if (seleccionado) {
        seleccionarPaquete(seleccionado.value);
    }
});
