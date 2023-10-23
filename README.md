# CF-DDNS
**CF-DDNS** is a Cloudflare dynamic DNS update script. Whether you're running a personal project from home or managing an SMB infrastructure without a static IP, CF-DDNS helps ensure that your self-hosted services remain accessible. Every 5 minutes, the script checks the server's public IP and updates the corresponding A-record on Cloudflare if any change is detected. Additionally, integrated with Twilio, the tool sends SMS alerts notifying users about IP changes, update failures, and server connectivity status.

## Features:
- **Automatic IP Detection**: Utilizes services like `icanhazip.com` and `api.ipify.org` to fetch the current public IP.
- **Cloudflare Integration**: Seamlessly fetches and updates the DNS record on Cloudflare.
- **Twilio SMS Alerts**: Receive real-time SMS notifications for significant events.
- **Logging**: Maintains a comprehensive log file detailing script activities and changes.

## How to Use:
1. **Setup**:
    - Clone the repository: 
      ```bash
      git clone TEA-AIR-E/CF-DDNS
      ```
    - Navigate to the project directory: 
      ```bash
      cd CF-DDNS
      ```

2. **Configuration**:
    - Create a `.env` file in the project directory.
    - Populate the `.env` file with your Cloudflare and Twilio credentials as follows:
      ```env
      CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
      CLOUDFLARE_ZONE_ID=your_cloudflare_zone_id
      CLOUDFLARE_RECORD_NAME=your_cloudflare_record_name
      TWILIO_ACCOUNT_SID=your_twilio_account_sid
      TWILIO_AUTH_TOKEN=your_twilio_auth_token
      TWILIO_FROM=your_twilio_from_number
      TWILIO_TO=your_twilio_to_number
      ```

3. **Running the Script**:
    - You can run the script using: 
      ```bash
      python main.py
      ```
    - It is recommended to set up a cron job to execute the script every 5 minutes for real-time updates. A sample cron setup might look like:
      ```bash
      */5 * * * * /usr/bin/python3 /path/to/your/script/main.py
      ```

  ## Todo
  - Add requirements.txt
  - Make a bash installer
      - Add cron job installer
      - Add empty .env file
      - Add config script?
