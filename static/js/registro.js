

 function validarNumeros(event, campoId) {
            var charCode = event.which ? event.which : event.keyCode;
            if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                alert("El campo "+campoId+" solo acepta números");
                return false;
            }
            return true;
 }

 function validarSinNum(event, campoId) {
            var charCode = event.which ? event.which : event.keyCode;
            if (charCode >=48 && charCode <= 57) {
                event.preventDefault();
                alert("El Campo "+campoId+" no acepta números");
                return false;
            }
            return true;
 }

function validarSelect() {
            var selectElement = document.getElementById("provincia");
            var selectedValue = selectElement.value;
            if (selectedValue === "") {
                alert("Debes seleccionar una provincia.");
                return false;
            }
            return true;
}

function validarContrasena() {
            var contrasena = document.getElementById("contrasena").value;
            if (contrasena.length < 8 || contrasena.length > 16) {
                document.getElementById("mensaje").textContent = "La contraseña debe tener entre 8 y 16 caracteres";
            } else {
                document.getElementById("mensaje").textContent = "";
            }
}