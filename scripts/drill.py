"""Build a ~25-mark algebra fluency sheet and its worked answers.

Usage (from the project root, with the venv active):
    python scripts/drill.py                    # drill-YYYY-MM-DD for today
    python scripts/drill.py --date 2026-11-02  # that day's sheet
    python scripts/drill.py --seed 7 --name drill-test

Writes, with the same LaTeX templates as build_pdf.py:
    out/to-remarkable/NAME_questions.pdf   the questions, easier ones first
    out/to-remarkable/NAME_answers.pdf     worked answers (never sent to the tablet)
    out/drills/NAME.json                   the questions and answers as text

Difficulty rises week by week. The level is the number of whole weeks since
2026-10-16 (level 0 that week), capped at MAX_LEVEL. Each level widens the
number ranges, and at set levels templates change or join the sheet:
  level 1   completing the square with a ≠ 1; quadratics in disguise (x², √x);
            adding and subtracting algebraic fractions
  level 2   discriminant / range-of-k problems; quadratics in eˣ; brackets
            in linear inequalities; negative x² coefficients in quadratic
            inequalities; the two easiest templates retire
  level 3   surd-form answers to quadratics; fractional p when completing
            the square; harder algebraic fractions; more templates retire
From 2026-11-15, A-level algebra joins too (partial fractions, modulus,
composite and inverse functions, binomial expansion with negative and
fractional n, rational expressions): two or three A-level questions a day
mixed in with the AS ones. Their level counts weeks from 2026-11-15.

Every template available at the current level appears at least once in any
7 days. The draw reads the previous six days' daily records in out/drills/:
a template not on any of them (and available all that time) must go on
today's sheet, and the rest of the sheet is filled with the least recently
used templates, ties broken at random with harder ones more likely at
higher levels, until it has 24-27 marks. A day with no sheet counts as a day
the template didn't appear. The sheet lists its questions easiest first. Numbers are chosen so answers come out clean (integers, small
fractions, simple surds), and SymPy works out or checks every answer, so an
answer can't disagree with its question. The seed defaults to the date, so
rebuilding a day's sheet gives the same questions.
"""

import argparse
import json
import re
import random
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Callable

import sympy as sp

import build_pdf
from paths import OUT_DIR, ensure_out_dir

x, y, k = sp.symbols("x y k")

START = date(2026, 10, 16)
ALEVEL_START = date(2026, 11, 15)
MAX_LEVEL = 6
MIN_MARKS, MAX_MARKS = 24, 27
WINDOW = 7  # every available template appears at least once in any WINDOW days


def weeks_since(start, day):
    return max(0, (day - start).days // 7)


def level_for(day):
    """AS level: whole weeks since START, capped at MAX_LEVEL."""
    return min(MAX_LEVEL, weeks_since(START, day))


def alevel_level_for(day):
    """A-level level, or None before ALEVEL_START."""
    return None if day < ALEVEL_START else min(MAX_LEVEL, weeks_since(ALEVEL_START, day))


# ---------------------------------------------------------------- helpers

def tex(expr):
    """LaTeX for a SymPy expression, highest power first."""
    expr = sp.sympify(expr)
    text = sp.latex(expr, order="lex" if expr.free_symbols - {x} else None, ln_notation=True)
    # \ln{\left(8 \right)} -> \ln 8
    return re.sub(r"\\ln{\\left\((\d+) \\right\)}", r"\\ln \1", text)


def ordered(coef, const, var):
    """coef·var + const, positive term first: '3y + 5', 'y - 8', '8 - 3k'."""
    if coef > 0:
        return lin(coef, const, var)
    return f"{const} {term(coef, var)}" if const else f"-{lead(-coef)}{var}"


def poly(expr, var=x):
    """LaTeX for a polynomial, highest power first."""
    return sp.latex(sp.Poly(sp.expand(expr), var).as_expr())


def dfrac(expr):
    """LaTeX with full-size fractions, for answers that are fractions."""
    return tex(expr).replace(r"\frac", r"\dfrac")


def signed(n):
    """'+ 3' or '- 3', for writing a term after another one."""
    return f"+ {tex(n)}" if n >= 0 else f"- {tex(-n)}"


def paren(n):
    """A number to write after an operator: (-4) in brackets, 4 as is."""
    return f"({n})" if n < 0 else f"{n}"


def term(coef, var):
    """'+ 3x', '- x', '+ \\frac{1}{2}x' ... for a term after another one."""
    coef = sp.sympify(coef)
    size = "" if abs(coef) == 1 and var else tex(abs(coef))
    return f"{'+' if coef > 0 else '-'} {size}{var}"


def lead(a):
    """A leading coefficient: '' for 1, '-' for -1, else the number."""
    return {1: "", -1: "-"}.get(a, tex(a))


def lin(p, r, var="x"):
    """'px + r' with tidy signs, e.g. lin(2, -3) = '2x - 3', lin(1, 0) = 'x'."""
    return f"{lead(p)}{var}" + (f" {signed(r)}" if r else "")


def nonzero(rng, low, high):
    return rng.choice([n for n in range(low, high + 1) if n != 0])


def nice(value, max_denominator=3):
    value = sp.nsimplify(value)
    return value.is_rational and value.q <= max_denominator


def set_text(solutions, var="x"):
    """'$x < -5$ or $x > 7$' and the like, for a SymPy Interval or Union."""
    pieces = solutions.args if isinstance(solutions, sp.Union) else (solutions,)
    out = []
    for piece in sorted(pieces, key=lambda p: p.inf):
        if not isinstance(piece, sp.Interval):
            raise ValueError(f"not an interval: {piece}")
        lo, hi = piece.start, piece.end
        below = "<" if piece.left_open else r"\leqslant"
        above = "<" if piece.right_open else r"\leqslant"
        if lo == -sp.oo and hi == sp.oo:
            raise ValueError("all real numbers")
        if lo == -sp.oo:
            out.append(f"${var} {above} {tex(hi)}$")
        elif hi == sp.oo:
            out.append(f"${var} {'>' if piece.left_open else r'\geqslant'} {tex(lo)}$")
        else:
            out.append(f"${tex(lo)} {below} {var} {above} {tex(hi)}$")
    return " or ".join(out)


def interval_ends_nice(solutions, max_denominator=4):
    pieces = solutions.args if isinstance(solutions, sp.Union) else (solutions,)
    if not pieces or not all(isinstance(p, sp.Interval) for p in pieces):
        return False
    ends = [e for p in pieces for e in (p.start, p.end) if e.is_finite]
    return bool(ends) and all(nice(e, max_denominator) for e in ends)


def question(topic, marks, text, steps, answer):
    return {"topic": topic, "marks": marks, "question": text, "steps": steps, "answer": answer}


# ---------------------------------------------------------------- AS templates
# Each takes (rng, level) and returns question(...).

def surds_simplify(rng, level):
    k_ = rng.choice([2, 3, 5, 6, 7] + ([10, 11, 13] if level else []))
    p, q = rng.sample(range(2, 6 + level), 2)
    a, b = p * p * k_, q * q * k_
    total = sp.sqrt(a) + sp.sqrt(b)
    return question(
        "Surds", 1,
        f"Write $\\sqrt{{{a}}} + \\sqrt{{{b}}}$ in the form $c\\sqrt{{{k_}}}$, where $c$ is an integer.",
        [f"$\\sqrt{{{a}}} = \\sqrt{{{p * p}}}\\sqrt{{{k_}}} = {p}\\sqrt{{{k_}}}$ and "
         f"$\\sqrt{{{b}}} = \\sqrt{{{q * q}}}\\sqrt{{{k_}}} = {q}\\sqrt{{{k_}}}$"],
        f"${tex(total)}$")


def indices(rng, level):
    a = rng.choice([2, 3] + ([4, 5] if level >= 2 else []))
    n = rng.choice([2, 3])
    m = rng.randint(2, 4 + level // 2)
    root = rng.choice([2, 3]) if level >= 2 else 2
    numerator = a ** n
    divisors = [d for d in sp.divisors(numerator) if 1 < d < numerator]
    # From level 3 the coefficient may be a fraction.
    b = rng.choice(divisors + ([5, 7] if level >= 3 else []))
    xp = sp.symbols("x", positive=True)
    power = sp.Rational(m * n) - sp.Rational(1, root)
    coefficient = sp.Rational(numerator, b)
    assert sp.simplify((a * xp ** m) ** n / (b * xp ** sp.Rational(1, root)) - coefficient * xp ** power) == 0
    root_text = "\\sqrt{x}" if root == 2 else "\\sqrt[3]{x}"
    return question(
        "Indices", 2,
        f"Simplify fully $$\\frac{{({a}x^{{{m}}})^{{{n}}}}}{{{b}{root_text}}}$$\n"
        "giving your answer in the form $kx^{p}$.",
        [f"$({a}x^{{{m}}})^{{{n}}} = {numerator}x^{{{m * n}}}$ and ${root_text} = x^{{\\frac{{1}}{{{root}}}}}$",
         f"$\\dfrac{{{numerator}x^{{{m * n}}}}}{{{b}x^{{\\frac{{1}}{{{root}}}}}}} = "
         f"\\dfrac{{{numerator}}}{{{b}}}x^{{{m * n} - \\frac{{1}}{{{root}}}}}$"],
        f"${dfrac(coefficient)}x^{{{tex(power)}}}$")


def expanding(rng, level):
    span = 5 + level
    a, b = nonzero(rng, -span, span), nonzero(rng, -span, span)
    p = rng.choice([2, 3]) if level >= 2 else 1
    c, d = rng.choice([2, 3] + ([4, 5] if level else [])), nonzero(rng, -4 - level, 4 + level)
    first = sp.expand((p * x + a) * (x + b))
    full = sp.expand(first * (c * x + d))
    return question(
        "Algebraic expressions", 2,
        f"Expand and simplify $({lin(p, a)})({lin(1, b)})({lin(c, d)})$.",
        [f"$({lin(p, a)})({lin(1, b)}) = {poly(first)}$",
         f"$({poly(first)})({lin(c, d)}) = {poly(full)}$"],
        f"${poly(full)}$")


def linear_inequality(rng, level):
    # a x + b < c x + d with a - c negative half the time, so the sign flips.
    span = 7 + level
    while True:
        a, c = rng.randint(-4 - level, span), rng.randint(-4 - level, span)
        if a == c or a == 0 or c == 0:
            continue
        root = rng.randint(-6, 6)
        b = rng.randint(-12, 12)
        d = (a - c) * root + b
        if d != 0 and b != 0:
            break
    sign = rng.choice(["<", ">"])
    flip = a - c < 0
    final = {"<": ">", ">": "<"}[sign] if flip else sign
    # From level 2 the left side is in brackets when it factorises, as a(x + b/a).
    if level >= 2 and abs(a) > 1 and b % a == 0:
        left = f"{a}({lin(1, b // a)})"
        steps = [f"Expand: ${a}x {signed(b)} {sign} {c}x {signed(d)}$"]
    else:
        left = f"{a}x {signed(b)}"
        steps = []
    steps.append(f"${a - c}x {sign} {d - b}$")
    if flip:
        steps.append(f"Dividing by ${a - c}$, a negative number, reverses the inequality.")
    assert sp.solve_univariate_inequality(
        sp.sympify(f"{a}*x + {b} {sign} {c}*x + {d}"), x, relational=False) == (
        sp.Interval.open(root, sp.oo) if final == ">" else sp.Interval.open(-sp.oo, root))
    return question(
        "Inequalities", 2,
        f"Solve $${left} {sign} {c}x {signed(d)}$$",
        steps,
        f"$x {final} {root}$")


def factorising(rng, level):
    while True:
        k_ = rng.choice([1, 2, 3] + ([4, 5] if level >= 2 else []))
        p = rng.choice([1, 2, 3] + ([4, 5] if level >= 2 else []))
        q, r = nonzero(rng, -5 - level, 5 + level), nonzero(rng, -5 - level, 5 + level)
        if sp.gcd(p, q) == 1 and not (p == 1 and q == r):
            break
    # From level 3, sometimes a difference of two squares inside instead.
    if level >= 3 and rng.random() < 0.4:
        p, q = rng.choice([2, 3, 4, 5]), rng.choice([1, 3, 5, 7])
        if sp.gcd(p, q) != 1:
            q = 1
        quadratic = sp.expand((p * x - q) * (p * x + q))
    else:
        quadratic = sp.expand((p * x + q) * (x + r))
    expr = sp.expand(k_ * x * quadratic)
    common = f"{k_}x" if k_ > 1 else "x"
    return question(
        "Algebraic expressions", 2,
        f"Factorise completely $${poly(expr)}$$",
        [f"Take out the common factor ${common}$: ${common}({poly(quadratic)})$"],
        f"${tex(sp.factor(expr))}$")


def rearranging(rng, level):
    while True:
        a, b, c = nonzero(rng, 2, 6 + level), nonzero(rng, -9 - level, 9 + level), nonzero(rng, -5, 5)
        # From level 2 the x in the denominator has a coefficient too.
        d = rng.choice([2, 3, 4]) if level >= 2 else 1
        # ac + bd = 0 would make the fraction cancel down to a constant.
        if a * c + b * d != 0:
            break
    # c y + b, written with the positive term first.
    top = ordered(c, b, "y")
    bottom = f"{lead(d)}y - {a}"
    solved = sp.solve(sp.Eq(y, (a * x + b) / (d * x - c)), x)[0]
    assert sp.simplify(solved - (c * y + b) / (d * y - a)) == 0
    return question(
        "Algebraic expressions", 2,
        f"Make $x$ the subject of $$y = \\frac{{{lin(a, b)}}}{{{lin(d, -c)}}}$$",
        [f"$y({lin(d, -c)}) = {lin(a, b)}$",
         f"${lead(d)}xy {term(-c, 'y')} = {lin(a, b)}$",
         f"${lead(d)}xy - {a}x = {top}$",
         f"$x({bottom}) = {top}$"],
        f"$x = \\dfrac{{{top}}}{{{bottom}}}$")


def simultaneous_linear(rng, level):
    span = 6 + level
    while True:
        x0, y0 = nonzero(rng, -5 - level, span), nonzero(rng, -5 - level, span)
        a1, a2 = rng.randint(1, span), rng.randint(1, span)
        b1, b2 = nonzero(rng, -5 - level, span), nonzero(rng, -5 - level, span)
        if a1 * b2 - a2 * b1 != 0 and abs(b1) != abs(b2):
            break
    c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
    det = a1 * b2 - a2 * b1
    assert sp.solve([a1 * x + b1 * y - c1, a2 * x + b2 * y - c2], [x, y]) == {x: x0, y: y0}
    return question(
        "Equations", 2,
        "Solve the simultaneous equations\n"
        f"$$\\begin{{aligned}}{tex(a1 * x + b1 * y)} &= {c1}\\\\ {tex(a2 * x + b2 * y)} &= {c2}\\end{{aligned}}$$",
        [f"Multiply the first equation by ${b2}$ and the second by ${b1}$, then subtract to eliminate $y$:",
         f"$({a1 * b2} - {paren(a2 * b1)})x = {c1 * b2} - {paren(c2 * b1)}$, "
         f"so ${det}x = {c1 * b2 - c2 * b1}$ and $x = {x0}$",
         f"Substitute into the first equation: ${a1 * x0} {term(b1, 'y')} = {c1}$, so $y = {y0}$"],
        f"$x = {x0},\\ y = {y0}$")


def rationalising(rng, level):
    max_b, max_d = (5, 4) if level < 2 else (6, 6)
    n_choices = [1, 2, -1] + ([3, -2, -3] if level >= 2 else [])
    while True:
        b = rng.randint(2, max_b)
        # Square-free k, so √k is already in its simplest form.
        k_ = rng.choice([n for n in range(2, 20 + 5 * level) if all(e == 1 for e in sp.factorint(n).values())])
        d = b * b - k_
        m, n = nonzero(rng, -6 - level, 6 + level), rng.choice(n_choices)
        # (m + n√k)(b + √k) = (mb + nk) + (m + nb)√k, over b² − k.
        rational, irrational = m * b + n * k_, m + n * b
        if (d != 0 and abs(d) <= max_d and rational % d == 0 and irrational % d == 0 and irrational != 0
                and abs(rational // d) <= 20 + 5 * level and abs(irrational // d) <= 20):
            break
    s = sp.sqrt(k_)
    p, q = rational // d, irrational // d
    assert sp.simplify((m + n * s) / (b - s) - (p + q * s)) == 0
    root = f"\\sqrt{{{k_}}}"
    numerator = f"{m} {term(n, root)}"
    return question(
        "Surds", 2,
        f"Write $$\\frac{{{numerator}}}{{{b} - {root}}}$$\n"
        f"in the form $p + q{root}$, where $p$ and $q$ are integers.",
        [f"Multiply top and bottom by $({b} + {root})$.",
         f"Denominator: $({b} - {root})({b} + {root}) = {b * b} - {k_} = {d}$",
         f"Numerator: $({numerator})({b} + {root}) = {rational} {term(irrational, root)}$",
         f"$\\dfrac{{{rational} {term(irrational, root)}}}{{{d}}}$"],
        f"${p} {term(q, root)}$")


def solving_quadratic(rng, level):
    # From level 3, half the time: no factors, answers in surd form.
    if level >= 3 and rng.random() < 0.5:
        while True:
            a, b, c = rng.choice([1, 2]), nonzero(rng, -8, 8), nonzero(rng, -9, 9)
            disc = b * b - 4 * a * c
            if disc > 0 and not sp.sqrt(disc).is_rational:
                break
        # (-b ± s√t) / 2a, with any common factor of -b, s and 2a cancelled.
        s, t = sp.sqrt(disc).as_coeff_Mul()
        g = sp.gcd_list([b, s, 2 * a])
        top, root, bottom = -b // g, f"{lead(s // g)}{tex(t)}", 2 * a // g
        roots_text = f"{top} \\pm {root}" if bottom == 1 else f"\\dfrac{{{top} \\pm {root}}}{{{bottom}}}"
        mine = {sp.Rational(top, bottom) + sign * (s // g) * t / bottom for sign in (1, -1)}
        assert {sp.nsimplify(v) for v in sp.solve(a * x ** 2 + b * x + c, x)} == {sp.nsimplify(v) for v in mine}
        return question(
            "Equations", 3,
            f"Solve $${poly(a * x ** 2 + b * x + c)} = 0$$\ngiving your answers in simplest surd form.",
            ["$x = \\dfrac{-b \\pm \\sqrt{b^2 - 4ac}}{2a} = "
             f"\\dfrac{{{-b} \\pm \\sqrt{{{b * b} - {paren(4 * a * c)}}}}}{{{2 * a}}} = "
             f"\\dfrac{{{-b} \\pm \\sqrt{{{disc}}}}}{{{2 * a}}}$",
             f"$\\sqrt{{{disc}}} = {tex(sp.sqrt(disc))}$"],
            f"$x = {roots_text}$")
    span = 7 + level
    while True:
        p, q, r = rng.choice([2, 3] + ([4, 5] if level >= 2 else [])), nonzero(rng, -span, span), nonzero(rng, -6 - level, 6 + level)
        if sp.gcd(p, q) == 1:
            break
    expr = sp.expand((p * x + q) * (x + r))
    roots = sorted(sp.solve(expr, x))
    return question(
        "Equations", 2,
        f"Solve $${poly(expr)} = 0$$",
        [f"$({lin(p, q)})({lin(1, r)}) = 0$"],
        "$x = " + "$ or $x = ".join(tex(v) for v in roots) + "$")


def completing_square(rng, level):
    # Level 0: a = 1. Level 1 on: a ≠ 1. Level 3: p may be a half.
    # Level 4: a may be negative.
    if level == 0:
        a = 1
    else:
        a = rng.choice([2, 3, 4, 5] + ([-1, -2, -3] if level >= 4 else []))
    if level >= 3 and rng.random() < 0.5:
        p = sp.Rational(rng.choice([-9, -7, -5, -3, -1, 1, 3, 5, 7, 9]), 2)
    else:
        p = sp.Integer(nonzero(rng, -5 - level, 5 + level))
    # Pick the constant term c, then q follows; c must be an integer.
    c = rng.randint(-12 - level, 12 + level)
    q = c - a * p * p
    expr = a * x ** 2 + 2 * a * p * x + c
    assert sp.expand(a * (x + p) ** 2 + q - expr) == 0
    steps = []
    if a != 1:
        steps.append(f"${poly(expr)} = {lead(a)}(x^2 {term(2 * p, 'x')}) {signed(c)}$")
    steps.append(f"$x^2 {term(2 * p, 'x')} = (x {signed(p)})^2 - {tex(p * p)}$")
    steps.append(f"${lead(a)}(x {signed(p)})^2 {signed(-a * p * p)} {signed(c)}$")
    constants = "integers" if p.q == 1 and q.q == 1 else "constants"
    form = "(x + p)^2 + q$, where $p$ and $q$" if a == 1 else "a(x + p)^2 + q$, where $a$, $p$ and $q$"
    return question(
        "Quadratics", 2 if a == 1 else 3,
        f"Write $${poly(expr)}$$\nin the form ${form} are {constants}.",
        steps,
        f"${lead(a)}(x {signed(p)})^2 {signed(q)}$")


def algebraic_fractions(rng, level):
    span = 5 + level
    while True:
        r = nonzero(rng, -span, span)
        p, q = rng.choice([1, 2, 3]), nonzero(rng, -6 - level, 6 + level)
        s, t = rng.choice([1, 2, 3] if level >= 3 else [1]), nonzero(rng, -span, span)
        # Numerator (sx + t)(x + r), denominator (x + r)(px + q); only x + r is shared.
        if (sp.gcd(p, q) == 1 and sp.gcd(s, t) == 1 and sp.Rational(-q, p) not in (-r, sp.Rational(-t, s))
                and sp.Rational(-t, s) != -r):
            break
    if level < 3:
        s, t = 1, -r  # the difference of two squares, as before level 3
    numerator = sp.expand((s * x + t) * (x + r))
    denominator = sp.expand((x + r) * (p * x + q))
    simplified = sp.cancel(numerator / denominator)
    assert simplified == sp.cancel((s * x + t) / (p * x + q))
    return question(
        "Algebraic expressions", 2,
        f"Simplify fully $$\\frac{{{poly(numerator)}}}{{{poly(denominator)}}}$$",
        [f"$\\dfrac{{({lin(s, t)})({lin(1, r)})}}{{({lin(1, r)})({lin(p, q)})}}$"],
        f"${dfrac(simplified)}$")


def disguised_quadratic(rng, level):
    """A quadratic in x², √x or eˣ: u² − (u₁ + u₂)u + u₁u₂ = 0."""
    kind = rng.choice(["square", "root"] + (["exp"] if level >= 2 else []))
    # From level 3, one root for u can be negative, which must be rejected.
    reject = level >= 3 and rng.random() < 0.5
    while True:
        if kind == "square":
            u1, u2 = rng.sample([1, 4, 9, 16, 25] + ([2, 3, 5] if level >= 3 else []), 2)
        else:
            u1, u2 = rng.sample(range(1, 6 + level), 2)
        if reject:
            u2 = -u2
        if u1 != u2:
            break
    s, p = u1 + u2, u1 * u2
    u_name, to_x, shown = {
        "square": ("x^2", lambda u: [sp.sqrt(u), -sp.sqrt(u)], f"x^4 {term(-s, 'x^2')} {signed(p)} = 0"),
        "root": ("\\sqrt{x}", lambda u: [sp.Integer(u) ** 2], f"x {term(-s, '\\sqrt{x}')} {signed(p)} = 0"),
        "exp": ("e^x", lambda u: [sp.log(u)], f"e^{{2x}} {term(-s, 'e^x')} {signed(p)} = 0"),
    }[kind]
    equation = {"square": x ** 4 - s * x ** 2 + p, "root": x - s * sp.sqrt(x) + p,
                "exp": sp.exp(2 * x) - s * sp.exp(x) + p}[kind]
    good = [u for u in (u1, u2) if u > 0]
    solutions = sorted({v for u in good for v in to_x(u)}, key=lambda v: float(v))
    # SymPy solves the original equation and must agree.
    assert sp.solveset(equation, x, sp.S.Reals) == sp.FiniteSet(*solutions)
    lo, hi = sorted((u1, u2))
    steps = [f"Let $u = {u_name}$: $u^2 {term(-s, 'u')} {signed(p)} = 0$",
             f"$(u {signed(-lo)})(u {signed(-hi)}) = 0$, so $u = {lo}$ or $u = {hi}$"]
    bad = [u for u in (u1, u2) if u < 0]
    if bad:
        steps.append(f"${u_name} = {bad[0]}$ has no real solutions, so reject it.")
    for u in good:
        steps.append(f"${u_name} = {u}$ gives " + " or ".join(f"$x = {tex(v)}$" for v in to_x(u)))
    return question(
        "Quadratics", 3,
        f"Find all the real solutions of $${shown}$$",
        steps,
        ", ".join(f"$x = {tex(v)}$" for v in solutions))


def adding_fractions(rng, level):
    """Add or subtract two algebraic fractions as one fraction in simplest form."""
    op = rng.choice(["+", "-"])
    sign = 1 if op == "+" else -1
    span = 5 + level

    def first_fraction(a, denominator):
        return f"\\frac{{{a}}}{{{denominator}}}" if a > 0 else f"-\\frac{{{-a}}}{{{denominator}}}"
    if level >= 3 and rng.random() < 0.5:
        # a/(x + p) ± b/(x² − p²): the common denominator is x² − p².
        a, b, p = nonzero(rng, -6, 6), rng.randint(1, 9), rng.randint(1, span)
        expr = sp.Integer(a) / (x + p) + sign * sp.Integer(b) / (x ** 2 - p ** 2)
        question_text = f"{first_fraction(a, lin(1, p))} {op} \\frac{{{b}}}{{x^2 - {p * p}}}"
        steps = [f"$x^2 - {p * p} = (x - {p})(x + {p})$",
                 f"$\\dfrac{{{lead(a)}(x - {p}) {op} {b}}}{{(x - {p})(x + {p})}}$"]
    else:
        while True:
            a, b = nonzero(rng, -6, 6), rng.randint(1, 6)
            p, q = nonzero(rng, -span, span), nonzero(rng, -span, span)
            expr = sp.Integer(a) / (x + p) + sign * sp.Integer(b) / (x + q)
            numerator, denominator = sp.fraction(sp.cancel(sp.together(expr)))
            # Keep both factors in the denominator and x in the numerator.
            if p != q and sp.degree(denominator, x) == 2 and sp.degree(numerator, x) == 1:
                break
        question_text = f"{first_fraction(a, lin(1, p))} {op} \\frac{{{b}}}{{{lin(1, q)}}}"
        steps = [f"$\\dfrac{{{lead(a)}({lin(1, q)}) {op} {lead(b)}({lin(1, p)})}}{{({lin(1, p)})({lin(1, q)})}}$"]
    numerator, denominator = sp.fraction(sp.cancel(sp.together(expr)))
    assert sp.cancel(numerator / denominator - expr) == 0
    answer = f"\\dfrac{{{poly(numerator)}}}{{{tex(sp.factor(denominator))}}}"
    steps.append(f"${answer}$")
    return question(
        "Algebraic expressions", 3,
        f"Write $${question_text}$$\nas a single fraction in its simplest form.",
        steps,
        f"${answer}$")


def quadratic_inequality(rng, level):
    span = 7 + level
    while True:
        p, q, r = rng.choice([1, 2, 3]), nonzero(rng, -span, span), nonzero(rng, -6 - level, 6 + level)
        if sp.gcd(p, q) == 1 and sp.Rational(-q, p) != -r:
            break
    # From level 2 the x² coefficient can be negative (an ∩-shaped curve).
    lead_sign = rng.choice([1, -1]) if level >= 2 else 1
    expr = sp.expand(lead_sign * (p * x + q) * (x + r))
    low, high = sorted(sp.solve(expr, x))
    sign = rng.choice(["<", ">"] + ([r"\leqslant", r"\geqslant"] if level >= 2 else []))
    relation = {"<": expr < 0, ">": expr > 0, r"\leqslant": expr <= 0, r"\geqslant": expr >= 0}[sign]
    solutions = sp.solve_univariate_inequality(relation, x, relational=False)
    negative = sign in ("<", r"\leqslant")
    inside = negative == (lead_sign > 0)
    shape = "U-shaped" if lead_sign > 0 else "n-shaped"
    return question(
        "Inequalities", 2,
        f"Find the set of values of $x$ for which $${poly(expr)} {sign} 0$$",
        [f"Critical values: $({lin(p, q)})({lin(1, r)}) = 0$, so $x = {tex(low)}$ or $x = {tex(high)}$",
         f"The coefficient of $x^2$ is {'positive' if lead_sign > 0 else 'negative'}, so the curve is {shape} "
         f"and the expression is {'negative' if negative else 'positive'} "
         f"{'between' if inside else 'outside'} the critical values."],
        set_text(solutions))


def discriminant(rng, level):
    """Range of k for which a quadratic in x has two, no, or some real roots."""
    while True:
        a = rng.choice([1, 2, 3])
        # k in the x coefficient, the constant term, or both.
        where = rng.choice(["b", "c", "both"])
        b = sp.sympify((rng.choice([1, 2]) * k if where != "c" else 0) + nonzero(rng, -8, 8))
        c = sp.sympify((nonzero(rng, -3, 3) * k if where != "b" else 0) + rng.randint(-9, 9))
        disc = sp.expand(b ** 2 - 4 * a * c)
        if sp.degree(disc, k) != 2 and not (level >= 4 and sp.degree(disc, k) == 1):
            continue
        roots = sp.solve(disc, k)
        if len(roots) == sp.degree(disc, k) and all(nice(v, 2) for v in roots):
            break
    condition, relation, rel_text = rng.choice([
        ("two distinct real roots", disc > 0, ">"),
        ("no real roots", disc < 0, "<"),
        ("real roots", disc >= 0, r"\geqslant"),
    ])
    solutions = sp.solve_univariate_inequality(relation, k, relational=False)
    if solutions in (sp.S.EmptySet, sp.S.Reals):
        return discriminant(rng, level)
    def in_k(e):
        """'8 - 3k', 'k + 6', or a plain number."""
        return ordered(e.coeff(k), e.subs(k, 0), "k") if e.free_symbols else tex(e)
    b_text = f"+ ({in_k(b)})x" if b.free_symbols else term(b, "x")
    c_text = f"+ ({in_k(c)})" if c.free_symbols else signed(c)
    equation = f"{lead(a)}x^2 {b_text} {c_text} = 0"
    return question(
        "Quadratics", 4,
        f"The equation $${equation}$$\nwhere $k$ is a constant, has {condition}.\n"
        "Find the set of possible values of $k$.",
        [f"{condition.capitalize()} means $b^2 - 4ac {rel_text} 0$.",
         f"$b^2 - 4ac = ({in_k(b)})^2 - 4({a})({in_k(c)}) = {poly(disc, k)}$",
         f"${poly(disc, k)} = {tex(sp.factor(disc))}$, critical values $k = "
         + "$ and $k = ".join(tex(v) for v in sorted(sp.solve(disc, k))) + "$"],
        set_text(solutions, "k"))


def simultaneous_quadratic(rng, level):
    # Pick an integer point on the line and a curve through it, then keep
    # the pair if the other intersection is also rational with a small
    # denominator.
    curves = [(1, 0, 1), (1, 0, 2), (2, 0, 1), (1, 1, 0), (1, 0, -1), (1, 1, 1), (0, 1, 1), (3, 0, 1)]
    if level >= 2:
        curves += [(2, -1, 1), (1, 2, -1), (2, 1, -1), (4, 0, -1)]
    while True:
        m, c = nonzero(rng, -3 - level // 2, 3 + level // 2), rng.randint(-5 - level, 5 + level)
        x1 = rng.randint(-3 - level // 2, 3 + level // 2)
        y1 = m * x1 + c
        a, b, e = rng.choice(curves)
        curve = a * x ** 2 + b * x * y + e * y ** 2
        rhs = curve.subs({x: x1, y: y1})
        substituted = sp.expand(curve.subs(y, m * x + c) - rhs)
        if rhs == 0 or sp.degree(substituted, x) != 2:
            continue
        xs = sorted(sp.solve(substituted, x))
        if len(xs) == 2 and all(v.is_rational and v.q <= 3 for v in xs):
            break
    line = f"y {term(-m, 'x')}"
    on_line = tex(m * x + c)
    # The curve with (mx + c) written in place of y, term by term.
    pieces = [(a, "x^2"), (b, f"x({on_line})"), (e, f"({on_line})^2")]
    shown = " ".join(term(k_, text) for k_, text in pieces if k_).removeprefix("+ ")
    solutions = [(v, m * v + c) for v in xs]
    assert {(s[x], s[y]) for s in sp.solve([y - m * x - c, curve - rhs], [x, y], dict=True)} == set(solutions)
    coeffs = sp.Poly(substituted, x).all_coeffs()
    common = sp.gcd_list(coeffs) * sp.sign(coeffs[0])
    reduced = sp.expand(substituted / common)
    steps = [f"From the first equation, $y = {tex(m * x + c)}$.",
             f"Substitute: ${shown} = {rhs}$",
             f"${poly(substituted)} = 0$" + (f", so ${poly(reduced)} = 0$" if common != 1 else ""),
             f"${tex(sp.factor(reduced))} = 0$, so $x = {tex(xs[0])}$ or $x = {tex(xs[1])}$"]
    return question(
        "Equations", 3,
        "Solve the simultaneous equations\n"
        f"$$\\begin{{aligned}}{line} &= {c}\\\\ {tex(curve)} &= {rhs}\\end{{aligned}}$$",
        steps,
        " and ".join(f"$x = {tex(a_)},\\ y = {tex(b_)}$" for a_, b_ in solutions))


# ---------------------------------------------------------------- A-level templates
# The same signature; level here counts weeks from ALEVEL_START.

def frac_term(coef, denominator, first=False):
    """'+ \\dfrac{3}{x + 2}' (or '\\dfrac{3}{x + 2}' first in a sum)."""
    text = f"\\dfrac{{{tex(abs(coef))}}}{{{denominator}}}"
    if first:
        return text if coef > 0 else f"-{text}"
    return f"{'+' if coef > 0 else '-'} {text}"


def partial_fractions(rng, level):
    span = 5 + level
    p, q = rng.sample([n for n in range(-span, span + 1) if n != 0], 2)
    if level >= 2 and rng.random() < 0.5:
        # A/(x + p) + B/(x + p)² + C/(x + q)
        A, B, C = (nonzero(rng, -5, 5) for _ in range(3))
        numerator = sp.expand(A * (x + p) * (x + q) + B * (x + q) + C * (x + p) ** 2)
        denominator = f"({lin(1, p)})^2({lin(1, q)})"
        mine = A / (x + p) + B / (x + p) ** 2 + C / (x + q)
        answer = (f"{frac_term(A, lin(1, p), True)} {frac_term(B, f'({lin(1, p)})^2')} "
                  f"{frac_term(C, lin(1, q))}")
        steps = [f"${poly(numerator)} \\equiv A({lin(1, p)})({lin(1, q)}) + B({lin(1, q)}) + C({lin(1, p)})^2$",
                 f"$x = {-p}$: ${numerator.subs(x, -p)} = {q - p}B$, so $B = {B}$",
                 f"$x = {-q}$: ${numerator.subs(x, -q)} = {(p - q) ** 2}C$, so $C = {C}$",
                 f"Compare $x^2$ terms: ${sp.Poly(numerator, x).coeff_monomial(x ** 2)} = A + C$, so $A = {A}$"]
        marks = 4
    else:
        A, B = nonzero(rng, -6, 6), nonzero(rng, -6, 6)
        numerator = sp.expand(A * (x + q) + B * (x + p))
        # From level 1 the denominator is printed expanded, to be factorised first.
        denominator = poly((x + p) * (x + q)) if level >= 1 else f"({lin(1, p)})({lin(1, q)})"
        mine = A / (x + p) + B / (x + q)
        answer = f"{frac_term(A, lin(1, p), True)} {frac_term(B, lin(1, q))}"
        steps = ([f"${denominator} = ({lin(1, p)})({lin(1, q)})$"] if level >= 1 else []) + [
            f"${poly(numerator)} \\equiv A({lin(1, q)}) + B({lin(1, p)})$",
            f"$x = {-p}$: ${numerator.subs(x, -p)} = {q - p}A$, so $A = {A}$",
            f"$x = {-q}$: ${numerator.subs(x, -q)} = {p - q}B$, so $B = {B}$"]
        marks = 3
    full = numerator / sp.expand((x + p) ** (2 if marks == 4 else 1) * (x + q))
    assert sp.simplify(sp.apart(full, x) - mine) == 0
    return question(
        "Algebraic methods", marks,
        f"Express $$\\frac{{{poly(numerator)}}}{{{denominator}}}$$\nin partial fractions.",
        steps,
        f"${answer}$")


def modulus(rng, level):
    kinds = ["eq_line", "eq_abs"] + (["ineq_abs"] if level >= 1 else []) + (["ineq_line"] if level >= 2 else [])
    kind = rng.choice(kinds)
    span = 4 + level
    while True:
        a, b = rng.randint(1, span), nonzero(rng, -6 - level, 6 + level)
        # Inside a modulus the x coefficient is positive, as it would be printed.
        c = rng.randint(1, 3) if kind.endswith("abs") else nonzero(rng, -3, 3)
        d = rng.randint(-8 - level, 8 + level)
        if abs(c) == a:
            continue
        left = sp.Abs(a * x + b)
        right = sp.Abs(c * x + d) if kind.endswith("abs") else c * x + d
        right_text = f"|{lin(c, d)}|" if kind.endswith("abs") else lin(c, d)
        if kind.startswith("eq"):
            solutions = sp.solveset(sp.Eq(left, right), x, sp.S.Reals)
            if isinstance(solutions, sp.FiniteSet) and len(solutions) >= 1 and all(nice(v, 4) for v in solutions):
                break
        else:
            sign = rng.choice(["<", ">"])
            relation = left < right if sign == "<" else left > right
            solutions = sp.solve_univariate_inequality(relation, x, relational=False)
            if solutions not in (sp.S.EmptySet, sp.S.Reals) and interval_ends_nice(solutions):
                break
    # Hand working: the two linear cases, a ± (cx + d).
    cases = sorted({sp.Rational(d - b, a - c), sp.Rational(-(b + d), a + c)}, key=float)
    if kind == "eq_line":
        steps = [f"Either ${lin(a, b)} = {lin(c, d)}$, giving $x = {tex(sp.Rational(d - b, a - c))}$, "
                 f"or $-({lin(a, b)}) = {lin(c, d)}$, giving $x = {tex(sp.Rational(-(b + d), a + c))}$"]
        for v in cases:
            if c * v + d < 0:
                steps.append(f"At $x = {tex(v)}$, ${lin(c, d)} = {tex(c * v + d)} < 0$, so reject it.")
        assert set(solutions) == {v for v in cases if c * v + d >= 0}
        answer, marks = ", ".join(f"$x = {tex(v)}$" for v in sorted(solutions, key=float)), 3
        text = f"Solve $$|{lin(a, b)}| = {right_text}$$"
    elif kind == "eq_abs":
        steps = [f"Either ${lin(a, b)} = {lin(c, d)}$, giving $x = {tex(sp.Rational(d - b, a - c))}$",
                 f"or ${lin(a, b)} = -({lin(c, d)})$, giving $x = {tex(sp.Rational(-(b + d), a + c))}$"]
        assert set(solutions) == set(cases)
        answer, marks = ", ".join(f"$x = {tex(v)}$" for v in sorted(solutions, key=float)), 3
        text = f"Solve $$|{lin(a, b)}| = {right_text}$$"
    elif kind == "ineq_abs":
        squared = sp.expand((a * x + b) ** 2 - (c * x + d) ** 2)
        steps = [f"Square both sides: $({lin(a, b)})^2 {sign} ({lin(c, d)})^2$",
                 f"${poly(squared)} {sign} 0$, critical values $x = "
                 + "$ and $x = ".join(tex(v) for v in cases) + "$"]
        assert sp.solve_univariate_inequality(squared < 0 if sign == "<" else squared > 0, x,
                                              relational=False) == solutions
        answer, marks = set_text(solutions), 4
        text = f"Find the set of values of $x$ for which $$|{lin(a, b)}| {sign} {right_text}$$"
    else:
        valid = [v for v in cases if c * v + d >= 0]
        steps = [f"Critical values where $y = |{lin(a, b)}|$ meets $y = {lin(c, d)}$: "
                 + (" and ".join(f"$x = {tex(v)}$" for v in valid) if valid else "none"),
                 f"Sketch both graphs: $|{lin(a, b)}|$ is {'below' if sign == '<' else 'above'} "
                 f"${lin(c, d)}$ for the values shown."]
        answer, marks = set_text(solutions), 4
        text = f"Find the set of values of $x$ for which $$|{lin(a, b)}| {sign} {right_text}$$"
    return question("Algebra and functions", marks, text, steps, answer)


def composite_inverse(rng, level):
    f_kind = rng.choice(["linear", "rational"] + (["exp"] if level >= 2 else []))
    span = 5 + level
    while True:
        a, b, c = nonzero(rng, -span, span), nonzero(rng, -9, 9), nonzero(rng, -span, span)
        if f_kind != "rational" or a * c - b != 0:
            break
    if f_kind == "linear":
        f = a * x + b
        f_text, f_domain = lin(a, b), "x \\in \\mathbb{R}"
        # (y − b)/a, written with a positive denominator and none when a = ±1.
        top = lin(1, -b, "y") if a > 0 else ordered(-1, b, "y")
        solved = top if abs(a) == 1 else f"\\dfrac{{{top}}}{{{abs(a)}}}"
        inverse_steps = [f"$y = {lin(a, b)}$, so $x = {solved}$"]
        linear_inverse = solved.replace("y", "x")
    elif f_kind == "rational":
        f = (a * x + b) / (x + c)
        f_text, f_domain = f"\\dfrac{{{lin(a, b)}}}{{{lin(1, c)}}}", f"x \\in \\mathbb{{R}},\\ x \\neq {-c}"
        inverse_steps = [f"$y({lin(1, c)}) = {lin(a, b)}$",
                         f"$xy {term(-a, 'x')} = {ordered(-c, b, 'y')}$, "
                         f"so $x = \\dfrac{{{ordered(-c, b, 'y')}}}{{y {signed(-a)}}}$"]
    else:
        a = abs(a)
        f = a * sp.exp(x) + b
        f_text, f_domain = f"{lead(a)}e^x {signed(b)}", "x \\in \\mathbb{R}"
        inverse_steps = [f"$y = {f_text}$, so $e^x = \\dfrac{{y {signed(-b)}}}{{{a}}}$ and "
                         f"$x = \\ln\\left(\\dfrac{{y {signed(-b)}}}{{{a}}}\\right)$"]
    inverse = sp.solve(sp.Eq(y, f), x)[0].subs(y, x)
    assert sp.simplify(f.subs(x, inverse) - x) == 0
    m, n = nonzero(rng, -4, 4), rng.randint(-6, 6)
    g = rng.choice([m * x + n, x ** 2 + n]) if level >= 1 else m * x + n
    g_text = poly(g)
    order = rng.choice(["fg", "gf"])
    composite = sp.cancel(sp.together(f.subs(x, g) if order == "fg" else g.subs(x, f)))
    if f_kind == "exp":
        composite = sp.expand(f.subs(x, g) if order == "fg" else g.subs(x, f))
        composite_text = tex(composite)
    else:
        num, den = sp.fraction(composite)
        composite_text = poly(num) if den == 1 else f"\\dfrac{{{poly(num)}}}{{{tex(sp.factor(den))}}}"
    if f_kind == "exp":
        inverse_text = f"\\ln\\left(\\dfrac{{x {signed(-b)}}}{{{a}}}\\right)"
    elif f_kind == "linear":
        inverse_text = linear_inverse
        assert sp.simplify(sp.sympify((x - b) / a) - inverse) == 0
    else:
        inverse_text = dfrac(sp.cancel(inverse))
    assert sp.simplify(sp.sympify(composite) - (f.subs(x, g) if order == "fg" else g.subs(x, f))) == 0
    inner, outer = ("g", "f") if order == "fg" else ("f", "g")
    # The outer function's formula with the inner one written in place of x.
    texts = {"f": f_text, "g": g_text}
    if outer == "f" and f_kind == "exp":
        substituted = texts["f"].replace("e^x", f"e^{{{texts['g']}}}")
    else:
        substituted = texts[outer].replace("x", f"\\left({texts[inner]}\\right)")
    return question(
        "Functions", 4,
        "The functions f and g are defined by\n"
        f"$$\\begin{{aligned}}\\mathrm{{f}}(x) &= {f_text}, \\quad {f_domain}\\\\ "
        f"\\mathrm{{g}}(x) &= {g_text}, \\quad x \\in \\mathbb{{R}}\\end{{aligned}}$$\n"
        "(a) Find $\\mathrm{f}^{-1}(x)$.\n"
        f"(b) Find $\\mathrm{{{order}}}(x)$, giving your answer in its simplest form.",
        ["(a) " + inverse_steps[0]] + inverse_steps[1:] +
        [f"(b) $\\mathrm{{{order}}}(x) = \\mathrm{{{outer}}}(\\mathrm{{{inner}}}(x)) = {substituted}$"],
        f"(a) $\\mathrm{{f}}^{{-1}}(x) = {inverse_text}$ (b) $\\mathrm{{{order}}}(x) = {composite_text}$")


def binomial(rng, level):
    powers = [sp.Integer(-1), sp.Integer(-2), sp.Rational(1, 2), sp.Rational(-1, 2)]
    if level >= 1:
        powers += [sp.Integer(-3), sp.Rational(1, 3), sp.Rational(-1, 3), sp.Rational(3, 2)]
    n = rng.choice(powers)
    # From level 2 the constant isn't 1, so it has to be taken out first.
    if level >= 2:
        a = rng.choice({1: [2, 3], 2: [4, 9], 3: [8, 27]}[n.q])
    else:
        a = 1
    b = nonzero(rng, -4, 4)
    ratio = sp.Rational(b, a)
    outside = sp.Integer(a) ** n
    c1, c2 = n * ratio, n * (n - 1) / 2 * ratio ** 2
    coeffs = [outside, outside * c1, outside * c2]
    series = sp.series((a + b * x) ** n, x, 0, 3).removeO()
    assert all(sp.simplify(series.coeff(x, i) - coeffs[i]) == 0 for i in range(3))
    expansion = f"{tex(coeffs[0])} {term(coeffs[1], 'x')} {term(coeffs[2], 'x^2')}"
    steps = []
    if a != 1:
        steps.append(f"$({a} {term(b, 'x')})^{{{tex(n)}}} = {a}^{{{tex(n)}}}"
                     f"\\left(1 {term(ratio, 'x')}\\right)^{{{tex(n)}}} = {tex(outside)}"
                     f"\\left(1 {term(ratio, 'x')}\\right)^{{{tex(n)}}}$")
    steps.append(f"$\\left(1 {term(ratio, 'x')}\\right)^{{{tex(n)}}} = 1 + ({tex(n)})({tex(ratio)}x) + "
                 f"\\dfrac{{({tex(n)})({tex(n - 1)})}}{{2}}({tex(ratio)}x)^2 + \\dots"
                 f" = 1 {term(c1, 'x')} {term(c2, 'x^2')} + \\dots$")
    steps.append(f"Valid for $|{tex(ratio)}x| < 1$")
    return question(
        "Algebraic methods", 4,
        "Find the first three terms, in ascending powers of $x$, of the binomial expansion of\n"
        f"$$({a} {term(b, 'x')})^{{{tex(n)}}}$$\n"
        "giving each coefficient in its simplest form, and state the range of values of $x$ "
        "for which the expansion is valid.",
        steps,
        f"${expansion} + \\dots$, valid for $|x| < {tex(abs(1 / ratio))}$")


def rational_expressions(rng, level):
    """Multiply or divide two algebraic fractions and simplify."""
    # Distinct linear factors: no two share a root, so only the intended ones cancel.
    while True:
        factors = []
        for _ in range(6):
            p = rng.choice([1, 1, 2] + ([3] if level >= 2 else []))
            r = nonzero(rng, -6, 6)
            if sp.gcd(p, r) == 1:
                factors.append(p * x + r)
        roots = [sp.solve(f, x)[0] for f in factors]
        if len(factors) == 6 and len(set(roots)) == 6:
            break
    L1, L2, L3, L4, L5, L6 = factors
    first = (L1 * L2, L3 * L4)
    if level >= 2:
        second, op = (L2 * L5, L4 * L6), "\\div"            # result L1 L6 / (L3 L5)
        expr = (first[0] / first[1]) / (second[0] / second[1])
    elif level >= 1:
        second, op = (L2, L4), "\\div"                      # result L1 / L3
        expr = (first[0] / first[1]) / (second[0] / second[1])
    else:
        second, op = (L4, L2), "\\times"                    # result L1 / L3
        expr = (first[0] / first[1]) * (second[0] / second[1])
    result = sp.cancel(expr)
    num, den = sp.fraction(sp.factor(result))
    answer = f"\\dfrac{{{tex(num)}}}{{{tex(den)}}}"
    assert sp.cancel(sp.factor(result) - expr) == 0

    def shown(pair, factorised, frac="\\frac"):
        f = (lambda e: tex(sp.factor(e))) if factorised else poly
        return f"{frac}{{{f(pair[0])}}}{{{f(pair[1])}}}"
    return question(
        "Algebraic methods", 3,
        f"Simplify fully $${shown(first, False)} {op} {shown(second, False)}$$",
        [f"Factorise: ${shown(first, True, '\\dfrac')} {op} {shown(second, True, '\\dfrac')}$",
         "Turn the division into multiplication by the reciprocal, then cancel common factors."
         if op == "\\div" else "Cancel common factors."],
        f"${answer}$")


# ---------------------------------------------------------------- choosing the sheet

@dataclass(frozen=True)
class Template:
    make: Callable
    rank: float            # sheet order, easiest first
    unlock: int = 0        # first level it appears at
    retire: int = None     # level it stops appearing at
    alevel: bool = False


TEMPLATES = [
    Template(surds_simplify, 1, retire=2),
    Template(indices, 2),
    Template(expanding, 3, retire=3),
    Template(linear_inequality, 4, retire=3),
    Template(factorising, 5),
    Template(rearranging, 6),
    Template(simultaneous_linear, 7, retire=4),
    Template(rationalising, 8),
    Template(solving_quadratic, 9),
    Template(completing_square, 10),
    Template(algebraic_fractions, 11),
    Template(binomial, 11.5, alevel=True),
    Template(rational_expressions, 11.8, alevel=True),
    Template(adding_fractions, 12, unlock=1),
    Template(partial_fractions, 12.5, alevel=True),
    Template(composite_inverse, 13, alevel=True),
    Template(disguised_quadratic, 13.5, unlock=1),
    Template(quadratic_inequality, 14),
    Template(modulus, 14.5, alevel=True),
    Template(discriminant, 15, unlock=2),
    Template(simultaneous_quadratic, 16),
]
TOP_RANK = max(t.rank for t in TEMPLATES)


def available(level, alevel):
    """(AS templates for this level, A-level templates or [])."""
    as_level = [t for t in TEMPLATES if not t.alevel and t.unlock <= level
                and (t.retire is None or level < t.retire)]
    a_level = [t for t in TEMPLATES if t.alevel] if alevel else []
    return as_level, a_level


def available_names(day):
    as_pool, a_pool = available(level_for(day), alevel_level_for(day) is not None)
    return {t.make.__name__ for t in as_pool + a_pool}


def read_history(day, folder=None):
    """{date: set of template names} from the daily drill records
    (out/drills/drill-YYYY-MM-DD.json) of the WINDOW - 1 days before `day`.

    Only daily records count: a set built with --name is a test or extra
    sheet. Records made before templates were recorded add nothing.
    """
    folder = folder or OUT_DIR / "drills"
    history = {}
    for back in range(1, WINDOW):
        past = day - timedelta(days=back)
        path = folder / f"drill-{past.isoformat()}.json"
        if path.is_file():
            record = json.loads(path.read_text(encoding="utf-8"))
            history[past] = {q["template"] for q in record["questions"] if "template" in q}
    return history


def due_names(day, history):
    """Templates that must go on `day`'s sheet to keep the 7-day guarantee.

    A template is due when it was available on each of the previous six days
    and is available today, but none of those days' sheets had it. Days
    without a sheet count as days it didn't appear.
    """
    window = [day - timedelta(days=back) for back in range(1, WINDOW)]
    due = available_names(day)
    for past in window:
        due &= available_names(past)
        due -= history.get(past, set())
    return due


def make_sheet(seed, day=START, history=None):
    """The day's questions, easiest first.

    `history` is read_history(day): the templates on the previous six days'
    sheets. Templates that are due (see due_names) go in first, then the
    least recently used, so every template available at the level appears
    at least once in every 7 days. Ties are broken at random, harder
    templates more likely as the level rises.
    """
    rng = random.Random(seed)
    history = history or {}
    level, a_level_level = level_for(day), alevel_level_for(day)
    as_pool, a_pool = available(level, a_level_level is not None)
    due = due_names(day, history)
    last_seen = {}
    for past, names in history.items():
        for name in names:
            last_seen[name] = max(past, last_seen.get(name, date.min))

    def rotation(pool):
        """Due first, then least recently used; ties in weighted random order
        (u^(1/w) keys, so a weight w template is w times as likely to lead)."""
        def key(t):
            name = t.make.__name__
            weight = 1 + level * t.rank / TOP_RANK
            return (name not in due, last_seen.get(name, date.min), -rng.random() ** (1 / weight))
        return sorted(pool, key=key)

    chosen, marks, missed = [], 0, []

    def add(template, lvl):
        nonlocal marks
        item = template.make(rng, lvl)
        if marks + item["marks"] > MAX_MARKS:
            if template.make.__name__ in due:
                missed.append(template.make.__name__)
            return
        item["template"] = template.make.__name__
        item["level"] = lvl
        chosen.append((template.rank, item))
        marks += item["marks"]

    # A-level questions first (two or three, more if more are due), so the
    # AS ones fill the marks around them.
    a_count = 0
    for template in rotation(a_pool):
        if template.make.__name__ in due or a_count < (2 if a_level_level < 2 else 3):
            add(template, a_level_level)
            a_count += 1
    # Then AS templates: every due one, and the rest until the marks are filled.
    for template in rotation(as_pool):
        if template.make.__name__ in due or marks < MIN_MARKS:
            add(template, level)
    if marks < MIN_MARKS:
        raise SystemExit(f"drill: only {marks} marks could be filled at level {level}")
    if missed:
        # Only when several days had no sheet: too much is due for one day.
        print(f"drill: due but no room on {day}: {', '.join(missed)}", file=sys.stderr)
    return [item for _, item in sorted(chosen, key=lambda pair: pair[0])]


# ---------------------------------------------------------------- PDFs

def answer_block(number, item):
    lines = [f"\\msquestion{{{number}}}{{{build_pdf.escape_text(item['topic'])}}}{{{item['marks']}}}"]
    lines += [f"\\mspoint{{}}{{{build_pdf.bank_to_latex(step)}}}" for step in item["steps"]]
    lines.append(f"\\mspoint{{Answer:}}{{{build_pdf.bank_to_latex(item['answer'])}}}")
    return "\n".join(lines) + "\n"


def build(name, seed, day=None):
    """Build NAME_questions.pdf and NAME_answers.pdf for `day`. Returns the sheet."""
    if not build_pdf.SET_NAME_RE.match(name):
        raise SystemExit(f"set name {name!r}: use only letters, digits, '-', '_' and '.'")
    day = day or date.today()
    sheet = make_sheet(seed, day, read_history(day))
    build_dir = ensure_out_dir(f"build/{name}")
    out_dir = ensure_out_dir("to-remarkable")
    total = sum(item["marks"] for item in sheet)
    level = f"level {level_for(day)}" + (f", A level {alevel_level_for(day)}" if alevel_level_for(day) is not None else "")
    cover = build_pdf.escape_text(f"Algebra drill ({level}) · {len(sheet)} questions · Total {total} marks · "
                                  f"Suggested time {build_pdf.suggested_minutes(total)} minutes")
    title = build_pdf.escape_text(name)

    questions = "\n".join(
        f"\\bankquestion{{{n}}}{{{build_pdf.escape_text(item['topic'])}}}{{{item['marks']}}}"
        f"{{{build_pdf.working_space_cm(item['marks'])}cm}}{{%\n{build_pdf.bank_to_latex(item['question'])}}}\n"
        for n, item in enumerate(sheet, 1))
    answers = "\n".join(answer_block(n, item) for n, item in enumerate(sheet, 1))
    for template, heading, body, suffix in [("questions.tex", title, questions, "questions"),
                                            ("markscheme.tex", f"{title} --- answers", answers, "answers")]:
        tex_path = build_dir / f"{name}_{suffix}.tex"
        tex_path.write_text(build_pdf.fill_template(template, heading, cover, body), encoding="utf-8")
        build_pdf.compile_or_exit(tex_path, out_dir / f"{name}_{suffix}.pdf")

    record = ensure_out_dir("drills") / f"{name}.json"
    record.write_text(json.dumps({"seed": seed, "date": day.isoformat(), "questions": sheet},
                                 indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return sheet


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(),
                        help="the day the sheet is for, which sets its level (default today)")
    parser.add_argument("--name", help="set name (default drill-YYYY-MM-DD)")
    parser.add_argument("--seed", type=int, help="random seed (default: from the date)")
    args = parser.parse_args()
    name = args.name or f"drill-{args.date.isoformat()}"
    seed = args.seed if args.seed is not None else args.date.toordinal()
    sheet = build(name, seed, args.date)
    print(f"{name}: {len(sheet)} questions, {sum(i['marks'] for i in sheet)} marks, level {level_for(args.date)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
