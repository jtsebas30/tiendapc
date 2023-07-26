
 var errores=0;

 function validarTarjeta(event) {
            var charCode = event.which ? event.which : event.keyCode;
            if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                event.preventDefault();
                alert("No se aceptan caracteres en el número de tarjeta");
                errores++;
                console.log(errores)
                return false;
            }
            return true;
 }

 function validarTarjetaCVC(event) {
            var charCode = event.which ? event.which : event.keyCode;
            if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                event.preventDefault();

                alert("El CVC de la tarjeta son unicamente números");
                errores++;
                console.log(errores)
                return false;
            }
            return true;
 }

 function validarSelectMes() {
            var selectElement = document.getElementById("mes");
            var selectedValue = selectElement.value;
            if (selectedValue === "") {
            console.log("error de validador");
                alert("Debes seleccionar el mes de la Tarjeta.");
                return false;
            }
            console.log("validador correcto");
            return true;
}

 function validarSelectAnio() {
            var selectElement = document.getElementById("anio");
            var selectedValue = selectElement.value;
            if (selectedValue === "") {
                alert("Debes seleccionar el año de la Tarjeta.");
                return false;
            }
            return true;
}

function validarFormulario() {
            // Asignar el valor de "errores" al campo oculto antes de enviar el formulario
            document.getElementById("errores").value = errores;

            // Reiniciar el contador de errores para futuras interacciones
            errores = 0;

            // Permitir el envío del formulario
            return true;
        }