document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const promptInput = document.getElementById('prompt-input');
    const chatContainer = document.getElementById('chat-container');
    const sendButton = document.getElementById('send-button');
    const chatList = document.getElementById('chat-list');
    const newChatBtn = document.getElementById('new-chat-btn');
    const stopButton = document.getElementById('stop-button');
    const agentTabs = document.querySelectorAll('.agent-tab');
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    
    // File inputs
    const fileInput = document.getElementById('file-input');
    const attachButton = document.getElementById('attach-button');
    const filePreviewContainer = document.getElementById('file-preview-container');

    let currentSessionId = null;
    let abortController = null;
    let targetAgent = "Auto";
    let selectedFiles = [];

    // Setup Agent Tabs
    agentTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active from all
            agentTabs.forEach(t => t.classList.remove('active'));
            // Add active to clicked
            tab.classList.add('active');
            
            targetAgent = tab.getAttribute('data-agent');
            
            if (targetAgent === "Auto") {
                promptInput.placeholder = "Type your prompt here...";
            } else {
                promptInput.placeholder = `Ask the ${tab.innerText}...`;
            }
        });
    });

    // Setup Hamburger Menu
    if (hamburgerMenu && sidebar && sidebarOverlay) {
        hamburgerMenu.addEventListener('click', () => {
            sidebar.classList.add('open');
            sidebarOverlay.classList.add('open');
        });

        sidebarOverlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('open');
        });
        
        // Also close sidebar when a chat is clicked on mobile
        chatList.addEventListener('click', (e) => {
            if (e.target.closest('.chat-item') && window.innerWidth <= 768) {
                sidebar.classList.remove('open');
                sidebarOverlay.classList.remove('open');
            }
        });
    }

    // Setup File Attachments
    attachButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const newFiles = Array.from(e.target.files);
        if (selectedFiles.length + newFiles.length > 10) {
            alert("You can only attach a maximum of 10 files.");
            return;
        }
        selectedFiles = [...selectedFiles, ...newFiles];
        updateFilePreviews();
        fileInput.value = ''; // Reset input
    });

    function updateFilePreviews() {
        filePreviewContainer.innerHTML = '';
        selectedFiles.forEach((file, index) => {
            const chip = document.createElement('div');
            chip.className = 'file-chip';
            
            let contentHtml = `<span>${file.name}</span>`;
            if (file.type.startsWith('image/')) {
                const imgUrl = URL.createObjectURL(file);
                contentHtml = `<img src="${imgUrl}" alt="${file.name}"><span>${file.name}</span>`;
            }

            chip.innerHTML = `
                ${contentHtml}
                <span class="remove-btn" data-index="${index}">×</span>
            `;
            filePreviewContainer.appendChild(chip);
        });
        
        // Add remove listeners
        document.querySelectorAll('.file-chip .remove-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idx = parseInt(e.target.getAttribute('data-index'));
                selectedFiles.splice(idx, 1);
                updateFilePreviews();
            });
        });
    }

    // Load all chats on startup
    loadChatList();

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function clearChatContainer() {
        chatContainer.innerHTML = '';
        addMessage('Hello! I am your Master Router Agent. What can I help you with today?', false, null);
    }

    async function loadChatList() {
        try {
            const response = await fetch('/api/v1/chats');
            const sessions = await response.json();
            
            chatList.innerHTML = '';
            sessions.forEach(session => {
                const item = document.createElement('div');
                item.className = 'chat-item';
                if (session.session_id === currentSessionId) {
                    item.classList.add('active');
                }
                
                const dateStr = new Date(session.updated_at * 1000).toLocaleString();
                
                item.innerHTML = `
                    <div class="chat-title">${session.title}</div>
                    <div class="chat-date">${dateStr}</div>
                `;
                
                item.addEventListener('click', () => loadChatHistory(session.session_id));
                chatList.appendChild(item);
            });
        } catch (e) {
            console.error("Failed to load chat list", e);
        }
    }

    async function loadChatHistory(sessionId) {
        currentSessionId = sessionId;
        try {
            const response = await fetch(`/api/v1/chats/${sessionId}`);
            const data = await response.json();
            
            chatContainer.innerHTML = ''; // clear all
            
            data.history.forEach(msg => {
                addMessage(msg.content, msg.is_user, msg.agent);
            });
            
            loadChatList(); // Refresh active state
        } catch (e) {
            console.error("Failed to load chat history", e);
        }
    }

    newChatBtn.addEventListener('click', () => {
        currentSessionId = null;
        clearChatContainer();
        loadChatList();
    });

    function addMessage(content, isUser = false, agentName = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'system'}`;
        
        let agentTagHtml = '';
        if (agentName && !isUser) {
            agentTagHtml = `<div class="agent-tag">${agentName}</div>`;
        }

        const avatarText = isUser ? 'ME' : 'AI';
        
        // Parse markdown if it's an AI response and marked.js is loaded
        const displayContent = isUser ? content : (window.marked ? marked.parse(content) : content);

        messageDiv.innerHTML = `
            <div class="avatar">${avatarText}</div>
            <div class="bubble">
                ${agentTagHtml}
                <div class="content">${displayContent}</div>
            </div>
        `;
        
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv;
    }

    function showTypingIndicator() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system typing-msg';
        messageDiv.innerHTML = `
            <div class="avatar">AI</div>
            <div class="bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const task = promptInput.value.trim();
        if (!task) return;

        // Add user message
        addMessage(task, true);
        
        // Clear input and disable send button
        promptInput.value = '';
        promptInput.disabled = true;
        sendButton.style.display = 'none';
        stopButton.style.display = 'flex';
        
        // Setup AbortController
        abortController = new AbortController();
        
        // Show typing indicator
        const typingIndicator = showTypingIndicator();

        try {
            // Upload files first if any
            let uploadedImages = [];
            let uploadedFileContents = [];
            
            if (selectedFiles.length > 0) {
                const formData = new FormData();
                selectedFiles.forEach(f => formData.append('files', f));
                
                const uploadResp = await fetch('/api/v1/upload', {
                    method: 'POST',
                    body: formData,
                    signal: abortController.signal
                });
                
                if (!uploadResp.ok) {
                    throw new Error(`Upload failed with status ${uploadResp.status}`);
                }
                
                const uploadData = await uploadResp.json();
                uploadedImages = uploadData.images || [];
                uploadedFileContents = uploadData.file_contents || [];
                
                // Clear selection
                selectedFiles = [];
                updateFilePreviews();
            }

            // Call FastAPI backend
            const response = await fetch('/api/v1/task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                signal: abortController.signal,
                body: JSON.stringify({
                    task: task,
                    context: {},
                    session_id: currentSessionId,
                    target_agent: targetAgent,
                    images: uploadedImages,
                    file_contents: uploadedFileContents
                })
            });

            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }

            const data = await response.json();
            currentSessionId = data.session_id; // Capture session id
            
            // Remove typing indicator
            typingIndicator.remove();
            
            // Parse response and display
            const agentOutput = data.result.agent_output;
            addMessage(agentOutput.result, false, agentOutput.agent);
            
            // Refresh sidebar
            loadChatList();
            
        } catch (error) {
            typingIndicator.remove();
            if (error.name === 'AbortError') {
                addMessage(`<span style="color: var(--text-muted);">Generation stopped.</span>`, false, 'System');
            } else {
                console.error('Error calling API:', error);
                addMessage(`<span style="color: #ef4444;">Error: Could not connect to AI server. (${error.message})</span>`, false, 'System Error');
            }
        } finally {
            // Re-enable input
            abortController = null;
            promptInput.disabled = false;
            sendButton.style.display = 'flex';
            stopButton.style.display = 'none';
            promptInput.focus();
        }
    });

    stopButton.addEventListener('click', () => {
        if (abortController) {
            abortController.abort();
        }
    });
});
