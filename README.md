# dosnapshotman.py

`dosnapshotman.py` is a Python script designed to automate the management of snapshots for DigitalOcean droplets. It ensures that only the last specified number of snapshots are retained for each droplet and provides options for verbose output and Telegram notifications. The script supports multiple DigitalOcean accounts.

## Features

- **Snapshot Management**: Automatically handles snapshots for your DigitalOcean droplets.
- **Configurable Retention**: Retains a specified number of snapshots per droplet, configurable via `.env`.
- **Multi-Account Support**: Manages snapshots across multiple DigitalOcean accounts.
- **Notifications**: Sends operation statuses via Telegram.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6 or higher
- `doctl` - DigitalOcean’s official command-line tool for managing DigitalOcean products.
- `pip` for installing Python packages.

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/drhdev/dosnapshotman.py.git
   cd dosnapshotman.py
   ```

2. **Install Required Python Libraries**
   ```
   pip install python-dotenv requests
   ```

3. **Set Up Configuration Files**
   - Copy the `.env.example` file to a new file named `.env`:
     ```
     cp .env.example .env
     ```
   - Modify the `.env` file with your actual configuration details. 

## Configuration

The script uses environment variables stored in an `.env` file for configuration to keep sensitive data secure. You must set up this file before running the script:

- **DIGITALOCEAN_API_KEY_1** and **DIGITALOCEAN_API_KEY_2**: Your DigitalOcean personal access tokens.
- **TELEGRAM_TOKEN**: Your Telegram bot token.
- **TELEGRAM_CHAT_ID**: The chat ID where you want the bot to send messages.
- **DROPLET_IDS**: Comma-separated list of droplet IDs to manage.
- **BACKUP_COUNTS**: Comma-separated list corresponding to the number of snapshots to retain for each droplet.

## Usage

Simply run the script using Python:

```
python dosnapshotman.py
```

There are no command-line options for this script; all configurations are handled through the `.env` file.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with your suggested changes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contact

For support or queries, please open an issue on the GitHub repository at [https://github.com/drhdev/dosnapshotman.py](https://github.com/drhdev/dosnapshotman.py).
