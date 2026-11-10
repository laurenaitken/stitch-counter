"""Tests for expand_pattern()."""

import pytest

from stitch_pattern.pattern import expand_pattern


@pytest.mark.parametrize(
    "text, expected",
    [
        ("k1, p1, k1, p1", ['k', 'p', 'k', 'p']),
        ("k5, p2", ['k', 'k', 'k', 'k', 'k', 'p', 'p']),
        ("k2 p2 * k1 p1 * x3", ['k', 'k', 'p', 'p', 'k', 'p', 'k', 'p', 'k', 'p']),
        ("k2 p2 * k1 p1 * x3 k1", ['k', 'k', 'p', 'p', 'k', 'p', 'k', 'p', 'k', 'p', 'k']),
        ("* k1 * x2 * p1 * x2", ['k', 'k', 'p', 'p']),
        ("k p k p", ['k', 'p', 'k', 'p']),
        ("k10", ['k'] * 10),
        ("yo k2", ['yo', 'k', 'k']),
        ("k2tog", ['k2tog']),
        ("* k2tog p1 * x2", ['k2tog', 'p', 'k2tog', 'p']),
    ],
    ids=[
        "basic",
        "counted",
        "repeat",
        "repeat-then-stitch",
        "two-repeats",
        "no-counts",
        "two-digit-count",
        "yarn-over",
        "k2tog-single-entry",
        "k2tog-in-repeat",
    ],
)
def test_expand_pattern_returns_stitch_list(text, expected):
    """Valid patterns expand to one list entry per stitch."""
    assert expand_pattern(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("K3 P2", ['k', 'k', 'k', 'p', 'p']),
        ("K3 p2", ['k', 'k', 'k', 'p', 'p']),
        ("k3 P2", ['k', 'k', 'k', 'p', 'p']),
        ("K2TOG", ['k2tog']),
        ("YO", ['yo']),
    ],
    ids=["upper-both", "upper-first", "upper-second", "upper-k2tog", "upper-yo"],
)
def test_expand_pattern_ignores_case(text, expected):
    """Upper and lower case abbreviations give the same result."""
    assert expand_pattern(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("k1,p1", ['k', 'p']),
        ("k1 , p1", ['k', 'p']),
        ("k1, p1,", ['k', 'p']),
        ("k1,, p1", ['k', 'p']),
        ("k1   p1", ['k', 'p']),
        ("k2, * k1 p1 * x2", ['k', 'k', 'k', 'p', 'k', 'p']),
    ],
    ids=[
        "no-space-after-comma",
        "space-before-comma",
        "trailing-comma",
        "double-comma",
        "extra-spaces",
        "commas-and-spaces-mixed",
    ],
)
def test_expand_pattern_accepts_messy_separators(text, expected):
    """Commas, spaces and mixtures of both all separate instructions."""
    assert expand_pattern(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "*k1 p1* x2",
        "* k1 p1 * x2",
        "*k1 p1 * x2",
    ],
    ids=["tight", "spaced", "mixed"],
)
def test_expand_pattern_accepts_flexible_asterisk_spacing(text):
    """Spaces around the asterisks do not change the result."""
    assert expand_pattern(text) == ['k', 'p', 'k', 'p']


@pytest.mark.parametrize(
    "text, message",
    [
        ("k2, p1, z3", "Unknown abbreviation"),
        ("k2 x3", "no repeat"),
    ],
    ids=["unknown-abbreviation", "count-without-repeat"],
)
def test_expand_pattern_rejects_unusable_text(text, message):
    """Text that cannot be expanded raises a ValueError with a clear message."""
    with pytest.raises(ValueError, match=message):
        expand_pattern(text)
