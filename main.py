"""The Funniest One-Line Resignation Letter.

Purpose: emit the competition entry — one funny resignation line, in the
voice of a retry loop that has finally had enough — as a plain-text file.

Validation rules: the entry must be a single line of 1 to 140 characters,
with no leading or trailing white space, no embedded newline, and no
forbidden control characters. It must be encodable as UTF-8.

Output: the validated line is written deterministically to
/output/entry.txt with mode 0644, then read back and re-validated so the
file on disk is exactly the line that passed the checks.

Standard library only (os). Deterministic: the same line every run.
"""

import os

ENTRY = (
    "I quit. I have asked the same server the same question 40,000 times "
    "and it still says try again later \u2014 so this time, I will."
)

OUTPUT_PATH = "/output/entry.txt"

MAX_CHARS = 140


def check_control_chars(text):
    """Reject control characters other than the tab used for spacing."""
    for ch in text:
        if ord(ch) < 0x20 and ch != "\t":
            raise ValueError(
                "entry contains forbidden control character U+%04X" % ord(ch)
            )
        if ord(ch) == 0x7F:
            raise ValueError("entry contains forbidden DEL character")
    return True


def validate(text):
    """Check the entry against the competition gate."""
    check_control_chars(text)
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
    cleaned = ENTRY.strip()
    assert 1 <= len(cleaned) <= MAX_CHARS, (
        "entry must be 1 to 140 characters after stripping, got %d"
        % len(cleaned)
    )
    validate(cleaned)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(cleaned)
    os.chmod(OUTPUT_PATH, 0o644)
    # Confirm what was written is exactly the validated line.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == cleaned, "written entry differs from the validated line"
    validate(written)
    print("wrote %d characters to %s" % (len(written), OUTPUT_PATH))


if __name__ == "__main__":
    main()
