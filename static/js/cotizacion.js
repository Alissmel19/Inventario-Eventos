let conceptos = [];


// ============================================================
// PAQUETES
// ============================================================

const paquetes = {

    consumo: {

        nombre: "Evento por Consumo",

        descripcion:
            "Consumo de alimentos y bebidas seleccionados. " +
            "Se agrega 10% de propina."

    },


    orquideas: {

        nombre:
            "Evento por Consumo + Salón Las Orquídeas",

        descripcion:
            "Incluye 5 horas de salón, aire acondicionado, " +
            "sonido profesional, proyector, mesas y sillas. " +
            "Costo del salón: $250.00."

    },


    vip: {

        nombre:
            "Paquete VIP",

        descripcion:
            "Experiencia completa con alimentación, bebidas, " +
            "montaje y servicio. " +
            "Vegetariano $33.75 p/p, pollo $37.25 p/p " +
            "y carne $40.75 p/p."

    }

};


// ============================================================
// SELECCIONAR PAQUETE
// ============================================================

function seleccionarPaquete(id) {

    const info = document.getElementById(
        "packageInfo"
    );

    if (!paquetes[id]) {
        return;
    }

    info.innerHTML = `

        <strong>
            ${paquetes[id].nombre}
        </strong>

        <p>
            ${paquetes[id].descripcion}
        </p>

    `;

}


// ============================================================
// AGREGAR CONCEPTO
// ============================================================

function agregarConcepto(
    nombre,
    tipo,
    precio,
    unidad
) {

    precio = parseFloat(precio);

    let cantidad = 1;

    const personasInput =
        document.getElementById("personas");

    const personas =
        parseInt(personasInput.value) || 1;


    if (unidad === "persona") {

        cantidad = personas;

    }


    conceptos.push({

        nombre: nombre,

        tipo: tipo,

        precio: precio,

        unidad: unidad,

        cantidad: cantidad

    });


    renderizarConceptos();

}


// ============================================================
// AGREGAR VARIABLE
// ============================================================

function agregarVariable(
    nombre,
    precio,
    unidad
) {

    precio = parseFloat(precio);

    let cantidad = 1;

    const personas =
        parseInt(
            document.getElementById("personas").value
        ) || 1;


    if (unidad === "persona") {

        cantidad = personas;

    }


    conceptos.push({

        nombre: nombre,

        tipo: "Opcional",

        precio: precio,

        unidad: unidad,

        cantidad: cantidad

    });


    renderizarConceptos();

}


// ============================================================
// ACTUALIZAR PERSONAS
// ============================================================

function actualizarPersonas() {

    const personas =
        parseInt(
            document.getElementById("personas").value
        ) || 1;


    conceptos.forEach(function (concepto) {

        if (
            concepto.unidad === "persona"
        ) {

            concepto.cantidad =
                personas;

        }

    });


    renderizarConceptos();

}


// ============================================================
// RENDERIZAR TABLA
// ============================================================

function renderizarConceptos() {

    const tbody =
        document.getElementById(
            "cotizacionBody"
        );

    const empty =
        document.getElementById(
            "emptyMessage"
        );


    tbody.innerHTML = "";


    if (conceptos.length === 0) {

        empty.style.display = "block";

        calcularTotales();

        return;

    }


    empty.style.display = "none";


    conceptos.forEach(
        function (concepto, index) {

            const total =
                concepto.precio *
                concepto.cantidad;


            const fila =
                document.createElement("tr");


            fila.innerHTML = `

                <td>

                    <strong>
                        ${concepto.nombre}
                    </strong>

                    <small>
                        ${concepto.tipo}
                    </small>

                </td>


                <td>

                    <input
                        type="number"
                        min="1"
                        value="${concepto.cantidad}"
                        onchange="cambiarCantidad(
                            ${index},
                            this.value
                        )"
                    >

                </td>


                <td>
                    ${concepto.unidad}
                </td>


                <td>
                    $${concepto.precio.toFixed(2)}
                </td>


                <td>
                    <strong>
                        $${total.toFixed(2)}
                    </strong>
                </td>


                <td>

                    <button
                        type="button"
                        class="delete-btn"
                        onclick="eliminarConcepto(${index})"
                    >
                        ×
                    </button>

                </td>

            `;


            tbody.appendChild(fila);

        }
    );


    calcularTotales();

}


// ============================================================
// CAMBIAR CANTIDAD
// ============================================================

function cambiarCantidad(
    index,
    cantidad
) {

    cantidad =
        parseInt(cantidad) || 1;


    conceptos[index].cantidad =
        cantidad;


    renderizarConceptos();

}


// ============================================================
// ELIMINAR
// ============================================================

function eliminarConcepto(index) {

    conceptos.splice(
        index,
        1
    );


    renderizarConceptos();

}


// ============================================================
// FILTRAR CATÁLOGO
// ============================================================

function filtrarCatalogo() {

    const texto =
        document
            .getElementById(
                "buscarConcepto"
            )
            .value
            .toLowerCase();


    const categoria =
        document
            .getElementById(
                "categoryFilter"
            )
            .value;


    const elementos =
        document.querySelectorAll(
            ".catalog-item"
        );


    elementos.forEach(
        function (elemento) {

            const nombre =
                elemento.dataset.nombre
                    .toLowerCase();


            const tipo =
                elemento.dataset.tipo;


            const coincideNombre =
                nombre.includes(texto);


            const coincideCategoria =
                categoria === "todas" ||
                tipo === categoria;


            if (
                coincideNombre &&
                coincideCategoria
            ) {

                elemento.style.display =
                    "";

            } else {

                elemento.style.display =
                    "none";

            }

        }
    );

}


// ============================================================
// CALCULAR TOTALES
// ============================================================

function calcularTotales() {

    let subtotal = 0;


    conceptos.forEach(
        function (concepto) {

            subtotal +=
                concepto.precio *
                concepto.cantidad;

        }
    );


    const descuento =
        parseFloat(
            document
                .getElementById(
                    "descuento"
                )
                .value
        ) || 0;


    const porcentajePropina =
        parseFloat(
            document
                .getElementById(
                    "propina"
                )
                .value
        ) || 0;


    const porcentajeIVA =
        parseFloat(
            document
                .getElementById(
                    "iva"
                )
                .value
        ) || 0;


    const base =
        Math.max(
            subtotal - descuento,
            0
        );


    const montoPropina =
        base *
        (
            porcentajePropina / 100
        );


    const montoIVA =
        base *
        (
            porcentajeIVA / 100
        );


    const total =
        base +
        montoPropina +
        montoIVA;


    const personas =
        parseInt(
            document
                .getElementById(
                    "personas"
                )
                .value
        ) || 1;


    const costoPersona =
        total / personas;


    document.getElementById(
        "subtotal"
    ).innerText =
        "$" + subtotal.toFixed(2);


    document.getElementById(
        "baseImponible"
    ).innerText =
        "$" + base.toFixed(2);


    document.getElementById(
        "montoPropina"
    ).innerText =
        "$" + montoPropina.toFixed(2);


    document.getElementById(
        "montoIVA"
    ).innerText =
        "$" + montoIVA.toFixed(2);


    document.getElementById(
        "total"
    ).innerText =
        "$" + total.toFixed(2);


    document.getElementById(
        "costoPersona"
    ).innerText =
        "$" + costoPersona.toFixed(2);

}


// ============================================================
// GENERAR COTIZACIÓN
// ============================================================

function generarCotizacion() {

    const cliente =
        document
            .getElementById(
                "cliente"
            )
            .value
            .trim();


    const tipoEvento =
        document
            .getElementById(
                "tipoEvento"
            )
            .value;


    const fecha =
        document
            .getElementById(
                "fechaEvento"
            )
            .value;


    const lugar =
        document
            .getElementById(
                "lugarEvento"
            )
            .value;


    if (!cliente) {

        alert(
            "Ingresa el nombre del cliente."
        );

        return;

    }


    if (!tipoEvento) {

        alert(
            "Selecciona el tipo de evento."
        );

        return;

    }


    if (!fecha) {

        alert(
            "Selecciona la fecha del evento."
        );

        return;

    }


    if (!lugar) {

        alert(
            "Selecciona el lugar del evento."
        );

        return;

    }


    calcularTotales();


    alert(
        "La cotización fue preparada correctamente.\n\n" +
        "Por ahora los datos son temporales y no se guardarán " +
        "en la base de datos."
    );

}