const operationSelect = document.getElementById("operation");

const createFields = document.getElementById("createFields");
const joinFields = document.getElementById("joinFields");

const sendBtn = document.getElementById("sendBtn");

const jsonPreview = document.getElementById("jsonPreview");
const responseText = document.getElementById("response");

const popup = document.getElementById("popup");
const createdKeyInput = document.getElementById("createdKey");
const copyKeyBtn = document.getElementById("copyKeyBtn");
const closePopupBtn = document.getElementById("closePopupBtn");

const chatSection = document.getElementById("chatSection");
const currentRoomInfo = document.getElementById("currentRoomInfo");

const chatMessage = document.getElementById("chatMessage");
const sendMessageBtn = document.getElementById("sendMessageBtn");

const chatLog = document.getElementById("chatLog");

let currentRoomKey = null;
let currentUsername = null;

const OPERATION = {
  CREATE: "CREATE",
  JOIN: "JOIN",
  MESSAGE: "MESSAGE",
  GET_HISTORY: "GET_HISTORY",
};

function createUUID() {
  return crypto.randomUUID();
}

function createHeader(payload) {
  const jsonPayload = JSON.stringify(payload);

  return {
    json_size: jsonPayload.length,
    operation_size: payload.operation.length,
    payload_size: jsonPayload.length,
  };
}

function showCreateFields() {
  createFields.classList.remove("hidden");
  joinFields.classList.add("hidden");
}

function showJoinFields() {
  createFields.classList.add("hidden");
  joinFields.classList.remove("hidden");
}

function createPacket(payload) {
  return {
    header: createHeader(payload),
    payload: payload,
  };
}

async function fetchMessageHistory() {
  if (!currentRoomKey) {
    return;
  }

  const payload = {
    operation: OPERATION.GET_HISTORY,
    key: currentRoomKey,
  };

  const packet = createPacket(payload);

  try {
    const response = await window.api.sendToServer("udp", packet);
    const responseData = JSON.parse(response);

    if (responseData.status === "success") {
      chatLog.textContent = "";

      if (responseData.history.length === 0) {
        chatLog.textContent = "No messages yet.";
      } else {
        responseData.history.forEach((msg) => {
          chatLog.textContent += `${msg.username}: ${msg.message}\n`;
        });
      }
    }

    responseText.textContent = response;
  } catch (error) {
    responseText.textContent = error;
  }
}

operationSelect.addEventListener("change", () => {
  const operation = operationSelect.value;

  if (operation === "create") {
    showCreateFields();
  }

  if (operation === "join") {
    showJoinFields();
  }
});

sendBtn.addEventListener("click", async () => {
  const operation = operationSelect.value;

  let payload;
  let protocol;

  if (operation === "create") {
    const roomName = document.getElementById("createRoomName").value;
    const password = document.getElementById("createPassword").value;
    const key = createUUID();

    payload = {
      operation: OPERATION.CREATE,
      room_name: roomName,
      password: password,
      key: key,
      users: [],
    };

    protocol = "tcp";
  }

  if (operation === "join") {
    const key = document.getElementById("joinKey").value;
    const username = document.getElementById("username").value;

    payload = {
      operation: OPERATION.JOIN,
      key: key,
      username: username,
    };

    protocol = "udp";
  }

  const packet = createPacket(payload);
  jsonPreview.textContent = JSON.stringify(packet, null, 2);

  try {
    const response = await window.api.sendToServer(protocol, packet);
    responseText.textContent = response;

    if (operation === "create") {
      createdKeyInput.value = payload.key;
      popup.classList.remove("hidden");
    }

    if (operation === "join") {
      currentRoomKey = payload.key;
      currentUsername = payload.username;

      chatSection.classList.remove("hidden");

      currentRoomInfo.textContent =
        `Joined Room: ${currentRoomKey}\nUsername: ${currentUsername}`;

      await fetchMessageHistory();
    }
  } catch (error) {
    responseText.textContent = error;
  }
});

sendMessageBtn.addEventListener("click", async () => {
  const message = chatMessage.value;

  if (!message.trim()) {
    return;
  }

  if (!currentRoomKey || !currentUsername) {
    chatLog.textContent += "\nYou must join a room first.";
    return;
  }

  const payload = {
    operation: OPERATION.MESSAGE,
    key: currentRoomKey,
    username: currentUsername,
    message: message,
  };

  const packet = createPacket(payload);
  jsonPreview.textContent = JSON.stringify(packet, null, 2);

  try {
    const response = await window.api.sendToServer("udp", packet);
    responseText.textContent = response;

    await fetchMessageHistory();

    chatMessage.value = "";
  } catch (error) {
    chatLog.textContent += `\nError: ${error}`;
  }
});

copyKeyBtn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(createdKeyInput.value);
  copyKeyBtn.textContent = "Copied!";
});

closePopupBtn.addEventListener("click", () => {
  popup.classList.add("hidden");
  copyKeyBtn.textContent = "Copy Key";
});

showCreateFields();