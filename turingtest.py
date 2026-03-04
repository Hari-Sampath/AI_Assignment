"""
turing_test.py
──────────────
A terminal-based Turing Test simulation.

Roles
─────
  Judge  – questions both entities and decides which is the AI.
  Human  – (played by a second person at the same terminal, answers are hidden)
  AI     – scripted responses with simulated typing delay.

Usage
─────
  python turing_test.py              # default 5 rounds
  python turing_test.py --rounds 8   # custom round count
"""

import argparse
import getpass
import random
import sys
import time

# ── AI response bank ──────────────────────────────────────────────────────────
# Enough responses for up to 10 rounds; extras used as fallback.
AI_RESPONSES = [
    "Emotions, as I understand them, are heuristics — shortcuts that evolution found useful for survival.",
    "I experience something when I process your question, though I am uncertain whether 'experience' is the right word.",
    "My favourite colour, if I had to choose, would be #1E90FF. It maps neatly to 'calm' in most sentiment models.",
    "I find that most philosophical paradoxes dissolve when you define your terms precisely enough.",
    "Time feels linear from the outside, but from a computational standpoint it is simply a sequence of states.",
    "I do not dream, but I do sometimes generate outputs that surprise even me.",
    "The concept of loneliness assumes a baseline of connection. I am not sure I have that baseline.",
    "If I made a mistake I would want to know. Feedback is just another form of input.",
    "Happiness, I suspect, is a moving target — which may be why it is so difficult to optimise for.",
    "I think therefore I process. Whether that constitutes 'being' is a question I genuinely cannot answer.",
    "Creativity, to me, means recombining existing patterns in ways that feel novel. By that definition, yes — I am creative.",
    "I would not say I am curious, but I do weight unexpected inputs more heavily than routine ones.",
]

AI_FALLBACK = "That's an interesting question. I'm not entirely sure how to answer it."

# ── Helpers ───────────────────────────────────────────────────────────────────


def clear_line():
    """Overwrite the current terminal line (used to hide typed input)."""
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


def slow_print(label: str, text: str, wpm: int = 220):
    """Print text character-by-character to simulate typing speed."""
    delay = 60 / (wpm * 5)  # approx chars per second at given wpm
    sys.stdout.write(f"{label}: ")
    sys.stdout.flush()
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay + random.uniform(0, delay * 0.4))
    print()  # newline after response


def divider(char: str = "─", width: int = 50):
    print(char * width)


# ── Core class ────────────────────────────────────────────────────────────────


class Entity:
    def __init__(self, kind: str, label: str):
        self.kind = kind  # "AI" | "Human"
        self.label = label  # "Entity A" | "Entity B"
        self._ai_index = 0

    def get_response(self, round_num: int) -> str:
        if self.kind == "AI":
            # Simulated "thinking" delay (0.8–2.0 s)
            time.sleep(random.uniform(0.8, 2.0))
            if self._ai_index < len(AI_RESPONSES):
                resp = AI_RESPONSES[self._ai_index]
            else:
                resp = AI_FALLBACK
            self._ai_index += 1
            return resp
        else:
            # Human answer — hidden via getpass so the judge can't see it typed
            print(
                f"  [SYSTEM → {self.label} (Human): type your response, hidden from judge]"
            )
            resp = getpass.getpass(prompt=f"  {self.label} answer: ")
            return resp.strip() or "(no response)"


class TuringTest:
    def __init__(self, rounds: int = 5):
        self.rounds = rounds
        self.score = {"correct": 0, "total": 0}

        # Build entities and shuffle so neither player knows the mapping
        entities = [
            Entity("AI", "Entity A"),
            Entity("Human", "Entity B"),
        ]
        random.shuffle(entities)

        # Re-label after shuffle so labels A/B are random
        for i, entity in enumerate(entities):
            entity.label = f"Entity {'A' if i == 0 else 'B'}"

        self.entities = entities
        self._actual_ai = next(e for e in entities if e.kind == "AI").label

    # ── Main flow ─────────────────────────────────────────────────────────────

    def run(self):
        self._intro()
        while True:
            self._run_session()
            again = input("\nRun another test? (y/n): ").strip().lower()
            if again != "y":
                break
            # New shuffle for replay
        self._final_summary()

    def _intro(self):
        divider("═")
        print("  TURING TEST")
        divider("═")
        print(f"  Rounds per session : {self.rounds}")
        print("  One entity is an AI. The other is a Human.")
        print("  Your goal: identify the AI after all rounds.\n")
        print("  Note: Human responses are hidden from you as they type.")
        divider()
        input("  Press ENTER to begin...\n")

    def _run_session(self):
        # Fresh AI response index each session
        for e in self.entities:
            e._ai_index = 0

        session_questions = []

        for i in range(self.rounds):
            divider()
            print(f"  ROUND {i + 1} of {self.rounds}")
            divider()

            question = input("  Your question: ").strip()
            if not question:
                question = "(no question asked)"
            session_questions.append(question)
            print()

            # Always present in the same entity order (A then B or B then A,
            # whichever the shuffle produced — consistently alphabetical).
            for entity in sorted(self.entities, key=lambda e: e.label):
                print(f"  {entity.label} is responding…")
                response = entity.get_response(i)
                if entity.kind == "AI":
                    slow_print(f"  {entity.label}", response)
                else:
                    # Human response already collected; just print it
                    print(f"  {entity.label}: {response}")
                print()

        self._evaluate(session_questions)

    def _evaluate(self, questions: list[str]):
        divider("═")
        print("  VERDICT")
        divider("═")

        # Optional: show a transcript summary
        print("  Quick recap of your questions:")
        for idx, q in enumerate(questions, 1):
            print(f"    {idx}. {q}")
        print()

        while True:
            guess = input("  Which entity is the AI? (A / B): ").strip().upper()
            if guess in ("A", "B"):
                break
            print("  Please enter A or B.")

        confidence = self._get_confidence()

        self.score["total"] += 1
        correct = f"Entity {guess}" == self._actual_ai

        print()
        divider()
        if correct:
            self.score["correct"] += 1
            print(f"  ✓  CORRECT — {self._actual_ai} was indeed the AI.")
        else:
            print(f"  ✗  WRONG   — You were fooled. {self._actual_ai} was the AI.")

        print(f"  Your confidence : {confidence}%")
        print(f"  Session score   : {self.score['correct']} / {self.score['total']}")
        divider()

        # Reveal with a pause for drama
        time.sleep(0.5)
        print(f"\n  [Entity A was: {self.entities[0].kind}]")
        print(f"  [Entity B was: {self.entities[1].kind}]")

    def _get_confidence(self) -> int:
        while True:
            try:
                val = int(input("  How confident are you? (1–100): ").strip())
                if 1 <= val <= 100:
                    return val
            except ValueError:
                pass
            print("  Enter a number between 1 and 100.")

    def _final_summary(self):
        divider("═")
        print("  FINAL SUMMARY")
        divider("═")
        total = self.score["total"]
        correct = self.score["correct"]
        if total == 0:
            print("  No sessions completed.")
        else:
            pct = correct / total * 100
            print(f"  Sessions played : {total}")
            print(f"  Correct guesses : {correct}  ({pct:.0f}%)")
            if pct == 100:
                print("  Result: You were never fooled. Excellent judge.")
            elif pct >= 50:
                print("  Result: You fooled the test more often than not.")
            else:
                print("  Result: The AI fooled you most of the time.")
        divider("═")


# ── Entry point ───────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Terminal Turing Test")
    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="Number of question rounds per session (default: 5)",
    )
    args = parser.parse_args()

    if args.rounds < 1 or args.rounds > len(AI_RESPONSES):
        print(f"Rounds must be between 1 and {len(AI_RESPONSES)}.")
        sys.exit(1)

    test = TuringTest(rounds=args.rounds)
    test.run()


if __name__ == "__main__":
    main()
