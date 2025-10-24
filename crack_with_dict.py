#!/usr/bin/env python3

import subprocess
import sys

# Common short passwords to try first
common_passwords = [
    "password", "test", "admin", "user", "hello", "world",
    "a", "aa", "ab", "abc", "abcd", 
    "pass", "pwd", "key", "secret", "login",
    "qwerty", "letmein", "welcome", "monkey", "dragon"
]

# Generate all 1-4 letter combinations
for length in range(1, 5):
    current = ['a'] * length
    while True:
        common_passwords.append(''.join(current))
        # Increment
        i = length - 1
        while i >= 0:
            if current[i] == 'z':
                current[i] = 'a'
                i -= 1
            else:
                current[i] = chr(ord(current[i]) + 1)
                break
        if i < 0:
            break

# Read decrypted passwords
with open('decrypted_passwords.txt', 'r') as f:
    lines = f.readlines()

cracked = []
print("Trying to crack passwords with dictionary...")

for line in lines[:20]:  # Try first 20
    username, hash_val = line.strip().split(':')
    print(f"Cracking {username} ({hash_val})...")
    
    for pwd in common_passwords:
        result = subprocess.run(['./hasher', pwd], capture_output=True, text=True)
        computed_hash = result.stdout.strip().split('\n')[-1]
        
        if computed_hash == hash_val:
            print(f"  Found: {pwd}")
            cracked.append((username, pwd))
            break
    
    if len(cracked) >= 8:
        break

# Write to CSV
with open('plaintext-passwords-cracker.csv', 'w') as f:
    f.write('username,password\n')
    for username, pwd in cracked:
        f.write(f'{username},{pwd}\n')

print(f"\nCracked {len(cracked)} passwords!")
