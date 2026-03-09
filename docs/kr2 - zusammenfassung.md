# Kryptographie – Zusammenfassung Vorlesung 2
_Prof. Dr. Björn Grohmann · HWR Berlin_ _Nur neuer Inhalt (ab Folie 73) – Wiederholungen aus Vorlesung 1 ausgelassen_

---

## Message Authentication Code (MAC)

Ein **MAC** (Message Authentication Code) ist ein kurzer Tag `t`, der mit einem symmetrischen Schlüssel `k` aus einer Nachricht `m` berechnet wird:

```
t = MAC(k, m)
```

MAC bietet **Integrität** und **Authentizität**, aber keine Vertraulichkeit. Sender und Empfänger teilen denselben Schlüssel.

### Angriffsvektoren auf MACs (von stark → schwach)

|Stärke|Angriff|Beschreibung|
|---|---|---|
|Stärkster|**Total Break**|Alle Systemparameter sind gebrochen; Angreifer kann für beliebige Nachricht einen MAC erzeugen|
||**Selective Forgery**|MAC für eine Nachricht erzeugbar, die _vor_ dem Angriff vom Angreifer gewählt wurde|
|Schwächster|**Existential Forgery**|MAC für _irgendeine_ Nachricht erzeugbar (auch sinnlose)|

---

## Wie man lange Nachrichten NICHT mit einem MAC versehen sollte

Mehrere naive Konstruktionen sind unsicher:

1. **Kein Schlüssel im MAC**: Angreifer kann eigene Blöcke einfügen.
2. **Alle Blöcke mit demselben Schlüssel unabhängig MACen** (`t_i = MAC(k, m_i)`): Reihenfolge der Blöcke kann vertauscht werden (Reordering-Angriff).
3. **Mit laufender Blocknummer** (`t_i = MAC(k, i || m_i)`): Blöcke aus verschiedenen Nachrichten können gemischt werden.
4. **Nachrichten-ID hinzufügen** (`t_i = MAC(k, id || i || m_i)`): Letzter Block kann weggelassen werden (Truncation-Angriff).
5. **Länge im letzten Block kodieren**: Erst dann ist die Konstruktion sicher (CBC-MAC-Variante).

---

## HMAC (Hash-MAC)

```
HMAC(k, m) = H( (k XOR opad) || H( (k XOR ipad) || m ) )
```

**H** ist eine kryptographische Hash-Funktion mit den Eigenschaften:

- Effizient zu berechnen
- Schwer zu invertieren (Einwegfunktion)
- Kollisionsresistenz: schwer, zwei Eingaben mit gleichem Hash zu finden
- Kleine Eingabeänderungen → große Ausgabeänderungen (Diffusion / Lawineneffekt)

`opad` und `ipad` sind feste Konstanten (Byte-Padding).

---

## Kombinationen von Verschlüsselung und MAC

Es gibt drei Möglichkeiten, Verschlüsselung (Enc) und MAC zu kombinieren:

|Variante|Schema|Empfehlung|
|---|---|---|
|**Encrypt-then-MAC**|`c = Enc(k₁, m)` → `t = MAC(k₂, c)`|✅ Empfohlen (z. B. TLS 1.3)|
|**MAC-then-Encrypt**|`t = MAC(k₂, m)` → `c = Enc(k₁, m \| t)`|⚠️ Problematisch (z. B. Padding-Oracle-Angriff in TLS < 1.3)|
|**Encrypt-and-MAC**|`c = Enc(k₁, m)` und `t = MAC(k₂, m)` parallel|⚠️ MAC kann Klartextinfo leaken|

**Encrypt-then-MAC** ist die sichere Variante: Der MAC schützt den Chiffretext, sodass manipulierte Ciphertexte sofort erkannt werden, bevor sie entschlüsselt werden.

---

## Authenticated Encryption with Associated Data (AEAD)

**AEAD** kombiniert Verschlüsselung und Authentifizierung in einem einzigen Algorithmus:

```
(c, t) = AEAD_Enc(k, nonce, m, aad)
m      = AEAD_Dec(k, nonce, c, t, aad)
```

- `m` = Plaintext (wird verschlüsselt **und** authentifiziert)
- `aad` = _Associated Authenticated Data_ (wird nur authentifiziert, nicht verschlüsselt, z. B. Header)
- Gibt `⊥` zurück, wenn die Authentifizierung fehlschlägt

### Beispiel: ChaCha20-Poly1305

- **ChaCha20**: Stromchiffre (Verschlüsselung)
- **Poly1305**: MAC über den Ciphertext
- Eingaben: 256-bit Key, 96-bit Nonce, Plaintext
- Weit verbreitet in TLS 1.3, SSH, WireGuard

### Beispiel: Galois Counter Mode (GCM)

- Kombiniert **CTR-Mode** (Verschlüsselung mit AES) und **GHASH** (MAC über das Galois-Feld GF(2¹²⁸))
- Standard für AES-GCM in TLS 1.3

---

## Symmetric Search over Encrypted Data

Problem: Wie kann man auf verschlüsselten Daten (z. B. in der Cloud) suchen, ohne den Schlüssel preiszugeben?

|Ansatz|Idee|Problem|
|---|---|---|
|**1. Idee**|Alice gibt Bob Wort `W` + Schlüssel `k`|Bob kennt den Schlüssel → kein Datenschutz|
|**2. Idee**|Alice gibt Bob `Enc(W)` + zugehörigen Schlüssel|Deterministisches Enc → gleiche Wörter → gleiche Ciphertexte → Häufigkeitsanalyse möglich|
|**3. Idee**|Pseudorandom Function (PRF)-basierter Index: Alice erstellt eine verschlüsselte Lookup-Tabelle. Für jedes Wort `w` wird ein Token `T = PRF(k, w)` erzeugt und der zugehörige Index verschlüsselt gespeichert.|Leakt _access pattern_ (welche Dokumente abgerufen werden)|

Die dritte Idee ist die Grundlage von **Searchable Symmetric Encryption (SSE)**. Sie erlaubt Bob, anhand eines Tokens zu suchen, ohne `k` oder `w` zu kennen.

---

## Public-Key-Kryptographie

### Das Schlüsselaustauschproblem

Bei symmetrischer Kryptographie müssen beide Parteien denselben geheimen Schlüssel kennen – aber wie tauscht man ihn sicher aus, wenn nur ein unsicherer Kanal verfügbar ist?

### Merkle Puzzle (1974)

Alice erzeugt `n` verschlüsselte Rätsel mit je einer ID und einem Schlüssel. Bob löst zufällig eines davon (brute force, O(n)). Ein Angreifer muss im Durchschnitt `n/2` Rätsel lösen (O(n)). Vorteil ist quadratisch: O(n) Aufwand für Alice/Bob, O(n²) für Angreifer. Praktisch zu ineffizient.

### Idee: Virtual Black Box (VBB) Obfuscator

Idee: Ein Programm so verschleiern, dass man es zwar ausführen, aber nicht "verstehen" kann. Ein VBB-Obfuscator würde Public-Key-Kryptographie aus einer OWF ermöglichen. **Leider existiert kein allgemeiner VBB-Obfuscator** (Barak et al. 2001 bewiesen Unmöglichkeit). Schwächere Varianten (_Indistinguishability Obfuscation_, iO) sind noch Forschungsthema.

---

## Diffie-Hellman-Schlüsselaustausch

Ermöglicht zwei Parteien, über einen öffentlichen Kanal einen gemeinsamen geheimen Schlüssel zu vereinbaren.

```
Öffentlich bekannt: Gruppe G, Generator g, Primzahl p

Alice wählt a (geheim),  sendet A = g^a mod p
Bob   wählt b (geheim),  sendet B = g^b mod p

Gemeinsames Geheimnis: K = B^a mod p = A^b mod p = g^(ab) mod p
```

Sicherheit basiert auf dem **Diskreten-Logarithmus-Problem (DLP)**: Gegeben `g`, `p` und `g^a mod p`, ist es schwer, `a` zu berechnen.

---

## Das Diskrete-Logarithmus-Problem (DLP)

**Definition:**

- Gegeben: Gruppe `G`, Generator `g`, Element `y = g^x`
- Gesucht: `x = log_g(y)`

Das Berechnen von `g^x` ist effizient (schnelle Exponentiation: O(log x) Multiplikationen). Die Umkehrung (diskreter Logarithmus) ist für große Gruppen rechnerisch schwer (kein effizienter Algorithmus bekannt für klassische Computer).

---

## Einheitengruppe eines endlichen Körpers: ModP

Die Menge `ℤ_p* = {1, 2, ..., p-1}` mit Multiplikation modulo `p` (p prim) bildet eine **zyklische Gruppe** der Ordnung `p-1`.

- Es gibt einen **Generator** `g`, sodass `{g^0, g^1, ..., g^(p-2)} = ℤ_p*`
- Für Diffie-Hellman wählt man `p` und `g` so, dass die Gruppe groß genug ist (heute ≥ 2048 Bit)

**Fermat'scher kleiner Satz:**  
`a^(p-1) ≡ 1 (mod p)` für alle `a` mit `ggT(a,p) = 1`

---

## Elliptische Kurven

Elliptische Kurven bieten dieselbe Sicherheit wie ModP-Gruppen, aber mit **viel kleineren Schlüsseln**.

**Kurvendefinition** (Weierstraß-Form):

```
y² = x³ + ax + b   (über einem Körper K)
```

mit Bedingung `4a³ + 27b² ≠ 0` (keine Singularitäten).

### Gruppengesetz auf elliptischen Kurven

Punkte auf der Kurve bilden eine abelsche Gruppe mit:

- **Neutrales Element**: Punkt im Unendlichen `O`
- **Addition** `P + Q`: Schneide die Linie durch `P` und `Q` mit der Kurve; reflektiere den dritten Schnittpunkt an der x-Achse
- **Verdoppelung** `2P`: Tangente an `P`; reflektiere zweiten Schnittpunkt

### ECDLP (Elliptic Curve Discrete Logarithm Problem)

Gegeben Punkte `P` und `Q = k·P`, finde `k`. Gilt als schwerer als DLP in ModP → kleinere Schlüssel möglich.

|Sicherheitsniveau|RSA/DH Schlüssellänge|ECC Schlüssellänge|
|---|---|---|
|128 Bit|3072 Bit|256 Bit|
|256 Bit|15360 Bit|521 Bit|

**Bekannte Kurven**: NIST P-256, Curve25519 (X25519, Ed25519)

---

## RSA (Rivest–Shamir–Adleman, 1977)

### Schlüsselgenerierung

```
1. Wähle zwei große Primzahlen p, q
2. n = p · q         (öffentlich, RSA-Modulus)
3. φ(n) = (p-1)(q-1) (Eulersche Phi-Funktion, geheim)
4. Wähle e mit ggT(e, φ(n)) = 1   (öffentlicher Exponent, oft e = 65537)
5. Berechne d = e⁻¹ mod φ(n)      (privater Exponent)

Öffentlicher Schlüssel: (n, e)
Privater Schlüssel:     (n, d)
```

### Ver- und Entschlüsselung

```
Verschlüsselung: c = m^e mod n
Entschlüsselung: m = c^d mod n
```

Korrektheit folgt aus dem **Satz von Euler**: `m^(φ(n)) ≡ 1 (mod n)`, daher `m^(e·d) ≡ m (mod n)`.

---

## Das Faktorisierungsproblem

Sicherheit von RSA basiert auf der Annahme, dass es schwer ist, `n = p · q` in seine Primfaktoren zu zerlegen.

- Multiplikation `p · q → n`: effizient (O(log²n))
- Faktorisierung `n → p, q`: schwer (bester klassischer Algorithmus: Zahlkörpersieb, subexponentiell aber nicht polynomial)

**Wichtig**: Faktorisierungsproblem ≠ RSA-Sicherheit direkt. Es ist nicht bewiesen, dass Faktorisierung äquivalent zu RSA-Brechen ist, aber kein besserer Angriff ist bekannt.

---

## Wie misst man Sicherheit? (3. Ansatz: IND-CCA)

**IND-CCA** (_Indistinguishability under Chosen Ciphertext Attack_) ist das stärkste gängige Sicherheitsmodell für Public-Key-Verschlüsselung.

Erweiterung des IND-CPA-Spiels: Der Angreifer darf zusätzlich ein **Decryption Oracle** befragen (außer für den Challenge-Ciphertext).

Ein Schema ist **IND-CCA-sicher**, wenn kein effizienter Angreifer einen Vorteil `> negl(n)` hat.

**Naives RSA (textbook RSA) ist NICHT IND-CPA-sicher**, da es deterministisch ist. Lösung: Padding-Schemata.

---

## OAEP (Optimal Asymmetric Encryption Padding)

**OAEP** macht RSA probabilistisch und erreicht IND-CCA2-Sicherheit im Random-Oracle-Modell.

```
Eingabe: Nachricht m, zufällige Seed r

X = (m || 0...0) XOR G(r)    (G = Pseudozufallsfunktion)
Y = r XOR H(X)               (H = Hashfunktion)

RSA-Input: (X || Y)
```

**Entschlüsselung**: RSA anwenden, dann OAEP umkehren. In der Praxis: **RSA-OAEP** aus PKCS#1 v2.x.

---

## ElGamal-Verschlüsselung

Auf Diffie-Hellman basierendes Public-Key-Verfahren (Taher Elgamal, 1985).

### Schlüsselgenerierung

```
Öffentlich: Gruppe G, Generator g, Primzahl p
Privat:     x (zufällig gewählt)
Öffentlich: h = g^x mod p
```

### Verschlüsselung (probabilistisch)

```
Wähle zufälliges r
c₁ = g^r mod p
c₂ = m · h^r mod p
Ciphertext: (c₁, c₂)
```

### Entschlüsselung

```
m = c₂ · (c₁^x)⁻¹ mod p
```

**Korrektheit**: `c₁^x = g^(rx)`, und `c₂ / c₁^x = m · h^r / g^(rx) = m · g^(xr) / g^(xr) = m`

**Sicherheit**: Basiert auf der **Computational Diffie-Hellman (CDH)** Annahme. ElGamal ist IND-CPA-sicher unter der DDH-Annahme.

**Nachteil**: Ciphertext ist doppelt so lang wie die Nachricht (Ciphertext-Expansion).

---

## Übersicht: Symmetrische vs. Asymmetrische Kryptographie

|Eigenschaft|Symmetrisch (z. B. AES, ChaCha20)|Asymmetrisch (z. B. RSA, ElGamal)|
|---|---|---|
|Schlüssel|Ein gemeinsamer geheimer Schlüssel|Schlüsselpaar (öffentlich/privat)|
|Geschwindigkeit|Schnell|Langsam (10–1000× langsamer)|
|Schlüsselaustausch|Problem (sicherer Kanal nötig)|Kein sicherer Kanal nötig|
|Anwendung|Bulk-Datenverschlüsselung|Schlüsselaustausch, Signaturen|
|Praxis|Beide kombiniert in **Hybrid-Kryptographie**||

In der Praxis: Asymmetrische Kryptographie tauscht einen Session-Key aus, der dann für symmetrische Verschlüsselung verwendet wird (z. B. TLS Handshake).