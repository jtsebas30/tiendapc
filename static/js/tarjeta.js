 function validarTarjeta(event) {
            var charCode = event.which ? event.which : event.keyCode;
            if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                event.preventDefault();
                alert("No se aceptan caracteres en el número de tarjeta");
                return false;
            }
            return true;
 }

 function validarTarjetaCVC(event) {
            var charCode = event.which ? event.which : event.keyCode;
            if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                event.preventDefault();
                alert("El CVC de la tarjeta son unicamente números");
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
