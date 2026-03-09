# Kryptographie – Zusammenfassung Vorlesung 1

**Prof. Dr. Björn Grohmann | HWR Berlin | 16.02.2026**

---

## 1. Einführung: Die Geschichte von Maria Stuart

Die Vorlesung beginnt mit einem historischen Beispiel: Maria Stuart (1542–1587), Königin von Schottland, wurde durch das Scheitern ihrer verschlüsselten Kommunikation zum Tode verurteilt. Im sogenannten **Babington-Plot (1586)** kommunizierte sie über geheime Briefe mit Anthony Babington, die in Bierfässern geschmuggelt wurden. Sir Francis Walsingham (Geheimdienstchef von Elizabeth I.) und sein Kryptoanalyst Thomas Phelippes fingen die Briefe ab und entschlüsselten sie. Maria Stuarts Chiffre – eine einfache monoalphabetische Substitution mit Symbolen für Buchstaben und häufige Wörter – bot keinen ausreichenden Schutz.

**Was fehlte für sichere Kommunikation?**

- **Vertraulichkeit (Confidentiality):** Nur berechtigte Empfänger sollen den Inhalt lesen können.
- **Integrität (Integrity):** Die Nachricht darf nicht unbemerkt verändert werden.
- **Authentizität (Authenticity):** Der Absender muss zweifelsfrei identifizierbar sein.

---

## 2. Häufigkeitsanalyse

Einfache Substitutionschiffren lassen sich durch **Häufigkeitsanalyse** brechen: Man zählt, wie oft jedes Symbol im Geheimtext vorkommt, und vergleicht die Verteilung mit der bekannten Buchstabenhäufigkeit der Sprache.

Im Englischen ist z. B. **E** mit ca. 11,16 % der häufigste Buchstabe, gefolgt von A (8,50 %), R (7,58 %), I (7,54 %), O (7,16 %) usw. Samuel Morse nutzte diese Erkenntnis bereits für sein Morsealphabet – häufige Buchstaben bekamen kurze Codes.

---

## 3. Klassische Chiffren

### 3.1 Caesar-Chiffre

Jeder Buchstabe wird um eine feste Anzahl *n* im Alphabet verschoben:

- **Verschlüsselung:** E_n(x) = x + n mod 26
- **Entschlüsselung:** D_n(x) = x − n mod 26

Beispiel (n = 3): A → X, B → Y, E → B. Der Schlüsselraum ist mit nur 25 möglichen Verschiebungen trivial klein und per Brute-Force sofort zu brechen.

### 3.2 Vigenère-Chiffre

Eine polyalphabetische Substitution: Ein Schlüsselwort wird wiederholt über den Klartext gelegt. Jeder Buchstabe wird mit einem anderen Caesar-Shift verschlüsselt.

- **Verschlüsselung:** C_i = M_i + K_i mod 26
- **Entschlüsselung:** M_i = C_i − K_i mod 26

Beispiel: Plaintext „attackatdawn" + Key „LEMONLEMONLE" → Ciphertext „LXFOPVEFRNHR"

**Schwäche:** Durch den **Kasiski-Test** lässt sich die Schlüssellänge ermitteln. Wiederholt sich ein Muster im Klartext und fällt es auf dieselbe Schlüsselposition, entsteht ein identisches Muster im Geheimtext. Der Abstand solcher Wiederholungen ist ein Vielfaches der Schlüssellänge.

### 3.3 Homophone Chiffren

Versuch, die Häufigkeitsanalyse zu erschweren: Jedem Buchstaben werden mehrere Symbole zugeordnet, proportional zu seiner Häufigkeit. Trotzdem bieten sie keinen vollständigen Schutz.

### 3.4 Beale-Chiffren

Ein berühmtes ungelöstes Kryptorätsel: Drei Chiffretexte (Zahlenfolgen) sollen den Standort eines vergrabenen Schatzes beschreiben. Chiffretext 2 wurde mithilfe der US-Unabhängigkeitserklärung als Schlüsseltext entschlüsselt (jede Zahl verweist auf das Anfangswort im Dokument). Chiffretexte 1 und 3 sind bis heute ungeknackt.

---

## 4. Informationstheoretische Sicherheit

### 4.1 Informationsgehalt und Entropie

**Informationsgehalt** eines Zeichens x mit Wahrscheinlichkeit p_x:

> I_x = log(1/p_x) = −log(p_x)

Je seltener ein Zeichen, desto größer sein Informationsgehalt.

**Entropie** H(X) – der mittlere Informationsgehalt einer Zufallsvariable:

> H(X) = −∑_x p_x · log(p_x)

**Bedingte Entropie:**

> H(X|Y) = H(X, Y) − H(Y)
>
> H(X, Y) ≤ H(X) + H(Y)

### 4.2 Perfekte Sicherheit (Shannon)

Claude Shannon (1916–2001) definierte: Ein Verschlüsselungssystem hat **perfekte Sicherheit (Perfect Secrecy)**, genau dann wenn:

> **H(M|E) = H(M)**

Das bedeutet: Die bedingte Entropie der Nachricht M gegeben den Geheimtext E ist gleich der Entropie von M allein. Anders formuliert: **M und E sind stochastisch unabhängig** – der Geheimtext verrät keinerlei Information über den Klartext. Jeder Chiffretext ist unabhängig vom Klartext gleich wahrscheinlich.

### 4.3 One-Time Pad (OTP)

Das einzige Verfahren, das perfekte Sicherheit erreicht:

- Der Schlüssel wird per **XOR** mit dem Klartext verknüpft: E = P ⊕ K
- Der Schlüssel muss **echt zufällig** sein
- Der Schlüssel muss **mindestens so lang wie die Nachricht** sein
- Der Schlüssel darf **nur einmal** verwendet werden

**Problem:** Der Schlüssel muss genauso lang sein wie die Nachricht und sicher übertragen werden – in der Praxis meist nicht handhabbar.

---

## 5. Kryptographische Primitive

### 5.1 Einwegfunktionen (One-Way Functions – OWF)

Eine Funktion f : {0,1}* → {0,1}* mit |f(x)| = |x| ist eine Einwegfunktion, wenn:

1. **Leicht zu berechnen:** Es existiert ein Polynomialzeit-Algorithmus A mit A(x) = f(x) für alle x.
2. **Schwer umzukehren:** Für jeden probabilistischen Polynomialzeit-Algorithmus A', jedes Polynom p(.) und alle hinreichend großen n gilt: Pr[A'(f(U_n)) = f⁻¹ ∘ f(U_n)] < 1/p(n)

Anschaulich: x → f(x) ist einfach und schnell, f(x) → x erfordert exponentiellen Aufwand.

### 5.2 Pseudo-Zufallszahlengeneratoren (PRG/PRNG)

Eine Funktion G : {0,1}* → {0,1}* mit Streckungsfunktion l(n) ist ein PRG, wenn:

1. G ist ein **Polynomialzeit-Algorithmus**
2. Für jedes x gilt: |G(x)| = l(|x|) > |x| (Ausgabe ist länger als Eingabe)
3. Die Verteilungen {G(U_n)} und {U_l(n)} sind **berechnungsmäßig ununterscheidbar** (computational indistinguishability)

**Berechnungsmäßige Ununterscheidbarkeit** (Definition 13.4): Zwei Wahrscheinlichkeitsensembles {X_n} und {Y_n} sind berechnungsmäßig ununterscheidbar, wenn für jeden probabilistischen Polynomialzeit-Algorithmus A und jedes Polynom p(.) ab einem N gilt:

> |Pr(A(X_n) = 1) − Pr(A(Y_n) = 1)| < 1/p(n)

**Amplifikation der Streckungsfunktion** (Theorem 13.10): Hat man einen PRG mit Streckungsfunktion n + 1, dann existiert für jedes Polynom l(n) ein PRG mit Streckungsfunktion l(n). Dies geschieht durch iteriertes Anwenden von G₁.

### 5.3 Zusammenhang OWF ↔ PRG

> **Theorem: Pseudo-Zufallszahlengeneratoren existieren genau dann, wenn Einwegfunktionen existieren.**

**PRG → OWF:** Aus einem PRG G : {0,1}^n → {0,1}^{2n} kann man eine OWF konstruieren: f(xy) = G(x) wobei |x| = |y| = n. Die Funktion „vergisst" die Hälfte der Eingabe.

**OWF → PRG:** Über den Umweg eines **Hardcore-Prädikats (HCP)**. Sei f eine OWF, dann ist b(x, r) = Skalarprodukt von x und r mod 2 ein Hardcore-Prädikat von f'(x,r) = (f(x), r). Der PRG ergibt sich als G(s) = f'(s) ∘ b(s). Ein HCP ist leicht zu berechnen, aber aus f(x) allein nicht vorhersagbar (Wahrscheinlichkeit < 1/2 + 1/p(n)).

---

## 6. Symmetrische Verschlüsselung

Eine Chiffre heißt **symmetrisch**, wenn für Ver- und Entschlüsselung dasselbe Schlüsselmaterial verwendet wird.

### 6.1 Strom-Chiffren

Prinzip: Ein kurzer Schlüssel (Seed) wird durch einen PRNG zu einem langen Schlüsselstrom gestreckt, der per XOR mit dem Klartext verknüpft wird.

**ChaCha20** – eine moderne Strom-Chiffre:

- **Eingaben:** 256-Bit Schlüssel, 32-Bit Zähler, 96-Bit Nonce, beliebig langer Klartext
- **Ausgabe:** Geheimtext gleicher Länge
- **Kernoperation – Quarter Round:** Arbeitet auf vier 32-Bit-Werten (a, b, c, d) mit Addition, XOR und Rotation:
  1. a += b; d ^= a; d <<<= 16
  2. c += d; b ^= c; b <<<= 12
  3. a += b; d ^= a; d <<<= 8
  4. c += d; b ^= c; b <<<= 7
- Ein **inner_block** besteht aus 8 Quarter Rounds (4 Spalten + 4 Diagonalen)
- **chacha20_block:** Zustand = Konstanten | Key | Counter | Nonce → 10× inner_block → Zustand addieren → serialisieren
- Verschlüsselung: Für jeden 64-Byte-Block wird ein Schlüsselstrom erzeugt und per XOR verknüpft

### 6.2 Block-Chiffren

Ein Klartextblock fester Größe wird mit einem Schlüssel in einen Geheimtextblock gleicher Größe transformiert. Die zentrale Frage: Wie verschlüsselt man Daten, die länger als ein Block sind? → **Betriebsmodi**

---

## 7. Betriebsmodi (Modes of Operation)

### 7.1 ECB (Electronic Codebook)

Jeder Block wird unabhängig verschlüsselt. **Problem:** Identische Klartextblöcke ergeben identische Geheimtextblöcke → Muster bleiben sichtbar. Nicht IND-CPA-sicher.

### 7.2 CBC (Cipher Block Chaining)

Jeder Klartextblock wird vor der Verschlüsselung mit dem vorherigen Geheimtextblock XOR-verknüpft. Der erste Block wird mit einem **Initialization Vector (IV)** verknüpft. **Achtung:** Anfällig für **Padding Oracle Attacks** – wenn das System bei der Entschlüsselung zwischen Padding-Fehlern und anderen Fehlern unterscheidet, kann der Klartext ohne Schlüsselkenntnis rekonstruiert werden.

### 7.3 CTR (Counter Mode)

Wandelt eine Block-Chiffre in eine Strom-Chiffre um: Nonce + fortlaufender Zähler werden verschlüsselt und per XOR mit dem Klartext verknüpft. Vorteil: Parallelisierbar, kein Padding nötig.

### 7.4 OFB (Output Feedback)

Der IV wird verschlüsselt, das Ergebnis als nächster Eingabeblock verwendet. Der Schlüsselstrom ist unabhängig vom Klartext.

### 7.5 CFB (Cipher Feedback)

Ähnlich wie OFB, aber der Geheimtext (statt des Verschlüsselungsoutputs) wird als nächster Eingabeblock verwendet.

### 7.6 Cipher Text Stealing

Ein Verfahren, das Padding vermeidet, indem der letzte vollständige und der letzte unvollständige Block geschickt vertauscht und kombiniert werden.

---

## 8. Kryptoanalyse und Angriffsmodelle

Die Angriffstypen sind nach aufsteigender Stärke des Angreifers geordnet:

| Angriffstyp | Fähigkeit des Angreifers |
|---|---|
| **Ciphertext-only** | Kennt nur den Geheimtext |
| **Known Plaintext** | Kennt Paare von Klartext und Geheimtext |
| **Chosen Plaintext (CPA)** | Kann beliebige Klartexte verschlüsseln lassen |
| **Adaptive Chosen Plaintext** | Wie CPA, kann aber Anfragen adaptiv stellen |
| **Chosen Ciphertext (CCA)** | Kann beliebige Geheimtexte entschlüsseln lassen |
| **Adaptive Chosen Ciphertext** | Wie CCA, adaptiv |

### IND-CPA-Sicherheit

Das „Find-then-Guess"-Spiel: Ein Angreifer A interagiert mit einem Challenger C. C erzeugt einen Schlüssel k und ein Bit b ∈ {0,1}. A darf beliebig viele Klartexte verschlüsseln lassen, wählt dann zwei Nachrichten M₁, M₂ gleicher Länge. C verschlüsselt M_b und gibt den Geheimtext zurück. A muss b erraten. Die Chiffre ist IND-CPA-sicher, wenn der Vorteil von A vernachlässigbar ist: Adv(A) = |Pr[b = b'] − 1/2| ≈ 0.

---

## 9. DES und AES

### 9.1 Data Encryption Standard (DES, 1977)

- **Blockgröße:** 64 Bit
- **Schlüssellänge:** 56 Bit (effektiv)
- **Struktur:** Feistel-Netzwerk mit 16 Runden
- **Feistel-Netzwerk:** Der Block wird in zwei Hälften (L, R) geteilt. Pro Runde: L_{i+1} = R_i und R_{i+1} = L_i ⊕ F(R_i, K_i). Die Entschlüsselung funktioniert durch Anwenden der Rundenschlüssel in umgekehrter Reihenfolge.
- **Kritik (Diffie & Hellman):** Die 56-Bit-Schlüssellänge ist zu kurz für exhaustive Suche. Empfehlung: mindestens 128 Bit.
- **Heute als unsicher eingestuft.**

### 9.2 Advanced Encryption Standard (AES, 2001)

- **Blockgröße:** 128 Bit
- **Schlüssellängen:** 128, 192 oder 256 Bit
- **Runden:** 10 (AES-128), 12 (AES-192) oder 14 (AES-256)
- **Gilt als sicher**

**AES-128 Algorithmus** (Pseudocode):

1. Schlüsselexpansion: K → (K₀, ..., K₁₀)
2. s ← M ⊕ K₀
3. Für r = 1 bis 10:
   - s ← SubBytes(s)
   - s ← ShiftRows(s)
   - Falls r ≤ 9: s ← MixColumns(s)
   - s ← s ⊕ K_r

**Die vier Transformationen:**

- **SubBytes:** Nichtlineare Byte-Substitution über eine S-Box. Jedes Byte wird durch sein multiplikatives Inverses in GF(2⁸) ersetzt und anschließend affin transformiert.
- **ShiftRows:** Zeilenweises zyklisches Verschieben (Zeile 0: kein Shift, Zeile 1: 1 Byte, Zeile 2: 2 Bytes, Zeile 3: 3 Bytes).
- **MixColumns:** Spaltenweise Multiplikation mit einem festen Polynom c(x) über GF(2⁸). Sorgt für Diffusion.
- **AddRoundKey:** XOR des Zustands mit dem Rundenschlüssel.

### Mathematik hinter der AES-S-Box

AES arbeitet im endlichen Körper **GF(2⁸)** mit dem irreduziblen Polynom:

> m(x) = x⁸ + x⁴ + x³ + x + 1

- **Addition:** XOR der Koeffizienten (entspricht XOR der Bytes)
- **Multiplikation:** Polynommultiplikation modulo m(x)
- **Multiplikatives Inverses:** Berechnung mittels des **erweiterten euklidischen Algorithmus**: Finde a(x), c(x) sodass b(x)·a(x) + m(x)·c(x) = 1

Die S-Box-Konstruktion ist zweistufig: (1) Multiplikatives Inverses in GF(2⁸), dann (2) affine Transformation über GF(2), dargestellt als Matrixmultiplikation plus Konstantenvektor.

---

## 10. Anwendungen kryptographischer Primitive

### 10.1 Lamport's One-Time-Signature

Ein digitales Signaturverfahren, das nur auf Einwegfunktionen basiert:

- **Schlüsselerzeugung:** Generiere 2 × 256 Zufallswerte r_i^0 und r_i^1 (geheimer Schlüssel sk). Der öffentliche Schlüssel pk besteht aus den Bildern unter einer OWF h: y_i^b = h(r_i^b).
- **Signatur:** Für jedes Bit b_i der Nachricht (als 256-Bit-Hash) wird r_i^{b_i} veröffentlicht.
- **Verifikation:** Berechne h auf die Signaturwerte und vergleiche mit den passenden Werten im öffentlichen Schlüssel.
- **Einmal-Eigenschaft:** Jeder Schlüssel darf nur für eine Signatur verwendet werden.

### 10.2 Bit Commitment Protokoll

Ein Zweiphasen-Verfahren, bei dem Alice sich auf ein Bit b festlegt (Commit), ohne dass Bob es kennt, und es später enthüllt (Reveal).

**Naiver Ansatz (mit PRG):**

- Commit: Alice wählt Seed s, sendet G_m(s) und B_{m+1}(s) ⊕ b
- Reveal: Alice sendet s, Bob verifiziert

**Problem:** Alice könnte zwei Seeds finden, die in den ersten m Bits übereinstimmen, aber im (m+1)-ten Bit differieren → Betrug möglich.

**Verbessertes Protokoll:**

- Bob sendet einen zufälligen Vektor R = (r₁, ..., r_{3n})
- Alice wählt Seed s und sendet d_i = B_i(s) wenn r_i = 0, bzw. d_i = B_i(s) ⊕ b wenn r_i = 1
- Die Wahrscheinlichkeit, dass Alice betrügen kann, ist höchstens 2^{−n}

---

## Zusammenfassung der Kernkonzepte

| Konzept | Kernaussage |
|---|---|
| Perfect Secrecy | H(M\|E) = H(M), erfordert Schlüssel ≥ Nachrichtenlänge |
| One-Time Pad | Einziges perfekt sicheres Verfahren, aber unpraktisch |
| Einwegfunktion | Leicht zu berechnen, schwer umzukehren |
| PRG | Streckt kurzen Seed zu pseudo-zufälligem, langem Output |
| OWF ↔ PRG | Existieren genau dann, wenn das jeweils andere existiert |
| Symmetrische Chiffre | Gleicher Schlüssel für Ver- und Entschlüsselung |
| Strom-Chiffre | PRNG + XOR (z. B. ChaCha20) |
| Block-Chiffre | Feste Blockgröße, verschiedene Betriebsmodi |
| DES | 56-Bit Schlüssel, heute unsicher |
| AES | 128/192/256-Bit Schlüssel, Arithmetik in GF(2⁸), sicher |
| IND-CPA | Standardsicherheitsbegriff für symmetrische Verschlüsselung |
