  $(document).ready(function () {
            // Mostrar u ocultar el chatbot al hacer clic en el botón flotante
            $("#chatbot-toggle").click(function () {
                $("#chatbot-container").toggle();
            });

            // Cerrar el chatbot al hacer clic en el botón "X"
            $("#chatbot-close").click(function () {
                $("#chatbot-container").hide();
            });

             // Escucha el evento click del botón "Enviar"
    document.getElementById("send-button").addEventListener("click", function () {
        // Obtiene el mensaje ingresado por el usuario
        const userInput = document.getElementById("user-input").value;

        // Añade el mensaje del usuario al chat
        appendUserMessage(userInput);

        // Responde con un mensaje estático del chatbot
        setTimeout(function () {
            const response = "Gracias por tu mensaje: " + userInput;
            appendBotMessage(response);
        }, 1000);
    });

    // Función para añadir el mensaje del usuario al chat
    function appendUserMessage(message) {
        const userMessage = '<div class="chat-message user-message">' + message + '</div>';
        document.querySelector(".chat-content").insertAdjacentHTML("beforeend", userMessage);
        document.getElementById("user-input").value = "";
    }

    // Función para añadir el mensaje del chatbot al chat
    function appendBotMessage(message) {
        const botMessage = '<div class="chat-message bot-message">' + message + '</div>';
        document.querySelector(".chat-content").insertAdjacentHTML("beforeend", botMessage);
    }
        });