"""Expand knitting pattern text into one list entry per stitch.

Supported syntax:
    - Stitch abbreviations: ``k`` (knit), ``p`` (purl), ``yo`` (yarn over) and
      ``k2tog`` (knit two together).
    - A number after a stitch repeats it, so ``k5`` means five knit stitches.
      A stitch with no number counts once.
    - ``* ... * xN`` repeats the stitches between the asterisks N times.
    - Commas and spaces both work as separators, and input is not case
      sensitive.
"""

import re

KNOWN_STITCHES = ("k", "p", "yo", "k2tog")
REPEAT_MARKER = "*"
REPEAT_COUNT = "x"

# Longest names first, so "k2tog" is matched before "k" reads it as "k2".
_STITCH_NAMES = "|".join(sorted(KNOWN_STITCHES, key=len, reverse=True))
_STITCH_PATTERN = re.compile(rf"({_STITCH_NAMES})([0-9]*)")
_REPEAT_COUNT_PATTERN = re.compile(rf"{REPEAT_COUNT}([0-9]+)")


def parse_pattern(text):
    """Split pattern text into a list of ``(name, count)`` tokens.

    Args:
        text (str): The original pattern text, for example ``"K2, p1"``.

    Returns:
        list[tuple[str, int]]: One token per instruction, in the order they
        appear, with lowercase names:

        - a stitch is ``(name, count)``, for example ``('k', 2)``. A stitch
          with no number has a count of 1.
        - a repeat marker is ``('*', 1)``.
        - a repeat count such as ``x3`` is ``('x', 3)``.

    Raises:
        ValueError: 
            1. Instruction is not a known stitch, repeat marker or
            repeat count
            2. Empty pattern text is entered
            3. Empty repeat
            4. Invalid stitch/repeat count
            5. Repeat count multiplied by 0
            6. Unclosed asterisks
    """
    if text == "" or text == " ":
        raise ValueError("Pattern empty")
    normalised = text.lower().replace(REPEAT_MARKER, f" {REPEAT_MARKER} ")
    normalised = normalised.replace(",", " ")

    tokens = []
    for piece in normalised.split():
        if piece == REPEAT_MARKER:
            tokens.append((REPEAT_MARKER, 1))
            continue

        repeat_count = _REPEAT_COUNT_PATTERN.fullmatch(piece)
        if repeat_count:
            if int(repeat_count.group(1)) == 0:
                raise ValueError("Cannot repeat by 0")
            tokens.append((REPEAT_COUNT, int(repeat_count.group(1))))
            continue

        stitch = _STITCH_PATTERN.fullmatch(piece)
        if stitch is None:
            if any(piece.startswith(name) for name in KNOWN_STITCHES):
                raise ValueError("Invalid count")
            else:
                raise ValueError(f"Unknown abbreviation: {piece!r}")
        name, digits = stitch.groups()
        if digits and int(digits) == 0:
            raise ValueError("Invalid count")
        tokens.append((name, int(digits) if digits else 1))

    return tokens


def expand_pattern(text):
    """Turn pattern text into a flat list with one entry per stitch.

    Args:
        text (str): A pattern such as ``"k2, * p1 k1 * x3"``. Commas and
            spaces both work as separators, and input is not case sensitive.

    Returns:
        list[str]: One entry per stitch, in knitting order. ``'k2tog'`` counts
        as a single entry, not two stitches.

    Raises:
        ValueError: If the text contains an unknown abbreviation, or a repeat
            count (``x3``) with no repeat before it.

    Example:
        >>> expand_pattern("k5, p2")
        ['k', 'k', 'k', 'k', 'k', 'p', 'p']
    """
    stitches = []
    repeat_group = None
    inside_repeat = False

    for name, count in parse_pattern(text):
        if name == REPEAT_MARKER:
            inside_repeat = not inside_repeat
            if inside_repeat:
                repeat_group = []
            else:
                if len(repeat_group) == 0:
                    raise ValueError("Empty repeat")
        elif name == REPEAT_COUNT:
            if repeat_group is None:
                raise ValueError(f"Repeat count x{count} has no repeat before it")
            stitches.extend(repeat_group * count)
        else:
            target = repeat_group if inside_repeat else stitches
            target.extend([name] * count)
    if inside_repeat:
        raise ValueError("Missing opening/closing asterisk")

    return stitches
