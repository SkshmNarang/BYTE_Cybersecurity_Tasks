# BYTE MAIT Cybersecurity Recruitment 2026
# Task 01: Cryptography - Automated Solver Script
# Target: Decode Base64 transport layer and decrypt Beaufort cipher layer

import base64
import sys

CHALLENGE_CIPHERTEXT = "QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9"
BEAUFORT_KEY = "CYBR"

def decode_base64_layer(encoded_str: str) -> str:
    """
    Decodes the outer Base64 transport layer.
    """
    try:
        decoded_bytes = base64.b64decode(encoded_str.strip())
        decoded_text = decoded_bytes.decode("utf-8")
        return decoded_text
    except Exception as e:
        print(f"[-] Base64 decoding failed: {e}", file=sys.stderr)
        sys.exit(1)

def decrypt_beaufort(ciphertext: str, key: str) -> str:
    """
    Decrypts ciphertext using the Beaufort cipher over Z_26.
    Formula: P = (K - C) mod 26
    
    Preserves:
      - Character casing (uppercase / lowercase)
      - Non-alphabetical symbols ({ }, _, digits)
    """
    plaintext = []
    key_idx = 0
    key_upper = key.upper()
    key_len = len(key_upper)

    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            c_val = ord(ch.upper()) - ord('A')
            k_val = ord(key_upper[key_idx % key_len]) - ord('A')
            
            # Beaufort formula: (Key - Cipher) mod 26
            p_val = (k_val - c_val) % 26
            plaintext.append(chr(p_val + base))
            
            # Key index advances only on alphabetical characters
            key_idx += 1
        else:
            # Pass through digits, braces, underscores untouched
            plaintext.append(ch)

    return "".join(plaintext)

def solve():
    print("=" * 65)
    print("  BYTE MAIT Cybersecurity Recruitment 2026 - Task 01 Solver")
    print("=" * 65)
    print(f"[*] Raw Challenge Input : {CHALLENGE_CIPHERTEXT}")

    # Step 1: Base64 Decode
    intermediate_text = decode_base64_layer(CHALLENGE_CIPHERTEXT)
    print(f"[+] Stage 1 (Base64)    : {intermediate_text}")

    # Step 2: Beaufort Decrypt
    final_flag = decrypt_beaufort(intermediate_text, BEAUFORT_KEY)
    print(f"[+] Stage 2 (Beaufort)  : {final_flag}")
    print("=" * 65)
    print(f"[SUCCESS] Extracted Flag: {final_flag}")
    print("=" * 65)

    # Sanity Verification
    expected_flag = "BYTE{bY73_L8A_ChuKA_B4dLaV}"
    assert final_flag == expected_flag, f"Flag mismatch: {final_flag} != {expected_flag}"
    return final_flag

if __name__ == "__main__":
    solve()
