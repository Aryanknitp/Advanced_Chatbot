// Register operational DOM anchor endpoints when scripts finish linking
const messageInput = document.getElementById("message");
const chatWindow = document.getElementById("chat");
const sendButton = document.getElementById("sendBtn");

// Attach an ambient keypress engine listener to capture standard Enter key cycles
messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});

// function appendMessage(sender, text) {
//   // Construct explicit protective wrappers to stop raw markup string injections
//   const rowElement = document.createElement("div");
//   rowElement.classList.add("message-row", `${sender}-row`);

//   const bubbleElement = document.createElement("div");
//   bubbleElement.classList.add("bubble");
//   // Using textContent completely neutralizes unexpected raw HTML evaluation security exploits
//   bubbleElement.textContent = text;

//   rowElement.appendChild(bubbleElement);
//   chatWindow.appendChild(rowElement);

//   // Smoothly align workspace visibility frame targeting the latest additions
//   chatWindow.scrollTop = chatWindow.scrollHeight;
// }


function appendMessage(sender, text) {
  const rowElement = document.createElement("div");
  rowElement.classList.add("message-row", `${sender}-row`);

  const bubbleElement = document.createElement("div");
  bubbleElement.classList.add("bubble");

  if (sender === "user") {
    // User messages remain safe plain text
    bubbleElement.textContent = text;
  } else {
    // 1. Escapes any accidental raw HTML tags to prevent cross-site scripting (XSS)
    let sanitizedText = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // 2. Converts Markdown links [Anchor Text](URL) into real HTML links with safety attributes
    // This regex captures: [Any text here](http://... or https://...)
    const markdownLinkRegex = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g;
    
    sanitizedText = sanitizedText.replace(markdownLinkRegex, (match, anchorText, url) => {
      return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="chat-link">${anchorText}</a>`;
    });

    // Render the safely converted markup layout
    bubbleElement.innerHTML = sanitizedText;
  }

  rowElement.appendChild(bubbleElement);
  chatWindow.appendChild(rowElement);

  // Smooth scroll view alignment targeting latest responses
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function sendMessage() {
  const messageText = messageInput.value.trim();
  
  // Protect pipeline from submitting whitespace-only requests
  if (!messageText) return;

  // Append user text elements immediately to the interface log
  appendMessage("user", `You: ${messageText}`);
  messageInput.value = "";

  // Render a sleek placeholder bubble while Groq handles execution processing
  const loadingRow = document.createElement("div");
  loadingRow.classList.add("message-row", "bot-row");
  const loadingBubble = document.createElement("div");
  loadingBubble.classList.add("bubble");
  loadingBubble.textContent = "Bot is typing...";
  loadingRow.appendChild(loadingBubble);
  chatWindow.appendChild(loadingRow);
  chatWindow.scrollTop = chatWindow.scrollHeight;

  // Dispatch data to your local backend server environment
  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: messageText }),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Network request execution blocked");
      return response.json();
    })
    .then((payload) => {
      // Clear away the typing placeholder element
      loadingRow.remove();
      
      // Print out the securely sanitized final string response content
      appendMessage("bot", `Bot: ${payload.reply}`);
    })
    .catch((error) => {
      loadingRow.remove();
      appendMessage("bot", `System Failure: Unable to clear network routing. (${error.message})`);
    });
}
