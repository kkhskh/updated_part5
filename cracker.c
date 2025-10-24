// Do NOT change this file!

// You may want to write a bash script to crack multiple passwords without
// babysitting your computer.

#include <stdio.h>
#include <string.h>

#include "crackpw.h"


int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s <hex_hash_lowercase>\n", argv[0]);
        return 1;
    }

    const char* hex_hash = argv[1];

    if (strlen(hex_hash) != 8) {
        printf("ERROR: the hash must be 4 bytes.\n");
        return 1;
    }

    unsigned int hash = 0;
    for (const char* cptr = hex_hash; *cptr; ++cptr) {
        char c = *cptr;
        hash = hash << 4;
        if (c >= 'A' && c <= 'F') {
            c += ('a' - 'A');
        }

        if (c >= '0' && c <= '9') {
            hash += c - '0';
        } else if (c >= 'a' && c <= 'f') {
            hash += c + 10 - 'a';
        } else {
            printf("ERROR: the hash must be in hex!\n");
            return 1;
        }
    }

    printf("Attempting to crack hash %08x ...\n", hash);

    char cracked[256];
    int cracked_len = crackpw(cracked, hash);

    if (cracked_len <= 0) {
        printf("Cracking unsuccessful :(\n");
        return 1;
    }

    cracked[cracked_len] = 0;
    printf("Success! The cracked password is:\n%s\n", cracked);
    return 0;
}
