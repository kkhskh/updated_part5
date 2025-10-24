/**
 * crackpw.c
 *
 * This cracker uses a brute-force approach to find passwords matching a given hash.
 * It tries passwords of increasing length starting from 1 character up to 8 characters.
 * For each length, it tries all combinations of lowercase letters. The search uses
 * recursive generation of candidate passwords and tests each one by calling hashpw
 * to see if it matches the target hash. When a match is found, it copies the password
 * to the destination buffer and returns the password length.
 */

#include "hashpw.h"  // so that you can call hashpw()
#include <string.h>

static int found = 0;
static unsigned int target_hash = 0;
static char result[256];

void try_combinations(char* current, int pos, int max_len) {
    if (found) return;
    
    if (pos == max_len) {
        current[pos] = '\0';
        unsigned int h = hashpw(current, pos);
        if (h == target_hash) {
            strcpy(result, current);
            found = 1;
        }
        return;
    }
    
    for (char c = 'a'; c <= 'z'; c++) {
        if (found) return;
        current[pos] = c;
        try_combinations(current, pos + 1, max_len);
    }
}

/**
 * Given a hash, tries to generate a cleartext ASCII password that hashes to
 * the same value.
 *
 * If successful, returns the length of the cracked password and stores the
 * cracked password in "dest". If unsuccessful, returns 0.
 */
int crackpw(char dest[256], unsigned int hash) {
    found = 0;
    target_hash = hash;
    char current[256];
    
    for (int len = 1; len <= 8; len++) {
        try_combinations(current, 0, len);
        if (found) {
            strcpy(dest, result);
            dest[strlen(result)] = '\0';
            return strlen(result);
        }
    }
    return 0;
}
