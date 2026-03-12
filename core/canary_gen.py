import random
import string
import json

def get_random_string(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def generate_env():
    """Generates a fake .env file content."""
    traps = {
        "DB_HOST": "127.0.0.1",
        "DB_USER": "admin_backup",
        "DB_PASS": get_random_string(20),
        "AWS_ACCESS_KEY_ID": f"AKIA{get_random_string(16).upper()}",
        "AWS_SECRET_ACCESS_KEY": get_random_string(40),
        "STRIPE_SECRET_KEY": f"sk_test_{get_random_string(24)}",
        "CANARY_TOKEN_ID": f"trigger_{get_random_string(8)}"
    }
    content = "# DECOY ENVIRONMENT FILE - USED FOR FORENSIC MONITORING\n"
    content += "# If you are seeing this, it means you have unauthorized access.\n\n"
    for key, value in traps.items():
        content += f"{key}={value}\n"
    return content

def generate_db_config():
    """Generates a fake database config (PHP format)."""
    db_pass = get_random_string(18)
    content = """<?php
/**
 * DECOY DATABASE CONFIGURATION
 * This file is for forensic traps. 
 * Any connection attempt to this host will trigger a high-priority alert.
 */
define('DB_SERVER', 'mysql-internal.backup-vault.net');
define('DB_USERNAME', 'legacy_root');
define('DB_PASSWORD', '{0}');
define('DB_NAME', 'production_backup_2025');

// Log access attempt internally
$ip = $_SERVER['REMOTE_ADDR'];
// error_log("DECOY_ACCESS_DETECTED: " . $ip);
?>""".format(db_pass)
    return content

def generate_passwords_txt():
    """Generates a fake passwords.txt file."""
    content = "vault_master_key: {0}\n".format(get_random_string(32))
    content += "root_ssh_bypass: {0}\n".format(get_random_string(12))
    content += "admin_panel_emergency: {0}\n".format(get_random_string(10))
    return content

if __name__ == "__main__":
    # Test generation
    print("--- ENV TRAP ---")
    print(generate_env())
    print("\n--- DB TRAP ---")
    print(generate_db_config())
