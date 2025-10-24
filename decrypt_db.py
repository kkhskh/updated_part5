#!/usr/bin/env python3

from Crypto.Cipher import AES
import binascii

# The AES-128 ECB decryption key I found
key_hex = "3b99c216f1ae2dd69b70f5e800fc9aec"
key = binascii.unhexlify(key_hex)
with open('leaked_app/password.db', 'rb') as f:
    encrypted_data = f.read()

# Create AES cipher in ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# Decrypt the data (AES processes 16-byte blocks)
decrypted_data = cipher.decrypt(encrypted_data)

# Parse the decrypted data - each entry is 16 bytes
# Format appears to be username (null-terminated) + password hash (4 bytes)
entries = []
for i in range(0, len(decrypted_data), 16):
    block = decrypted_data[i:i+16]
    # Try to parse as null-terminated string + hash
    try:
        # Find null terminator
        null_idx = block.find(b'\x00')
        if null_idx > 0:
            username = block[:null_idx].decode('ascii', errors='ignore')
            # Get the 4-byte hash (last 4 bytes of the block)
            hash_bytes = block[12:16]
            hash_hex = binascii.hexlify(hash_bytes).decode('ascii')
            entries.append((username, hash_hex))
            print(f"Username: {username}, Hash: {hash_hex}")
    except:
        pass

with open('decrypted_passwords.txt', 'w') as f:
    for username, hash_hex in entries:
        f.write(f"{username}:{hash_hex}\n")

print(f"\nDecrypted {len(entries)} password entries")
print("Saved to decrypted_passwords.txt")
