"""Draft builder for 8MA0-01 SAM (AS Pure, sample assessment materials).

Run (from the project root, with the venv active):
    python extraction/8MA0-01_SAM.py        # writes out/drafts/8MA0-01_SAM.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-01_SAM.json

Everything here is transcribed from the source PDFs, read as page images (the
question paper's text layer is unreadable). There is no examiner report for the
SAM, so examiner_notes, difficulty and difficulty_evidence are all null.
Follow CLAUDE.md for every field.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report, part_key  # noqa: E402
from paths import ensure_out_dir  # noqa: E402

P, S = "8MA0-01", "SAM"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "14c"); label as printed (e.g. "14(c)")."""
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
Q3 = [r"Given that the point $A$ has position vector $3\mathbf{i}-7\mathbf{j}$ and the point $B$ has position vector "
      r"$8\mathbf{i}+3\mathbf{j}$,"]
Q3A = r"find the vector $\overrightarrow{AB}$"
Q4 = [r"$$\mathrm{f}(x)=4x^3-12x^2+2x-6$$"]
Q4A = r"Use the factor theorem to show that $(x-3)$ is a factor of $\mathrm{f}(x)$."
Q7A = [r"Find the first 3 terms, in ascending powers of $x$, of the binomial expansion of",
       r"$\left(2-\frac{x}{2}\right)^7$, giving each term in its simplest form."]
Q8 = [r"[Figure 1: triangle $ABC$ with $AB$ horizontal and labelled 30 m, $C$ above $AB$; angle $70^\circ$ marked at $A$ "
      r"and angle $60^\circ$ marked at $B$; marked “Not to scale”.]",
      r"A triangular lawn is modelled by the triangle $ABC$, shown in Figure 1. The length $AB$ is to be 30 m long.",
      r"Given that angle $BAC=70^\circ$ and angle $ABC=60^\circ$,"]
Q8A = "calculate the area of the lawn to 3 significant figures."
Q11A = ["Prove that for all positive values of $x$ and $y$", r"$$\sqrt{xy}\leqslant\frac{x+y}{2}$$"]
Q12 = ["A student was asked to give the exact solution to the equation", r"$$2^{2x+4}-9(2^x)=0$$",
       "The student’s attempt is shown below:",
       r"$$\begin{aligned}&2^{2x+4}-9(2^x)=0\\&2^{2x}+2^4-9(2^x)=0\\&\text{Let }2^x=y\\&y^2-9y+8=0\\"
       r"&(y-8)(y-1)=0\\&y=8\text{ or }y=1\\&\text{So }x=3\text{ or }x=0\end{aligned}$$"]
Q13A = "Factorise completely $x^3+10x^2+25x$"
Q13B = ["Sketch the curve with equation", "$$y=x^3+10x^2+25x$$",
        "showing the coordinates of the points at which the curve cuts or touches the $x$-axis."]
Q14 = [r"[Figure 2: axes $t$ (horizontal) and $\log_{10}P$ (vertical) with origin $O$; a straight line $l$ with positive "
       r"gradient meets the vertical axis at $(0,5)$.]",
       r"A town’s population, $P$, is modelled by the equation $P=ab^t$, where $a$ and $b$ are constants and $t$ is the "
       r"number of years since the population was first recorded.",
       r"The line $l$ shown in Figure 2 illustrates the linear relationship between $t$ and $\log_{10}P$ for the "
       r"population over a period of 100 years.",
       r"The line $l$ meets the vertical axis at $(0, 5)$ as shown. The gradient of $l$ is $\frac{1}{200}$."]
Q14A = "Write down an equation for $l$."
Q14B = "Find the value of $a$ and the value of $b$."
Q16 = [r"[Figure 4: plan of the pool: a rectangle $ABDE$ with $A$ top left, $E$ top right, $B$ below $A$ and $D$ below "
       r"$E$; the top edge $AE$ is labelled $2x$ m and the side $ED$ is labelled $y$ m; $AE$ and $BD$ are dashed; a "
       r"semicircle $BCD$ lies below $BD$, with $C$ at its lowest point.]",
       "Figure 4 shows the plan view of the design for a swimming pool.",
       r"The shape of this pool $ABCDEA$ consists of a rectangular section $ABDE$ joined to a semicircular section $BCD$ "
       r"as shown in Figure 4.",
       r"Given that $AE=2x$ metres, $ED=y$ metres and the area of the pool is 250 m$^2$,"]
Q16A = ["show that the perimeter, $P$ metres, of the pool is given by", r"$$P=2x+\frac{250}{x}+\frac{\pi x}{2}$$"]
Q17 = ["A circle $C$ with centre at $(-2, 6)$ passes through the point $(10, 11)$."]
Q17A = "Show that the circle $C$ also passes through the point $(10, 1)$."

LATEX = {
    "01": L("The line $l$ passes through the points $A(3, 1)$ and $B(4, -2)$.", "Find an equation for $l$."),
    "02": L("The curve $C$ has equation", "$$y=2x^2-12x+16$$", "Find the gradient of the curve at the point $P(5, 6)$.",
            NOGRAPH),
    "03a": L(*Q3, "(a) " + Q3A),
    "03b": L(*Q3, "(a) " + Q3A,
             r"(b) Find $\left|\overrightarrow{AB}\right|$. Give your answer as a simplified surd."),
    "04a": L(*Q4, Q4A),
    "04b": L(*Q4, "(a) " + Q4A, r"(b) Hence show that 3 is the only real root of the equation $\mathrm{f}(x)=0$"),
    "05": L("Given that", r"$$\mathrm{f}(x)=2x+3+\frac{12}{x^2},\quad x>0$$",
            r"show that $\displaystyle\int_1^{2\sqrt{2}}\mathrm{f}(x)\,\mathrm{d}x=16+3\sqrt{2}$"),
    "06": L("Prove, from first principles, that the derivative of $3x^2$ is $6x$."),
    "07a": L(*Q7A),
    "07b": L("(a) " + Q7A[0], Q7A[1],
             r"(b) Explain how you would use your expansion to give an estimate for the value of $1.995^7$"),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, "(a) " + Q8A, "(b) Why is your answer unlikely to be accurate to the nearest square metre?"),
    "09": L(r"Solve, for $360^\circ\leqslant x<540^\circ$,", r"$$12\sin^2x+7\cos x-13=0$$",
            "Give your answers to one decimal place.", NOGRAPH),
    "10": L("The equation $kx^2+4kx+3=0$, where $k$ is a constant, has no real roots.", "Prove that",
            r"$$0\leqslant k<\frac{3}{4}$$"),
    "11a": L(*Q11A),
    "11b": L("(a) " + Q11A[0], Q11A[1],
             "(b) Prove by counter example that this is not true when $x$ and $y$ are both negative."),
    "12a": L(*Q12, "Identify the two errors made by the student."),
    "12b": L(*Q12, "Find the exact solution to the equation."),
    "13a": L(Q13A),
    "13b": L("(a) " + Q13A, "(b) " + Q13B[0], *Q13B[1:]),
    "13c": L("(a) " + Q13A, "(b) " + Q13B[0], *Q13B[1:],
             "The point with coordinates $(-3, 0)$ lies on the curve with equation",
             "$$y=(x+a)^3+10(x+a)^2+25(x+a)$$", "where $a$ is a constant.",
             "(c) Find the two possible values of $a$."),
    "14a": L(*Q14, Q14A),
    "14b": L(*Q14, "(a) " + Q14A, "(b) " + Q14B),
    "14c": L(*Q14, "(a) " + Q14A, "(b) " + Q14B, "(c) With reference to the model interpret",
             "(i) the value of the constant $a$,", "(ii) the value of the constant $b$."),
    "14d": L(*Q14, "(a) " + Q14A, "(b) " + Q14B, "(d) Find",
             r"(i) the population predicted by the model when $t=100$, giving your answer to the nearest hundred "
             r"thousand,",
             "(ii) the number of years it takes the population to reach 200 000, according to the model."),
    "14e": L(*Q14, "State two reasons why this may not be a realistic population model."),
    "15": L(r"[Figure 3: the curve $C_1$, a U-shaped parabola crossing the positive $y$-axis with its minimum point to "
            r"the right of the $y$-axis and above the $x$-axis; the curve $C_2$, rising steeply from below the $x$-axis "
            r"just to the right of $O$, crossing the $x$-axis and continuing to rise more gently to the right, below "
            r"$C_1$; marked “Diagram not drawn to scale”.]",
            "The curve $C_1$, shown in Figure 3, has equation $y=4x^2-6x+4$.",
            r"The point $P\left(\frac{1}{2}, 2\right)$ lies on $C_1$",
            r"The curve $C_2$, also shown in Figure 3, has equation $y=\frac{1}{2}x+\ln(2x)$.",
            "The normal to $C_1$ at the point $P$ meets $C_2$ at the point $Q$.",
            "Find the exact coordinates of $Q$.", NOGRAPH),
    "16a": L(*Q16, *Q16A),
    "16b": L(*Q16, "(a) " + Q16A[0], Q16A[1], r"(b) Explain why $0<x<\sqrt{\frac{500}{\pi}}$"),
    "16c": L(*Q16, "(a) " + Q16A[0], Q16A[1],
             "(c) Find the minimum perimeter of the pool, giving your answer to 3 significant figures."),
    "17a": L(*Q17, Q17A),
    "17b": L(*Q17, "(a) " + Q17A,
             r"The tangent to the circle $C$ at the point $(10, 11)$ meets the $y$ axis at the point $P$ and the tangent "
             r"to the circle $C$ at the point $(10, 1)$ meets the $y$ axis at the point $Q$.",
             "(b) Show that the distance $PQ$ is 58 explaining your method clearly."),
}

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", COORD, "3.1", 3, LATEX["01"],
      [r"M1 (AO 1.1b): Uses $y=mx+c$ with both $(3, 1)$ and $(4, -2)$ and attempt to find $m$ or $c$. Notes: Need correct "
       r"use of the given coordinates. Note that a correct answer implies all three marks in this question",
       r"A1 (AO 1.1b): $m=-3$. Notes: Need fractions simplified to $-3$ (in ways 1 and 2)",
       r"A1 (AO 1.1b): $c=10$ so $y=-3x+10$ o.e. Notes: Need constants combined accurately. N.B. Answer left in the form "
       r"$(y-1)=-3(x-3)$ or $(y-(-2))=-3(x-4)$ is awarded M1A1A0 as answers should be simplified by constants being "
       r"collected",
       r"ALT: Or Way 2 — M1 (AO 1.1b): Uses $\frac{y-y_1}{x-x_1}=\frac{y_2-y_1}{x_2-x_1}$ with both $(3, 1)$ and "
       r"$(4, -2)$. Notes: Need correct use of the given coordinates",
       r"ALT: Or Way 2 — A1 (AO 1.1b): Gradient simplified to $-3$ (may be implied). Notes: Need fractions simplified to "
       r"$-3$ (in ways 1 and 2)",
       r"ALT: Or Way 2 — A1 (AO 1.1b): $y=-3x+10$ o.e. Notes: Need constants combined accurately",
       r"ALT: Or Way 3 — M1 (AO 1.1b): Uses $ax+by+k=0$ and substitutes both $x=3$ when $y=1$ and $x=4$ when $y=-2$ with "
       r"attempt to solve to find $a$, $b$ or $k$ in terms of one of them. Notes: Need correct use of the given "
       r"coordinates",
       r"ALT: Or Way 3 — A1 (AO 1.1b): Obtains $a=3b$, $k=-10b$ or $3k=-10a$",
       r"ALT: Or Way 3 — A1 (AO 1.1b): Obtains $a=3$, $b=1$, $k=-10$ Or writes $3x+y-10=0$ o.e. Notes: Need constants "
       r"combined accurately"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02", "2", DIFF, "7.2, 7.1", 4, LATEX["02"],
      [r"M1 (AO 1.1a): Attempt to differentiate. Notes: Differentiation implied by one correct term",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}y}{\mathrm{d}x}=4x-12$. Notes: Correct differentiation",
       r"M1 (AO 1.1b): Substitutes $x=5\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}x}=\ldots$ Notes: Attempts to substitute "
       r"$x=5$ into their derived function",
       r"A1ft (AO 1.1b): $\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}x}=8$. Notes: Substitutes $x=5$ into $\textbf{their}$ "
       r"derived function $\textbf{correctly}$ i.e. Correct calculation of their $\mathrm{f}'(5)$ so follow through slips "
       r"in differentiation"],
      False, 3),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", VEC, "9.4, 9.3", 2, LATEX["03a"],
      [r"M1 (AO 1.1b): Attempts $\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}$ or similar. Notes: Attempts "
       r"subtraction but may omit brackets. Note that the correct answer implies M1A1 in each part of this question",
       r"A1 (AO 1.1b): $\overrightarrow{AB}=5\mathbf{i}+10\mathbf{j}$. Notes: cao (allow column vector notation)"],
      False, 4),
    e("03b", "3(b)", VEC, "9.2, 2.2", 2, LATEX["03b"],
      [r"M1 (AO 1.1b): Finds length using ‘Pythagoras’ $\left|AB\right|=\sqrt{(5)^2+(10)^2}$. Notes: Correct use of "
       r"Pythagoras theorem or modulus formula using their answer to (a). Note that the correct answer implies M1A1 in "
       r"each part of this question",
       r"A1ft (AO 1.1b): $\left|AB\right|=5\sqrt{5}$. Notes: $\left|AB\right|=5\sqrt{5}$ ft from their answer to (a)"],
      False, 4),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", ALG, "2.6", 2, LATEX["04a"],
      [r"M1 (AO 1.1b): States or uses $\mathrm{f}(+3)=0$. Notes: States or uses $\mathrm{f}(+3)=0$",
       r"A1 (AO 1.1b): $4(3)^3-12(3)^2+2(3)-6=108-108+6-6=0$ and so $(x-3)$ is a factor. Notes: See correct work "
       r"evaluating and achieving zero, together with correct conclusion"],
      False, 5),
    e("04b", "4(b)", ALG, "2.6, 2.3", 4, LATEX["04b"],
      [r"M1 (AO 2.1): Begins division or factorisation so $4x^3-12x^2+2x-6=(x-3)(4x^2+\ldots)$. Notes: Needs to have "
       r"$(x-3)$ and first term of quadratic correct",
       r"A1 (AO 1.1b): $4x^3-12x^2+2x-6=(x-3)(4x^2+2)$. Notes: Must be correct – may further factorise to "
       r"$2(x-3)(2x^2+1)$",
       r"M1 (AO 2.1): Considers the roots of their quadratic function using completion of square or discriminant. Notes: "
       r"Considers their quadratic for no real roots by use of completion of the square or consideration of discriminant "
       r"then",
       r"A1* (AO 2.4): $(4x^2+2)=0$ has no real roots with a reason (e.g. negative number does not have a real square "
       r"root, or $4x^2+2>0$ for all $x$. So $x=3$ is the only real root of $\mathrm{f}(x)=0$ *. Notes: A correct "
       r"explanation"],
      False, 5),

    # ---------------- Q5 ----------------
    e("05", "5", INT, "8.3, 8.2, 2.2", 5, LATEX["05"],
      [r"B1 (AO 1.1b): $\mathrm{f}(x)=2x+3+12x^{-2}$. Notes: Correct function with numerical powers",
       r"M1 (AO 1.1a): Attempts to integrate. Notes: Allow for raising power by one. $x^n\to x^{n+1}$",
       r"A1 (AO 1.1b): $\int\left(+2x+3+\frac{12}{x^2}\right)\mathrm{d}x=x^2+3x-\frac{12}{x}$. Notes: Correct three terms",
       r"M1 (AO 1.1b): $\left((2\sqrt{2})^2+3(2\sqrt{2})-\frac{12(\sqrt{2})}{2\times2}\right)-(-8)$. Notes: Substitutes "
       r"limits and rationalises denominator",
       r"A1* (AO 1.1b): $=16+3\sqrt{2}$ *. Notes: Completely correct, no errors seen"],
      False, 6),

    # ---------------- Q6 ----------------
    e("06", "6", DIFF, "7.1", 4, LATEX["06"],
      [r"B1 (AO 2.1): Considers $\frac{3(x+h)^2-3x^2}{h}$. Notes: Gives correct fraction as in the scheme above or "
       r"$\frac{3(x+\delta x)^2-3x^2}{\delta x}$",
       r"M1 (AO 1.1b): Expands $3(x+h)^2=3x^2+6xh+3h^2$. Notes: Expands the bracket as above or "
       r"$3(x+\delta x)^2=3x^2+6x\delta x+3(\delta x)^2$",
       r"A1 (AO 1.1b): So gradient $=\frac{6xh+3h^2}{h}=6x+3h$ or $\frac{6x\delta x+3(\delta x)^2}{\delta x}=6x+3\delta x$. "
       r"Notes: Substitutes correctly into earlier fraction and simplifies",
       r"A1* (AO 2.5): States as $h\to0$, gradient $\to6x$ so in the limit derivative $=6x$ *. Notes: Uses Completes the "
       r"proof, as above ( may use $\delta x\to0$), considers the limit and states a conclusion with no errors"],
      False, 7),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", SEQ, "4.1", 4, LATEX["07a"],
      [r"M1 (AO 1.1b): $\left(2-\frac{x}{2}\right)^7=2^7+\binom{7}{1}2^6\cdot\left(-\frac{x}{2}\right)+\binom{7}{2}2^5"
       r"\cdot\left(-\frac{x}{2}\right)^2+\ldots$ Notes: Need correct binomial coefficient with correct power of 2 and "
       r"correct power of $x$. Coefficients may be given in any correct form; e.g. 1, 7, 21 or ${}^7C_0$, ${}^7C_1$, "
       r"${}^7C_2$ or equivalent",
       r"B1 (AO 1.1b): $\left(2-\frac{x}{2}\right)^7=128+\ldots$ Notes: Correct answer, simplified as given in the scheme",
       r"A1 (AO 1.1b): $\left(2-\frac{x}{2}\right)^7=\ldots-224x+\ldots$ Notes: Correct answer, simplified as given in the "
       r"scheme",
       r"A1 (AO 1.1b): $\left(2-\frac{x}{2}\right)^7=\ldots+\ldots+168x^2\ (+\ldots)$. Notes: Correct answer, simplified "
       r"as given in the scheme"],
      False, 8),
    e("07b", "7(b)", SEQ, "4.1", 1, LATEX["07b"],
      [r"B1 (AO 2.4): Solve $\left(2-\frac{x}{2}\right)=1.995$ so $x=0.01$ and state that 0.01 would be substituted for "
       r"$x$ into the expansion. Notes: Needs a full explanation i.e. to state $x=0.01$ and that this would be "
       r"substituted and that it is a solution of $\left(2-\frac{x}{2}\right)=1.995$"],
      False, 8),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", TRIG, "5.1", 4, LATEX["08a"],
      [r"M1 (AO 2.1): Way 1: Finds third angle of triangle and uses or states $\frac{x}{\sin60^\circ}=\frac{30}"
       r"{\sin\text{“}50^\circ\text{”}}$. Notes: Uses sine rule with their third angle to find one of the unknown side "
       r"lengths",
       r"A1 (AO 1.1b): Way 1: So $x=\frac{30\sin60^\circ}{\sin50^\circ}\ (=33.9)$. Notes: Finds expression for, or value "
       r"of either side length",
       r"M1 (AO 3.1a): Area $=\frac{1}{2}\times30\times x\times\sin70^\circ$ or $\frac{1}{2}\times30\times y\times\sin60$. "
       r"Notes: Completes method to find area of triangle",
       r"A1ft (AO 1.1b): $=478\text{ m}^2$. Notes: Obtains a correct answer for their value of $x$ or their value of $y$",
       r"ALT: Way 2 — M1 (AO 2.1): Finds third angle of triangle and uses or states $\frac{y}{\sin70^\circ}=\frac{30}"
       r"{\sin\text{“}50^\circ\text{”}}$. Notes: Uses sine rule with their third angle to find one of the unknown side "
       r"lengths",
       r"ALT: Way 2 — A1 (AO 1.1b): So $y=\frac{30\sin70^\circ}{\sin50^\circ}\ (=36.8)$. Notes: Finds expression for, "
       r"or value of either side length"],
      True, 10),
    e("08b", "8(b)", TRIG, "5.1", 1, LATEX["08b"],
      [r"B1 (AO 3.2b): Plausible reason e.g. Because the angles and the side length are not given to four significant "
       r"figures Or e.g. The lawn may not be flat. Notes: As information given in the question may not be accurate to 4sf "
       r"or the lawn may not be flat so modelling by a plane figure may not be accurate"],
      True, 10),

    # ---------------- Q9 ----------------
    e("09", "9", TRIG, "5.4, 5.3", 5, LATEX["09"],
      [r"M1 (AO 3.1a): Uses $\sin^2x=1-\cos^2x\Rightarrow12(1-\cos^2x)+7\cos x-13=0$. Notes: Uses correct identity",
       r"A1 (AO 1.1b): $\Rightarrow12\cos^2x-7\cos x+1=0$. Notes: Correct three term quadratic",
       r"M1 (AO 1.1b): Uses solution of quadratic to give $\cos x=$ Notes: Solves their three term quadratic to give "
       r"values for $\cos x$. (The correct answers are $\cos x=\frac{1}{3}$ or $\frac{1}{4}$ but this is not necessary "
       r"for this method mark)",
       r"M1 (AO 1.1b): Uses inverse cosine on their values, giving two correct follow through values (see note). Notes: "
       r"Uses inverse cosine on their values, giving two correct follow through values - may be outside the given domain",
       r"A1 (AO 1.1b): $\Rightarrow x=430.5^\circ,\ 435.5^\circ$. Notes: Two correct answers in the given domain"],
      False, 12),

    # ---------------- Q10 ----------------
    e("10", "10", ALG, "2.3, 2.5, 1.1", 4, LATEX["10"],
      [r"B1 (AO 3.1a): Realises that $k=0$ will give no real roots as equation becomes $3=0$ (proof by contradiction). "
       r"Notes: Explains why $k=0$ gives no real roots",
       r"M1 (AO 2.4): (For $k\neq0$) quadratic has no real roots provided $b^2<4ac$ so $16k^2<12k$. Notes: Considers "
       r"discriminant to give quadratic inequality – does not need the $k\neq0$ for this mark",
       r"M1 (AO 1.1b): $4k(4k-3)<0$ with attempt at solution. Notes: Attempts solution of quadratic inequality",
       r"A1* (AO 2.1): So $0<k<\frac{3}{4}$, which together with $k=0$ gives $0\leqslant k<\frac{3}{4}$ *. Notes: Draws "
       r"conclusion, which is a printed answer, with no errors (dependent on all three previous marks)"],
      False, 14),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", PROOF, "1.1, 2.2", 2, LATEX["11a"],
      [r"M1 (AO 2.1): Way 1: Since $x$ and $y$ are positive, their square roots are real and so "
       r"$(\sqrt{x}-\sqrt{y})^2\geqslant0$ giving $x-2\sqrt{x}\sqrt{y}+y\geqslant0$. Notes: Need two stages of the three "
       r"stage argument involving the three stages, squaring, square rooting terms and rearranging",
       r"A1* (AO 2.2a): $\therefore2\sqrt{xy}\leqslant x+y$ provided $x$ and $y$ are positive and so "
       r"$\sqrt{xy}\leqslant\frac{x+y}{2}$ *. Notes: Need all three stages making the correct deduction to achieve the "
       r"printed result",
       r"ALT: Way 2 Longer method — M1 (AO 2.1): Since $(x-y)^2\geqslant0$ for real values of $x$ and $y$, "
       r"$x^2-2xy+y^2\geqslant0$ and so $4xy\leqslant x^2+2xy+y^2$ i.e. $4xy\leqslant(x+y)^2$. Notes: Need two stages of "
       r"the three stage argument involving the three stages, squaring, square rooting terms and rearranging",
       r"ALT: Way 2 Longer method — A1* (AO 2.2a): $\therefore2\sqrt{xy}\leqslant x+y$ provided $x$ and $y$ are positive "
       r"and so $\sqrt{xy}\leqslant\frac{x+y}{2}$ *. Notes: Need all three stages making the correct deduction to achieve "
       r"the printed result"],
      False, 15),
    e("11b", "11(b)", PROOF, "1.1", 1, LATEX["11b"],
      [r"B1 (AO 2.4): Let $x=-3$ and $y=-5$ then LHS $=\sqrt{15}$ and RHS $=-4$ so as $\sqrt{15}>-4$ result does not "
       r"apply. Notes: Chooses two negative values and substitutes, then states conclusion"],
      False, 15),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", ALG, "2.1", 2, LATEX["12a"],
      [r"B1 (AO 2.3): $2^{2x}+2^4$ is wrong in line 2 - it should be $2^{2x}\times2^4$. Notes: Lists error in line 2 (as "
       r"above)",
       r"B1 (AO 2.3): In line 4, $2^4$ has been replaced by 8 instead of by 16. Notes: Lists error in line 4 (as above)"],
      False, 16),
    e("12b", "12(b)", EXP, "6.5, 6.4, 2.1", 2, LATEX["12b"],
      [r"M1 (AO 2.1): Way 1: $2^{2x+4}-9(2^x)=0$, $2^{2x}\times2^4-9(2^x)=0$, Let $2^x=y$, $16y^2-9y=0$. Notes: Correct "
       r"work with powers reaching this equation",
       r"A1 (AO 1.1b): Way 1: $y=\frac{9}{16}$ or $y=0$. So $x=\log_2\left(\frac{9}{16}\right)$ or "
       r"$\frac{\log\left(\frac{9}{16}\right)}{\log2}$ o.e. with no second answer. Notes: Correct answer here – there are "
       r"many exact equivalents",
       r"ALT: Way 2 — M1 (AO 2.1): $(2x+4)\log2-\log9-x\log2=0$. Notes: Correct work with powers reaching this equation",
       r"ALT: Way 2 — A1 (AO 1.1b): $x=\frac{\log9}{\log2}-4$ o.e. Notes: Correct answer here – there are many exact "
       r"equivalents"],
      False, 16),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", ALG, "2.6", 2, LATEX["13a"],
      [r"M1 (AO 1.1b): $x^3+10x^2+25x=x(x^2+10x+25)$. Notes: Takes out factor $x$",
       r"A1 (AO 1.1b): $=x(x+5)^2$. Notes: Correct factorisation – allow $x(x+5)(x+5)$"],
      False, 18),
    e("13b", "13(b)", ALG, "2.7", 2, LATEX["13b"],
      [r"M1 (AO 1.1b): A cubic with correct orientation. [Sketch: a positive cubic touching the $x$-axis at $-5$ (a "
       r"maximum), with a minimum between $-5$ and $O$ below the $x$-axis, then passing through the origin and rising.] "
       r"Notes: Correct shape",
       r"A1ft (AO 1.1b): Curve passes through the origin $(0, 0)$ and touches at $(-5, 0)$ (see note below for ft). "
       r"Notes: Curve passes through the origin $(0, 0)$ and touches at $(-5, 0)$ – allow follow through from incorrect "
       r"factorisation"],
      False, 18),
    e("13c", "13(c)", ALG, "2.8, 2.6", 3, LATEX["13c"],
      [r"M1 (AO 3.1a): Curve has been translated $a$ to the left. Notes: May be implied by one of the correct answers for "
       r"$a$ or by a statement",
       r"A1ft (AO 3.2a): $a=-2$. Notes: ft from their cubic as long as it meets the $x$-axis only twice",
       r"A1ft (AO 1.1b): $a=3$. Notes: ft from their cubic as long as it meets the $x$-axis only twice"],
      False, 18),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", EXP, "6.6", 2, LATEX["14a"],
      [r"M1 (AO 1.1b): $\log_{10}P=mt+c$. Notes: Uses a linear equation to relate $\log P$ and $t$",
       r"A1 (AO 1.1b): $\log_{10}P=\frac{1}{200}t+5$. Notes: Correct use of gradient and intercept to give a correct line "
       r"equation"],
      True, 20),
    e("14b", "14(b)", EXP, "6.6, 6.4", 4, LATEX["14b"],
      [r"M1 (AO 2.1): Way 1: As $P=ab^t$ then $\log_{10}P=t\log_{10}b+\log_{10}a$. Notes: $\textbf{Way 1:}$ Uses logs "
       r"correctly to give log equation",
       r"M1 (AO 1.1b): Way 1: $\log_{10}b=\frac{1}{200}$ or $\log_{10}a=5$. Notes: $\textbf{Way 1:}$ Identifies $\log b$ "
       r"or $\log a$ or both",
       r"A1 (AO 1.1b): So $a=100\,000$ $\textbf{or}$ $b=1.0116$. Notes: Correct value for $a$ or $b$",
       r"A1 (AO 1.1b): Both $a=100\,000$ $\textbf{and}$ $b=1.0116$ (awrt 1.01). Notes: Correct values for both",
       r"ALT: Way 2 — M1 (AO 2.1): As $\log_{10}P=\frac{t}{200}+5$ then $P=10^{\left(\frac{t}{200}+5\right)}="
       r"10^510^{\left(\frac{t}{200}\right)}$. Notes: $\textbf{Way 2:}$ Uses powers correctly to “undo” log equation and "
       r"expresses as product of two powers",
       r"ALT: Way 2 — M1 (AO 1.1b): $a=10^5$ or $b=10^{\left(\frac{1}{200}\right)}$. Notes: $\textbf{Way 2:}$ Identifies "
       r"$a$ or $b$ as powers of 10",
       r"ALT: Way 2 — A1 (AO 1.1b): So $a=100\,000$ $\textbf{or}$ $b=1.0116$. Notes: Correct value for $a$ or $b$",
       r"ALT: Way 2 — A1 (AO 1.1b): Both $a=100\,000$ $\textbf{and}$ $b=1.0116$ (awrt 1.01). Notes: Correct values for "
       r"both"],
      True, 20),
    e("14c", "14(c)", EXP, "6.7, 6.6", 2, LATEX["14c"],
      [r"B1 (AO 3.4): (c)(i) The initial population. Notes: Accept equivalent answers e.g. The population at $t=0$",
       r"B1 (AO 3.4): (c)(ii) The proportional increase of population each year. Notes: So accept rate at which the "
       r"population is increasing each year or scale factor 1.01 or increase of 1% per year"],
      True, 20),
    e("14d", "14(d)", EXP, "6.7, 6.4", 3, LATEX["14d"],
      [r"B1 (AO 3.4): (d)(i) 300000 to nearest hundred thousand. Notes: cao",
       r"M1 (AO 3.4): (d)(ii) Uses $200\,000=ab^t$ with their values of $a$ and $b$ or $\log_{10}200000=\frac{1}{200}t+5$ "
       r"and rearranges to give $t=$ Notes: As in the scheme",
       r"A1ft (AO 1.1b): (d)(ii) 60.2 years to 3sf. Notes: On their values of $a$ and $b$ with correct log work"],
      True, 20),
    e("14e", "14(e)", EXP, "6.7", 2, LATEX["14e"],
      [r"B1 (AO 3.5b): Any two valid reasons- e.g. • 100 years is a long time and population may be affected by wars and "
       r"disease • Inaccuracies in measuring gradient may result in widely different estimates • Population growth may "
       r"not be proportional to population size • The model predicts unlimited growth. Notes: As given in the scheme – any "
       r"two valid reasons [the mark scheme awards these two marks as one B2 (AO 3.5b); this line is the first of them]",
       r"B1 (AO 3.5b): [second mark of the B2 above: a second valid reason]"],
      True, 20),

    # ---------------- Q15 ----------------
    e("15", "15", DIFF, "7.3, 3.1, 6.3", 8, LATEX["15"],
      [r"M1 (AO 3.1a): Finds $\frac{\mathrm{d}y}{\mathrm{d}x}=8x-6$. Notes: Differentiates correctly",
       r"M1 (AO 1.1b): Gradient of curve at $P$ is $-2$. Notes: Substitutes $x=\frac{1}{2}$ to find gradient (may make a "
       r"slip)",
       r"M1 (AO 1.1b): Normal gradient is $-\frac{1}{m}=\frac{1}{2}$. Notes: Uses negative reciprocal gradient",
       r"A1 (AO 1.1b): So equation of normal is $(y-2)=\frac{1}{2}\left(x-\frac{1}{2}\right)$ or $4y=2x+7$. Notes: Correct "
       r"equation for normal",
       r"M1 (AO 3.1a): Eliminates $y$ between $y=\frac{1}{2}x+\ln(2x)$ and their normal equation to give an equation in "
       r"$x$. Notes: Attempts to eliminate $y$ to find an equation in $x$",
       r"M1 (AO 1.1b): Solves their $\ln2x=\frac{7}{4}$ so $x=\frac{1}{2}\mathrm{e}^{\frac{7}{4}}$. Notes: Attempts to "
       r"solve their equation using exp",
       r"M1 (AO 1.1b): Substitutes to give value for $y$. Notes: Uses their $x$ value to find $y$",
       r"A1 (AO 1.1b): Point $Q$ is $\left(\frac{1}{2}\mathrm{e}^{\frac{7}{4}},\ \frac{1}{4}\mathrm{e}^{\frac{7}{4}}+"
       r"\frac{7}{4}\right)$. Notes: Any correct exact form"],
      True, 22),

    # ---------------- Q16 ----------------
    e("16a", "16(a)", ALG, "2.6", 4, LATEX["16a"],
      [r"B1 (AO 2.1): Sets $2xy+\frac{\pi x^2}{2}=250$. Notes: Correct area equation",
       r"M1 (AO 1.1b): Obtain $y=\frac{250-\frac{\pi x^2}{2}}{2x}$ and substitute into $P$. Notes: Rearranges "
       r"$\textbf{their}$ area equation to make $y$ the subject of the formula and attempt to use with an expression for "
       r"$P$",
       r"M1 (AO 2.1): Use $P=2x+2y+\pi x$ with their $y$ substituted. Notes: Use correct equation for perimeter with their "
       r"$y$ substituted",
       r"A1* (AO 1.1b): $P=2x+\frac{250}{x}-\frac{\pi x^2}{2x}+\pi x=2x+\frac{250}{x}+\frac{\pi x}{2}$ *. Notes: Completely "
       r"correct solution to obtain and state printed answer"],
      True, 24),
    e("16b", "16(b)", ALG, "2.5", 2, LATEX["16b"],
      [r"M1 (AO 2.4): $x>0$ and $y>0$ (distance) $\Rightarrow\frac{250-\frac{\pi x^2}{2}}{2x}>0$ or "
       r"$250-\frac{\pi x^2}{2}>0$ o.e. Notes: States $x>0$ and $y>0$ and uses their expression from (a) to form "
       r"inequality",
       r"A1* (AO 3.2a): As $x$ and $y$ are distances they are positive so $0<x<\sqrt{\frac{500}{\pi}}$ *. Notes: Explains "
       r"that $x$ and $y$ are positive because they are distances, and uses correct expression for $y$ to give the "
       r"printed answer correctly"],
      True, 24),
    e("16c", "16(c)", DIFF, "7.3, 7.2", 4, LATEX["16c"],
      [r"M1 (AO 3.4): Differentiates $P$ with negative index correct in $\frac{\mathrm{d}P}{\mathrm{d}x}$; "
       r"$x^{-1}\to x^{-2}$. Notes: Attempt to differentiate $P$ (deals with negative power of $x$ correctly)",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}P}{\mathrm{d}x}=2-\frac{250}{x^2}+\frac{\pi}{2}$. Notes: Correct differentiation",
       r"M1 (AO 1.1b): Sets $\frac{\mathrm{d}P}{\mathrm{d}x}=0$ and proceeds to $x=$ Notes: Sets derived function equal "
       r"to zero and obtains $x=$",
       r"A1 (AO 1.1b): Substitutes their $x$ into $P=2x+\frac{250}{x}+\frac{\pi x}{2}$ to give perimeter $=59.8$ M. "
       r"Notes: The value of $x$ may not be seen (it is 8.37 to 3sf or $\sqrt{\left(\frac{500}{4+\pi}\right)}$) Need to "
       r"see awrt 59.8 M with units included for the perimeter"],
      True, 24),

    # ---------------- Q17 ----------------
    e("17a", "17(a)", COORD, "3.2", 3, LATEX["17a"],
      [r"M1 (AO 3.1a): Way 1: Finds circle equation $(x\pm2)^2+(y\mp6)^2=(10\pm(-2))^2+(11\mp6)^2$. Notes: Starts to use "
       r"information in question to find equation of circle or radius of circle",
       r"M1 (AO 1.1b): Way 1: Checks whether $(10, 1)$ satisfies their circle equation. Notes: Completes method for "
       r"checking that $(10, 1)$ lies on circle",
       r"A1* (AO 2.1): Way 1: Obtains $(x+2)^2+(y-6)^2=13^2$ and checks that $(10+2)^2+(1-6)^2=13^2$ so states that "
       r"$(10, 1)$ lies on $C$ *. Notes: Completely correct explanation with no errors concluding with statement that "
       r"circle passes through $(10, 1)$",
       r"ALT: Way 2 — M1 (AO 3.1a): Finds distance between $(-2, 6)$ and $(10, 11)$. Notes: Starts to use information in "
       r"question to find equation of circle or radius of circle",
       r"ALT: Way 2 — M1 (AO 1.1b): Finds distance between $(-2, 6)$ and $(10, 1)$. Notes: Completes method for checking "
       r"that $(10, 1)$ lies on circle",
       r"ALT: Way 2 — A1* (AO 2.1): Concludes that as distance is the same $(10, 1)$ lies on the circle $C$ *. Notes: "
       r"Completely correct explanation with no errors concluding with statement that circle passes through $(10, 1)$"],
      False, 26),
    e("17b", "17(b)", COORD, "3.2, 3.1", 7, LATEX["17b"],
      [r"M1 (AO 3.1a): Finds radius gradient $\frac{11-6}{10-(-2)}$ or $\frac{1-6}{10-(-2)}$ $(m)$. Notes: Calculates "
       r"$\frac{11-6}{10-(-2)}$ or $\frac{1-6}{10-(-2)}$ $(m)$",
       r"M1 (AO 1.1b): Finds gradient perpendicular to their radius using $-\frac{1}{m}$. Notes: Finds $-\frac{1}{m}$ "
       r"(correct answer is $-\frac{12}{5}$ $\textbf{or}$ $\frac{12}{5}$). This is referred to as $m'$ in the next note",
       r"M1 (AO 1.1b): Finds (equation and ) $y$ intercept of tangent (see note below). Notes: Attempts "
       r"$y-11=\mathit{their}\left(-\frac{12}{5}\right)(x-10)$ or $y-1=\mathit{their}\left(\frac{12}{5}\right)(x-10)$ and "
       r"puts $x=0$, or uses vectors to find intercept e.g. $\frac{y-11}{10}=-m'$",
       r"A1 (AO 1.1b): Obtains a correct value for $y$ intercept of their tangent i.e. 35 or $-23$. Notes: One correct "
       r"intercept 35 or $-23$",
       r"M1 (AO 1.1b): Way 1: Deduces gradient of second tangent. Notes: Way 1: Uses the negative of their previous "
       r"tangent gradient or uses a correct $-\frac{12}{5}$ or $\frac{12}{5}$",
       r"M1 (AO 1.1b): Way 1: Finds (equation and ) $y$ intercept of second tangent. Notes: Way 1: Attempts the second "
       r"tangent equation and puts $x=0$ or uses vectors to find intercept e.g. $\frac{11-y}{10}=m'$",
       r"A1* (AO 1.1b): So obtains distance $PQ=35+23=58$*. Notes: Ways 1 and 2: Obtain 58 correctly from a valid method",
       r"ALT: Way 2 — M1 (AO 1.1b): Deduces midpoint of $PQ$ from symmetry $(0, 6)$. Notes: Finds midpoint of $PQ$ from "
       r"symmetry. (This is at $(0, 6)$)",
       r"ALT: Way 2 — M1 (AO 1.1b): Uses this to find other intercept. Notes: Uses this midpoint to find second intercept "
       r"or to find difference between midpoint and first intercept. e.g. $35-6=29$ then $6-29=-23$ so second intercept "
       r"is at $(-23, 0)$"],
      False, 26),
]

# No examiner report is published for the SAM, so there is nothing to apply.
W = None
REPORT = {}

# No report, so no difficulty can be judged: every part is (None, None).
RATINGS = {q: (None, None) for q in
           ["01", "02", "03a", "03b", "04a", "04b", "05", "06", "07a", "07b", "08a", "08b", "09", "10", "11a", "11b",
            "12a", "12b", "13a", "13b", "13c", "14a", "14b", "14c", "14d", "14e", "15", "16a", "16b", "16c", "17a",
            "17b"]}


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
