/*
  In Phase 2's client.py, we created a raw socket, 
  used a recv_thread to receive messages in the background, 
  and used the main loop to handle input().

  In Phase 3, the browser natively provides the "WebSocket" object - 
  so we don't need to manually create a thread. The browser 
  monitors the connection in the background for us.
*/

const loginScreen = document.getElementById("login-screen");
const chatScreen = document.getElementById("chat-screen");
const usernameInput = document.getElementById("username-input");
const joinBtn = document.getElementById("join-btn");
const errorMsg = document.getElementById("error-msg");

const messagesDiv = document.getElementById("messages");
const messageForm = document.getElementById("message-form");
const messageInput = document.getElementById("message-input");
const userListEl = document.getElementById("user-list");
const userCountEl = document.getElementById("user-count");

let socket = null;
let myUsername = null;

joinBtn.addEventListener("click", joinChat);
usernameInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") joinChat();
});

function joinChat() {
  const username = usernameInput.value.trim();
  if (!username) {
    errorMsg.textContent = "Please enter a username!";
    return;
  }

  myUsername = username;

  // In Phase 2: client.connect(('127.0.0.1', 12345))
  // In Phase 3: We use a WebSocket URL.
  // The protocol is "ws://" - similar to HTTP, but
  // the connection is kept open as a persistent stream.
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/${encodeURIComponent(username)}`;

  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    loginScreen.classList.add("hidden");
    chatScreen.classList.remove("hidden");
    messageInput.focus();
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    handleIncoming(data);
  };

  socket.onclose = () => {
    addSystemMessage("Connection to the server was lost. Please refresh the page.");
  };

  socket.onerror = () => {
    errorMsg.textContent = "Failed to connect. Please check if the server is running.";
  };
}

function handleIncoming(data) {
  if (data.type === "message") {
    addChatMessage(data.user, data.text, data.time, data.user === myUsername);
  } else if (data.type === "system") {
    addSystemMessage(`${data.text}  (${data.time})`);
  } else if (data.type === "user_list") {
    updateUserList(data.users);
  }
}

function addChatMessage(user, text, time, isMe) {
  const wrapper = document.createElement("div");
  wrapper.className = "msg" + (isMe ? " me" : "");

  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = `${user} · ${time}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  wrapper.appendChild(meta);
  wrapper.appendChild(bubble);
  messagesDiv.appendChild(wrapper);
  scrollToBottom();
}

function addSystemMessage(text) {
  const wrapper = document.createElement("div");
  wrapper.className = "msg system";
  wrapper.textContent = text;
  messagesDiv.appendChild(wrapper);
  scrollToBottom();
}

function updateUserList(users) {
  userListEl.innerHTML = "";
  users.forEach((u) => {
    const li = document.createElement("li");
    li.textContent = u;
    userListEl.appendChild(li);
  });
  userCountEl.textContent = `${users.length} online`;
}

function scrollToBottom() {
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

messageForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = messageInput.value.trim();
  if (!text || !socket || socket.readyState !== WebSocket.OPEN) return;

  // In Phase 2: client.send(msg.encode('utf-8'))
  // In Phase 3: socket.send(text) - the browser 
  // automatically packages and sends it as a text frame.
  socket.send(text);
  messageInput.value = "";
});