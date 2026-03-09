# Cryptography – Practical Examples CLI

Interactive command-line tool with hands-on examples for all topics covered in the **Kryptographie** lectures (KR1–KR3) at HWR Berlin (Prof. Dr. Björn Grohmann).

## Setup

```bash
# Requires uv and Python 3.12+
uv run main.py
```

No external dependencies – everything uses the Python standard library.

## Topics Covered

### KR1 – Classical & Symmetric Cryptography

| # | Example | Concepts |
|---|---------|----------|
| 1 | Caesar Cipher | Monoalphabetic substitution, mod 26 |
| 2 | Caesar Brute Force | Exhaustive key search (25 keys) |
| 3 | Vigenère Cipher | Polyalphabetic substitution |
| 4 | Frequency Analysis | Letter distribution, breaking substitution ciphers |
| 5 | One-Time Pad | XOR encryption, perfect secrecy (Shannon) |
| 6 | Entropy Calculation | Information content, H(X) = −Σ p·log(p) |
| 7 | PRNG | Linear Congruential Generator, crypto vs non-crypto RNG |
| 8 | ChaCha20 Quarter Round | ARX operations (Add, Rotate, XOR) |
| 9 | Block Cipher Modes | ECB vs CBC vs CTR – why ECB leaks patterns |
| 10 | Feistel Network | DES structure, encrypt/decrypt with reversed keys |
| 11 | GF(2⁸) Arithmetic | AES S-Box math, multiplication & inverse in GF(2⁸) |
| 12 | Lamport Signature | One-time signature from one-way functions |

### KR2 – MACs, Public-Key Crypto & Key Exchange

| # | Example | Concepts |
|---|---------|----------|
| 13 | HMAC | Hash-based MAC, tamper detection |
| 14 | Encrypt-then-MAC | EtM vs MtE vs E&M, why EtM is recommended |
| 15 | Diffie-Hellman | Key exchange over insecure channel, DLP |
| 16 | RSA Encryption | Key generation, encrypt/decrypt, textbook RSA weakness |
| 17 | ElGamal Encryption | Probabilistic encryption, ciphertext expansion |
| 18 | Elliptic Curves | Point addition, scalar multiplication, ECDLP |

### KR3 – Signatures, TLS & Quantum

| # | Example | Concepts |
|---|---------|----------|
| 19 | RSA Signature | Sign/verify, existential forgery attack |
| 20 | ECDSA | Elliptic curve signatures, sign & verify |
| 21 | X.509 Certificates | Chain of trust, CRL, OCSP |
| 22 | TLS 1.3 Handshake | Protocol flow, cipher suites, PFS |
| 23 | BB84 QKD | Quantum key distribution, eavesdropper detection |
| 24 | Quantum Impact | Shor's & Grover's algorithms, post-quantum crypto |

## Usage

```
$ uv run main.py

============================================================
  Cryptography – Practical Examples CLI
  Based on lectures KR1–KR3 (Prof. Dr. Grohmann, HWR Berlin)
============================================================

  KR1 – Classical & Symmetric Cryptography
  ─────────────────────────────────────────
    [ 1] Caesar Cipher
    [ 2] Caesar Brute Force
    ...

Select an example: 1
```

Each example is interactive – you can provide custom inputs or use the defaults.

## Project Structure

```
├── main.py          # CLI app with all 24 examples
├── docs/
│   ├── kr1 - zusammenfassung.md
│   ├── kr2 - zusammenfassung.md
│   └── kr3 - zusammenfassung.md
├── pyproject.toml
└── README.md
```
