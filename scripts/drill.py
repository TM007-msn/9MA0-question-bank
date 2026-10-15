"""Build a ~25-mark algebra fluency sheet and its worked answers.

Usage (from the project root, with the venv active):
    python scripts/drill.py                    # drill-YYYY-MM-DD for today
    python scripts/drill.py --date 2026-11-02  # that day's sheet
    python scripts/drill.py --seed 7 --name drill-test

Writes, with the same LaTeX templates as build_pdf.py:
    out/to-remarkable/NAME_questions.pdf   the questions, easier ones first
    out/to-remarkable/NAME_answers.pdf     worked answers (never sent to the tablet)
    out/drills/NAME.json                   the questions and answers as text

One question from each template below, with random numbers chosen so the
answers come out clean (integers, small fractions, simple surds). SymPy works
out every answer from the question, so an answer can't disagree with its
question. The seed defaults to the date, so rebuilding a day's sheet gives
the same questions.
"""

import argparse
import json
import random
import sys
from datetime import date

import sympy as sp

import build_pdf
from paths import ensure_out_dir

x, y = sp.symbols("x y")


# ---------------------------------------------------------------- helpers

def tex(expr):
    """LaTeX for a SymPy expression, highest power first."""
    expr = sp.sympify(expr)
    return sp.latex(expr, order="lex" if expr.free_symbols - {x} else None)


def poly(expr):
    """LaTeX for a polynomial in x, highest power first."""
    return sp.latex(sp.Poly(sp.expand(expr), x).as_expr())


def signed(n):
    """'+ 3' or '- 3', for writing a term after another one."""
    return f"+ {tex(n)}" if n >= 0 else f"- {tex(-n)}"


def paren(n):
    """A number to write after an operator: (-4) in brackets, 4 as is."""
    return f"({n})" if n < 0 else f"{n}"


def term(coef, var):
    """'+ 3x', '- x', ... for a term after another one."""
    size = "" if abs(coef) == 1 else str(abs(coef))
    return f"{'+' if coef > 0 else '-'} {size}{var}"


def nonzero(rng, low, high):
    return rng.choice([n for n in range(low, high + 1) if n != 0])


def question(topic, marks, text, steps, answer):
    return {"topic": topic, "marks": marks, "question": text, "steps": steps, "answer": answer}


# ---------------------------------------------------------------- templates
# Each takes a random.Random and returns question(...). They are listed
# roughly from easiest to hardest, which is the order they go on the sheet.

def surds_simplify(rng):
    k = rng.choice([2, 3, 5, 6, 7])
    p, q = rng.sample(range(2, 6), 2)
    a, b = p * p * k, q * q * k
    total = sp.sqrt(a) + sp.sqrt(b)
    return question(
        "Surds", 1,
        f"Write $\\sqrt{{{a}}} + \\sqrt{{{b}}}$ in the form $c\\sqrt{{{k}}}$, where $c$ is an integer.",
        [f"$\\sqrt{{{a}}} = \\sqrt{{{p * p}}}\\sqrt{{{k}}} = {p}\\sqrt{{{k}}}$ and "
         f"$\\sqrt{{{b}}} = \\sqrt{{{q * q}}}\\sqrt{{{k}}} = {q}\\sqrt{{{k}}}$"],
        f"${tex(total)}$")


def indices(rng):
    a = rng.choice([2, 3])
    n = rng.choice([2, 3])
    m = rng.randint(2, 4)
    numerator = a ** n
    b = rng.choice([d for d in sp.divisors(numerator) if 1 < d < numerator] or [1])
    xp = sp.symbols("x", positive=True)
    result = sp.simplify((a * xp ** m) ** n / (b * sp.sqrt(xp)))
    power = sp.Rational(m * n) - sp.Rational(1, 2)
    return question(
        "Indices", 2,
        f"Simplify fully $$\\frac{{({a}x^{{{m}}})^{{{n}}}}}{{{b}\\sqrt{{x}}}}$$\n"
        "giving your answer in the form $kx^{p}$.",
        [f"$({a}x^{{{m}}})^{{{n}}} = {numerator}x^{{{m * n}}}$ and $\\sqrt{{x}} = x^{{\\frac{{1}}{{2}}}}$",
         f"$\\dfrac{{{numerator}x^{{{m * n}}}}}{{{b}x^{{\\frac{{1}}{{2}}}}}} = "
         f"\\dfrac{{{numerator}}}{{{b}}}x^{{{m * n} - \\frac{{1}}{{2}}}}$"],
        f"${tex(sp.Rational(numerator, b))}x^{{{tex(power)}}}$"
        if result == sp.Rational(numerator, b) * xp ** power else None)


def expanding(rng):
    a, b = nonzero(rng, -5, 5), nonzero(rng, -5, 5)
    c, d = rng.choice([2, 3]), nonzero(rng, -4, 4)
    first = sp.expand((x + a) * (x + b))
    full = sp.expand(first * (c * x + d))
    return question(
        "Algebraic expressions", 2,
        f"Expand and simplify $(x {signed(a)})(x {signed(b)})({c}x {signed(d)})$.",
        [f"$(x {signed(a)})(x {signed(b)}) = {poly(first)}$",
         f"$({poly(first)})({c}x {signed(d)}) = {poly(full)}$"],
        f"${poly(full)}$")


def linear_inequality(rng):
    # a x + b < c x + d with a - c negative half the time, so the sign flips.
    while True:
        a, c = rng.randint(-4, 7), rng.randint(-4, 7)
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
    steps = [f"${a - c}x {sign} {d - b}$"]
    if flip:
        steps.append(f"Dividing by ${a - c}$, a negative number, reverses the inequality.")
    return question(
        "Inequalities", 2,
        f"Solve $${a}x {signed(b)} {sign} {c}x {signed(d)}$$",
        steps,
        f"$x {final} {root}$")


def factorising(rng):
    while True:
        k = rng.choice([1, 2, 3])
        p = rng.choice([1, 2, 3])
        q, r = nonzero(rng, -5, 5), nonzero(rng, -5, 5)
        if sp.gcd(p, q) == 1 and not (p == 1 and q == r):
            break
    expr = sp.expand(k * x * (p * x + q) * (x + r))
    quadratic = sp.expand((p * x + q) * (x + r))
    common = f"{k}x" if k > 1 else "x"
    return question(
        "Algebraic expressions", 2,
        f"Factorise completely $${poly(expr)}$$",
        [f"Take out the common factor ${common}$: ${common}({poly(quadratic)})$"],
        f"${tex(sp.factor(expr))}$")


def rearranging(rng):
    while True:
        a, b, c = nonzero(rng, 2, 6), nonzero(rng, -9, 9), nonzero(rng, -5, 5)
        # b = -ac would make the fraction cancel down to the constant a.
        if b + a * c != 0:
            break
    # c y + b, written with the positive term first.
    top = f"{c if abs(c) != 1 else ''}y {signed(b)}" if c > 0 else f"{b} {term(c, 'y')}"
    solved = sp.solve(sp.Eq(y, (a * x + b) / (x - c)), x)[0]
    # SymPy checks the hand-written answer.
    assert sp.simplify(solved - (c * y + b) / (y - a)) == 0
    return question(
        "Algebraic expressions", 2,
        f"Make $x$ the subject of $$y = \\frac{{{a}x {signed(b)}}}{{x {signed(-c)}}}$$",
        [f"$y(x {signed(-c)}) = {a}x {signed(b)}$",
         f"$xy {term(-c, 'y')} = {a}x {signed(b)}$",
         f"$xy - {a}x = {top}$",
         f"$x(y - {a}) = {top}$"],
        f"$x = \\dfrac{{{top}}}{{y - {a}}}$")


def simultaneous_linear(rng):
    while True:
        x0, y0 = nonzero(rng, -5, 6), nonzero(rng, -5, 6)
        a1, a2 = rng.randint(1, 6), rng.randint(1, 6)
        b1, b2 = nonzero(rng, -5, 6), nonzero(rng, -5, 6)
        if a1 * b2 - a2 * b1 != 0 and abs(b1) != abs(b2):
            break
    c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
    det = a1 * b2 - a2 * b1
    return question(
        "Equations", 2,
        "Solve the simultaneous equations\n"
        f"$$\\begin{{aligned}}{tex(a1 * x + b1 * y)} &= {c1}\\\\ {tex(a2 * x + b2 * y)} &= {c2}\\end{{aligned}}$$",
        [f"Multiply the first equation by ${b2}$ and the second by ${b1}$, then subtract to eliminate $y$:",
         f"$({a1 * b2} - {paren(a2 * b1)})x = {c1 * b2} - {paren(c2 * b1)}$, "
         f"so ${det}x = {c1 * b2 - c2 * b1}$ and $x = {x0}$",
         f"Substitute into the first equation: ${a1 * x0} {term(b1, 'y')} = {c1}$, so $y = {y0}$"],
        f"$x = {x0},\\ y = {y0}$")


def rationalising(rng):
    while True:
        b = rng.randint(2, 5)
        # Square-free k, so √k is already in its simplest form.
        k = rng.choice([n for n in range(2, 20) if all(e == 1 for e in sp.factorint(n).values())])
        d = b * b - k
        m, n = nonzero(rng, -6, 6), rng.choice([1, 2, -1])
        # (m + n√k)(b + √k) = (mb + nk) + (m + nb)√k, over b² − k.
        rational, irrational = m * b + n * k, m + n * b
        if (d != 0 and abs(d) <= 4 and rational % d == 0 and irrational % d == 0 and irrational != 0
                and abs(rational // d) <= 20 and abs(irrational // d) <= 20):
            break
    s = sp.sqrt(k)
    p, q = rational // d, irrational // d
    # SymPy checks the hand-worked p + q√k.
    assert sp.simplify((m + n * s) / (b - s) - (p + q * s)) == 0
    root = f"\\sqrt{{{k}}}"
    numerator = f"{m} {term(n, root)}"
    return question(
        "Surds", 2,
        f"Write $$\\frac{{{numerator}}}{{{b} - {root}}}$$\n"
        f"in the form $p + q{root}$, where $p$ and $q$ are integers.",
        [f"Multiply top and bottom by $({b} + {root})$.",
         f"Denominator: $({b} - {root})({b} + {root}) = {b * b} - {k} = {d}$",
         f"Numerator: $({numerator})({b} + {root}) = {rational} {term(irrational, root)}$",
         f"$\\dfrac{{{rational} {term(irrational, root)}}}{{{d}}}$"],
        f"${p} {term(q, root)}$")


def solving_quadratic(rng):
    while True:
        p, q, r = rng.choice([2, 3]), nonzero(rng, -7, 7), nonzero(rng, -6, 6)
        if sp.gcd(p, q) == 1:
            break
    expr = sp.expand((p * x + q) * (x + r))
    roots = sorted(sp.solve(expr, x))
    return question(
        "Equations", 2,
        f"Solve $${poly(expr)} = 0$$",
        [f"$({p}x {signed(q)})(x {signed(r)}) = 0$"],
        "$x = " + "$ or $x = ".join(tex(v) for v in roots) + "$")


def completing_square(rng):
    a = rng.choice([1, 2, 3])
    p = nonzero(rng, -5, 5)
    q = rng.randint(-12, 12)
    expr = sp.expand(a * (x + p) ** 2 + q)
    b, c = 2 * a * p, a * p * p + q
    lead = f"{a}" if a > 1 else ""
    steps = []
    if a > 1:
        steps.append(f"${poly(expr)} = {a}(x^2 {signed(2 * p)}x) {signed(c)}$")
    steps.append(f"$x^2 {signed(2 * p)}x = (x {signed(p)})^2 - {p * p}$")
    steps.append(f"${lead}(x {signed(p)})^2 - {a * p * p} {signed(c)}$")
    return question(
        "Quadratics", 2,
        f"Write $${poly(expr)}$$\n"
        "in the form $" + ("a" if a > 1 else "") + "(x + p)^2 + q$, where "
        + ("$a$, " if a > 1 else "") + "$p$ and $q$ are integers.",
        steps,
        f"${lead}(x {signed(p)})^2 {signed(q)}$")


def algebraic_fractions(rng):
    while True:
        r = nonzero(rng, -5, 5)
        p, q = rng.choice([1, 2, 3]), nonzero(rng, -6, 6)
        if sp.gcd(p, q) == 1 and (p, q) != (1, r) and (p, q) != (1, -r):
            break
    numerator = sp.expand((x - r) * (x + r))
    denominator = sp.expand((x + r) * (p * x + q))
    simplified = sp.cancel(numerator / denominator)
    return question(
        "Algebraic expressions", 2,
        f"Simplify fully $$\\frac{{{poly(numerator)}}}{{{poly(denominator)}}}$$",
        [f"$\\dfrac{{(x {signed(-r)})(x {signed(r)})}}{{(x {signed(r)})({p if p > 1 else ''}x {signed(q)})}}$"],
        "$" + tex(simplified).replace(r"\frac", r"\dfrac") + "$")


def quadratic_inequality(rng):
    while True:
        p, q, r = rng.choice([1, 2, 3]), nonzero(rng, -7, 7), nonzero(rng, -6, 6)
        if sp.gcd(p, q) == 1 and sp.Rational(-q, p) != -r:
            break
    expr = sp.expand((p * x + q) * (x + r))
    low, high = sorted(sp.solve(expr, x))
    sign = rng.choice(["<", ">"])
    if sign == "<":
        answer = f"${tex(low)} < x < {tex(high)}$"
        region = "between the roots"
    else:
        answer = f"$x < {tex(low)}$ or $x > {tex(high)}$"
        region = "outside the roots"
    p_text = f"{p}" if p > 1 else ""
    return question(
        "Inequalities", 2,
        f"Find the set of values of $x$ for which $${poly(expr)} {sign} 0$$",
        [f"Critical values: $({p_text}x {signed(q)})(x {signed(r)}) = 0$, so $x = {tex(low)}$ or $x = {tex(high)}$",
         f"The coefficient of $x^2$ is positive, so the curve is U-shaped and the expression is {'negative' if sign == '<' else 'positive'} {region}."],
        answer)


def simultaneous_quadratic(rng):
    # Pick an integer point on the line and a curve through it, then keep
    # the pair if the other intersection is also rational with a small
    # denominator.
    curves = [(1, 0, 1), (1, 0, 2), (2, 0, 1), (1, 1, 0), (1, 0, -1), (1, 1, 1), (0, 1, 1), (3, 0, 1)]
    while True:
        m, c = nonzero(rng, -3, 3), rng.randint(-5, 5)
        x1 = rng.randint(-3, 3)
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
    shown = " ".join(term(k, text) for k, text in pieces if k).removeprefix("+ ")
    solutions = [(v, m * v + c) for v in xs]
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


TEMPLATES = [surds_simplify, indices, expanding, linear_inequality, factorising, rearranging,
             simultaneous_linear, rationalising, solving_quadratic, completing_square,
             algebraic_fractions, quadratic_inequality, simultaneous_quadratic]


def make_sheet(seed):
    """One question from each template, in the order listed (easiest first)."""
    rng = random.Random(seed)
    sheet = []
    for template in TEMPLATES:
        item = template(rng)
        if item["answer"] is None:
            raise SystemExit(f"{template.__name__}: SymPy's answer didn't match the worked steps")
        sheet.append(item)
    return sheet


# ---------------------------------------------------------------- PDFs

def answer_block(number, item):
    lines = [f"\\msquestion{{{number}}}{{{build_pdf.escape_text(item['topic'])}}}{{{item['marks']}}}"]
    lines += [f"\\mspoint{{}}{{{build_pdf.bank_to_latex(step)}}}" for step in item["steps"]]
    lines.append(f"\\mspoint{{Answer:}}{{{build_pdf.bank_to_latex(item['answer'])}}}")
    return "\n".join(lines) + "\n"


def build(name, seed):
    """Build NAME_questions.pdf and NAME_answers.pdf. Returns the sheet."""
    if not build_pdf.SET_NAME_RE.match(name):
        raise SystemExit(f"set name {name!r}: use only letters, digits, '-', '_' and '.'")
    sheet = make_sheet(seed)
    build_dir = ensure_out_dir(f"build/{name}")
    out_dir = ensure_out_dir("to-remarkable")
    total = sum(item["marks"] for item in sheet)
    cover = build_pdf.escape_text(f"Algebra drill · {len(sheet)} questions · Total {total} marks · "
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
    record.write_text(json.dumps({"seed": seed, "questions": sheet}, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    return sheet


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(),
                        help="the day the sheet is for (default today)")
    parser.add_argument("--name", help="set name (default drill-YYYY-MM-DD)")
    parser.add_argument("--seed", type=int, help="random seed (default: from the date)")
    args = parser.parse_args()
    name = args.name or f"drill-{args.date.isoformat()}"
    seed = args.seed if args.seed is not None else args.date.toordinal()
    sheet = build(name, seed)
    print(f"{name}: {len(sheet)} questions, {sum(i['marks'] for i in sheet)} marks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
