const presenceSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/presence/'
);

presenceSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    const statusEl = document.querySelector(
        `[data-user-id="${data.user_id}"] .status`
    );

    if (!statusEl) return;

    if (data.state === "online") {
        statusEl.innerHTML = "🟢 Online";
    } else {
        statusEl.innerHTML = "⚪ Offline";
    }
};
