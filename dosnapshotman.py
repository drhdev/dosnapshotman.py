#!/usr/bin/env python3

"""
Script Name: dosnapshotman.py
Version: 0.1
Author: drhdev
License: GNU General Public License v3.0
Description: dosnapshotman.py is a Python script designed to automate the management of snapshots for DigitalOcean droplets.
             It ensures that only the last specified number of snapshots are retained for each droplet and provides options
             for verbose output and Telegram notifications. The script supports multiple DigitalOcean accounts.

GitHub URL: https://github.com/drhdev/dosnapshotman.py

Installation:
1. Ensure that 'doctl', the DigitalOcean command line tool, is installed on your system. You can install it by following the instructions here:
   https://www.digitalocean.com/docs/apis-clis/doctl/how-to/install/

2. Clone the repository:
   git clone https://github.com/drhdev/dosnapshotman.py.git
   cd dosnapshotman.py

3. Install required Python libraries:
   pip install python-dotenv requests

4. Configure the .env file:
   Create a .env file in the same directory as the script and include the necessary API keys and settings as described in the README.

Usage:
Run the script with the following commands:
python dosnapshotman.py
Options:
- No additional command line options are implemented. Configure all settings via the .env file.

Environment Setup:
- Ensure your DigitalOcean API keys and Telegram bot settings are correctly configured in the .env file.
- Adjust the BACKUP_COUNTS in the .env file to specify the number of snapshots to retain per droplet.

Contributing:
Contributions are welcome. Please fork the repository, make your changes, and submit a pull request on GitHub.
"""


import os
import subprocess
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API keys and settings from .env
api_keys = {
    "droplet-id-1": os.getenv("DIGITALOCEAN_API_KEY_1"),
    "droplet-id-2": os.getenv("DIGITALOCEAN_API_KEY_1"),
    "droplet-id-3": os.getenv("DIGITALOCEAN_API_KEY_2"),
    "droplet-id-4": os.getenv("DIGITALOCEAN_API_KEY_2")
}

telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
droplet_ids = os.getenv("DROPLET_IDS").split(',')
backup_counts = list(map(int, os.getenv("BACKUP_COUNTS").split(',')))

# Function to run doctl commands
def run_doctl_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return (False, result.stderr)
    return (True, result.stdout)

# Function to send Telegram messages
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {
        "chat_id": telegram_chat_id,
        "text": message
    }
    requests.post(url, data=data)

# Manage snapshots
def manage_snapshots():
    messages = []
    for droplet_id, backup_count in zip(droplet_ids, backup_counts):
        api_key = api_keys[droplet_id]
        command = f"doctl compute droplet-action snapshot {droplet_id} --access-token {api_key} --format ID,Name"
        success, output = run_doctl_command(command)
        if not success:
            messages.append(f"Failed to take snapshot for droplet {droplet_id}: {output}")
            continue

        # Manage retention
        list_command = f"doctl compute snapshot list --resource-type droplet --format ID --no-header --access-token {api_key}"
        success, output = run_doctl_command(list_command)
        if not success:
            messages.append(f"Error retrieving snapshots for droplet {droplet_id}: {output}")
            continue

        snapshots = output.strip().split('\n')
        if len(snapshots) > backup_count:
            for snapshot in snapshots[backup_count:]:
                del_command = f"doctl compute snapshot delete {snapshot} --force --access-token {api_key}"
                success, output = run_doctl_command(del_command)
                if not success:
                    messages.append(f"Failed to delete snapshot {snapshot} for droplet {droplet_id}: {output}")
                else:
                    messages.append(f"Deleted snapshot {snapshot} for droplet {droplet_id}")

    return messages

# Main function to handle script execution
if __name__ == "__main__":
    message = "\n".join(manage_snapshots())
    print(message)  # Verbose output
    send_telegram_message(message)  # Send via Telegram
