# KR3 – Zusammenfassung
**Vorlesung:** Kryptographie & Rechnernetze 3  
**Dozent:** Prof. Dr. Björn Grohmann  
**Datum:** 02.03.2026

---
## 1. Digitale Signaturen
### Grundprinzip

Eine digitale Signatur ermöglicht es, die **Integrität**, **Authentizität** und **Non-Repudiation** (Nicht-Abstreitbarkeit) einer Nachricht zu gewährleisten.

**Ablauf:**

- **Sender:** Nachricht `M` + `PrivateKey` → Secure Signature Algorithm → `Sign`
- **Empfänger:** Verifiziert mit `PublicKey`, berechnet `Sign'` und prüft `Sign == Sign'`

### Formale Algorithmen

|Algorithmus|Funktion|
|---|---|
|`keygen(1^k) → (sk, pk)`|Schlüsselpaar generieren|
|`sign(m, sk) → σ`|Nachricht signieren|
|`verify(σ, m, pk) → d`|Signatur verifizieren|

### Mögliche Angriffsziele (Adversarial Goals)

- **Total Break:** Angreifer Oscar kann Alices privaten Signieralgorithmus vollständig ableiten.
- **Selective Forgery:** Oscar kann eine gültige Signatur für eine von jemand anderem gewählte Nachricht erstellen (mit nicht-vernachlässigbarer Wahrscheinlichkeit).
- **Existential Forgery** _(relevant für Praxis)_: Oscar kann eine gültige Signatur für mindestens eine beliebige Nachricht erstellen.

---

## 2. Beispiel: RSA-Signatur

### Signaturformel

$$s = m^d \pmod{n}$$

- `s` = Signatur
- `m` = zu signierende Nachricht
- `d` = privater Exponent
- `n` = öffentlicher Modulus

### Existential Forgery Attack gegen RSA

Oscar kennt Bobs öffentlichen Schlüssel `k_pub = (n, e)`. Er:

1. Wählt eine beliebige Signatur `s ∈ ℤ_n`
2. Berechnet die „Nachricht": `x ≡ s^e mod n`
3. Präsentiert Alice das Paar `(x, s)`

Alice verifiziert: `s^e ≡ x' mod n` → da `x' = x` → **gültige Signatur!**

> ⚠️ RSA ohne Padding ist anfällig für Existential Forgery!

---

## 3. RSA-PSS (Probabilistic Signature Scheme)

RSA-PSS verhindert die oben genannte Attacke durch gezieltes **Padding** vor der Signatur:

**Prozess:**

1. Nachricht `M` wird gehasht → `mHash`
2. `M' = [8 × 0x00 Bytes | mHash | salt]` wird erneut gehasht → `H`
3. `DB = [PS | 0x01 | salt]`
4. `maskedDB = DB ⊕ MGF(H)` (Mask Generation Function)
5. Encoded Message: `EM = [maskedDB | H | TF]`

---

## 4. ECDSA – Elliptic Curve Digital Signature Algorithm

### Signieren (Alice, Nachricht `m`)

1. `e = HASH(m)` (z.B. SHA-2)
2. `z` = die `L_n` linksten Bits von `e`
3. Wähle zufälliges `k ∈ [1, n-1]`
4. Berechne Kurvenpunkt: `(x₁, y₁) = k × G` _(G = Generator der EC-Gruppe)_
5. `r = x₁ mod n`
6. `s = k⁻¹(z + r·d_A) mod n` _(d_A = geheimer Schlüssel von Alice)_
7. Signatur: `(r, s)`

### Verifizieren (Bob)

1. Überprüfe, dass `Q_A` (Alices öffentlicher Schlüssel) ein gültiger Kurvenpunkt ist
2. Berechne `e = HASH(m)`, `z` = linkste `L_n` Bits
3. `u₁ = zs⁻¹ mod n`, `u₂ = rs⁻¹ mod n`
4. `(x₁, y₁) = u₁ × G + u₂ × Q_A`
5. Signatur gültig wenn `r ≡ x₁ (mod n)`

---

## 5. Zertifikate (Certificates)

### Kernproblem

> _Wie kann Alice sicher sein, dass ein Public Key wirklich zu Bob gehört?_

### Lösung: Certificate Authority (CA)

Eine vertrauenswürdige Instanz (CA) bestätigt die Identität einer Person und signiert deren Public Key mit ihrem eigenen Private Key.

**Inhalt eines Zertifikats (X.509):**

- Name, Organisation, Adresse, Land
- Gültigkeitszeitraum
- Public Key des Inhabers
- Digitale Signatur der CA

### Zertifikatskette (Chain of Trust)

```
Endnutzer-Zertifikat
    ← signiert von CA
        CA-Zertifikat
            ← signiert von Root CA
                Root CA (selbstsigniert, vertrauensanker)
```

### X.509-Struktur (RFC 5280)

```
Certificate ::= SEQUENCE {
    tbsCertificate    TBSCertificate,
    signatureAlgorithm AlgorithmIdentifier,
    signature         BIT STRING
}
```

### Zertifikatswiderruf

**CRL (Certificate Revocation List):** Wird periodisch heruntergeladen.  
**OCSP (Online Certificate Status Protocol):** Status wird bei Bedarf online abgefragt.

**Widerrufsgründe (RFC 5280):** `unspecified`, `keyCompromise`, `cACompromise`, `affiliationChanged`, `superseded`, `cessationOfOperation`, `certificateHold`, `removeFromCRL`, `privilegeWithdrawn`, `aACompromise`

---

## 6. Identity-Based Encryption (IBE)

**Grundidee (Boneh & Franklin, 2001):** Der öffentliche Schlüssel ist die **Identität** (z.B. eine E-Mail-Adresse), kein separater Schlüssel wird benötigt.

### Beteiligte Instanz: PKG (Private Key Generator)

- Kennt den Master-Key `sk_PKG`
- Gibt nach Authentifizierung den privaten Schlüssel `sk_ID_Bob` heraus

### Mathematische Grundlage: Bilineare Abbildung

Eine bilineare Abbildung `ê: G₁ × G₁ → G₂` mit den Eigenschaften:

1. **Bilinear:** `ê(aP, bQ) = ê(P, Q)^ab`
2. **Nicht-degeneriert**
3. **Effizient berechenbar**

### IBE-Algorithmen (Boneh-Franklin)

- **Setup:** Generiert Parameter `(q, G₁, G₂, ê, n, P, P_pub, H₁, H₂)`, Master-Key `s ∈ ℤ_q*`
- **Extract:** `d_ID = s · Q_ID` wobei `Q_ID = H₁(ID)`
- **Encrypt:** `C = ⟨rP, M ⊕ H₂(g_ID^r)⟩` mit `g_ID = ê(Q_ID, P_pub)`
- **Decrypt:** `V ⊕ H₂(ê(d_ID, U)) = M`

Das funktioniert, da: `e(d, U) = e(sQ, rP) = e(Q, sP)^r`

---

## 7. Historisches Beispiel: The Babington Plot (1586)

### Schichtenmodell der Kommunikationssicherheit

Das historische Beispiel mit Maria Stuart und Anthony Babington illustriert ein **dreischichtiges Sicherheitsmodell**:

|Schicht|Beschreibung|Akteure|
|---|---|---|
|**Conspiracy Layer**|Inhalt der geheimen Kommunikation|Maria Stuart ↔ Babington|
|**Carrier Layer**|Übertragungsweg|Gilbert Gifford als Bote|
|**Beer Barrel Layer**|Physisches Medium|Bierfass als Versteck|

### Security der einzelnen Schichten

**Beer Barrel Layer:** Walsingham kompromittierte das physische Medium (fing die Nachrichten ab).

**Carrier Layer:** Gilbert Gifford arbeitete als Doppelagent für Walsingham.

**Conspiracy Layer:**

- **Verschlüsselung:** Substitutionschiffre (angreifbar durch Frequenzanalyse)
- **Authenticated Encryption:** AES-CTR-Mode + GMAC
- **Schlüsselaustausch:** Diffie-Hellman (`a^x mod p` ↔ `a^y mod p`)
- **Problem:** Man-in-the-Middle-Angriff möglich ohne Authentifizierung
- **Lösung:** Public Key + digitale Signatur `Sign(sk_A, M)` + Zertifikate (PKI)

---

## 8. Transport Layer Security (TLS)

### Ziel (RFC 8446, TLS 1.3)

Sicherer Kanal zwischen zwei kommunizierenden Parteien mit:

- **Authentication:** Server wird immer, Client optional authentifiziert
- **Confidentiality:** Daten nur für Endpunkte sichtbar
- **Integrity:** Manipulationen werden erkannt

### Einordnung im OSI-Modell

TLS liegt zwischen **Session/Presentation Layer** (OSI 5/6) und **Transport Layer** (OSI 4):

```
Application → TLS/SSL → TCP/UDP → Network → Data Link → Physical
```

### TLS-Komponenten

- **Handshake Layer:** Handshake, Alert, Change Cipher Spec (nur für Kompatibilität in v1.3)
- **Record Layer:** Fragmentierung, Kompression (entfernt in v1.3), Authentifizierung, Verschlüsselung

### TLS Handshake (vereinfacht)

```
Client                          Server
  ClientHello (key_share, etc.) →
                ← ServerHello, {EncryptedExtensions},
                   {Certificate}, {CertificateVerify}, {Finished}
  {Certificate}, {CertificateVerify}, {Finished} →
  [Application Data] ↔ [Application Data]
```

### TLS Key Exchange Modi

- **(EC)DHE** – Diffie-Hellman über finite Felder oder elliptische Kurven
- **PSK-only** – Pre-Shared Key
- **PSK mit (EC)DHE**

### SSL/TLS Versionshistorie

|Version|Jahr|Status|
|---|---|---|
|SSL 1.0|–|Unveröffentlicht|
|SSL 2.0|1995|Deprecated 2011|
|SSL 3.0|1996|Deprecated 2015|
|TLS 1.0|1999|Deprecated 2021|
|TLS 1.1|2006|Deprecated 2021|
|TLS 1.2|2008|Noch in Nutzung|
|**TLS 1.3**|**2018**|**Aktuell**|

### Bekannte TLS-Angriffe

> _"Attacks always get better; they never get worse"_

BEAST, POODLE, LOGJAM, RC4 (Harmful?), Heartbleed, LUCKY 13, Raccoon Attack, ALPACA Attack, TLS-RENEGOTIATION, u.v.m.

### Cipher-Sicherheit (Auswahl)

- **Sicher in TLS 1.3:** AES-GCM, AES-CCM, ChaCha20-Poly1305
- **Unsicher/Entfernt:** AES-CBC (abhängig von Mitigations), 3DES, RC4 (verboten in TLS 1.1+)
- **Datenintegrität in TLS 1.3:** Nur AEAD

### TLS-Anwendungsprotokolle

|Protokoll|Beschreibung|
|---|---|
|HTTPS|HTTP über TLS/TCP|
|SMTPS|Sicheres Mail-Transfer-Protokoll|
|POP3S|Post-Office-Protokoll (sicher)|
|IMAPS|Internet Message Access (sicher)|
|FTPS|File Transfer (sicher)|
|SIPS|Session Initiation (sicher)|

---

## 9. QUIC

QUIC kombiniert TLS-Sicherheit mit UDP-basiertem Transport und ersetzt den TCP+TLS-Stack:

```
Traditionell:  HTTP/2 | TLS | TCP | IP
QUIC:          HTTP/2 | QUIC (Multistream, Encryption, Congestion, Reliability) | UDP | IP
```

**QUIC-Vorteile:** Eingebettete Verschlüsselung, Multistream, schnellerer Handshake (0-RTT möglich), bessere Performance bei Paketverlusten.

---

## 10. IPSec

IPSec arbeitet auf **Layer 3 (Network Layer)** des OSI-Modells.

### Modi

**Tunnel Mode:** Das gesamte ursprüngliche IP-Paket wird verschlüsselt und in ein neues IP-Paket eingebettet (Gateway zu Gateway).

### Protokolle

|Header|Bietet|
|---|---|
|**AH (Authentication Header)**|Authentifizierung des gesamten Pakets (kein Verschlüsseln)|
|**ESP (Encapsulating Security Payload)**|Verschlüsselung + Authentifizierung der Daten|

---

## 11. Quantenmechanik – Grundlagen

### Relevante Phänomene

- **Nondeterminismus:** Messung eines Quantenzustands ergibt zufälliges, nicht vorhersagbares Ergebnis → echte Zufallszahlengeneratoren (QRNG)
- **Superposition:** Ein Qubit kann gleichzeitig `|0⟩` und `|1⟩` sein: `1/√2 |alive⟩ + 1/√2 |dead⟩`
- **Verschränkung (Entanglement):** Zwei Qubits sind korreliert, auch über Distanz: `|↑⟩|↑⟩ + |↓⟩|↓⟩`
- **Unschärfe (Uncertainty):** Heisenbergsche Unschärferelation – Ort und Impuls nicht gleichzeitig exakt messbar

---

## 12. Quantum Key Distribution – BB84 Protokoll

**Erfinder:** Charles Bennett & Gilles Brassard (1984)

### Ablauf

1. Alice wählt zufällige Bits und kodiert sie in Photonen (mit zufällig gewählten Basen)
2. Bob misst die Photonen mit zufällig gewählten Basen
3. Alice und Bob vergleichen ihre Basen (öffentlich)
4. Bits mit übereinstimmenden Basen ergeben den **Sifted Key**

**Sicherheit:** Jede Messung durch Eve verändert den Quantenzustand (Messung = Störung). In 25 % der Fälle führt Eves Abhören zu einem Bitfehler → Eve ist **nachweisbar**.

### No-Cloning-Theorem

Quantenzustände können **nicht kopiert** werden → klassische Repeater funktionieren nicht → Lösung: **Quantum Repeater**

### Satellite-QKD

BB84 über Satelliten ermöglicht Quantenkommunikation über >1000 km (z.B. Micius-Satellit).

---

## 13. Quantencomputer & Auswirkungen auf Kryptographie

### Shors Algorithmus

Peter Shor (1994): Kann **ganzzahlige Faktorisierung** und **diskrete Logarithmen** in **polynomialer Zeit** lösen.

**Konsequenz:**

|Algorithmus|Verwendung|Pre-Shor-Sicherheit|Post-Shor-Sicherheit|
|---|---|---|---|
|RSA-3072|Verschlüsselung/Signatur|128 Bit|**keine**|
|DH-3072|Schlüsselaustausch|128 Bit|**keine**|
|DSA-3072|Signatur|128 Bit|**keine**|
|256-bit ECDH/ECDSA|Schlüsselaustausch/Signatur|128 Bit|**keine**|

### Grovers Algorithmus

Lov Grover: Findet eine Nadel im Heuhaufen der Größe N in **O(√N)** Schritten.

**Konsequenz:** Halbierung der effektiven Schlüssellänge symmetrischer Verfahren.

|Algorithmus|Pre-Grover-Sicherheit|Post-Grover-Sicherheit|
|---|---|---|
|AES-128|128 Bit|**64 Bit**|
|AES-256|256 Bit|128 Bit ✓|
|SHA-256|256 Bit*|128 Bit* ✓|
|SHA-3|256 Bit*|128 Bit* ✓|

### Simons Algorithmus

Löst Simons Problem exponentiell schneller als klassische Algorithmen:

- Klassisch: `Ω(2^(n/2))` Anfragen
- Quantum: `O(n)` Anfragen

### Im Quantenzeitalter gebrochene Konstruktionen

Durch quantenbasierte Angriffe (insbesondere via Simons Algorithmus) sind viele klassische Konstruktionen **gebrochen**:

- Even-Mansour
- 3-Runden-Feistel
- LRW
- CBC-MAC
- GMAC
- PMAC
- GCM
- OCB
- … (und viele weitere)

> ⚠️ Dies motiviert die Notwendigkeit von **Post-Quantum Cryptography (PQC)**.

---

## Überblick: Key Takeaways

|Thema|Kernaussage|
|---|---|
|Digitale Signaturen|Bieten Integrität, Authentizität, Non-Repudiation|
|RSA-Signatur|Ohne Padding anfällig für Existential Forgery|
|RSA-PSS|Sicheres Padding schützt vor Forgery-Angriffen|
|ECDSA|Effizientere Alternative zu RSA auf Basis elliptischer Kurven|
|Zertifikate (X.509)|PKI löst das Problem der Public-Key-Authentizität|
|IBE|Identität als öffentlicher Schlüssel, PKG verteilt private Schlüssel|
|TLS 1.3|Modernes Protokoll: AEAD, keine Kompression, PFS durch (EC)DHE|
|QUIC|TLS-Sicherheit direkt in UDP eingebettet, schnellerer Verbindungsaufbau|
|IPSec|Sicherheit auf Netzwerkschicht, Tunnel- und Transportmodus|
|Quantenmechanik|Nondeterminismus, Superposition, Verschränkung als Grundlage für QKD|
|BB84|Quantenschlüsselaustausch, sicher durch No-Cloning-Theorem|
|Shors Algorithmus|Bricht RSA, DH, ECDH, ECDSA vollständig|
|Grovers Algorithmus|Halbiert effektive Schlüssellänge symmetrischer Verfahren|
|Post-Quantum-Krypto|Notwendigkeit neuer quantenresistenter Verfahren|

---

_Tags: #Kryptographie #TLS #Signaturen #RSA #ECDSA #Zertifikate #IBE #QuantumCryptography #BB84 #PostQuantum #HWR_