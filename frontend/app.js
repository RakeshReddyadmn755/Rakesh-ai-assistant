async function sendMessage() {
  const input = document.getElementById("user-input");
  const question = input.value;
  if (!question) return;

  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div class='user-msg'>You: ${question}</div>`;

  const response = await fetch("https://your-backend-url.onrender.com/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  const data = await response.json();
  chatBox.innerHTML += `<div class='ai-msg'>AI: ${data.answer}</div>`;
  input.value = "";
}
