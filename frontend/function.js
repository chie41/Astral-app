// Định nghĩa URL API cho backend
const API_URL = "http://localhost:8000/api/chat"; // URL API của backend cho chức năng chat

// Hàm gửi tin nhắn trong chat
// Được gọi bởi: 
// 1. Nhấn vào nút "Cat Assistant (V1)" (version-label)
// 2. Nhấn vào nút gửi (send-btn)
// 3. Nhấn phím Enter trong ô nhập tin nhắn (chatInput)
async function sendMessage() {
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const chatMessages = document.getElementById('chatMessages');
  const assistantHeader = document.getElementById('assistantHeader');

  assistantHeader.classList.add('hidden');

  const messageText = chatInput.value.trim();
  let userMessage = document.createElement('div');
  userMessage.classList.add('message', 'user');
  userMessage.innerHTML = `
    <div class="message-content">${messageText || 'Hi, I want to create a machine learning model to predict future sales based on past transaction data. Can you help me?'}</div>
  `;
  chatMessages.appendChild(userMessage);

  // Clear input immediately after sending (moved up from bottom)
  chatInput.value = '';
  chatInput.placeholder = 'Moew~ Describe your project!';
  sendBtn.classList.remove('active');
  sendBtn.disabled = true;

  const payload = {
    user_id: "default",
    message: messageText || "Hi, I want to create a machine learning model to predict future sales based on past transaction data. Can you help me?"
  };

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    // Add loading dots to AI message
    let assistantMessage = document.createElement('div');
    assistantMessage.classList.add('message', 'assistant');
    assistantMessage.innerHTML = `
      <img src="image/logo.png" alt="Cat Assistant" />
      <div class="message-content"><span class="loading-dots"><span>.</span><span>.</span><span>.</span></span></div>
    `;
    chatMessages.appendChild(assistantMessage);
    const messageContentDiv = assistantMessage.querySelector('.message-content');

    // Đọc stream dần
    let isFirstChunk = true; // Track first chunk to clear loading dots
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      const htmlChunk = chunk.replace(/\n/g, '<br>');
      if (isFirstChunk) {
        // Clear loading dots on first chunk
        messageContentDiv.innerHTML = '';
        isFirstChunk = false;
      }
      messageContentDiv.innerHTML += htmlChunk;
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

  } catch (error) {
    const errorMessage = document.createElement('div');
    errorMessage.classList.add('message', 'assistant');
    errorMessage.innerHTML = `
      <img src="image/logo.png" alt="Cat Assistant" />
      <div class="message-content">❌ Error: ${error.message}</div>
    `;
    chatMessages.appendChild(errorMessage);
  }

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hàm mở modal xác nhận trong boxchat.html
// Được gọi bởi: Nhấn vào nút "Create" trong tin nhắn của trợ lý
function openModal() {
  document.getElementById('confirmModal').style.display = 'flex';
}

// Hàm đóng modal xác nhận trong boxchat.html
// Được gọi bởi: Nhấn vào nút "Nah" trong modal xác nhận
function closeModal() {
  document.getElementById('confirmModal').style.display = 'none';
}

// Hàm xác nhận tạo dự án và chuyển hướng
// Được gọi bởi: Nhấn vào nút "Yeah" trong modal xác nhận
function confirmProject() {
  window.location.href = 'manualcreationstep1.html';
}

// Thiết lập các sự kiện lắng nghe cho boxchat.html
// Được gọi khi trang boxchat.html tải xong (onload)
function setupBoxChatListeners() {
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');

  chatInput.addEventListener('input', function () {
    if (chatInput.value.trim() !== '') {
      chatInput.placeholder = '';
      sendBtn.classList.add('active');
      sendBtn.disabled = false;
    } else {
      chatInput.placeholder = 'Moew~ Describe your project!';
      sendBtn.classList.remove('active');
      sendBtn.disabled = true;
    }
  });

  chatInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey && chatInput.value.trim() !== '') {
      e.preventDefault();
      sendMessage();
    }
  });

  sendBtn.addEventListener('click', function () {
    if (!sendBtn.disabled) {
      sendMessage();
    }
  });
}