"""Expand knitting pattern text into one list entry per stitch.

Supported syntax:
    - Stitch abbreviations: ``k`` (knit), ``p`` (purl) and ``k2tog``
      (knit two together).
    - A number after a stitch repeats it, so ``k5`` means five knit stitches.
    - ``* ... * xN`` repeats the stitches between the asterisks N times.
    - Commas and spaces both work as separators, and input is not case
      sensitive.
"""


def parse_pattern(text):
    """Split pattern text into a list of cleaned instructions.

    Args:
        text (str): The original pattern text, for example ``"K2, p1"``.

    Returns:
        list: One item per instruction, in the order they appear. Repeat
        markers (``'*'``) and ``'k2tog'`` are plain strings. Every other
        instruction is a ``(name, count)`` tuple with a lowercase name, for
        example ``('k', 2)``. A repeat count such as ``x3`` is the tuple
        ``('x', 3)``.
    """
    text = text.replace("*", " * ")
    if ',' not in text:
        split_text = text.split()
    else:
        split_text = text.split(',')

    stitch_tuples = []
    for instruction in split_text:
        instruction = instruction.strip()
        if instruction in ['*', 'k2tog']:
            stitch_tuples.append(instruction)
        else:
            stitch_tuples.append((instruction[0].lower(), int(instruction[1])))

    return stitch_tuples


def expand_pattern(text):
    """Turn pattern text into a flat list with one entry per stitch.

    Args:
        text (str): A pattern such as ``"k2, * p1 k1 * x3"``. Commas and
            spaces both work as separators, and input is not case sensitive.

    Returns:
        list[str]: One entry per stitch, in knitting order. ``'k2tog'`` counts
        as a single entry, not two stitches.

    Example:
        >>> expand_pattern("k5, p2")
        ['k', 'k', 'k', 'k', 'k', 'p', 'p']
    """
    stitch_tuples = parse_pattern(text)
    final_stitch_list = []
    repeat_started = False

    for stitch in stitch_tuples:
        if stitch == '*':
            if not repeat_started:
                repeat_started = True
                repeated_pattern = []

            else:
                repeat_started = False

        elif stitch[0] == 'x':
            repeated_pattern = repeated_pattern * stitch[1]
            final_stitch_list.extend(repeated_pattern)

        elif stitch == 'k2tog':
            if repeat_started:
                repeated_pattern.append(stitch)
            else:
                final_stitch_list.append(stitch)
        else:
            count = 0
            while count < stitch[1]:
                if repeat_started:
                    repeated_pattern.append(stitch[0])
                else:
                    final_stitch_list.append(stitch[0])
                count += 1

    return final_stitch_list
