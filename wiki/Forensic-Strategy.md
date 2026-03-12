# Forensic Deception Strategy 🎣

Resistance Test moves beyond passive defense into **Active Deception**.

## 🛡️ The "Digital Tripwire" Concept
A forensic decoy (Honey-token) is a file that looks valuable but contains fake data. 
- **The Bait:** A file named `.env` containing a fake `DB_PASSWORD`.
- **The Trap:** Since no real user or system process needs to touch this file, any access attempt is **100% confirmed malicious**.

## 🚀 How to Deploy the Defense
1. **Generate Bait:** Use the dashboard to generate payload content for `.env`, `SQL Config`, or `Root Keys`.
2. **Plant the Seed:** Create these files in your production root directory.
3. **Monitor:** Use server tools like `Auditd` (Linux) or `File Integrity Monitoring (FIM)` to alert you the second a decoy is opened.

## 📊 Strategic Value
- **Early Warning:** Catch hackers during the "Reconnaissance" phase, before they find real data.
- **Attacker Profiling:** Log the IP and behavior of anyone touching the decoys.
- **Time Wasting:** Force the hacker to spend hours пытаться to use fake credentials.
