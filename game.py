"""
SpyGame : four missions, tiered scoring, rank reveal.
"""
import sys
from rsa_core  import derive_private_key, encrypt_block, decrypt_block
from encoding  import (clean_message, text_to_blocks, block_to_number,
                       number_to_block, encrypt_message, decrypt_message)


MISSION_MSG = "I AM AN UNDERCOVER SPY AT UITM"

MAX_SCORE = 160

RANKS = [
    (0,   39,  "Civilian         — you need more training"),
    (40,  79,  "Rookie           — promising start"),
    (80,  109, "Field Agent      — solid performance"),
    (110, 139, "Senior Agent     — impressive work"),
    (140, 999, "Master           — perfect execution"),
]

# Blocks asked in L3 (encrypt) and L4 (decrypt)
_L3_INDICES = [0, 2, 4]
_L4_INDICES = [1, 3, 5]


class SpyGame:
    def __init__(self, n, e):
        self.n     = n
        self.e     = e
        self.d     = derive_private_key(n, e)
        self.score = 0

    # Design function

    def banner(self, text):
        line = "=" * 54
        print(f"\n{line}")
        print(f"  {text}")
        print(f"{line}")

    def rank(self):
        for lo, hi, label in RANKS:
            if lo <= self.score <= hi:
                return label
        return "Unknown rank"

    def show_score(self):
        print(f"\n  ── Current score: {self.score} / {MAX_SCORE} pts  |  Rank: {self.rank()} ──")

    # Input function
    def _prompt(self, msg):
        """
        Wrap input(). Intercepts:
          s → show score and re-prompt
          x → confirm then exit
        Returns the raw answer for any other input.
        """
        while True:
            raw = input(msg).strip()
            if raw.lower() == 's':
                self.show_score()
            elif raw.lower() == 'x':
                confirm = input("  Exit game? [y/n]: ").strip().lower()
                if confirm == 'y':
                    print("\n  Mission aborted. Goodbye, Agent.\n")
                    sys.exit(0)
            else:
                return raw

    # Points
    def _award(self, attempt, hint_used=False):
        """Return points for a correct answer by attempt number."""
        pts = {1: 20, 2: 10, 3: 5}.get(attempt, 0)
        if hint_used:
            pts = max(pts - 5, 0)
        return pts

    # Introduction 
    def show_briefing(self):
        self.banner("UITM SPY ACADEMY — CLASSIFIED")
        print("""
            Welcome, Agent. Enemy spies monitor all communications.
            Use RSA to encrypt — then decrypt — your secret message.

            PUBLIC KEY  → anyone can encrypt
            PRIVATE KEY → only you can decrypt

            Your key pair:
                n = 1 964 556 481
                e = 456 899

            Block size  : 4 letters
            Encoding    : A=65, B=66 ... Z=90 (ASCII)

            SCORING  (per question, 3 attempts max)
                Attempt 1 correct : +20 pts
                Attempt 2 correct : +10 pts
                Attempt 3 correct :  +5 pts
                Hint used         :  -5 pts from award

            TIP: type  s  at any prompt to see your score.
                type  x  at any prompt to exit.
                    """)
        self._prompt("  Press ENTER to start your first mission...")

    # level 1: block encoding
    def level_1(self):
        self.banner("MISSION 1 — Encode a block")
        block     = "IAMA"
        correct_m = block_to_number(block)

        print(f"\n  Convert this 4-letter block to its RSA integer.")
        print(f"  Block : {block}")
        print(f"  Rule  : 2-digit ASCII per letter, concatenated.")
        print(f"  E.g.  : I=73, A=65, M=77, A=65 → 73657765")

        for attempt in range(1, 4):
            raw = self._prompt(f"\n  [s] score  [x] exit   Attempt {attempt}/3: ")
            if raw == str(correct_m):
                pts = self._award(attempt)
                self.score += pts
                print(f"  Correct! +{pts} pts")
                self.show_score()
                return
            else:
                print(f"  Not quite. Remember: 2 digits per letter, no spaces.")

        print(f"  Answer was: {correct_m}")
        self.show_score()

    #  level 2: block encryotion
    def level_2(self):
        self.banner("MISSION 2 — Encrypt a block")
        m         = 73657765
        correct_c = encrypt_block(m, self.e, self.n)

        print(f"\n  Encrypt this block value using the public key.")
        print(f"  m       = {m}")
        print(f"  Formula : c = m^e mod n")
        print(f"  Python  : pow({m}, {self.e}, {self.n})")

        hint_used = False
        for attempt in range(1, 4):
            raw = self._prompt(f"\n  [h] hint  [s] score  [x] exit   Attempt {attempt}/3: ")
            if raw.lower() == 'h':
                if not hint_used:
                    hint_used = True
                    print(f"  Hint: open Python → pow({m}, {self.e}, {self.n})")
                else:
                    print(f"  Hint already used.")
                continue
            if raw == str(correct_c):
                pts = self._award(attempt, hint_used)
                self.score += pts
                print(f"  Correct! +{pts} pts" + (" (hint penalty applied)" if hint_used else ""))
                self.show_score()
                return
            print("  Not quite. Check your formula.")

        print(f"  Answer was: {correct_c}")
        self.show_score()

    # level 3: Encrypt full message
    def level_3(self):
        self.banner("MISSION 3 — Encrypt the full message")
        print(f"\n  Message: {MISSION_MSG}")
        print(f"  (spaces removed before processing)\n")

        ciphers = encrypt_message(MISSION_MSG, self.e, self.n, encrypt_block)
        blocks  = text_to_blocks(MISSION_MSG)

        print("  Block   | Numeric m    | Cipher c")
        print("  " + "-" * 44)
        for b, c in zip(blocks, ciphers):
            m = block_to_number(b)
            print(f"  {b:<8}| {m:<13}| {c}")

        print("\n  Now YOU encrypt 3 blocks. Use: pow(m, e, n)")
        print(f"  e = {self.e},  n = {self.n}\n")

        for idx in _L3_INDICES:
            blk       = blocks[idx]
            m_val     = block_to_number(blk)
            correct_c = ciphers[idx]
            print(f"  Block [{idx}] = {blk}  →  m = {m_val}")
            for attempt in range(1, 4):
                raw = self._prompt(f"  [s] score  [x] exit   Attempt {attempt}/3 → c = ")
                if raw == str(correct_c):
                    pts = self._award(attempt)
                    self.score += pts
                    print(f"  Correct! +{pts} pts")
                    break
                print("  Not quite.")
            else:
                print(f"  Answer was: {correct_c}")
            print()

        self.show_score()

    #  level 4: Decrypt full message
    def level_4(self):
        self.banner("MISSION 4 — Decrypt the full message")
        print(f"\n  You intercept these cipher blocks. Recover the plaintext.")
        print(f"  Formula : m = c^d mod n")
        print(f"  d = {self.d},  n = {self.n}\n")

        ciphers = encrypt_message(MISSION_MSG, self.e, self.n, encrypt_block)
        blocks  = text_to_blocks(MISSION_MSG)

        print("  #  | Cipher c")
        print("  " + "-" * 30)
        for i, c in enumerate(ciphers):
            print(f"  [{i}] | {c}")

        print("\n  Decrypt 3 cipher blocks. Use: pow(c, d, n)")
        print(f"  d = {self.d},  n = {self.n}\n")

        for idx in _L4_INDICES:
            c_val     = ciphers[idx]
            correct_m = decrypt_block(c_val, self.d, self.n)
            print(f"  Cipher [{idx}] = {c_val}")
            for attempt in range(1, 4):
                raw = self._prompt(f"  [s] score  [x] exit   Attempt {attempt}/3 → m = ")
                if raw == str(correct_m):
                    pts = self._award(attempt)
                    self.score += pts
                    word = number_to_block(correct_m)
                    print(f"  Correct! +{pts} pts  →  decoded: {word}")
                    break
                print("  Not quite. Check pow(c, d, n).")
            else:
                word = number_to_block(correct_m)
                print(f"  Answer was: {correct_m}  ({word})")
            print()

        self.show_score()

    #  game over 
    def game_over(self):
        """Print final score/rank and return True if player wants to replay."""
        self.banner("MISSION COMPLETE")
        print(f"\n  Final score : {self.score} / {MAX_SCORE} points")
        print(f"  Your rank   : {self.rank()}")
        print()

        while True:
            raw = input("  [1] Play Again    [2] Exit\n  Choice: ").strip()
            if raw == '1':
                return True
            if raw == '2':
                print("\n  Thank you for serving UITM Spy Academy.\n")
                return False
            print("  Enter 1 or 2.")

    # Game looping
    def run(self):
        self.show_briefing()
        while True:
            self.score = 0
            self.level_1()
            self.level_2()
            self.level_3()
            self.level_4()
            if not self.game_over():
                break
