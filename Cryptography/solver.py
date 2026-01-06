import base64
import binascii
import re

class UniversalDecoder:
    def __init__(self, target):
        self.target = target.strip()
        self.results = []

    def log_result(self, method, decoded):
        try:
            # Only log if it's printable text
            if all(32 <= ord(c) <= 126 or c in "\n\r\t" for c in decoded):
                self.results.append((method, decoded))
        except: pass

    def solve_bases(self):
        """Covers: Base64, Base32, Base16 (Hex), Base85, Ascii85"""
        funcs = [
            ("Base64", base64.b64decode),
            ("Base32", base64.b32decode),
            ("Base16/Hex", lambda x: binascii.unhexlify(re.sub(r'[^0-9a-fA-F]', '', x))),
            ("Base85", base64.b85decode),
            ("Ascii85", base64.a85decode),
        ]
        for name, func in funcs:
            try:
                res = func(self.target).decode('utf-8', errors='ignore')
                self.log_result(name, res)
            except: continue

    def solve_rotations(self):
        """Covers: Caesar, ROT13, and all 26 Alpha Shifts"""
        alpha = "abcdefghijklmnopqrstuvwxyz"
        for shift in range(1, 26):
            decoded = ""
            for char in self.target:
                if char.lower() in alpha:
                    idx = (alpha.index(char.lower()) - shift) % 26
                    new_char = alpha[idx]
                    decoded += new_char.upper() if char.isupper() else new_char
                else:
                    decoded += char
            self.log_result(f"ROT-{shift}", decoded)

