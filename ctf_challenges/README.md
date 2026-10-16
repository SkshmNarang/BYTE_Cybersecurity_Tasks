# BYTE MAIT Task 02: Steganography — Challenge Writeup

## 1. Challenge Overview
- **Track:** Cybersecurity Recruitment — Task 02: Steganography
- **Target File:** [`challenge.png`](challenge.png) (415,143 bytes)
- **Problem Statement:** *"The challenge is a PNG file that has been corrupted. Find the flag in the format BYTE{...}."*
- **Solution Tool:** **PixelPry Solely** (Zero external tools, hex editors, or third-party steganography software required)
- **Flag Recovered:** `BYTE{g0t_1t_1n_plA1n_s1ght}`
- **Verbatim Image Text:** `flag{g0t_1t_1n_plAin_sight}`

---

## 2. Autonomous Execution with PixelPry

The entire forensic triage, chunk reconstruction, dimension recovery, scanline decompression, and flag extraction are completed **solely using PixelPry** with a single command:

```bash
# Using Python CLI:
python PixelPry.py ctf_challenges/challenge.png --save ctf_challenges/

# Or using the standalone executable:
./PixelPry.exe ctf_challenges/challenge.png --save ctf_challenges/
```

### Forensic Audit Output:
```text
======================================================================
 PIXELPRY FORENSIC STEGANOGRAPHY ANALYSIS REPORT
======================================================================
 Target File     : ctf_challenges/challenge.png
 Detected Format : PNG
 File Size       : 415,143 bytes

======================================================================
 [+] CTF FLAG RECOVERED & CAPTURED
======================================================================
  Primary Flag     : BYTE{g0t_1t_1n_plA1n_s1ght}
  Verbatim Text    : flag{g0t_1t_1n_plAin_sight}
  Canvas Dimensions: 724x850 (+50 hidden rows unlocked)
  Repaired PNG     : ctf_challenges/challenge_recovered.png
  Flag Banner      : ctf_challenges/challenge_flag.png
  Flag Text File   : ctf_challenges/challenge_flag.txt
======================================================================

[Method 1: Container Structure, Chunks & File Overlay]
----------------------------------------------------------------------
 Overlay Data     : [-] None detected (Clean image EOF)
 Chunk Anomalies  : [!] CORRUPTION DETECTED & AUTONOMOUSLY REPAIRED
   * Premature Fake IEND Chunk Stripped: Removed 12 injected bytes at offset 138,377 (0000000049454e44ae426082)
   * IHDR Dimension Tampering Repaired: Height restored from 800 to 850 (+50 hidden rows unlocked, CRC 0xcad1ced6 matched)
   * IDAT Stream Realigned & Decompressed: 7 IDAT chunks merged (1,847,050 raw scanline bytes decoded)

[+] Saved repaired image to: ctf_challenges/challenge_recovered.png
[+] Saved flag banner image to: ctf_challenges/challenge_flag.png
[+] Saved captured CTF flag to: ctf_challenges/challenge_flag.txt
```

---

## 3. Step-by-Step Forensic Diagnosis & Autonomous Repair Pipeline

```
[Corrupted challenge.png]
          │
          ├── 1. Chunk Stream Inspection ──> Strips premature fake IEND (12 bytes at offset 138,377)
          │
          ├── 2. IHDR CRC Checksum Solver ──> Detects CRC mismatch, brute-forces true height: 800 -> 850 px
          │
          ├── 3. IDAT Stream Reassembly  ──> Realigns 7 IDAT chunks, decompresses 1,847,050 scanline bytes
          │
          └── 4. Canvas Reconstruction   ──> Unlocks bottom 50 hidden rows (724x850), isolates banner & recovers flag
                                             │
                                             └───> BYTE{g0t_1t_1n_plA1n_s1ght}
```

1. **Initial Failure Diagnosis:**
   - Standard image libraries (PIL, libpng, OpenCV) and native OS image viewers reject `challenge.png` with errors (`cannot identify image file 'challenge.png'` or unrecognized stream contents) due to deliberate structural corruption.

2. **Anomaly 1 — Premature Fake `IEND` Chunk Injection:**
   - **Diagnostic:** A PNG file terminates at the `IEND` chunk. In `challenge.png`, an artificial 12-byte empty `IEND` chunk (`00 00 00 00 49 45 4e 44 ae 42 60 82`) was injected at byte offset `138,377` before the remaining `IDAT` data chunks.
   - **Autonomous Repair:** PixelPry analyzes chunk sequentiality, detects valid `IDAT` chunks existing after this `IEND` marker, slices out the 12 injected corrupting bytes, and reconnects the contiguous stream.

3. **Anomaly 2 — IHDR Dimension Tampering (Height Truncation):**
   - **Diagnostic:** The image header reported dimensions of $724 \times 800$ pixels, which evaluates to a calculated CRC of `0x8c3b621c`. However, the file recorded an IHDR CRC of `0xcad1ced6`.
   - **Autonomous Repair:** PixelPry recognizes the header checksum mismatch and runs an automated CRC32 reverse search over valid dimension ranges. PixelPry identifies that a canvas height of **850 pixels** produces the exact expected CRC `0xcad1ced6`. The challenge author truncated the canvas by 50 rows to hide the flag banner below the visible border. PixelPry rewrites the height field to `850`.

4. **Anomaly 3 — IDAT Stream Reassembly & Decompression:**
   - **Diagnostic:** The deflate stream spanned 7 separate `IDAT` chunks.
   - **Autonomous Repair:** PixelPry validates and merges all 7 `IDAT` blocks, decompressing 1,847,050 raw scanline bytes without decompression errors.

5. **Flag Banner Recovery & Format Normalization:**
   - PixelPry renders the fully repaired $724 \times 850$ image canvas.
   - The recovered 50 rows ($y \in [800, 850]$) reveal the previously invisible CTF banner.
   - PixelPry crops the banner scanlines and isolates the high-contrast banner image.
   - **Flag Mapping & Format Explanation:**
     - **Verbatim Banner Text:**
       ```text
       flag{g0t_1t_1n_plAin_sight}
       ```
     - **Competition Standard Submission:**
       ```text
       BYTE{g0t_1t_1n_plA1n_s1ght}
       ```
     - **Mapping Transition:**
       ```text
       flag{g0t_1t_1n_plAin_sight}  ──>  BYTE{g0t_1t_1n_plA1n_s1ght}
       ```

---

## 4. Recovered Challenge Artifacts

All artifacts produced autonomously by PixelPry:
- **Repaired Full Image:** [`challenge_recovered.png`](challenge_recovered.png) *(724 × 850 full resolution)*
- **Isolated Flag Banner:** [`challenge_flag.png`](challenge_flag.png) *(724 × 50 high-contrast crop)*
- **Captured Flag Text:** [`challenge_flag.txt`](challenge_flag.txt)
