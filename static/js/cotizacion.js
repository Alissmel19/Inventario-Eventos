
"use strict";

/* =========================================================
   CONFIGURACIÓN Y ESTADO
========================================================= */

let conceptos = [];
let paqueteSeleccionado = null;

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

    // paquetes_json llega como una lista desde Django.
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
    const nombre = nombrePaqueteActual();

    return nombre.includes("consumo") ||
           nombre.includes("corporativo");
}

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
            "Cambiar de paquete actualizará los incluidos y eliminará " +
            "los conceptos seleccionados. ¿Deseas continuar?"
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
    const nombre = String(paquete.nombre || "").toLowerCase();

    const esPrivado =
        nombre.includes("privado") &&
        (
            nombre.includes("standard") ||
            nombre.includes("estandar") ||
            nombre.includes("estándar") ||
            nombre.includes("premium")
        );

    // Mostrar información del paquete.
    const info = document.getElementById("packageInfo");

    if (info) {
        info.replaceChildren();

        const titulo = document.createElement("h3");
        titulo.textContent = paquete.nombre;

        const descripcion = document.createElement("p");
        descripcion.textContent = paquete.descripcion || "";

        info.append(titulo, descripcion);
    }

    // La lista de incluidos se mostrará en el detalle de cotización.
    const configuracion = document.getElementById("configuracionPaquete");
    if (configuracion) configuracion.hidden = true;

    const listaServicios = document.getElementById("serviciosIncluidos");
    if (listaServicios) listaServicios.replaceChildren();

    // Reiniciar los conceptos según el nuevo paquete.
    conceptos = [];

    if (esPrivado) {
        const servicios = Array.isArray(paquete.servicios)
            ? paquete.servicios
            : [];

          servicios.forEach(servicio => {
              const nombreServicio = String(servicio.nombre || "").toLowerCase();
              const esSalon = [1, 19, 24].includes(Number(servicio.id));
              const esPorUnidad = nombreServicio.includes("florero");
              const personas = obtenerPersonas();

              conceptos.push({
                  catalogo_id: Number(servicio.id),
                  nombre: String(servicio.nombre),
                  tipo: "Incluido en paquete",
                  precio: Number(servicio.precio || 0),
                  unidad: esSalon ? "evento" : esPorUnidad ? "unidad" : "persona",
                  cantidad: esSalon ? 1 : esPorUnidad ? 1 : personas,
                  incluido: true
              });
          });
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

function esPremium(elemento) {
    const tipo = (elemento.dataset.tipo || "").toLowerCase();
    const nombre = (elemento.dataset.nombre || "").toLowerCase();

    return tipo.includes("premium") ||
           nombre.includes("premium");
}

function esPlatilloEstandar(elemento) {
    const tipo = (elemento.dataset.tipo || "")
        .trim()
        .toLowerCase();

    return tipo.includes("plato estandard") ||
           tipo.includes("plato estándar") ||
           tipo.includes("plato standard") ||
           tipo.includes("plato estandar");
}

function filtrarCatalogo() {
    const texto = (
        document.getElementById("buscarConcepto")?.value || ""
    ).toLowerCase().trim();

    const categoria = (
        document.getElementById("categoryFilter")?.value || "todas"
    ).toLowerCase().trim();

    const nombrePaquete = nombrePaqueteActual();
    const esEstandar = esPaqueteEstandar();
    const esPremium = nombrePaquete.includes("premium");

    let visibles = 0;

    document.querySelectorAll(".catalog-item").forEach(item => {
        const nombre = (item.dataset.nombre || "")
            .toLowerCase().trim();

        const tipo = (item.dataset.tipo || "")
            .toLowerCase().trim();

        let permitido = true;

        if (esEstandar) {
            permitido = esPlatilloEstandar(item);
        } else if (esPremium) {
            permitido =
                tipo.includes("entrada premium") ||
                tipo.includes("plato fuerte premium");
        }

        const coincideTexto = !texto || nombre.includes(texto);
        const coincideCategoria =
            categoria === "todas" || tipo === categoria;

        const visible =
            permitido && coincideTexto && coincideCategoria;

        item.style.display = visible ? "" : "none";

        const boton = item.querySelector("button");
        if (boton) boton.disabled = !visible;

        if (visible) visibles++;
    });

    const empty = document.getElementById("catalogEmpty");
    if (empty) empty.style.display = visibles ? "none" : "block";
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

        // En eventos por consumo no se permite contratar DJ ni bocinas.
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
   AGREGAR CONCEPTOS
========================================================= */

function agregarConcepto(id, nombre, tipo, precio, unidad) {
    if (!paqueteSeleccionado) {
        alert("Primero selecciona un paquete.");
        return;
    }
    console.log("PLATO:", id, nombre, tipo, precio, unidad);

    const precioNumero = Number(precio);
    const unidadNormalizada = String(unidad || "unidad").toLowerCase();

    if (!Number.isFinite(precioNumero) || precioNumero < 0) {
        alert("El precio del concepto no es válido.");
        return;
    }

    const personas = obtenerPersonas();

    conceptos.push({
        catalogo_id: Number(id),
        nombre: String(nombre),
        tipo: String(tipo || ""),
        precio: precioNumero,
        unidad: unidadNormalizada,
        cantidad: unidadNormalizada === "persona" ? personas : 1,
        incluido: false
    });

    renderizarConceptos();
    calcularTotales();
}

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

    conceptos.push({
        catalogo_id: Number(id),
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
    const concepto = conceptos[index];

    if (!concepto || concepto.incluido) {
        return;
    }

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

    vacio.style.display = conceptos.length ? "none" : "block";

    conceptos.forEach((concepto, index) => {
        const fila = document.createElement("tr");

        // Nombre y tipo de concepto
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

        // Cantidad: bloqueada únicamente para los incluidos
        const celdaCantidad = document.createElement("td");


        celdaCantidad.appendChild(
            crearEntrada(
                concepto.cantidad,
                0.01,
                valor => cambiarCantidad(index, valor)
            )
        );

        // Unidad
        const celdaUnidad = crearCelda(concepto.unidad);

        // Precio: bloqueado únicamente para los incluidos
        const celdaPrecio = document.createElement("td");

        if (concepto.incluido) {
            celdaPrecio.textContent = dinero(concepto.precio);
        } else {
            celdaPrecio.appendChild(
                crearEntrada(
                    concepto.precio,
                    "0.01",
                    valor => cambiarPrecio(index, valor)
                )
            );
        }

        // Total
        const celdaTotal = document.createElement("td");
        const total = document.createElement("strong");

        total.textContent = dinero(
            concepto.precio * concepto.cantidad
        );

        celdaTotal.appendChild(total);

        // Acción: los incluidos no se pueden eliminar
        const celdaEliminar = document.createElement("td");

        if (concepto.incluido) {
            const etiqueta = document.createElement("span");
            etiqueta.textContent = "Incluido";
            etiqueta.className = "concepto-incluido";

            celdaEliminar.appendChild(etiqueta);
        } else {
            const boton = document.createElement("button");

            boton.type = "button";
            boton.className = "delete-btn";
            boton.textContent = "Eliminar";

            boton.addEventListener("click", () => {
                eliminarConcepto(index);
            });

            celdaEliminar.appendChild(boton);
        }

        // Agregar todas las celdas a la fila
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
    // Los incluidos se muestran, pero no se cobran nuevamente.
    const conceptosCobrables = conceptos.filter(
        concepto => concepto.incluido !== true
    );

    const subtotal = conceptosCobrables.reduce((suma, concepto) => {
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

    const porcentajePropina = llevaPropina()
        ? Math.max(0, Number(obtenerValor("propina")) || 0)
        : 0;

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
        alert("Completa el cliente, tipo de evento, fecha y lugar.");
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
        paquete_nombre: paquete.nombre,


       
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
        ?.addEventListener("input", actualizarPersonas);

    const seleccionado = document.querySelector(
        'input[name="paquete"]:checked'
    );

    if (seleccionado) {
        seleccionarPaquete(seleccionado.value);
    }
});
