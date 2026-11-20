"use strict";

/* =========================================================
   CONFIGURACIÓN Y ESTADO
========================================================= */

let conceptos = [];
let paqueteSeleccionado = null;
let subpaqueteSeleccionadoId = "";

const paquetes = window.PAQUETES_BERAKA || {};

function dinero(valor) {
    return "$" + (Number(valor) || 0).toFixed(2);
}

function obtenerValor(id) {
    return document.getElementById(id)?.value?.trim() || "";
}

function obtenerPersonas() {
    return Math.max(1, parseInt(obtenerValor("personas"), 10) || 1);
}

/* =========================================================
   PAQUETES
========================================================= */

function obtenerRadioPaquete(id) {
    return Array.from(
        document.querySelectorAll('input[name="paquete"]')
    ).find(radio => String(radio.value) === String(id));
}

function obtenerPaqueteActual(id) {
    const radio = obtenerRadioPaquete(id);
    const tarjeta = radio?.closest(".package-option");

    const configurado = Array.isArray(paquetes)
        ? paquetes.find(p => String(p.id) === String(id)) || {}
        : paquetes[String(id)] || {};

    return {
        ...configurado,
        nombre:
            radio?.dataset.nombre ||
            configurado.nombre ||
            tarjeta?.querySelector("h3")?.textContent?.trim() ||
            "Paquete seleccionado",
        descripcion:
            radio?.dataset.descripcion ||
            configurado.descripcion ||
            tarjeta?.querySelector("p")?.textContent?.trim() ||
            ""
    };
}

function nombrePaqueteActual() {
    if (!paqueteSeleccionado) return "";

    return String(
        obtenerPaqueteActual(paqueteSeleccionado).nombre || ""
    ).toLowerCase();
}

function esPaqueteEstandar() {
    const nombre = nombrePaqueteActual();

    return nombre.includes("estándar") ||
           nombre.includes("estandar");
}

function llevaPropina() {
    return true;
}

/* =========================================================
   CONCEPTOS INCLUIDOS
========================================================= */

function convertirConceptoIncluido(item, esSubpaquete = false) {
    const grupo = String(item.grupo || "").toLowerCase();

    const unidades = {
        platillo: "persona",
        bebida: "persona",
        servicio: "evento",
        servicio_opcional: "evento",
        montaje: "unidad"
    };

    const unidad = unidades[grupo] || "unidad";
    const personas = obtenerPersonas();

    return {
        catalogo_id: Number(item.id),
        nombre: String(item.nombre || ""),
        tipo: grupo,
        grupo: grupo,
        precio: Number(item.precio ?? 0),
        unidad: unidad,
        cantidad: unidad === "persona"
            ? personas
            : Number(item.cantidad || 1),
        incluido: true,
        obligatorio: Boolean(item.obligatorio),
        cortesia: Boolean(item.cortesia),
        esSubpaquete: esSubpaquete,
        subpaquete_id: esSubpaquete
            ? String(subpaqueteSeleccionadoId)
            : ""
    };
}

function cargarConceptosIncluidos(lista) {
    if (!Array.isArray(lista)) return;

    lista.forEach(item => {
        conceptos.push(convertirConceptoIncluido(item));
    });
}

/* =========================================================
   SELECTOR DE MODALIDADES / SUBPAQUETES
========================================================= */

function cargarSelectorSubpaquetes(paquete) {
    const contenedor = document.getElementById("contenedorSubpaquetes");
    const selector = document.getElementById("subpaqueteSeleccionado");

    if (!contenedor || !selector) return;

    selector.replaceChildren();

    const inicial = document.createElement("option");
    inicial.value = "";
    inicial.textContent = "Selecciona un menú";
    selector.appendChild(inicial);

    const subpaquetes = Array.isArray(paquete.subpaquetes)
        ? paquete.subpaquetes
        : [];

    if (!subpaquetes.length) {
        contenedor.hidden = true;
        return;
    }

    subpaquetes.forEach(subpaquete => {
        const opcion = document.createElement("option");
        opcion.value = String(subpaquete.id);
        opcion.textContent = subpaquete.nombre;
        selector.appendChild(opcion);
    });

    contenedor.hidden = false;
}

function seleccionarSubpaquete(id) {

    subpaqueteSeleccionadoId = String(id || "");

    // Limpiar búsqueda anterior.
    const busqueda = document.getElementById("buscarConcepto");

    if (busqueda) {
        busqueda.value = "";
    }

    // Actualizar el catálogo con la modalidad elegida.
    filtrarCatalogo();

    renderizarConceptos();
}
/* =========================================================
   SELECCIONAR PAQUETE
========================================================= */

function seleccionarPaquete(id) {
    id = String(id);

    const radioActual = obtenerRadioPaquete(id);

    if (!radioActual) return;

    if (
        paqueteSeleccionado &&
        paqueteSeleccionado !== id &&
        conceptos.length > 0
    ) {
        const continuar = confirm(
            "Cambiar de paquete actualizará los conceptos incluidos " +
            "y eliminará los conceptos seleccionados. ¿Deseas continuar?"
        );

        if (!continuar) {
            const anterior = obtenerRadioPaquete(paqueteSeleccionado);

            if (anterior) anterior.checked = true;

            radioActual.checked = false;
            return;
        }
    }

    paqueteSeleccionado = id;
    radioActual.checked = true;

    const paquete = obtenerPaqueteActual(id);

    const info = document.getElementById("packageInfo");

    if (info) {
        info.replaceChildren();

        const titulo = document.createElement("h3");
        titulo.textContent = paquete.nombre;

        const descripcion = document.createElement("p");
        descripcion.textContent = paquete.descripcion || "";

        info.append(titulo, descripcion);
    }

    conceptos = [];

    cargarConceptosIncluidos(
        (paquete.conceptos || []).filter(
            item => item.obligatorio === true
        )
    );

    subpaqueteSeleccionadoId = "";

    cargarSelectorSubpaquetes(paquete);

    const selector = document.getElementById("subpaqueteSeleccionado");

    if (selector) {
        selector.value = "";
    }

    const configuracion = document.getElementById("configuracionPaquete");

    if (configuracion) {
        configuracion.hidden = false;
    }

    const busqueda = document.getElementById("buscarConcepto");
    const categoria = document.getElementById("categoryFilter");

    if (busqueda) busqueda.value = "";
    if (categoria) categoria.value = "todas";

    actualizarVisibilidadPropina();

    filtrarCatalogo();
    filtrarServicios();
    renderizarConceptos();
    calcularTotales();
}

/* =========================================================
   CATÁLOGO Y FILTROS
========================================================= */

function normalizarFiltro(valor) {
    return String(valor || "")
        .toLocaleLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .trim();
}


function filtrarCatalogo() {
    const texto = normalizarFiltro(
        document.getElementById("buscarConcepto")?.value || ""
    );

    const paquete = paqueteSeleccionado
        ? obtenerPaqueteActual(paqueteSeleccionado)
        : null;

    const subpaquetes = paquete?.subpaquetes || [];

    const subpaqueteActivo = subpaquetes.find(
        sub => String(sub.id) === String(subpaqueteSeleccionadoId)
    );

    const mostrarTodo = document.getElementById(
        "mostrarMenuCompleto"
    )?.checked || false;

    // Obtener únicamente los platillos de la modalidad seleccionada.
    const conceptosModalidad = subpaqueteActivo?.conceptos || [];

    const platillosModalidad = conceptosModalidad.filter(
        concepto =>
            normalizarFiltro(concepto.grupo) === "platillo"
    );

    const idsPermitidos = new Set(
        platillosModalidad.map(concepto => String(concepto.id))
    );

    // Aplicar filtro especial solamente cuando la modalidad
    // tiene platillos realmente relacionados en la base de datos.
    const aplicarFiltroModalidad = idsPermitidos.size > 0;

    const elementos = Array.from(
        document.querySelectorAll(".catalog-item")
    );

    let visibles = 0;

    elementos.forEach(item => {
        const id = String(item.dataset.id || "");
        const grupo = normalizarFiltro(item.dataset.grupo);
        const nombre = normalizarFiltro(item.dataset.nombre);

        const esPlatillo = grupo === "platillo";

        const perteneceModalidad =
            esPlatillo && idsPermitidos.has(id);

        const coincideBusqueda =
            texto.length > 0 && nombre.includes(texto);

        let visible;

        if (mostrarTodo || coincideBusqueda) {
            // Mostrar todo al solicitarlo o al buscar.
            visible = true;
        } else if (aplicarFiltroModalidad) {
            // Premium: mostrar inicialmente sus platos fuertes.
            visible = perteneceModalidad;
        } else {
            // Los demás paquetes muestran todo el catálogo.
            visible = true;
        }

        item.style.display = visible ? "" : "none";

        item.classList.toggle(
            "platillo-modalidad",
            perteneceModalidad
        );

        if (visible) visibles++;
    });

    // Ordenar los platos de la modalidad al principio.
    const catalogo = document.querySelector(".catalog-grid");

    if (catalogo && aplicarFiltroModalidad) {
        elementos.sort((a, b) => {
            const prioridadA =
                a.classList.contains("platillo-modalidad") ? 1 : 0;

            const prioridadB =
                b.classList.contains("platillo-modalidad") ? 1 : 0;

            return prioridadB - prioridadA;
        });

        elementos.forEach(item => catalogo.appendChild(item));
    }

    const empty = document.getElementById("catalogEmpty");


    if (empty) {
        empty.style.display = visibles === 0 ? "block" : "none";
    }
}

window.filtrarCatalogo = filtrarCatalogo;

/* =========================================================
   SERVICIOS OPCIONALES
========================================================= */

function filtrarServicios() {
    const paqueteId = String(paqueteSeleccionado || "");

    document.querySelectorAll(".variable-card").forEach(elemento => {
        const nombre = (
            elemento.querySelector("h3")?.textContent || ""
        ).toLowerCase();

        const boton = elemento.querySelector("button");

        const restringido =
            paqueteId === "3" &&
            (
                nombre.includes("dj") ||
                nombre.includes("bocina")
            );

        elemento.style.display = restringido ? "none" : "";

        if (boton) {
            boton.disabled = restringido;
        }
    });
}

/* =========================================================
   AGREGAR CONCEPTOS DEL CATÁLOGO
========================================================= */


function agregarConcepto(id, nombre, tipo, precio, unidad, grupo = "") {
    if (!paqueteSeleccionado) {
        alert("Primero selecciona un paquete.");
        return;
    }

    const precioNumero = Number(precio);
    const unidadNormalizada = String(unidad || "unidad").toLowerCase();

    if (!Number.isFinite(precioNumero) || precioNumero < 0) {
        alert("El precio del concepto no es válido.");
        return;
    }

    const grupoNormalizado = String(grupo || "").toLowerCase();

    const conceptoCoincidente = conceptos.find(concepto =>
        String(concepto.grupo || "").toLowerCase() === grupoNormalizado &&
        String(concepto.catalogo_id) === String(id)
    );

    if (conceptoCoincidente) {
        if (conceptoCoincidente.incluido === true) {
            conceptoCoincidente.nombre = String(nombre);
            conceptoCoincidente.tipo = String(tipo || "");
            conceptoCoincidente.precio = precioNumero;
            conceptoCoincidente.unidad = unidadNormalizada;
            conceptoCoincidente.cantidad = unidadNormalizada === "persona"
                ? obtenerPersonas()
                : 1;
            conceptoCoincidente.incluido = false;
            conceptoCoincidente.subpaquete_id = String(
                subpaqueteSeleccionadoId || ""
            );

            renderizarConceptos();
            filtrarCatalogo();
            calcularTotales();
            return;
        }

        alert("Este concepto ya está agregado a la cotización.");
        return;
    }

    conceptos.push({
        catalogo_id: Number(id),
        nombre: String(nombre),
        tipo: String(tipo || ""),
        grupo: String(grupo || ""),
        subpaquete_id: String(subpaqueteSeleccionadoId || ""),
        precio: precioNumero,
        unidad: unidadNormalizada,
        cantidad: unidadNormalizada === "persona"
            ? obtenerPersonas()
            : 1,
        incluido: false,
        esSubpaquete: false
    });

    renderizarConceptos();
    filtrarCatalogo();
    calcularTotales();
}


/* =========================================================
   AGREGAR SERVICIOS OPCIONALES
========================================================= */

function agregarVariable(id, nombre, precio, unidad) {
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

    const yaExiste = conceptos.some(concepto =>
        String(concepto.catalogo_id) === String(id) &&
        concepto.grupo === "servicio_opcional"
    );

    if (yaExiste) {
        alert("Este servicio ya está agregado.");
        return;
    }

    conceptos.push({
        catalogo_id: Number(id),
        nombre: String(nombre),
        tipo: "Servicio opcional",
        precio: precioNumero,
        unidad: String(unidad || "evento"),
        cantidad: unidad === "persona" ? personas : 1,
        grupo: "servicio_opcional",
        incluido: false
    });

    renderizarConceptos();
    calcularTotales();
}

window.agregarVariable = agregarVariable;

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
    if (!conceptos[index]) return;

    conceptos.splice(index, 1);

    renderizarConceptos();
    filtrarCatalogo();
    calcularTotales();
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
   TABLA DE COTIZACIÓN
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

    // Los conceptos incluidos se mantienen en la lógica interna del paquete,
    // pero no se muestran en la tabla de conceptos seleccionados.
    const conceptosVisibles = conceptos
        .map((concepto, index) => ({ concepto, index }))
        .filter(({ concepto }) => concepto.incluido !== true);

    vacio.style.display = conceptosVisibles.length ? "none" : "block";

    conceptosVisibles.forEach(({ concepto, index }) => {
        const fila = document.createElement("tr");

        const celdaNombre = document.createElement("td");

        const nombre = document.createElement("strong");
        nombre.textContent = concepto.nombre;

        const tipo = document.createElement("small");
        tipo.textContent = concepto.tipo;

        celdaNombre.append(
            nombre,
            document.createElement("br"),
            tipo
        );

        const celdaCantidad = document.createElement("td");

        celdaCantidad.appendChild(
            crearEntrada(
                concepto.cantidad,
                0.01,
                valor => cambiarCantidad(index, valor)
            )
        );

        const celdaUnidad = crearCelda(concepto.unidad);

        const celdaPrecio = document.createElement("td");

        celdaPrecio.appendChild(
            crearEntrada(
                concepto.precio,
                "0",
                valor => cambiarPrecio(index, valor)
            )
        );

        const celdaTotal = document.createElement("td");

        const total = document.createElement("strong");

        total.textContent = dinero(
            concepto.incluido
                ? 0
                : concepto.precio * concepto.cantidad
        );

        celdaTotal.appendChild(total);

        const celdaEliminar = document.createElement("td");

        const boton = document.createElement("button");

        boton.type = "button";
        boton.className = "delete-btn";
        boton.textContent = "Eliminar";

        boton.addEventListener("click", () => {
            eliminarConcepto(index);
        });

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
   CÁLCULOS Y PROPINA
========================================================= */

function actualizarVisibilidadPropina() {
    const mostrar = llevaPropina();

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
    const subtotal = conceptos.reduce((suma, concepto) => {
        if (concepto.incluido) return suma;

        return suma + (
            Number(concepto.precio || 0) *
            Number(concepto.cantidad || 0)
        );
    }, 0);

    const descuento = Math.max(
        0,
        Number(obtenerValor("descuento")) || 0
    );

    const base = Math.max(0, subtotal - descuento);

    const porcentajePropina = Math.max(
        0,
        Number(obtenerValor("propina")) || 0
    );

    const propina = base * porcentajePropina / 100;
    const total = base + propina;
    const personas = Math.max(1, obtenerPersonas());

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
    actualizar("costoPersona", total / personas);

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
   GUARDAR COTIZACIÓN
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
        alert(
            "Completa el cliente, tipo de evento, fecha y lugar."
        );
        return;
    }

    if (!conceptos.length && !esPaqueteEstandar()) {
        alert("Agrega al menos un concepto a la cotización.");
        return;
    }

    const totales = calcularTotales();

    const boton = document.querySelector(
        'button[onclick="generarCotizacion()"]'
    );

    const paquete = obtenerPaqueteActual(paqueteSeleccionado);
    const selectorSubpaquete = document.getElementById("subpaqueteSeleccionado");
    const subpaqueteNombre = selectorSubpaquete?.selectedOptions?.[0]?.textContent?.trim() || "";

    const payload = {
        cliente,
        telefono: obtenerValor("telefono"),
        correo: obtenerValor("correo"),
        tipo_evento: tipoEvento,
        fecha_evento: fecha,
        hora_inicio: obtenerValor("horaInicio"),
        hora_fin: obtenerValor("horaFin"),
        personas,
        cantidad_ninos: Number(
        document.getElementById("cantidad_ninos")?.value || 0
        ),
        lugar,
        direccion: obtenerValor("direccionEvento"),
        observaciones: obtenerValor("observaciones"),
        paquete_id: paqueteSeleccionado,
        paquete_nombre: paquete.nombre,
        subpaquete_id: subpaqueteSeleccionadoId || "",
        subpaquete_nombre: subpaqueteNombre,

        conceptos: conceptos.map(concepto => ({
            catalogo_id: concepto.catalogo_id,
            nombre: concepto.nombre,
            tipo: concepto.tipo,
            precio: Number(concepto.precio),
            unidad: concepto.unidad,
            cantidad: Number(concepto.cantidad),
            incluido: concepto.incluido === true
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
                resultado.error ||
                "No se pudo guardar la cotización."
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

        alert(
            "No se pudo guardar la cotización:\n" +
            error.message
        );

    } finally {
        if (boton) {
            boton.disabled = false;
            boton.textContent = "Generar cotización";
        }
    }
}

window.generarCotizacion = generarCotizacion;

/* =========================================================
   INICIALIZACIÓN
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    filtrarCatalogo();
    filtrarServicios();
    actualizarVisibilidadPropina();
    renderizarConceptos();

    document.getElementById("descuento")
        ?.addEventListener("input", calcularTotales);

    document.getElementById("propina")
        ?.addEventListener("input", calcularTotales);

    document.getElementById("personas")
        ?.addEventListener("change", actualizarPersonas);

    document.getElementById("buscarConcepto")
        ?.addEventListener("input", filtrarCatalogo);

    document.getElementById("categoryFilter")
        ?.addEventListener("change", filtrarCatalogo);

    document.getElementById("mostrarMenuCompleto")
        ?.addEventListener("change", filtrarCatalogo);

    document.getElementById("subpaqueteSeleccionado")
        ?.addEventListener("change", evento => {
            seleccionarSubpaquete(evento.target.value);
        });

    document.querySelectorAll('input[name="paquete"]')
        .forEach(radio => {
            radio.addEventListener("change", () => {
                seleccionarPaquete(radio.value);
            });
        });
});