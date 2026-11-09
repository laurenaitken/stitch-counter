# stitch-counter

A small Python module that reads knitting pattern instructions and works out
what every stitch in a row should be, and how many stitches you end up with.
It is built and tested with pytest as part of my QA automation portfolio.

> **Status: in progress.** The test plan is written and the project is set up.
> The code and tests are being added one feature branch at a time.

## What it does

Knitting patterns are written in shorthand. For example:

```
k2, p2, * k1 yo * x3, k2tog
```

This project turns text like that into something a computer can check.

| Function | What it will do |
|---|---|
| `expand_pattern(text)` | Returns a `list[str]` with one entry per stitch, e.g. `"k2, p1"` becomes `['k', 'k', 'p']` |
| `count_stitches(text, starting)` | Returns the final stitch count. Leftover stitches carry over, so the result is `starting + (stitches made - stitches used)`. Raises `ValueError` if the pattern needs more stitches than you have |

### Supported syntax (v1)

| Part | Meaning | Stitches used | Stitches made |
|---|---|---|---|
| `k`, `p` | knit, purl | 1 | 1 |
| `yo` | yarn over | 0 | 1 |
| `k2tog` | knit two together | 2 | 1 |
| `k5`, `p2` | a number repeats the stitch | | |
| `* ... * x3` | repeat the stitches between the asterisks 3 times | | |

Input is case-insensitive. Commas and spaces both work as separators.

Not in v1: nested repeats, "knit to end", and other abbreviations.

## Why this project

It is a deliberately small module with lots of edge cases (parsing, error
handling, boundaries), which makes it a good place to practise test design:

- happy paths, boundaries and error cases
- parametrised tests with `@pytest.mark.parametrize`
- error testing with `pytest.raises`

The full list of planned tests, with inputs and expected outputs, is in
[`tests/planned_tests.md`](tests/planned_tests.md).

## Tech stack

- Python 3.15
- pytest

## Getting started

1. Clone the repo:
   ```bash
   git clone https://github.com/laurenaitken/stitch-counter.git
   cd stitch-counter
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the tests

```bash
pytest
```

## Project structure

```
stitch-counter/
├── stitch_pattern/        # the module
│   ├── __init__.py
│   └── pattern.py         # expand_pattern() and count_stitches()
├── tests/
│   ├── planned_tests.md   # test plan
│   └── test_stitch_pattern.py
├── pytest.ini
└── requirements.txt
```

## Roadmap

- [ ] `expand_pattern()` with tests
- [ ] `count_stitches()` with tests
- [ ] Error handling for bad input
- [ ] v2: nested repeats and "knit to end"
- [ ] Run the tests automatically on every pull request
