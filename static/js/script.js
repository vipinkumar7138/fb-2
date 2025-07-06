// Tab switching function
document.addEventListener('DOMContentLoaded', function() {
    // Highlight active tab based on current URL
    const currentPath = window.location.pathname;
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(button => {
        if (button.getAttribute('href') === currentPath) {
            button.classList.add('active');
        }
    });
});

// Show notification function
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notification-text');
    
    // Set notification color based on type
    if (type === 'error') {
        notification.style.backgroundColor = 'var(--danger-color)';
    } else if (type === 'warning') {
        notification.style.backgroundColor = 'var(--warning-color)';
        notificationText.style.color = 'var(--dark-color)';
    } else {
        notification.style.backgroundColor = 'var(--success-color)';
    }
    
    notificationText.textContent = message;
    notification.style.display = 'flex';
    
    setTimeout(() => {
        notification.style.display = 'none';
        notificationText.style.color = ''; // Reset color
    }, 3000);
}

// Form input toggling functions
function toggleTokenInput() {
    const tokenOption = document.getElementById('tokenOption').value;
    document.getElementById('singleTokenInput').classList.toggle('hidden', tokenOption !== 'single');
    document.getElementById('tokenFileInput').classList.toggle('hidden', tokenOption === 'single');
}

function toggleUidInput() {
    const uidOption = document.getElementById('uidOption').value;
    document.getElementById('singleUidInput').classList.toggle('hidden', uidOption !== 'single');
    document.getElementById('multipleUidInput').classList.toggle('hidden', uidOption === 'single');
}

function toggleReportTokenInput() {
    const tokenOption = document.getElementById('reportTokenOption').value;
    document.getElementById('reportSingleTokenInput').classList.toggle('hidden', tokenOption !== 'single');
    document.getElementById('reportTokenFileInput').classList.toggle('hidden', tokenOption === 'single');
}

function toggleGroupOptions() {
    const replyMode = document.getElementById('reply_mode').value;
    document.getElementById('group_ids_section').classList.toggle('hidden', replyMode === 'all');
}

// Clipboard function
function copyToClipboard(text, message = 'Copied to clipboard!') {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showNotification(message);
        } else {
            showNotification('Failed to copy!', 'error');
        }
    } catch (err) {
        console.error('Could not copy text: ', err);
        showNotification('Failed to copy!', 'error');
    }
    
    document.body.removeChild(textarea);
}

// Show error message in form
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let errorDiv = element.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('error-message')) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.color = 'var(--danger-color)';
        errorDiv.style.marginTop = '5px';
        errorDiv.style.fontSize = '0.9em';
        element.parentNode.insertBefore(errorDiv, element.nextSibling);
    }
    
    errorDiv.textContent = message;
}

// Clear error message
function clearError(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const errorDiv = element.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('error-message')) {
        errorDiv.textContent = '';
    }
}

// Show loading spinner
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    let spinner = container.querySelector('.spinner');
    if (!spinner) {
        spinner = document.createElement('div');
        spinner.className = 'spinner';
        container.appendChild(spinner);
    }
    
    spinner.style.display = 'block';
}

// Hide loading spinner
function hideLoading(containerId) {
    const spinner = document.getElementById(containerId)?.querySelector('.spinner');
    if (spinner) {
        spinner.style.display = 'none';
    }
}

// Show status message
function showStatus(containerId, message, type = 'success') {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    let statusDiv = container.querySelector('.status-message');
    if (!statusDiv) {
        statusDiv = document.createElement('div');
        statusDiv.className = 'status-message';
        container.appendChild(statusDiv);
    }
    
    statusDiv.className = `status-message status-${type}`;
    statusDiv.textContent = message;
    statusDiv.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 5000);
}

// UID Extractor Functions
function validateToken() {
    const accessToken = document.getElementById("access_token").value.trim();
    if (!accessToken) {
        showError("access_token", "Please enter a valid access token");
        return;
    }

    showLoading("tokenValidationResult");
    
    fetch('/uid_extractor/validate_token', {
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
                    <h4 style="color: var(--danger-color);">Invalid Token ❌</h4>
                    <p>${data.error.message || "This token is invalid or expired."}</p>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="result-item" style="border-left-color: var(--success-color);">
                    <h4 style="color: var(--success-color);">Valid Token ✅</h4>
                    <p><strong>Profile Name:</strong> ${data.name}</p>
                    <p><strong>Facebook ID:</strong> ${data.id}</p>
                    <button class="copy-btn" onclick="copyToClipboard('${data.id}', 'Facebook ID copied!')">
                        <i class="fas fa-copy"></i> Copy ID
                    </button>
                </div>
            `;
        }
    })
    .catch(error => {
        showStatus("tokenValidationResult", "Error validating token. Please try again.", "error");
    })
    .finally(() => {
        hideLoading("tokenValidationResult");
    });
}

function fetchMessengerChats() {
    const accessToken = document.getElementById("access_token").value.trim();
    if (!accessToken) {
        showError("access_token", "Please enter a valid access token");
        return;
    }

    showLoading("results");
    
    fetch('/uid_extractor/get_messenger_chats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: accessToken })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = '';
        
        if (data.error) {
            showStatus("results", `Error: ${data.error.message || data.error}`, "error");
        } else {
            if (data.chats && data.chats.length > 0) {
                data.chats.forEach(chat => {
                    const chatDiv = document.createElement("div");
                    chatDiv.className = "result-item";
                    chatDiv.innerHTML = `
                        <h4>${chat.name || 'Unnamed Chat'}</h4>
                        <p><strong>Chat UID:</strong> ${chat.id}</p>
                        <button class="copy-btn" onclick="copyToClipboard('${chat.id.replace(/'/g, "\\'")}', 'Chat UID copied!')">
                            <i class="fas fa-copy"></i> Copy UID
                        </button>
                    `;
                    resultsDiv.appendChild(chatDiv);
                });
            } else {
                showStatus("results", "No chats found", "warning");
            }
        }
    })
    .catch(error => {
        showStatus("results", `Error: ${error.message}`, "error");
        console.error('Error:', error);
    })
    .finally(() => {
        hideLoading("results");
    });
}

function fetchPosts() {
    const accessToken = document.getElementById("access_token").value.trim();
    if (!accessToken) {
        showError("access_token", "Please enter a valid access token");
        return;
    }

    showLoading("results");
    
    fetch('/uid_extractor/get_posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: accessToken })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = '';
        
        if (data.error) {
            showStatus("results", `Error: ${data.error.message || data.error}`, "error");
        } else {
            if (data.posts && data.posts.length > 0) {
                data.posts.forEach(post => {
                    const postDiv = document.createElement("div");
                    postDiv.className = "result-item";
                    postDiv.innerHTML = `
                        <h4>${post.name || 'Unnamed Post'}</h4>
                        <p><strong>Post UID:</strong> ${post.id}</p>
                        <p><strong>Profile:</strong> ${post.profile_name}</p>
                        <button class="copy-btn" onclick="copyToClipboard('${post.id.replace(/'/g, "\\'")}', 'Post UID copied!')">
                            <i class="fas fa-copy"></i> Copy UID
                        </button>
                    `;
                    resultsDiv.appendChild(postDiv);
                });
            } else {
                showStatus("results", "No posts found", "warning");
            }
        }
    })
    .catch(error => {
        showStatus("results", `Error: ${error.message}`, "error");
        console.error('Error:', error);
    })
    .finally(() => {
        hideLoading("results");
    });
}

// Form submission handlers
function handleFormSubmit(formId, successCallback) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        submitButton.disabled = true;
        
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            if (typeof successCallback === 'function') {
                successCallback(data);
            } else {
                showNotification(data || 'Operation completed successfully');
            }
        })
        .catch(error => {
            showNotification(error.message || 'An error occurred', 'error');
        })
        .finally(() => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        });
    });
}

// Initialize form handlers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize input toggles
    if (document.getElementById('tokenOption')) {
        toggleTokenInput();
        document.getElementById('tokenOption').addEventListener('change', toggleTokenInput);
    }
    
    if (document.getElementById('uidOption')) {
        toggleUidInput();
        document.getElementById('uidOption').addEventListener('change', toggleUidInput);
    }
    
    if (document.getElementById('reportTokenOption')) {
        toggleReportTokenInput();
        document.getElementById('reportTokenOption').addEventListener('change', toggleReportTokenInput);
    }
    
    if (document.getElementById('reply_mode')) {
        toggleGroupOptions();
        document.getElementById('reply_mode').addEventListener('change', toggleGroupOptions);
    }
    
    // Load logs if on logs page
    if (window.location.pathname.includes('/vip_logs')) {
        loadLogs();
    }
});

// Logs functions
function loadLogs() {
    showLoading('logsContainer');
    
    fetch('/vip_logs/get_logs')
    .then(response => response.json())
    .then(data => {
        const logsContainer = document.getElementById('logsContainer');
        logsContainer.innerHTML = '';
        
        if (data.logs.length === 0) {
            logsContainer.innerHTML = '<div class="result-item">No logs found.</div>';
            return;
        }
        
        data.logs.forEach(log => {
            const logDiv = document.createElement('div');
            logDiv.className = 'result-item';
            logDiv.innerHTML = `
                <h4>${log.action} (${log.status})</h4>
                <p><strong>Time:</strong> ${log.timestamp}</p>
                <p><strong>Details:</strong> ${log.details}</p>
            `;
            logsContainer.appendChild(logDiv);
        });
    })
    .catch(error => {
        showStatus('logsContainer', `Error loading logs: ${error.message}`, 'error');
    })
    .finally(() => {
        hideLoading('logsContainer');
    });
}

function downloadLogs() {
    showLoading('logsContainer');
    
    fetch('/vip_logs/download_logs')
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'vip_logs.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        showNotification(`Error downloading logs: ${error.message}`, 'error');
    })
    .finally(() => {
        hideLoading('logsContainer');
    });
}
