"""Draft builder for 9MA0-01 2021-10 (A level Pure Paper 1, October 2021).

Run (from the project root, with the venv active):
    python extraction/9MA0-01_2021-10.py        # writes out/drafts/9MA0-01_2021-10.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-01_2021-10.json

Everything here is transcribed from the source PDFs, read as page images
(figures at 200 dpi). Follow CLAUDE.md for every field.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report, part_key  # noqa: E402
from mark_codes import main_marks  # noqa: E402
from paths import ensure_out_dir  # noqa: E402

P, S = "9MA0-01", "2021-10"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "15ii"); label as printed (e.g. "15(ii)")."""
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
NUM = "Numerical methods"
VEC = "Vectors"


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


DY = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
DX = r"\,\mathrm{d}x"
I, J, K = r"\mathbf{i}", r"\mathbf{j}", r"\mathbf{k}"
SHOW = [r"In this question you should show all stages of your working.",
        r"Solutions relying entirely on calculator technology are not acceptable."]

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q2 = ["Given that", r"$$\mathrm{f}(x)=x^2-4x+5\qquad x\in\mathbb{R}$$"]
Q2A = r"express $\mathrm{f}(x)$ in the form $(x+a)^2+b$ where $a$ and $b$ are integers to be found."
Q3 = [r"The sequence $u_1,u_2,u_3,\ldots$ is defined by", r"$$u_{n+1}=k-\frac{24}{u_n}\qquad u_1=2$$",
      "where $k$ is an integer.", "Given that $u_1+2u_2+u_3=0$"]
Q3A = ["show that", "$$3k^2-58k+240=0$$"]
Q3B = "Find the value of $k$, giving a reason for your answer."
Q4 = [r"The curve with equation $y=\mathrm{f}(x)$ where", r"$$\mathrm{f}(x)=x^2+\ln(2x^2-4x+5)$$",
      r"has a single turning point at $x=\alpha$"]
Q4A = [r"Show that $\alpha$ is a solution of the equation", "$$2x^3-4x^2+7x-2=0$$"]
Q4M = ["The iterative formula", r"$$x_{n+1}=\frac{1}{7}(2+4x_n^{\,2}-2x_n^{\,3})$$",
       r"is used to find an approximate value for $\alpha$."]
Q5 = SHOW + ["A company made a profit of £20 000 in its first year of trading, Year 1",
             "A model for future trading predicts that the yearly profit will increase by 8% each year, so that the yearly "
             "profits will form a geometric sequence.",
             "According to the model,"]
Q6 = [r"[Figure 1: a triangle $ABC$ with $A$ at the bottom left, $C$ above and a little to the right of $A$, and $B$ to "
      r"the right, slightly above $A$.]",
      "Figure 1 shows a sketch of triangle $ABC$.", "Given that",
      rf"• $\overrightarrow{{AB}}=-3{I}-4{J}-5{K}$", rf"• $\overrightarrow{{BC}}={I}+{J}+4{K}$"]
Q6A = r"find $\overrightarrow{AC}$"
Q7 = ["The circle $C$ has equation", "$$x^2+y^2-10x+4y+11=0$$"]
Q8 = ["A scientist is studying the growth of two different populations of bacteria.",
      r"The number of bacteria, $N$, in the $\textbf{first}$ population is modelled by the equation",
      r"$$N=A\mathrm{e}^{kt}\qquad t\geqslant0$$",
      "where $A$ and $k$ are positive constants and $t$ is the time in hours from the start of the study.",
      "Given that", "• there were 1000 bacteria in this population at the start of the study",
      "• it took exactly 5 hours from the start of the study for this population to double"]
Q8A = "find a complete equation for the model."
Q9 = [r"$$\mathrm{f}(x)=\frac{50x^2+38x+9}{(5x+2)^2(1-2x)}\qquad x\neq-\frac{2}{5}\quad x\neq\frac{1}{2}$$",
      r"Given that $\mathrm{f}(x)$ can be expressed in the form",
      r"$$\frac{A}{5x+2}+\frac{B}{(5x+2)^2}+\frac{C}{1-2x}$$", "where $A$, $B$ and $C$ are constants"]
Q9A = ["(a) (i) find the value of $B$ and the value of $C$", "(ii) show that $A=0$"]
Q10A = [r"Given that $1+\cos2\theta+\sin2\theta\neq0$ prove that",
        r"$$\frac{1-\cos2\theta+\sin2\theta}{1+\cos2\theta+\sin2\theta}\equiv\tan\theta$$"]
Q11 = [r"[Figure 2: the curve $y=(\ln x)^2$ for $x>0$, coming down steeply from high up near the $y$-axis, touching the "
       r"$x$-axis at a minimum between $O$ and 2, then rising; the region $R$ under the curve between $x=2$ and $x=4$ is "
       r"shaded.]",
       "Figure 2 shows a sketch of part of the curve with equation", r"$$y=(\ln x)^2\qquad x>0$$",
       "The finite region $R$, shown shaded in Figure 2, is bounded by the curve, the line with equation $x=2$, the "
       "$x$-axis and the line with equation $x=4$"]
Q11T = ["The table below shows corresponding values of $x$ and $y$, with the values of $y$ given to 4 decimal places.",
        r"$$\begin{array}{|c|c|c|c|c|c|}\hline x&2&2.5&3&3.5&4\\\hline y&0.4805&0.8396&1.2069&1.5694&1.9218\\"
        r"\hline\end{array}$$"]
Q12 = [r"[Figure 3: the trajectory of the ball, $H$ against $x$: a curve starting at height 3 on the $H$-axis, rising to "
       r"a maximum and coming down to meet the $x$-axis.]",
       "Figure 3 is a graph of the trajectory of a golf ball after the ball has been hit until it first hits the ground.",
       "The vertical height, $H$ metres, of the ball above the ground has been plotted against the horizontal distance "
       "travelled, $x$ metres, measured from where the ball was hit.",
       "The ball is modelled as a particle travelling in a vertical plane above horizontal ground.",
       "Given that the ball",
       "• is hit from a point on the top of a platform of vertical height 3 m above the ground",
       "• reaches its maximum vertical height after travelling a horizontal distance of 90 m",
       "• is at a vertical height of 27 m above the ground after travelling a horizontal distance of 120 m",
       r"Given also that $H$ is modelled as a $\textbf{quadratic}$ function in $x$"]
Q12A = "find $H$ in terms of $x$"

LATEX = {
    "01": L(r"$$\mathrm{f}(x)=ax^3+10x^2-3ax-4$$",
            r"Given that $(x-1)$ is a factor of $\mathrm{f}(x)$, find the value of the constant $a$.",
            "You must make your method clear."),
    "02a": L(*Q2, Q2A),
    "02b": L(*Q2, "(a) " + Q2A, r"The curve with equation $y=\mathrm{f}(x)$", "• meets the $y$-axis at the point $P$",
             "• has a minimum turning point at the point $Q$", "(b) Write down", "(i) the coordinates of $P$",
             "(ii) the coordinates of $Q$"),
    "03a": L(*Q3, *Q3A),
    "03b": L(*Q3, "(a) " + Q3A[0], Q3A[1], "(b) " + Q3B),
    "03c": L(*Q3, "(a) " + Q3A[0], Q3A[1], "(b) " + Q3B, "(c) Find the value of $u_3$"),
    "04a": L(*Q4, *Q4A),
    "04b": L(*Q4, *Q4M, "Starting with $x_1=0.3$", "calculate, giving each answer to 4 decimal places,",
             "(i) the value of $x_2$", "(ii) the value of $x_4$"),
    "04c": L(*Q4, "(a) " + Q4A[0], Q4A[1], *Q4M,
             "Using a suitable interval and a suitable function that should be stated,",
             r"(c) show that $\alpha$ is 0.341 to 3 decimal places."),
    "05a": L(*Q5, "show that the profit for Year 3 will be £23 328"),
    "05b": L(*Q5, "find the first year when the yearly profit will exceed £65 000"),
    "05c": L(*Q5, "find the total profit for the first 20 years of trading, giving your answer to the nearest £1000"),
    "06a": L(*Q6, Q6A),
    "06b": L(*Q6, "(a) " + Q6A, r"(b) show that $\cos ABC=\frac{9}{10}$"),
    "07a": L(*Q7, "Find", "(i) the coordinates of the centre of $C$,",
             "(ii) the exact radius of $C$, giving your answer as a simplified surd."),
    "07b": L(*Q7, "The line $l$ has equation $y=3x+k$ where $k$ is a constant.", "Given that $l$ is a tangent to $C$,",
             "find the possible values of $k$, giving your answers as simplified surds."),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, "(a) " + Q8A,
             "(b) Hence find the rate of increase in the number of bacteria in this population exactly 8 hours from the "
             "start of the study. Give your answer to 2 significant figures."),
    "08c": L(*Q8, "(a) " + Q8A,
             r"The number of bacteria, $M$, in the $\textbf{second}$ population is modelled by the equation",
             r"$$M=500\mathrm{e}^{1.4kt}\qquad t\geqslant0$$",
             "where $k$ has the value found in part (a) and $t$ is the time in hours from the start of the study.",
             "Given that $T$ hours after the start of the study, the number of bacteria in the two different populations "
             "was the same,", "(c) find the value of $T$."),
    "09a": L(*Q9, *Q9A),
    "09b": L(*Q9, *Q9A, "(b) (i) Use binomial expansions to show that, in ascending powers of $x$",
             r"$$\mathrm{f}(x)=p+qx+rx^2+\ldots$$", "where $p$, $q$ and $r$ are simplified fractions to be found.",
             "(ii) Find the range of values of $x$ for which this expansion is valid."),
    "10a": L(*SHOW, *Q10A),
    "10b": L(*SHOW, "(a) " + Q10A[0], Q10A[1], r"(b) Hence solve, for $0<x<180^\circ$",
             r"$$\frac{1-\cos4x+\sin4x}{1+\cos4x+\sin4x}=3\sin2x$$",
             "giving your answers to one decimal place where appropriate."),
    "11a": L(*Q11, *Q11T, "Use the trapezium rule, with all the values of $y$ in the table, to obtain an estimate for the "
                          "area of $R$, giving your answer to 3 significant figures."),
    "11b": L(*Q11, "Use algebraic integration to find the exact area of $R$, giving your answer in the form",
             r"$$y=a(\ln2)^2+b\ln2+c$$", "where $a$, $b$ and $c$ are integers to be found."),
    "12a": L(*Q12, Q12A),
    "12b": L(*Q12, "(a) " + Q12A, "(b) Hence find, according to the model,",
             "(i) the maximum vertical height of the ball above the ground,",
             "(ii) the horizontal distance travelled by the ball, from when it was hit to when it first hits the ground, "
             "giving your answer to the nearest metre."),
    "12c": L(*Q12, "The possible effects of wind or air resistance are two limitations of the model.",
             "Give one other limitation of this model."),
    "13": L("A curve $C$ has parametric equations",
            r"$$x=\frac{t^2+5}{t^2+1}\qquad y=\frac{4t}{t^2+1}\qquad t\in\mathbb{R}$$",
            "Show that all points on $C$ satisfy", "$$(x-3)^2+y^2=4$$"),
    "14": L("Given that", r"$$y=\frac{x-4}{2+\sqrt{x}}\qquad x>0$$", "show that",
            rf"$${DY}=\frac{{1}}{{A\sqrt{{x}}}}\qquad x>0$$", "where $A$ is a constant to be found."),
    "15i": L(r"Use proof by exhaustion to show that for $n\in\mathbb{N}$, $n\leqslant4$", "$$(n+1)^3>3^n$$"),
    "15ii": L("Given that $m^3+5$ is odd, use proof by contradiction to show, using algebra, that $m$ is even."),
}

A1M = "ALT: Alt (1) by inspection"
A2M = "ALT: Alt (2) By division"
B1T = "ALT: (b) Alt 1"
B2T = "ALT: (b) Alt 2"
B3T = "ALT: (b) Alt 3"
A12 = "ALT: Alt (a)"
DQ = r"\frac{\mathrm{d}y}{\mathrm{d}x}"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", ALG, "2.6", 3, LATEX["01"],
      [r"M1 (AO 3.1a): $\mathrm{f}(1)=a(1)^3+10(1)^2-3a(1)-4=0$. Notes: Main method seen: Attempts $\mathrm{f}(1)=0$ to set "
       r"up an equation in $a$ It is implied by $a+10-3a-4=0$ Condone a slip but attempting $\mathrm{f}(-1)=0$ is M0",
       r"M1 (AO 1.1b): $6-2a=0\Rightarrow a=\ldots$ Notes: Solves a linear equation in $a$ . Using the main method it is "
       r"dependent upon having set $\mathrm{f}(\pm1)=0$ It is implied by a solution of $\pm a\pm10\pm3a\pm4=0$. Don't be "
       r"concerned about the mechanics of the solution.",
       r"A1 (AO 1.1b): $a=3$. Notes: $a=3$ (following correct work) Answers without working scores 0 marks. The method "
       r"must be made clear. Candidates cannot guess. However if a candidate states for example, when $a=3$, "
       r"$\mathrm{f}(x)=3x^3+10x^2-9x-4$ and shows that $(x-1)$ is a factor of this $\mathrm{f}(x)$ by an allowable "
       r"method, they should be awarded M1 M1 A1 E.g. 1: $3x^3+10x^2-9x-4=(x-1)(3x^2+13x+4)$ Hence $a=3$ E.g. 2: "
       r"$\mathrm{f}(x)=3x^3+10x^2-9x-4$, $\mathrm{f}(1)=3+10-9-4=0$ Hence $a=3$ The solutions via this method must end "
       r"with the value for $a$ to score the A1",
       rf"{A1M} which may be seen in a table/grid (the mark scheme's grid has $ax^2$, $(10+a)x$, 4 along the top and "
       rf"$x$, $-1$ down the side) $ax^3+10x^2-3ax-4=(x-1)(ax^2+(10+a)x+4)$ and sets terms in $x$ equal "
       rf"$-3a=-(10+a)+4\Rightarrow2a=6\Rightarrow a=3$ — M1: This method is implied by a $\textbf{{correct}}$ equation, "
       rf"usually $-3a=-(10+a)+4$",
       rf"{A1M} — M1: Attempts to find the quadratic factor which must be of the form $ax^2+\mathrm{{g}}(a)x\pm4$ and then "
       rf"forms and solves a linear equation formed by linking the coefficients or terms in $x$",
       rf"{A2M}: $x-1$ into $ax^3+10x^2-3ax-4$ with quotient $ax^2+(\pm10\pm a)x+(10-2a)$ and remainder term "
       rf"$(-2a+10)x$ — M1: This method is implied by a $\textbf{{correct}}$ equation, usually $-10+2a=-4$",
       rf"{A2M} — M1: Attempts to divide with quotient of $ax^2+(\pm10\pm a)x+\mathrm{{h}}(a)$ and then forms and solves a "
       rf"linear equation in $a$ formed by setting the remainder $=0$."],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", ALG, "2.3", 2, LATEX["02a"],
      [r"M1 (AO 1.2): $\mathrm{f}(x)=(x-2)^2\pm\ldots$ Notes: Achieves $(x-2)^2\pm\ldots$ or states $a=-2$",
       r"A1 (AO 1.1b): $\mathrm{f}(x)=(x-2)^2+1$. Notes: Correct expression $(x-2)^2+1$ ISW after sight of this Condone "
       r"$a=-2$ and $b=1$. Condone $(x-2)^2+1=0$"],
      False, 4),
    e("02b", "2(b)", ALG, "2.3, 2.7", 2, LATEX["02b"],
      [r"B1 (AO 1.1b): (b)(i) $P=(0,5)$. Notes: (i) B1: Correct coordinates for $P$. Allow to be expressed $x=0$, $y=5$",
       r"B1ft (AO 1.1b): (b)(ii) $Q=(2,1)$. Notes: (ii) B1ft: Correct coordinates for $Q$. Allow to be expressed $x=2$, "
       r"$y=1$ (Score for the correct answer or follow through their part (a) so allow $(-a,b)$ where $a$ and $b$ are "
       r"numeric) Score in any order if they state $P=(0,5)$ and $Q=(2,1)$",
       r"ALT: Allow part (b) to be awarded from a sketch. — B1: First B1 from a sketch crossing the $y$-axis at 5",
       r"ALT: Allow part (b) to be awarded from a sketch. — B1: Second B1 from a sketch with minimum at $(2,1)$"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", SEQ, "4.2, 2.3", 3, LATEX["03a"],
      [r"M1 (AO 1.1b): $u_2=k-12$, $u_3=k-\frac{24}{k-12}$. Notes: Attempts to apply the sequence formula once for either "
       r"$u_2$ or $u_3$. Usually for $u_2=k-\frac{24}{2}$ o.e. but could be awarded for "
       r"$u_3=k-\frac{24}{\text{their “}u_2\text{”}}$",
       r"dM1 (AO 1.1b): $u_1+2u_2+u_3=0\Rightarrow2+2(k-12)+k-\frac{24}{k-12}=0$. Notes: Award for • attempting to apply "
       r"the sequence formula to find both $u_2$ and $u_3$ • using $2+2\text{“}u_2\text{”}+\text{“}u_3\text{”}=0\Rightarrow$ "
       r"an equation in $k$ . The $u_3$ may have been incorrectly adapted",
       r"A1* (AO 2.1): $\Rightarrow3k-22-\frac{24}{k-12}=0\Rightarrow(3k-22)(k-12)-24=0\Rightarrow3k^2-36k-22k+264-24=0"
       r"\Rightarrow3k^2-58k+240=0$*. Notes: Fully correct work leading to the printed answer. There must be • (at least) "
       r"one correct intermediate line between $2+2(k-12)+k-\frac{24}{k-12}=0$ (o.e.) and the given answer that shows how "
       r"the fractions are “removed”. E.g. $(3k-22)(k-12)-24=0$ • no errors in the algebra. The = 0 may just appear at the "
       r"answer line."],
      False, 6),
    e("03b", "3(b)", SEQ, "4.2, 2.3", 2, LATEX["03b"],
      [r"M1 (AO 1.1b): $k=6,\left(\frac{40}{3}\right)$. Notes: Attempts to solve the quadratic which is implied by sight of "
       r"$k=6$. This may be awarded for any of • $3k^2-58k+240=(ak\pm c)(bk\pm d)=0$ where $ab=3,cd=240$ followed by "
       r"$k=$ • an attempt at the correct quadratic formula (or completing the square) • a calculator solution giving at "
       r"least $k=6$",
       r"A1 (AO 2.3): $k=6$ as $k$ must be an integer. Notes: Chooses $k=6$ and gives a minimal reason Examples of a "
       r"minimal reason are • 6 because it is an integer • 6 because it is a whole number • 6 because $\frac{40}{3}$ or "
       r"$13.\dot{3}$ is not an integer"],
      False, 6),
    e("03c", "3(c)", SEQ, "4.2", 1, LATEX["03c"],
      [r"B1 (AO 2.2a): $(u_3=)10$. Notes: Deduces the correct value of $u_3$."],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", DIFF, "7.4, 7.3", 4, LATEX["04a"],
      [r"M1 (AO 1.1b): $\mathrm{f}'(x)=2x+\frac{4x-4}{2x^2-4x+5}$. Notes: Differentiates $\ln(2x^2-4x+5)$ to obtain "
       r"$\frac{\mathrm{g}(x)}{2x^2-4x+5}$ where $\mathrm{g}(x)$ could be 1",
       r"A1 (AO 1.1b): $\mathrm{f}'(x)=2x+\frac{4x-4}{2x^2-4x+5}$. Notes: For $\mathrm{f}'(x)=2x+\frac{4x-4}{2x^2-4x+5}$",
       r"dM1 (AO 1.1b): $2x+\frac{4x-4}{2x^2-4x+5}=0\Rightarrow2x(2x^2-4x+5)+4x-4=0$. Notes: Sets their "
       r"$\mathrm{f}'(x)=ax+\frac{\mathrm{g}(x)}{2x^2-4x+5}=0$ and uses “correct” algebra, condoning slips, to obtain a "
       r"cubic equation. E.g Look for $ax(2x^2-4x+5)\pm\mathrm{g}(x)=0$ o.e. , condoning slips, followed by some attempt "
       r"to simplify",
       r"A1* (AO 2.1): $2x^3-4x^2+7x-2=0$*. Notes: Achieves $2x^3-4x^2+7x-2=0$ with no errors. (The dM1 mark must have "
       r"been awarded)"],
      False, 8),
    e("04b", "4(b)", NUM, "9.3", 3, LATEX["04b"],
      [r"M1 (AO 1.1b): (i) $x_2=\frac{1}{7}\left(2+4(0.3)^2-2(0.3)^3\right)$. Notes: Attempts to use the iterative formula "
       r"with $x_1=0.3$. If no method is shown award for $x_2=$ awrt 0.33",
       r"A1 (AO 1.1b): $x_2=0.3294$. Notes: $x_2=$ awrt 0.3294 Note that $\frac{1153}{3500}$ is correct Condone an "
       r"incorrect suffix if it is clear that a correct value has been found",
       r"A1 (AO 1.1b): (ii) $x_4=0.3398$. Notes: $x_4=$ awrt 0.3398 Condone an incorrect suffix if it is clear that a "
       r"correct value has been found"],
      False, 8),
    e("04c", "4(c)", NUM, "9.1", 2, LATEX["04c"],
      [r"M1 (AO 3.1a): $\mathrm{h}(x)=2x^3-4x^2+7x-2$ $\mathrm{h}(0.3415)=0.00366\ldots$ $\mathrm{h}(0.3405)=-0.00130\ldots$ "
       r"Notes: Attempts to substitute $x=0.3415$ and $x=0.3405$ into a suitable function and gets one value correct "
       r"(rounded or truncated to 1 sf). It is allowable to use a tighter interval that contains the root 0.340762654 "
       r"Examples of suitable functions are $2x^3-4x^2+7x-2$, $x-\frac{1}{7}(4x^2-2x^3+2)$ and $\mathrm{f}'(x)$ as this has "
       r"been found in part (a) with $\mathrm{f}'(0.3405)=-0.00067\ldots$, $\mathrm{f}'(0.3415)=(+)0.0018$ There must be "
       r"sufficient evidence for the function, which would be for example, a statement such as "
       r"$\mathrm{h}(x)=2x^3-4x^2+7x-2$ or sight of embedded values that imply the function, not just a value or values "
       r"even if both are correct. Condone $\mathrm{h}(x)$ being mislabelled as f "
       r"$\mathrm{h}(0.3415)=2\times0.3415^3-4\times0.3415^2+7\times0.3415-2$",
       r"A1 (AO 2.4): States: • there is a change of sign • $\mathrm{f}'(x)$ is continuous • $\alpha=0.341$ to 3dp. Notes: "
       r"Requires • both calculations correct (rounded or truncated to 1sf) • a statement that there is a change in sign "
       r"and that the function is continuous • a minimal conclusion e.g. ✓, proven, $\alpha=0.341$, root"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", SEQ, "4.6, 4.5", 1, LATEX["05a"],
      [r"B1* (AO 1.1b): $u_3=£20000\times1.08^2=(£)23328$*. Notes: Uses a correct method to show that the Profit in Year 3 "
       r"will be £23 328. Condone missing units E.g. $£20000\times1.08^2$ or $£20000\times108\%\times108\%$ This may be "
       r"obtained in two steps. E.g $\frac{8}{100}\times20000=1600$ followed by $\frac{8}{100}\times21600=1728$ with the "
       r"calculations $21600+1728=23328$ seen. Condone calculations seen as 8% of 20000 = 1600. This is a show that "
       r"question and the method must be seen. It is not enough to state Year 1 = £21 600, Year 2 = £ 23 328"],
      False, 12),
    e("05b", "5(b)", SEQ, "4.5, 4.6, 6.5", 3, LATEX["05b"],
      [r"M1 (AO 1.1b): $20\,000\times1.08^{n-1}>65\,000$. Notes: Sets up an inequality or an equation that will allow the "
       r"problem to be solved. Allow for example $N$ or $n$ for $n-1$. So award for $20\,000\times1.08^{n-1}>65\,000$, "
       r"$20\,000\times1.08^n=65\,000$ or $20\,000\times(108\%)^n\geqslant65\,000$ amongst others. Condone slips on the "
       r"20 000 and 65 000 but the 1.08 o.e. must be correct",
       r"M1 (AO 3.1b): $1.08^{n-1}>\frac{13}{4}\Rightarrow n-1>\frac{\ln(3.25)}{\ln(1.08)}$ or e.g. "
       r"$1.08^{n-1}>\frac{13}{4}\Rightarrow n-1>\log_{1.08}\left(\frac{13}{4}\right)$. Notes: Uses a correct strategy "
       r"involving logs in an attempt to solve a type of equation or inequality of the form seen above. It cannot be "
       r"awarded from a sum formula The equation/inequality must contain an index of $n-1$, $N$, $n$ etc. Again condone "
       r"slips on the 20 000 and 65 000 but additionally condone an error on the 1.08, which may appear as 1.8 for example "
       r"E.g. $20\,000\times1.08^n=65\,000\Rightarrow n\log1.08=\log\frac{65000}{20000}\Rightarrow n=\ldots$ E.g. "
       r"$2000\times1.8^n=65\,000\Rightarrow\log2000+n\log1.8=\log65000\Rightarrow n=\ldots$",
       r"A1 (AO 3.2a): Year 17. Notes: Interprets their decimal value and gives the correct year number. Year 17",
       r"ALT: The demand of the question dictates that solutions relying entirely on calculator technology are not "
       r"acceptable, BUT allow a solution that appreciates a correct term formula or the entire set of calculations where "
       r"you may see the numbers as part of a larger list — M1: E.g. Uses, or implies the use of, an acceptable "
       r"calculation and finds value(s) for $(n=16)\Rightarrow P=20000\times1.08^{15}=$ awrt 63400 or "
       r"$(n=17)\Rightarrow P=20000\times1.08^{16}=$ awrt 68500",
       r"ALT: Correct term formula / list — M1: $(n=16)\Rightarrow P=20000\times1.08^{15}=$ awrt 63400 and "
       r"$(n=17)\Rightarrow P=20000\times1.08^{16}=$ awrt 68500",
       r"ALT: Correct term formula / list — A1: 17 years following correct method and both M's"],
      False, 12),
    e("05c", "5(c)", SEQ, "4.5, 4.6", 2, LATEX["05c"],
      [r"M1 (AO 3.4): $S_{20}=\frac{20000(1-1.08^{20})}{1-1.08}$. Notes: Attempts to use the model with a correct sum "
       r"formula to find the total profit for the 20 years. You may see an attempt to find the sum of 20 terms via a list. "
       r"This is acceptable provided there are 20 terms with $u_n=1.08\times u_{n-1}$ seen at least 4 times and the sum "
       r"attempted. Condone a slip on the 20 000 (e.g appearing as 2 000) and/or a slip on the 1.08 with it being the "
       r"same “$r$” as in (b) . Do not condone 20 appearing as 19 for instance",
       r"A1 (AO 1.1b): Awrt (£) 915 000. Notes: awrt £915 000 but condone missing unit The demand of the question dictates "
       r"that all stages of working should be seen. An answer without working scores M0 A0"],
      False, 12),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", VEC, "10.3", 2, LATEX["06a"],
      [rf"M1 (AO 1.1b): $\overrightarrow{{AC}}=\overrightarrow{{AB}}+\overrightarrow{{BC}}=-3{I}-4{J}-5{K}+{I}+{J}+4{K}="
       rf"\ldots$ Notes: Attempts $\overrightarrow{{AC}}=\overrightarrow{{AB}}+\overrightarrow{{BC}}$ There must be attempt "
       rf"to add not subtract. If no method shown it may be implied by two correct components",
       rf"A1 (AO 1.1b): $=-2{I}-3{J}-{K}$. Notes: Correct vector. Allow $-2{I}-3{J}-{K}$ and "
       rf"$\begin{{pmatrix}}-2\\-3\\-1\end{{pmatrix}}$ but not $\begin{{pmatrix}}-2{I}\\-3{J}\\-1{K}\end{{pmatrix}}$"],
      True, 14),
    e("06b", "6(b)", VEC, "10.2, 5.1", 3, LATEX["06b"],
      [r"M1 (AO 1.1b): At least 2 of $(AC^2)=\text{“}2^2+3^2+1^2\text{”}$, $(AB^2)=3^2+4^2+5^2$, $(BC^2)=1^2+1^2+4^2$. "
       r"Notes: Attempts to “square and add” for at least 2 of the 3 sides. Follow through on their $\overrightarrow{AC}$ "
       r"Look for an attempt at either $a^2+b^2+c^2$ or $\sqrt{a^2+b^2+c^2}$",
       r"M1 (AO 3.1a): $2^2+3^2+1^2=3^2+4^2+5^2+1^2+1^2+4^2-2\sqrt{3^2+4^2+5^2}\sqrt{1^2+1^2+4^2}\cos ABC$. Notes: A correct "
       r"attempt to apply a correct cosine rule to the given problem; Condone slips on the lengths of the sides but the "
       r"sides must be in the correct position to find angle $ABC$",
       r"A1* (AO 2.1): $14=50+18-2\sqrt{50}\sqrt{18}\cos ABC\Rightarrow\cos ABC=\frac{50+18-14}{2\sqrt{50}\sqrt{18}}="
       r"\frac{9}{10}$*. Notes: Correct completion with sufficient intermediate work to establish the printed result. "
       r"Condone different labelling, e.g. $ABC\leftrightarrow\theta$ as long as it is clear what is meant It is OK to "
       r"move from a correct cosine rule $14=50+18-2\sqrt{50}\sqrt{18}\cos ABC$ via "
       r"$\cos ABC=\frac{54}{2\sqrt{50}\sqrt{18}}$ o.e. such as $\cos ABC=\frac{(5\sqrt{2})^2+(3\sqrt{2})^2-(\sqrt{14})^2}"
       r"{2\times5\sqrt{2}\times3\sqrt{2}}$ to $\cos ABC=\frac{9}{10}$",
       r"ALT: (b) Alternative — M1 (AO 1.1b): $AB^2=3^2+4^2+5^2$, $BC^2=1^2+1^2+4^2$. Notes: Correct application of "
       r"Pythagoras for sides $AB$ and $BC$ or their squares",
       rf"ALT: (b) Alternative — M1 (AO 3.1a): $\overrightarrow{{BA}}.\overrightarrow{{BC}}=(3{I}+4{J}+5{K}).({I}+{J}+4{K})="
       rf"27=\sqrt{{3^2+4^2+5^2}}\sqrt{{1^2+1^2+4^2}}\cos ABC$. Notes: Recognises the requirement for and applies the "
       rf"scalar product",
       r"ALT: (b) Alternative — A1* (AO 2.1): $27=\sqrt{50}\sqrt{18}\cos ABC\Rightarrow\cos ABC=\frac{27}{\sqrt{50}"
       r"\sqrt{18}}=\frac{9}{10}$*. Notes: Correct completion with sufficient intermediate work to establish the printed "
       r"result"],
      True, 14),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", COORD, "3.2", 4, LATEX["07a"],
      [r"M1 (AO 1.1b): (i) $(x-5)^2+(y+2)^2=\ldots$ Notes: Attempts to complete the square on by halving both $x$ and $y$ "
       r"terms. Award for sight of $(x\pm5)^2,(y\pm2)^2=\ldots$ This mark can be implied by a centre of $(\pm5,\pm2)$.",
       r"A1 (AO 1.1b): $(5,-2)$. Notes: Correct coordinates. (Allow $x=5$, $y=-2$)",
       r"M1 (AO 1.1b): (ii) $r=\sqrt{\text{“}5\text{”}^2+\text{“}2\text{”}^2-11}$. Notes: Correct strategy for the radius or "
       r"radius$^2$ . For example award for $r=\sqrt{\text{“}\pm5\text{”}^2+\text{“}\pm2\text{”}^2-11}$ or an attempt such as "
       r"$(x-a)^2-a^2+(y-b)^2-b^2+11=0\Rightarrow(x-a)^2+(y-b)^2=k\Rightarrow r^2=k$",
       r"A1 (AO 1.1b): $r=3\sqrt{2}$. Notes: $r=3\sqrt{2}$ . Do not accept for the A1 either $r=\pm3\sqrt{2}$ or $\sqrt{18}$ "
       r"The A1 can be awarded following sign slips on $(5,-2)$ so following "
       r"$r^2=\text{“}\pm5\text{”}^2+\text{“}\pm2\text{”}^2-11$"],
      False, 18),
    e("07b", "7(b)", COORD, "3.2, 2.3", 5, LATEX["07b"],
      [r"M1 (AO 2.1): $y=3x+k\Rightarrow x^2+(3x+k)^2-10x+4(3x+k)+11=0\Rightarrow x^2+9x^2+6kx+k^2-10x+12x+4k+11=0$. "
       r"Notes: (b) Main method seen M1: Substitutes $y=3x+k$ into the given equation (or their factorised version) and "
       r"makes progress by attempting to expand the brackets. Condone lack of = 0",
       r"A1 (AO 1.1b): $\Rightarrow10x^2+(6k+2)x+k^2+4k+11=0$. Notes: Correct 3 term quadratic equation. The terms must be "
       r"collected but this can be implied by correct $a$, $b$ and $c$",
       r"M1 (AO 3.1a): $b^2-4ac=0\Rightarrow(6k+2)^2-4\times10\times(k^2+4k+11)=0$. Notes: Recognises the requirement to "
       r"use $b^2-4ac=0$ (or equivalent) where both $b$ and $c$ are expressions in $k$ . It is dependent upon having "
       r"attempted to substitute $y=3x+k$ into the given equation",
       r"M1 (AO 1.1b): $\Rightarrow4k^2+136k+436=0\Rightarrow k=\ldots$ Notes: Solves 3TQ in $k$. See General Principles. "
       r"The 3TQ in $k$ must have been found as a result of attempt at $b^2-4ac\ldots0$",
       r"A1 (AO 2.2a): $k=-17\pm6\sqrt{5}$. Notes: Correct simplified values Look carefully at the method used. It is "
       r"possible to attempt this using gradients",
       rf"{B1T} — M1 (AO 2.1): $x^2+y^2-10x+4y+11=0\Rightarrow2x+2y{DQ}-10+4{DQ}=0$. Notes: Differentiates implicitly "
       rf"condoning slips but must have two ${DQ}$’s coming from correct terms",
       rf"{B1T} — A1 (AO 1.1b): Correct differentiation.",
       rf"{B1T} — M1 (AO 3.1a): Sets ${DQ}=3\Rightarrow x+3y+1=0$ and combines with equation for $C$ "
       rf"$\Rightarrow5x^2-50x+44=0$ or $5y^2+20y+11=0\Rightarrow x=\ldots$ or $y=\ldots$ Notes: Sets ${DQ}=3$, makes $y$ "
       rf"or $x$ the subject, substitutes back into $C$ and attempts to solve the resulting quadratic in $x$ or $y$.",
       rf"{B1T} — M1 (AO 1.1b): $x=\frac{{25\pm9\sqrt{{5}}}}{{5}}$, $y=\frac{{-10\pm3\sqrt{{5}}}}{{5}}$, "
       rf"$k=y-3x\Rightarrow k=\ldots$ Notes: Uses at least one pair of coordinates and $l$ to find at least one value for "
       rf"$k$. It is dependent upon having attempted both M's",
       rf"{B1T} — A1 (AO 2.2a): $k=-17\pm6\sqrt{{5}}$. Notes: Correct simplified values",
       rf"{B2T} — M1 A1 (AO 2.1, 1.1b): $x^2+y^2-10x+4y+11=0\Rightarrow2x+2y{DQ}-10+4{DQ}=0$. Notes: Very similar except "
       rf"it uses equation for $l$ instead of $C$ in mark 3 M1 A1: Correct differentiation (See alt 1)",
       rf"{B2T} — M1 (AO 3.1a): Sets ${DQ}=3\Rightarrow x+3y+1=0$ and combines with equation for $l$ $y=3x+k,x+3y=1$ "
       rf"$\Rightarrow x=\ldots$ and $y=\ldots$ in terms of $k$. Notes: Sets ${DQ}=3$, makes $y$ or $x$ the subject, "
       rf"substitutes back into $l$ to obtain $x$ and $y$ in terms of $k$",
       rf"{B2T} — M1 (AO 1.1b): $x=\frac{{-3k-1}}{{10}}$, $y=\frac{{k-3}}{{10}}$, $x^2+y^2-10x+4y+11=0\Rightarrow k=\ldots$ "
       rf"Notes: Substitutes for $x$ and $y$ into $C$ and solves resulting 3TQ in $k$",
       rf"{B2T} — A1 (AO 2.2a): $k=-17\pm6\sqrt{{5}}$. Notes: Correct simplified values",
       rf"{B3T} — M1: $y=3x+k\Rightarrow m=3\Rightarrow m_r=-\frac{{1}}{{3}}$. Notes: Applies negative reciprocal rule to "
       rf"obtain gradient of radius",
       rf"{B3T} — A1: $y+2=-\frac{{1}}{{3}}(x-5)$. Notes: Correct equation of radial line passing through the centre of $C$",
       rf"{B3T} — M1: $(x-5)^2+(y+2)^2=18$, $y+2=-\frac{{1}}{{3}}(x-5)\Rightarrow\frac{{10}}{{9}}(x-5)^2=18\Rightarrow "
       rf"x=\ldots$ or $\Rightarrow10(y+2)^2=18\Rightarrow y=\ldots$ Notes: Solves simultaneously to find $x$ or $y$ "
       rf"Alternatively solves “$y=-\frac{{1}}{{3}}x-\frac{{1}}{{3}}$” and $y=3x+k$ to get $x$ in terms of $k$ which they "
       rf"substitute in $x^2+(3x+k)^2-10x+4(3x+k)+11=0$ to form an equation in $k$.",
       rf"{B3T} — M1: $x=\frac{{25\pm9\sqrt{{5}}}}{{5}}$, $y=\frac{{-10\pm3\sqrt{{5}}}}{{5}}$, $k=y-3x\Rightarrow k=\ldots$ "
       rf"Notes: Applies $k=y-3x$ with at least one pair of values to find $k$",
       rf"{B3T} — A1: $k=-17\pm6\sqrt{{5}}$. Notes: Correct simplified values"],
      False, 18),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", EXP, "6.7, 6.5", 4, LATEX["08a"],
      [r"B1 (AO 3.4): $A=1000$. Notes: Mark as one complete question. Marks in (a) can be awarded from (b) Correct value of "
       r"$A$ for the model. Award if equation for model is of the form $N=1000\mathrm{e}^{-t}$",
       r"M1 (AO 1.1b): $2000=1000\mathrm{e}^{5k}$ or $\mathrm{e}^{5k}=2$. Notes: Uses the model to set up a correct equation "
       r"in $k$. Award for substituting $N=2000,t=5$ following through on their value for $A$.",
       r"M1 (AO 2.1): $\mathrm{e}^{5k}=2\Rightarrow5k=\ln2\Rightarrow k=\ldots$ Notes: Uses correct ln work to solve an "
       r"equation of the form $a\mathrm{e}^{5k}=b$ and obtain a value for $k$",
       r"A1 (AO 3.3): $N=1000\mathrm{e}^{\left(\frac{1}{5}\ln2\right)t}$ or $N=1000\mathrm{e}^{0.139t}$. Notes: Correct "
       r"equation of model. Condone an ambiguous $N=1000\mathrm{e}^{\frac{1}{5}\ln2t}$ unless followed by something "
       r"incorrect. Watch for $N=1000\times2^{\frac{t}{5}}$ which is also correct"],
      False, 22),
    e("08b", "8(b)", EXP, "6.2, 6.7", 2, LATEX["08b"],
      [r"M1 (AO 3.1b): $\frac{\mathrm{d}N}{\mathrm{d}t}=1000\times\left(\frac{1}{5}\ln2\right)\mathrm{e}^{\left(\frac{1}{5}"
       r"\ln2\right)t}$ or $\frac{\mathrm{d}N}{\mathrm{d}t}=1000\times0.139\mathrm{e}^{0.139t}$ "
       r"$\left(\frac{\mathrm{d}N}{\mathrm{d}t}\right)_{t=8}=1000\times\left(\frac{1}{5}\ln2\right)\mathrm{e}^{8\times"
       r"\frac{1}{5}\ln2}$ or $\left(\frac{\mathrm{d}N}{\mathrm{d}t}\right)_{t=8}=1000\times0.139\mathrm{e}^{0.139\times8}$. "
       r"Notes: Differentiates $\alpha\mathrm{e}^{kt}$ to $\beta\mathrm{e}^{kt}$ and substitutes $t=8$ (Condone "
       r"$\alpha=\beta$ so long as you can see an attempt to differentiate)",
       r"A1 (AO 1.1b): $=$ awrt 420. Notes: For awrt 420 (2sf). Answers to (b) and (c) appearing without working (i.e. "
       r"from a calculator). It is important that candidates show sufficient working to make their methods clear. (b) If "
       r"candidate has for example $N=1000\mathrm{e}^{0.139t}$, and then writes at $t=8$ $\frac{\mathrm{d}N}{\mathrm{d}t}=$ "
       r"awrt 420 award both marks. Just the answer from a correct model equation score SC 1,0."],
      False, 22),
    e("08c", "8(c)", EXP, "6.7, 6.4", 3, LATEX["08c"],
      [r"M1 (AO 3.4): $500\mathrm{e}^{1.4\times\left(\frac{1}{5}\ln2\right)T}=1000\mathrm{e}^{\left(\frac{1}{5}\ln2\right)T}$ "
       r"or $500\mathrm{e}^{1.4\times\text{“}0.139\text{”}t}=1000\mathrm{e}^{\text{“}0.139\text{”}t}$. Notes: Uses both "
       r"models to set up an equation in $T$ using their value for $k$, but also allow in terms of $k$",
       r"M1 (AO 2.1): Correct method of getting a linear equation in $T$ E.g. $0.08T\ln2=\ln2$ or "
       r"$1.4\times\text{“}0.139\text{”}T=\ln2+\text{“}0.139\text{”}t$. Notes: Uses correct processing using lns to obtain a "
       r"linear equation in $T$ (or $t$)",
       r"A1 (AO 1.1b): $T=12.5$ hours. Notes: Awrt 12.5 (c) The first M1 should be seen E.g "
       r"$500\mathrm{e}^{1.4\times\text{“}0.139\text{”}t}=1000\mathrm{e}^{\text{“}0.139\text{”}t}$ If the answer $T=12.5$ "
       r"appears without any further working score SC M1 M1 A0"],
      False, 22),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", ALG, "2.10", 4, LATEX["09a"],
      [r"M1 (AO 1.1b): (a)(i) $50x^2+38x+9\equiv A(5x+2)(1-2x)+B(1-2x)+C(5x+2)^2\Rightarrow B=\ldots$ or $C=\ldots$ Notes: "
       r"Uses a correct identity and makes progress using an appropriate strategy (e.g. sub $x=\frac{1}{2}$ ) to find a "
       r"value for $B$ or $C$. May be implied by one correct value (cover up rule).",
       r"A1 (AO 1.1b): $B=1$ and $C=2$. Notes: Both values correct",
       r"M1 (AO 2.1): (a)(ii) E.g. $x=0$ $x=0\Rightarrow9=2A+B+4C\Rightarrow9=2A+1+8\Rightarrow A=\ldots$ Notes: Uses an "
       r"appropriate method to establish an equation connecting $A$ with $B$ and/or $C$ and uses their values of $B$ "
       r"and/or $C$ to find a suitable equation in $A$. Amongst many different methods are: Compare terms in "
       r"$x^2\Rightarrow50=-10A+25C$ which would be implied by $50=-10A+25\times\text{“}2\text{”}$ Compare constant terms or "
       r"substitute $x=0\Rightarrow9=2A+B+4C$ implied by $9=2A+1+4\times2$",
       r"A1* (AO 1.1b): $A=0$*. Notes: Fully correct proof with no errors. Note: The second part is a proof so it is "
       r"important that a suitable proof/show that is seen. Candidates who write down 3 equations followed by three "
       r"answers (with no working) will score M1 A1 M0 A0"],
      False, 26),
    e("09b", "9(b)", SEQ, "4.1, 2.10", 7, LATEX["09b"],
      [r"M1 (AO 3.1a): (b)(i) $\frac{1}{(5x+2)^2}=(5x+2)^{-2}=2^{-2}\left(1+\frac{5}{2}x\right)^{-2}$ or "
       r"$(5x+2)^{-2}=2^{-2}+\ldots$ Notes: Applies the key steps of writing $\frac{1}{(5x+2)^2}$ as $(5x+2)^{-2}$ and takes "
       r"out a factor of $2^{-2}$ to form an expression of the form $(5x+2)^{-2}=2^{-2}(1+*x)^{-2}$ where * is not 1 or 5 "
       r"Alternatively uses direct expansion to obtain $2^{-2}+\ldots$",
       r"M1 (AO 1.1b): $\left(1+\frac{5}{2}x\right)^{-2}=1-2\left(\frac{5}{2}x\right)+\frac{-2(-2-1)}{2!}"
       r"\left(\frac{5}{2}x\right)^2+\ldots$ Notes: Correct attempt at the binomial expansion of $(1+*x)^{-2}$ up to the "
       r"term in $x^2$ Look for $1+(-2)*x+\frac{(-2)(-3)}{2}*x^2$ where * is not 5 or 1. Condone sign slips and lack of "
       r"$*^2$ on term 3. .... Alt Look for correct structure for 2nd and 3rd terms by direct expansion. See below",
       r"A1 (AO 1.1b): $2^{-2}\left(1+\frac{5}{2}x\right)^{-2}=\frac{1}{4}-\frac{5}{4}x+\frac{75}{16}x^2+\ldots$ Notes: For "
       r"a fully correct expansion of $(2+5x)^{-2}$ which may be unsimplified. This may have been combined with their "
       r"‘$B$’ A direct expansion would look like $(2+5x)^{-2}=2^{-2}+(-2)2^{-3}\times5x+\frac{(-2)(-3)}{2}2^{-4}\times"
       r"(5x)^2$",
       r"M1 (AO 1.1b): $\frac{1}{(1-2x)}=(1-2x)^{-1}=1+2x+\frac{-1(-1-1)}{2!}(2x)^2+.$ Notes: Correct attempt at the "
       r"binomial expansion of $(1-2x)^{-1}$ Look for $1+(-1)*x+\frac{(-1)(-2)}{2}*x^2$ where * is not 1",
       r"dM1 (AO 2.1): $\frac{1}{(5x+2)^2}+\frac{2}{1-2x}=\frac{1}{4}-\frac{5}{4}x+\frac{75}{16}x^2+\ldots+2+4x+8x^2+\ldots$ "
       r"Notes: Fully correct strategy that is dependent on the previous TWO method marks. There must be some attempt to "
       r"use their values of $B$ and $C$",
       r"A1 (AO 1.1b): $=\frac{9}{4}+\frac{11}{4}x+\frac{203}{16}x^2+\ldots$ Notes: Correct expression or correct values for "
       r"$p$, $q$ and $r$.",
       r"B1 (AO 2.2a): (b)(ii) $|x|<\frac{2}{5}$. Notes: Correct range. Allow also other forms, for example "
       r"$-\frac{2}{5}<x<\frac{2}{5}$ or $x\in\left(-\frac{2}{5},\frac{2}{5}\right)$ Do not allow multiple answers here. "
       r"The correct answer must be chosen if two answers are offered"],
      False, 26),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", TRIG, "5.8, 5.6", 4, LATEX["10a"],
      [r"M1 (AO 2.1): $\frac{1-\cos2\theta+\sin2\theta}{1+\cos2\theta+\sin2\theta}=\frac{1-(1-2\sin^2\theta)+2\sin\theta"
       r"\cos\theta}{1+\cos2\theta+\sin2\theta}$ or $\frac{1-\cos2\theta+\sin2\theta}{1+\cos2\theta+\sin2\theta}="
       r"\frac{1-\cos2\theta+\sin2\theta}{1+(2\cos^2\theta-1)+2\sin\theta\cos\theta}$. Notes: Attempts to use a correct "
       r"double angle formulae for both $\sin2\theta$ and $\cos2\theta$ (seen once). The application of the formula for "
       r"$\cos2\theta$ must be the one that cancels out the “1” So look for $\cos2\theta=1-2\sin^2\theta$ in the numerator "
       r"or $\cos2\theta=2\cos^2\theta-1$ in the denominator Note that $\cos2\theta=\cos^2\theta-\sin^2\theta$ may be used "
       r"as well as using $\cos^2\theta+\sin^2\theta=1$",
       r"A1 (AO 1.1b): $\frac{1-\cos2\theta+\sin2\theta}{1+\cos2\theta+\sin2\theta}=\frac{1-(1-2\sin^2\theta)+2\sin\theta"
       r"\cos\theta}{1+(2\cos^2\theta-1)+2\sin\theta\cos\theta}$. Notes: A1: "
       r"$\frac{1-(1-2\sin^2\theta)+2\sin\theta\cos\theta}{1+(2\cos^2\theta-1)+2\sin\theta\cos\theta}$ or "
       r"$\frac{2\sin^2\theta+2\sin\theta\cos\theta}{2\cos^2\theta+2\sin\theta\cos\theta}$",
       r"dM1 (AO 2.1): $=\frac{2\sin^2\theta+2\sin\theta\cos\theta}{2\cos^2\theta+2\sin\theta\cos\theta}="
       r"\frac{2\sin\theta(\sin\theta+\cos\theta)}{2\cos\theta(\cos\theta+\sin\theta)}$. Notes: Factorises numerator and "
       r"denominator in order to demonstrate cancelling of $(\sin\theta+\cos\theta)$",
       r"A1* (AO 1.1b): $=\frac{\sin\theta}{\cos\theta}=\tan\theta$*. Notes: Fully correct proof with no errors. You must "
       r"see an intermediate line of $\frac{2\sin\theta(\sin\theta+\cos\theta)}{2\cos\theta(\cos\theta+\sin\theta)}$ [with "
       r"the brackets struck through] or $\frac{\sin\theta}{\cos\theta}$ or even $\frac{2\sin\theta}{2\cos\theta}$ Withhold "
       r"this mark if you see, within the body of the proof, • notational errors. E.g. $\cos2\theta=1-2\sin^2$ or "
       r"$\cos\theta^2$ for $\cos^2\theta$ • mixed variables. E.g. $\cos2\theta=2\cos^2x-1$"],
      False, 30),
    e("10b", "10(b)", TRIG, "5.7, 5.6", 4, LATEX["10b"],
      [r"M1 (AO 3.1a): $\frac{1-\cos4x+\sin4x}{1+\cos4x+\sin4x}=3\sin2x\Rightarrow\tan2x=3\sin2x$ o.e. Notes: Makes the "
       r"connection with part (a) and writes the lhs as $\tan2x$ . Condone $x\leftrightarrow\theta$ $\tan2\theta=3\sin2\theta$",
       r"A1 (AO 1.1b): $\Rightarrow\sin2x-3\sin2x\cos2x=0\Rightarrow\sin2x(1-3\cos2x)=0\Rightarrow(\sin2x=0,)\cos2x="
       r"\frac{1}{3}$. Notes: Obtains $\cos2x=\frac{1}{3}$ o.e. with $x\leftrightarrow\theta$. You may see "
       r"$\sin^2x=\frac{1}{3}$ or $\cos^2x=\frac{2}{3}$ after use of double angle formulae.",
       r"A1 (AO 1.1b): $x=90^\circ$, awrt $35.3^\circ$, awrt $144.7^\circ$. Notes: Two “correct” values. Condone accuracy of "
       r"awrt $90^\circ$, $35^\circ$, $145^\circ$ Also condone radian values here. Look for 2 of awrt 0.62, 1.57, 2.53",
       r"A1 (AO 2.1): $x=90^\circ$, awrt $35.3^\circ$, awrt $144.7^\circ$. Notes: All correct (allow awrt) and no other "
       r"values in range. Condone $x\leftrightarrow\theta$ if used consistently Answers without working in (b): Just "
       r"answers and no working score 0 marks. If the first line is written out, i.e. $\tan2x=3\sin2x$ followed by all "
       r"three correct answers score 1100 ."],
      False, 30),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", NUM, "9.4", 3, LATEX["11a"],
      [r"B1 (AO 1.1b): $h=0.5$. Notes: Correct strip width. May be implied by $\frac{1}{2}\times\frac{1}{2}\{\ldots\}$ or "
       r"$\frac{1}{4}\times\{\ldots\}$",
       r"M1 (AO 1.1b): $A\approx\frac{1}{2}\times\frac{1}{2}\{0.4805+1.9218+2(0.8396+1.2069+1.5694)\}$. Notes: Correct "
       r"application of the trapezium rule. Look for $\frac{1}{2}\times\text{“}h\text{”}\{0.4805+1.9218+2(0.8396+1.2069+"
       r"1.5694)\}$ condoning slips in the digits. The bracketing must be correct but it is implied by awrt 2.41",
       r"A1 (AO 1.1b): $=2.41$. Notes: 2.41 only. This is not awrt"],
      True, 34),
    e("11b", "11(b)", INT, "8.5, 8.3, 6.4", 5, LATEX["11b"],
      [rf"M1 (AO 3.1a): $\int(\ln x)^2{DX}=x(\ln x)^2-\int x\times\frac{{2\ln x}}{{x}}{DX}$. Notes: Attempts parts the "
       rf"correct way round to achieve $\alpha x(\ln x)^2-\beta\int\ln x{DX}$ o.e. May be unsimplified (see scheme). Watch "
       rf"for candidates who know or learn $\int\ln x{DX}=x\ln x-x$ who may write $\int(\ln x)^2{DX}=\int(\ln x)(\ln x){DX}="
       rf"\ln x(x\ln x-x)-\int\frac{{x\ln x-x}}{{x}}{DX}$",
       rf"A1 (AO 1.1b): $\int(\ln x)^2{DX}=x(\ln x)^2-\int x\times\frac{{2\ln x}}{{x}}{DX}$. Notes: Correct expression which "
       rf"may be unsimplified",
       rf"dM1 (AO 2.1): $=x(\ln x)^2-2\int\ln x{DX}=x(\ln x)^2-2\left(x\ln x-\int\mathrm{{d}}x\right)=x(\ln x)^2-2x\ln x+2x$. "
       rf"Notes: Attempts parts again to (only condone coefficient errors) to achieve $\alpha x(\ln x)^2-\beta x\ln x\pm"
       rf"\gamma x$ o.e.",
       rf"ddM1 (AO 2.1): $\int_2^4(\ln x)^2{DX}=\left[x(\ln x)^2-2x\ln x+2x\right]_2^4=4(\ln4)^2-2\times4\ln4+2\times4-"
       rf"\left(2(\ln2)^2-2\times2\ln2+2\times2\right)=4(2\ln2)^2-16\ln2+8-2(\ln2)^2+4\ln2-4$. Notes: Applies the limits 4 "
       rf"and 2 to an expression of the form $\pm\alpha x(\ln x)^2\pm\beta x\ln x\pm\gamma x$, subtracts and applies "
       rf"$\ln4=2\ln2$ at least once. Both M's must have been awarded",
       r"A1 (AO 1.1b): $=14(\ln2)^2-12\ln2+4$. Notes: Correct answer",
       r"ALT: It is possible to do $\int(\ln x)^2\,\mathrm{d}x$ via a substitution $u=\ln x$ but it is very similar. — M1 "
       r"A1, dM1: $\int u^2\mathrm{e}^u\,\mathrm{d}u=u^2\mathrm{e}^u-\int2u\mathrm{e}^u\,\mathrm{d}u,=u^2\mathrm{e}^u-"
       r"2u\mathrm{e}^u\pm2\mathrm{e}^u$",
       r"ALT: Via substitution $u=\ln x$ — ddM1: Applies appropriate limits and uses $\ln4=2\ln2$ at least once to an "
       r"expression of the form $u^2\mathrm{e}^u-\beta u\mathrm{e}^u\pm\gamma\mathrm{e}^u$ Both M's must have been awarded"],
      True, 34),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", ALG, "2.11, 2.3, 7.3", 5, LATEX["12a"],
      [r"M1 (AO 3.3): $H=ax^2+bx+c$ and $x=0$, $H=3\Rightarrow H=ax^2+bx+3$. Notes: Translates the problem into a suitable "
       r"model and uses $H=3$ when $x=0$ to establish $c=3$ Condone with $a=\pm1$ so $H=x^2+bx+3$ will score M1 but little "
       r"else",
       r"M1 (AO 3.1b): $H=ax^2+bx+3$ and $x=120,H=27\Rightarrow27=14400a+120b+3$ or "
       r"$\frac{\mathrm{d}H}{\mathrm{d}x}=2ax+b=0$ when $x=90\Rightarrow180a+b=0$. Notes: For a correct attempt at using one "
       r"of the two other pieces of information within a quadratic model Either uses $H=27$ when $x=120$ (with $c=3$) to "
       r"produce a linear equation connecting $a$ and $b$ for the model Or differentiates and uses "
       r"$\frac{\mathrm{d}H}{\mathrm{d}x}=0$ when $x=90$. Alternatives exist here, using the symmetrical nature of the "
       r"curve, so they could use $x=-\frac{b}{2a}$ at vertex or use point (60, 27) or (180,3).",
       r"A1 (AO 1.1b): $H=ax^2+bx+3$ and $x=120,H=27\Rightarrow27=14400a+120b+3$ or "
       r"$\frac{\mathrm{d}H}{\mathrm{d}x}=2ax+b=0$ when $x=90\Rightarrow180a+b=0$. Notes: At least one correct equation "
       r"connecting $a$ and $b$. Remember “$a$” could have been set as negative so an equation such as "
       r"$27=-14400a+120b+3$ would be correct in these circumstances.",
       r"dM1 (AO 3.1b): $H=ax^2+bx+3$ and $x=120,H=27\Rightarrow27=14400a+120b+3$ and $\frac{\mathrm{d}H}{\mathrm{d}x}="
       r"2ax+b=0$ when $x=90\Rightarrow180a+b=0\Rightarrow a=\ldots,b=\ldots$ Notes: Fully correct strategy that uses "
       r"$H=ax^2+bx+3$ with the two other pieces of information in order to establish the values of both $a$ and $b$ for "
       r"the model",
       r"A1 (AO 1.1b): $H=-\frac{1}{300}x^2+\frac{3}{5}x+3$ o.e. Notes: Correct equation, not just the correct values of "
       r"$a$, $b$ and $c$. Award if seen in part (b)",
       rf"{A12} — M1 (AO 3.3): $H=a(x+b)^2+c$ and $x=90$ at $H_{{\max}}\Rightarrow H=a(x-90)^2+c$. Notes: The method using "
       rf"an alternative form of the equation can be scored in a very similar way. The first M is for the completed "
       rf"square form of the quadratic showing a maximum at $x=90$ So award M1 for $H=\pm a(x-90)^2+c$ or "
       rf"$H=\pm a(90-x)^2+c$ . Condone for this mark an equation with $a=1\Rightarrow H=(x-90)^2+c$ or "
       rf"$c=3\Rightarrow H=a(x-90)^2+3$ but will score little else",
       rf"{A12} — M1 (AO 3.1b): $H=3$ when $x=0\Rightarrow3=8100a+c$ or $H=27$ when $x=120\Rightarrow27=900a+c$",
       rf"{A12} — A1 (AO 1.1b): $H=3$ when $x=0\Rightarrow3=8100a+c$ or $H=27$ when $x=120\Rightarrow27=900a+c$",
       rf"{A12} — dM1 (AO 3.1b): $H=3$ when $x=0\Rightarrow3=8100a+c$ and $H=27$ when $x=120\Rightarrow27=900a+c$ "
       rf"$\Rightarrow a=\ldots,c=\ldots$",
       rf"{A12} — A1 (AO 1.1b): $H=-\frac{{1}}{{300}}(x-90)^2+30$ o.e Note that $H=-\frac{{1}}{{300}}(x-90)^2+30$ is "
       rf"equivalent to $H=-\frac{{1}}{{300}}(90-x)^2+30$ Other versions using symmetry are also correct so please look "
       rf"carefully at all responses E.g. Using a starting equation of $H=a(x-60)(x-120)+b$ leads to "
       rf"$H=-\frac{{1}}{{300}}(x-60)(x-120)+27$"],
      True, 38),
    e("12b", "12(b)", ALG, "2.11, 2.3", 3, LATEX["12b"],
      [r"B1 (AO 3.4): (b)(i) $x=90\Rightarrow H\left(=-\frac{1}{300}(90)^2+\frac{3}{5}(90)+3\right)=30$ m. Notes: Correct "
       r"height including the units. CAO",
       r"M1 (AO 3.4): (b)(ii) $H=0\Rightarrow-\frac{1}{300}x^2+\frac{3}{5}x+3=0\Rightarrow x=\ldots$ Notes: Uses $H=0$ and "
       r"attempts to solve for $x$. Usual rules for quadratics.",
       r"A1 (AO 3.2a): $x=(-4.868\ldots,)$ $184.868\ldots\Rightarrow x=185$ (m). Notes: Discards the negative solution (may "
       r"not be seen) and identifies awrt 185 m. Condone lack of units",
       r"ALT: Alt (b) — B1 (AO 3.4): $x=90\Rightarrow H=0^2+30=30$ m",
       r"ALT: Alt (b) — M1 (AO 3.4): $H=0\Rightarrow0=-\frac{1}{300}(x-90)^2+30\Rightarrow x=\ldots$",
       r"ALT: Alt (b) — A1 (AO 3.2a): $\Rightarrow x=185$ (m)"],
      True, 38),
    e("12c", "12(c)", ALG, "2.11", 1, LATEX["12c"],
      [r"B1 (AO 3.5b): Examples must focus on why the model may not be appropriate or give values/situations where the "
       r"model would break down: E.g. • The ground is unlikely to be horizontal • The ball is not a particle so has "
       r"dimensions/size • The ball is unlikely to travel in a vertical plane (as it will spin) • $H$ is not likely to be "
       r"a quadratic function in $x$. Notes: Candidate should either refer to an issue with one of the four aspects of "
       r"how the situation has been modelled or give a situation where the model breaks down • the ball has been "
       r"modelled as a particle • there may be trees (or other hazards) in the way that would affect the motion Condone "
       r"answers (where the link to the model is not completely made) such as • the ball will spin • ground is not flat "
       r"Do not accept answers which refer to the situation after it hits the ground (this isn't what was modelled) • the "
       r"ball will bounce after hitting the ground • it gives a negative height for some values for $x$ Do not accept "
       r"answers that do not refer to the model in question, or else give single word vague answers • the height of tee "
       r"may have been measured incorrectly • “friction”, “spin”, “force” etc • it does not take into account the weight "
       r"of the ball • it depends on how good the golfer is • the shape of the ball will affect the motion • you cannot "
       r"hit a ball the same distance each time you hit it"],
      True, 38),

    # ---------------- Q13 ----------------
    e("13", "13", COORD, "3.3, 3.2", 3, LATEX["13"],
      [r"M1 (AO 3.1a): $(x-3)^2+y^2=\left(\frac{t^2+5}{t^2+1}-3\right)^2+\left(\frac{4t}{t^2+1}\right)^2$. Notes: Attempts to "
       r"substitute the given parametric forms into the Cartesian equation or the lhs of the Cartesian equation. There "
       r"may have been an (incorrect) attempt to multiply out the $(x-3)^2$ term.",
       r"dM1 (AO 1.1b): $=\frac{(2-2t^2)^2+16t^2}{(t^2+1)^2}=\frac{4+8t^2+4t^4}{(t^2+1)^2}$. Notes: Attempts to combine (at "
       r"least the lhs) using correct processing into a single fraction, multiplies out and collects terms on the "
       r"numerator.",
       r"A1* (AO 2.1): $\frac{4(t^4+2t^2+1)}{(t^2+1)^2}=\frac{4(t^2+1)^2}{(t^2+1)^2}=4$*. Notes: Fully correct proof showing "
       r"all key steps",
       r"ALT: Alt — M1 (AO 3.1a): $x=\frac{t^2+5}{t^2+1}\Rightarrow xt^2+x=t^2+5\Rightarrow t^2=\frac{5-x}{x-1}$ "
       r"$y=\frac{4t}{t^2+1}\Rightarrow y^2=\frac{16t^2}{(t^2+1)^2}=\frac{16\left(\frac{5-x}{x-1}\right)}{\left(\frac{5-x}"
       r"{x-1}+1\right)^2}$. Notes: Adopts a correct strategy for eliminating $t$ to obtain an equation in terms of $x$ and "
       r"$y$ only. See scheme. Other methods exist which also lead to an appropriate equation. E.g using $t=\frac{y}{x-1}$",
       r"ALT: Alt — dM1 (AO 1.1b): $y^2=\frac{16\left(\frac{5-x}{x-1}\right)}{\left(\frac{5-x}{x-1}+1\right)^2}="
       r"16\left(\frac{5-x}{x-1}\right)\times\left(\frac{(x-1)}{5-x+x-1}\right)^2\Rightarrow y^2=(5-x)(x-1)$. Notes: Uses "
       r"correct processing to eliminate the fractions and start to simplify",
       r"ALT: Alt — A1* (AO 2.1): $y^2=(5-x)(x-1)\Rightarrow y^2=6x-x^2-5\Rightarrow y^2=4-(x-3)^2$ or other intermediate "
       r"step $\Rightarrow(x-3)^2+y^2=4$*. Notes: Fully correct proof showing all key steps"],
      False, 42),

    # ---------------- Q14 ----------------
    e("14", "14", DIFF, "7.4, 2.2", 4, LATEX["14"],
      [rf"M1 (AO 2.1): $y=\frac{{x-4}}{{2+\sqrt{{x}}}}\Rightarrow{DY}=\frac{{2+\sqrt{{x}}-(x-4)\frac{{1}}{{2}}x^{{-\frac{{1}}{{2}}}}}}"
       rf"{{(2+\sqrt{{x}})^2}}$. Notes: Attempts to use a correct rule e.g. quotient or product (& chain) rule to achieve the "
       rf"following forms Quotient : $\frac{{\alpha(2+\sqrt{{x}})-\beta(x-4)x^{{-\frac{{1}}{{2}}}}}}{{(2+\sqrt{{x}})^2}}$ but be "
       rf"tolerant of attempts where the $(2+\sqrt{{x}})^2$ has been incorrectly expanded Product: "
       rf"$\alpha(2+\sqrt{{x}})^{{-1}}+\beta x^{{-\frac{{1}}{{2}}}}(x-4)(2+\sqrt{{x}})^{{-2}}$ Alternatively with $t=\sqrt{{x}}$, "
       rf"$y=\frac{{t^2-4}}{{2+t}}\Rightarrow{DY}=\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}t}}\times\frac{{\mathrm{{d}}t}}{{\mathrm{{d}}x}}="
       rf"\frac{{2t(2+t)-(t^2-4)}}{{(2+t)^2}}\times\frac{{1}}{{2}}x^{{-\frac{{1}}{{2}}}}$ with same rules",
       rf"A1 (AO 1.1b): $y=\frac{{x-4}}{{2+\sqrt{{x}}}}\Rightarrow{DY}=\frac{{2+\sqrt{{x}}-(x-4)\frac{{1}}{{2}}x^{{-\frac{{1}}{{2}}}}}}"
       rf"{{(2+\sqrt{{x}})^2}}$. Notes: Correct derivative in any form. Must be in terms of a single variable (which could be "
       rf"$t$)",
       r"M1 (AO 1.1b): $=\frac{2+\sqrt{x}-(x-4)\frac{1}{2}x^{-\frac{1}{2}}}{(2+\sqrt{x})^2}=\frac{2+\sqrt{x}-\frac{1}{2}"
       r"\sqrt{x}+2x^{-\frac{1}{2}}}{(2+\sqrt{x})^2}=\frac{2\sqrt{x}+\frac{1}{2}x+2}{\sqrt{x}(2+\sqrt{x})^2}$. Notes: "
       r"Following a correct attempt at differentiation, it is scored for multiplying both numerator and denominator by "
       r"$\sqrt{x}$ and collecting terms to form a single fraction. It can also be scored from $\frac{uv'-vu'}{v^2}$ For "
       r"the $t=\sqrt{x}$, look for an attempt to simplify $\frac{t^2+4t+4}{(2+t)^2}\times\frac{1}{2t}$",
       rf"A1 (AO 2.1): $=\frac{{x+4\sqrt{{x}}+4}}{{2\sqrt{{x}}(2+\sqrt{{x}})^2}}=\frac{{(2+\sqrt{{x}})^2}}{{2\sqrt{{x}}"
       rf"(2+\sqrt{{x}})^2}}=\frac{{1}}{{2\sqrt{{x}}}}$. Notes: Correct expression showing all key steps with no errors or "
       rf"omissions. ${DY}$ must be seen at least once",
       r"ALT: Second scheme table (difference of two squares) — M1 (AO 2.1): $y=\frac{x-4}{2+\sqrt{x}}\Rightarrow y="
       r"\frac{(\sqrt{x}+2)(\sqrt{x}-2)}{2+\sqrt{x}}=\sqrt{x}-2$. Notes: Attempts to use difference of two squares. Can also "
       r"be scored using $t=\sqrt{x}\Rightarrow y=\frac{t^2-4}{t+2}\Rightarrow y=\frac{(t+2)(t-2)}{t+2}$",
       r"ALT: Second scheme table — A1 (AO 1.1b): $y=\sqrt{x}-2$ or $y=t-2$",
       r"ALT: Second scheme table — M1 (AO 1.1b): $\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{1}{2\sqrt{x}}$. Notes: Attempts to "
       r"differentiate an expression of the form $y=\sqrt{x}+b$",
       r"ALT: Second scheme table — A1 (AO 2.1): $\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{1}{2\sqrt{x}}$. Notes: Correct "
       r"expression showing all key steps with no errors or omissions. $\frac{\mathrm{d}y}{\mathrm{d}x}$ must be seen at "
       r"least once"],
      False, 44),

    # ---------------- Q15 ----------------
    e("15i", "15(i)", PROOF, "1.1", 2, LATEX["15i"],
      [r"M1 (AO 2.1): $n=1$, $2^3=8$, $3^1=3$, $(8>3)$ $n=2$, $3^3=27$, $3^2=9$, $(27>9)$ $n=3$, $4^3=64$, $3^3=27$, "
       r"$(64>27)$ $n=4$, $5^3=125$, $3^4=81$, $(125>81)$. Notes: A full and rigorous argument that uses all of $n=1$, 2, 3 "
       r"and 4 in an attempt to prove the given result. Award for attempts at both $(n+1)^3$ and $3^n$ for ALL values with "
       r"at least 5 of the 8 values correct. There is no requirement to compare their sizes, for example state that "
       r"$27>9$ Extra values, say $n=0$, may be ignored",
       r"A1 (AO 2.4): So if $n\leqslant4,n\in\mathbb{N}$ then $(n+1)^3>3^n$. Notes: Completes the proof with no errors and "
       r"an appropriate/allowable conclusion. This requires • all the values for $n=1$, 2, 3 and 4 correct. Ignore other "
       r"values • all pairs compared correctly • a minimal conclusion. Accept ✓ or hence proven for example"],
      False, 48),
    e("15ii", "15(ii)", PROOF, "1.1", 4, LATEX["15ii"],
      [r"M1 (AO 2.4): Begins the proof by negating the statement. “Let $m$ be odd ” or “Assume $m$ is not even”. Notes: "
       r"Begins the proof by negating the statement. See scheme This cannot be scored if the candidate attempts $m$ both "
       r"odd and even",
       r"M1 (AO 2.1): Set $m=(2p\pm1)$ and attempt $m^3+5=(2p\pm1)^3+5=\ldots$ Notes: For the key step in setting "
       r"$m=2p\pm1$ and attempting to expand $(2p\pm1)^3+5$ Award for a 4 term cubic expression.",
       r"A1 (AO 2.2a): $=8p^3+12p^2+6p+6$ AND deduces even. Notes: Correctly reaches $(2p+1)^3+5=8p^3+12p^2+6p+6$ and "
       r"states even. Alternatively reaches $(2p-1)^3+5=8p^3-12p^2+6p+4$ and states even.",
       r"A1 (AO 2.4): Completes proof which requires reason and conclusion • reason for $8p^3+12p^2+6p+6$ being even • "
       r"acceptable statement such as “this is a contradiction so if $m^3+5$ is odd then $m$ must be even”. Notes: A full "
       r"and complete argument that completes the contradiction proof. See scheme. (1) A reason why the expression "
       r"$8p^3+12p^2+6p+6$ or $8p^3-12p^2+6p+4$ is even Acceptable reasons are • all terms are even • sight of a "
       r"factorised expression E.g. $8p^3-12p^2+6p+4=2(4p^3-6p^2+3p+2)$ (2) Acceptable concluding statement Acceptable "
       r"concluding statements are • “this is a contradiction, so if $m^3+5$ is odd then $m$ is even” • “this is "
       r"contradiction, so proven.” • “So if $m^3+5$ is odd them $m$ is even” S.C If the candidate misinterprets the "
       r"demand and does not use proof by contradiction but states a counter example to the statement “if $m^3+5$ is odd "
       r"then $m$ must be even” such as when $m=\sqrt[3]{2}$ then they can score special case mark B1"],
      False, 48),
]

# Examiner report, sentence by sentence, in report order (the opening section on
# the paper changes is not attached to any question). Bulleted lists are joined
# into the sentence that introduces them, with "; ".
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "This was a very familiar and accessible question, and hence proved to be a suitable first question.", NO),
        (W, "A significant majority of candidates gave a fully correct response to this question, with the most common "
            "and successful approach being via the use of the factor theorem.", NO),
        (W, "Very few candidates tried to evaluate f (-1)."),
        (W, "Following on from correct use of f (1)=0, there were occasional errors in solving the resulting simple "
            "linear equation."),
        (W, "One (perhaps unexpected) error seen several times was to simplify $a(1)^3$ as $a^3$."),
        (W, "Algebraic division was attempted by some candidates, but the working needed here was much more complicated "
            "and so often led to errors (mainly with signs)."),
        (W, "This does highlight the importance of choosing the best method to a problem, as well as carrying it out "
            "accurately.", BACK),
    ],
    "02": [
        (W, "This focussed on the ability of a student to complete the square and proved to be as accessible as the "
            "first question.", NO),
        (W, "The vast majority of responses seen were fully correct."),
        ({"a"}, "In part (a) most candidates were able to score full marks."),
        ({"a"}, "The form $(x-2)^2+\\ldots$ was almost always achieved, although occasionally an incorrect "
                "$(x+2)^2+\\ldots$ was offered."),
        ({"a"}, "The most common error was having +9 instead of +1."),
        ({"b"}, "In response to part (b) both $P$ and $Q$ were often stated correctly with some candidates able to score "
                "the follow through mark for their $Q$ from their value of ‘$b$’ from part (a)."),
        ({"b"}, "Occasionally a mark was lost if they had $P$ =5 instead of $y$ =5 when $x$=0."),
        ({"b"}, "Very few sketches were seen, which if correctly labelled would have also scored full marks in (b)."),
        ({"b"}, "It was relatively common in (b)(ii) to see differentiation used, rather than the completed square "
                "expression.", NO),
    ],
    "03": [
        (W, "This proved to be a little more demanding than the first two questions but over 40% of candidates still "
            "scored all 6 marks.", NO),
        (W, "Errors seen by candidates are summarised below."),
        ({"a"}, r"In part (a) several candidates did not simplify $u_2$ sufficiently, giving $u_2=k-24/2$ which then lead "
                r"to a more complicated expression for $u_3$ which they had difficulty simplifying."),
        ({"a"}, "Some candidates did not use the given expression, but rather used $u_1+u_2+u_3=0$."),
        ({"b"}, "In part (b) candidates usually found both roots of the given quadratic either by factorisation or by "
                "use of the quadratic formula, with a small number by completing the square."),
        ({"b"}, "A significant minority failed to gain the A mark here as they did not state that 6 was an integer or "
                "that 40/3 was not an integer, with some excluding 40/3 on the grounds that it was irrational.", NO),
        ({"c"}, "Part (c) was invariably answered correctly by those who had solved the quadratic in part (b). although "
                "there were some candidates who gave a choice of answers.", NO),
    ],
    "04": [
        (W, "Aspects of this question proved to be more demanding than expected, but overall good marks were scored by "
            "candidates with most achieving over half marks in this question.", NO),
        ({"a"}, "Part(a) Almost all candidates identified the need to differentiate and set their expression equal to "
                "zero."),
        ({"a"}, "Although the derivative was often accurately found – the chain rule aspect of the log expression was "
                "omitted by some so that the expression $4x-4$ was not seen as the numerator of the required fraction."),
        ({"a"}, "Some numerators seen included $2x-2$, $2x-4$ or most often 1."),
        ({"a"}, "Manipulating their equation into the desired form was also an issue for some, with sign errors causing "
                "problems, whilst others could not properly convert their equation involving fractions into one not "
                "involving fractions."),
        ({"b"}, "Part (b) A significant majority of candidates obtained both required answers to this part."),
        ({"b"}, "Occasionally only $x_2$ and $x_3$ were found."),
        ({"b"}, "There were just a few occasions where a candidate had misread the 1/7 in the iterative formula as ½."),
        ({"b"}, "If the working was shown for this situation, then a method mark could still have been awarded.", BACK),
        ({"c"}, "Part (c) Whilst many candidates realised that a sign change of a function between 0.3405 and 0.3415 was "
                "required, it was also common to see an attempt at further iteration.", NO),
        ({"c"}, "This method was not acceptable as a proof of the location of the root.", BACK),
        ({"c"}, "A few chose to substitute into an inappropriate function such as f ($x$), or the iterative formula, and "
                "some failed to specify a function at all.", NO),
        ({"c"}, "For those who did use (typically) the expression from (a), most selected correct values to substitute "
                "in and identify the change of sign, finishing with a clear conclusion.", NO),
        ({"c"}, "It was very common, however, for the final mark to be lost in this part because there was no mention "
                "that the chosen function was continuous.", NO),
    ],
    "05": [
        (W, "This was yet another good source of marks with the modal mark being 6 out of 6, achieved by over 35% of "
            "the candidature.", NO),
        ({"a"}, r"Almost every candidate gained the B1 mark in part (a) with a fairly even split between those who used "
                r"$20\,000\times1.08^2$ and those who first calculated the profit after Year 1 = 21600 and then Year 2 = "
                r"23328 showing each step of their working to gain the mark.", NO),
        ({"b"}, "Part (b) was more problematic for many candidates."),
        ({"b"}, "There was a very good understanding of the inequality/equation to be formed, and the use of logs was "
                "almost always very good."),
        ({"b"}, "However, a significant minority of candidates failed to gain the final A mark giving an answer of 15.3 "
                "or 16 instead of Year 17."),
        ({"c"}, "Part (c) proved to be very well answered with the vast majority using the sum formula correctly."),
        ({"c"}, "Errors included using $n$ =19 instead of 20 in the formula or finding the 20th term instead of the "
                "sum."),
        ({"c"}, "A few candidates listed all the terms before adding them which often led to accuracy errors."),
    ],
    "06": [
        (W, "This was another question where the modal mark was full marks, this time achieved by over 40% of the "
            "candidates", NO),
        ({"a"}, r"Part(a) A very significant majority of candidates obtained vector $\boldsymbol{AC}$ correctly."),
        ({"a"}, r"Only a few subtracted rather than adding the given vectors $\boldsymbol{AB}$ and $\boldsymbol{BC}$."),
        ({"b"}, "Part (b) The vast majority of candidates made some progress in this part, realising that the lengths of "
                "the vectors would be required to solve this problem.", NO),
        ({"b"}, "A small minority then simply stopped, having done no more than finding the lengths of the sides of the "
                "triangle $ABC$, with some assuming that the triangle was right angled."),
        ({"b"}, "However most then went on to use the cosine rule to try to show the required result."),
        ({"b"}, "In almost all cases a correct cosine rule was stated and used, so that following on from a previous "
                "accuracy error, the method marks could be awarded."),
        ({"b"}, "Fully correct calculations were necessary in order to gain the final accuracy mark and very many "
                "candidates managed to do this and so gained full marks for this question.", NO),
        ({"b"}, "A few candidates, presumably those who had studied further maths, used the scalar product.", NO),
        ({"b"}, "This method would be perfectly acceptable, as long as the vectors are used the correct way around."),
        ({"b"}, r"Many using this method showed that $\cos ABC=-\frac{9}{10}$ but failed to explain why the answer should "
                r"be positive."),
    ],
    "07": [
        (W, "The first few marks in this question were very accessible but the final part of the question proved to be "
            "a useful discriminator especially around grade C and below.", NO),
        ({"a"}, "Part(a) The majority of candidates achieved full marks in this part.", NO),
        ({"a"}, r"Sign errors were responsible for most errors, although failure to halve was also seen with either or "
                r"both of $(x\pm10)^2$ and $(y\pm4)^2$ being seen."),
        ({"a"}, "Having achieved $(x-5)^2+(y+2)^2=18$, it rare to see the centre or radius not found correctly.", NO),
        ({"b"}, "Part (b) This part was found to be discriminating with complete solutions seen from only the most "
                "competent of candidates.", NO),
        ({"b"}, "The most common approach was to substitute $y=3x+k$ into the circle equation to find a quadratic in "
                "$x$ (with coefficients in terms of $k$) for the points of intersection."),
        ({"b"}, "Errors mostly arose when $(3x+k+2)^2$ was expanded incorrectly or the $2x+6kx$ terms not being gathered "
                "together."),
        ({"b"}, "Many solutions then stopped after the substitution and expansion step, as candidates did not seem to "
                "appreciate what to do with an equation of this complexity in two variables.", NO),
        ({"b"}, "Application of $b^2=4ac$ to find equal roots was used on many occasions but errors frequently "
                "occurred."),
        ({"b"}, "Only a very few solutions involved attempts via $b^2-4ac>0$."),
        ({"b"}, "It was not always obvious to see how a student had solved their quadratic (formula not quoted and "
                "values for $a$, $b$ and $c$ not seen) but a limited number of correct solutions were seen.", NO),
        ({"b"}, "Using a calculator quadratic solver was frequent and acceptable."),
        ({"b"}, "Several attempts started by using implicit differentiation on the circle equation."),
        ({"b"}, r"Although this is a possible method, it did not often go beyond using $\mathrm{d}y/\mathrm{d}x$ = 3 to "
                r"get $x+3y+1$= 0.", BACK),
        ({"b"}, "Another method seen several times was to find the equation of the normal ( i.e. the radius ) to try to "
                "make progress towards finding values of $k$, but this method also seldom went further than the "
                "equation of the line.", NO),
    ],
    "08": [
        (W, "This was the first significant modelling question on this paper.", NO),
        (W, "As with other series, candidates find aspects of modelling difficult."),
        ({"b", "c"}, "The barriers to success here were parts (b) and (c)."),
        ({"a"}, "In part (a) many candidates made progress and achieved a complete equation for the model with $k$ given "
                "exactly as ln(2)/5 or rounded to 0.139."),
        ({"a"}, "A few students rounded more accurately giving $k$ as 0.1386."),
        ({"a"}, "Some rounded $k$ to 0.14 and lost the accuracy mark."),
        ({"a"}, r"A fair number of students who failed to find the correct value of ‘$A$’ evaluated $\mathrm{e}^0$ as e."),
        ({"b"}, "In part (b) many students used an incorrect method to find the rate of increase in the number of "
                "bacteria."),
        ({"b"}, "Some substituted $t$ =8 into their expression for $N$, which just found the number of bacteria after 8 "
                "hours; others then went on to divide this number by 8 or even 1000 to try and find the rate of "
                "increase.", NO),
        ({"b"}, "Those who realised that the expression for $N$ needed to be differentiated to find the rate of increase "
                "often scored at least the method mark.", NO),
        ({"c"}, "For part (c) the majority of candidates who obtained the correct equation of the model in (a) were able "
                "to use both models given to set up an appropriate equation in $t$ or $T$ to gain the first method "
                "mark."),
        ({"c"}, "Processing the resulting equation using logs to obtain a linear equation in $t$ or $T$ posed more of a "
                "challenge and many made no further progress."),
        ({"c"}, "A large proportion who did attempt to make progress often used incorrect log work: some multiplied the "
                "logs rather than add them; others did not find the log of all the components, usually the ‘2’."),
        ({"c"}, "Some students combined the exponential functions incorrectly by dividing the powers rather than "
                "subtracting them."),
        ({"c"}, "Those scoring all three marks here were usually the most able candidates.", NO),
    ],
    "09": [
        (W, "This question was answered with varying degrees of success.", NO),
        (W, "Around 28% of the candidates failed to score any marks here at all, which was very suprising."),
        (W, "There were however many well formed and accurate solutions by careful candidates."),
        ({"a"}, "In part (a) most candidates managed to write down a correct identity and use an appropriate method to "
                "find values for $B$ and $C$."),
        ({"a"}, "To prove $A$ =0 was generally done via equating coefficients of $x^2$ or by setting $x$ = 0 or $x$=1."),
        ({"a"}, "A few candidates wrote down three equations for the coefficients and constants, but rarely was a "
                "correct set of solutions gained from this method.", NO),
        ({"a"}, "It was also not uncommon to see the RHS expanded either with or without the terms involving $A$ in an "
                "attempt to prove that $A$ = 0.", NO),
        ({"a"}, "Errors included having an incorrect identity from the start which resulted in no marks."),
        ({"b"}, "In part (b)(i) it was rare to see fully correct expansions.", NO),
        ({"b"}, "Good candidates often lost the final mark due to an error in adding the required terms."),
        ({"b"}, "A common error was forgetting to use their value for $C$ and only adding the expansion for "
                "$(1-2x)^{-1}$ rather than $C(1-2x)^{-1}$."),
        ({"b"}, "A few were unable to extract $2^{-1}$ correctly from $(5x+2)^{-2}$ (usually having this as 2).",
         {"ref": False, "note": "the mark scheme takes out a factor of $2^{-2}$"}),
        ({"b"}, "Other errors seen involved an expansion of $(1+2/5\\,x)^{-2}$ or else $(1+5/2\\,x)^2$ rather than "
                "$(1+5/2\\,x)^{-2}$."),
        ({"b"}, "Very few correct answers were seen for part (b)(ii) and this was very often not attempted.", NO),
        ({"b"}, "Those who did write a correct range sometimes also gave a second range which therefore did not gain the "
                "B mark here.", NO),
    ],
    "10": [
        (W, "This was found to be another discriminating question.", NO),
        (W, "Those who were familiar with the topic made good progress yet there were many other attempts that scored "
            "no marks at all.", NO),
        ({"a"}, r"Part(a) There were a significant number of fully correct solutions for this part, although some "
                r"candidates did not achieve the stage where both the numerator and denominators of their fraction "
                r"were factorised correctly with a common factor of ( $\sin\theta+\cos\theta$ ).", NO),
        ({"a"}, r"Another difficulty encountered by some, was how to use the different forms of the identity for "
                r"$\cos2\theta$ in order to deal with, and remove, the presence of both “1’s ” in the fraction."),
        ({"a"}, "Very few notational errors were seen, which was a pleasing improvement."),
        ({"b"}, r"Part (b) A significant number of candidates used the result of (a) correctly and started their "
                r"solution with $\tan2x=3\sin2x$."),
        ({"b"}, r"However, it was also the case that $\tan x=3\sin2x$ was seen several times as well.", NO),
        ({"b"}, r"Of those candidates who started correctly with $\tan2x=3\sin2x$, the significant majority simply "
                r"cancelled out the resulting factor of $\sin2x$ and in so doing neglected to consider the possibility "
                r"that $\sin2x=0$ and in so doing the solution $x=90^\circ$ was omitted from the fully correct list of "
                r"three answers.", NO),
        ({"b"}, r"Many candidates however, did state that $\cos2x=\frac{1}{3}$ and went on to get $35.3^\circ$ and "
                r"$144.7^\circ$ and so only one mark was lost."),
    ],
    "11": [
        (W, "The modal mark here was 3, most likely due to the accessibility of part (a).", NO),
        ({"b"}, "Marks in part (b) were only really awarded to the highest scoring candidates on this exam.", NO),
        ({"a"}, "Most candidates successfully answered part (a) applying the Trapezium Rule using all five values of $y$ "
                "from the given table."),
        ({"a"}, "Some students, who found the correct estimate of the area of $R$, failed to round their answer as "
                "requested, or occasionally rounded incorrectly, and lost the accuracy mark."),
        ({"a"}, "Errors, although rare, were usually as a result of an incorrect strip width."),
        ({"b"}, "In part (b) many candidates failed to recognise that integration by parts was needed to make "
                "progress."),
        ({"b"}, "Several students, who made progress and correctly applied ‘integration by parts’ twice, unfortunately "
                "lost the final accuracy mark due to sign or coefficient errors that had crept in."),
        ({"b"}, "Most who integrated appropriately applied the correct limits and applied ln(4) = 2ln(2)."),
        ({"b"}, r"Errors were many and varied here and included Candidates who believed that "
                r"$\int(\ln x)^2\,\mathrm{d}x=\frac{1}{3}(\ln x)^3$; Candidates who believed that $(\ln x)^2=2\ln x$"),
        ({"b"}, r"Candidates who used the substitution $u=\ln x$ seemed to more easily recognise "
                r"$\int u^2\mathrm{e}^u\,\mathrm{d}u$ as integration by parts twice."),
    ],
    "12": [
        (W, "This was the second modelling question on this paper.", NO),
        (W, "It proved to be a significant discriminator between candidates, with a significant minority making little "
            "or no progress.", BACK),
        (W, "It certainly seems to be a topic that students find hard to access.", BACK),
        ({"a"}, "Part (a) The most common approach which led to either partial or complete success was to start with "
                "$H=ax^2+bx+c$ and use (0,3) to find that $c$ =3."),
        ({"a"}, "Many candidates then used (120,27) to find an equation connecting $a$ and $b$, but sometimes no more "
                "progress was made."),
        ({"a"}, "Of those who did make further progress, the most common approach was to use differentiation and the "
                "knowledge that the gradient was zero when $x$=90 to get a second equation in $a$ and $b$.", NO),
        ({"a", "b"}, "Candidates using this approach often went on to get (a) fully correct and then also to gain most "
                     "if not all of the marks in (b) as well.", NO),
        ({"a"}, "It was only rarely that there was a misunderstanding about $H$=0 rather than $H$=3 when $x$=0.", NO),
        ({"a"}, "There were other methods used in (a) and any of these could have led to success if applied "
                "correctly.", NO),
        ({"a"}, "For example, using the fact that the quadratic has a turning point when $x$ =90 and so "
                "$H=a(x-90)^2+c$ was used correctly by some candidates."),
        ({"a"}, "Alternatively, using additional implied points such as (60,27) or (180,3) due to the symmetry of "
                "quadratic curves, was used appropriately by candidates.", NO),
        ({"b"}, "Part (b) Both parts were done well by candidates who had achieved a correct answer to (a)."),
        ({"b"}, "Part (b) (i) There were only a very few who omitted the units here."),
        ({"b"}, "A wrong answer to (a) would have made it difficult to gain the accuracy mark here.", NO),
        ({"b"}, "Part (b)(ii) A wrong answer to (a) could have scored a method mark here if the candidate’s quadratic "
                "had been solved correctly."),
        ({"c"}, "Part (c) A wide range of comments were quoted here– some of those that did not gain the B1.", NO),
        ({"c"}, "Many of these focussed on what happened to the ball after hitting the ground, or picked out a "
                "relatively trivial aspect such as the height of the tee being inaccurate.", BACK),
        ({"c"}, "Others mentioned the weight of the ball, or that it depended on the force of the contact.", NO),
        ({"c"}, "There were many acceptable comments."),
        ({"c"}, "These should have focussed on why one of the four modelling assumptions referred to in the question may "
                "not have been valid.", BACK),
        ({"c"}, "Acceptable responses included the fact that the ball is not a particle, the ground may not be "
                "horizontal, the path may not be a quadratic (parabola) or it might not travel in a vertical plane "
                "(Spin was mentioned in this context).", NO),
    ],
    "13": [
        (W, "A solution gaining all three marks was relatively rare to see, and there were many very poor "
            "demonstrations of algebraic manipulation seen."),
        (W, "Many candidates managed to score the first M mark but usually were unable to make further progress."),
        (W, "The attempts were split between candidates who attempted to substitute into the LHS of the Cartesian "
            "equation to give an equation/expression in $t$ and those who attempted to eliminate $t$, usually via "
            "$t^2=(5-x)/(x-1)$, to give an equation involving $x$ and $y$ only.", NO),
        (W, "The errors then ranged from incorrect squaring of a bracket to incorrect manipulation of fractions with "
            "very few unable to complete the proof"),
    ],
    "14": [
        (W, "This question proved equally challenging and very few fully correct solutions were seen.", NO),
        (W, r"The modal mark achieved here was 2, scored by over 40% of the candidates, most often for a fully correct "
            r"attempt at $\mathrm{d}y/\mathrm{d}x$."),
        (W, "Most solutions seen used the quotient rule although incorrect application of the rule often meant that no "
            "marks could be awarded."),
        (W, "The most common errors were subtracting the wrong way round on the numerator, or else adding the two "
            "expressions on the numerator."),
        (W, r"Differentiation of $\sqrt{x}$ suprisingly caused a few problems as well."),
        (W, "Product rule expansions seldom got past the first expression."),
        (W, "The ability to manipulate the ensuing algebraic expression was often lacking, with fractional terms within "
            "a fraction, the main cause for failure."),
        (W, "Alternative methods which might have simplified the algebra were seen, but only rarely."),
        (W, "Only a handful spotted that a difference of two squares method applied to the numerator would have made "
            "this a very simple problem.", NO),
    ],
    "15": [
        (W, "Candidates have not been too successful in answering questions on the topic of ‘Proof’ within this new "
            "specification, and this question proved to be no different.", NO),
        ({"i"}, "Part (i) The meaning of “proof by exhaustion” was not fully understood by all."),
        ({"i"}, "Many candidates failing to consider all four of the possible cases mentioned."),
        ({"i"}, "A common response was to test just $n$ =4 and $n$ =5 and conclude that it was true for $n$ = 4 but not "
                "$n$ = 5 so it was proven for $n\\leqslant4$.", NO),
        ({"i"}, "Some candidates who did consider all values of $n$ = 1,2,3 and 4, left some expressions unevaluated."),
        ({"i"}, "Occasionally the eight required values were found but there was no evidence that they were being "
                "compared."),
        ({"i"}, "It was essential that a proper conclusion is made at the end of a proof, and despite having convincing "
                "working and reasons, some candidates lost the final accuracy mark here because they did not have a "
                "conclusion saying that the required result was indeed true.", NO),
        ({"ii"}, "Part (ii) Very many candidates did score the first mark here for saying “Suppose that $m$ is odd”."),
        ({"ii"}, "However, a common error was to state “let $m^3+5$ be odd” instead leading to 0 marks."),
        ({"ii"}, "It was common to see $2p+1$ or $2k+1$ being used to represent an odd number and there were many "
                 "occasions where $(2p+1)^3+5$ was seen in a candidate’s working.", NO),
        ({"ii"}, "In some cases there were algebraic errors in attempting to expand the cube of $(2p+1)$, but most "
                 "candidates did achieve the required four term cubic $8p^3+12p^2+6p+6$."),
        ({"ii"}, "When this cubic was correct, those candidates very often went on to gain the next two accuracy marks "
                 "by proving, by factorisation, that $m^3+5$ was even, and then stating that there is a contradiction "
                 "(to the assumption that $m$ is odd) and so m must be even.", BACK),
    ],
}

# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
RATINGS = {
    "01": ("easy", ("01", 1)),
    "02a": ("easy", ("02", 2)),
    "02b": ("easy", ("02", 1)),
    "03a": ("medium", ("03", 0)),
    "03b": ("medium", ("03", 5)),
    "03c": ("easy", ("03", 6)),
    "04a": ("medium", ("04", 2)),
    "04b": ("easy", ("04", 5)),
    "04c": ("medium", ("04", 13)),
    "05a": ("easy", ("05", 1)),
    "05b": ("medium", ("05", 4)),
    "05c": ("easy", ("05", 5)),
    "06a": ("easy", ("06", 1)),
    "06b": ("medium", ("06", 7)),
    "07a": ("easy", ("07", 1)),
    "07b": ("hard", ("07", 4)),
    "08a": ("medium", ("08", 3)),
    "08b": ("hard", ("08", 7)),
    "08c": ("hard", ("08", 11)),
    "09a": ("easy", ("09", 3)),
    "09b": ("hard", ("09", 8)),
    "10a": ("medium", ("10", 2)),
    "10b": ("medium", ("10", 8)),
    "11a": ("easy", ("11", 2)),
    "11b": ("hard", ("11", 1)),
    "12a": ("medium", ("12", 4)),
    "12b": ("medium", ("12", 11)),
    "12c": ("medium", ("12", 18)),
    "13": ("hard", ("13", 0)),
    "14": ("hard", ("14", 0)),
    "15i": ("hard", ("15", 2)),
    "15ii": ("medium", ("15", 7)),
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
