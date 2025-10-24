/**
 * crackpw.c
 *
 * Strategy:
 * 1) Try a small wordlist (RockYou top 25k) with a few cheap variants.
 * 2) Fall back to brute-forcing lowercase passwords of length 1..4.
 * On a match, copy plaintext into dest, NUL-terminate, and return its length.
 * All data files are read via relative paths (e.g., data/rockyou-25k.txt).
 */

#include "hashpw.h"   // for hashpw()
#include <stdio.h>
#include <string.h>
#include <ctype.h>

static int try_candidate(char dest[256], unsigned int target, const char *s) {
    size_t len = strlen(s);
    if (len == 0 || len >= 256) return 0;
    unsigned int h = hashpw(s, (int)len);
    if (h == target) {
        memcpy(dest, s, len);
        dest[len] = '\0';
        return (int)len;
    }
    return 0;
}

static void capfirst(char *dst, const char *src) {
    size_t n = strlen(src);
    if (n == 0) { dst[0] = '\0'; return; }
    strcpy(dst, src);
    dst[0] = (char)toupper((unsigned char)dst[0]);
}

static int dict_phase(char dest[256], unsigned int target) {
    FILE *f = fopen("data/rockyou-25k.txt", "r");
    if (!f) return 0; // wordlist optional; skip if missing

    char line[256], var[256], with_suf[256];
    while (fgets(line, sizeof(line), f)) {
        // strip newline
        size_t n = strlen(line);
        while (n && (line[n-1] == '\n' || line[n-1] == '\r')) line[--n] = '\0';
        if (!n) continue;

        // as-is
        int got = try_candidate(dest, target, line);
        if (got) { fclose(f); return got; }

        // Capitalized
        capfirst(var, line);
        got = try_candidate(dest, target, var);
        if (got) { fclose(f); return got; }

        // + single digit
        if (n < 255) {
            for (char d = '0'; d <= '9'; ++d) {
                int written = snprintf(with_suf, sizeof(with_suf), "%s%c", line, d);
                if (written > 0 && written < (int)sizeof(with_suf)) {
                    got = try_candidate(dest, target, with_suf);
                    if (got) { fclose(f); return got; }
                }
            }
        }

        // + small year suffix
        for (int y = 2020; y <= 2025; ++y) {
            int written = snprintf(with_suf, sizeof(with_suf), "%s%d", line, y);
            if (written > 0 && written < (int)sizeof(with_suf)) {
                got = try_candidate(dest, target, with_suf);
                if (got) { fclose(f); return got; }
            }
        }
    }
    fclose(f);
    return 0;
}

static int brute_dfs(char dest[256], unsigned int target,
                     char *buf, int pos, int maxlen) {
    if (pos == maxlen) {
        buf[pos] = '\0';
        unsigned int h = hashpw(buf, pos);
        if (h == target) {
            strcpy(dest, buf);
            return pos;
        }
        return 0;
    }
    for (char c = 'a'; c <= 'z'; ++c) {
        buf[pos] = c;
        int got = brute_dfs(dest, target, buf, pos + 1, maxlen);
        if (got) return got;
    }
    return 0;
}

static int brute_phase(char dest[256], unsigned int target) {
    char buf[256];
    for (int len = 1; len <= 4; ++len) {
        int got = brute_dfs(dest, target, buf, 0, len);
        if (got) return got;
    }
    return 0;
}

/**
 * Given a hash, try to generate a cleartext ASCII password that hashes to it.
 * Return the length on success (and write into dest), else 0.
 */
int crackpw(char dest[256], unsigned int hash) {
    // 1) Dictionary (+ tiny variants)
    int got = dict_phase(dest, hash);
    if (got) return got;

    // 2) Tiny brute force (1..4 lowercase)
    got = brute_phase(dest, hash);
    if (got) return got;

    // Not found
    dest[0] = '\0';
    return 0;
}
