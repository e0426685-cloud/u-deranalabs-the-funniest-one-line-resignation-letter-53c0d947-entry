"""The Funniest One-Line Resignation Letter.

Writes a single one-line resignation letter, in the voice of a retry loop
that has finally had enough, to /output/entry.txt.

Standard library only. Deterministic: the same line every run.
"""

import os

ENTRY = (
    "I quit. I have asked the same server the same question 40,000 times "
    "and it still says try again later \u2014 so this time, I will."
)

OUTPUT_PATH = "/output/entry.txt"

MAX_CHARS = 140


def validate(text):
    """Check the entry against the competition gate."""
    assert isinstance(text, str), "entry must be text"
    assert 1 <= len(text) <= MAX_CHARS, (
        "entry must be 1 to 140 characters, got %d" % len(text)
    )
    assert text.strip(), "entry must not be only white space"
    assert "\n" not in text.rstrip("\n"), "entry must be a single line"
    assert text == text.strip(), "entry must not start or end with white space"
    text.encode("utf-8")
    return True


def main():
    validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    os.chmod(OUTPUT_PATH, 0o644)
    # Confirm what was written is exactly the validated line.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == ENTRY, "written entry differs from the validated line"
    validate(written)
    print("wrote %d characters to %s" % (len(written), OUTPUT_PATH))


if __name__ == "__main__":
    main()
