// टैब स्विचिंग फंक्शन
function openTool(toolId) {
    // सभी टैब कंटेंट छिपाएं
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // सभी टैब बटन डिएक्टिवेट करें
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // चयनित टैब दिखाएं
    document.getElementById(toolId).classList.add('active');
    
    // चयनित बटन एक्टिवेट करें
    event.currentTarget.classList.add('active');
}

// नोटिफिकेशन दिखाने का फंक्शन
function showNotification(message) {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notification-text');
    
    notificationText.textContent = message;
    notification.style.display = 'flex';
    
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

// टोकन वैलिडेशन फंक्शन
function validateToken() {
    const accessToken = document.getElementById("access_token").value.trim();
    if (!accessToken) {
        showError("कृपया एक वैध एक्सेस टोकन दर्ज करें");
        return;
    }

    fetch('/validate_token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: accessToken })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById("tokenValidationResult");
        if (data.error) {
            resultDiv.innerHTML = `
                <div class="result-item" style="border-left-color: var(--danger-color);">
                    <h4 style="color: var(--danger-color);">अमान्य टोकन ❌</h4>
                    <p>${data.error.message || "यह टोकन अमान्य या समाप्त हो चुका है।"}</p>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="result-item" style="border-left-color: var(--success-color);">
                    <h4 style="color: var(--success-color);">वैध टोकन ✅</h4>
                    <p><strong>प्रोफाइल नाम:</strong> ${data.name}</p>
                    <p><strong>फेसबुक आईडी:</strong> ${data.id}</p>
                    <button class="copy-btn" onclick="copyToClipboard('${data.id}', 'फेसबुक आईडी कॉपी की गई!')">
                        <i class="fas fa-copy"></i> आईडी कॉपी करें
                    </button>
                </div>
            `;
        }
    })
    .catch(error => {
        showError("टोकन वैलिडेट करने में त्रुटि। कृपया पुनः प्रयास करें।");
    });
}

// UID एक्सट्रैक्टर फंक्शन्स
function fetchMessengerChats() {
    const accessToken = document.getElementById("access_token").value.trim();
    if (!accessToken) {
        showError("कृपया एक वैध एक्सेस टोकन दर्ज करें");
        return;
    }

    fetch('/get_messenger_chats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: accessToken })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('नेटवर्क प्रतिक्रिया ठीक नहीं थी');
        }
        return response.json();
    })
    .then(data => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = '';
        
        if (data.error) {
            showError(`त्रुटि: ${data.error.message || data.error}`);
        } else {
            if (data.chats && data.chats.length > 0) {
                data.chats.forEach(chat => {
                    const chatDiv = document.createElement("div");
                    chatDiv.className = "result-item";
                    chatDiv.innerHTML = `
                        <h4>${chat.name || 'अनामित चैट'}</h4>
                        <p><strong>चैट UID:</strong> ${chat.id}</p>
                        <button class="copy-btn" onclick="copyToClipboard('${chat.id.replace(/'/g, "\\'")}', 'चैट UID कॉपी की गई!')">
                            <i class="fas fa-copy"></i> UID कॉपी करें
                        </button>
                    `;
                    resultsDiv.appendChild(chatDiv);
                });
            } else {
                showError("कोई चैट नहीं मिली");
            }
        }
    })
    .catch(error => {
        showError(`त्रुटि: ${error.message}`);
        console.error('त्रुटि:', error);
    });
}

function fetchPosts() {
    const accessToken = document.getElementById("access_token").value.trim();
    if (!accessToken) {
        showError("कृपया एक वैध एक्सेस टोकन दर्ज करें");
        return;
    }

    fetch('/get_posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: accessToken })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('नेटवर्क प्रतिक्रिया ठीक नहीं थी');
        }
        return response.json();
    })
    .then(data => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = '';
        
        if (data.error) {
            showError(`त्रुटि: ${data.error.message || data.error}`);
        } else {
            if (data.posts && data.posts.length > 0) {
                data.posts.forEach(post => {
                    const postDiv = document.createElement("div");
                    postDiv.className = "result-item";
                    postDiv.innerHTML = `
                        <h4>${post.name || 'अनामित पोस्ट'}</h4>
                        <p><strong>पोस्ट UID:</strong> ${post.id}</p>
                        <p><strong>प्रोफाइल:</strong> ${post.profile_name}</p>
                        <button class="copy-btn" onclick="copyToClipboard('${post.id.replace(/'/g, "\\'")}', 'पोस्ट UID कॉपी की गई!')">
                            <i class="fas fa-copy"></i> UID कॉपी करें
                        </button>
                    `;
                    resultsDiv.appendChild(postDiv);
                });
            } else {
                showError("कोई पोस्ट नहीं मिली");
            }
        }
    })
    .catch(error => {
        showError(`त्रुटि: ${error.message}`);
        console.error('त्रुटि:', error);
    });
}

// क्लिपबोर्ड फंक्शन
function copyToClipboard(text, message) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showNotification(message || "क्लिपबोर्ड पर कॉपी किया गया!");
        } else {
            showNotification("कॉपी करने में विफल!");
        }
    } catch (err) {
        console.error('टेक्स्ट कॉपी नहीं किया जा सका: ', err);
        showNotification("कॉपी करने में विफल!");
    }
    
    document.body.removeChild(textarea);
}

function showError(message) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div class="result-item" style="border-left-color: var(--danger-color);">
            <h4 style="color: var(--danger-color);">त्रुटि</h4>
            <p>${message}</p>
        </div>
    `;
}

// मैसेज सेंडर फंक्शन्स
function toggleTokenInput() {
    const tokenOption = document.getElementById('tokenOption').value;
    if (tokenOption === 'single') {
        document.getElementById('singleTokenInput').style.display = 'block';
        document.getElementById('tokenFileInput').style.display = 'none';
    } else {
        document.getElementById('singleTokenInput').style.display = 'none';
        document.getElementById('tokenFileInput').style.display = 'block';
    }
}

// UID इनपुट टॉगल फंक्शन
function toggleUidInput() {
    const uidOption = document.getElementById('uidOption').value;
    if (uidOption === 'single') {
        document.getElementById('singleUidInput').style.display = 'block';
        document.getElementById('multipleUidInput').style.display = 'none';
    } else {
        document.getElementById('singleUidInput').style.display = 'none';
        document.getElementById('multipleUidInput').style.display = 'block';
    }
}

// ऑटो रिपोर्टर फंक्शन्स
function toggleReportTokenInput() {
    const tokenOption = document.getElementById('reportTokenOption').value;
    if (tokenOption === 'single') {
        document.getElementById('reportSingleTokenInput').style.display = 'block';
        document.getElementById('reportTokenFileInput').style.display = 'none';
    } else {
        document.getElementById('reportSingleTokenInput').style.display = 'none';
        document.getElementById('reportTokenFileInput').style.display = 'block';
    }
}

// ऑटो रिप्लाई फंक्शन्स
function toggleGroupOptions() {
    const replyMode = document.getElementById('reply_mode').value;
    const groupIdsSection = document.getElementById('group_ids_section');
    
    if (replyMode === 'all') {
        groupIdsSection.style.display = 'none';
    } else {
        groupIdsSection.style.display = 'block';
    }
}

// लॉड लॉग्स फंक्शन
function loadLogs() {
    fetch('/get_logs')
