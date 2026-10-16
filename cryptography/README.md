# Task 01: Cryptography - Technical Writeup

## 1. Challenge Overview
* **Category:** Cryptography
* **Challenge Source:** [BYTE MAIT Cybersecurity Recruitment 2026](https://bytesoc.dev/tasks/cybersecurity/)
* **Problem Statement:** *"The challenge is a simple cipher challenge that has the flag in the format BYTE{...}."*
* **Challenge Ciphertext:**
  ```text
  QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9
  ```
* **Required Flag Format:** `BYTE{...}`

---

## 2. Multi-Layer Cryptanalysis

The challenge consists of two distinct cryptographic layers:
1. **Transport Encoding Layer:** Base64
2. **Confidentiality Encryption Layer:** Beaufort Cipher (Polyalphabetic Substitution)

```
[ Raw Input ] ---> ( Base64 Decode ) ---> [ Intermediate Ciphertext ] ---> ( Beaufort Decrypt: 'CYBR' ) ---> [ Flag ]
QkFJTnt...                                 BAIN{bA73_Q8R_...}                                                 BYTE{bY73...}
```

---

### Layer 1: Base64 Encoding Identification & Decoding

#### Reconnaissance & Fingerprinting:
1. **Length:** Exactly 36 characters (divisible by 4, representing 9 four-character blocks).
2. **Alphabet:** Strictly alphanumeric `[A-Za-z0-9]`, matching standard Base64 (RFC 4648).
3. **Absence of delimiters:** Curly braces `{}` and underscores `_` are absent at this stage, indicating the raw flag was encoded after encryption.

Decoding the 36-character string yields:
```text
BAIN{bA73_Q8R_ArhHC_X4yGcD}
```

---

### Layer 2: The Beaufort Cipher & Key Derivation

#### Observations on Intermediate Output:
1. **Preserved Flag Structure:** Braces `{}` at index 4 and end, and word separators `_` are preserved.
2. **Preserved Leetspeak Digits:** Numbers `7, 3, 8, 4` are passed through untouched.
3. **Prefix Mismatch:** The text begins with `BAIN{...}`, but the target format is `BYTE{...}`.

#### Known-Plaintext Attack (KPA):
Because we know the plaintext prefix is `BYTE` and the ciphertext prefix is `BAIN`, we map the letters to $\mathbb{Z}_{26}$ ($A=0, B=1, \dots, Z=25$):

| Character Index | Plaintext ($P$) | $P$ Value | Ciphertext ($C$) | $C$ Value | Sum $(P + C) \pmod{26}$ | Derived Key Letter |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | **B** | 1 | **B** | 1 | $(1 + 1) = 2$ | **C** |
| 1 | **Y** | 24 | **A** | 0 | $(24 + 0) = 24$ | **Y** |
| 2 | **T** | 19 | **I** | 8 | $(19 + 8) = 27 \equiv 1$ | **B** |
| 3 | **E** | 4 | **N** | 13 | $(4 + 13) = 17$ | **R** |

The sum $(P + C) \pmod{26}$ yields a constant 4-letter keyword: **`CYBR`** (thematic for *Cyber*).

This mathematical relationship satisfies the **Beaufort Cipher**:
$$C = (K - P) \pmod{26} \iff P = (K - C) \pmod{26}$$

Because integer addition is commutative ($C + P = P + C$), the Beaufort Cipher is an **involution (reciprocal cipher)**: encryption and decryption share the exact same algorithm.

---

## 3. Letter-by-Letter Decryption Walkthrough

Applying $P = (K - C) \pmod{26}$ with key `CYBR` across the message:

| Cipher Chunk | Key Applied | Decryption Math $\pmod{26}$ | Plaintext Output | Leetspeak Translation |
|---|---|---|---|---|
| `BAIN` | `C Y B R` | B->B, A->Y, I->T, N->E | `BYTE` | Standard flag prefix |
| `bA73` | `C Y` | b->b, A->Y, digits preserved | `bY73` | **byte** (7=t, 3=e) |
| `Q8R` | `B R` | Q->L, R->A, digit preserved | `L8A` | **laa** (Hindi: "bring") |
| `ArhHC` | `C Y B R C` | A->C, r->h, h->u, H->K, C->A | `ChuKA` | **chuka** (Hindi: "already done") |
| `X4yGcD` | `Y B R C Y` | X->B, y->d, G->L, c->a, D->V | `B4dLaV` | **badlav** (Hindi: "change") |

### Final Extracted Flag:
```text
BYTE{bY73_L8A_ChuKA_B4dLaV}
```

> **Cultural Meaning:**  
> In Hinglish, the flag spells **"BYTE laa chuka badlav"** (*"BYTE has already brought change"*). This is a direct punchline to the previous recruitment flag: `BYTE{byte_laaega_badlaav_...}` (*"BYTE will bring change"*).

---

## 4. How to Reproduce & Verify

### Method A: Automated Python Script
Run the automated solver script:
```bash
python solve.py
```

### Method B: CyberChef (Web GUI)
1. Open [CyberChef](https://gchq.github.io/CyberChef/).
2. Paste `QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9` into the **Input** pane.
3. Add **`From Base64`** recipe.
4. Add **`Beaufort Cipher`** recipe with Key: `CYBR`.
5. The flag `BYTE{bY73_L8A_ChuKA_B4dLaV}` will appear in the **Output** pane.
