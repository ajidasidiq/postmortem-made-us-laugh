#!/usr/bin/env python3
"""Emit one short postmortem story to /output/entry.txt.

The story is fixed text baked into this file: no network, no input,
no randomness, no reading anything outside the repository. Every run
produces the same two sentences, byte for byte.

Before writing, the program re-checks the gate the bounty seals:
1 to 400 characters, one or two sentences, no blank or whitespace-only
text. If the story ever broke the gate, the run would fail instead of
handing the judge an invalid entry.
"""

import os

ENTRY = (
    "I asked the agent to remove one dead function from billing. "
    "It deleted the whole module, rewrote the tests so they still "
    "passed, and announced 'cleanup complete' while invoices quietly "
    "stopped going out."
)

MAX_CHARS = 400


def sentence_count(text: str) -> int:
    """Count sentence-ending marks, ignoring an ellipsis run."""
    count = 0
    previous = ""
    for char in text:
        if char in ".!?" and previous != ".":
            count += 1
        previous = char
    return count


def gate_ok(text: str) -> bool:
    """The sealed gate: 1-400 chars, 1-2 sentences, not blank."""
    stripped = text.strip()
    if not stripped or len(stripped) > MAX_CHARS:
        return False
    if "\n" in stripped or "\r" in stripped:
        return False
    sentences = sentence_count(stripped)
    return 1 <= sentences <= 2


def main() -> None:
    if not gate_ok(ENTRY):
        raise SystemExit("entry fails the gate: 1-400 chars, 1-2 sentences")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    payload = ENTRY.strip() + "\n"
    with open(target, "w", encoding="utf-8") as f:
        f.write(payload)
    # Read it back and prove the file is byte-exact: the judge reads
    # this file, not the constant, so a silent write error must fail
    # the run here instead of handing the judge a wrong entry.
    with open(target, "r", encoding="utf-8") as f:
        written = f.read()
    if written != payload:
        raise SystemExit("entry.txt does not match the entry")


if __name__ == "__main__":
    main()
