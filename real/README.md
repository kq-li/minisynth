# CS 6120 L12

Kenneth Li (kql3)

## Overview

In `real.py`, I extended Minisynth with real number support, specifically for the task of solving polynomial equations with Z3. I just modified the parser and interpreter to support `**` (unfortunately, I had to remove bit shifting, which is not defined on reals). The example sketches in `real_sketches/` show how to compute roots and solve equations with the language syntax -- mostly involving use of the fundamental theorem of algebra and/or some educated guessing about the structure of the factored form. For example, `s2-bad.txt` tries to factor a polynomial with only one real root into three monomials, and Z3 can't solve this (and it shouldn't!). Once the polynomial's factoring is written in the correct form, as in `s2-good.txt`, Z3 solves it immediately.

### Observations

It seems that upon moving to real numbers, it's really easy to ask Z3 a question that it can't answer. Simply adding a leading coefficient hole, like in `s3-bad.txt`, causes Z3 to take a long time, but including that coefficient inside one of the factors, as we do in `s3-good.txt`, instantly resolves this. Also, `s4.txt`, which asks Z3 to find the roots of a degree 5 polynomial, caused Z3 to hang on my machine.

### Extension

This implementation had a hard time solving higher-order polynomials, but Z3 actually does a really good job finding single roots. I took advantage of this in `poly.py` to find one root, divide it out using polynomial long division, and iterate until irreducible; this is significantly more effective than the previous strategy, finding roots with ease (at the cost of slight precision loss). Parsing proved quite annoying for this, though, so I resorted to a simple "polynomial = list" representation for simplicity. Sketches for the extension live in `poly_sketches/`.
