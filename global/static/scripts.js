    const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";

    const chatSocket = new WebSocket(
        wsProtocol + window.location.host + "/ws/chat/"
    );

    chatSocket.onmessage = function(event) {

        const data = JSON.parse(event.data);

        console.log("Recebido:", data);

        const message_container = document.getElementById("message-container");
        const newDiv = document.createElement("div");

        newDiv.innerText = data.message ?? JSON.stringify(data);

        message_container.appendChild(newDiv);
    };

    chatSocket.onclose = function(e) {
        console.error("Chat socket closed unexpectedly");
    };