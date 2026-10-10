"""Draft builder for 8MA0-01 2022-06 (AS Pure, June 2022).

Run (from the project root, with the venv active):
    python extraction/8MA0-01_2022-06.py        # writes out/drafts/8MA0-01_2022-06.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-01_2022-06.json

Everything here is transcribed from the source PDFs (read as page images
where the text layer garbles maths). Follow CLAUDE.md for every field.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report, part_key  # noqa: E402
from paths import ensure_out_dir  # noqa: E402

P, S = "8MA0-01", "2022-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "04bii"); label as printed (e.g. "4(b)(ii)")."""
    return {"id": f"{P}_{S}_Q{q}", "paper": P, "series": S, "question": label, "topic": topic,
            "spec_ref": spec, "marks": marks, "question_latex": latex, "mark_scheme": ms,
            "examiner_notes": None, "difficulty": None, "difficulty_evidence": None,
            "has_diagram": diagram, "source_page": page, "source_file": SRC}


ALG = "Algebra and functions"
COORD = "Coordinate geometry in the (x,y) plane"
SEQ = "Sequences and series"
TRIG = "Trigonometry"
EXP = "Exponentials and logarithms"
DIFF = "Differentiation"
INT = "Integration"
VEC = "Vectors"
PROOF = "Proof"


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
SHOW = ["In this question you must show all stages of your working.",
        "Solutions relying entirely on calculator technology are not acceptable."]
Q2 = [r"$$\mathrm{f}(x)=2x^3+5x^2+2x+15$$"]
Q2B = ["Find the constants $a$, $b$ and $c$ such that", r"$$\mathrm{f}(x)=(x+3)(ax^2+bx+c)$$"]
Q3 = [r"The triangle $PQR$ is such that $\overrightarrow{PQ}=3\mathbf{i}+5\mathbf{j}$ and "
      r"$\overrightarrow{PR}=13\mathbf{i}-15\mathbf{j}$"]
Q4 = [r"[Figure 1: triangle $ABC$ with base $AC=7x$ cm, $AB=(x+2)$ cm, $BC=(3x+10)$ cm, angle $60^\circ$ at $A$ and "
      r"angle $\theta^\circ$ at $C$.]",
      r"Figure 1 shows a sketch of triangle $ABC$ with $AB=(x+2)$ cm, $BC=(3x+10)$ cm, $AC=7x$ cm, angle "
      r"$BAC=60^\circ$ and angle $ACB=\theta^\circ$"]
Q4AI = "Show that $17x^2-35x-48=0$"
Q5 = ["The mass, $A$ kg, of algae in a small pond, is modelled by the equation", "$$A=pq^t$$",
      "where $p$ and $q$ are constants and $t$ is the number of weeks after the mass of algae was first recorded.",
      r"Data recorded indicates that there is a linear relationship between $t$ and $\log_{10}A$ given by the equation",
      r"$$\log_{10}A=0.03t+0.5$$"]
Q7C = ["The curve $C$ has equation", "$$y=9x-x^3$$"]
Q8 = SHOW + [r"The air pressure, $P$ kg/cm$^2$, inside a car tyre, $t$ minutes from the instant when the tyre developed "
             r"a puncture is given by the equation",
             r"$$P=k+1.4\mathrm{e}^{-0.5t}\qquad t\in\mathbb{R}\qquad t\geqslant0$$",
             "where $k$ is a constant.",
             "Given that the initial air pressure inside the tyre was 2.2 kg/cm$^2$"]
Q8B = "From the instant when the tyre developed the puncture,"
Q9A = [r"Given that $p=\log_3x$, where $x>0$, find in simplest form in terms of $p$,",
       r"(i) $\log_3\left(\frac{x}{9}\right)$", r"(ii) $\log_3\left(\sqrt{x}\right)$"]
Q10 = [r"[Figure 2: part of the curve $C$ for $x\geqslant0$, starting on the positive $y$-axis, dipping to a minimum and "
       r"rising; the tangent $l$ touches $C$ at $P$ and crosses the positive $x$-axis; the region $R$ between the "
       r"$y$-axis, $C$, $l$ and the $x$-axis is shaded.]"] + SHOW + [
       "Figure 2 shows a sketch of part of the curve $C$ with equation",
       r"$$y=\frac{1}{3}x^2-2\sqrt{x}+3\qquad x\geqslant0$$",
       "The point $P$ lies on $C$ and has $x$ coordinate 4",
       "The line $l$ is the tangent to $C$ at $P$."]
Q10A = ["Show that $l$ has equation", "$$13x-6y-26=0$$"]
Q11 = [r"[Figure 3: the circle $C$ in the first quadrant, clear of both axes, and the line $l$ sloping down from the "
       r"second quadrant, crossing the negative $y$-axis, into the fourth quadrant.]",
       "Figure 3 shows the circle $C$ with equation", "$$x^2+y^2-10x-8y+32=0$$",
       "and the line $l$ with equation", "$$2y+x+6=0$$"]
Q12 = ["A company makes drinks containers out of metal.",
       "The containers are modelled as closed cylinders with base radius $r$ cm and height $h$ cm and the capacity of "
       "each container is 355 cm$^3$",
       "The metal used",
       "• for the circular base and the curved side costs 0.04 pence/cm$^2$",
       "• for the circular top costs 0.09 pence/cm$^2$",
       "Both metals used are of negligible thickness."]
Q12A = ["Show that the total cost, $C$ pence, of the metal for one container is given by",
        r"$$C=0.13\pi r^2+\frac{28.4}{r}$$"]
Q12B = "Use calculus to find the value of $r$ for which $C$ is a minimum, giving your answer to 3 significant figures."
Q12C = (r"Using $\frac{\mathrm{d}^2C}{\mathrm{d}r^2}$ prove that the cost is minimised for the value of $r$ found in "
        r"part (b).")
Q13A = ["Show that",
        r"$$\frac{1}{\cos\theta}+\tan\theta\equiv\frac{\cos\theta}{1-\sin\theta}\qquad\theta\neq(2n+1)90^\circ\quad "
        r"n\in\mathbb{Z}$$"]

LATEX = {
    "01": L("Find", r"$$\int\left(8x^3-\frac{3}{2\sqrt{x}}+5\right)\mathrm{d}x$$", "giving your answer in simplest form."),
    "02a": L(*Q2, r"Use the factor theorem to show that $(x+3)$ is a factor of $\mathrm{f}(x)$."),
    "02b": L(*Q2, *Q2B),
    "02c": L(*Q2, "(b) " + Q2B[0], Q2B[1], r"(c) Hence show that $\mathrm{f}(x)=0$ has only one real root."),
    "02d": L(*Q2, r"Write down the real root of the equation $\mathrm{f}(x-5)=0$"),
    "03a": L(*Q3, r"Find $\overrightarrow{QR}$"),
    "03b": L(*Q3, r"(a) Find $\overrightarrow{QR}$",
             r"(b) Hence find $\left|\overrightarrow{QR}\right|$ giving your answer as a simplified surd."),
    "03c": L(*Q3, "The point $S$ lies on the line segment $QR$ so that $QS:SR=3:2$", r"Find $\overrightarrow{PS}$"),
    "04ai": L(*Q4, Q4AI),
    "04aii": L(*Q4, "(a) (i) " + Q4AI, "(ii) Hence find the value of $x$."),
    "04b": L(*Q4, "(a) (i) " + Q4AI, "(ii) Hence find the value of $x$.",
             r"(b) Hence find the value of $\theta$ giving your answer to one decimal place."),
    "05a": L(*Q5, "Use this relationship to find a complete equation for the model in the form", "$$A=pq^t$$",
             "giving the value of $p$ and the value of $q$ each to 4 significant figures."),
    "05b": L(*Q5, "With reference to the model, interpret", "(i) the value of the constant $p$,",
             "(ii) the value of the constant $q$."),
    "05c": L(*Q5, "Find, according to the model,",
             "(i) the mass of algae in the pond when $t=8$, giving your answer to the nearest 0.5 kg,",
             "(ii) the number of weeks it takes for the mass of algae in the pond to reach 4 kg."),
    "05d": L(*Q5, "State one reason why this may not be a realistic model in the long term."),
    "06a": L("Find the first 4 terms, in ascending powers of $x$, of the binomial expansion of",
             r"$$\left(3-\frac{2x}{9}\right)^8$$", "giving each term in simplest form."),
    "06b": L(r"$$\mathrm{f}(x)=\left(\frac{x-1}{2x}\right)\left(3-\frac{2x}{9}\right)^8$$",
             r"Find the coefficient of $x^2$ in the series expansion of $\mathrm{f}(x)$, giving your answer as a "
             r"simplified fraction."),
    "07a": L("Factorise completely $9x-x^3$"),
    "07b": L(*Q7C, "Sketch $C$ showing the coordinates of the points at which the curve cuts the $x$-axis."),
    "07c": L(*Q7C, "The line $l$ has equation $y=k$ where $k$ is a constant.",
             "Given that $C$ and $l$ intersect at 3 distinct points,",
             "find the range of values for $k$, writing your answer in set notation.",
             "Solutions relying on calculator technology are not acceptable."),
    "08a": L(*Q8, "state the value of $k$."),
    "08b": L(*Q8, Q8B, "find the time taken for the air pressure to fall to 1 kg/cm$^2$",
             "Give your answer in minutes to one decimal place."),
    "08c": L(*Q8, "Find the rate at which the air pressure in the tyre is decreasing exactly 2 minutes from the "
             "instant when the tyre developed the puncture.",
             "Give your answer in kg/cm$^2$ per minute to 3 significant figures."),
    "09a": L(*Q9A),
    "09b": L("(a) " + Q9A[0], *Q9A[1:], "(b) Hence, or otherwise, solve",
             r"$$2\log_3\left(\frac{x}{9}\right)+3\log_3\left(\sqrt{x}\right)=-11$$",
             "giving your answer as a simplified fraction.",
             "Solutions relying on calculator technology are not acceptable."),
    "10a": L(*Q10, *Q10A),
    "10b": L(*Q10, "(a) " + Q10A[0], Q10A[1],
             "The region $R$, shown shaded in Figure 2, is bounded by the $y$-axis, the curve $C$, the line $l$ and the "
             "$x$-axis.",
             "(b) Find the exact area of $R$."),
    "11a": L(*Q11, "Find", "(i) the coordinates of the centre of $C$,", "(ii) the radius of $C$."),
    "11b": L(*Q11, "Find the shortest distance between $C$ and $l$."),
    "12a": L(*Q12, *Q12A),
    "12b": L(*Q12, "(a) " + Q12A[0], Q12A[1], "(b) " + Q12B),
    "12c": L(*Q12, "(a) " + Q12A[0], Q12A[1], "(b) " + Q12B, "(c) " + Q12C),
    "12d": L(*Q12, "(a) " + Q12A[0], Q12A[1], "(b) " + Q12B, "(c) " + Q12C,
             "(d) Hence find the minimum value of $C$, giving your answer to the nearest integer."),
    "13a": L(*SHOW, *Q13A),
    "13b": L(*SHOW, "Given that $\\cos2x\\neq0$", "solve for $0<x<90^\\circ$",
             r"$$\frac{1}{\cos2x}+\tan2x=3\cos2x$$", "giving your answers to one decimal place."),
    "14i": L("A student states", "“if $x^2$ is greater than 9 then $x$ must be greater than 3”",
             "Determine whether or not this statement is true, giving a reason for your answer."),
    "14ii": L("Prove that for all positive integers $n$,", "$$n^3+3n^2+2n$$", "is divisible by 6"),
}

# Earlier parts shown where a part needs their result (standalone sweep, 2026-10-10).
LATEX.update({
    "02d": L(
        r"$$\mathrm{f}(x)=2x^3+5x^2+2x+15$$",
        r"(a) Use the factor theorem to show that $(x+3)$ is a factor of $\mathrm{f}(x)$.",
        r"(d) Write down the real root of the equation $\mathrm{f}(x-5)=0$",
    ),
    "03c": L(
        r"The triangle $PQR$ is such that $\overrightarrow{PQ}=3\mathbf{i}+5\mathbf{j}$ and $\overrightarrow{PR}=13\mathbf{i}-15\mathbf{j}$",
        r"(a) Find $\overrightarrow{QR}$",
        r"The point $S$ lies on the line segment $QR$ so that $QS:SR=3:2$",
        r"(c) Find $\overrightarrow{PS}$",
    ),
    "06b": L(
        r"(a) Find the first 4 terms, in ascending powers of $x$, of the binomial expansion of",
        r"$$\left(3-\frac{2x}{9}\right)^8$$",
        r"giving each term in simplest form.",
        r"$$\mathrm{f}(x)=\left(\frac{x-1}{2x}\right)\left(3-\frac{2x}{9}\right)^8$$",
        r"(b) Find the coefficient of $x^2$ in the series expansion of $\mathrm{f}(x)$, giving your answer as a simplified fraction.",
    ),
    "07b": L(
        r"(a) Factorise completely $9x-x^3$",
        r"The curve $C$ has equation",
        r"$$y=9x-x^3$$",
        r"(b) Sketch $C$ showing the coordinates of the points at which the curve cuts the $x$-axis.",
    ),
    "08b": L(
        r"In this question you must show all stages of your working.",
        r"Solutions relying entirely on calculator technology are not acceptable.",
        r"The air pressure, $P$ kg/cm$^2$, inside a car tyre, $t$ minutes from the instant when the tyre developed a puncture is given by the equation",
        r"$$P=k+1.4\mathrm{e}^{-0.5t}\qquad t\in\mathbb{R}\qquad t\geqslant0$$",
        r"where $k$ is a constant.",
        r"Given that the initial air pressure inside the tyre was 2.2 kg/cm$^2$",
        r"(a) state the value of $k$.",
        r"From the instant when the tyre developed the puncture,",
        r"(b) find the time taken for the air pressure to fall to 1 kg/cm$^2$",
        r"Give your answer in minutes to one decimal place.",
    ),
    "11b": L(
        r"[Figure 3: the circle $C$ in the first quadrant, clear of both axes, and the line $l$ sloping down from the second quadrant, crossing the negative $y$-axis, into the fourth quadrant.]",
        r"Figure 3 shows the circle $C$ with equation",
        r"$$x^2+y^2-10x-8y+32=0$$",
        r"and the line $l$ with equation",
        r"$$2y+x+6=0$$",
        r"(a) Find",
        r"(i) the coordinates of the centre of $C$,",
        r"(ii) the radius of $C$.",
        r"(b) Find the shortest distance between $C$ and $l$.",
    ),
})

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", INT, "8.2, 2.1", 4,
      LATEX["01"],
      [r"M1 (AO 1.1b): $x^n\to x^{n+1}$. Notes: For raising any correct power of $x$ by 1 including $5\to5x$ (not for $+c$) "
       r"Also allow eg $x^3\to x^{3+1}$",
       r"A1 (AO 1.1b): $\int\left(8x^3-\frac{3}{2\sqrt{x}}+5\right)\mathrm{d}x=\frac{8x^4}{4}\ldots+5x$. Notes: For 2 correct "
       r"non-fractional power terms (allow unsimplified coefficients) and may appear on separate lines. The indices must be "
       r"processed. The $+c$ does not count as a correct term here. Condone the 1 appearing as a power or denominator such "
       r"as $\frac{5x^1}{1}$ for this mark.",
       r"A1 (AO 1.1b): $=\ldots-2\times\frac{3}{2}x^{\frac{1}{2}}+\ldots$ Notes: For the correct fractional power term (allow "
       r"unsimplified) Allow eg $+-2\times1.5\sqrt{x^1}$. Also allow fractions within fractions for this mark such as "
       r"$\frac{\frac{3}{2}}{\frac{1}{2}}x^{\frac{1}{2}}$",
       r"A1 (AO 1.1b): $=2x^4-3x^{\frac{1}{2}}+5x+c$. Notes: All correct and simplified and on one line including $+c$. Allow "
       r"$-3\sqrt{x}$ or $-\sqrt{9x}$ for $-3x^{\frac{1}{2}}$. Do not accept $+-3x^{\frac{1}{2}}$ for this mark. Award once a "
       r"correct expression is seen and isw but if there is any additional/incorrect notation and no correct expression "
       r"has been seen on its own, withhold the final mark. Eg. $\int2x^4-3x^{\frac{1}{2}}+5x+c\,\mathrm{d}x$ or "
       r"$2x^4-3x^{\frac{1}{2}}+5x+c=0$ with no correct expression seen earlier are both A0."],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", ALG, "2.6", 2, LATEX["02a"],
      [r"M1 (AO 1.1b): $\mathrm{f}(-3)=2(-3)^3+5(-3)^2+2(-3)+15=-54+45-6+15$. Notes: Attempts $\mathrm{f}(-3)$. Attempted "
       r"division by $(x+3)$ or $\mathrm{f}(3)$ is M0. Look for evidence of embedded values or two correct terms of "
       r"$\mathrm{f}(-3)=-54+45-6+15=\ldots$",
       r"A1 (AO 2.4): $\mathrm{f}(-3)=0\Rightarrow(x+3)$ is a factor. Notes: Achieves and states $\mathrm{f}(-3)=0$, and makes "
       r"a suitable conclusion. Sight of $\mathrm{f}(x)=0$ when $x=-3$ is also acceptable. It must follow M1. Accept, for "
       r"example, $\mathrm{f}(-3)=0\Rightarrow(x+3)$ is a factor. This may be seen in a preamble before finding "
       r"$\mathrm{f}(-3)=0$ but in these cases there must be a minimal statement ie QED, “proved”, tick etc."],
      False, 4),
    e("02b", "2(b)", ALG, "2.6", 2, LATEX["02b"],
      [r"M1 (AO 1.1b): At least 2 of: $a=2$, $b=-1$, $c=5$. Notes: Correct method implied by values for at least 2 correct "
       r"constants. Allow embedded in their $\mathrm{f}(x)$ or within their working if they use algebraic division/other "
       r"methods which may be seen in part (a) and used in part (b). [The mark scheme shows the long division of "
       r"$2x^3+5x^2+2x+15$ by $x+3$ giving quotient $2x^2-x+5$ and remainder 0, which scores M1A1.]",
       r"A1 (AO 1.1b): All of: $a=2$, $b=-1$, $c=5$. Notes: All values correct. Allow embedded in their $\mathrm{f}(x)$ or seen "
       r"as the quotient from algebraic division. Isw incorrectly stated values of $a$ $b$ and $c$ following a correct "
       r"quadratic expression seen."],
      False, 4),
    e("02c", "2(c)", ALG, "2.3, 2.6", 2, LATEX["02c"],
      [r"M1 (AO 2.1): $b^2-4ac=(-1)^2-4(2)(5)$. Notes: Either: considers the discriminant using their $a$, $b$ and $c$ (does "
       r"not need to be evaluated) $(b^2-4ac=)\,(-1)^2-4(2)(5)$ (the $(-1)^2$ may appear as $1^2$ and condone missing "
       r"brackets for this mark for $-1^2$). Discriminant $=-39$ is sufficient for M1; attempts to complete the square so "
       r"score for $2\left(x\pm\frac{1}{4}\right)^2+\ldots$; attempts to find the roots of the quadratic using the formula. "
       r"The values embedded in the formula score this mark. $\frac{1\pm\sqrt{(-1)^2-4\times2\times5}}{2\times2}$ (the "
       r"$(-1)^2$ may appear as $1^2$ and condone missing brackets for this mark for $-1^2$); Sketches a graph of the "
       r"quadratic. It must be a U shaped quadratic which does not cross the $x$-axis.",
       r"A1 (AO 2.4): $b^2-4ac=-39$ which is $<0$ so the quadratic has no real roots so $\mathrm{f}(x)=0$ has only 1 real root. "
       r"Notes: Provides a correct explanation from correct working. They must: Have a correct calculation; Explanation "
       r"that the quadratic has no (real) roots; Minimal conclusion stating that $\mathrm{f}(x)=0$ has only one root. eg "
       r"$b^2-4ac=-39<0$ so only one root is M1A0 (needs to explain the quadratic has no real roots) eg "
       r"$2\left(x-\frac{1}{4}\right)^2+\frac{39}{8}>0$ so no real roots (for the quadratic) so ($\mathrm{f}(x)$ has) only "
       r"one (real) root is M1A1. The value of the discriminant, completed square form "
       r"$2\left(x-\frac{1}{4}\right)^2+\frac{39}{8}$ or roots of the quadratic $\left(=\frac{1\pm\sqrt{39}i}{4}\right)$ "
       r"must be correct. If they sketch the quadratic graph it must be a U shaped quadratic which crosses the $y$-axis at 5 "
       r"and has a minimum in the 1st quadrant. They must explain that the graph does not cross the $x$-axis so no real "
       r"roots for the quadratic so only one root for $\mathrm{f}(x)=0$."],
      False, 4),
    e("02d", "2(d)", ALG, "2.8, 2.6", 1, LATEX["02d"],
      [r"B1 (AO 2.2a): $(x=)\,2$. Notes: 2 condone $(2, 0)$"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", VEC, "9.3", 2, LATEX["03a"],
      [r"M1 (AO 1.1a): $\overrightarrow{QR}=\overrightarrow{PR}-\overrightarrow{PQ}=13\mathbf{i}-15\mathbf{j}-(3\mathbf{i}"
       r"+5\mathbf{j})$. Notes: Attempts subtraction either way round. This cannot be awarded for adding the two vectors. If "
       r"no method shown it may be implied by one correct component. eg $10\mathbf{i}-10\mathbf{j}$ on its own can score M1.",
       r"A1 (AO 1.1b): $=10\mathbf{i}-20\mathbf{j}$. Notes: Correct answer. Allow $10\mathbf{i}-20\mathbf{j}$ and "
       r"$\begin{pmatrix}10\\-20\end{pmatrix}$ but not $\begin{pmatrix}10\mathbf{i}\\-20\mathbf{j}\end{pmatrix}$"],
      False, 8),
    e("03b", "3(b)", VEC, "9.2, 2.2", 2,
      LATEX["03b"],
      [r"M1 (AO 2.5): $\left|\overrightarrow{QR}\right|=\sqrt{\text{“}10\text{”}^2+\text{“}(-20)\text{”}^2}$. Notes: "
       r"Correct use of Pythagoras. Attempts to “square and add” before square rooting. The embedded values are sufficient. "
       r"Follow through on their $\overrightarrow{QR}$",
       r"A1ft (AO 1.1b): $=10\sqrt{5}$. Notes: $10\sqrt{5}$ following (a) of the form $\pm10\mathbf{i}\pm20\mathbf{j}$"],
      False, 8),
    e("03c", "3(c)", VEC, "9.3, 9.4", 2,
      LATEX["03c"],
      [r"M1 (AO 3.1a): $\overrightarrow{PS}=\overrightarrow{PQ}+\frac{3}{5}\overrightarrow{QR}=3\mathbf{i}+5\mathbf{j}"
       r"+\frac{3}{5}(\text{“}10\mathbf{i}-20\mathbf{j}\text{”})=\ldots$ or $\overrightarrow{PS}=\overrightarrow{PR}"
       r"+\frac{2}{5}\overrightarrow{RQ}=13\mathbf{i}-15\mathbf{j}+\frac{2}{5}(\text{“}-10\mathbf{i}+20\mathbf{j}"
       r"\text{”})=\ldots$ Notes: Full attempt at finding a $\overrightarrow{PS}$. They must be attempting "
       r"$\overrightarrow{PQ}\pm\frac{3}{5}\overrightarrow{QR}$ or $\overrightarrow{PS}=\overrightarrow{PR}\pm\frac{2}{5}"
       r"\overrightarrow{RQ}$ but condone arithmetical slips after that. Cannot be scored for just stating eg "
       r"$\overrightarrow{PQ}\pm\frac{3}{5}\overrightarrow{QR}$. Follow through on their $\overrightarrow{QR}$. Terms do not "
       r"need to be collected for this mark. If no method shown it may be implied by one correct component following "
       r"through on their $\overrightarrow{QR}$",
       r"A1 (AO 1.1b): $=9\mathbf{i}-7\mathbf{j}$. Notes: Correct vector as shown. Allow $9\mathbf{i}-7\mathbf{j}$ and "
       r"$\begin{pmatrix}9\\-7\end{pmatrix}$. Only withhold the mark for $\begin{pmatrix}9\mathbf{i}\\-7\mathbf{j}"
       r"\end{pmatrix}$ if the mark has not already been withheld in (a) for $\begin{pmatrix}10\mathbf{i}\\-20\mathbf{j}"
       r"\end{pmatrix}$",
       r"ALT: Alt (c) (Expressing $\overrightarrow{PS}$ in terms of the given vectors; they must be attempting "
       r"$\frac{2}{5}\overrightarrow{PQ}+\frac{3}{5}\overrightarrow{PR}$) — M1: $\left(\overrightarrow{PS}="
       r"\overrightarrow{PQ}+\frac{3}{5}\overrightarrow{QR}=\overrightarrow{PQ}+\frac{3}{5}(\overrightarrow{PR}-"
       r"\overrightarrow{PQ})\right)\Rightarrow\frac{2}{5}\overrightarrow{PQ}+\frac{3}{5}\overrightarrow{PR}="
       r"\frac{2}{5}(3\mathbf{i}+5\mathbf{j})+\frac{3}{5}(13\mathbf{i}-15\mathbf{j})=\ldots$",
       r"ALT: Alt (c) — A1: Correct vector as shown. Allow $9\mathbf{i}-7\mathbf{j}$ and $\begin{pmatrix}9\\-7"
       r"\end{pmatrix}$. Only withhold the mark for $\begin{pmatrix}9\mathbf{i}\\-7\mathbf{j}\end{pmatrix}$ if the mark has "
       r"not already been withheld in (a) for $\begin{pmatrix}10\mathbf{i}\\-20\mathbf{j}\end{pmatrix}$"],
      False, 8),

    # ---------------- Q4 ----------------
    e("04ai", "4(a)(i)", TRIG, "5.1, 2.3", 3, LATEX["04ai"],
      [r"M1 (AO 3.1a): $(3x+10)^2=(x+2)^2+(7x)^2-2(x+2)(7x)\cos60^\circ$ oe. Notes: (a)(i) Mark (a) and (b) together. "
       r"Recognises the need to apply the cosine rule and attempts to use it with the sides in the correct positions and the "
       r"formula applied correctly. Condone invisible brackets and slips on $3x+10$ as $3x-10$. The angles and lengths must "
       r"be in the correct positions. Cos 60 may be $\frac{1}{2}$ from the start",
       r"dM1 (AO 1.1b): Uses $\cos60^\circ=\frac{1}{2}$, expands the brackets and proceeds to a 3 term quadratic equation. "
       r"Notes: Uses $\cos60^\circ=\frac{1}{2}$, expands the brackets and proceeds to a 3TQ. You may see the use of "
       r"$\cos60^\circ=\frac{1}{2}$ in earlier work, but they must proceed to a 3TQ as well to score this mark. It is "
       r"dependent on the first method mark.",
       r"A1* (AO 2.1): $17x^2-35x-48=0$ *. Notes: Obtains the correct quadratic equation with the $=0$ with no errors seen in "
       r"the main body of their solution. Condone the recovery of invisible brackets as long as the intention is clear. You "
       r"do not need to explicitly see cos 60 to score full marks.",
       r"ALT: Alternatively (a)(i), trigonometry (with the mark scheme's diagram of the perpendicular $BX$ from $B$ to $AC$: "
       r"$BX=\frac{\sqrt{3}}{2}(x+2)$ cm, $AX=(x+2)\cos60^\circ$ cm, $XC=\frac{13x-2}{2}$ cm) — M1 (AO 3.1a): "
       r"Alternatively, uses trigonometry to find $AX$ and then equates two expressions for the length $BX$. You may see "
       r"variations of this if they use Pythagoras or trigonometry to find $BX$ and then apply Pythagoras to the triangle "
       r"$BXC$."],
      True, 10),
    e("04aii", "4(a)(ii)", TRIG, "5.1, 2.3", 1, LATEX["04aii"],
      [r"B1 (AO 3.2a): $x=3$. Notes: Selects the appropriate value i.e. $x=3$ only. The other root must either be rejected if "
       r"found or $x=3$ must be the only root used in part (b). Can be implied by awrt 13.2 in (b)"],
      True, 10),
    e("04b", "4(b)", TRIG, "5.1", 2,
      LATEX["04b"],
      [r"M1 (AO 1.1b): $\frac{5}{\sin ACB}=\frac{19}{\sin60^\circ}\Rightarrow\sin ACB=\ldots\left(\frac{5\sqrt{3}}{38}\right)$ "
       r"or e.g. $5^2=21^2+19^2-2\times19\times21\cos ACB\Rightarrow\cos ACB=\ldots\left(\frac{37}{38}\right)$. Notes: Using "
       r"their value for $x$ this mark is for either: applying the sine rule correctly (or considers 2 right angled "
       r"triangles) and proceeding to obtain a value for $\sin ACB$ or applying the cosine rule correctly and proceeding to "
       r"obtain a value for $\cos ACB$. Condone slips calculating the lengths $AB$, $BC$ and $AC$. At least one of them "
       r"should be found correctly for their value for $x$ (Also allow if the sine rule or cosine rule is applied correctly "
       r"to find a value for $\sin ABC\left(=\frac{21\sqrt{3}}{38}\right)$ or $\cos ACB\left(=-\frac{11}{38}\right)$)",
       r"A1 (AO 1.1b): $\theta=$ awrt 13.2. Notes: awrt 13.2 (answers with little working eg just lengths on the diagram can "
       r"score M1A1)"],
      True, 10),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", EXP, "6.6, 6.4", 4, LATEX["05a"],
      [r"M1 (AO 1.1b): $p=10^{0.5}$ (or $\log_{10}p=0.5$) or $q=10^{0.03}$ (or $\log_{10}q=0.03$). Notes: A correct equation in "
       r"$p$ or $q$. May be implied by a correct value for $p$ or $q$. Also score for rearranging the equation to the form "
       r"$A=10^{0.5}\ldots10^{0.03t}$",
       r"A1 (AO 1.1b): $p=$ awrt 3.162 or $q=$ awrt 1.072. Notes: For $p=$ awrt 3.162 or $q=$ awrt 1.072. May be embedded "
       r"within the equation.",
       r"dM1 (AO 3.1a): $p=10^{0.5}$ (or $\log_{10}p=0.5$) and $q=10^{0.03}$ (or $\log_{10}q=0.03$). Notes: Correct equations "
       r"in $p$ and $q$. Also score for rearranging the equation to the form $A=10^{0.5}\times10^{0.03t}$",
       r"A1 (AO 3.3): $A=3.162\times1.072^t$. Notes: Complete equation with $p=$ awrt 3.162 and $q=$ awrt 1.072. Must be seen "
       r"in (a). If $p$ and $q$ are just stated but the equation is not written with the values embedded then withhold this "
       r"mark. Withhold the final mark if the correct values for $p$ and $q$ result from incorrect working such as "
       r"$A=10^{0.5}+10^{0.03t}\Rightarrow A=3.162\times1.072^t$. If $p$ and $q$ are stated the wrong way round, take the "
       r"stated equation as their final answer and isw."],
      False, 14),
    e("05b", "5(b)", EXP, "6.7", 2,
      LATEX["05b"],
      [r"B1 (AO 3.4): (i) The initial mass (in kg) of algae (in the pond). Notes: Must reference mass of algae and relating to "
       r"initially/at the start/beginning. Examples of acceptable answers: The mass of algae originally (in the pond); $p$ "
       r"is the mass of algae when $t=0$. Examples of answers we would not accept: $p$ is how much algae there is at the "
       r"beginning; The relationship between algae and number of weeks",
       r"B1 (AO 3.4): (ii) The ratio of algae from one week to the next. Notes: Must reference the rate of change/multiplier "
       r"and the time frame eg per week/every week/each week. Examples of acceptable answers: $q$ is the rate at which the "
       r"mass of algae increases for every week; The amount of algae increases by 7.2% each week (condone amount for mass "
       r"in ii); The proportional increase in mass of the algae each week. Examples of answers we would not accept: $q$ is "
       r"how much algae will increase when $t$ increases by 1; The amount that grows per unit of time; The rate at which "
       r"the mass of algae in the small pond increases after $t$ number of weeks; The rate in which the algae mass increases"],
      False, 14),
    e("05c", "5(c)", EXP, "6.7, 6.5", 3,
      LATEX["05c"],
      [r"B1 (AO 2.2a): (i) 5.5 kg. Notes: cao (including units)",
       r"M1 (AO 3.4): (ii) $4=\text{“}3.162\text{”}\times\text{“}1.072\text{”}^t$ or $\log_{10}4=0.03t+0.5$. Notes: Setting "
       r"up a correct equation to find $t$ using the given equation or their part (a). Substitution of $A=4$ into their "
       r"equation for $A$ or the given equation is sufficient for this mark.",
       r"A1 (AO 1.1b): awrt 3.4 (weeks). Notes: awrt 3.4 (weeks). Accept any acceptable method (including trial and "
       r"improvement) Condone lack of units. isw if they subsequently convert to weeks and days. Allow awrt 3.5 (weeks) "
       r"following $p=$ awrt 3.16 and $q=$ awrt 1.07. An answer of only awrt 3.4 is M1A1, but an answer of 4 (weeks) with no "
       r"working is M0A0"],
      False, 14),
    e("05d", "5(d)", EXP, "6.7", 1,
      LATEX["05d"],
      [r"B1 (AO 3.5b): The model predicts unlimited growth; The weather may affect the rate of growth. Notes: Any reason why "
       r"the rate of change, growth or the mass of algae might change or why the model in not realistic. Be generous with "
       r"the awarding of this mark as long as the answer has engaged with the context of the problem or the model. Examples "
       r"of acceptable answers: Seasonal changes (which would affect the growth rate); Overcrowding (as it is a small pond); "
       r"Algae may stop growing (the model predicts unlimited growth); Algae may die / be removed / eaten (so the rate of "
       r"growth may not continue at the same rate). Examples of answers we would not accept: There could be other factors "
       r"that affect the amount of algae (too vague); The mass of algae might change"],
      False, 14),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", SEQ, "4.1", 4, LATEX["06a"],
      [r"B1 (AO 1.1b): $3^8$ or 6561 as the constant term. Notes: Sight of $3^8$ or 6561 as the constant term.",
       r"M1 (AO 1.1b): $\left(3-\frac{2x}{9}\right)^8=\ldots+{}^8C_1(3)^7\left(-\frac{2x}{9}\right)+{}^8C_2(3)^6\left(-\frac{2x}"
       r"{9}\right)^2+{}^8C_3(3)^5\left(-\frac{2x}{9}\right)^3+\ldots$ Notes: An attempt at the binomial expansion. This can "
       r"be awarded for the correct structure of the 2nd, 3rd or 4th term. The correct binomial coefficient must be "
       r"associated with the correct power of 3 and the correct power of $(\pm)\frac{2x}{9}$. Condone invisible brackets eg "
       r"${}^8C_2(3)^6-\frac{2x^2}{9}$ for this mark.",
       r"A1 (AO 1.1b): $=\ldots+8\times(3)^7\left(-\frac{2x}{9}\right)+28\times(3)^6\left(-\frac{2x}{9}\right)^2+56(3)^5\left("
       r"-\frac{2x}{9}\right)^3$. Notes: For a correct simplified or unsimplified second or fourth term (with binomial "
       r"coefficients evaluated). $+8\times(3)^7\left(-\frac{2x}{9}\right)$ or $+56(3)^5\left(-\frac{2x}{9}\right)^3$",
       r"A1 (AO 1.1b): $=6561-3888x+1008x^2-\frac{448}{3}x^3+\ldots$ Notes: $6561-3888x+1008x^2-\frac{448}{3}x^3$ Ignore any "
       r"extra terms and allow the terms to be listed. Allow the exact equivalent to $-\frac{448}{3}$ eg $-149.\dot{3}$ but not "
       r"$-149.3$. Condone $x^1$ and eg $+-3888x$. Do not isw if they multiply all the terms by eg 3",
       r"ALT: Alt(a) — B1: Sight of $3^8(1+\ldots)$ or 6561 as the constant term",
       r"ALT: Alt(a) — M1: An attempt at the binomial expansion $\left(1-\frac{2}{27}x\right)^8$. This can be awarded for the "
       r"correct structure of the 2nd, 3rd or 4th term. The correct binomial coefficient must be associated with the correct "
       r"power of $(\pm)\frac{2x}{27}$. Condone invisible brackets for this mark. Score for any of: "
       r"$8\times-\frac{2}{27}x$, $\frac{8\times7}{2}\times\left(-\frac{2}{27}x\right)^2$, $\frac{8\times7\times6}{6}\times"
       r"\left(-\frac{2}{27}x\right)^3$ which may be implied by any of $-\frac{16}{27}x$, $+\frac{112}{729}x^2$, "
       r"$-\frac{448}{19683}x^3$",
       r"ALT: Alt(a) — A1: For a correct simplified or unsimplified second or fourth term including being multiplied by $3^8$",
       r"ALT: Alt(a) — A1: $6561-3888x+1008x^2-\frac{448}{3}x^3$ Ignore any extra terms and allow the terms to be listed. "
       r"Allow the exact equivalent to $-\frac{448}{3}$ eg $-149.\dot{3}$ but not $-149.3$. Condone $x^1$ and eg $+-3888x$"],
      False, 18),
    e("06b", "6(b)", SEQ, "4.1, 2.1", 2,
      LATEX["06b"],
      [r"M1 (AO 3.1a): Coefficient of $x^2$ is $\frac{1}{2}\times\text{“}1008\text{”}-\frac{1}{2}\times\text{“}-\frac{448}"
       r"{3}\text{”}$. Notes: Adopts a correct strategy for the required coefficient. This requires an attempt to calculate "
       r"$\pm\frac{1}{2}$ their coefficient of $x^2$ from part (a) $\pm\frac{1}{2}$ their coefficient of $x^3$ from part (a). "
       r"There must be an attempt to bring these terms together to a single value. ie they cannot just circle the relevant "
       r"terms in the expansion for this mark. The strategy may be implied by their answer. Condone any appearance of $x^2$ "
       r"or $x^3$ appearing in their intermediate working.",
       r"A1 (AO 1.1b): $=\frac{1736}{3}$ (or $578\frac{2}{3}$). Notes: $\frac{1736}{3}$ or $578\frac{2}{3}$. Do not accept "
       r"$578.\dot{6}$ or $\frac{1736}{3}x^2$"],
      False, 18),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", ALG, "2.6", 2, LATEX["07a"],
      [r"M1 (AO 1.1b): $9x-x^3=x(9-x^2)$. Notes: Takes out a factor of $x$ or $-x$. Scored for $\pm x(\pm9\pm x^2)$ May be "
       r"implied by the correct answer or $\pm x(\pm x\pm3)(\pm x\pm3)$. Also allow if they attempt to take out a factor of "
       r"$(\pm x\pm3)$ so score for $(\pm x\pm3)(\pm3x\pm x^2)$",
       r"A1 (AO 1.1b): $9x-x^3=x(3-x)(3+x)$ oe. Notes: Correct factorisation. $x(3-x)(3+x)$ on its own scores M1A1. Allow eg "
       r"$-x(x-3)(x+3)$, $x(x-3)(-x-3)$ or other equivalent expressions. Condone an $=0$ appearing on the end and condone eg "
       r"$x$ written as $(x+0)$."],
      False, 22),
    e("07b", "7(b)", ALG, "2.7", 2,
      LATEX["07b"],
      [r"B1 (AO 1.1b): A cubic with correct orientation (the mark scheme sketch shows a negative cubic with a minimum to the "
       r"left of the $y$-axis and a maximum to the right, crossing the $x$-axis at $-3$, $O$ and 3). Notes: Correct shape "
       r"(negative cubic) appearing anywhere on a set of axes. It must have a minimum to the left and maximum to the right. "
       r"Be tolerant of pen slips. Judge the intent of the shape. (see examples)",
       r"B1 (AO 1.1b): Passes though origin, $(3, 0)$ and $(-3, 0)$. Notes: Passes through each of the origin, $(3, 0)$ and "
       r"$(-3, 0)$ and no other points on the $x$ axis. (The graph should not turn on any of these points). The points may be "
       r"indicated as just 3 and $-3$ on the axes. Condone $x$ and $y$ to be the wrong way round eg $(0,-3)$ for $(-3, 0)$ as "
       r"long as it is on the correct axis but do not allow $(-3, 0)$ to be labelled as $(3, 0)$. [The mark scheme then shows "
       r"example candidate sketches marked B1B0, B0B1 and B1B1.]"],
      False, 22),
    e("07c", "7(c)", DIFF, "7.3, 2.5", 3,
      LATEX["07c"],
      [r"M1 (AO 3.1a): $y=9x-x^3\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}x}=9-3x^2=0\Rightarrow x=(\pm)\sqrt{3}\Rightarrow "
       r"y=\ldots$ Notes: *Be aware the value of $y$ can be solved directly using a calculator which is not acceptable* Uses "
       r"a correct strategy for the $y$ value of either the maximum or minimum. E.g. differentiates to achieve a quadratic, "
       r"solves $\frac{\mathrm{d}y}{\mathrm{d}x}=0$ and uses their $x$ to find $y$",
       r"A1 (AO 1.1b): $y=(\pm)6\sqrt{3}$. Notes: Either or both of the values $(\pm)6\sqrt{3}$. Cannot be scored for an "
       r"answer without any working seen.",
       r"A1ft (AO 2.5): $\left\{k\in\mathbb{R}:-6\sqrt{3}<k<6\sqrt{3}\right\}$ oe. Notes: Correct answer in any acceptable set "
       r"notation following through their $6\sqrt{3}$. Condone $\left\{\text{“}-6\sqrt{3}\text{”}<k<\text{“}6\sqrt{3}"
       r"\text{”}\right\}$ or $\left\{\text{“}-6\sqrt{3}\text{”}<k\right\}\cap\left\{k<\text{“}6\sqrt{3}\text{”}\right\}$ "
       r"but not $\left\{\text{“}-6\sqrt{3}\text{”}<k\right\}\cup\left\{k<\text{“}6\sqrt{3}\text{”}\right\}$. Note: If "
       r"there is a contradiction of their solution on different lines of working do not penalise intermediate working and "
       r"mark what appears to be their final answer. Must be in terms of $k$"],
      False, 22),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", EXP, "6.7, 6.1", 1, LATEX["08a"],
      [r"B1 (AO 1.1b): $(k=)\,0.8$. Notes: Completes the equation for the model by obtaining $(k=)\,0.8$ or equivalent."],
      False, 26),
    e("08b", "8(b)", EXP, "6.7, 6.3", 3,
      LATEX["08b"],
      [r"M1 (AO 3.1b): $1=0.8+1.4\mathrm{e}^{-0.5t}\Rightarrow1.4\mathrm{e}^{-0.5t}=0.2$. Notes: *Be aware this could be solved "
       r"entirely using a calculator which is not acceptable* For using the model with $P=1$ and their value for $k$ from (a) "
       r"and proceeding to $A\mathrm{e}^{\pm0.5t}=B$. Condone if $A$ or $B$ are negative for this mark.",
       r"M1 (AO 1.1b): $-0.5t=\ln\left(\frac{0.2}{1.4}\right)\Rightarrow t=\ldots$ Notes: Uses correct log work to solve an "
       r"equation of the form $A\mathrm{e}^{\pm0.5t}=B$ leading to a value for $t$. They cannot proceed directly to awrt 3.9 "
       r"without some intermediate working seen. Eg $t=2\ln7$ or $-2\ln\left(\frac{1}{7}\right)$ is acceptable. Also allow "
       r"$1.4\mathrm{e}^{-0.5t}=0.2\Rightarrow-0.5t=-1.9459\ldots\Rightarrow t=\ldots$ This cannot be scored from an "
       r"unsolvable equation (eg when their $k\geqslant1$ so that $\mathrm{e}^{\pm0.5t}\leqslant0$).",
       r"A1 (AO 1.1b): awrt 3.9 minutes. Notes: Accept awrt 3.9 minutes or $t=$ awrt 3.9 with correct working seen. eg "
       r"$1.4\mathrm{e}^{-0.5t}=0.2\Rightarrow t=3.9$ would be M1M0A0"],
      False, 26),
    e("08c", "8(c)", DIFF, "7.2, 7.1", 2,
      LATEX["08c"],
      [r"M1 (AO 3.1b): $\left(\frac{\mathrm{d}P}{\mathrm{d}t}=\right)-0.7\mathrm{e}^{-0.5t}$, $\left(\frac{\mathrm{d}P}"
       r"{\mathrm{d}t}\right)_{t=2}=-0.7\mathrm{e}^{-0.5\times2}$. Notes: *Be aware this can be solved entirely using a "
       r"calculator which is not acceptable* Links rate of change to gradient and differentiates to obtain an expression of "
       r"the form $A\mathrm{e}^{-0.5t}$ and substitutes $t=2$. Do not accept $At\mathrm{e}^{-0.5t}$ as the derivative. Beware "
       r"that substituting $t=2$ and proceeding from $\mathrm{e}^{-1}$ to $\mathrm{e}^{-2}$ is M0A0",
       r"A1 (AO 1.1b): = awrt 0.258 (kg/cm$^2$ per minute). Notes: Obtains awrt 0.258 with differentiation seen. (Units not "
       r"required) Condone awrt $-0.258$. Awrt $\pm0.258$ with no working is M0A0. Isw after a correct answer is seen. "
       r"(Ignore in (c) any spurious notation on the LHS when differentiating such as $P=\ldots$ or "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}=\ldots$)"],
      False, 26),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", EXP, "6.4", 2, LATEX["09a"],
      [r"B1 (AO 1.2): (i) $\log_3\left(\frac{x}{9}\right)=\log_3x-\log_39=p-2$. Notes: Recalls the subtraction law of logs and "
       r"so obtains $p-2$",
       r"B1 (AO 1.1b): (ii) $\log_3\left(\sqrt{x}\right)=\frac{1}{2}p$. Notes: $\frac{1}{2}p$ oe"],
      False, 28),
    e("09b", "9(b)", EXP, "6.4, 6.3", 4,
      LATEX["09b"],
      [r"M1 (AO 1.1b): $2\log_3\left(\frac{x}{9}\right)+3\log_3\left(\sqrt{x}\right)=-11\Rightarrow2p-4+\frac{3}{2}p=-11"
       r"\Rightarrow p=\ldots$ Notes: *Be aware this should be solved by non-calculator methods* Uses their results from part "
       r"(a) to form a linear equation in $p$ and attempts to solve leading to a value for $p$. Allow slips in their "
       r"rearrangement when solving. Allow a misread forming the equation equal to 11 instead of $-11$",
       r"A1 (AO 1.1b): $p=-2$. Notes: Correct value for $p$",
       r"M1 (AO 1.1b): $\log_3x=-2\Rightarrow x=3^{-2}$. Notes: Uses $\log_3x=p\Rightarrow x=3^p$ following through on what "
       r"they consider to be their $p$. It must be a value rather than $p$",
       r"A1 (AO 1.1b): $x=\frac{1}{9}$. Notes: $(x=)\,\frac{1}{9}$ cao with correct working seen. Must be this fraction. Do "
       r"not penalise invisible brackets as long as the intention is clear.",
       r"ALT: Alternative for (b) not using (a) — M1 (AO 1.1b): $2\log_3\left(\frac{x}{9}\right)+3\log_3\left(\sqrt{x}\right)"
       r"=-11\Rightarrow\log_3\left(\frac{x}{9}\right)^2+\log_3\left(\sqrt{x}\right)^3=-11\Rightarrow\log_3\frac{x^{\frac{7}"
       r"{2}}}{81}=-11$. Notes: Correct use of log rules to achieve an equation of the form $\log_3\ldots=\log_3\ldots$ or "
       r"$\log_3\ldots=$ a number (typically $-11$). Condone arithmetical slips.",
       r"ALT: Alternative for (b) not using (a) — A1 (AO 1.1b): $\Rightarrow\frac{x^{\frac{7}{2}}}{81}=3^{-11}$ or equivalent "
       r"eg $x^{\frac{7}{2}}=3^{-7}$. Notes: Correct equation with logs removed.",
       r"ALT: Alternative for (b) not using (a) — M1 (AO 1.1b): $x^{\frac{7}{2}}=81\times3^{-11}\Rightarrow x^{\frac{7}{2}}="
       r"3^4\times3^{-11}=3^{-7}\Rightarrow x=\left(3^{-7}\right)^{\frac{2}{7}}=3^{-2}$. Notes: Uses inverse operations to "
       r"find $x$. Condone slips but look for proceeding from $x^{\frac{a}{b}}=\ldots\Rightarrow x=\ldots^{\frac{b}{a}}$ where "
       r"they have to deal with a fractional power.",
       r"ALT: Alternative for (b) not using (a) — A1 (AO 1.1b): $x=\frac{1}{9}$. Notes: $(x=)\,\frac{1}{9}$ cao with correct "
       r"working seen. Must be this fraction. Do not penalise invisible brackets as long as the intention is clear."],
      False, 28),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", DIFF, "7.3, 7.2, 3.1", 5, LATEX["10a"],
      [r"M1 (AO 1.1b): $y=\frac{1}{3}x^2-2\sqrt{x}+3\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{2}{3}x-x^{-\frac{1}{2}}$. "
       r"Notes: (a) Calculators: If no algebraic differentiation seen then maximum in a) is M0A0B1M1A0*. $x^n\to x^{n-1}$ "
       r"seen at least once $\ldots x^2\to\ldots x^1$, $\ldots x^{\frac{1}{2}}\to\ldots x^{-\frac{1}{2}}$, $3\to0$. Also "
       r"accept on sight of eg $\ldots x^{\frac{1}{2}}\to\ldots x^{\frac{1}{2}-1}$",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{2}{3}x-x^{-\frac{1}{2}}$. Notes: $\frac{2}{3}x-x^{-\frac{1}{2}}$ "
       r"or any unsimplified equivalent (indices must be processed) accept the use of $0.\dot{6}x$ but not rounded or "
       r"ambiguous values eg $0.6x$ or eg $0.66\ldots x$",
       r"B1 (AO 1.1b): $x=4\Rightarrow y=\frac{13}{3}$. Notes: Correct $y$ coordinate of $P$. May be seen embedded in an "
       r"attempt of the equation of $l$",
       r"M1 (AO 2.1): $\left(\frac{\mathrm{d}y}{\mathrm{d}x}\right)_{x=4}=\frac{2}{3}\times4-4^{-\frac{1}{2}}\left(=\frac{13}"
       r"{6}\right)$ $\therefore y-\frac{13}{3}=\frac{13}{6}(x-4)$. Notes: Fully correct strategy for an equation for $l$. "
       r"Look for $y-\text{“}\frac{13}{3}\text{”}=\text{“}\frac{13}{6}\text{”}(x-4)$ where their $\frac{13}{6}$ is from "
       r"differentiating the equation of the curve and substituting in $x=4$ into their $\frac{\mathrm{d}y}{\mathrm{d}x}$ "
       r"and the $y$ coordinate is from substituting $x=4$ into the given equation. If they use $y=mx+c$ they must proceed "
       r"as far as $c=\ldots$ to score this mark. Do not allow this mark if they use a perpendicular gradient.",
       r"A1* (AO 1.1b): $13x-6y-26=0$ *. Notes: Obtains the printed answer with no errors."],
      True, 30),
    e("10b", "10(b)", INT, "8.3, 8.2", 5,
      LATEX["10b"],
      [r"M1 (AO 1.1b): $\int\left(\frac{x^2}{3}-2\sqrt{x}+3\right)\mathrm{d}x=\frac{x^3}{9}-\frac{4}{3}x^{\frac{3}{2}}+3x(+c)$. "
       r"Notes: (b) Calculators: If no algebraic integration seen then maximum in b) is M0A0B1M1A0. $x^n\to x^{n+1}$ seen at "
       r"least once. Eg $\ldots x^2\to\ldots x^3$, $\ldots x^{\frac{1}{2}}\to\ldots x^{\frac{3}{2}}$, $3\to3x^1$. Allow eg "
       r"$\ldots x^2\to\ldots x^{2+1}$. The $+c$ is not a valid term for this mark.",
       r"A1 (AO 1.1b): $\frac{x^3}{9}-\frac{4}{3}x^{\frac{3}{2}}+3x$. Notes: $\frac{x^3}{9}-\frac{4}{3}x^{\frac{3}{2}}+3x$ or "
       r"any unsimplified equivalent (indices must be processed) accept the use of exact decimals for $\frac{1}{9}$ "
       r"$(0.\dot{1})$ and $-\frac{4}{3}$ $(-1.\dot{3})$ but not rounded or ambiguous values.",
       r"B1 (AO 2.2a): $y=0\Rightarrow x=2$. Notes: Deduces the correct value for $x$ for the intersection of $l$ with the "
       r"$x$-axis. May be seen indicated on Figure 2.",
       r"M1 (AO 3.1a): Area of $R$ is $\left[\frac{x^3}{9}-\frac{4}{3}x^{\frac{3}{2}}+3x\right]_0^4-\frac{1}{2}\times(4-"
       r"\text{“}2\text{”})\times\text{“}\frac{13}{3}\text{”}=\frac{76}{9}-\frac{13}{3}$. Notes: Fully correct strategy "
       r"for the area. This needs to include: a correct attempt at the area of the triangle using their values (could use "
       r"integration); a correct attempt at the area under the curve using 0 and 4 in their integrated expression; the two "
       r"values subtracted. Be aware of those who mix up using the $y$-coordinate of $P$ and the gradient at $P$ which is "
       r"M0. The values embedded in an expression is sufficient to score this mark.",
       r"A1 (AO 1.1b): $=\frac{37}{9}$. Notes: $\frac{37}{9}$ or exact equivalent eg $4\frac{1}{9}$ or $4.\dot{1}$ but not "
       r"$4.111\ldots$ isw after a correct answer",
       r"ALT: Other strategy (area under the curve between 0 and 2, then the difference between the curve and the straight "
       r"line between 2 and 4: $\int_0^2\frac{x^2}{3}-2\sqrt{x}+3\,\mathrm{d}x+\int_2^4\frac{x^2}{3}-2\sqrt{x}-\frac{13}{6}x"
       r"+\frac{22}{3}\,\mathrm{d}x$) — M1: $x^n\to x^{n+1}$ seen at least once on either integral (or on the equation of "
       r"the line $y=\frac{1}{3}x+3$)",
       r"ALT: Other strategy — A1: for correct integration of either integral $\frac{x^3}{9}-\frac{4}{3}x^{\frac{3}{2}}+3x$ "
       r"or $\frac{x^3}{9}-\frac{4}{3}x^{\frac{3}{2}}-\frac{13}{12}x^2+\frac{22}{3}x$ (may be unsimplified/uncollected terms "
       r"but the indices must be processed with/without the $+C$)",
       r"ALT: Other strategy — B1: Correct value for $x$ can be seen from the top of the first integral (or bottom value of "
       r"the second integral)",
       r"ALT: Other strategy — M1: Correct strategy for the area eg. $\left[\frac{x^3}{9}-\frac{4}{3}x^{\frac{3}{2}}+3x"
       r"\right]_0^2+\left[\frac{x^3}{9}-\frac{4}{3}x^{\frac{3}{2}}-\frac{13}{12}x^2+\frac{22}{3}x\right]_2^4=\frac{62}{9}-"
       r"\frac{4}{3}(2)^{\frac{3}{2}}+\frac{76}{9}-\frac{101}{9}+\frac{4}{3}(2)^{\frac{3}{2}}$",
       r"ALT: Other strategy — A1: $\frac{37}{9}$ or exact equivalent eg $4\frac{1}{9}$ or $4.\dot{1}$ but not 4.1 or "
       r"$4.111\ldots$ (The mark scheme adds: You could also see use of the area of a trapezium and/or the use of the line "
       r"$y=\frac{1}{3}x+3$ to find other areas which could be combined or used as part of the strategy to find $R$. Ignore "
       r"areas which are not used. The marks should still be able to be applied as per the scheme. Eg Area of trapezium "
       r"$-$ (Area between $y=\frac{1}{3}x+3$ and curve $C$ + area of triangle) $=\frac{44}{3}-\frac{56}{9}-\frac{13}{3}="
       r"\frac{37}{9}$, with the area of the large trapezium $=\frac{1}{2}\times\left(3+\frac{13}{3}\right)\times4="
       r"\frac{44}{3}$.)"],
      True, 30),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", COORD, "3.2", 3, LATEX["11a"],
      [r"M1 (AO 1.1b): $(x\pm5)^2+(y\pm4)^2$. Notes: Attempts to complete the square for both $x$ and $y$ terms "
       r"$(x\pm5)^2\ldots(y\pm4)^2$ which may be implied by a centre of $(\pm5,\pm4)$",
       r"A1 (AO 1.1b): (i) Centre is $(5, 4)$. Notes: Centre $(5, 4)$",
       r"A1 (AO 1.1b): (ii) Radius is 3. Notes: Radius 3"],
      True, 34),
    e("11b", "11(b)", COORD, "3.2, 3.1, 2.4", 5, LATEX["11b"],
      [r"B1 (AO 2.2a): $2y+x+6=0\Rightarrow y=-\frac{1}{2}x+\ldots\Rightarrow-\frac{1}{2}\to2$. Notes: Deduces the gradient of "
       r"the perpendicular to $l$ is 2. May be seen in the equation for the perpendicular line to $l$",
       r"M1 (AO 3.1a): $m_N=2\Rightarrow y-4=2(x-5)$; $y-4=2(x-5)$, $2y+x+6=0\Rightarrow x=\ldots, y=\ldots$ Notes: A fully "
       r"correct strategy for finding the intersection. This requires use of their gradient of the perpendicular which "
       r"cannot be the gradient of $l$. Look for $y-\text{“}4\text{”}=\text{“}2\text{”}(x-\text{“}5\text{”})$ where "
       r"$(5,4)$ is their centre being solved simultaneously with the equation of $l$. Do not be concerned with the mechanics "
       r"of their rearrangement when solving simultaneously. Many are finding the $y$-intercept of $l$ $(0,-3)$ which is M0",
       r"A1 (AO 1.1b): Intersection is at $\left(\frac{6}{5},-\frac{18}{5}\right)$ oe. Notes: "
       r"$\left(\frac{6}{5},-\frac{18}{5}\right)$ or equivalent eg $(1.2, -3.6)$. They do not have to be written as "
       r"coordinates and may be seen within their working rather than explicitly stated. They may also be written on the "
       r"diagram.",
       r"dM1 (AO 3.1a): Distance from centre to intersection is $\sqrt{\left(5-\frac{6}{5}\right)^2+\left(4+\frac{18}{5}"
       r"\right)^2}$ So distance required is $\sqrt{\left(\text{“}5\text{”}-\text{“}\frac{6}{5}\text{”}\right)^2+\left("
       r"\text{“}4\text{”}+\text{“}\frac{18}{5}\text{”}\right)^2}-\text{“}3\text{”}$. Notes: Fully correct strategy for "
       r"finding the required distance e.g. correct use of Pythagoras to find the distance between their centre and their "
       r"intersection and then completes the problem by subtracting their radius. Condone a sign slip subtracting their "
       r"$-\frac{18}{5}$. It is dependent on the previous method mark.",
       r"A1 (AO 1.1b): $=\frac{19\sqrt{5}}{5}-3$ (or awrt 5.50). Notes: Correct value e.g. $\sqrt{\frac{361}{5}}-3$ or "
       r"$\frac{19\sqrt{5}-15}{5}$. Also allow awrt 5.50. Isw after a correct answer is seen.",
       r"ALT: Alternatively (b), dM1 via the circle — dM1 (AO 3.1a): Alternatively, they solve simultaneously their "
       r"$y=2x-6$ with the equation of the circle and then find the distance between this intersection point and the point "
       r"of intersection between $l$ and the normal. They must choose the smaller positive root of the solution to their "
       r"quadratic. Eg $(x-5)^2+(2x-6-4)^2=9\Rightarrow5x^2-50x+125=9$; $x=\frac{25-3\sqrt{5}}{5}$, "
       r"$y=\frac{20-6\sqrt{5}}{5}$; Distance between two points: $\sqrt{\left(\text{“}\frac{25-3\sqrt{5}}{5}\text{”}-"
       r"\text{“}\frac{6}{5}\text{”}\right)^2+\left(\text{“}\frac{20-6\sqrt{5}}{5}\text{”}+\text{“}\frac{18}{5}\text{”}"
       r"\right)^2}$",
       r"ALT: Alt (b), vector methods — B1M1: Attempts to find the perpendicular distance between their $(5,4)$ and "
       r"$x+2y+6=0$ by substituting the values into the formula to find the distance between a point $(x, y)$ and a line "
       r"$ax+by+c=0$ $\Rightarrow\frac{|ax+by+c|}{\sqrt{a^2+b^2}}=\frac{|\text{“}5\text{”}\times\text{“}1\text{”}+"
       r"\text{“}4\text{”}\times\text{“}2\text{”}+\text{“}6\text{”}|}{\sqrt{\text{“}1\text{”}^2+\text{“}2\text{”}^2}}$",
       r"ALT: Alt (b), vector methods — A1: $\frac{|5\times1+4\times2+6|}{\sqrt{1^2+2^2}}\left(=\frac{19}{\sqrt{5}}\right)$",
       r"ALT: Alt (b), vector methods — dM1: Distance $=\text{“}\frac{19\sqrt{5}}{5}\text{”}-3$",
       r"ALT: Alt (b), vector methods — A1: $\frac{19\sqrt{5}-15}{5}$"],
      True, 34),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", ALG, "2.6, 2.1", 4, LATEX["12a"],
      [r"B1 (AO 1.1b): $V=\pi r^2h=355\Rightarrow h=\frac{355}{\pi r^2}$ $\left(\text{or }rh=\frac{355}{\pi r}\text{ or }\pi rh"
       r"=\frac{355}{r}\right)$. Notes: Correct expression for $h$ or $rh$ or $\pi rh$ in terms of $r$. This may be implied by "
       r"their later substitution.",
       r"M1 (AO 3.4): $C=0.04(\pi r^2+2\pi rh)+0.09(\pi r^2)$. Notes: Scored for the sum of the three terms of the form "
       r"$0.04\ldots r^2$, $0.09\ldots r^2$ and $0.04\times\ldots rh$. The $0.04\times\ldots rh$ may be implied by eg "
       r"$0.04\times\ldots r\times\frac{355}{\pi r^2}$ if $h$ has already been replaced",
       r"dM1 (AO 2.1): $C=0.13\pi r^2+0.08\pi rh=0.13\pi r^2+0.08\pi r\left(\frac{355}{\pi r^2}\right)$. Notes: Substitutes "
       r"$h$ or $rh$ or $\pi rh$ into their equation for $C$ which must be of an allowable form (see above) to obtain an "
       r"equation connecting $C$ and $r$. It is dependent on a correct expression for $h$ or $rh$ or $\pi rh$ in terms of $r$",
       r"A1* (AO 1.1b): $C=0.13\pi r^2+\frac{28.4}{r}$ *. Notes: Achieves given answer with no errors. Allow Cost instead of "
       r"$C$ but they cannot just have an expression. As a minimum you must see: the separate equation for volume; the two "
       r"costs for the top and bottom separate before combining; a substitution before seeing the $\frac{28.4}{r}$ term. Eg "
       r"$355=\pi r^2h$ and $C=0.04\pi r^2+0.09\pi r^2+0.04\times2\pi rh=0.13\pi r^2+0.08\pi\times\left(\frac{355}{\pi r}"
       r"\right)$"],
      False, 38),
    e("12b", "12(b)", DIFF, "7.3, 7.2", 4, LATEX["12b"],
      [r"M1 (AO 3.4): $\frac{\mathrm{d}C}{\mathrm{d}r}=0.26\pi r-\frac{28.4}{r^2}$. Notes: Differentiates to obtain at least "
       r"$r^{-1}\to r^{-2}$",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}C}{\mathrm{d}r}=0.26\pi r-\frac{28.4}{r^2}$. Notes: Correct derivative.",
       r"M1 (AO 1.1b): $\frac{\mathrm{d}C}{\mathrm{d}r}=0\Rightarrow r^3=\frac{28.4}{0.26\pi}\Rightarrow r=\ldots$ Notes: Sets "
       r"$\frac{\mathrm{d}C}{\mathrm{d}r}=0$ and solves for $r$. There must have been some attempt at differentiation of the "
       r"equation for $C$ ($\ldots r^2\to\ldots r$ or $\ldots r^{-1}\to\ldots r^{-2}$) Do not be concerned with the "
       r"mechanics of their rearrangement and do not withhold this mark if their solution for $r$ is negative",
       r"A1 (AO 1.1b): $r=\sqrt[3]{\frac{1420}{13\pi}}=3.26\ldots$ Notes: Correct value for $r$. Allow exact value or awrt "
       r"3.26"],
      False, 38),
    e("12c", "12(c)", DIFF, "7.3", 2,
      LATEX["12c"],
      [r"M1 (AO 1.1b): $\left(\frac{\mathrm{d}^2C}{\mathrm{d}r^2}=\right)0.26\pi+\frac{56.8}{r^3}=0.26\pi+\frac{56.8}"
       r"{\text{“}3.26\text{”}^3}$. Notes: Finds $\frac{\mathrm{d}^2C}{\mathrm{d}r^2}$ at their (positive) $r$ or considers "
       r"the sign of $\frac{\mathrm{d}^2C}{\mathrm{d}r^2}$. This mark can be scored as long as their second derivative is of "
       r"the form $A+\frac{B}{r^3}$ where $A$ and $B$ are non zero",
       r"A1 (AO 2.4): $\left(\frac{\mathrm{d}^2C}{\mathrm{d}r^2}=\right)(2.45..)>0$ Hence minimum (cost). Notes: Requires: A "
       r"correct $\frac{\mathrm{d}^2C}{\mathrm{d}r^2}$; Either: deduces $\frac{\mathrm{d}^2C}{\mathrm{d}r^2}>0$ for $r>0$ "
       r"(without evaluating). There must be some minimal explanation as to why it is positive; substitute their positive "
       r"$r$ into $\frac{\mathrm{d}^2C}{\mathrm{d}r^2}$ without evaluating and deduces $\frac{\mathrm{d}^2C}{\mathrm{d}r^2}>0$ "
       r"for $r>0$; evaluate $\frac{\mathrm{d}^2C}{\mathrm{d}r^2}$ (which must be awrt 2.5) and deduces "
       r"$\frac{\mathrm{d}^2C}{\mathrm{d}r^2}>0$ for $r>0$"],
      False, 38),
    e("12d", "12(d)", DIFF, "7.3", 2,
      LATEX["12d"],
      [r"M1 (AO 3.4): $C=0.13\pi(\text{“}3.26\text{”})^2+\frac{28.4}{\text{“}3.26\text{”}}$. Notes: Uses the model and "
       r"their positive $r$ found in (b) to find the minimum cost. Their $r$ embedded in the expression is sufficient. May be "
       r"seen in (b) but must be used in (d).",
       r"A1 (AO 1.1b): $(C=)\,13$. Notes: $(C=)\,13$ ignore units"],
      False, 38),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", TRIG, "5.3", 3, LATEX["13a"],
      [r"M1 (AO 1.1b): $\frac{1}{\cos\theta}+\tan\theta=\frac{1+\sin\theta}{\cos\theta}$ or $\frac{(1+\sin\theta)\cos\theta}"
       r"{\cos^2\theta}$. Notes: (a) If starting with the LHS: Condone if another variable for $\theta$ is used except for the "
       r"final mark. Combines terms with a common denominator. The numerator must be correct for their common denominator.",
       r"dM1 (AO 2.1): $=\frac{1+\sin\theta}{\cos\theta}\times\frac{1-\sin\theta}{1-\sin\theta}=\frac{1-\sin^2\theta}{\cos\theta"
       r"(1-\sin\theta)}=\frac{\cos^2\theta}{\cos\theta(1-\sin\theta)}$ or $\frac{(1+\sin\theta)\cos\theta}{\cos^2\theta}="
       r"\frac{(1+\sin\theta)\cos\theta}{1-\sin^2\theta}=\frac{(1+\sin\theta)\cos\theta}{(1+\sin\theta)(1-\sin\theta)}$. "
       r"Notes: Either: $\frac{1+\sin\theta}{\cos\theta}$: Multiplies numerator and denominator by $1-\sin\theta$, uses the "
       r"difference of two squares and applies $\cos^2\theta=1-\sin^2\theta$; $\frac{(1+\sin\theta)\cos\theta}"
       r"{\cos^2\theta}$: Uses $\cos^2\theta=1-\sin^2\theta$ on the denominator, applies the difference of two squares. It is "
       r"dependent on the previous method mark.",
       r"A1* (AO 1.1b): $=\frac{\cos\theta}{1-\sin\theta}$ *. Notes: Fully correct proof with correct notation and no errors "
       r"in the main body of their work. Withhold this mark for writing eg sin instead of $\sin\theta$ anywhere in the "
       r"solution and for eg $\sin\theta^2$ instead of $\sin^2\theta$",
       r"ALT: Alt(a) If starting with the RHS (condone if another variable is used for $\theta$ except for the final mark) — "
       r"M1: Multiplies by $\frac{1+\sin\theta}{1+\sin\theta}$ leading to $\frac{\cos\theta(1+\sin\theta)}{1-\sin^2\theta}$ "
       r"or Multiplies by $\frac{\cos\theta}{\cos\theta}$ leading to $\frac{\cos^2\theta}{\cos\theta(1-\sin\theta)}$",
       r"ALT: Alt(a) If starting with the RHS — dM1: Applies $\cos^2\theta=1-\sin^2\theta$ and cancels the $\cos\theta$ factor "
       r"from the numerator and denominator leading to $\frac{1+\sin\theta}{\cos\theta}$ or Applies $\cos^2\theta=1-"
       r"\sin^2\theta$ and uses the difference of two squares leading to $\frac{(1+\sin\theta)(1-\sin\theta)}{\cos\theta"
       r"(1-\sin\theta)}$. It is dependent on the previous method mark.",
       r"ALT: Alt(a) If starting with the RHS — A1*: Fully correct proof with correct notation and no errors in the main body "
       r"of their work. If they work from both the LHS and the RHS and meet in the middle with both sides the same then they "
       r"need to conclude at the end by stating the original equation."],
      False, 42),
    e("13b", "13(b)", TRIG, "5.4, 5.3", 5,
      LATEX["13b"],
      [r"M1 (AO 2.1): $\frac{1}{\cos2x}+\tan2x=3\cos2x\Rightarrow1+\sin2x=3\cos^22x=3(1-\sin^22x)$. Notes: (b) *Be aware that "
       r"this can be done entirely on their calculator which is not acceptable* Either multiplies through by $\cos2x$ and "
       r"applies $\cos^22x=1-\sin^22x$ to obtain an equation in $\sin2x$ only or alternatively sets "
       r"$\frac{\cos2x}{1-\sin2x}=3\cos2x$ and multiplies by $1-\sin2x$",
       r"A1 (AO 1.1b): $\Rightarrow3\sin^22x+\sin2x-2=0$. Notes: Correct equation or equivalent. The $=0$ may be implied by "
       r"their later work (Condone notational slips in their working)",
       r"M1 (AO 1.1b): $\sin2x=\frac{2}{3}, (-1)\Rightarrow2x=\ldots\Rightarrow x=\ldots$ Notes: Solves for $\sin2x$, uses "
       r"arcsin to obtain at least one value for $2x$ and divides by 2 to obtain at least one value for $x$. The roots of the "
       r"quadratic can be found using a calculator. They cannot just write down values for $x$ from their quadratic in "
       r"$\sin2x$",
       r"A1 (AO 1.1b): $x=20.9^\circ, 69.1^\circ$. Notes: For 1 of the required angles. Accept awrt 21 or awrt 69. Also accept "
       r"awrt 0.36 rad or awrt 1.21 rad",
       r"A1 (AO 1.1b): $x=20.9^\circ, 69.1^\circ$. Notes: For both angles (awrt 20.9 and awrt 69.1) and no others inside the "
       r"range. If they find $x=45$ it must be rejected. (Condone notational slips in their working)",
       r"ALT: Second scheme column (using (a)) — M1 (AO 2.1): $\frac{\cos2x}{1-\sin2x}=3\cos2x\Rightarrow\cos2x="
       r"3\cos2x(1-\sin2x)$",
       r"ALT: Second scheme column (using (a)) — A1 (AO 1.1b): $\Rightarrow\cos2x(2-3\sin2x)=0$"],
      False, 42),

    # ---------------- Q14 ----------------
    e("14i", "14(i)", PROOF, "1.1", 1,
      LATEX["14i"],
      [r"B1 (AO 2.3): The statement is not true because e.g. when $x=-4$, $x^2=16$ (which is $>9$ but $x<3$). Notes: "
       r"Identifies the error in the statement by giving: a counter example and a reason eg $x=-4$ with $x^2=16$ eg $x=-4$ "
       r"with $(-4)^2>9$; concludes not true. There should be no errors seen including the use of brackets. The conclusion "
       r"could be a preamble. Do not accept “sometimes true” or equivalent. Alternatively, explains why the statement is not "
       r"true Eg. It is not true as when $x<-3$ then $x^2>9$ so $x$ does not have to be greater than 3. Eg. $x^2>9\Rightarrow "
       r"x<-3$ or $x>3$ so not true"],
      False, 46),
    e("14ii", "14(ii)", PROOF, "1.1, 2.6", 3, LATEX["14ii"],
      [r"M1 (AO 2.1): $n^3+3n^2+2n=n(n^2+3n+2)=n(n+1)(n+2)$. Notes: Takes out a factor of $n$ and attempts to factorise the "
       r"resulting quadratic.",
       r"A1 (AO 2.2a): $n(n+1)(n+2)$ is the product of 3 consecutive integers. Notes: Deduces that the expression is the "
       r"product of 3 consecutive integers",
       r"A1 (AO 2.4): As $n(n+1)(n+2)$ is a multiple of 2 and a multiple of 3 it must be a multiple of 6 and so "
       r"$n^3+3n^2+2n$ is divisible by 6 for all integers $n$. Notes: Explains that as the expression is a multiple of 3 and "
       r"2, it must be a multiple of 6 and so is divisible by 6. If you see any method which appears to be credit worthy but "
       r"is not covered by the scheme then send to review"],
      False, 46),
]

# Examiner report, sentence by sentence, in report order.
# A sentence that mentions another part only in passing is tagged with the
# part it is about. Report errors keep their wording and get a [sic: ...] note.
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, r"The vast majority scored M1 for either $2x^4$ or $5x$."),
        (W, r"The most common error was dealing with coefficient of $x^{\frac{1}{2}}$ with a substantial number of "
            r"candidates who were unable to process the fractional power."),
        (W, r"Many candidates rewrote the term as $\frac{3}{2}x^{\frac{1}{2}}$ while others made mistakes with the "
            r"coefficient and rewrote it as $6x^{\frac{1}{2}}$ or $6x^{-\frac{1}{2}}$.", NO),
        (W, "A few attempted to integrate both the top and bottom of the fraction."),
        (W, r"Of those who had rewritten the term correctly as $\frac{3}{2}x^{-\frac{1}{2}}$ some made mistakes when "
            r"simplifying the coefficient of the integrated term.", NO),
        (W, r"$\frac{3}{4}x^{\frac{1}{2}}$ was seen several times."),
        (W, "Sometimes the correct unsimplified expression was seen first but several candidates just wrote down their "
            "answer without showing their workings."),
        (W, r"Quite a few omitted $+c$ following 3 correct terms and lost the final A1."),
        (W, r"Some candidates still lack confidence with notation such as an integral sign or $\mathrm{d}x$ appearing on "
            r"the final line which resulted in the final mark being lost.", NO),
    ],
    "02": [
        (W, "This question proved to be a successful question for many candidates with many being able to score most of "
            "the marks.", NO),
        ({"a"}, r"In part (a) the most common error here was to omit $\mathrm{f}(-3)=0$ in their response losing the A "
                r"mark."),
        ({"a"}, "A minority of candidates failed to use the Factor Theorem required and proceeded to do algebraic long "
                "division which did not score any marks."),
        ({"a"}, r"A number of candidates used incorrect language such as stating that $(x+3)$ was a root of "
                r"$\mathrm{f}(x)$.", NO),
        ({"b"}, "In part (b) the vast majority scored full marks here using division very successfully."),
        ({"b"}, "If candidates had done algebraic division in part (a), then as long as they used this result in part (b) "
                "then they were able to score still for this earlier work.", NO),
        ({"c"}, "In part (c), the majority of candidates understood the idea of using the discriminant to prove the "
                "quadratic part had no solutions."),
        ({"c"}, r"Most were able to correctly evaluate the discriminant correctly although some achieved a value of $-41$ "
                r"instead."),
        ({"c"}, r"With many responses, they often lacked a convincing conclusion clearly stating that as the quadratic had "
                r"no solutions then $\mathrm{f}(x)=0$ has only one solution."),
        ({"c"}, "Many just stated that the quadratic had no real roots or just showed the discriminant was negative and so "
                "only one root."),
        ({"c"}, r"Some incorrectly stated $(x+3)$ as the real root."),
        ({"c"}, "A few candidates chose to use the quadratic formula and show two imaginary roots and one real root."),
        ({"c"}, "These candidates were often successful, but some just embedded the values into the quadratic formula and "
                "stated “math error” for example which was not sufficient explanation.", BACK),
        ({"d"}, "Part (d) was poorly answered if it was attempted at all.", NO),
        ({"d"}, r"The most common wrong answers seen were 8, 5, $-2$ and 400 whilst the correct answer was rarely seen "
                r"showing poor understanding of the question."),
    ],
    "03": [
        (W, "Many candidates tackled this question well, scoring full marks."),
        (W, "Only a few made either no attempt or scored 0 for their efforts."),
        ({"a", "c"}, "The use of diagrams was widespread and seemed to aid those candidates in parts (a) and (c) to "
                     "clarify their work.", NO),
        ({"a"}, "In part (a), errors were either adding the given vectors, subtracting the incorrect way round, or "
                "arithmetic errors involving negative numbers."),
        ({"a"}, r"Many candidates chose to use $-\overrightarrow{PQ}+\overrightarrow{PR}$ rather than "
                r"$\overrightarrow{PR}-\overrightarrow{PQ}$ and seemed to have more success with the $\mathbf{j}$ "
                r"component."),
        ({"b"}, "In part (b), the concept and calculation of the magnitude of a vector was clearly understood by the vast "
                "majority and this was evaluated with very few errors seen; the A mark was usually only being lost by "
                "candidates with a component error in (a).", NO),
        ({"b"}, "A minority of candidates attempted to construct a scale drawing: most of these were unsuccessful at "
                "providing sufficient evidence to score the method mark.", NO),
        ({"c"}, "Part (c) did provide problems for a number of candidates, although a pleasing number provided full "
                "solutions which were often concise."),
        ({"c"}, r"Some continued down the line of attempting to calculate magnitudes using the answer to (b) and "
                r"magnitudes of the given vectors, whilst others failed to find the appropriate proportion of "
                r"$\overrightarrow{QR}$ (usually using $\frac{2}{3}$ or $\frac{1}{3}$)."),
        ({"c"}, r"The other main error seen was candidates failing to take proper account of the direction of "
                r"$\overrightarrow{RS}$."),
        ({"c"}, r"Others just found the appropriate proportion of $\overrightarrow{QR}$ but did not provide a full method "
                r"and scored no marks as a result."),
    ],
    "04": [
        ({"ai"}, "Many candidates did not attempt part (a)(i) or tackled it poorly.", NO),
        ({"aii", "b"}, "However, the majority of these candidates were still able to go on and score some marks in part "
                       "(a)(ii) and part (b) and this resulted in a significant proportion of candidates achieving all 3 "
                       "of the final marks.", BACK),
        ({"ai"}, "In (a)(i), the correct statement of the cosine rule usually produced a full solution, even though several "
                 "responses clearly showed amendments to once flawed working to be able to reach the given equation."),
        ({"ai"}, "Here, some candidates attempted to fudge their working to correct their work but were unsuccessful in "
                 "correcting each line fully."),
        ({"ai"}, r"The common errors seen were the failure to change signs when removing brackets after a minus sign and "
                 r"candidates multiplying the entire RHS of the equation by $\frac{1}{2}$ when applying $\cos60$ rather "
                 r"than just the $-2x(x-7)$."),
        ({"ai"}, r"The absence of “$=0$” was rare but still occurred."),
        ({"aii"}, r"In (a)(ii), the $x=-\frac{16}{17}$ was not always rejected, although almost all of these candidates used "
                  r"$x=3$ in part (b) and were able to gain credit.", NO),
        ({"aii"}, "Very few candidates used both values in part (b)."),
        ({"b"}, "Errors in part (b) were few and far between."),
        ({"b"}, "The main problems that occurred included incorrect manipulation of the sine rule (usually scoring M1A0) "
                "and the use of the incorrect sides in the sine rule (scoring M0A0)."),
        ({"b"}, "There were some very long-winded routes seen, with the area formula attempted twice and the cosine rule "
                "used, both with limited success."),
    ],
    "05": [
        (W, "Generally, candidates found this question accessible with many scoring consistently throughout.", NO),
        ({"a"}, r"In part (a), most candidates were able to make progress often correctly establishing the values of $p$ "
                r"and $q$ following a valid method."),
        ({"a"}, r"A significant proportion of candidates, who correctly calculated the values of both $p$ and $q$, failed "
                r"to write down “a complete equation for the model” in the required form, and a small minority candidates "
                r"failed to evaluate $p$ and $q$ to four decimal places.",
         {"note": "the question asks for 4 significant figures"}),
        ({"a"}, "The need to carefully read the question’s requirements should be emphasised to candidates and whilst in a "
                "number of questions we will allow anything which rounds to that level of accuracy, the modelling "
                "questions in particular can sometimes require a specific level of rounding to score full marks.", NO),
        ({"b"}, r"In part (b), generally candidates understood that the demand of the question was to interpret the values "
                r"of $p$ and $q$ in context although some answers such as “it is the gradient of the line” were seen.",
         NO),
        ({"b"}, r"Most candidates were able to interpret the model well enough to understand that the value of $p$ was "
                r"the initial mass in kg of the algae in the pond."),
        ({"b"}, "Those that failed to score this mark usually referred to the “amount” of algae rather than the mass of "
                "algae.", BACK),
        ({"b"}, r"Candidates needed to understand that the constant $q$ was the rate at which the mass of algae increased "
                r"each week."),
        ({"b"}, r"It was a common misconception that the $q$ was the amount the mass of algae increases by each week.", NO),
        ({"b"}, r"Incomplete explanations without reference to the time frame were also common for example, “the "
                r"constant $q$ is the rate at which the algae increases.”", NO),
        ({"c"}, "In part (c), candidates who had a correct equation were generally able to complete the substitution "
                "successfully."),
        ({"c"}, r"Some candidates gained full marks after having incorrectly answered part (a), by using the equation "
                r"linking $\log_{10}A$ and $t$ given in the question."),
        ({"c"}, "As it was a modelling question, units were required to score this mark; most candidates used the correct "
                "units.", NO),
        ({"c"}, "This part of the question was also well attempted by many candidates."),
        ({"c"}, r"Those who found difficulties often tried to use $t=8$ which was information given for use in part i.", NO),
        ({"d"}, "In part (d), there were two limitations of the model: the first being the fact that it predicted unlimited "
                "growth and the second being that it predicted that the rate of growth remained constant.", NO),
        ({"d"}, "Most candidates successfully identified one of these limitations and were able to give a sufficient "
                "reason to explain in context why this was unrealistic.", BACK),
        ({"d"}, "Common explanations included a change in conditions – sunlight/temperature changes, algae dying or being "
                "removed, and the pond eventually being fully covered and the algae running out of resources to consume, "
                "leading to a slowing of the growth rate."),
    ],
    "06": [
        ({"a", "b"}, "The binomial question was fairly typical in its structure, so most candidates were able to make a "
                     "lot of progress in part (a), but part (b) proved to be much more challenging.", NO),
        ({"a"}, "Part (a) was general answered well, with almost all candidates scoring at least the first 2 marks."),
        ({"a"}, "Of those who did not score all of the marks, the most common mistake was ignoring the negative sign in "
                "the bracket.", NO),
        ({"a"}, r"Candidate dealt well with the coefficient of $x$, remembering in most cases to apply the power to it.",
         NO),
        ({"b"}, "Part (b) on the other hand was misunderstood by many candidates."),
        ({"b"}, r"Several simply stated the coefficient of the $x^2$ term in their expansion, or attempted to multiply the "
                r"bracket by their coefficient of $x^2$, leading to variations of $\frac{(504x^2-504x^3)}{x}$."),
        ({"b"}, r"A significant minority understood what was being asked of them, but incorrectly wrote $\frac{1}{2x}$ as "
                r"$2x^{-1}$ instead of $\frac{1}{2}x^{-1}$."),
    ],
    "07": [
        ({"a", "b"}, "Generally, candidates scored well in the first two parts of this question, by factorising the cubic "
                     "expression and drawing a graph."),
        ({"c"}, "The final part, however, where the candidates were required to find a range, was very poorly answered, "
                "with few gaining any marks and very few reaching the correct final answer."),
        ({"a"}, r"In part (a) almost all candidates successfully identified the factor of $x$ and were able to take this "
                r"factor out of the expression correctly.", NO),
        ({"a"}, r"Many candidates were confused by the negative $x^3$ term and it was common to see sign errors in their "
                r"final answer $x(x+3)(x-3)$ was a common incorrect answer, possibly made after using the equation solver "
                r"on the calculator to find the roots 3 and $-3$.", NO),
        ({"a"}, "Time permitting, candidates should be reminded to check that their factorisation is correct by expanding "
                "the result."),
        ({"b"}, "Part (b) proved to be accessible to most candidates and there were many fully correct responses seen."),
        ({"b"}, "Candidates who had made a sign error in part (a), were often able to recover and went on to draw a "
                "completely correct graph."),
        ({"b"}, "Axes were labelled with a scale in almost all diagrams."),
        ({"b"}, "However, a minority of candidates dropped one mark by sketching the graph of a positive cubic (with the "
                "correct roots), whilst a few candidates did not have their negative cubic curve going through the "
                "required roots."),
        ({"c"}, "Part (c) proved to be very challenging."),
        ({"c"}, "Candidates were unable to identify the need to differentiate with many of them treating the equation as "
                "if it were quadratic and attempting to find the discriminant.", NO),
        ({"c"}, r"Candidates who recognised the need to differentiate generally went on to find the $x$ coordinates "
                r"successfully, however, it was common for these candidates to write an inequality in terms of $x$ rather "
                r"than moving forward to find the associated $y$ coordinates.", NO),
        ({"c"}, "It appears many candidates are not truly confident in the specific meaning of the terms “domain” and "
                "“range”.", NO),
        ({"c"}, r"Of the relatively few candidates who did correctly calculate the $y$ coordinate of the turning points, "
                r"some still lost the final mark by failing to use correct set notation."),
        ({"c"}, r"A few responses were seen where decimal approximations to $\pm6\sqrt{3}$ had clearly been obtained from "
                r"calculator technology alone and these gained no credit.", NO),
    ],
    "08": [
        (W, "This question was reasonably well attempted."),
        (W, "Logs continue to be an area of challenge for many candidates but despite this, a significant proportion were "
            "able to earn a good number of marks here.", NO),
        ({"a"}, r"In part (a), many candidates were able to earn the mark for recognising that it was necessary to set "
                r"$t=0$ and correctly obtained $k=0.8$.", NO),
        ({"a"}, r"The most common error here occurred when candidates assumed, in error, that $\mathrm{e}^0=0$ and so "
                r"obtained $k=2.2$"),
        ({"b"}, r"In part (b), the majority of candidates were able to recognise that they needed to set their equation for "
                r"$P$ equal to 1."),
        ({"b"}, r"Those who had achieved $k=0.8$ in (a) usually made good progress and scored full marks in this part.", NO),
        ({"b"}, r"Those candidates who obtained $k=2.2$ were able to make a first step in solving the equation.", NO),
        ({"b"}, "They were, however, limited in their progress as the equation was ultimately unsolvable, but many "
                "attempted to persevere through taking logs of a negative value which was not creditworthy.", BACK),
        ({"b"}, r"Some candidates misunderstood the context here and thought that they needed $P=1.2$, perhaps misreading "
                r"the question which asked for a drop to an air pressure of 1 kg/cm$^3$ rather than a drop in air "
                r"pressure of 1 kg/cm$^3$.", {"note": "the question gives the pressure in kg/cm$^2$"}),
        ({"b"}, "Nonetheless these candidates were usually able to make good progress as the resulting equation was "
                "solvable in this case and some good log work was seen.", BACK),
        ({"b"}, "There were a small proportion of candidates who were clearly less secure in their log work however and "
                "some attempted to take logs of each term separately before rearranging or neglected to divide by 1.4 "
                "before taking logs."),
        ({"b"}, r"A small number of candidates attempted to use $\log_{10}$ rather than natural logs."),
        ({"b"}, "Almost all candidates realised they need to show all stages of their working and it was rare to see "
                "answers appear from nowhere due to overreliance on a calculator.", NO),
        ({"c"}, "Part (c) of this question was a good differentiator and was a challenge to many candidates."),
        ({"c"}, "For a significant proportion of candidates, “rate” did not signal the need for rate of change and hence "
                "differentiation."),
        ({"c"}, r"It was common to see candidates simply substituting in $t=2$ into their equation for $P$ to obtain "
                r"$P=1.32$.", NO),
        ({"c"}, r"Of those candidates who did attempt to find $\frac{\mathrm{d}P}{\mathrm{d}t}$ many seemed to struggle "
                r"with the chain rule.", NO),
        ({"c"}, r"Some candidates obtained results of the form $At\mathrm{e}^{-0.5t}$, whilst others retained the constant "
                r"term 0.8 when differentiating."),
        ({"c"}, r"Others began by substituting in $t=2$ and then proceeded from $\mathrm{e}^{-2}$ to $\mathrm{e}^{-1}$ or "
                r"‘differentiated’ $\mathrm{e}^{-1}$ to get $\mathrm{e}^{-2}$."),
        ({"c"}, r"It was common for candidates who were able to progress to a correct value to give the final answer of "
                r"$-0.258$ rather than 0.258 but this was condoned.", NO),
    ],
    "09": [
        (W, "Candidates still find working with logs a challenge and this type of question requires a careful approach to "
            "applying the laws of logarithms and making use of the “hence” which linked the two parts together."),
        ({"a"}, "Many candidates found part (a) difficult and hence this impacted on the overall scores.", NO),
        ({"a"}, "It required the understanding and use of logarithm laws.", BACK),
        ({"a"}, r"A majority were unable to write part (i) in terms of $p$ often because they could not simplify "
                r"$\log_39$."),
        ({"a"}, "Part (ii) was more successful."),
        ({"b"}, "In part (b), a pleasing number of the candidates received full marks with the majority not connecting part "
                "(a) to part (b), often starting again from the original equation and using laws of logarithms."),
        ({"b"}, r"Those candidates that did see the link often went on to find $p=-2$ and thus $x=\frac{1}{3}$.",
         {"ref": False, "note": "the mark scheme answer is $x=\\frac{1}{9}$"}),
        ({"b"}, r"However, a significant number stopped after finding the value of $p$ rather than $x$."),
        ({"b"}, "Those that had the linear terms correct in part (a) found this part easy and many proceeded to gain full "
                "marks.", NO),
        (W, r"Overall, there were far too many candidates unable to make any progress with this question on logs and many "
            r"indicated a lack of understanding of the relationship $p=\log_3x\Leftrightarrow x=3^p$"),
    ],
    "10": [
        (W, "This question was, on the whole, well-attempted and provided some differentiation between candidates."),
        ({"a"}, r"In part (a), the majority of candidates were able to correctly work through the steps required to derive "
                r"the equation of the tangent to curve $C$."),
        ({"a"}, r"The vast majority were able to successfully and accurately differentiate the equation of the curve and to "
                r"evaluate it at $x=4$ to find the gradient.", NO),
        ({"a"}, r"Most were then able to determine the $y$ coordinate of $P$ (although some candidates appeared to use the "
                r"equation of the tangent to find this value rather than the equation of the curve).", NO),
        ({"a"}, r"Most were confident and well prepared to correctly find the equation of the tangent, commonly using "
                r"$y-y_1=m(x-x_1)$ but also often $y=mx+c$ equally successfully."),
        ({"a"}, r"A small number of candidates incorrectly worked with the gradient of the normal rather than the gradient "
                r"of the tangent and there was sometimes confusion between the value of the gradient and the value of the "
                r"$y$ coordinate at $P$: $\frac{13}{6}$ and $\frac{13}{3}$ respectively."),
        ({"a"}, "There were a small number of candidates who worked from the equation of the tangent and who appeared to "
                "be attempting to verify this equation rather than deriving it.", NO),
        ({"b"}, "Most candidates made an attempt at part (b), and many were able to undertake some integration correctly."),
        ({"b"}, "There were sometimes slips on the fractional powers and the coefficients."),
        ({"b"}, "This question was effective at differentiating between those candidates who were able to clearly identify "
                "a strategy to determine the required area and many were successful in doing so.", NO),
        ({"b"}, r"Most who were successful, employed the main mark scheme approach of determining the area under the curve "
                r"between $x=0$ and $x=4$ followed by subtracting the area of the triangle however there were a number of "
                r"different approaches seen, including finding the area under the curve from $x=0$ to $x=2$ together with "
                r"the area between the curve and line between $x=2$ and $x=4$."),
        ({"b"}, "Errors were perhaps a little more common in the second of these two approaches perhaps due sign errors "
                "when subtracting the two equations.", BACK),
        ({"b"}, r"Unfortunately, though, a number of candidates were not clear on the strategy required and so it was not "
                r"uncommon to see attempts which stopped after calculating the area under the curve between $x=0$ and "
                r"$x=4$ and thus a value of $\frac{76}{9}$ was a fairly common incorrect final answer.", NO),
        ({"b"}, r"Others using one of the alternative approaches simply found the integral of the difference between the "
                r"two equations between $x=0$ and $x=4$ or between $x=0$ and $x=2$ and failed to go on the find the area "
                r"under the curve separately."),
        ({"b"}, "Most candidates had few issues identifying the intercept of the tangent with the x-axis but there was "
                "sometimes confusion in identifying the base and/or the height of the triangle when this was required to "
                "find the area.", NO),
        ({"b"}, "Some candidates lost the final A mark in this question by not giving the exact answer, giving it as a "
                "rounded decimal instead.", NO),
    ],
    "11": [
        ({"a", "b"}, "This question often enabled candidates to score marks in the first part, however, part (b) proved "
                     "to be very good at discriminating between the most able candidates.", NO),
        ({"a"}, "In part (a), there were very few non attempts."),
        ({"a"}, "Unfortunately, some did not know how to complete the square correctly and used 10 and 8, thus losing the "
                "marks."),
        ({"a"}, "The majority of candidates achieved full marks, however or two marks because of a slip, usually in "
                "finding the radius."),
        ({"b"}, "Part (b) was challenging for many; non attempts or attempts which achieved no marks were common."),
        ({"b"}, "Quite a few candidates scored the B mark for the gradient of the perpendicular and some went on to find "
                "the equation of the normal, but they did not find the point of intersection of the straight lines and so "
                "could not progress to the remaining marks."),
        ({"b"}, "It was common to see one of the straight-line equations substituted into the equation of the circle.",
         NO),
        ({"b"}, "Those who substituted the normal equation and had also found the point of intersection of the straight "
                "lines, often correctly found the distance between the points correctly and gained full marks.", NO),
        ({"b"}, "Those who found the distance between the centre and the point of intersection of the straight lines, "
                "often forgot to subtract 3 for the radius, thus losing the last two marks.", NO),
        ({"b"}, r"A large number of candidates found the $y$ intercept of the line $l$, and then the distance between "
                r"(0,3) and the centre.", {"note": "the $y$-intercept of $l$ is $(0,-3)$"}),
        ({"b"}, "A very small number of candidates used a vector method."),
    ],
    "12": [
        (W, "This was one of the most challenging questions on the paper for candidates, although it was a familiar "
            "structure to this type of problem and there was access to later parts as part (a) was a “show” question.",
         NO),
        ({"a"}, "Many candidates struggled with part (a)."),
        ({"a"}, "A few were able to gain the first B mark or make an attempt to sum the areas of the component parts, but "
                "many were unsure what to do with the 0.04 and 0.09."),
        ({"a"}, "A significant number equated these to the expressions for area.", BACK),
        ({"a"}, r"Better candidates were able to clearly identify the two circular ends and the curved surface, attaching "
                r"the correct costing to each and eliminating the $h$."),
        ({"a"}, "The small minority of candidates then scored 3/4 as they omitted to use C = or Cost = ."),
        ({"b", "c", "d"}, "Although the answer was given for part (a) numerous candidates made no attempts in the later "
                          "parts or failed to differentiate part (b) and so made no progress with part (c) or part (d)."),
        ({"b"}, "Most candidates achieved at least a method mark in (b) for attempting to differentiate."),
        ({"b"}, "A significant number of candidates set the second derivative equal to 0 and solved, instead of the first "
                "derivative."),
        ({"c"}, "In part (c), it was common for many of those who had understood the demands in part (b), to progress and "
                "find the second derivative.", NO),
        ({"c"}, "A lot were unsure what to do with it at this point, however, with a significant number equating it to zero "
                "and solving (sometimes when they had already solved correctly for 3.26 in (b)).", BACK),
        ({"d"}, "Of those who achieved a positive answer in (b), most were able to substitute into the model for M1 here.",
         NO),
        ({"d"}, "It is clear that many candidates had not read the question carefully or checked their answer, as a lot of "
                "candidates gave the answer £13 instead of 13p in part (d), which fortunately for them was condoned on "
                "this occasion.", NO),
        ({"d"}, "Candidates could be encouraged to sense check their modelling questions more as there were a variety of "
                "clear unfeasible answers here, including negative answers, and many hundreds of pounds."),
        ({"d"}, "Many also did not read that their answer should be rounded to the nearest integer, and lost marks "
                "unnecessarily."),
    ],
    "13": [
        (W, "There were a number of completely blank responses to both parts of this question."),
        (W, "This was either due to timing on the paper or possibly due to this topic not having been covered in "
            "sufficient depth due to disruption to learning.", BACK),
        ({"a"}, "In part (a), most of the attempts started with the LHS."),
        ({"a"}, r"Many scored no marks at all but quite a few combined terms with a common denominator to achieve the first "
                r"mark, usually $\frac{1+\sin\theta}{\cos\theta}$."),
        ({"a"}, r"However, very few progressed from this with many using “identities” such as $1+\sin\theta\equiv"
                r"\cos\theta$ and $\cos\theta\equiv1-\sin\theta$ to get to the RHS.", BACK),
        ({"a"}, "Candidates should avoid approaches to this type of problem involving an identity where it is treated as "
                "an equation where possible.", NO),
        ({"b"}, "In part (b) it was pleasing to see candidates making an attempt although there were quite a few with "
                "nothing at all correct.", NO),
        ({"b"}, r"These often had incorrect or irrelevant identities, resulting in equations which could not be solved for "
                r"$\sin2x$, meaning that they could not access the last method mark.", BACK),
        ({"b"}, r"Those who did achieve $\sin2x=\frac{2}{3}$ (or $-1$) usually solved correctly to get, at least, one value "
                r"of $x$, usually $x=20.9$ and very often the second value too.", NO),
        ({"b"}, "Most who got to this stage usually rejected any other values and scored full marks.", BACK),
        ({"b"}, r"Often, they had cancelled the $\cos2x$ earlier in their working, so they did not have to reject the extra "
                r"values at the end."),
        ({"b"}, "Usually this should be avoided, although on this occasion the domain meant that this did not affect their "
                "final answer.", BACK),
        ({"b"}, "It was pleasing to see that candidates had not tried to answer the question entirely by calculator by just "
                "stating the angles and the use of radians rather than degrees was not typically seen.", NO),
        ({"b"}, "Many did not recognise the relevance of part (a) and began this part from scratch, often successfully, "
                "even though they had not shown any relevant working for part (a)."),
    ],
    "14": [
        (W, "This question was poorly answered by the vast majority of candidates, although its position on the paper "
            "reflected that this topic is still a challenge to many.", NO),
        ({"i"}, r"In part (a), many candidates focussed inappropriately on $x=9$ and $x=\pm3$, taking no account of the $>$ "
                r"signs in the question.", {"note": "the paper numbers this part (i)"}),
        ({"i"}, r"For those choosing to correctly look for counter examples, a lack of brackets (e.g. $-4^2$) meant their "
                r"work was inaccurate and they did not score the mark, or they did not give an acceptable conclusion.",
         NO),
        ({"i"}, r"Several candidates only considered $x>3$ and it was surprising how many candidates concluded the "
                r"statement was true as a result.", NO),
        ({"i"}, "Finally, some candidates misinterpreted the syntax of the question, resulting in answers like “sometimes "
                "true”, which gained no credit, even though they had recognised the values required to find a counter "
                "example."),
        ({"ii"}, "In part (b), the few candidates gaining any credit managed to factorise and then occasionally state that "
                 "these were consecutive values, thus gaining 1 or occasionally 2 marks.",
         {"ref": False, "note": "the paper numbers this part (ii)"}),
        ({"ii"}, "A rare candidate went on to achieve the final accuracy mark using this approach with correct reasoning.",
         NO),
        ({"ii"}, r"The most common attempts generally included consideration of $n$ being even and then $n$ being odd with "
                 r"appropriate substitutions into the factorised expression and then an algebraic attempt which could not "
                 r"make any progress."),
        ({"ii"}, r"Less common was an attempt to write $n$ as the variations of $6k$, $6k+1$ etc. and complete similar "
                 r"algebraic work."),
        ({"ii"}, "This produced multiples of 6 but almost all candidates failed to progress to show the result holds for "
                 "all 6 cases.", BACK),
        ({"ii"}, r"A few attempts at induction were seen."),
        ({"ii"}, r"These normally started with a factorisation, the use of $n=1$ and attempts at algebraic manipulation to "
                 r"the stage showing $\mathrm{f}(k+1)=\mathrm{f}(k)+\mathrm{g}(k)$.", BACK),
        ({"ii"}, r"Here, candidates generally made errors in the getting the coefficients of $\mathrm{g}(k)$ or failed to "
                 r"factorise to the point at which they could reasonably conclude that $\mathrm{g}(k)$ was a multiple of "
                 r"6, instead often incorrectly changing their expression so that a factor of 6 then appeared."),
    ],
}


def at(q, opening):
    """(question, index) of the one REPORT sentence for q starting with these words."""
    hits = [i for i, s in enumerate(REPORT[q]) if s[1].startswith(opening)]
    if len(hits) != 1:
        raise SystemExit(f"Q{q}: {opening!r} matches {len(hits)} sentences")
    return q, hits[0]


# Difficulty by judgement (rubric in CLAUDE.md): rate by how many completed the part.
RATINGS = {
    "01": ("medium", at("01", "The most common error was dealing")),
    "02a": ("medium", at("02", "In part (a) the most common error")),
    "02b": ("easy", at("02", "In part (b) the vast majority")),
    "02c": ("medium", at("02", "With many responses")),
    "02d": ("hard", at("02", "Part (d) was poorly answered")),
    "03a": ("easy", at("03", "Many candidates tackled this question well")),
    "03b": ("easy", at("03", "In part (b), the concept and calculation")),
    "03c": ("medium", at("03", "Part (c) did provide problems")),
    "04ai": ("hard", at("04", "Many candidates did not attempt part (a)(i)")),
    "04aii": ("easy", at("04", "In (a)(ii), the")),
    "04b": ("easy", at("04", "Errors in part (b) were few")),
    "05a": ("medium", at("05", "A significant proportion of candidates")),
    "05b": ("medium", at("05", "It was a common misconception")),
    "05c": ("easy", at("05", "This part of the question was also well attempted")),
    "05d": ("easy", at("05", "Most candidates successfully identified")),
    "06a": ("easy", at("06", "Part (a) was general answered well")),
    "06b": ("hard", at("06", "Part (b) on the other hand")),
    "07a": ("medium", at("07", "Many candidates were confused")),
    "07b": ("easy", at("07", "Part (b) proved to be accessible")),
    "07c": ("hard", at("07", "The final part, however")),
    "08a": ("easy", at("08", "In part (a), many candidates were able")),
    "08b": ("easy", at("08", "Those who had achieved $k=0.8$")),
    "08c": ("hard", at("08", "Part (c) of this question was a good differentiator")),
    "09a": ("medium", at("09", "A majority were unable to write part (i)")),
    "09b": ("medium", at("09", "However, a significant number stopped")),
    "10a": ("easy", at("10", "In part (a), the majority of candidates")),
    "10b": ("medium", at("10", "This question was effective at differentiating")),
    "11a": ("easy", at("11", "The majority of candidates achieved full marks")),
    "11b": ("hard", at("11", "Part (b) was challenging for many")),
    "12a": ("hard", at("12", "Many candidates struggled with part (a)")),
    "12b": ("medium", at("12", "A significant number of candidates set the second derivative")),
    "12c": ("hard", at("12", "A lot were unsure what to do")),
    "12d": ("medium", at("12", "Many also did not read")),
    "13a": ("hard", at("13", "However, very few progressed")),
    "13b": ("medium", at("13", "In part (b) it was pleasing")),
    "14i": ("hard", at("14", "This question was poorly answered")),
    "14ii": ("hard", at("14", "In part (b), the few candidates")),
}


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
        main = [m for m in entry["mark_scheme"] or [] if not m.startswith("ALT:")]
        if entry["mark_scheme"] is not None and len(main) != entry["marks"]:
            raise SystemExit(f"{entry['id']}: {len(main)} main mark-scheme lines for {entry['marks']} marks")
    return entries


if __name__ == "__main__":
    out = ensure_out_dir("drafts") / f"{P}_{S}.json"
    entries = build()
    out.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(entries)} entries, {sum(x['marks'] or 0 for x in entries)} marks -> {out}")
