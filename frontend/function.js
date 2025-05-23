// Định nghĩa URL API cho backend
const API_URL = "http://localhost:8000/api/chat"; // URL API của backend cho chức năng chat

// Hàm bật/tắt dropdown của người dùng trong thanh điều hướng
// Được gọi bởi: Nhấn vào hồ sơ người dùng (avatar + tên người dùng) trong thanh điều hướng
function toggleDropdown() {
  const dropdown = document.getElementById('userDropdown');
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

//Xóa mọi thông tin đang tạo dở
async function clearChatSession() {
  const payload = { user_id: "default" };
  const url = "http://localhost:8000/api/clear_session";

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error(`Lỗi ${response.status}:`, errText);
      return;
    }

    const result = await response.json();
    console.log(result.message);
  } catch (error) {
    console.error("Lỗi khi gọi API:", error);
  }
}

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

    console.log("dhsaid")
    let assistantMessage = document.createElement('div');
    assistantMessage.classList.add('message', 'assistant');
    assistantMessage.innerHTML = `<img src="image/logo.png" alt="Cat Assistant" /><div class="message-content"></div>`;
    chatMessages.appendChild(assistantMessage);
    const messageContentDiv = assistantMessage.querySelector('.message-content');

    // Đọc stream dần
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      const htmlChunk = chunk.replace(/\n/g, '<br>'); // <-- Sửa tại đây
      messageContentDiv.innerHTML += htmlChunk;
      chatMessages.scrollTop = chatMessages.scrollHeight;

    }

    //Tạo nút bấm dưới text AI 
    if (messageContentDiv.innerText.toLowerCase().includes("thông tin dự án")) {
      console.log("Thêm nút tạo dự án")
      const createBtn = document.createElement("button");
      createBtn.innerText = "Tạo";
      createBtn.className = "create-btn"; // gợi ý: bạn có thể định nghĩa CSS cho nút này
      createBtn.onclick = openModal; // gọi hàm tạo project
      messageContentDiv.appendChild(createBtn); // thêm nút vào ngay sau tin nhắn của assistant
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

  chatInput.value = '';
  chatInput.placeholder = 'Moew~ Describe your project!';
  sendBtn.classList.remove('active');
  sendBtn.disabled = true;

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
async function confirmProject() {

  const payload = {
    user_id: "default",
  };


  try {
    const response = await fetch("http://localhost:8000/api/confirm_create_project", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
    console.log(result.message);

    if (result.status === 'ok') {
      localStorage.setItem('project_suggestion', JSON.stringify(result.config));
      window.location.href = 'manualcreationstep1.html';
    } else {
      alert("Không thể tạo project.");
    }
  } catch (err) {
    alert("Lỗi khi xác nhận tạo project: " + err.message);
  }
}

// Hàm mở modal tạo dự án mới trong dashboard.html
// Được gọi bởi: Nhấn vào nút "+ New project" (new-project-btn)
async function openNewProjectModal() {
  await clearChatSession()

  localStorage.removeItem('project_suggestion');
  document.getElementById('newProjectModal').style.display = 'flex';
}

// Hàm đóng modal tạo dự án mới trong dashboard.html
// Được gọi bởi: Nhấn vào nút "×" (close-btn) trong modal tạo dự án mới
function closeNewProjectModal() {
  localStorage.removeItem('project_suggestion');
  document.getElementById('newProjectModal').style.display = 'none';

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