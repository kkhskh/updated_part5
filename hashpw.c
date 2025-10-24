/**
 * hashpw.c
 *
 * I reverse engineered this hash function by disassembling the proton binary and analyzing the calculate_pw_hash function at address 0x08048c1b. The function takes a plaintext string and its length as parameters. I traced through the assembly instructions to understand the algorithm. The function initializes a hash variable to zero and iterates through each character of the input string. For each character, it converts the character to a signed integer, then creates a value by shifting the character left by 8 bits and adding it to itself, effectively multiplying by 257. This value is XORed with the current hash, and then the hash is shifted left by one bit. After processing all characters, if the length is greater than zero, the function ORs the first character of the string with the hash. Finally, the hash is XORed with the constant 0xfeedface before returning. I translated these assembly operations directly into equivalent C code with the same logic flow and arithmetic operations.
 */


unsigned int hashpw(const char* plaintext, int len) {
    unsigned int hash = 0;
    int i;
    
    for (i = 0; i < len; i++) {
        int c = (int)(signed char)plaintext[i];
        int temp = (c << 8) + c;
        hash ^= temp;
        hash <<= 1;
    }
    
    if (len > 0) {
        int first_char = (int)(signed char)plaintext[0];
        hash |= first_char;
    }
    
    hash ^= 0xfeedface;
    
    return hash;
}
