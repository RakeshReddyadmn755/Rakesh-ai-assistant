async function sendMessage() {
  const input = document.getElementById("user-input");
  const question = input.value.trim();
  if (!question) return;

  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div class='user-msg'>You: “${question}”</div>`;

  try {
    const response = await fetch("https://rakesh-ai-assistant.onrender.com/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await response.json();
    console.log("API response:", data);  // Log for debugging

    if (data.answer) {
      chatBox.innerHTML += `<div class='ai-msg'>AI: ${data.answer}</div>`;
    } else if (data.error) {
      chatBox.innerHTML += `<div class='ai-msg'>AI Error: ${data.error}</div>`;
    } else {
      chatBox.innerHTML += `<div class='ai-msg'>AI: [No response]</div>`;
    }
  } catch (err) {
    console.error("Fetch failed:", err);
    chatBox.innerHTML += `<div class='ai-msg'>AI Error: ${err.message}</div>`;
  }

  input.value = "";
}
