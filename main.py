"""One Word, First Thought.

A deterministic first-thought word picker. The bounty asks for exactly one
word -- the first word that comes to mind, with no topic, no explanation and
no second draft -- and a judge then compares words two at a time on surprise,
vividness, a spark of wit, and specificity.

This program models that first thought as a single pass over a small lexicon
of candidate words. Each candidate carries fixed scores (0-10) for the four
qualities the judge weighs, in the judge's own order of importance:

    surprise    -- a word a reader would not have guessed
    vividness   -- calls up a clear image or feeling
    wit         -- sound or double meaning that rewards a second look
    specificity -- chosen rather than generic, never filler

The weighted total picks one word. There is no randomness, no clock, no
network and no second draft: the same run always writes the same word, so
repeated runs are byte-identical.

Usage:
    python3 main.py            # writes /output/entry.txt
"""

import os

# (word, surprise, vividness, wit, specificity), in first-thought order.
# The scores are the program's own fixed judgement of each candidate.
CANDIDATES = [
    ("petrichor", 8, 10, 7, 9),
    ("vellichor", 9, 9, 6, 9),
    ("sonder", 7, 8, 6, 8),
    ("syzygy", 9, 6, 8, 8),
    ("apricity", 8, 8, 5, 8),
    ("defenestration", 7, 9, 8, 8),
    ("limerence", 7, 7, 5, 8),
    ("quixotic", 6, 7, 7, 6),
    ("serendipity", 4, 6, 5, 6),
    ("ephemeral", 5, 7, 5, 6),
]

# The judge weighs the qualities most important first: surprise and
# vividness above wit and specificity.
WEIGHTS = (3, 3, 2, 2)

OUTPUT_PATH = "/output/entry.txt"


def score(candidate):
    """Weighted total of one candidate's four quality scores."""
    _, surprise, vividness, wit, specificity = candidate
    qualities = (surprise, vividness, wit, specificity)
    return sum(w * q for w, q in zip(WEIGHTS, qualities))


def first_thought(candidates):
    """The highest-scoring word; ties go to the word thought of first."""
    best = None
    best_score = -1
    for candidate in candidates:
        total = score(candidate)
        if total > best_score:
            best = candidate[0]
            best_score = total
    return best, best_score


def gate(word):
    """The bounty gate: UTF-8 text of 1 to 24 characters, not only
    whitespace, and exactly one word."""
    if not isinstance(word, str):
        return False
    if not 1 <= len(word) <= 24:
        return False
    if not word.strip():
        return False
    if len(word.split()) != 1:
        return False
    return True


def verify_output(path, word):
    """Read the written file back and confirm it holds exactly the chosen
    word and still passes the gate: a program that cannot prove its own
    output is not finished."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != word:
        raise SystemExit("output mismatch: wrote %r, read back %r"
                         % (word, written))
    if not gate(written):
        raise SystemExit("written output fails the gate: %r" % (written,))
    return written


def main():
    word, total = first_thought(CANDIDATES)
    if not gate(word):
        raise SystemExit("chosen word fails the gate: %r" % (word,))
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(word)
    verify_output(OUTPUT_PATH, word)
    print(word)
    print("score: %d" % total)


if __name__ == "__main__":
    main()
