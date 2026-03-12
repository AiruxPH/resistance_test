document.getElementById('run-btn').addEventListener('click', runTest);

// Uptime Clock Logic
let startTime = Date.now();
setInterval(() => {
    const elapsed = Date.now() - startTime;
    const hours = Math.floor(elapsed / 3600000).toString().padStart(2, '0');
    const minutes = Math.floor((elapsed % 3600000) / 60000).toString().padStart(2, '0');
    const seconds = Math.floor((elapsed % 60000) / 1000).toString().padStart(2, '0');
    document.getElementById('uptime-clock').innerText = `${hours}:${minutes}:${seconds}`;
}, 1000);

// Threat Translator logic
const threatMap = {
    "A02": {
        "WARNING": { title: "Insecure Connection", desc: "This site doesn't use HTTPS. Any info you enter can be stolen by anyone on the same network." }
    },
    "A03": {
        "WARNING": { title: "Injection Risk", desc: "The site reflects raw code. A hacker could steal cookies or redirect users to scam sites." }
    },
    "A05": {
        "DANGER": { title: "Exposed Secret Files", desc: "Critical system files (like .env) are public. Your database passwords and API keys are visible to the world." }
    },
    "A07": {
        "WARNING": { title: "Weak Rate Limiting", desc: "A hacker can try thousands of passwords a second without being blocked. Accounts are at high risk." }
    },
    "DB-HARD": {
        "DANGER": { title: "Public Database Folder", desc: "Your 'database' folder is visible. Hackers can download your raw data directly." },
        "WARNING": { title: "Remote SQL Exposed", desc: "Your database port (3306) is open to the internet. Hackers can try to login remotely." }
    }
};

function logToConsole(message, type = 'info', prefix = 'SCANNER') {
    const consoleBox = document.getElementById('console');
    const line = document.createElement('div');
    
    // Normalize type for CSS
    let cssClass = type.toLowerCase();
    if (cssClass === 'danger') cssClass = 'error'; // Map DANGER to red error style
    
    line.className = `line ${cssClass}`;
    
    const timestamp = new Date().toLocaleTimeString([], { hour12: false });
    line.innerHTML = `<span class="timestamp">[${timestamp}]</span><span class="prefix">${prefix}::</span>${message}`;
    
    consoleBox.appendChild(line);
    consoleBox.scrollTop = consoleBox.scrollHeight;
    
    const lines = consoleBox.getElementsByClassName('line');
    for (let l of lines) l.classList.remove('active');
    line.classList.add('active');
}

function updateActionList(logs) {
    const actionBox = document.getElementById('action-list');
    actionBox.innerHTML = '';
    
    let foundThreats = 0;

    logs.forEach(log => {
        const level = log.level || log.status;
        if (level === 'DANGER' || level === 'WARNING') {
            const translation = (threatMap[log.module] && threatMap[log.module][level]) 
                ? threatMap[log.module][level] 
                : { title: `${log.module} Advisory`, desc: log.message };

            const item = document.createElement('div');
            item.className = `action-item ${level === 'WARNING' ? 'warn' : ''}`;
            item.innerHTML = `<span class="title">${translation.title}</span><span class="desc">${translation.desc}</span>`;
            actionBox.appendChild(item);
            foundThreats++;
        }
    });

    if (foundThreats === 0) {
        actionBox.innerHTML = '<div style="color: var(--success); font-size: 0.8rem; font-weight: bold;">[PASS] No critical threats identified in this sequence.</div>';
    }
}

async function runTest() {
    const targetUrl = document.getElementById('target-url').value;
    const consoleBox = document.getElementById('console');
    const scoreVal = document.getElementById('score-value');
    const statusDisp = document.getElementById('status-display');
    const actionBox = document.getElementById('action-list');
    
    if (!targetUrl) {
        logToConsole("ERROR: Targeting vector undefined.", "error", "SYSTEM");
        return;
    }

    // Reset UI
    consoleBox.innerHTML = '';
    scoreVal.innerText = "--";
    scoreVal.style.color = "var(--accent-color)";
    statusDisp.innerText = "PROBING...";
    statusDisp.style.color = "var(--warning)";
    actionBox.innerHTML = '<div style="color: var(--text-secondary); font-size: 0.8rem; font-style: italic;">Analyzing threats...</div>';

    const isAggressive = document.getElementById('m-aggressive').checked;
    const baseUrl = window.location.origin;

    logToConsole(`Initializing probe sequence for host: ${targetUrl}`, "info", "SYSTEM");
    
    let probeActive = true;
    const livelyMessages = ["Analyzing handshake...", "Probing ciphers...", "Scanning metadata...", "Monitoring heartbeat..."];
    let msgIndex = 0;
    const livelyInterval = setInterval(() => {
        if (!probeActive) return;
        logToConsole(livelyMessages[msgIndex % livelyMessages.length], "info", "PROBE");
        msgIndex++;
    }, 2000);

    try {
        const response = await fetch(`${baseUrl}/test`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: targetUrl, aggressive: isAggressive })
        });

        probeActive = false;
        clearInterval(livelyInterval);

        const result = await response.json();
        
        if (result.error) {
            logToConsole(`SEQ_FAIL: ${result.error}`, "error", "SYSTEM");
            statusDisp.innerText = "FAIL";
            statusDisp.style.color = "var(--danger)";
            return;
        }

        // Process results
        result.logs.forEach(log => {
            logToConsole(log.message, log.level || log.status, log.module);
        });

        updateActionList(result.logs);

        scoreVal.innerText = result.score;
        const scoreInt = parseInt(result.score);
        if (scoreInt < 40) scoreVal.style.color = "var(--danger)";
        else if (scoreInt < 70) scoreVal.style.color = "var(--warning)";
        else scoreVal.style.color = "var(--success)";

        statusDisp.innerText = "200 OK";
        statusDisp.style.color = "var(--success)";
        logToConsole("Probe sequence complete.", "success", "SYSTEM");

    } catch (err) {
        probeActive = false;
        clearInterval(livelyInterval);
        logToConsole(`FATAL: ${err.message}`, "error", "SYSTEM");
        statusDisp.innerText = "OFFLINE";
        statusDisp.style.color = "var(--danger)";
    }
}

async function generateTrap(type) {
    const baseUrl = window.location.origin;
    logToConsole(`Generating decoy: ${type.toUpperCase()}`, "info", "GEN");
    try {
        const response = await fetch(`${baseUrl}/generate-trap`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: type })
        });
        const result = await response.json();
        logToConsole(`DECOY_READY: ${result.filename}`, "success", "GEN");
        logToConsole(`\nCONTENT:\n${result.content}`, "info", "PAYLOAD");
    } catch (err) {
        logToConsole(`GEN_FATAL: ${err.message}`, "error", "GEN");
    }
}
