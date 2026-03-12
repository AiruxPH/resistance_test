# Developer API Reference 🛠️

Extend the Resistance Test engine or integrate it into your own DevOps tools.

## ⚙️ Core Engine: `tester.py`
The engine is a modular Python class that supports multi-threading.

### `ResistanceTester(target_url, aggressive=False)`
- **`target_url`**: The fully qualified host to audit.
- **`aggressive`**: Boolean. If true, increases probe count and decreases wait times.

### `run_all()`
Launches all modules using `ThreadPoolExecutor`.

## 🌐 Web API: `server.py`
Standard JSON endpoints for integration.

### `POST /test`
**Payload:**
```json
{
  "url": "https://target.host",
  "aggressive": true
}
```
**Response:**
```json
{
  "logs": [...],
  "score": "85%"
}
```

### `POST /generate-trap`
**Payload:**
```json
{
  "type": "env|db|txt"
}
```
**Response:**
```json
{
  "content": "PAYLOAD_HERE",
  "filename": ".env.decoy"
}
```
