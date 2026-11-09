# Planned functions

## expand_pattern(text)
Returns list[str] that tells a user what each individual stitch in a row should be.

## count_stitches(text, starting)
Returns an int of the final stitch count after completing a row and raises an error if a user runs out of stitches. Leftover stitches are carried over, so starting stitch is added to (stitches made - stitches used).

# Tests

## Test 1
Happy path: expand_pattern() returns a list of strings for a basic pattern

Input: "k1, p1, k1, p1"
Expected output: ['k', 'p', 'k', 'p']

## Test 2
Happy path: count_stitches() returns the correct number of stitches

Input: "k p k p", starting=4
Expected output: 4

## Test 3
Edge case: empty pattern returns an error

Input: "" or " "
Expected output: ValueError("Pattern empty")

## Test 4
Edge case: "k2tog" when starting with 1 stitch throws an error

Input: "k2tog", starting=1
Output: ValueError("Not enough stitches to complete pattern")

## Test 5
Boundary case: "k2tog" on 2 stitches

Input: "k2tog", starting=2
Output: 1

## Test 6
Edge case: Throw an error message for anything x0

Input: "* k2 p3 * x0"
Expected output: ValueError("Cannot multiply repeats by 0")

## Test 7
Edge case: Throw an error message for no closing *

Input: "* k5 p3"
Expected output: ValueError("No closing asterisk")

## Test 8
Edge case: check capitalisation of stitch abbreviations

Inputs: "K3 P2" | "K3 p2" | "k3 P2" (all case combinations are accepted)
expand_pattern() expected output: ['k', 'k', 'k', 'p', 'p']
count_stitches() with starting=5 expected output: 5

## Test 9
Happy path: expand_pattern() returns list of strings for counted abbreviation

Input: "k5, p2"
Expected output: ['k', 'k', 'k', 'k', 'k', 'p', 'p']

## Test 10
Happy path: expand_pattern() returns list of strings for repeats (**)

Input: "k2 p2 * k1 p1 * x3"
Expected output: ['k', 'k', 'p', 'p', 'k', 'p', 'k', 'p', 'k', 'p']

## Test 11
Happy path: count_stitches() returns correct number of stitches for complex pattern (repeats and complex stitches like 'k2tog')

Input: "k1 p1 k2tog * k2 p1 * x4 k1 p1", starting=18
Expected output: 17

## Test 12
Edge case: unknown abbreviation

Input: "k2, p1, z3"
Expected output: ValueError("Unknown abbreviation")

## Test 13
Edge case: invalid counts

Inputs: "k2, p-1" | "k2, k1.5" | "k0" | "* k1 * xabc" | "* k1 *" (repeat with no count)
Expected output: ValueError("Invalid count")

## Test 14
Edge case: bad asterisk

Inputs: "k2 ** p1 k2 k3" | "k2 * * x2" (empty repeats)
Expected output: ValueError("Bad asterisk")

## Test 15
Edge case: messy inputs

Inputs: "k1,p1" | "k1 , p1" | "k1, p1," | "k1,, p1"
Expected outputs: ['k', 'p']

## Test 16
Happy path: 'yo' is accepted

Input: "yo k5", starting=5
Expected output: 6

## Test 17
Edge case: repeat pushes usage over limit

Input: "*k2* x3", starting=5
Expected output: ValueError("Not enough stitches to complete pattern")

## Test 18
Edge case: Invalid starting value

Inputs: "k1 p1", starting=-1 | "k1 p1", starting="abc" | "k1 p1", starting=2.5
Expected output: ValueError("Invalid starting value")

## Test 19
Edge case: spacing around asterisks is flexible

Inputs: "*k1 p1* x2" | "* k1 p1 * x2" | "*k1 p1 * x2"
Expected output: ['k', 'p', 'k', 'p']

## Test 20
Boundary case: starting with 0 stitches

Input: "yo", starting=0
Expected output: 1

Input: "k1", starting=0
Expected output: ValueError("Not enough stitches to complete pattern")

# Parametrised Tests

## expand_pattern(): input to expected list
Tests: 1, 8 (expand), 9, 10, 15, 19

## expand_pattern(): input to ValueError
Tests: 3, 6, 7, 12, 13, 14

## count_stitches(): (text, starting) to expected int
Tests: 2, 5, 8 (count), 11, 16, 20 (yo on 0 stitches)

## count_stitches(): (text, starting) to ValueError
Tests: 4, 17, 18, 20 (k1 on 0 stitches)