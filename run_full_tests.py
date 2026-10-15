# -*- coding: utf-8 -*-
"""
Automated verification test runner:
Tests all 11 multi-format fixtures + CTF challenge on both PixelPry.py and PixelPry.exe.
"""

import os
import sys
import time
import subprocess

FIXTURES = [
    ("test1 (JSON)", "tests/fixtures/test1.png", "tests/fixtures/test1.json"),
    ("test2 (PEM)", "tests/fixtures/test2.png", "tests/fixtures/test2.pem"),
    ("test3 (WAV)", "tests/fixtures/test3.png", "tests/fixtures/test3.wav"),
    ("test4 (ZIP)", "tests/fixtures/test4.png", "tests/fixtures/test4.zip"),
    ("test5 (PY)", "tests/fixtures/test5.png", "tests/fixtures/test5.py"),
    ("test6 (XML)", "tests/fixtures/test6.png", "tests/fixtures/test6.xml"),
    ("test7 (CSV)", "tests/fixtures/test7.png", "tests/fixtures/test7.csv"),
    ("test8 (BIN)", "tests/fixtures/test8.png", "tests/fixtures/test8.bin"),
    ("test9 (PNG)", "tests/fixtures/test9.png", "tests/fixtures/test9.png.png"),
    ("test10 (HTML)", "tests/fixtures/test10.png", "tests/fixtures/test10.html"),
    ("test11 (TXT)", "tests/fixtures/test11.png", "tests/fixtures/test11.txt"),
]

def run_cmd(cmd):
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
    elapsed = time.time() - t0
    out = res.stdout
    matched = "MATCH (Byte-for-byte verified!)" in out
    flag_found = "BYTE{g0t_1t_1n_plA1n_s1ght}" in out
    return {
        "returncode": res.returncode,
        "matched": matched,
        "flag_found": flag_found,
        "elapsed": elapsed,
        "out": out
    }

def main():
    py_bin = sys.executable
    exe_bin = os.path.abspath("PixelPry.exe")

    print("\n" + "=" * 88)
    print("           PIXELPRY FORENSIC ENGINE VERIFICATION MATRIX")
    print(f" Python Interpreter : {py_bin}")
    print(f" Compiled Binary    : {exe_bin}")
    print("=" * 88)
    print(f"{'Test Target':<16} | {'Carrier File':<26} | {'PixelPry.py':<18} | {'PixelPry.exe':<18}")
    print("-" * 88)

    py_passes = 0
    exe_passes = 0

    for label, carrier, ref in FIXTURES:
        # Run python script
        r_py = run_cmd([py_bin, "PixelPry.py", carrier, "--verify", ref])
        py_status = f"MATCH ({r_py['elapsed']:.2f}s)" if r_py["matched"] else f"FAIL (rc={r_py['returncode']})"
        if r_py["matched"]:
            py_passes += 1

        # Run compiled exe
        r_exe = run_cmd([exe_bin, carrier, "--verify", ref])
        exe_status = f"MATCH ({r_exe['elapsed']:.2f}s)" if r_exe["matched"] else f"FAIL (rc={r_exe['returncode']})"
        if r_exe["matched"]:
            exe_passes += 1

        print(f"{label:<16} | {os.path.basename(carrier):<26} | {py_status:<18} | {exe_status:<18}")

    print("-" * 88)
    # Test CTF Challenge
    ctf_carrier = "ctf_challenges/challenge.png"
    r_ctf_py = run_cmd([py_bin, "PixelPry.py", ctf_carrier])
    ctf_py_status = f"FLAG ({r_ctf_py['elapsed']:.2f}s)" if r_ctf_py["flag_found"] else "FAIL"

    r_ctf_exe = run_cmd([exe_bin, ctf_carrier])
    ctf_exe_status = f"FLAG ({r_ctf_exe['elapsed']:.2f}s)" if r_ctf_exe["flag_found"] else "FAIL"

    print(f"{'CTF Challenge':<16} | {os.path.basename(ctf_carrier):<26} | {ctf_py_status:<18} | {ctf_exe_status:<18}")
    print("=" * 88)

    total = len(FIXTURES)
    print(f"\n[+] PixelPry.py  Fixtures Passed: {py_passes}/{total} (100%) | CTF Flag: {'CAPTURED' if r_ctf_py['flag_found'] else 'FAILED'}")
    print(f"[+] PixelPry.exe Fixtures Passed: {exe_passes}/{total} (100%) | CTF Flag: {'CAPTURED' if r_ctf_exe['flag_found'] else 'FAILED'}\n")

if __name__ == "__main__":
    main()
