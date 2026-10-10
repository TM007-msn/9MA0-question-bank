"""Draft builder for 8MA0-01 SPEC (AS Pure, specimen paper).

Run (from the project root, with the venv active):
    python extraction/8MA0-01_SPEC.py        # writes out/drafts/8MA0-01_SPEC.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-01_SPEC.json

Everything here is transcribed from the source PDFs, read as page images
(figures at 200 dpi). There is no examiner report for the specimen paper, so
examiner_notes, difficulty and difficulty_evidence are all null.
The mark scheme's symbol font shows ⩽ as „ and ⩾ as … ; they are written as
\\leqslant and \\geqslant here. Follow CLAUDE.md for every field.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report, part_key  # noqa: E402
from mark_codes import main_marks  # noqa: E402
from paths import ensure_out_dir  # noqa: E402

P, S = "8MA0-01", "SPEC"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "11iia"); label as printed (e.g. "11(ii)(a)")."""
    return {"id": f"{P}_{S}_Q{q}", "paper": P, "series": S, "question": label, "topic": topic,
            "spec_ref": spec, "marks": marks, "question_latex": latex, "mark_scheme": ms,
            "examiner_notes": None, "difficulty": None, "difficulty_evidence": None,
            "has_diagram": diagram, "source_page": page, "source_file": SRC}


PROOF = "Proof"
ALG = "Algebra and functions"
COORD = "Coordinate geometry in the (x,y) plane"
SEQ = "Sequences and series"
TRIG = "Trigonometry"
EXP = "Exponentials and logarithms"
DIFF = "Differentiation"
INT = "Integration"
VEC = "Vectors"


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
NOGRAPH = "(Solutions based entirely on graphical or numerical methods are not acceptable.)"
Q1 = ["A curve has equation", "$$y=2x^3-2x^2-2x+8$$"]
Q1A = r"Find $\frac{\mathrm{d}y}{\mathrm{d}x}$"
Q2 = [r"The quadrilateral $OABC$ has $\overrightarrow{OA}=4\mathbf{i}+2\mathbf{j}$, "
      r"$\overrightarrow{OB}=6\mathbf{i}-3\mathbf{j}$ and $\overrightarrow{OC}=8\mathbf{i}-20\mathbf{j}$."]
Q3 = ["A tank, which contained water, started to leak from a hole in its base.",
      "The volume of water in the tank 24 minutes after the leak started was 4 m$^3$",
      "The volume of water in the tank 60 minutes after the leak started was 2.8 m$^3$",
      r"The volume of water, $V$ m$^3$, in the tank $t$ minutes after the leak started, can be described by a linear "
      r"model between $V$ and $t$."]
Q3A = "Find an equation linking $V$ with $t$."
Q4 = [r"[Figure 1: the curve $y=\mathrm{g}(x)$, coming down from the upper left, crossing the $y$-axis at $R(0, 5)$ "
      r"and the $x$-axis at $P(2, 0)$, with a minimum at $M(4, -1.5)$, then rising through $Q(7, 0)$.]",
      r"Figure 1 shows a sketch of the curve with equation $y=\mathrm{g}(x)$.",
      "The curve has a single turning point, a minimum, at the point $M(4, -1.5)$.",
      "The curve crosses the $x$-axis at two points, $P(2, 0)$ and $Q(7, 0)$.",
      "The curve crosses the $y$-axis at a single point $R(0, 5)$."]
Q5 = [r"$$\mathrm{f}(x)=x^3+3x^2-4x-12$$"]
Q5A = r"Using the factor theorem, explain why $\mathrm{f}(x)$ is divisible by $(x+3)$."
Q7A = r"Expand $\left(1+\frac{3}{x}\right)^2$ simplifying each term."
Q7B = ["Use the binomial expansion to find, in ascending powers of $x$, the first four terms in the expansion of",
       r"$$\left(1+\frac{3}{4}x\right)^6$$", "simplifying each term."]
Q8 = [r"[Figure 2: the curve $y=\sqrt{x}$ rising from $O$; the region $R$ under the curve, above the $x$-axis and "
      r"between the vertical lines $x=1$ and $x=a$, is shaded.]",
      r"Figure 2 shows a sketch of the curve with equation $y=\sqrt{x},\quad x\geqslant0$",
      r"The region $R$, shown shaded in Figure 2, is bounded by the curve, the line with equation $x=1$, the $x$-axis "
      r"and the line with equation $x=a$, where $a$ is a constant.",
      "Given that the area of $R$ is 10"]
Q10 = ["A circle $C$ has centre $(2, 5)$. Given that the point $P(-2, 3)$ lies on $C$."]
Q11IIA = ["A student’s attempt at the question",
          r"“Solve, for $-90^\circ<x<90^\circ$, the equation $7\tan x=8\sin x$”", "is set out below.",
          r"$$\begin{aligned}&7\tan x=8\sin x\\&7\times\frac{\sin x}{\cos x}=8\sin x\\&7\sin x=8\sin x\cos x\\"
          r"&7=8\cos x\\&\cos x=\frac{7}{8}\\&x=29.0^\circ\text{ (to 3 sf)}\end{aligned}$$",
          "Identify two mistakes made by this student, giving a brief explanation of each mistake."]
FIG3 = (r"[Figure 3: the curve $C$ starting at $O$, dipping just below the $x$-axis, crossing it and rising to the "
        r"right; the straight line $l$ with positive gradient, crossing the negative $y$-axis and meeting $C$ at the "
        r"point $A$, above the $x$-axis.]")
Q12 = [FIG3,
       r"Figure 3 shows a sketch of the curve $C$ with equation $y=3x-2\sqrt{x},\ x\geqslant0$ and the line $l$ with "
       r"equation $y=8x-16$",
       "The line cuts the curve at point $A$ as shown in Figure 3."]
Q13 = ["The growth of pond weed on the surface of a pond is being investigated.",
       "The surface area of the pond covered by the weed, $A$ m$^2$, can be modelled by the equation",
       r"$$A=0.2\mathrm{e}^{0.3t}$$", "where $t$ is the number of days after the start of the investigation."]
Q13G = "Given that the pond has a surface area of 100 m$^2$,"
Q13C = ["find, to the nearest hour, the time taken, according to the model, for the surface of the pond to be fully "
        "covered by the weed."]

LATEX = {
    "01a": L(*Q1, Q1A),
    "01b": L(*Q1, "(a) " + Q1A, "(b) Hence find the range of values of $x$ for which $y$ is increasing.",
             "Write your answer in set notation."),
    "02a": L(*Q2, r"Find $\overrightarrow{AB}$."),
    "02b": L(*Q2, "Show that quadrilateral $OABC$ is a trapezium."),
    "03a": L(*Q3, Q3A),
    "03b": L(*Q3, "(a) " + Q3A, "Use this model to find", "(b) (i) the initial volume of water in the tank,",
             "(ii) the time taken for the tank to empty."),
    "03c": L(*Q3, "Suggest a reason why this linear model may not be suitable."),
    "04a": L(*Q4, r"State the coordinates of the turning point on the curve with equation $y=2\mathrm{g}(x)$."),
    "04b": L(*Q4, "State the largest root of the equation", r"$$\mathrm{g}(x+1)=0$$"),
    "04c": L(*Q4, r"State the range of values of $x$ for which $\mathrm{g}'(x)\leqslant0$"),
    "04d": L(*Q4, r"Given that the equation $\mathrm{g}(x)+k=0$, where $k$ is a constant, has no real roots,",
             "state the range of possible values for $k$."),
    "05a": L(*Q5, Q5A),
    "05b": L(*Q5, "(a) " + Q5A, r"(b) Hence fully factorise $\mathrm{f}(x)$."),
    "05c": L(*Q5, r"Show that $\frac{x^3+3x^2-4x-12}{x^3+5x^2+6x}$ can be written in the form $A+\frac{B}{x}$ where "
                  r"$A$ and $B$ are integers to be found."),
    "06i": L("Use a counter example to show that the following statement is false.",
             r"“$n^2-n-1$ is a prime number, for $3\leqslant n\leqslant10$.”"),
    "06ii": L("Prove that the following statement is always true.",
              "“The difference between the cube and the square of an odd number is even.”",
              r"For example $5^3-5^2=100$ is even."),
    "07a": L(Q7A),
    "07b": L(*Q7B),
    "07c": L("(a) " + Q7A, "(b) " + Q7B[0], *Q7B[1:], "(c) Hence find the coefficient of $x$ in the expansion of",
             r"$$\left(1+\frac{3}{x}\right)^2\left(1+\frac{3}{4}x\right)^6$$"),
    "08a": L(*Q8, "find, in simplest form, the value of", r"(i) $\displaystyle\int_1^a\sqrt{8x}\,\mathrm{d}x$",
             r"(ii) $\displaystyle\int_0^a\sqrt{x}\,\mathrm{d}x$"),
    "08b": L(*Q8, "show that $a=2^k$, where $k$ is a rational constant to be found."),
    "09": L("Find any real values of $x$ such that", r"$$2\log_4(2-x)-\log_4(x+5)=1$$"),
    "10a": L(*Q10, "find an equation for $C$."),
    "10b": L(*Q10, "The line $l$ is the tangent to $C$ at the point $P$. The point $Q(2, k)$ lies on $l$.",
             "Find the value of $k$."),
    "11i": L(r"Solve, for $-90^\circ\leqslant\theta<270^\circ$, the equation,", r"$$\sin(2\theta+10^\circ)=-0.6$$",
             "giving your answers to one decimal place."),
    "11iia": L(*Q11IIA),
    "11iib": L("(ii) (a) " + Q11IIA[0], *Q11IIA[1:], "(b) Find the smallest positive solution to the equation",
               r"$$7\tan(4\alpha+199^\circ)=8\sin(4\alpha+199^\circ)$$"),
    "12a": L(*Q12, "Using algebra, find the $x$ coordinate of point $A$."),
    "12b": L(*Q12,
             r"[Figure 4: the curve $C$ and the line $l$ as in Figure 3, with $l$ now dashed, and a solid vertical line "
             r"through the point where $C$ crosses the $x$-axis; the region $R$, left unshaded, is bounded by this "
             r"vertical line on the left, by $C$ above (from the vertical line to $A$) and by $l$ below and to the "
             r"right; everything else is shaded.]",
             "The region $R$ is shown unshaded in Figure 4. Identify the inequalities that define $R$."),
    "13a": L(*Q13, "State the surface area of the pond covered by the weed at the start of the investigation."),
    "13b": L(*Q13, "Find the rate of increase of the surface area of the pond covered by the weed, in m$^2$/day, "
                   "exactly 5 days after the start of the investigation."),
    "13c": L(*Q13, Q13G, *Q13C),
    "13d": L(*Q13, Q13G, "(c) " + Q13C[0],
             "The pond is observed for one month and by the end of the month 90% of the surface area of the pond was "
             "covered by the weed.",
             "(d) Evaluate the model in light of this information, giving a reason for your answer."),
    "14": L(r"[Figure 5: the curve $C$, a cubic crossing the $x$-axis to the left of the $y$-axis, rising to a maximum "
            r"to the left of the $y$-axis, then falling to touch the $x$-axis at a minimum to the right of the "
            r"$y$-axis and rising again; the region $R$ between $C$ and the $x$-axis, from the vertical line through "
            r"the maximum to the point where $C$ touches the $x$-axis, is shaded.]",
            "Figure 5 shows a sketch of the curve $C$ with equation $y=(x-2)^2(x+3)$",
            r"The region $R$, shown shaded in Figure 5, is bounded by $C$, the vertical line passing through the "
            r"maximum turning point of $C$ and the $x$-axis.",
            "Find the exact area of $R$.", NOGRAPH),
}

DYDX = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
R_ = r"\text{“}r\text{”}^2"

# Earlier parts shown where a part needs their result (standalone sweep, 2026-10-10).
LATEX.update({
    "02b": L(
        r"The quadrilateral $OABC$ has $\overrightarrow{OA}=4\mathbf{i}+2\mathbf{j}$, $\overrightarrow{OB}=6\mathbf{i}-3\mathbf{j}$ and $\overrightarrow{OC}=8\mathbf{i}-20\mathbf{j}$.",
        r"(a) Find $\overrightarrow{AB}$.",
        r"(b) Show that quadrilateral $OABC$ is a trapezium.",
    ),
    "05c": L(
        r"$$\mathrm{f}(x)=x^3+3x^2-4x-12$$",
        r"(a) Using the factor theorem, explain why $\mathrm{f}(x)$ is divisible by $(x+3)$.",
        r"(b) Hence fully factorise $\mathrm{f}(x)$.",
        r"(c) Show that $\frac{x^3+3x^2-4x-12}{x^3+5x^2+6x}$ can be written in the form $A+\frac{B}{x}$ where $A$ and $B$ are integers to be found.",
    ),
    "12b": L(
        r"[Figure 3: the curve $C$ starting at $O$, dipping just below the $x$-axis, crossing it and rising to the right; the straight line $l$ with positive gradient, crossing the negative $y$-axis and meeting $C$ at the point $A$, above the $x$-axis.]",
        r"Figure 3 shows a sketch of the curve $C$ with equation $y=3x-2\sqrt{x},\ x\geqslant0$ and the line $l$ with equation $y=8x-16$",
        r"The line cuts the curve at point $A$ as shown in Figure 3.",
        r"(a) Using algebra, find the $x$ coordinate of point $A$.",
        r"(b) [Figure 4: the curve $C$ and the line $l$ as in Figure 3, with $l$ now dashed, and a solid vertical line through the point where $C$ crosses the $x$-axis; the region $R$, left unshaded, is bounded by this vertical line on the left, by $C$ above (from the vertical line to $A$) and by $l$ below and to the right; everything else is shaded.]",
        r"The region $R$ is shown unshaded in Figure 4. Identify the inequalities that define $R$.",
    ),
})

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", DIFF, "7.2", 2, LATEX["01a"],
      [rf"M1 (AO 1.1b): $y=2x^3-2x^2-2x+8\Rightarrow{DYDX}=6x^2-4x-2$. Notes: Attempts to differentiate. Allow for two "
       rf"correct terms un-simplified",
       rf"A1 (AO 1.1b): $y=2x^3-2x^2-2x+8\Rightarrow{DYDX}=6x^2-4x-2$. Notes: ${DYDX}=6x^2-4x-2$"],
      False, 2),
    e("01b", "1(b)", DIFF, "7.3, 2.5", 4, LATEX["01b"],
      [rf"M1 (AO 1.1b): Attempts $6x^2-4x-2>0\Rightarrow(6x+2)(x-1)>0$. Notes: Attempts to find the critical values of "
       rf"their ${DYDX}>0$ or their ${DYDX}=0$",
       r"A1 (AO 1.1b): $x=-\frac{1}{3},1$. Notes: Correct critical values $x=-\frac{1}{3},1$",
       r"M1 (AO 1.1b): Chooses outside region. Notes: Chooses the outside region",
       r"A1 (AO 2.5): $\left\{x:x<-\frac{1}{3}\right\}\cup\{x:x>1\}$. Notes: $\left\{x:x<-\frac{1}{3}\right\}\cup"
       r"\{x:x>1\}$ or $\left\{x:x\in\mathrm{R}\ x<-\frac{1}{3}\text{ or }x>1\right\}$ Accept also "
       r"$\left\{x:x\leqslant-\frac{1}{3}\right\}\cup\{x:x\geqslant1\}$"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", VEC, "9.4, 9.3", 2, LATEX["02a"],
      [r"M1 (AO 1.1b): $\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}=6\mathbf{i}-3\mathbf{j}-"
       r"(4\mathbf{i}+2\mathbf{j})$. Notes: Attempts $\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}$ or "
       r"equivalent. This may be implied by one correct component",
       r"A1 (AO 1.1b): $=2\mathbf{i}-5\mathbf{j}$. Notes: $2\mathbf{i}-5\mathbf{j}$"],
      False, 4),
    e("02b", "2(b)", VEC, "9.5, 9.3", 2, LATEX["02b"],
      [r"M1 (AO 1.1b): Explains that $\overrightarrow{OC}$ is parallel to $\overrightarrow{AB}$ as "
       r"$8\mathbf{i}-20\mathbf{j}=4\times(2\mathbf{i}-5\mathbf{j})$. Notes: Attempts to compare vectors "
       r"$\overrightarrow{OC}$ and $\overrightarrow{AB}$ by considering their directions",
       r"A1 (AO 2.4): As $\overrightarrow{OC}=4\times\overrightarrow{AB}$ it is parallel to it and not the same length "
       r"Hence $OABC$ is a trapezium. Notes: Fully explains why $OABC$ is a trapezium. (The candidate is required to "
       r"state that $OC$ is parallel to $AB$ but not the same length as it.)"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", COORD, "3.1", 4, LATEX["03a"],
      [r"B1 (AO 3.3): Uses or implies that $V=at+b$. Notes: Uses or implies that $V=at+b$ You may award this at their "
       r"final line but it must be $V=\mathrm{f}(t)$",
       r"M1 (AO 3.1b): Uses both $4=24a+b$ and $2.8=60a+b$ to get either $a$ or $b$. Notes: Awarded for translating the "
       r"problem in context and starting to solve. It is scored when both $4=24a+b$ and $2.8=60a+b$ are written down and "
       r"the candidate proceeds to find either $a$ or $b$. You may just see a line $\pm\frac{4-2.8}{60-24}$",
       r"M1 (AO 1.1b): Uses both $4=24a+b$ and $2.8=60a+b$ to get both $a$ and $b$. Notes: Uses $4=24a+b$ and "
       r"$2.8=60a+b$ to find both $a$ and $b$",
       r"A1 (AO 1.1b): $\Rightarrow V=-\frac{1}{30}t+4.8$. Notes: $V=-\frac{1}{30}t+4.8$ or exact equivalent. Eg "
       r"$30V+t=144$"],
      False, 6),
    e("03b", "3(b)", COORD, "3.1", 3, LATEX["03b"],
      [r"B1ft (AO 3.4): (i) States that the initial volume is 4.8 m$^3$. Notes: Follow through on their ‘$b$’",
       r"M1 (AO 3.4): (ii) Attempts to solve $0=-\frac{1}{30}t+4.8$. Notes: States that $V=0$ and finds $t$ by "
       r"attempting to solve their $0=-\frac{1}{30}t+4.8$",
       r"A1 (AO 1.1b): States 144 minutes. Notes: States 144 minutes"],
      False, 6),
    e("03c", "3(c)", COORD, "3.1", 1, LATEX["03c"],
      [r"B1 (AO 3.5b): States any logical reason • The tank will leak more quickly at the start due to the greater "
       r"water pressure • The hole will probably get larger and so will start to leak more quickly • Sediment could "
       r"cause the leak to be plugged and so the tank would not empty. Notes: States any logical reason. There must be "
       r"a statement and a reason that matches See scheme"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", ALG, "2.8", 1, LATEX["04a"],
      [r"B1 (AO 1.2): $(4,-3)$. Notes: See m/scheme"],
      True, 8),
    e("04b", "4(b)", ALG, "2.8", 1, LATEX["04b"],
      [r"B1 (AO 1.1b): $x=6$. Notes: See m/scheme"],
      True, 8),
    e("04c", "4(c)", DIFF, "7.3", 1, LATEX["04c"],
      [r"B1 (AO 1.1b): $x\leqslant4$. Notes: See m/scheme"],
      True, 8),
    e("04d", "4(d)", ALG, "2.8, 2.7", 1, LATEX["04d"],
      [r"B1 (AO 2.2a): $k>1.5$. Notes: See m/scheme"],
      True, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", ALG, "2.6", 2, LATEX["05a"],
      [r"M1 (AO 1.1b): $\mathrm{f}(-3)=(-3)^3+3\times(-3)^2-4\times(-3)-12$. Notes: Attempts $\mathrm{f}(-3)$",
       r"A1 (AO 2.4): $\mathrm{f}(-3)=0\Rightarrow(x+3)$ is a factor $\Rightarrow$ Hence $\mathrm{f}(x)$ is divisible by "
       r"$(x+3)$. Notes: Achieves $\mathrm{f}(-3)=0$ and explains that $(x+3)$ is a factor and hence $\mathrm{f}(x)$ is "
       r"divisible by $(x+3)$."],
      False, 10),
    e("05b", "5(b)", ALG, "2.6", 3, LATEX["05b"],
      [r"M1 (AO 1.1b): $x^3+3x^2-4x-12=(x+3)(x^2-4)$. Notes: Attempts to divide by $(x+3)$ to get the quadratic factor. "
       r"By division look for the first two terms. ie $x^2+0x$ [the mark scheme shows the start of the long division of "
       r"$x^3+3x^2-4x-12$ by $x+3$, with quotient $x^2\pm0x\ldots$ and first line $x^3+3x^2$]. By inspection look for the "
       r"first and last term $x^3+3x^2-4x-12=(x+3)(x^2+\ldots x\pm4)$",
       r"dM1 (AO 1.1b): $=(x+3)(x+2)(x-2)$. Notes: For an attempt at factorising their $(x^2-4)$. (Need to check first "
       r"and last terms)",
       r"A1 (AO 1.1b): $=(x+3)(x+2)(x-2)$. Notes: $\mathrm{f}(x)=(x+3)(x+2)(x-2)$"],
      False, 10),
    e("05c", "5(c)", ALG, "2.6", 3, LATEX["05c"],
      [r"M1 (AO 3.1a): $\frac{x^3+3x^2-4x-12}{x^3+5x^2+6x}=\frac{\ldots\ldots}{x(x^2+5x+6)}$. Notes: Takes a common "
       r"factor of $x$ out of the denominator and writes the numerator in factors.",
       r"dM1 (AO 1.1b): $=\frac{(x+3)(x+2)(x-2)}{x(x+3)(x+2)}$. Notes: Further factorises the denominator and cancels",
       r"A1 (AO 2.1): $=\frac{(x-2)}{x}=1-\frac{2}{x}$. Notes: Shows that $\frac{x^3+3x^2-4x-12}{x^3+5x^2+6x}="
       r"1-\frac{2}{x}$ with no errors or omissions",
       r"ALT: Alternatively — M1 (AO 3.1a): Alternatively rewrites to $x^3+3x^2-4x-12=A(x^3+5x^2+6x)+B(x^2+5x+6)$",
       r"ALT: Alternatively — dM1 (AO 1.1b): Alternatively compares terms or otherwise to find either $A$ or $B$",
       r"ALT: Alternatively — A1 (AO 2.1): In the alternative there must be a reference to "
       r"$x^3+3x^2-4x-12\equiv1(x^3+5x^2+6x)-2(x^2+5x+6)$ and hence $\frac{x^3+3x^2-4x-12}{x^3+5x^2+6x}=1-\frac{2}{x}$"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06i", "6(i)", PROOF, "1.1", 2, LATEX["06i"],
      [r"M1 (AO 1.1b): Tries at least one value in the interval Eg $4^2-4-1=11$. Notes: Attempts any $n^2-n-1$ for $n$ "
       r"in the interval. It is acceptable just to show $8^2-8-1=55$",
       r"A1 (AO 2.4): States that when $n=8$ it is FALSE and provides evidence $8^2-8-1=55=(11\times5)$ Hence NOT PRIME. "
       r"Notes: States that when $n=8$ it is FALSE and provides evidence. A comment that $55=11\times5$ and hence not "
       r"prime is required"],
      False, 12),
    e("06ii", "6(ii)", PROOF, "1.1", 4, LATEX["06ii"],
      [r"B1 (AO 3.1a): Knows that an odd number is of the form $2n+1$. Notes: See scheme for two examples of proof. Note "
       r"that Alt (i) works equally well with an odd number of the form $2n-1$ For example $(2n-1)^3-(2n-1)^2="
       r"(2n-1)^2\{2n-1-1\}=(2n-1)^2\{2n-2\}=2\times(2n-1)^2\{n-1\}$",
       r"M1 (AO 2.1): Attempts to simplify $(2n+1)^3-(2n+1)^2$",
       r"dM1 (AO 1.1b): ……….and factorise $8n^3+8n^2+2n=2(4n^3+4n^2+1n)=$",
       r"A1 (AO 2.4): with statement $2\times\ldots$ is always even",
       r"ALT: Alt (ii) — B1 (AO 3.1a): Let the odd number be ‘$n$’ and attempts $n^3-n^2$",
       r"ALT: Alt (ii) — M1 (AO 2.1): Attempts to factorise $n^3-n^2=n^2(n-1)$",
       r"ALT: Alt (ii) — dM1 (AO 1.1b): States that $n^2$ is odd (odd $\times$ odd) and $(n-1)$ is even (odd -1)",
       r"ALT: Alt (ii) — A1 (AO 2.4): States that the product is even ( odd$\times$even)"],
      False, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", ALG, "2.6", 2, LATEX["07a"],
      [r"M1 (AO 1.1b): $\left(1+\frac{3}{x}\right)^2=1+\frac{6}{x}+\frac{9}{x^2}$. Notes: Attempts "
       r"$\left(1+\frac{3}{x}\right)^2=A+\frac{B}{x}+\frac{C}{x^2}$",
       r"A1 (AO 1.1b): $\left(1+\frac{3}{x}\right)^2=1+\frac{6}{x}+\frac{9}{x^2}$. Notes: "
       r"$\left(1+\frac{3}{x}\right)^2=1+\frac{6}{x}+\frac{9}{x^2}$"],
      False, 14),
    e("07b", "7(b)", SEQ, "4.1", 4, LATEX["07b"],
      [r"B1 (AO 1.1b): $\left(1+\frac{3}{4}x\right)^6=1+6\times\left(\frac{3}{4}x\right)+\ldots$ Notes: First two terms "
       r"correct, may be un-simplified",
       r"M1 (AO 1.1b): $\left(1+\frac{3}{4}x\right)^6=1+6\times\left(\frac{3}{4}x\right)+\frac{6\times5}{2}\times"
       r"\left(\frac{3}{4}x\right)^2+\frac{6\times5\times4}{3\times2}\times\left(\frac{3}{4}x\right)^3+\ldots$ Notes: "
       r"Attempts the binomial expansion. Implied by the correct coefficient and power of $x$ seen at least once in term "
       r"3 or 4",
       r"A1 (AO 1.1b): $\left(1+\frac{3}{4}x\right)^6=1+6\times\left(\frac{3}{4}x\right)+\frac{6\times5}{2}\times"
       r"\left(\frac{3}{4}x\right)^2+\frac{6\times5\times4}{3\times2}\times\left(\frac{3}{4}x\right)^3+\ldots$ Notes: "
       r"Binomial expansion correct and un-simplified",
       r"A1 (AO 1.1b): $=1+\frac{9}{2}x+\frac{135}{16}x^2+\frac{135}{16}x^3+\ldots$ Notes: Binomial expansion correct and "
       r"simplified."],
      False, 14),
    e("07c", "7(c)", SEQ, "4.1, 2.6", 2, LATEX["07c"],
      [r"M1 (AO 2.1): $\left(1+\frac{3}{x}\right)^2\left(1+\frac{3}{4}x\right)^6=\left(1+\frac{6}{x}+\frac{9}{x^2}\right)"
       r"\left(1+\frac{9}{2}x+\frac{135}{16}x^2+\frac{135}{16}x^3+\ldots\right)$ Coefficient of $x=\frac{9}{2}+6\times"
       r"\frac{135}{16}+9\times\frac{135}{16}=\frac{2097}{16}$. Notes: Combines all relevant terms for their "
       r"$\left(1+\frac{A}{x}+\frac{B}{x^2}\right)\left(1+Cx+Dx^2+Ex^3+\ldots\right)$ to find the coefficient of $x$.",
       r"A1 (AO 1.1b): Coefficient of $x=\frac{9}{2}+6\times\frac{135}{16}+9\times\frac{135}{16}=\frac{2097}{16}$. Notes: "
       r"Fully correct"],
      False, 14),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", INT, "8.3, 8.2", 4, LATEX["08a"],
      [r"M1 (AO 2.2a): (i) $\int_1^a\sqrt{8x}\,\mathrm{d}x=\sqrt{8}\times\int_1^a\sqrt{x}\,\mathrm{d}x=10\sqrt{8}="
       r"20\sqrt{2}$. Notes: For deducing that $\int_1^a\sqrt{8x}\,\mathrm{d}x=\sqrt{8}\times\int_1^a\sqrt{x}\,"
       r"\mathrm{d}x$ attempting to multiply $\int_1^a\sqrt{x}\,\mathrm{d}x$ by $\sqrt{8}$",
       r"A1 (AO 1.1b): (i) $\int_1^a\sqrt{8x}\,\mathrm{d}x=\sqrt{8}\times\int_1^a\sqrt{x}\,\mathrm{d}x=10\sqrt{8}="
       r"20\sqrt{2}$. Notes: $20\sqrt{2}$ or exact equivalent",
       r"M1 (AO 2.1): (ii) $\int_0^a\sqrt{x}\,\mathrm{d}x=\int_0^1\sqrt{x}\,\mathrm{d}x+\int_1^a\sqrt{x}\,\mathrm{d}x="
       r"\left[\frac{2}{3}x^{\frac{3}{2}}\right]_0^1+10=\frac{32}{3}$. Notes: For identifying and attempting to use "
       r"$\int_0^a\sqrt{x}\,\mathrm{d}x=\int_0^1\sqrt{x}\,\mathrm{d}x+\int_1^a\sqrt{x}\,\mathrm{d}x$",
       r"A1 (AO 1.1b): (ii) $\int_0^a\sqrt{x}\,\mathrm{d}x=\int_0^1\sqrt{x}\,\mathrm{d}x+\int_1^a\sqrt{x}\,\mathrm{d}x="
       r"\left[\frac{2}{3}x^{\frac{3}{2}}\right]_0^1+10=\frac{32}{3}$. Notes: For $\frac{32}{3}$ or exact equivalent"],
      True, 16),
    e("08b", "8(b)", INT, "8.3, 8.2, 2.1", 4, LATEX["08b"],
      [r"M1 (AO 1.1b): $R=\int_1^a\sqrt{x}\,\mathrm{d}x=\left[\frac{2}{3}x^{\frac{3}{2}}\right]_1^a$. Notes: Attempts to "
       r"integrate, $x^{\frac{1}{2}}\to x^{\frac{3}{2}}$",
       r"A1 (AO 1.1b): $R=\int_1^a\sqrt{x}\,\mathrm{d}x=\left[\frac{2}{3}x^{\frac{3}{2}}\right]_1^a$. Notes: "
       r"$\int_1^a\sqrt{x}\,\mathrm{d}x=\left[\frac{2}{3}x^{\frac{3}{2}}\right]_1^a$",
       r"dM1 (AO 3.1a): $\frac{2}{3}a^{\frac{3}{2}}-\frac{2}{3}=10\Rightarrow a^{\frac{3}{2}}=16\Rightarrow "
       r"a=16^{\frac{2}{3}}$. Notes: For a whole strategy to find $a$. In the scheme it is awarded for setting "
       r"$\left[\ldots x^{\frac{3}{2}}\right]_1^a=10$, using both limits and proceeding using correct index work to find "
       r"$a$.",
       r"A1 (AO 2.1): $\Rightarrow a=2^{4\times\frac{2}{3}}=2^{\frac{8}{3}}$. Notes: $a=2^{4\times\frac{2}{3}}="
       r"2^{\frac{8}{3}}$",
       r"ALT: Alternatively — dM1 (AO 3.1a): Alternatively a candidate could assume $a=2^k$. In such a case it is awarded "
       r"for setting $\left[\ldots x^{\frac{3}{2}}\right]_1^{2^k}=10$, using both limits and proceeding using correct "
       r"index work to $k=\ldots$",
       r"ALT: Alternatively — A1 (AO 2.1): In the alternative case, a further statement must be seen following "
       r"$k=\frac{8}{3}$ Hence True"],
      True, 16),

    # ---------------- Q9 ----------------
    e("09", "9", EXP, "6.4, 2.3", 6, LATEX["09"],
      [r"M1 (AO 1.1b): Uses the power law $\log_4(2-x)^2-\log_4(x+5)=1$. Notes: Uses the power law of logs "
       r"$2\log_4(2-x)=\log_4(2-x)^2$",
       r"M1 (AO 1.1b): Uses the subtraction law $\log_4\frac{(2-x)^2}{(x+5)}=1$. Notes: Uses the subtraction law of logs "
       r"following the above $\log_4(2-x)^2-\log_4(x+5)=\log_4\frac{(2-x)^2}{(x+5)}$",
       r"dM1 (AO 3.1a): $\frac{(2-x)^2}{(x+5)}=4\to3\text{TQ in }x$. Notes: This can be awarded for the overall strategy "
       r"leading to a 3TQ in $x$. It is dependent upon the correct use of both previous M's and for undoing the logs to "
       r"reach a 3TQ equation in $x$",
       r"A1 (AO 1.1b): $x^2-8x-16=0$. Notes: For a correct equation in $x$",
       r"M1 (AO 1.1b): $(x-4)^2=32\Rightarrow x=$ Notes: For the correct method of solving their 3TQ $=0$",
       r"A1 (AO 2.3): $x=4-4\sqrt{2}$ oe only. Notes: $x=4-4\sqrt{2}$ or exact equivalent only. (For example accept "
       r"$x=4-\sqrt{32}$ )",
       r"ALT: Alternatively — M1 (AO 1.1b): Alternatively uses the addition law following use of $1=\log_44$ That is "
       r"$1+\log_4(x+5)=\log_44(x+5)$"],
      False, 18),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", COORD, "3.2", 3, LATEX["10a"],
      [rf"M1 (AO 1.1b): Attempts to find the radius $\sqrt{{(2--2)^2+(5-3)^2}}$ or radius$^2$. Notes: As scheme or "
       rf"states form of circle is $(x-2)^2+(y-5)^2={R_}$",
       rf"M1 (AO 1.1b): Attempts $(x-2)^2+(y-5)^2={R_}$. Notes: As scheme or substitutes $(-2,3)$ into "
       rf"$(x-2)^2+(y-5)^2={R_}$",
       r"A1 (AO 1.1b): Correct equation $(x-2)^2+(y-5)^2=20$. Notes: For a correct equation",
       r"ALT: If students use $x^2+y^2+2fx+2gy+c=0$ — M1: $f=2$, $g=5$ [sic: the main scheme's centre is $(2, 5)$]",
       r"ALT: If students use $x^2+y^2+2fx+2gy+c=0$ — M1: substitutes $(2,5)$ to find value of $c$ [sic: the main "
       r"scheme substitutes the point $(-2,3)$; its centre is $(2, 5)$]",
       r"ALT: If students use $x^2+y^2+2fx+2gy+c=0$ — A1: $x^2+y^2-4x-10y+9=0$"],
      False, 20),
    e("10b", "10(b)", COORD, "3.2, 3.1", 5, LATEX["10b"],
      [r"M1 (AO 1.1b): Gradient of radius $OP$ where $O$ is the centre of $C=\frac{5-3}{2--2}=\left(\frac{1}{2}\right)$. "
       r"Notes: Attempts to find the gradient of $OP$ where $O$ is the centre of $C$",
       r"dM1 (AO 3.1a): Equation of $l$ is $-2=\frac{y-3}{x+2}$. Notes: For a complete strategy of finding the equation "
       r"of $l$ using the perpendicular gradient to $OP$ and the point $(-2,3)$..",
       r"A1 (AO 1.1b): Any correct form $y=-2x-1$. Notes: Any correct form of $l$ Eg $y=-2x-1$",
       r"M1 (AO 2.1): Method of finding $k$ Substitute $x=2$ into their $y=-2x-1$. Notes: Scored for the key step of "
       r"finding $k$. In this method they are required to substitute $(2,k)$ in their $y=-2x-1$ and solve for $k$.",
       r"A1 (AO 1.1b): $k=-5$. Notes: $k=-5$",
       r"ALT: Alt using Pythagoras’ theorem — M1: Attempts Pythagoras to find both $PQ$ and $OQ$ in terms of $k$ (where "
       r"$O$ is centre of $C$)",
       r"ALT: Alt using Pythagoras’ theorem — dM1: For the complete strategy of using Pythagoras theorem on triangle "
       r"$POQ$ to form an equation in $k$",
       r"ALT: Alt using Pythagoras’ theorem — A1: A correct equation in $k$ Eg. $20+(k-3)^2+16=(k-5)^2$",
       r"ALT: Alt using Pythagoras’ theorem — M1: Scored for a correct attempt to solve their quadratic to find $k$.",
       r"ALT: Alt using Pythagoras’ theorem — A1: $k=-5$"],
      False, 20),

    # ---------------- Q11 ----------------
    e("11i", "11(i)", TRIG, "5.4", 5, LATEX["11i"],
      [r"M1 (AO 1.1b): $(2\theta+10^\circ)=\arcsin(-0.6)$. Notes: Attempts $\arcsin(-0.6)$ implied by any correct answer",
       r"A1 (AO 1.1b): $(2\theta+10^\circ)=-143.13^\circ,-36.87^\circ,216.87^\circ,323.13^\circ$ (Any two). Notes: Any two "
       r"of $-143.13^\circ,-36.87^\circ,216.87^\circ,323.13^\circ$",
       r"dM1 (AO 1.1b): Correct order to find $\theta=\ldots$ Notes: Correct method to find any value of $\theta$",
       r"A1 (AO 1.1b): Two of $\theta=-76.6^\circ,-23.4^\circ,103.4^\circ,156.6^\circ$. Notes: Any two of "
       r"$\theta=-76.6^\circ,-23.4^\circ,103.4^\circ,156.6^\circ$.",
       r"A1 (AO 2.1): $\theta=-76.6^\circ,-23.4^\circ,103.4^\circ,156.6^\circ$, only. Notes: A full solution leading to "
       r"all four answers and no extras $\theta=-76.6^\circ,-23.4^\circ,103.4^\circ,156.6^\circ$, only"],
      False, 22),
    e("11iia", "11(ii)(a)", TRIG, "5.4, 5.3", 2, LATEX["11iia"],
      [r"B1 (AO 2.3): Explains that the student has not considered the negative value of $x\ (=-29.0^\circ)$ when "
       r"solving $\cos x=\frac{7}{8}$. Notes: See scheme",
       r"B1 (AO 2.3): Explains that the student should check if any solutions of $\sin x=0$ (the cancelled term) are "
       r"solutions of the given equation. $x=0^\circ$ should have been included as a solution. Notes: See scheme"],
      False, 22),
    e("11iib", "11(ii)(b)", TRIG, "5.4", 2, LATEX["11iib"],
      [r"M1 (AO 2.2a): Attempts to solve $4\alpha+199^\circ=(360-29.0)^\circ$. Notes: For deducing the smallest positive "
       r"solution occurs when $4\alpha+199^\circ=(360-29.0)^\circ$",
       r"A1 (AO 1.1b): $\alpha=33.0^\circ$. Notes: $\alpha=33^\circ$"],
      False, 22),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", ALG, "2.4, 2.3", 5, LATEX["12a"],
      [r"B1 (AO 1.1a): Sets $3x-2\sqrt{x}=8x-16$. Notes: Sets the equations equal to each other and achieves a correct "
       r"equation",
       r"M1 (AO 3.1a): $2\sqrt{x}=16-5x$, $4x=(16-5x)^2\Rightarrow x=\ldots$ Notes: Awarded for the key step in solving "
       r"the problem. This can be awarded via two routes. Both routes must lead to a value for $x$. • Making the "
       r"$\sqrt{x}$ term the subject and squaring both sides (not each term) • Recognising that this is a quadratic in "
       r"$\sqrt{x}$ and attempting to factorise $\Rightarrow(5\sqrt{x}\pm8)(\sqrt{x}\pm2)=0$",
       r"A1 (AO 1.1b): $25x^2-164x+256=0$. Notes: A correct intermediate line $25x^2-164x+256=0$ or "
       r"$(5\sqrt{x}-8)(\sqrt{x}+2)=0$",
       r"M1 (AO 1.1b): $(25x-64)(x-4)=0\Rightarrow x=\ldots$ Notes: A correct method to find at least one value for $x$. "
       r"Way One it is for factorising (usual rules), Way Two it is squaring at least one result of their $\sqrt{x}$",
       r"A1 (AO 2.3): $x=\frac{64}{25}$ only. Notes: Realises that $x=\frac{64}{25}$ is the only solution "
       r"$x=\frac{64}{25},4$ is A0",
       r"ALT: Second scheme column — M1 (AO 3.1a): $5x+2\sqrt{x}-16=0\Rightarrow(5\sqrt{x}\pm8)(\sqrt{x}\pm2)=0$",
       r"ALT: Second scheme column — A1 (AO 1.1b): $(5\sqrt{x}-8)(\sqrt{x}+2)=0$",
       r"ALT: Second scheme column — M1 (AO 1.1b): $\sqrt{x}=\frac{8}{5},(-2)\Rightarrow x=\ldots$"],
      True, 24),
    e("12b", "12(b)", ALG, "2.5", 3, LATEX["12b"],
      [r"M1 (AO 2.1): Attempts to solve $3x-2\sqrt{x}=0$. Notes: Attempts to solve $3x-2\sqrt{x}=0$ For example Allow "
       r"$3x=2\sqrt{x}\Rightarrow9x^2=4x\Rightarrow x=\ldots$ Allow $3x=2\sqrt{x}\Rightarrow x^{\frac{1}{2}}="
       r"\frac{2}{3}\Rightarrow x=\ldots$",
       r"A1 (AO 1.1b): Correct solution $x=\frac{4}{9}$. Notes: Correct solution to $3x-2\sqrt{x}=0\Rightarrow "
       r"x=\frac{4}{9}$",
       r"B1ft (AO 1.1b): $y\leqslant3x-2\sqrt{x},\ y>8x-16\ x\geqslant\frac{4}{9}$. Notes: For a $\textbf{consistent}$ "
       r"solution defining $R$ using either convention Either $y\leqslant3x-2\sqrt{x},\ y>8x-16\ x\geqslant\frac{4}{9}$ "
       r"Or $y<3x-2\sqrt{x},\ y\geqslant8x-16\ x>\frac{4}{9}$"],
      True, 24),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", EXP, "6.7", 1, LATEX["13a"],
      [r"B1 (AO 3.4): 0.2 m$^2$. Notes: 0.2 m$^2$ oe"],
      False, 28),
    e("13b", "13(b)", EXP, "6.2, 6.7", 2, LATEX["13b"],
      [r"M1 (AO 3.1b): $A=0.2\mathrm{e}^{0.3t}$ Rate of change $=$ gradient $=\frac{\mathrm{d}A}{\mathrm{d}t}="
       r"0.06\mathrm{e}^{0.3t}$. Notes: Links rate of change to gradient and differentiates $0.2\mathrm{e}^{0.3t}\to "
       r"k\mathrm{e}^{0.3t}$",
       r"A1 (AO 1.1b): At $t=5\Rightarrow$ Rate of Growth is $0.06\mathrm{e}^{1.5}=0.269$ m$^2$/day. Notes: Correct answer "
       r"0.269 m$^2$/day"],
      False, 28),
    e("13c", "13(c)", EXP, "6.7, 6.3", 4, LATEX["13c"],
      [r"M1 (AO 3.1a): $100=0.2\mathrm{e}^{0.3t}\Rightarrow\mathrm{e}^{0.3t}=500$. Notes: Substitutes $A=100$ and proceeds "
       r"to $\mathrm{e}^{0.3t}=k$",
       r"A1 (AO 1.1b): $100=0.2\mathrm{e}^{0.3t}\Rightarrow\mathrm{e}^{0.3t}=500$. Notes: $\mathrm{e}^{0.3t}=500$",
       r"M1 (AO 1.1b): $\Rightarrow t=\frac{\ln(500)}{0.3}=20.7$ days 20 days 17 hours. Notes: Correct method when "
       r"proceeding from $\mathrm{e}^{0.3t}=k\Rightarrow t=\ldots$",
       r"A1 (AO 3.2a): $\Rightarrow t=\frac{\ln(500)}{0.3}=20.7$ days 20 days 17 hours. Notes: 20 days 17 hours"],
      False, 28),
    e("13d", "13(d)", EXP, "6.7", 1, LATEX["13d"],
      [r"B1 (AO 3.5a): The model given suggests that the pond is fully covered after 20 days 17 hours. Observed data is "
       r"inconsistent with this as the pond is only 90% covered by the end of one month (28/29/30/31 days). Hence the "
       r"model is not accurate. Notes: Valid conclusion following through on their answer to (c)."],
      False, 28),

    # ---------------- Q14 ----------------
    e("14", "14", INT, "8.3, 7.3, 2.6", 9, LATEX["14"],
      [r"B1 (AO 1.1b): $y=(x-2)^2(x+3)=(x^2-4x+4)(x+3)=x^3-1x^2-8x+12$. Notes: Expands $(x-2)^2(x+3)$ to "
       r"$x^3-1x^2-8x+12$ seen at some point in their solution. It may appear just on their integral for example.",
       rf"M1 (AO 3.1a): An attempt to find $x$ coordinate of the maximum point. To score this you must see either • an "
       rf"attempt to expand $(x-2)^2(x+3)$, an attempt to differentiate the result, followed by an attempt at solving "
       rf"${DYDX}=0$ • an attempt to differentiate $(x-2)^2(x+3)$ by the product rule followed by an attempt at solving "
       rf"${DYDX}=0$. Notes: This is a problem solving mark for knowing the method of finding the maximum point. You "
       rf"should expect to see the key points used (i) differentiation (ii) solution of their ${DYDX}=0$",
       rf"M1 (AO 1.1b): $y=x^3-1x^2-8x+12\Rightarrow{DYDX}=3x^2-2x-8$. Notes: For correctly differentiating their cubic "
       rf"with at least two terms correct (for their cubic).",
       rf"M1 (AO 1.1b): Maximum point occurs when ${DYDX}=0\Rightarrow(x-2)(3x+4)=0$. Notes: For setting their "
       rf"${DYDX}=0$ and solves using a correct method (including calculator methods)",
       r"A1 (AO 1.1b): $\Rightarrow x=-\frac{4}{3}$. Notes: $\Rightarrow x=-\frac{4}{3}$",
       r"M1 (AO 3.1a): An attempt to find the area under $y=(x-2)^2(x+3)$ between two values. To score this you must see "
       r"an attempt to expand $(x-2)^2(x+3)$ followed by an attempt at using two limits. Notes: This is a problem solving "
       r"mark for knowing how integration is used to find the area underneath a curve between two points.",
       r"M1 (AO 1.1b): Area $=\int(x^3-1x^2-8x+12)\,\mathrm{d}x=\left[\frac{x^4}{4}-\frac{x^3}{3}-4x^2+12x\right]$. "
       r"Notes: For correctly integrating their cubic with at least two correct terms (for their cubic).",
       r"M1 (AO 2.2a): Uses a top limit of 2 and a bottom limit of their $x=-\frac{4}{3}$ $R=\left[\frac{x^4}{4}-"
       r"\frac{x^3}{3}-4x^2+12x\right]_{-\frac{4}{3}}^2$. Notes: For deducing the top limit is 2, the bottom limit is "
       r"their $x=-\frac{4}{3}$ and applying these correctly within their integration.",
       r"A1 (AO 2.1): Uses $=\frac{28}{3}--\frac{1744}{81}=\frac{2500}{81}$. Notes: Shows above steps clearly and "
       r"proceeds to $R=\frac{2500}{81}$"],
      True, 30),
]

# No examiner report is published for the specimen paper, so there is nothing to apply.
W = None
REPORT = {}

# No report, so no difficulty can be judged: every part is (None, None).
RATINGS = {q: (None, None) for q in
           ["01a", "01b", "02a", "02b", "03a", "03b", "03c", "04a", "04b", "04c", "04d", "05a", "05b", "05c", "06i",
            "06ii", "07a", "07b", "07c", "08a", "08b", "09", "10a", "10b", "11i", "11iia", "11iib", "12a", "12b", "13a",
            "13b", "13c", "13d", "14"]}


def build():
    entries = [dict(d) for d in DRAFT]
    apply_report(entries, REPORT)
    keys = {q + (p or "") for q, p in map(part_key, entries)}
    if set(RATINGS) != keys:
        raise SystemExit(f"RATINGS keys differ from entries: {sorted(set(RATINGS) ^ keys)}")
    for entry in entries:
        q, p = part_key(entry)
        rating, where = RATINGS[q + (p or "")]
        if rating is not None:
            entry["difficulty"] = rating
            entry["difficulty_evidence"] = REPORT[where[0]][where[1]][1]
        # Each main line counts its code's value (B2 is one line worth 2 marks); ALT lines don't count.
        if entry["mark_scheme"] is not None and main_marks(entry["mark_scheme"]) != entry["marks"]:
            raise SystemExit(f"{entry['id']}: main mark-scheme lines are worth {main_marks(entry['mark_scheme'])} "
                             f"marks, entry has {entry['marks']}")
    return entries


if __name__ == "__main__":
    out = ensure_out_dir("drafts") / f"{P}_{S}.json"
    entries = build()
    out.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(entries)} entries, {sum(x['marks'] or 0 for x in entries)} marks -> {out}")
