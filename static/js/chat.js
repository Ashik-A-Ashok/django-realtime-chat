const socket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + receiverId + '/'
);

const chatBox = document.getElementById('chat-box');
const input = document.getElementById('message-input');

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (!data.message) return;

    const div = document.createElement('div');
    div.innerText = data.sender + ': ' + data.message;
    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
};

function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    socket.send(JSON.stringify({
        type: "message",
        message: message
    }));

    input.value = '';
}

input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});
