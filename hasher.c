// Do NOT change this file!

#include <stdio.h>
#include <string.h>

#include "hashpw.h"


int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s <plaintext>\n", argv[0]);
        return 1;
    }

    const char* plaintext = argv[1];
    unsigned int hashed = hashpw(plaintext, strlen(plaintext));
    printf("The hash of \"%s\" is:\n%08x\n", plaintext, hashed);
    return 0;
}
