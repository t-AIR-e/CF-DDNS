"""
How to use:
1. Create a .env file in the same directory as this file
2. Add the following variables to the .env file:
    CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
    CLOUDFLARE_ZONE_ID=your_cloudflare_zone_id
    CLOUDFLARE_RECORD_NAME=your_cloudflare_record_name
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_FROM=your_twilio_from_number
    TWILIO_TO=your_twilio_to_number
3. Run the script - Set on 5 minute cron job
"""
# Import required modules and libraries
import base64
import datetime
import re
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set Cloudflare API credentials
CLOUDFLARE_API_TOKEN = os.environ['CLOUDFLARE_API_TOKEN']
CLOUDFLARE_ZONE_ID = os.environ['CLOUDFLARE_ZONE_ID']
CLOUDFLARE_RECORD_NAME = os.environ['CLOUDFLARE_RECORD_NAME']
# Set Twilio API credentials
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_FROM = os.environ['TWILIO_FROM']
TWILIO_TO = os.environ['TWILIO_TO']


def log(message):
    with open('log.txt', 'a') as log_file:
        log_file.write(f'{message}\n')
# print current date and time for logging
print(f'Running script... {datetime.datetime.now()}')
log(f'Running script... {datetime.datetime.now()}')

# Define send_alert function - sends SMS alert via Twilio
def send_alert(title, body):
    try:
        # Create Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Send SMS alert
        message = client.messages.create(
            body=f'{title}: {body}',
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        log(f'Sent SMS alert to {TWILIO_TO} with Message Id: {message.sid}')
        print(f'Sent SMS alert to {TWILIO_TO} with Message Id: {message.sid}')
    except Exception as error:
        log(f'An error occurred: {error}')
        print(f'An error occurred: {error}')
        message = None

    return message

def check_ip():
    # Get current public IP
    try:
        response = requests.get('http://ipv4.icanhazip.com')
        response.raise_for_status()
        current_ip = response.text.strip()
        log(f'Public IP: {current_ip}')
        print(f'Public IP: {current_ip}')
    except requests.exceptions.RequestException:
        try:
            response = requests.get('https://api.ipify.org')
            response.raise_for_status()
            current_ip = response.text.strip()
            log(f'Public IP: {current_ip}')
            print(f'Public IP: {current_ip}')
        except requests.exceptions.RequestException as e:
            log(f'Error getting public IP: {e}')
            print(f'Error getting public IP: {e}')
            send_alert('💥 - Public IP check failed', f'Error getting public IP: {e}')
            return

    # Validate public IP
    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', current_ip):
        print(f'Invalid public IP: {current_ip}')
        send_alert('💥 - Public IP check failed', f'Invalid public IP: {current_ip}')
        return

    # Get current DNS record IP
    try:
        response = requests.get(
            f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records?type=A&name={CLOUDFLARE_RECORD_NAME}',
            headers={
                'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
                'Content-Type': 'application/json',
            },
        )
        response.raise_for_status()
        dns_ip = response.json()['result'][0]['content']
        print(f'DNS IP: {dns_ip}')
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f'Error getting DNS record: {e}')
        send_alert('💥 - DNS check failed', f'Error getting DNS record: {e}')
        return
    # Check if IPs match
    if current_ip != dns_ip:
        # Update DNS record
        try:
            record_id = response.json()['result'][0]['id']
            response = requests.put(
                f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{record_id}',
                headers={
                    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
                    'Content-Type': 'application/json',
                },
                json={
                    'type': 'A',
                    'name': CLOUDFLARE_RECORD_NAME,
                    'content': current_ip,
                    'ttl': 300,
                    'proxied': False,
                },
            )
            response.raise_for_status()
            message = f'Updated DNS record to {current_ip}'
            print(message)
            log(message)
            send_alert('✅ - DNS update successful', message)
        except (requests.exceptions.RequestException, KeyError) as e:
            message = f'Error updating DNS record: {e}'
            print(message)
            log(message)
            send_alert('💥 - DNS update failed', message)
# Run check_ip function
if __name__ == '__main__':
    # Call check_ip function
    check_ip()
    log(f'Finished script... {datetime.datetime.now()}')
