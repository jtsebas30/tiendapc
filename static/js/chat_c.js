// Variables para la bola flotante y el chat
var floatingButton = document.getElementById("floatingButton");
var chatContainer = document.getElementById("chatContainer");
var closeButton = document.getElementById("closeButton");
var chatBody = document.getElementById("chatBody");
var userInput = document.getElementById("userInput");

// Función para mostrar/ocultar el chat al hacer clic en la bola flotante
floatingButton.addEventListener("click", function () {
    chatContainer.style.display = "block";
    // Mostrar mensaje de bienvenida
});

closeButton.addEventListener("click", function () {
    chatContainer.style.display = "none";
});

// Función para enviar mensajes
function sendMessage() {
    var userMessage = userInput.value;
    appendMessage("Tú", userMessage);

    // Enviar el mensaje al servidor mediante una solicitud POST
    fetch("/get_response_c", {
        method: "POST",
        body: new URLSearchParams({"user_message": userMessage}),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.text())
    .then(data => {
        appendMessage("Chatbot", data);
    });

    userInput.value = "";
}

// Función para agregar mensajes al chat
function appendMessage(sender, message) {
    var newMessage = document.createElement("div");
    newMessage.className = "message";

    if (message.trim().toUpperCase() === "BIENVENIDA") {
        // Mostrar solo el contenido del mensaje de bienvenida
        newMessage.textContent = "¡Hola, Bienvenido a CompuEc! ¿En que puedo ayudarte?";
    } else {
        // Mostrar mensaje normal con remitente
        newMessage.textContent = sender + ": " + message;
    }

    chatBody.appendChild(newMessage);
}

// Agregar mensaje de bienvenida al cargar el chat
window.addEventListener("load", function () {
    appendMessage("Chatbot", "BIENVENIDA");
});