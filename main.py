"""
Cryptography CLI – Practical examples for all lecture topics.
Run: python main.py
"""

import hashlib
import hmac
import math
import os
import random
import string
import struct
import sys
from collections import Counter


# ─────────────────────────── Helpers ───────────────────────────


def heading(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def pause() -> None:
    input("\n⏎  Press Enter to continue...")


def ask(prompt: str, default: str = "") -> str:
    if default:
        result = input(f"{prompt} [{default}]: ").strip()
        return result if result else default
    return input(f"{prompt}: ").strip()


# ─────────────────────────── KR1 ──────────────────────────────


# 1 – Caesar Cipher
def caesar_cipher() -> None:
    heading("Caesar Cipher  (KR1 §3.1)")
    text = ask("Plaintext", "HELLO WORLD")
    shift = int(ask("Shift (n)", "3"))

    encrypt = ""
    for ch in text.upper():
        if ch.isalpha():
            encrypt += chr((ord(ch) - 65 + shift) % 26 + 65)
        else:
            encrypt += ch

    decrypt = ""
    for ch in encrypt:
        if ch.isalpha():
            decrypt += chr((ord(ch) - 65 - shift) % 26 + 65)
        else:
            decrypt += ch

    print(f"  Plaintext : {text.upper()}")
    print(f"  Encrypted : {encrypt}")
    print(f"  Decrypted : {decrypt}")
    print(f"\n  Key space is only 25 → trivially broken by brute force.")


# 2 – Caesar Brute Force
def caesar_brute_force() -> None:
    heading("Caesar Brute Force  (KR1 §3.1)")
    cipher = ask("Ciphertext", "KHOOR ZRUOG")
    print()
    for shift in range(1, 26):
        plain = ""
        for ch in cipher.upper():
            if ch.isalpha():
                plain += chr((ord(ch) - 65 - shift) % 26 + 65)
            else:
                plain += ch
        marker = " ◀" if shift == 3 else ""
        print(f"  Shift {shift:2d}: {plain}{marker}")


# 3 – Vigenère Cipher
def vigenere_cipher() -> None:
    heading("Vigenère Cipher  (KR1 §3.2)")
    text = ask("Plaintext", "ATTACKATDAWN")
    key = ask("Key", "LEMON")
    text = text.upper()
    key = key.upper()

    encrypted = ""
    for i, ch in enumerate(text):
        if ch.isalpha():
            shift = ord(key[i % len(key)]) - 65
            encrypted += chr((ord(ch) - 65 + shift) % 26 + 65)
        else:
            encrypted += ch

    decrypted = ""
    for i, ch in enumerate(encrypted):
        if ch.isalpha():
            shift = ord(key[i % len(key)]) - 65
            decrypted += chr((ord(ch) - 65 - shift) % 26 + 65)
        else:
            decrypted += ch

    print(f"  Plaintext : {text}")
    print(f"  Key       : {''.join(key[i % len(key)] for i in range(len(text)))}")
    print(f"  Encrypted : {encrypted}")
    print(f"  Decrypted : {decrypted}")


# 4 – Frequency Analysis
def frequency_analysis() -> None:
    heading("Frequency Analysis  (KR1 §2)")
    text = ask("Text to analyse", "The quick brown fox jumps over the lazy dog")
    letters = [ch.upper() for ch in text if ch.isalpha()]
    total = len(letters)
    counts = Counter(letters)
    print(f"\n  Total letters: {total}\n")
    for ch, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        bar = "█" * int(cnt / total * 50)
        print(f"  {ch}: {cnt:3d} ({cnt/total*100:5.1f}%)  {bar}")

    print("\n  English expected top-5: E (11.2%), A (8.5%), R (7.6%), I (7.5%), O (7.2%)")


# 5 – One-Time Pad (XOR)
def one_time_pad() -> None:
    heading("One-Time Pad  (KR1 §4.3)")
    text = ask("Plaintext", "HELLO")
    text_bytes = text.encode()
    key = os.urandom(len(text_bytes))

    cipher = bytes(a ^ b for a, b in zip(text_bytes, key))
    decrypted = bytes(a ^ b for a, b in zip(cipher, key))

    print(f"  Plaintext  : {text}")
    print(f"  Key (hex)  : {key.hex()}")
    print(f"  Cipher(hex): {cipher.hex()}")
    print(f"  Decrypted  : {decrypted.decode()}")
    print("\n  Perfect secrecy: key is truly random & as long as the message.")


# 6 – Entropy
def entropy_demo() -> None:
    heading("Entropy & Information Content  (KR1 §4.1)")
    text = ask("Text", "ABRACADABRA")
    counts = Counter(text)
    total = len(text)
    print(f"\n  Symbol frequencies (n={total}):\n")
    h = 0.0
    for sym, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        p = cnt / total
        info = -math.log2(p)
        h += p * info
        print(f"  '{sym}': p={p:.3f}  I={info:.3f} bit")
    print(f"\n  Entropy H(X) = {h:.4f} bit/symbol")
    print(f"  Max entropy for {len(counts)} symbols = {math.log2(len(counts)):.4f} bit/symbol")


# 7 – PRNG (Linear Congruential Generator)
def prng_demo() -> None:
    heading("Pseudo-Random Number Generator  (KR1 §5.2)")
    print("  Simple LCG:  X_{n+1} = (a * X_n + c) mod m")
    seed = int(ask("Seed", "42"))
    a, c, m = 1103515245, 12345, 2**31
    x = seed
    print(f"\n  Parameters: a={a}, c={c}, m=2^31")
    print(f"  First 10 values:\n")
    for i in range(10):
        x = (a * x + c) % m
        print(f"  X_{i+1:2d} = {x:>12d}  (bits: {x >> 16 & 0xFF:08b})")
    print("\n  Note: LCGs are NOT cryptographically secure.")
    print("  A crypto PRNG must be computationally indistinguishable from true random.")


# 8 – ChaCha20 Quarter Round
def chacha20_quarter_round() -> None:
    heading("ChaCha20 Quarter Round  (KR1 §6.1)")

    def rotl32(v: int, n: int) -> int:
        return ((v << n) | (v >> (32 - n))) & 0xFFFFFFFF

    def quarter_round(a: int, b: int, c: int, d: int):
        a = (a + b) & 0xFFFFFFFF; d ^= a; d = rotl32(d, 16)
        c = (c + d) & 0xFFFFFFFF; b ^= c; b = rotl32(b, 12)
        a = (a + b) & 0xFFFFFFFF; d ^= a; d = rotl32(d, 8)
        c = (c + d) & 0xFFFFFFFF; b ^= c; b = rotl32(b, 7)
        return a, b, c, d

    a, b, c, d = 0x11111111, 0x01020304, 0x9B8D6F43, 0x01234567
    print(f"  Before: a=0x{a:08X}  b=0x{b:08X}  c=0x{c:08X}  d=0x{d:08X}")
    a, b, c, d = quarter_round(a, b, c, d)
    print(f"  After:  a=0x{a:08X}  b=0x{b:08X}  c=0x{c:08X}  d=0x{d:08X}")
    print("\n  The quarter round mixes 4 words using ADD, XOR, ROTATE.")
    print("  A full ChaCha20 block = 10 × (4 column + 4 diagonal) quarter rounds.")


# 9 – Block Cipher Modes (ECB vs CBC vs CTR) – simplified demo
def block_cipher_modes() -> None:
    heading("Block Cipher Modes  (KR1 §7)")
    print("  Demonstrating ECB vs CBC vs CTR with a simple XOR 'block cipher'.\n")

    plaintext = ask("Plaintext (multiple of 4 chars)", "AAAA AAAA BBBB CCCC")
    key_byte = 0x5A  # simple XOR key for demonstration

    # Pad to multiple of 4
    while len(plaintext) % 4 != 0:
        plaintext += " "
    blocks = [plaintext[i:i+4] for i in range(0, len(plaintext), 4)]

    # ECB
    ecb_enc = []
    for block in blocks:
        enc = bytes(b ^ key_byte for b in block.encode())
        ecb_enc.append(enc.hex())
    print(f"  ECB: {ecb_enc}")
    print("  → Identical plaintext blocks produce identical ciphertext blocks!\n")

    # CBC
    iv = os.urandom(4)
    cbc_enc = []
    prev = iv
    for block in blocks:
        xored = bytes(a ^ b for a, b in zip(block.encode(), prev))
        enc = bytes(b ^ key_byte for b in xored)
        cbc_enc.append(enc.hex())
        prev = enc
    print(f"  CBC (IV={iv.hex()}): {cbc_enc}")
    print("  → Identical blocks now produce different ciphertext.\n")

    # CTR
    nonce = os.urandom(2)
    ctr_enc = []
    for i, block in enumerate(blocks):
        counter_block = nonce + struct.pack(">H", i)
        keystream = bytes(b ^ key_byte for b in counter_block)
        enc = bytes(a ^ b for a, b in zip(block.encode(), keystream))
        ctr_enc.append(enc.hex())
    print(f"  CTR (nonce={nonce.hex()}): {ctr_enc}")
    print("  → Parallelisable, no padding needed.")


# 10 – Feistel Network (DES structure)
def feistel_network() -> None:
    heading("Feistel Network  (KR1 §9.1 – DES Structure)")
    print("  Simplified 4-round Feistel network (8-bit blocks).\n")

    def f(r: int, k: int) -> int:
        return (r * k + 0x3C) & 0xFF

    plaintext = int(ask("Plaintext byte (0-255)", "171"))
    keys = [0x1A, 0x2B, 0x3C, 0x4D]

    l, r = (plaintext >> 4) & 0xF, plaintext & 0xF
    print(f"  Input:  L={l:04b}  R={r:04b}")
    for i in range(4):
        new_l = r
        new_r = l ^ (f(r, keys[i]) & 0xF)
        print(f"  Round {i+1}: L={new_l:04b}  R={new_r:04b}  (key=0x{keys[i]:02X})")
        l, r = new_l, new_r

    cipher = (l << 4) | r
    print(f"\n  Ciphertext: {cipher} (0x{cipher:02X})")

    # Decrypt (reverse key order)
    l, r = (cipher >> 4) & 0xF, cipher & 0xF
    for i in range(3, -1, -1):
        new_r = l
        new_l = r ^ (f(l, keys[i]) & 0xF)
        l, r = new_l, new_r
    decrypted = (l << 4) | r
    print(f"  Decrypted:  {decrypted} (0x{decrypted:02X})")


# 11 – GF(2^8) Arithmetic (AES S-Box math)
def gf28_arithmetic() -> None:
    heading("GF(2⁸) Arithmetic – AES S-Box  (KR1 §9.2)")
    print("  AES operates in GF(2⁸) with irreducible polynomial:")
    print("  m(x) = x⁸ + x⁴ + x³ + x + 1  (0x11B)\n")
    MOD = 0x11B

    def gf_mul(a: int, b: int) -> int:
        result = 0
        for _ in range(8):
            if b & 1:
                result ^= a
            hi = a & 0x80
            a = (a << 1) & 0xFF
            if hi:
                a ^= MOD & 0xFF
            b >>= 1
        return result

    def gf_inv(a: int) -> int:
        if a == 0:
            return 0
        # Using Fermat's little theorem: a^(254) = a^(-1) in GF(2^8)
        r = a
        for _ in range(6):
            r = gf_mul(r, r)
            r = gf_mul(r, a)
        r = gf_mul(r, r)
        return r

    a = int(ask("First byte (hex, e.g. 57)", "57"), 16)
    b = int(ask("Second byte (hex, e.g. 83)", "83"), 16)

    product = gf_mul(a, b)
    inv_a = gf_inv(a)

    print(f"\n  0x{a:02X} × 0x{b:02X} = 0x{product:02X}  (in GF(2⁸))")
    print(f"  0x{a:02X}⁻¹     = 0x{inv_a:02X}")
    print(f"  Verify: 0x{a:02X} × 0x{inv_a:02X} = 0x{gf_mul(a, inv_a):02X}  (should be 0x01)")

    # S-Box affine transform
    def sbox(byte: int) -> int:
        b = gf_inv(byte)
        # Affine transformation
        result = 0
        for i in range(8):
            bit = 0
            for j in range(8):
                bit ^= (b >> ((i + j) % 8)) & 1
            bit ^= (0x63 >> i) & 1
            result |= (bit & 1) << i
        return result

    s = sbox(a)
    print(f"\n  AES S-Box(0x{a:02X}) = 0x{s:02X}")


# 12 – Lamport One-Time Signature
def lamport_signature() -> None:
    heading("Lamport One-Time Signature  (KR1 §10.1)")
    msg = ask("Message to sign", "Hi")
    msg_hash = hashlib.sha256(msg.encode()).digest()
    bits = ''.join(f'{b:08b}' for b in msg_hash)
    num_bits = 16  # Demo with first 16 bits only
    bits = bits[:num_bits]

    print(f"  Message hash (first {num_bits} bits): {bits}\n")

    # Key generation
    sk = [
        (os.urandom(16), os.urandom(16))  # (r_i^0, r_i^1)
        for _ in range(num_bits)
    ]
    pk = [
        (hashlib.sha256(pair[0]).digest()[:8], hashlib.sha256(pair[1]).digest()[:8])
        for pair in sk
    ]

    print("  Key generation: 2×16 random values, hashed for public key.")

    # Sign
    signature = [sk[i][int(bits[i])] for i in range(num_bits)]
    print(f"  Signature: {num_bits} revealed secret values.\n")

    # Verify
    valid = True
    for i in range(num_bits):
        expected = pk[i][int(bits[i])]
        actual = hashlib.sha256(signature[i]).digest()[:8]
        if expected != actual:
            valid = False
            break
    print(f"  Verification: {'✓ VALID' if valid else '✗ INVALID'}")
    print("  ⚠ Each key pair must only be used ONCE!")


# ─────────────────────────── KR2 ──────────────────────────────


# 13 – HMAC
def hmac_demo() -> None:
    heading("HMAC  (KR2 – Hash-MAC)")
    msg = ask("Message", "Hello, World!")
    key = ask("Key", "supersecretkey")

    tag = hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()
    print(f"\n  HMAC-SHA256({msg!r}, key={key!r}):")
    print(f"  {tag}")

    # Verify
    tampered = msg + "!"
    tag2 = hmac.new(key.encode(), tampered.encode(), hashlib.sha256).hexdigest()
    print(f"\n  Tampered message {tampered!r}:")
    print(f"  {tag2}")
    print(f"  Tags match: {tag == tag2}  → tampering detected!")


# 14 – Diffie-Hellman Key Exchange
def diffie_hellman() -> None:
    heading("Diffie-Hellman Key Exchange  (KR2)")
    print("  Public parameters:")
    # Small prime for demo
    p = 23
    g = 5
    print(f"  p = {p}, g = {g}\n")

    a = random.randint(2, p - 2)  # Alice's secret
    b = random.randint(2, p - 2)  # Bob's secret

    A = pow(g, a, p)  # Alice sends
    B = pow(g, b, p)  # Bob sends

    K_alice = pow(B, a, p)
    K_bob = pow(A, b, p)

    print(f"  Alice: secret a={a}, sends A = g^a mod p = {A}")
    print(f"  Bob:   secret b={b}, sends B = g^b mod p = {B}")
    print(f"\n  Alice computes: B^a mod p = {K_alice}")
    print(f"  Bob   computes: A^b mod p = {K_bob}")
    print(f"  Shared secret:  {K_alice}  (match: {K_alice == K_bob})")

    print("\n  --- Now with larger numbers (2048-bit safe prime) ---\n")
    # Use a known safe prime (RFC 3526 Group 14, first few digits for display)
    p_big = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
    g_big = 2
    a_big = random.randint(2, p_big - 2)
    b_big = random.randint(2, p_big - 2)
    A_big = pow(g_big, a_big, p_big)
    B_big = pow(g_big, b_big, p_big)
    K_a = pow(B_big, a_big, p_big)
    K_b = pow(A_big, b_big, p_big)
    print(f"  Shared secret (first 32 hex chars): {K_a:0512x}"[:42] + "...")
    print(f"  Keys match: {K_a == K_b}")


# 15 – RSA
def rsa_demo() -> None:
    heading("RSA Encryption  (KR2)")

    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def mod_inverse(e: int, phi: int) -> int:
        g, x, _ = extended_gcd(e, phi)
        if g != 1:
            raise ValueError("No inverse")
        return x % phi

    def extended_gcd(a: int, b: int):
        if a == 0:
            return b, 0, 1
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

    p, q = 61, 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = mod_inverse(e, phi)

    print(f"  Key generation:")
    print(f"  p={p}, q={q}, n=p×q={n}")
    print(f"  φ(n)=(p-1)(q-1)={phi}")
    print(f"  e={e}  (public exponent, gcd(e,φ)={gcd(e, phi)})")
    print(f"  d={d}  (private exponent, e⁻¹ mod φ)")
    print(f"\n  Public key:  (n={n}, e={e})")
    print(f"  Private key: (n={n}, d={d})")

    m = int(ask("\n  Message (number < n)", "42"))
    c = pow(m, e, n)
    decrypted = pow(c, d, n)
    print(f"\n  Encrypt: {m}^{e} mod {n} = {c}")
    print(f"  Decrypt: {c}^{d} mod {n} = {decrypted}")

    # Textbook RSA weakness
    print("\n  ⚠ Textbook RSA is deterministic → NOT IND-CPA secure!")
    print("  In practice, use RSA-OAEP (PKCS#1 v2.x) for padding.")


# 16 – ElGamal
def elgamal_demo() -> None:
    heading("ElGamal Encryption  (KR2)")
    p = 467
    g = 2
    x = random.randint(2, p - 2)  # private key
    h = pow(g, x, p)  # public key

    print(f"  Public:  p={p}, g={g}, h=g^x mod p={h}")
    print(f"  Private: x={x}\n")

    m = int(ask("Message (number < p)", "42"))
    r = random.randint(2, p - 2)
    c1 = pow(g, r, p)
    c2 = (m * pow(h, r, p)) % p

    print(f"\n  Encrypt (r={r}):")
    print(f"  c1 = g^r mod p = {c1}")
    print(f"  c2 = m · h^r mod p = {c2}")

    # Decrypt
    s = pow(c1, x, p)
    s_inv = pow(s, p - 2, p)  # Fermat's little theorem
    decrypted = (c2 * s_inv) % p
    print(f"\n  Decrypt: c2 · (c1^x)⁻¹ mod p = {decrypted}")
    print(f"  Ciphertext is 2× message size (c1, c2).")


# 17 – Elliptic Curve Point Addition
def elliptic_curve_demo() -> None:
    heading("Elliptic Curve Arithmetic  (KR2)")
    print("  Curve: y² = x³ + ax + b  over F_p\n")

    # Small curve for demo: y² = x³ + 2x + 3 mod 97
    a, b, p = 2, 3, 97
    print(f"  a={a}, b={b}, p={p}")
    print(f"  4a³+27b²={4*a**3 + 27*b**2} (≠0 ✓)\n")

    def ec_add(P, Q, a, p):
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and y1 != y2:
            return None  # Point at infinity
        if P == Q:
            lam = (3 * x1 * x1 + a) * pow(2 * y1, p - 2, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, p - 2, p) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    def ec_mul(k, P, a, p):
        result = None
        addend = P
        while k:
            if k & 1:
                result = ec_add(result, addend, a, p)
            addend = ec_add(addend, addend, a, p)
            k >>= 1
        return result

    # Find a point on the curve
    G = None
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        for y in range(p):
            if (y * y) % p == rhs:
                G = (x, y)
                break
        if G:
            break

    print(f"  Generator G = {G}")
    P2 = ec_add(G, G, a, p)
    print(f"  2G = G + G = {P2}")
    P3 = ec_add(P2, G, a, p)
    print(f"  3G = 2G + G = {P3}")

    k = 7
    Pk = ec_mul(k, G, a, p)
    print(f"  {k}G = {Pk}")

    print("\n  ECDLP: Given G and kG, finding k is computationally hard.")
    print("  ECC-256 ≈ RSA-3072 security with much smaller keys.")


# ─────────────────────────── KR3 ──────────────────────────────


# 18 – RSA Digital Signature
def rsa_signature_demo() -> None:
    heading("RSA Digital Signature  (KR3 §2)")

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

    p, q = 61, 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = extended_gcd(e, phi)[1] % phi

    msg = ask("Message", "Hello Bob")
    h = int.from_bytes(hashlib.sha256(msg.encode()).digest()[:4], "big") % n

    sig = pow(h, d, n)
    verified = pow(sig, e, n)

    print(f"\n  Hash(msg) mod n = {h}")
    print(f"  Signature s = hash^d mod n = {sig}")
    print(f"  Verify: s^e mod n = {verified}")
    print(f"  Valid: {verified == h}")

    # Existential forgery demo
    print("\n  --- Existential Forgery Attack (Textbook RSA) ---")
    fake_sig = random.randint(2, n - 1)
    fake_msg = pow(fake_sig, e, n)
    print(f"  Attacker picks random s = {fake_sig}")
    print(f"  Computes 'message' = s^e mod n = {fake_msg}")
    print(f"  Verification: {fake_sig}^{e} mod {n} = {fake_msg} ✓")
    print("  ⚠ Valid signature for a meaningless message! Use RSA-PSS instead.")


# 19 – ECDSA (simplified)
def ecdsa_demo() -> None:
    heading("ECDSA – Elliptic Curve Digital Signature  (KR3 §4)")
    print("  Simplified demo over a small curve.\n")

    # Curve y² = x³ + 7 mod 67 (simplified)
    a_coeff, b_coeff, p = 0, 7, 67

    def ec_add(P, Q):
        if P is None: return Q
        if Q is None: return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and y1 != y2:
            return None
        if P == Q:
            lam = (3 * x1 * x1 + a_coeff) * pow(2 * y1, p - 2, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, p - 2, p) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    def ec_mul(k, P):
        result = None
        addend = P
        while k:
            if k & 1:
                result = ec_add(result, addend)
            addend = ec_add(addend, addend)
            k >>= 1
        return result

    # Find generator and order
    G = (2, 19)  # point on y²=x³+7 mod 67: 19²=361≡26, 2³+7=15≡15... let me find a valid one
    # Find a valid point
    for x in range(p):
        rhs = (x**3 + a_coeff * x + b_coeff) % p
        for y in range(p):
            if (y * y) % p == rhs:
                G = (x, y)
                break
        if G:
            break

    # Find order of G
    n_order = 1
    Q = G
    while Q is not None:
        Q = ec_add(Q, G)
        n_order += 1
        if n_order > p + 10:
            break

    print(f"  Curve: y² = x³ + {b_coeff} mod {p}")
    print(f"  G = {G}, order n = {n_order}")

    # Key gen
    d_a = random.randint(1, n_order - 1)
    Q_a = ec_mul(d_a, G)
    print(f"  Private key d = {d_a}")
    print(f"  Public key Q = d·G = {Q_a}")

    # Sign
    msg = ask("\n  Message", "Sign me!")
    z = int.from_bytes(hashlib.sha256(msg.encode()).digest()[:2], "big") % n_order
    k = random.randint(1, n_order - 1)
    R = ec_mul(k, G)
    if R is None:
        print("  Unlucky k, try again.")
        return
    r = R[0] % n_order
    if r == 0:
        print("  Unlucky r=0, try again.")
        return
    s = (pow(k, n_order - 2, n_order) * (z + r * d_a)) % n_order
    print(f"\n  z = SHA256(msg) mod n = {z}")
    print(f"  Signature: (r={r}, s={s})")

    # Verify
    s_inv = pow(s, n_order - 2, n_order)
    u1 = (z * s_inv) % n_order
    u2 = (r * s_inv) % n_order
    P_verify = ec_add(ec_mul(u1, G), ec_mul(u2, Q_a))
    if P_verify is not None:
        print(f"  Verify: u1·G + u2·Q = {P_verify}")
        print(f"  r ≡ x₁ mod n? {r} == {P_verify[0] % n_order}: {r == P_verify[0] % n_order}")


# 20 – Certificate Chain Visualization
def certificate_demo() -> None:
    heading("X.509 Certificate Chain  (KR3 §5)")
    print("  A simplified visualization of a certificate chain of trust.\n")

    print("  ┌─────────────────────────────────────┐")
    print("  │  Root CA (self-signed)               │")
    print("  │  Subject: TrustRoot Global CA        │")
    print("  │  Issuer:  TrustRoot Global CA        │")
    print("  │  Public Key: RSA 4096-bit            │")
    print("  │  Validity: 2020-01-01 – 2040-12-31   │")
    print("  │  Signature: self-signed              │")
    print("  └──────────────┬──────────────────────┘")
    print("                 │ signs")
    print("  ┌──────────────▼──────────────────────┐")
    print("  │  Intermediate CA                     │")
    print("  │  Subject: TrustRoot Intermediate     │")
    print("  │  Issuer:  TrustRoot Global CA        │")
    print("  │  Public Key: RSA 2048-bit            │")
    print("  │  Validity: 2023-01-01 – 2030-12-31   │")
    print("  │  Signature: by Root CA               │")
    print("  └──────────────┬──────────────────────┘")
    print("                 │ signs")
    print("  ┌──────────────▼──────────────────────┐")
    print("  │  End-Entity Certificate              │")
    print("  │  Subject: www.example.com            │")
    print("  │  Issuer:  TrustRoot Intermediate     │")
    print("  │  Public Key: ECDSA P-256             │")
    print("  │  Validity: 2025-01-01 – 2026-01-01   │")
    print("  │  Signature: by Intermediate CA       │")
    print("  └─────────────────────────────────────┘")
    print()
    print("  Revocation checking:")
    print("  • CRL  – Certificate Revocation List (periodic download)")
    print("  • OCSP – Online Certificate Status Protocol (on-demand)")


# 21 – TLS 1.3 Handshake Visualization
def tls_handshake_demo() -> None:
    heading("TLS 1.3 Handshake  (KR3 §8)")
    print("  Simplified TLS 1.3 full handshake (1-RTT):\n")
    print("  Client                                Server")
    print("  ──────                                ──────")
    print("  ClientHello")
    print("    • supported_versions: TLS 1.3")
    print("    • cipher_suites: [AES-256-GCM-SHA384,")
    print("                      CHACHA20-POLY1305-SHA256]")
    print("    • key_share: x25519 public key  ──────►")
    print()
    print("                              ◄──────  ServerHello")
    print("                                        • selected cipher suite")
    print("                                        • key_share: x25519 public")
    print("                              ◄──────  {EncryptedExtensions}")
    print("                              ◄──────  {Certificate}")
    print("                              ◄──────  {CertificateVerify}")
    print("                              ◄──────  {Finished}")
    print()
    print("  {Finished}  ──────────────────────►")
    print()
    print("  [Application Data]  ◄═══════════►  [Application Data]")
    print()
    print("  Cipher suites in TLS 1.3:")
    print("  • TLS_AES_128_GCM_SHA256")
    print("  • TLS_AES_256_GCM_SHA384")
    print("  • TLS_CHACHA20_POLY1305_SHA256")
    print("  • TLS_AES_128_CCM_SHA256")
    print()
    print("  Key exchange: (EC)DHE or PSK with (EC)DHE")
    print("  → Perfect Forward Secrecy (PFS) guaranteed")


# 22 – BB84 Quantum Key Distribution
def bb84_demo() -> None:
    heading("BB84 Quantum Key Distribution  (KR3 §12)")
    n = 16
    print(f"  Simulating BB84 with {n} qubits.\n")

    bases = ["+", "×"]  # rectilinear, diagonal
    bits_0 = {"+" : "↕", "×": "⤢"}
    bits_1 = {"+" : "↔", "×": "⤡"}

    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(bases) for _ in range(n)]
    bob_bases = [random.choice(bases) for _ in range(n)]

    # Bob's measurement
    bob_bits = []
    for i in range(n):
        if bob_bases[i] == alice_bases[i]:
            bob_bits.append(alice_bits[i])  # correct measurement
        else:
            bob_bits.append(random.randint(0, 1))  # random result

    print("  Alice bits:  ", " ".join(str(b) for b in alice_bits))
    print("  Alice bases: ", " ".join(b for b in alice_bases))
    print("  Bob bases:   ", " ".join(b for b in bob_bases))
    print("  Bob bits:    ", " ".join(str(b) for b in bob_bits))
    print()

    # Sifting
    match = [alice_bases[i] == bob_bases[i] for i in range(n)]
    print("  Basis match: ", " ".join("✓" if m else "✗" for m in match))

    sifted = [alice_bits[i] for i in range(n) if match[i]]
    print(f"\n  Sifted key ({len(sifted)} bits): {''.join(str(b) for b in sifted)}")

    # Eve simulation
    print("\n  --- With Eavesdropper (Eve) ---")
    eve_bases = [random.choice(bases) for _ in range(n)]
    eve_bits = []
    forwarded = []
    for i in range(n):
        if eve_bases[i] == alice_bases[i]:
            eve_bits.append(alice_bits[i])
            forwarded.append(alice_bits[i])
        else:
            measured = random.randint(0, 1)
            eve_bits.append(measured)
            forwarded.append(measured)

    bob_bits_eve = []
    for i in range(n):
        if bob_bases[i] == eve_bases[i]:
            bob_bits_eve.append(forwarded[i])
        else:
            bob_bits_eve.append(random.randint(0, 1))

    errors = sum(
        1 for i in range(n)
        if match[i] and alice_bits[i] != bob_bits_eve[i]
    )
    matched_count = sum(match)
    error_rate = errors / matched_count * 100 if matched_count else 0
    print(f"  Error rate in sifted key: {errors}/{matched_count} = {error_rate:.0f}%")
    print(f"  Expected ~25% error rate when Eve intercepts → Eve detected!")
    print("\n  Security relies on No-Cloning Theorem: quantum states cannot be copied.")


# 23 – Encrypt-then-MAC vs alternatives
def encrypt_then_mac_demo() -> None:
    heading("Encrypt-then-MAC vs MAC-then-Encrypt  (KR2)")
    msg = ask("Message", "Secret data").encode()
    k1 = os.urandom(16)  # encryption key
    k2 = os.urandom(16)  # MAC key

    # Simple XOR "encryption" for demo
    keystream = (k1 * (len(msg) // len(k1) + 1))[:len(msg)]
    ciphertext = bytes(a ^ b for a, b in zip(msg, keystream))

    # Encrypt-then-MAC (recommended)
    tag_etm = hmac.new(k2, ciphertext, hashlib.sha256).hexdigest()[:16]
    print(f"  Encrypt-then-MAC (✓ recommended):")
    print(f"    Ciphertext: {ciphertext.hex()}")
    print(f"    MAC(ciphertext): {tag_etm}")
    print(f"    → Tampering detected BEFORE decryption\n")

    # MAC-then-Encrypt
    tag_mte = hmac.new(k2, msg, hashlib.sha256).digest()[:8]
    combined = msg + tag_mte
    keystream2 = (k1 * (len(combined) // len(k1) + 1))[:len(combined)]
    ct_mte = bytes(a ^ b for a, b in zip(combined, keystream2))
    print(f"  MAC-then-Encrypt (⚠ problematic):")
    print(f"    Ciphertext: {ct_mte.hex()}")
    print(f"    → Must decrypt first to check MAC → padding oracle risk\n")

    print("  TLS 1.3 uses AEAD (e.g., AES-GCM, ChaCha20-Poly1305)")
    print("  which combines encryption + authentication in one step.")


# 24 – Quantum Impact on Crypto
def quantum_impact() -> None:
    heading("Quantum Computing Impact  (KR3 §13)")
    print("  Shor's Algorithm – breaks public-key crypto:\n")
    data = [
        ("RSA-3072", "128 bit", "BROKEN"),
        ("DH-3072", "128 bit", "BROKEN"),
        ("ECDH-256", "128 bit", "BROKEN"),
        ("ECDSA-256", "128 bit", "BROKEN"),
    ]
    print(f"  {'Algorithm':<15} {'Classical':<15} {'Post-Quantum'}")
    print(f"  {'─'*15} {'─'*15} {'─'*15}")
    for alg, classical, pq in data:
        print(f"  {alg:<15} {classical:<15} {pq}")

    print("\n  Grover's Algorithm – halves symmetric key strength:\n")
    data2 = [
        ("AES-128", "128 bit", "64 bit ✗"),
        ("AES-256", "256 bit", "128 bit ✓"),
        ("SHA-256", "256 bit", "128 bit ✓"),
    ]
    print(f"  {'Algorithm':<15} {'Classical':<15} {'Post-Grover'}")
    print(f"  {'─'*15} {'─'*15} {'─'*15}")
    for alg, classical, pq in data2:
        print(f"  {alg:<15} {classical:<15} {pq}")

    print("\n  → Use AES-256 and prepare for Post-Quantum Cryptography (PQC)")
    print("  → NIST PQC standards: CRYSTALS-Kyber (KEM), CRYSTALS-Dilithium (signatures)")


# ─────────────────────────── Menu ─────────────────────────────

MENU = [
    ("KR1 – Classical & Symmetric Cryptography", [
        ("1", "Caesar Cipher", caesar_cipher),
        ("2", "Caesar Brute Force", caesar_brute_force),
        ("3", "Vigenère Cipher", vigenere_cipher),
        ("4", "Frequency Analysis", frequency_analysis),
        ("5", "One-Time Pad (XOR)", one_time_pad),
        ("6", "Entropy Calculation", entropy_demo),
        ("7", "PRNG (Linear Congruential)", prng_demo),
        ("8", "ChaCha20 Quarter Round", chacha20_quarter_round),
        ("9", "Block Cipher Modes (ECB/CBC/CTR)", block_cipher_modes),
        ("10", "Feistel Network (DES structure)", feistel_network),
        ("11", "GF(2⁸) Arithmetic (AES S-Box)", gf28_arithmetic),
        ("12", "Lamport One-Time Signature", lamport_signature),
    ]),
    ("KR2 – MACs, Public-Key Crypto & Key Exchange", [
        ("13", "HMAC", hmac_demo),
        ("14", "Encrypt-then-MAC", encrypt_then_mac_demo),
        ("15", "Diffie-Hellman Key Exchange", diffie_hellman),
        ("16", "RSA Encryption", rsa_demo),
        ("17", "ElGamal Encryption", elgamal_demo),
        ("18", "Elliptic Curve Arithmetic", elliptic_curve_demo),
    ]),
    ("KR3 – Signatures, TLS & Quantum", [
        ("19", "RSA Digital Signature", rsa_signature_demo),
        ("20", "ECDSA Signature", ecdsa_demo),
        ("21", "X.509 Certificate Chain", certificate_demo),
        ("22", "TLS 1.3 Handshake", tls_handshake_demo),
        ("23", "BB84 Quantum Key Distribution", bb84_demo),
        ("24", "Quantum Impact on Cryptography", quantum_impact),
    ]),
]


def print_menu() -> None:
    print("\n" + "=" * 60)
    print("  Cryptography – Practical Examples CLI")
    print("=" * 60)
    for section_title, items in MENU:
        print(f"\n  {section_title}")
        print(f"  {'─' * (len(section_title))}")
        for key, label, _ in items:
            print(f"    [{key:>2}] {label}")
    print(f"\n    [ q] Quit")
    print()


def main() -> None:
    lookup = {}
    for _, items in MENU:
        for key, _, func in items:
            lookup[key] = func

    while True:
        print_menu()
        choice = ask("Select an example").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("\nGoodbye!\n")
            break
        if choice in lookup:
            try:
                lookup[choice]()
            except (ValueError, KeyboardInterrupt) as e:
                if isinstance(e, KeyboardInterrupt):
                    print("\n  Cancelled.")
                else:
                    print(f"\n  Error: {e}")
            pause()
        else:
            print("  Invalid choice. Try again.")


if __name__ == "__main__":
    main()
