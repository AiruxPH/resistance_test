/**
 * Resistance Test Dashboard Logic
 * Handles UI events and communicates with the Python backend.
 */

document.getElementById('run-btn').addEventListener('click', async () => {
    const targetUrl = document.getElementById('target-url').value;
    const consoleEl = document.getElementById('console');
    const runBtn = document.getElementById('run-btn');

    if (!targetUrl) {
        logToConsole("Error: Target URL is required.", "error");
        return;
    }

    // Reset UI
    consoleEl.innerHTML = "";
    runBtn.disabled = true;
    runBtn.innerText = "TESTING...";
    document.getElementById('score-value').innerText = "--";

    const isAggressive = document.getElementById('m-aggressive').checked;
    
    // Dynamic host detection
    const baseUrl = window.location.origin;

    logToConsole(`Initializing Security Resistance Test via Backend for: ${targetUrl}`, "info");
    if (isAggressive) {
        logToConsole("WARNING: Aggressive Mode Enabled. Safety throttles reduced.", "warning");
    }
    
    try {
        const response = await fetch(`${baseUrl}/test`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                url: targetUrl,
                aggressive: isAggressive
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();
        
        // Display logs from the Python engine
        if (data.logs) {
            data.logs.forEach(log => {
                const statusType = log.status.toLowerCase();
                logToConsole(`${log.module}: ${log.message}`, statusType);
            });
        }

        document.getElementById('score-value').innerText = data.score || "0%";
        logToConsole("Test Sequence Completed.", "success");

    } catch (error) {
        logToConsole(`Backend Error: ${error.message}`, "error");
        logToConsole("Make sure server.py is running on http://127.0.0.1:5000", "warning");
    } finally {
        runBtn.disabled = false;
        runBtn.innerText = "INITIALIZE TEST";
    }
});

async function generateTrap(type) {
    logToConsole(`Generating Forensic Trap: ${type.toUpperCase()}...`, "info");
    
    // Dynamic host detection
    const baseUrl = window.location.origin;
    
    try {
        const response = await fetch(`${baseUrl}/generate-trap`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: type })
        });

        if (!response.ok) throw new Error("Server Error");

        const data = await response.json();
        
        logToConsole(`SUCCESS: Generated ${data.filename}`, "success");
        logToConsole("--- START OF CONTENT ---", "info");
        
        // Log content line by line for readability
        data.content.split('\n').forEach(line => {
            if (line.trim()) logToConsole(line, "warning");
        });
        
        logToConsole("--- END OF CONTENT ---", "info");
        logToConsole(`Place this file as '${data.filename}' in a sensitive directory to catch unauthorized snooper.`, "success");

    } catch (error) {
        logToConsole(`Generation Error: ${error.message}`, "error");
    }
}

function logToConsole(message, type = "") {
    const consoleEl = document.getElementById('console');
    const line = document.createElement('div');
    line.className = `line ${type}`;
    
    const timestamp = new Date().toLocaleTimeString();
    line.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
    
    consoleEl.appendChild(line);
    consoleEl.scrollTop = consoleEl.scrollHeight;
}

async function simulateTestStep(id, message) {
    logToConsole(message, "info");
    return new Promise(resolve => {
        setTimeout(() => {
            const success = Math.random() > 0.2;
            if (success) {
                logToConsole(`Module ${id}: Passed.`, "success");
            } else {
                logToConsole(`Module ${id}: Potential vulnerability detected!`, "warning");
            }
            resolve();
        }, 800);
    });
}
