function filtrarEventos() {

    const texto = document
        .getElementById("buscarEvento")
        .value
        .toLowerCase();

    const estado = document
        .getElementById("filtroEstado")
        .value
        .toLowerCase();

    const filas = document.querySelectorAll(
        "#tablaEventos tbody tr"
    );

    filas.forEach(function (fila) {

        const contenido = fila
            .innerText
            .toLowerCase();

        const coincideTexto =
            contenido.includes(texto);

        const estadoFila =
            fila
                .querySelector(".status")
                ?.innerText
                .toLowerCase() || "";

        const coincideEstado =
            estado === "" ||
            estadoFila === estado;

        if (
            coincideTexto &&
            coincideEstado
        ) {

            fila.style.display = "";

        } else {

            fila.style.display = "none";

        }

    });

}