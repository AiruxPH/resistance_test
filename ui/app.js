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

function logToConsole(message, type = 'info', prefix = 'SCANNER') {
    const consoleBox = document.getElementById('console');
    const line = document.createElement('div');
    line.className = `line ${type}`;
    
    const timestamp = new Date().toLocaleTimeString([], { hour12: false });
    line.innerHTML = `<span class="timestamp">[${timestamp}]</span><span class="prefix">${prefix}::</span>${message}`;
    
    consoleBox.appendChild(line);
    consoleBox.scrollTop = consoleBox.scrollHeight;
    
    // Add "active" pulse to current line
    const lines = consoleBox.getElementsByClassName('line');
    for (let l of lines) l.classList.remove('active');
    line.classList.add('active');
}

async function runTest() {
    const targetUrl = document.getElementById('target-url').value;
    const consoleBox = document.getElementById('console');
    const scoreVal = document.getElementById('score-value');
    const statusDisp = document.getElementById('status-display');
    
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

    const isAggressive = document.getElementById('m-aggressive').checked;
    const baseUrl = window.location.origin;

    logToConsole(`Initializing probe sequence for host: ${targetUrl}`, "info", "SYSTEM");
    if (isAggressive) {
        logToConsole("WARNING: AGGRESSIVE_MODE active. Stability risk detected.", "warning", "SYSTEM");
    }

    // --- Lively Console Logic ---
    let probeActive = true;
    const livelyMessages = [
        "Analyzing network handshake...",
        "Probing TLS cipher suites...",
        "Identifying endpoint architecture...",
        "Scanning for exposed metadata...",
        "Testing rate-limit resilience...",
        "Injecting baseline payloads...",
        "Monitoring server heartbeat...",
        "Verifying database path security..."
    ];

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

        // Output real logs
        result.logs.forEach(log => {
            const level = (log.level || log.status || 'info').toLowerCase();
            logToConsole(log.message, level, log.module);
        });

        // Finalize score
        scoreVal.innerText = result.score;
        const scoreInt = parseInt(result.score);
        if (scoreInt < 40) scoreVal.style.color = "var(--danger)";
        else if (scoreInt < 70) scoreVal.style.color = "var(--warning)";
        else scoreVal.style.color = "var(--success)";

        statusDisp.innerText = "200 OK";
        statusDisp.style.color = "var(--success)";
        logToConsole("Probe sequence complete. Analysis report generated.", "success", "SYSTEM");

    } catch (err) {
        probeActive = false;
        clearInterval(livelyInterval);
        logToConsole(`FATAL: Connection to backend lost. ${err.message}`, "error", "SYSTEM");
        statusDisp.innerText = "OFFLINE";
        statusDisp.style.color = "var(--danger)";
    }
}

async function generateTrap(type) {
    const baseUrl = window.location.origin;
    logToConsole(`Initializing decoy generation: ${type.toUpperCase()}`, "info", "GEN");
    
    try {
        const response = await fetch(`${baseUrl}/generate-trap`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: type })
        });

        const result = await response.json();
        if (result.error) {
            logToConsole(`GEN_ERR: ${result.error}`, "error", "GEN");
        } else {
            logToConsole(`DECOY_READY: Copying payload to log stream...`, "success", "GEN");
            logToConsole(`\nFILE: ${result.filename}\nCONTENT:\n${result.content}`, "info", "PAYLOAD");
        }
    } catch (err) {
        logToConsole(`GEN_FATAL: ${err.message}`, "error", "GEN");
    }
}
