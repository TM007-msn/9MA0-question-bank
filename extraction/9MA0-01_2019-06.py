"""Draft builder for 9MA0-01 2019-06 (A level Pure Paper 1, June 2019).

Run (from the project root, with the venv active):
    python extraction/9MA0-01_2019-06.py        # writes out/drafts/9MA0-01_2019-06.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-01_2019-06.json

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

P, S = "9MA0-01", "2019-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "04bi"); label as printed (e.g. "4(b)(i)")."""
    return {"id": f"{P}_{S}_Q{q}", "paper": P, "series": S, "question": label, "topic": topic,
            "spec_ref": spec, "marks": marks, "question_latex": latex, "mark_scheme": ms,
            "examiner_notes": None, "difficulty": None, "difficulty_evidence": None,
            "has_diagram": diagram, "source_page": page, "source_file": SRC}


PROOF = "Proof"
ALG = "Algebra and functions"
SEQ = "Sequences and series"
TRIG = "Trigonometry"
EXP = "Exponentials and logarithms"
DIFF = "Differentiation"
INT = "Integration"


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


DY = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
DXY = r"\frac{\mathrm{d}x}{\mathrm{d}y}"
DX = r"\,\mathrm{d}x"

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q2 = [r"[Figure 1: the curve $y=\cos x$ drawn on a grid of unit squares, with $x$ from about $-7$ to 7 and $y$ from "
      r"$-3$ to 3; the curve has maximum points at $(0, 1)$ and near each end of the grid, minimum points at about "
      r"$x=\pm3.1$, and crosses the $x$-axis four times.]",
      r"Figure 1 shows a plot of part of the curve with equation $y=\cos x$ where $x$ is measured in radians. Diagram 1, "
      r"on the opposite page, is a copy of Figure 1."]
Q2A = ["Use Diagram 1 to show why the equation", r"$$\cos x-2x-\frac{1}{2}=0$$",
       "has only one real root, giving a reason for your answer."]
Q3 = [r"$$y=\frac{5x^2+10x}{(x+1)^2}\qquad x\neq-1$$"]
Q3A = rf"Show that ${DY}=\frac{{A}}{{(x+1)^n}}$ where $A$ and $n$ are constants to be found."
Q4A = ["Find the first three terms, in ascending powers of $x$, of the binomial expansion of",
       r"$$\frac{1}{\sqrt{4-x}}$$", "giving each coefficient in its simplest form."]
Q4M = [r"The expansion can be used to find an approximation to $\sqrt{2}$",
       "Possible values of $x$ that could be substituted into this expansion are:",
       r"• $x=-14$ because $\frac{1}{\sqrt{4-x}}=\frac{1}{\sqrt{18}}=\frac{\sqrt{2}}{6}$",
       r"• $x=2$ because $\frac{1}{\sqrt{4-x}}=\frac{1}{\sqrt{2}}=\frac{\sqrt{2}}{2}$",
       r"• $x=-\frac{1}{2}$ because $\frac{1}{\sqrt{4-x}}=\frac{1}{\sqrt{\frac{9}{2}}}=\frac{\sqrt{2}}{3}$",
       "(b) Without evaluating your expansion,"]
Q5 = [r"$$\mathrm{f}(x)=2x^2+4x+9\qquad x\in\mathbb{R}$$"]
Q6A = [r"Solve, for $-180^\circ\leqslant\theta\leqslant180^\circ$, the equation", r"$$5\sin2\theta=9\tan\theta$$",
       "giving your answers, where necessary, to one decimal place.",
       "[Solutions based entirely on graphical or numerical methods are not acceptable.]"]
Q7 = ["In a simple model, the value, £$V$, of a car depends on its age, $t$, in years.",
      "The following information is available for car $A$", "• its value when new is £20 000",
      "• its value after one year is £16 000"]
Q7A = "Use an exponential model to form, for car $A$, a possible equation linking $V$ with $t$."
Q7M = ["The value of car $A$ is monitored over a 10-year period.", "Its value after 10 years is £2 000"]
Q8 = [r"[Figure 2: the curve $y=x(x+2)(x-4)$, a cubic crossing the $x$-axis at a negative value, at $O$ and at a positive "
      r"value, with a maximum to the left of the $y$-axis and a minimum to the right of it; the region $R_1$ between the "
      r"curve and the negative $x$-axis is shaded, and the region $R_2$ below the positive $x$-axis, between the curve and "
      r"the vertical line through $b$ (a little to the right of $O$), is shaded.]",
      "Figure 2 shows a sketch of part of the curve with equation $y=x(x+2)(x-4)$.",
      "The region $R_1$ shown shaded in Figure 2 is bounded by the curve and the negative $x$-axis."]
Q8A = r"Show that the exact area of $R_1$ is $\frac{20}{3}$"
Q8M = ["The region $R_2$ also shown shaded in Figure 2 is bounded by the curve, the positive $x$-axis and the line with "
       "equation $x=b$, where $b$ is a positive constant and $0<b<4$",
       "Given that the area of $R_1$ is equal to the area of $R_2$"]
Q9 = ["Given that $a>b>0$ and that $a$ and $b$ satisfy the equation", r"$$\log a-\log b=\log(a-b)$$"]
Q11 = ["A competitor is running a 20 kilometre race.",
       "She runs each of the first 4 kilometres at a steady pace of 6 minutes per kilometre.",
       "After the first 4 kilometres, she begins to slow down.",
       "In order to estimate her finishing time, the time that she will take to complete each subsequent kilometre is "
       "modelled to be 5% greater than the time that she took to complete the previous kilometre."]
Q11B = [r"how that her estimated time, in minutes, to run the $r$th kilometre, for $5\leqslant r\leqslant20$, is",
        r"$$6\times1.05^{r-4}$$"]
Q12 = [r"$$\mathrm{f}(x)=10\mathrm{e}^{-0.25x}\sin x,\qquad x\geqslant0$$"]
Q12A = (r"Show that the $x$ coordinates of the turning points of the curve with equation $y=\mathrm{f}(x)$ satisfy the "
        r"equation $\tan x=4$")
Q12F = [r"[Figure 3: the curve $y=\mathrm{f}(x)$ for $x\geqslant0$, starting at $O$, rising to a tall peak and then "
        r"oscillating about the $x$-axis with peaks and troughs that get smaller and smaller.]",
        r"Figure 3 shows a sketch of part of the curve with equation $y=\mathrm{f}(x)$."]
Q12B = ["Sketch the graph of $H$ against $t$ where", r"$$\mathrm{H}(t)=\left|10\mathrm{e}^{-0.25t}\sin t\right|\qquad "
        r"t\geqslant0$$", "showing the long-term behaviour of this curve."]
Q12M = [r"The function $\mathrm{H}(t)$ is used to model the height, in metres, of a ball above the ground $t$ seconds "
        r"after it has been kicked."]
Q13 = ["The curve $C$ with equation", r"$$y=\frac{p-3x}{(2x-q)(x+3)}\qquad x\in\mathbb{R},x\neq-3,x\neq2$$",
       r"where $p$ and $q$ are constants, passes through the point $\left(3,\frac{1}{2}\right)$ and has two vertical "
       r"asymptotes with equations $x=2$ and $x=-3$"]
Q13A = ["(i) Explain why you can deduce that $q=4$", "(ii) Show that $p=15$"]
Q14 = ["The curve $C$, in the standard Cartesian plane, is defined by the equation",
       r"$$x=4\sin2y\qquad\frac{-\pi}{4}<y<\frac{\pi}{4}$$", "The curve $C$ passes through the origin $O$"]
Q14A = rf"Find the value of ${DY}$ at the origin."

LATEX = {
    "01": L(r"$$\mathrm{f}(x)=3x^3+2ax^2-4x+5a$$",
            r"Given that $(x+3)$ is a factor of $\mathrm{f}(x)$, find the value of the constant $a$."),
    "02a": L(*Q2, *Q2A),
    "02b": L(*Q2, "(a) " + Q2A[0], *Q2A[1:], r"Given that the root of the equation is $\alpha$, and that $\alpha$ is small,",
             r"(b) use the small angle approximation for $\cos x$ to estimate the value of $\alpha$ to 3 decimal places."),
    "03a": L(*Q3, Q3A),
    "03b": L(*Q3, "(a) " + Q3A, rf"(b) Hence deduce the range of values for $x$ for which ${DY}<0$"),
    "04a": L(*Q4A),
    "04bi": L("(a) " + Q4A[0], *Q4A[1:], *Q4M,
              "(i) state, giving a reason, which of the three values of $x$ should not be used"),
    "04bii": L("(a) " + Q4A[0], *Q4A[1:], *Q4M,
               r"(ii) state, giving a reason, which of the three values of $x$ would lead to the most accurate "
               r"approximation to $\sqrt{2}$"),
    "05a": L(*Q5, r"Write $\mathrm{f}(x)$ in the form $a(x+b)^2+c$, where $a$, $b$ and $c$ are integers to be found."),
    "05b": L(*Q5, r"Sketch the curve with equation $y=\mathrm{f}(x)$ showing any points of intersection with the "
                  r"coordinate axes and the coordinates of any turning point."),
    "05c": L(*Q5, r"(i) Describe fully the transformation that maps the curve with equation $y=\mathrm{f}(x)$ onto the "
                  r"curve with equation $y=\mathrm{g}(x)$ where", r"$$\mathrm{g}(x)=2(x-2)^2+4x-3\qquad x\in\mathbb{R}$$",
             "(ii) Find the range of the function", r"$$\mathrm{h}(x)=\frac{21}{2x^2+4x+9}\qquad x\in\mathbb{R}$$"),
    "06a": L(*Q6A),
    "06b": L("(a) " + Q6A[0], *Q6A[1:], "(b) Deduce the smallest positive solution to the equation",
             r"$$5\sin(2x-50^\circ)=9\tan(x-25^\circ)$$"),
    "07a": L(*Q7, Q7A),
    "07b": L(*Q7, "(a) " + Q7A, *Q7M, "(b) Evaluate the reliability of your model in light of this information."),
    "07c": L(*Q7, "(a) " + Q7A, *Q7M, "The following information is available for car $B$",
             "• it has the same value, when new, as car $A$", "• its value depreciates more slowly than that of car $A$",
             "(c) Explain how you would adapt the equation found in (a) so that it could be used to model the value of "
             "car $B$."),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, "(a) " + Q8A, *Q8M, "(b) verify that $b$ satisfies the equation", r"$$(b+2)^2(3b^2-20b+20)=0$$"),
    "08c": L(*Q8, *Q8M, "The roots of the equation $3b^2-20b+20=0$ are 1.225 and 5.442 to 3 decimal places.",
             "The value of $b$ is therefore 1.225 to 3 decimal places.",
             "Explain, with the aid of a diagram, the significance of the root 5.442"),
    "09a": L(*Q9, "show that", r"$$a=\frac{b^2}{b-1}$$"),
    "09b": L(*Q9, "(a) show that", r"$$a=\frac{b^2}{b-1}$$",
             "(b) Write down the full restriction on the value of $b$, explaining the reason for this restriction."),
    "10i": L(r"Prove that for all $n\in\mathbb{N}$, $n^2+2$ is not divisible by 4"),
    "10ii": L(r"“Given $x\in\mathbb{R}$, the value of $|3x-28|$ is greater than or equal to the value of $(x-9)$.”",
              "State, giving a reason, if the above statement is always true, sometimes true or never true."),
    "11a": L(*Q11, "Using the model,",
             "show that her time to run the first 6 kilometres is estimated to be 36 minutes 55 seconds,"),
    "11b": L(*Q11, "S" + Q11B[0], Q11B[1]),
    "11c": L(*Q11, "(b) S" + Q11B[0], Q11B[1],
             "(c) Estimate the total time, in minutes and seconds, that she will take to complete the race."),
    "12a": L(*Q12, Q12A),
    "12b": L(*Q12, *Q12F, *Q12B),
    "12c": L(*Q12, "(a) " + Q12A, *Q12F, "(b) " + Q12B[0], *Q12B[1:], *Q12M, "Using this model, find",
             "(c) the maximum height of the ball above the ground between the first and second bounce."),
    "12d": L(*Q12, *Q12F, "(b) " + Q12B[0], *Q12B[1:], *Q12M,
             "(d) Explain why this model should not be used to predict the time of each bounce."),
    "13a": L(*Q13, *Q13A),
    "13b": L(*Q13, "(a) " + Q13A[0], Q13A[1],
             r"[Figure 4: part of the curve $C$ to the right of the $y$-axis, coming down steeply from high up, crossing "
             r"the $x$-axis to the right of $x=3$ and then running just below the $x$-axis; the region $R$ between $C$, "
             r"the $x$-axis and the vertical line at $x=3$ is shaded.]",
             r"Figure 4 shows a sketch of part of the curve $C$. The region $R$, shown shaded in Figure 4, is bounded by "
             r"the curve $C$, the $x$-axis and the line with equation $x=3$",
             r"(b) Show that the exact value of the area of $R$ is $a\ln2+b\ln3$, where $a$ and $b$ are rational "
             r"constants to be found."),
    "14a": L(*Q14, Q14A),
    "14b": L(*Q14, "(a) " + Q14A,
             r"(b) (i) Use the small angle approximation for $\sin2y$ to find an equation linking $x$ and $y$ for points "
             r"close to the origin.", "(ii) Explain the relationship between the answers to (a) and (b)(i)."),
    "14c": L(*Q14, "Show that, for all points $(x, y)$ lying on $C$,", rf"$${DY}=\frac{{1}}{{a\sqrt{{b-x^2}}}}$$",
             "where $a$ and $b$ are constants to be found."),
}

OPT2 = "ALT: Option 2"
OPT3 = "ALT: Option 3"
ALGP = "ALT: Example of a very similar algebraic proof"
LOGP = "ALT: Example of a proof via logic"
CONP = "ALT: Example of proof via contradiction"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", ALG, "2.6", 3, LATEX["01"],
      [r"M1 (AO 3.1a): Attempts $\mathrm{f}(-3)=3\times(-3)^3+2a\times(-3)^2-4\times-3+5a=0$. Notes: Chooses a suitable "
       r"method to set up a correct equation in $a$ which may be unsimplified. This is mainly applying $\mathrm{f}(-3)=0$ "
       r"leading to a correct equation in $a$. Missing brackets may be recovered. Other methods may be seen but they are "
       r"more demanding If division is attempted must produce a correct equation in a similar way to the "
       r"$\mathrm{f}(-3)=0$ method [the mark scheme shows the long division of $3x^3+2ax^2-4x+5a$ by $x+3$, with quotient "
       r"$3x^2+(2a-9)x+23-6a$ and last line $(23-6a)x+69-18a$] So accept $5a=69-18a$ or equivalent, where it implies that "
       r"the remainder will be 0 You may also see variations on the table below. In this method the terms in $x$ are "
       r"equated to $-4$ [the mark scheme shows a grid with $x$ and 3 multiplying $3x^2$, $(2a-9)x$ and $\frac{5a}{3}$, "
       r"giving $6a-27+\frac{5a}{3}=-4$]",
       r"M1 (AO 1.1b): Solves linear equation $23a=69\Rightarrow a=\ldots$ Notes: This is scored for an attempt at solving "
       r"a linear equation in $a$. For the main scheme it is dependent upon having attempted $\mathrm{f}(\pm3)=0$. Allow "
       r"for a linear equation in $a$ leading to $a=\ldots$. Don’t be too concerned with the mechanics of this. Via "
       r"division accept a division of $3x^3+2ax^2-4x+5a$ by $x+3$ (quotient starting $3x^2\ldots$) followed by a "
       r"remainder in $a$ set $=0\Rightarrow a=\ldots$ or two terms in $a$ are equated so that the remainder $=0$ FYI the "
       r"correct remainder via division is $23a+12-81$ oe",
       r"A1 (AO 1.1b): $a=3$ cso. Notes: $a=3$ cso An answer of 3 with no incorrect working can be awarded 3 marks"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", ALG, "2.7, 5.3", 2, LATEX["02a"],
      [r"B1 (AO 3.1a): [Diagram 1 with the line $y=2x+\frac{1}{2}$ drawn through the curve $y=\cos x$, meeting it once.] "
       r"Notes: Draws $y=2x+\frac{1}{2}$ on Figure 1 or Diagram 1 with an attempt at the correct gradient and the correct "
       r"intercept. Look for a straight line with an intercept at $\approx\frac{1}{2}$ and a further point at "
       r"$\approx\left(\frac{1}{2},1\frac{1}{2}\right)$ Allow a tolerance of 0.25 of a square in either direction on these "
       r"two points. It must appear in quadrants 1, 2 and 3.",
       r"B1 (AO 2.4): For an allowable linear graph and explaining that there is only one intersection. Notes: There must "
       r"be an allowable linear graph on Figure 1 or Diagram1 for this to be awarded Explains that as there is only one "
       r"intersection so there is just one root. This requires a reason and a minimal conclusion. The question asks "
       r"candidates to explain but as a bare minimum allow one “intersection” Note: An allowable linear graph is one with "
       r"intercept of $\pm\frac{1}{2}$ with one intersection with $\cos x$ OR gradient of $\pm2$ with one intersection "
       r"with $\cos x$"],
      True, 4),
    e("02b", "2(b)", TRIG, "5.2, 2.3", 3, LATEX["02b"],
      [r"M1 (AO 1.1b): $\cos x-2x-\frac{1}{2}=0\Rightarrow1-\frac{x^2}{2}-2x-\frac{1}{2}=0$. Notes: Attempts to use the "
       r"small angle approximation $\cos x=1-\frac{x^2}{2}$ in the given equation. The equation must be in a single "
       r"variable but may be recovered later in the question.",
       r"dM1 (AO 1.1b): Solves their $x^2+4x-1=0$. Notes: Proceeds to a 3TQ in a single variable and attempts to solve. "
       r"See General Principles The previous M must have been scored. Allow completion of square or formula or "
       r"calculator. Do not allow attempts via factorisation unless their equation does factorise. You may have to use "
       r"your calculator to check if a calculator is used.",
       r"A1 (AO 1.1b): Allow awrt 0.236 but accept $-2+\sqrt{5}$. Notes: Allow $-2+\sqrt{5}$ or awrt 0.236. Do not allow "
       r"this where there is another root given and it is not obvious that 0.236 has been chosen."],
      True, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", DIFF, "7.4", 4, LATEX["03a"],
      [rf"M1 (AO 3.1a): Correct method used in attempting to differentiate $y=\frac{{5x^2+10x}}{{(x+1)^2}}$. Notes: "
       rf"Attempts to use a correct rule to differentiate Eg: Use of quotient (& chain) rules on "
       rf"$y=\frac{{5x^2+10x}}{{(x+1)^2}}$ Alternatively uses the product (and chain) rules on "
       rf"$y=(5x^2+10x)(x+1)^{{-2}}$ Condone slips but expect $\left({DY}\right)=\frac{{(x+1)^2\times(Ax+B)-(5x^2+10x)"
       rf"\times(Cx+D)}}{{(x+1)^4}}$ $(A,B,C,D>0)$ or $\left({DY}\right)=\frac{{(x+1)^2\times(Ax+B)-(5x^2+10x)\times"
       rf"(Cx+D)}}{{\left((x+1)^2\right)^2}}$ $(A,B,C,D>0)$ using the quotient rule or $\left({DY}\right)=(x+1)^{{-2}}"
       rf"\times(Ax+B)+(5x^2+10x)\times C(x+1)^{{-3}}$ $(A,B,C\neq0)$ using the product rule. Condone missing brackets and "
       rf"slips for the M mark. For instance if they quote $u=5x^2+10$, $v=(x+1)^2$ and don’t make the differentiation "
       rf"easier, they can be awarded this mark for applying the correct rule. Also allow where they quote the correct "
       rf"formula, give values of $u$ and $v$, but only have $v$ rather than $v^2$ the denominator.",
       rf"A1 (AO 1.1b): ${DY}=\frac{{(x+1)^2\times(10x+10)-(5x^2+10x)\times2(x+1)}}{{(x+1)^4}}$ oe. Notes: A correct "
       rf"(unsimplified) answer Eg. $\left({DY}\right)=\frac{{(x+1)^2\times(10x+10)-(5x^2+10x)\times2(x+1)}}{{(x+1)^4}}$ "
       rf"or equivalent via the quotient rule. OR $\left({DY}\right)=(x+1)^{{-2}}\times(10x+10)+(5x^2+10x)\times"
       rf"-2(x+1)^{{-3}}$ or equivalent via the product rule",
       rf"M1 (AO 2.1): Factorises/Cancels term in $(x+1)$ and attempts to simplify ${DY}=\frac{{(x+1)\times(10x+10)-"
       rf"(5x^2+10x)\times2}}{{(x+1)^3}}=\frac{{A}}{{(x+1)^3}}$. Notes: A valid attempt to proceed to the given form of the "
       rf"answer. It is dependent upon having a quotient rule of $\pm\frac{{v\mathrm{{d}}u-u\mathrm{{d}}v}}{{v^2}}$ and "
       rf"proceeding to $\frac{{A}}{{(x+1)^3}}$ It can also be scored on a quotient rule of "
       rf"$\pm\frac{{v\mathrm{{d}}u-u\mathrm{{d}}v}}{{v}}$ and proceeding to $\frac{{A}}{{(x+1)}}$ You may see candidates "
       rf"expanding terms in the numerator. FYI $10x^3+30x^2+30x+10-10x^3-30x^2-20x$ but under this method they must reach "
       rf"the same expression as required by the main method. Using the product rule expect to see a common denominator "
       rf"being used correctly before the above",
       rf"A1 (AO 1.1b): ${DY}=\frac{{10}}{{(x+1)^3}}$. Notes: ${DY}=\frac{{10}}{{(x+1)^3}}$ There is no requirement to see "
       rf"${DY}=$ and they can recover from missing brackets/slips.",
       r"ALT: Alt via division — M1 (AO 3.1a): Writes $y=\frac{5x^2+10x}{(x+1)^2}$ in form $y=A\pm\frac{B}{(x+1)^2}$ "
       r"$A,B\neq0$",
       r"ALT: Alt via division — A1 (AO 1.1b): Writes $y=\frac{5x^2+10x}{(x+1)^2}$ in the form $y=5-\frac{5}{(x+1)^2}$",
       rf"ALT: Alt via division — M1 (AO 2.1): Uses the chain rule $\Rightarrow{DY}=\frac{{C}}{{(x+1)^3}}$ (May be scored "
       rf"from $A=0$ )",
       rf"ALT: Alt via division — A1 (AO 1.1b): ${DY}=\frac{{10}}{{(x+1)^3}}$ which cannot be awarded from incorrect value "
       rf"of $A$"],
      False, 6),
    e("03b", "3(b)", DIFF, "7.3", 1, LATEX["03b"],
      [rf"B1ft (AO 2.2a): For $x<-1$ Follow through on their ${DY}=\frac{{A}}{{(x+1)^n}},n=1,3$. Notes: Score for deducing "
       rf"the correct answer of $x<-1$ This can be scored independent of their answer to part (a). Alternatively score for "
       rf"a correct ft answer for their ${DY}=\frac{{A}}{{(x+1)^n}}$ where $A<0$ and $n=1,3$ award for $x>-1$. So for "
       rf"example if $A>0$ and $n=1,3\Rightarrow x<-1$",
       r"ALT: Alt via division — B1ft (AO 2.2a): For $x<-1$ or correct follow through"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", SEQ, "4.1", 4, LATEX["04a"],
      [r"M1 (AO 2.1): $\frac{1}{\sqrt{4-x}}=(4-x)^{-\frac{1}{2}}=4^{-\frac{1}{2}}\times(1\pm\ldots)$. Notes: For the "
       r"strategy of expanding $\frac{1}{\sqrt{4-x}}$ using the binomial expansion. You must see $4^{-\frac{1}{2}}$ oe and "
       r"an expansion which may or may not be combined.",
       r"M1 (AO 1.1b): Uses a “correct” binomial expansion for their $(1+ax)^n=1+nax+\frac{n(n-1)}{2}a^2x^2+$ Notes: Uses "
       r"a correct binomial expansion for their $(1\pm ax)^n=1\pm nax\pm\frac{n(n-1)}{2}a^2x^2+$ Condone sign slips and "
       r"the “$a$” not being squared in term 3. Condone $a=\pm1$ Look for an attempt at the correct binomial coefficient "
       r"for their $n$, being combined with the correct power of $ax$",
       r"A1 (AO 1.1b): $\left(1-\frac{x}{4}\right)^{-\frac{1}{2}}=1+\left(-\frac{1}{2}\right)\left(-\frac{x}{4}\right)+"
       r"\frac{\left(-\frac{1}{2}\right)\times\left(-\frac{3}{2}\right)}{2}\left(-\frac{x}{4}\right)^2$. Notes: "
       r"$\left(1-\frac{x}{4}\right)^{-\frac{1}{2}}=1+\left(-\frac{1}{2}\right)\left(-\frac{x}{4}\right)+"
       r"\frac{\left(-\frac{1}{2}\right)\times\left(-\frac{3}{2}\right)}{2}\left(-\frac{x}{4}\right)^2$ unsimplified FYI "
       r"the simplified form is $1+\frac{x}{8}+\frac{3x^2}{128}$ Accept the terms with commas between.",
       r"A1 (AO 1.1b): $\frac{1}{\sqrt{4-x}}=\frac{1}{2}+\frac{1}{16}x+\frac{3}{256}x^2$. Notes: "
       r"$\frac{1}{\sqrt{4-x}}=\frac{1}{2}+\frac{1}{16}x+\frac{3}{256}x^2$ Ignore subsequent terms. Allow with commas "
       r"between.",
       r"ALT: Note: Alternatively $(4-x)^{-\frac{1}{2}}=4^{-\frac{1}{2}}+\left(-\frac{1}{2}\right)4^{-\frac{3}{2}}(-x)+"
       r"\frac{\left(-\frac{1}{2}\right)\left(-\frac{3}{2}\right)}{2}4^{-\frac{5}{2}}(-x)^2+\ldots$ — M1: For "
       r"$4^{-\frac{1}{2}}+\ldots$",
       r"ALT: Note: Alternatively — M1: As above but allow slips on the sign of $x$ and the value of $n$",
       r"ALT: Note: Alternatively — A1: Correct unsimplified (as above)",
       r"ALT: Note: Alternatively — A1: As main scheme"],
      False, 8),
    e("04bi", "4(b)(i)", SEQ, "4.1", 1, LATEX["04bi"],
      [r"B1 (AO 2.4): States $x=-14$ and gives a valid reason. Eg explains that the expansion is not valid for $|x|>4$. "
       r"Notes: (b) Any evaluations of the expansions are irrelevant. Look for a suitable value and a suitable reason for "
       r"both parts. Requires $x=-14$ with a suitable reason. Eg. $x=-14$ as the expansion is only valid for $|x|<4$ or "
       r"equivalent. Eg ‘$x=-14$ as $|-14|>4$’ or ‘I cannot use $x=-14$ as $\left|\frac{-14}{4}\right|>1$’ Eg. "
       r"‘$x=-14$ as is outside the range $|x|<4$’ Do not allow ‘$-14$ is too big’ or ‘$x=-14,|x|<4$’ either way around "
       r"without some reference to the validity of the expansion."],
      False, 8),
    e("04bii", "4(b)(ii)", SEQ, "4.1", 1, LATEX["04bii"],
      [r"B1 (AO 2.4): States $x=-\frac{1}{2}$ and gives a valid reason. Eg. explains that it is closest to zero. Notes: (b) "
       r"Any evaluations of the expansions are irrelevant. Look for a suitable value and a suitable reason for both "
       r"parts. Requires $x=-\frac{1}{2}$ with a suitable reason. Eg. $x=-\frac{1}{2}$ as it is ‘the smallest/smaller "
       r"value’ or ‘$x=-\frac{1}{2}$ as the value closest to zero’ (that will give the more accurate approximation). The "
       r"bracketed statement is not required."],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", ALG, "2.3", 3, LATEX["05a"],
      [r"B1 (AO 1.1b): $2x^2+4x+9=2(x\pm k)^2\pm\ldots$ $a=2$. Notes: Achieves $2x^2+4x+9=2(x\pm k)^2\pm\ldots$ or states "
       r"that $a=2$",
       r"M1 (AO 1.1b): Full method $2x^2+4x+9=2(x+1)^2\pm\ldots$ $a=2$ & $b=1$. Notes: Deals correctly with first two "
       r"terms of $2x^2+4x+9$. Scored for $2x^2+4x+9=2(x+1)^2\pm\ldots$ or stating that $a=2$ and $b=1$",
       r"A1 (AO 1.1b): $2x^2+4x+9=2(x+1)^2+7$. Notes: $2x^2+4x+9=2(x+1)^2+7$ Note that this may be done in a variety of "
       r"ways including equating $2x^2+4x+9$ with the expanded form of $a(x+b)^2+c\equiv ax^2+2abx+ab^2+c$"],
      False, 10),
    e("05b", "5(b)", ALG, "2.3, 2.7", 3, LATEX["05b"],
      [r"B1 (AO 1.2): U shaped curve any position but not through (0,0) [Sketch: a U-shaped parabola with its minimum at "
       r"$(-1,7)$ and $y$-intercept at $(0,9)$.] Notes: For a U-shaped curve in any position not passing through $(0,0)$. "
       r"Be tolerant of slips of the pen but do not allow if the curve bends back on itself",
       r"B1 (AO 1.1b): $y$ - intercept at $(0,9)$. Notes: A curve with a $y$ - intercept on the +ve $y$ axis of 9. The "
       r"curve cannot just stop at $(0,9)$ Allow the intercept to be marked 9, $(0,9)$ but not $(9,0)$",
       r"B1ft (AO 2.2a): Minimum at $(-1,7)$. Notes: For a minimum at $(-1,7)$ in quadrant 2. This may be implied by $-1$ "
       r"and 7 marked on the axes in the correct places. The curve must be a U shape and not a cubic say. Follow through "
       r"on a minimum at $(-b,c)$, marked in the correct quadrant, for their $a(x+b)^2+c$"],
      False, 10),
    e("05c", "5(c)", ALG, "2.9, 2.3", 4, LATEX["05c"],
      [r"M1 (AO 3.1a): (i) Deduces translation with one correct aspect. Notes: Deduces translation with one correct aspect "
       r"or states $\begin{pmatrix}2\\-4\end{pmatrix}$ with no reference to ‘translate’. Allow instead of the word "
       r"translate, shift or move. $\mathrm{g}(x)=\mathrm{f}(x-2)-4$ can score M1 For example, possible methods of "
       r"arriving at this deduction are: • $\mathrm{f}(x)\to\mathrm{g}(x)$ is $2x^2+4x+9\to2(x-2)^2+4(x-2)+5$ So "
       r"$\mathrm{g}(x)=\mathrm{f}(x-2)-4$ • $\mathrm{g}(x)=2(x-1)^2+3$ New curve has its minimum at $(1,3)$ so "
       r"$(-1,7)\to(1,3)$ • Using a graphical calculator to sketch $y=\mathrm{g}(x)$ and compares to the sketch of "
       r"$y=\mathrm{f}(x)$ In almost all cases you will not allow if the candidate gives two different types of "
       r"transformations. Eg, stretch and .....",
       r"A1 (AO 2.2a): Translate $\begin{pmatrix}2\\-4\end{pmatrix}$. Notes: Requires both ‘translate’ and "
       r"‘$\begin{pmatrix}2\\-4\end{pmatrix}$’ Allow ‘shift’ or move’ instead of translate. So condone “ Move shift 2 "
       r"(units) to the right and move 4 (units) down However, for M1 A1, it is possible to reflect in $x=0$ and "
       r"translate $\begin{pmatrix}0\\-4\end{pmatrix}$, so please consider all responses. SC: If the candidate writes "
       r"translate $\begin{pmatrix}-2\\4\end{pmatrix}$ or “ move 2 (units) to the left and 4 (units) up” score M1 A0",
       r"M1 (AO 3.1a): (ii) $\mathrm{h}(x)=\frac{21}{\text{“}2(x+1)^2+7\text{”}}\Rightarrow$ (maximum) value "
       r"$\frac{21}{\text{“}7\text{”}}(=3)$. Notes: Correct attempt at finding the maximum value (although it may not be "
       r"stated as a maximum) • Uses part (a) to write $\mathrm{h}(x)=\frac{21}{\text{“}2(x+1)^2+7\text{”}}$ and attempts "
       r"to find $\frac{21}{\text{their “}7\text{”}}$ • Attempts to differentiate, sets $4x+4=0\to x=-1$ and substitutes "
       r"into $\mathrm{h}(x)=\frac{21}{2x^2+4x+9}$ • Uses a graphical calculator to sketch $y=\mathrm{h}(x)$ and "
       r"establishes the ‘maximum’ value $(\ldots,3)$",
       r"A1ft (AO 1.1b): $0<\mathrm{h}(x)\leqslant3$. Notes: $0<\mathrm{h}(x)\leqslant3$ Allow for "
       r"$0<\mathrm{h}\leqslant3$ $(0,3]$ and $0<y\leqslant3$ but not $0<x\leqslant3$ Follow through on their "
       r"$a(x+b)^2+c$ so award for $0<\mathrm{h}(x)\leqslant\frac{21}{c}$"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", TRIG, "5.7, 5.5, 5.6", 6, LATEX["06a"],
      [r"M1 (AO 3.1a): $5\sin2\theta=9\tan\theta\Rightarrow10\sin\theta\cos\theta=9\times\frac{\sin\theta}{\cos\theta}$ "
       r"$A\cos^2\theta=B$ or $C\sin^2\theta=D$ or $P\cos^2\theta\sin\theta=Q\sin\theta$. Notes: Scored for the whole "
       r"strategy of attempting to form an equation in one function of the form given in the scheme. For this to be "
       r"awarded there must be an attempt at using $\sin2\theta=\ldots\sin\theta\cos\theta$, "
       r"$\tan\theta=\frac{\sin\theta}{\cos\theta}$ and possibly $\pm1\pm\sin^2\theta=\pm\cos^2\theta$ to form an equation "
       r"in one “function” usually $\sin^2\theta$ or $\cos^2\theta$ Allow for this mark equations of the form "
       r"$P\cos^2\theta\sin\theta=Q\sin\theta$ oe",
       r"A1 (AO 1.1b): For a correct simplified equation in one trigonometric function Eg $10\cos^2\theta=9$ "
       r"$10\sin^2\theta=1$ oe. Notes: Uses the correct identities $\sin2\theta=2\sin\theta\cos\theta$ and "
       r"$\tan\theta=\frac{\sin\theta}{\cos\theta}$ to form a correct simplified equation in one trigonometric function. "
       r"It is usually one of the equations given in the scheme, but you may see equivalent correct equations such as "
       r"$10=9\sec^2\theta$ which is acceptable, but in almost all cases it is for a correct equation in $\sin\theta$ or "
       r"$\cos\theta$",
       r"dM1 (AO 2.1): Correct order of operations For example $10\cos^2\theta=9\Rightarrow\theta=\arccos(\pm)"
       r"\sqrt{\frac{9}{10}}$. Notes: Uses the correct order of operations for their equation, usually in terms of just "
       r"$\sin\theta$ or $\cos\theta$, to find at least one value for $\theta$ (Eg. square root before invcos). It is "
       r"dependent upon the previous M. Note that some candidates will use $\cos^2\theta=\frac{\pm\cos2\theta\pm1}{2}$ and "
       r"the same rules apply. Look for correct order of operations.",
       r"A1 (AO 1.1b): Any one of the four values awrt $\theta=\pm18.4^\circ,\pm161.6^\circ$. Notes: Any one of the four "
       r"values awrt $\pm18.4^\circ,\pm161.6^\circ$. Allow 0.32 (rad) or 2.82 (rad)",
       r"A1 (AO 1.1b): All four values $\theta=$ awrt $\pm18.4^\circ,\pm161.6^\circ$. Notes: All four values awrt "
       r"$\pm18.4^\circ,\pm161.6^\circ$ and no other values apart from $0^\circ,\pm180^\circ$",
       r"B1 (AO 1.1b): $\theta=0^\circ,\pm180^\circ$. Notes: $\theta=0^\circ,\pm180^\circ$ This can be scored independent "
       r"of method."],
      False, 14),
    e("06b", "6(b)", TRIG, "5.7, 2.9", 2, LATEX["06b"],
      [r"M1 (AO 1.1b): Attempts to solve $x-25^\circ=-18.4^\circ$. Notes: Attempts to solve "
       r"$x-25^\circ=\text{“}\theta\text{”}$ where $\theta$ is a solution of their part (a)",
       r"A1ft (AO 2.2a): $x=6.6^\circ$. Notes: For awrt $x=6.6^\circ$ but you may ft on their $\theta+25^\circ$ where "
       r"$-25<\theta<0$ If multiple answers are given, the correct value for their $\theta$ must be chosen"],
      False, 14),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", EXP, "6.7", 4, LATEX["07a"],
      [r"M1 (AO 3.3): Uses a model $V=A\mathrm{e}^{\pm kt}$ oe (See next page for other suitable models). Notes: (a) "
       r"Option 1 For $V=A\mathrm{e}^{\pm kt}$ Do not allow if $k$ is fixed, eg $k=-0.5$ Condone different variables "
       r"$V\leftrightarrow y$ $t\leftrightarrow x$ for this mark, but for A1 $V$ and $t$ must be used.",
       r"M1 (AO 1.1b): Eg. Substitutes $t=0,V=20\,000\Rightarrow A=20\,000$. Notes: Substitutes $t=0\Rightarrow "
       r"A=20\,000$ into their exponential model Candidates may start by simply writing $V=20000\mathrm{e}^{kt}$ which "
       r"would be M1 M1",
       r"dM1 (AO 3.1b): Eg. Substitutes $t=1,V=16\,000\Rightarrow16\,000=20\,000\mathrm{e}^{-1k}\Rightarrow k=\ldots$ "
       r"Notes: Substitutes $t=1\Rightarrow16\,000=20\,000\mathrm{e}^{-1k}\Rightarrow k=\ldots$ via the correct use of "
       r"logs. It is dependent upon both previous M’s.",
       r"A1 (AO 1.1b): $V=20000\mathrm{e}^{-0.223t}$. Notes: $V=20000\mathrm{e}^{-0.223t}$ (with accuracy to at least 3sf) "
       r"or $V=20000\mathrm{e}^{t\ln0.8}$ A correct linking formula with correct constants must be seen somewhere in the "
       r"question",
       rf"{OPT2} — M1: For $V=Ar^t$ or equivalent such as $V=kr^{{t-1}}$ Condone different variables $V\leftrightarrow y$ "
       rf"$t\leftrightarrow x$ for this mark, but for A1 $V$ and $t$ must be used.",
       rf"{OPT2} — M1: Uses $t=0\Rightarrow A=20\,000$ in their model. Alternatively uses $(0,20000)$ and $(1,16000)$ to "
       rf"give $r=\frac{{4}}{{5}}$ oe You may award if one of the number pair $(0,20000)$ or $(1,16000)$ works in an "
       rf"allowable model",
       rf"{OPT2} — dM1: $t=1\Rightarrow16\,000=20\,000r^1\Rightarrow r=\ldots$ Dependent upon both previous M’s In the "
       rf"alternative it would be for using $r=\frac{{4}}{{5}}$ with one of the points to find $A=20\,000$ You may award "
       rf"if both number pairs $(0,20000)$ or $(1,16000)$ work in an allowable model",
       rf"{OPT2} — A1: $V=20000\times0.8^t$ Note that $V=20000\times1.25^{{-t}}$ $V=16000\times0.8^{{t-1}}$ and is also "
       rf"correct",
       rf"{OPT3} — M1: They may suggest an exponential model with a lower bound. For example, for "
       rf"$V=A\mathrm{{e}}^{{\pm kt}}+2000$ The bound must be stated but do not allow k to be fixed . Allow as long as the "
       rf"bound < 10 000",
       rf"{OPT3} — M1: $t=0,V=20\,000\Rightarrow A=18\,000$",
       rf"{OPT3} — dM1: $t=1,V=16\,000\Rightarrow16\,000=2\,000+18\,000\mathrm{{e}}^k\Rightarrow k=\ldots$ Dependent upon "
       rf"both previous M’s",
       rf"{OPT3} — A1: $V=18\,000\times\mathrm{{e}}^{{-0.251t}}+2\,000$",
       r"ALT: It is entirely possible that they start part (a) from a differential equation. — M1: "
       r"$\frac{\mathrm{d}V}{\mathrm{d}t}=kV\Rightarrow\int\frac{\mathrm{d}V}{V}=\int k\,\mathrm{d}t\Rightarrow\ln V=kt+c$",
       r"ALT: From a differential equation — M1: $\ln20000=c$",
       r"ALT: From a differential equation — dM1: Using $t=1,V=16\,000\Rightarrow k=\ldots$",
       r"ALT: From a differential equation — A1: $\ln V=-\ln\left(\frac{5}{4}\right)t+\ln20000$"],
      False, 18),
    e("07b", "7(b)", EXP, "6.7, 2.11", 2, LATEX["07b"],
      [r"M1 (AO 3.4): Substitutes $t=10$ in their $V=20000\mathrm{e}^{-0.223t}\Rightarrow V=$ (£2150). Notes: Uses a model "
       r"of the form $V=A\mathrm{e}^{\pm kt}$ to find the value of $V$ when $t=10$.",
       r"A1 (AO 3.5a): Eg. The model is reliable as £2150 ≈ £2000. Notes: This can only be scored from an acceptable model "
       r"with correct constants with accuracy to at least 2sf . Compares $V=$ (£) 2150 with (£) 2 000 and states “reliable "
       r"as 2150 ≈ 2000 ” or “reasonably good as they are close” or “OK but a little high”. Allow a candidate to argue "
       r"that it is unreliable as long as they state a suitable reason. Eg. “It is too far away from £2000” or “It is "
       r"over £100 away, so it is not good” Do not allow “it is not a good model because it is not the same”",
       r"ALT: Option 1, alternatively — M1: Alternatively substitutes $V=2000$ into their model and finds $t$",
       r"ALT: Option 1, alternatively — A1: In the alternative it is for comparing their value of $t$ with 10 and making a "
       r"suitable comment as to the reliability of their model with a reason. $V=20000\mathrm{e}^{-0.223t}\Rightarrow2000="
       r"20000\mathrm{e}^{-0.223t}\Rightarrow t=10.3$ years. Deduction Reliable model as the time is approximately the same "
       r"as 10 years. A candidate can argue that the model is unreliable if they can give a suitable reason.",
       rf"{OPT2} — M1: Uses a model of the form $V=Ar^t$ oe to find the value of $V$ when $t=10$. Eg. "
       rf"$20000\times0.8^{{10}}$ Alternatively substitutes $V=2000$ into their model and finds $t$",
       rf"{OPT2} — A1: This can only be scored from an acceptable model with correct constants also allowing an accuracy "
       rf"to 2sf. Compares (£) 2147 with (£) 2 000 and states “reliable as 2147 ≈ 2000 ” or “reasonably good as they are "
       rf"close” or “OK but a little high”. Allow a candidate to argue that it is unreliable as long as they state a "
       rf"suitable reason. Eg. “It is too far away from £2000” or “It is over £100 away, so it is not good” Do not allow "
       rf"“it is not a good model because it is not the same”",
       rf"{OPT3} — M1: Uses their model to find the value of $V$ when $t=10$. Alternatively substitutes $V=2000$ into their "
       rf"model and finds $t$",
       rf"{OPT3} — A1: For $V=18\,000\times\mathrm{{e}}^{{-0.251\times10}}+2\,000=$ £3462.83 Deduction: Unreliable model "
       rf"as £3462.83 is not close to £2 000 This can only be scored from an acceptable model with correct constants"],
      False, 18),
    e("07c", "7(c)", EXP, "6.7, 2.11", 1, LATEX["07c"],
      [r"B1ft (AO 3.3): Make the “$-0.223$” less negative. Notes: For a correct statement. Eg states that the value of "
       r"their ‘$-0.223$’ should become less negative. Condone the fact that they don’t state their $-0.223$ doesn’t lie "
       r"in the range $(-0.223,0)$",
       r"ALT: Alt — B1ft (AO 3.3): Adapt model to for example $V=18000\mathrm{e}^{-0.223t}+2000$",
       r"ALT: Alt — B1ft (AO 3.3): Alt states that the value of their ‘0.223’ should become smaller. If they refer to $k$ "
       r"then refer to the model and apply the same principles.",
       rf"{OPT2} — B1ft: States a value of $r$ in the range $(0.8,1)$ or states would increase the value of “0.8” They do "
       rf"not need to state that “0.8” must lie in the range $(0.8,1)$ Condone increase the 0.8. Also allow decrease the "
       rf"“1.25” for $V=20000\times1.25^{{-t}}$",
       rf"{OPT3} — B1: States make the value of $k$ or the $-0.251$ greater (or less negative) so that it lies in the range "
       rf"$(-0.251,0)$ Condone ‘make the value of $k$ or the $-0.251$ greater (or less negative)’"],
      False, 18),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", INT, "8.3", 4, LATEX["08a"],
      [r"B1 (AO 1.1b): $y=x(x+2)(x-4)=x^3-2x^2-8x$. Notes: Expands $x(x+2)(x-4)$ to $x^3-2x^2-8x$ (They may be in a "
       r"different order)",
       rf"M1 (AO 1.1b): $\int x^3-2x^2-8x{DX}\to\frac{{1}}{{4}}x^4-\frac{{2}}{{3}}x^3-4x^2$. Notes: Correct attempt at "
       rf"integration of their cubic seen in at least two terms. Look for an expansion to a cubic and $x^n\to x^{{n+1}}$ "
       rf"seen at least twice",
       rf"dM1 (AO 2.2a): Attempts area using the correct strategy $\int_{{-2}}^0y{DX}$. Notes: For a correct strategy to "
       rf"find the area of $R_1$ It is dependent upon the previous M and requires a substitution of $-2$ into $\pm$ their "
       rf"integrated function. The limit of 0 may not be seen. Condone $\left[\frac{{1}}{{4}}x^4-\frac{{2}}{{3}}x^3-4x^2"
       rf"\right]_{{-2}}^0=\frac{{20}}{{3}}$ oe for this mark",
       r"A1* (AO 2.1): $\left[\frac{1}{4}x^4-\frac{2}{3}x^3-4x^2\right]_{-2}^0=(0)-\left(4-\frac{-16}{3}-16\right)="
       r"\frac{20}{3}$ *. Notes: For a rigorous argument leading to area of $R_1=\frac{20}{3}$ For this to be awarded the "
       r"integration must be correct and the limits must be the correct way around and embedded or calculated values "
       r"must be seen. Eg. Look for $-\left(4+\frac{16}{3}-16\right)$ or $-\left(\frac{1}{4}(-2)^4-\frac{2}{3}(-2)^3-"
       r"4(-2)^2\right)$ oe before you see the $\frac{20}{3}$ Note: It is possible to do this integration by parts."],
      True, 22),
    e("08b", "8(b)", INT, "8.3, 2.6", 4, LATEX["08b"],
      [r"M1 (AO 1.1b): For setting ‘their’ $\frac{1}{4}b^4-\frac{2}{3}b^3-4b^2=\pm\frac{20}{3}$. Notes: For setting their "
       r"$\frac{1}{4}b^4-\frac{2}{3}b^3-4b^2=\pm\frac{20}{3}$ or $\left[\frac{1}{4}x^4-\frac{2}{3}x^3-4x^2\right]_{-2}^b=0$",
       r"A1 (AO 2.2a): For correctly deducing that $3b^4-8b^3-48b^2+80=0$. Notes: Deduces that $3b^4-8b^3-48b^2+80=0$. "
       r"Terms may be in a different order but expect integer coefficients. It must have followed "
       r"$\frac{1}{4}b^4-\frac{2}{3}b^3-4b^2=-\frac{20}{3}$ oe. Do not award this mark for "
       r"$\frac{1}{4}b^4-\frac{2}{3}b^3-4b^2+\frac{20}{3}=0$ unless they attempt the second part of this question by "
       r"expansion and then divide the resulting expanded expression by 12",
       r"M1 (AO 1.1b): Attempts to factorise $3b^4-8b^3-48b^2\pm80=(b+2)(b+2)(3b^2\ldots b\ldots20)$. Notes: Attempts to "
       r"factorise $3b^4-8b^3-48b^2\pm80=(b+2)(b+2)(3b^2\ldots b\ldots20)$ via repeated division or inspection. FYI "
       r"$3b^4-8b^3-48b^2+80=(b+2)(3b^3-14b^2-20b+40)$ Allow an attempt via inspection "
       r"$3b^4-8b^3-48b^2\pm80=(b^2+4b+4)(3b^2\ldots b\ldots20)$ but do not allow candidates to just write out "
       r"$3b^4-8b^3-48b^2+80=(b+2)^2(3b^2-20b+20)$ which is really just copying out the given answer.",
       r"A1* (AO 2.1): Achieves $(b+2)^2(3b^2-20b+20)=0$ with no errors. Notes: Correctly reaches "
       r"$(b+2)^2(3b^2-20b+20)=0$ with no errors and must have $=0$",
       r"ALT: Alternatively — M1 (AO 1.1b): Alternatively attempts to expand $(b+2)^2(3b^2-20b+20)$ achieving terms of a "
       r"quartic expression",
       r"ALT: Alternatively — A1* (AO 2.1): In the alternative obtains both equations in the same form and states that "
       r"they are same. Allow ✓ QED etc here."],
      True, 22),
    e("08c", "8(c)", INT, "8.3", 2, LATEX["08c"],
      [r"B1 (AO 1.1b): [Sketch: the cubic with a vertical line to the right of 4 and the regions between the curve and "
       r"the $x$-axis shaded.] States that between $x=-2$ and $x=5.442$ the area above the $x$-axis = area below the "
       r"$x$-axis. Notes: Please watch for candidates who answer this on Figure 2 which is fine Sketches the curve and a "
       r"vertical line to the right of 4 ($x=5.442$ may not be labelled.)",
       r"B1 (AO 2.4): States that between $x=-2$ and $x=5.442$ the area above the $x$-axis = area below the $x$-axis. "
       r"Notes: Explains that (between $x=-2$ and $x=5.442$ ) the area above the $x$-axis = area below the $x$ -axis with "
       r"appropriate areas shaded or labelled. Another correct statement is that the net area between 0 and 5.442 is "
       r"$-\frac{20}{3}$ Look carefully at what is written. There are many correct statements/ deductions. Eg. “ (area "
       r"between 0 and 4) - (area between 4 and 5.442) = 20/3”. Diagram below for your information. [The mark scheme's "
       r"diagram marks $R_1=\frac{20}{3}$, $R_2=\frac{20}{3}$, $R_3=36.03$ and $R_4=36.03$.]",
       r"ALT: Alternatively — B1 (AO 2.4): Alternatively states that the area between 1.225 and 4 is the same as the area "
       r"between 4 and 5.442"],
      True, 22),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", EXP, "6.4", 3, LATEX["09a"],
      [r"B1 (AO 1.2): States $\log a-\log b=\log\frac{a}{b}$. Notes: States or uses $\log a-\log b=\log\frac{a}{b}$. This "
       r"may be awarded anywhere in the question and may be implied by a starting line of $\frac{a}{b}=a-b$ oe. Watch out "
       r"for $\log a-\log b=\frac{\log a}{\log b}=\log\left(\frac{a}{b}\right)$ which could score 010",
       r"M1 (AO 1.1b): Proceeds from $\frac{a}{b}=a-b\to\ldots\to ab-a=b^2$. Notes: Attempts to make ‘$a$’ the subject. "
       r"Awarded for proceeding from $\frac{a}{b}=a-b$ to a point where the two terms in $a$ are on the same side of the "
       r"equation and the term in $b$ is on the other.",
       r"A1* (AO 2.1): $ab-a=b^2\to a(b-1)=b^2\Rightarrow a=\frac{b^2}{b-1}$ *. Notes: CSO. Shows clear reasoning and "
       r"correct mathematics leading to $a=\frac{b^2}{b-1}$. Bracketing must be correct. Allow a candidate to proceed "
       r"from $ab-a=b^2$ to $a=\frac{b^2}{b-1}$ without the intermediate line.",
       r"ALT: Alternatively — B1 (AO 1.2): Alternatively takes $\log b$ to the rhs and uses the addition law "
       r"$\log(a-b)+\log b=\log(a-b)b$.",
       r"ALT: Alt (a): substituting $a=\frac{b^2}{b-1}$ into both sides of the given identity, $\log a-\log b=\log(a-b)"
       r"\Rightarrow\log\left(\frac{b^2}{b-1}\right)-\log b=\log\left(\frac{b^2}{b-1}-b\right)$ — B1: Score for "
       r"$\log\left(\frac{b^2}{b-1}\right)-\log b=\log\left(\frac{b}{b-1}\right)$",
       r"ALT: Alt (a) — M1: Attempts to write $\frac{b^2}{b-1}-b$ as a single fraction "
       r"$\frac{b^2}{b-1}-b=\frac{b^2-b(b-1)}{b-1}$ Allow as two separate fractions with the same common denominator",
       r"ALT: Alt (a) — A1*: Achieves lhs and rhs as $\log\left(\frac{b}{b-1}\right)$ and makes a comment such as “hence "
       r"true”"],
      False, 26),
    e("09b", "9(b)", EXP, "6.3, 2.5", 2, LATEX["09b"],
      [r"B1 (AO 2.2a): States either $b>1$ or $b\neq1$ with reason $\frac{b^2}{b-1}$ is not defined at $b=1$ oe. Notes: "
       r"For deducing $b\neq1$ as $a\to\infty$ oe such as “you cannot divide by 0” or correctly deducing that $b>1$. They "
       r"may state that $b$ cannot be less than 1.",
       r"B1 (AO 2.4): States $b>1$ and explains that as $a>0\Rightarrow\frac{b^2}{b-1}>0\Rightarrow b>1$. Notes: For $b>1$ "
       r"and explaining that as $a>0\Rightarrow\frac{b^2}{b-1}>0\Rightarrow b>1$ (as $b^2$ is positive) As a minimum "
       r"accept that $b>1$ as $a$ cannot be negative. Note that $a>b>1$ is a correct statement but not sufficient on its "
       r"own without an explanation."],
      False, 26),

    # ---------------- Q10 ----------------
    e("10i", "10(i)", PROOF, "1.1", 4, LATEX["10i"],
      [r"M1 (AO 2.1): Example of an algebraic proof: For $n=2m$, $n^2+2=4m^2+2$. Notes: General points for marking "
       r"question 10 (i): • Students who just try random numbers in part (i) are not going to score any marks. • Students "
       r"can mix and match methods. Eg you may see odd numbers via logic and even via algebra • Students who state "
       r"$4m^2+2$ cannot be divided by (instead of is not divisible by) cannot be awarded credit for the "
       r"accuracy/explanation marks, unless they state correctly that $4m^2+2$ cannot be divided by 4 to give an integer. "
       r"• Students who write $n^2+2=4k\Rightarrow k=\frac{1}{4}n^2+\frac{1}{2}$ which is not a whole number gains no "
       r"credit unless they then start to look at odd and even numbers for instance • Proofs via induction usually tend "
       r"to go nowhere unless they proceed as in the main scheme • Watch for unusual methods that are worthy of credit "
       r"(See below) • If the final conclusion is $n\in\mathbb{R}$ then the final mark is withheld. $n\in\mathbb{Z}^+$ is "
       r"correct Watch for methods that may not be in the scheme that you feel may deserve credit. If you are uncertain "
       r"of a method please refer these up to your team leader. Note that M0 A0 M1 A1 and M0 A0 M1 A0 are not possible "
       r"due to the way the scheme is set up M1: Awarded for setting up the proof for either the even or odd numbers.",
       r"A1 (AO 1.1b): Concludes that this number is not divisible by 4 (as the explanation is trivial). Notes: Concludes "
       r"correctly with a reason why $n^2+2$ cannot be divisible by 4 for either $n$ odd or even.",
       r"dM1 (AO 2.1): For $n=2m+1$, $n^2+2=(2m+1)^2+2=\ldots$ FYI $(4m^2+4m+3)$. Notes: Awarded for setting up the proof "
       r"for both even and odd numbers",
       r"A1* (AO 2.4): Correct working and concludes that this is a number in the 4 times table add 3 so cannot be "
       r"divisible by 4 or writes $4(m^2+m)+3$ ..........AND states ......hence true for all. Notes: Fully correct proof "
       r"with valid explanation and conclusion for all $n$",
       r"ALT: Eg 1. Solving part (i) by modulo arithmetic. [The mark scheme's table: all $n\in\mathbb{N}$ mod 4: 0, 1, 2, "
       r"3; all $n^2\in\mathbb{N}$ mod 4: 0, 1, 0, 1; all $n^2+2\in\mathbb{N}$ mod 4: 2, 3, 2, 3.] Hence for all $n$, "
       r"$n^2+2$ is not divisible by 4.",
       rf"{ALGP} — M1 (AO 2.1): For $n=2m$, $\frac{{4m^2+2}}{{4}}=m^2+\frac{{1}}{{2}}$",
       rf"{ALGP} — A1 (AO 1.1b): Concludes that this is not divisible by 4 due to the $\frac{{1}}{{2}}$ (A suitable reason "
       rf"is required)",
       rf"{ALGP} — dM1 (AO 2.1): For $n=2m+1$, $\frac{{n^2+2}}{{4}}=\frac{{4m^2+4m+3}}{{4}}=m^2+m+\frac{{3}}{{4}}$",
       rf"{ALGP} — A1* (AO 2.4): Concludes that this is not divisible by 4 due to the $\frac{{3}}{{4}}$ ...AND states ...... "
       rf"hence for all $n$, $n^2+2$ is not divisible by 4",
       rf"{LOGP} — M1 (AO 2.1): When $n$ is odd, “odd $\times$odd” = odd",
       rf"{LOGP} — A1 (AO 1.1b): so $n^2+2$ is odd , so (when $n$ is odd) $n^2+2$ cannot be divisible by 4",
       rf"{LOGP} — dM1 (AO 2.1): When $n$ is even, it is a multiple of 2, so “even $\times$even” is a multiple of 4",
       rf"{LOGP} — A1* (AO 2.4): Concludes that when $n$ is even $n^2+2$ cannot be divisible by 4 because $n^2$ is "
       rf"divisible by 4…..AND STATES ……..trues for all $n$.",
       rf"{CONP} — M1 (AO 2.1): Sets up the contradiction ‘Assume that $n^2+2$ is divisible by $4\Rightarrow n^2+2=4k$’",
       rf"{CONP} — A1 (AO 1.1b): $\Rightarrow n^2=4k-2=2(2k-1)$ and concludes even Note that the M mark (for setting up "
       rf"the contradiction must have been awarded)",
       rf"{CONP} — dM1 (AO 2.1): States that $n^2$ is even, then $n$ is even and hence $n^2$ is a multiple of 4",
       rf"{CONP} — A1* (AO 2.4): Explains that if $n^2$ is a multiple of 4 then $n^2+2$ cannot be a multiple of 4 and hence "
       rf"divisible by 4 Hence there is a contradiction and concludes Hence true for all $n$.",
       r"ALT: A similar proof exists via contradiction where — A1: $n^2=2(2k-1)\Rightarrow n=\sqrt{2}\times\sqrt{2k-1}$",
       r"ALT: A similar proof exists via contradiction where — dM1: States that $2k-1$ is odd, so does not have a factor "
       r"of 2, meaning that $n$ is irrational"],
      False, 28),
    e("10ii", "10(ii)", PROOF, "1.1, 2.7", 2, LATEX["10ii"],
      [r"M1 (AO 2.3): Proof using numerical values: SOMETIMES TRUE and chooses any number $x:9.25<x<9.5$ and shows false "
       r"Eg $x=9.4$ $|3x-28|=0.2$ and $x-9=0.4$ ✗. Notes: M1: States or implies ‘sometimes true’ or ‘not always true’ and "
       r"gives an example where it is not true.",
       r"A1 (AO 2.4): Then chooses a number where it is true Eg $x=12$ $|3x-28|=8$ $x-9=3$ ✓. Notes: A1: and gives an "
       r"example where it is true,",
       r"ALT: Graphical Proof — M1 (AO 2.3): States or implies “sometimes true” Sketches both graphs on the same axes. "
       r"Expect shapes and relative positions to be correct. V shape on +ve $x$ -axis Linear graph with +ve gradient "
       r"intersecting twice [The mark scheme's sketch shows the V shape and the line crossing it twice.]",
       r"ALT: Graphical Proof — A1 (AO 2.4): Graphs accurate and explains that as there are points where "
       r"$|3x-28|<x-9$ and points where $|3x-28|>x-9$ oe in words like ‘above’ and ‘below’ or ‘dips below at one point’",
       r"ALT: Proof via algebra — M1 (AO 2.3): States sometimes true and attempts to solve both $3x-28<x-9$ and "
       r"$-3x+28<x-9$ or one of these with the bound $9.\dot{3}$",
       r"ALT: Proof via algebra — A1 (AO 2.4): States that it is false when $9.25<x<9.5$ or $9.25<x<9.\dot{3}$ or "
       r"$9.\dot{3}<x<9.5$",
       r"ALT: Alt: It is possible to find where it is always true — M1 (AO 2.3): States sometimes true and attempts to "
       r"solve where it is just true Solves both $3x-28\geqslant x-9$ and $-3x+28\geqslant x-9$",
       r"ALT: Alt: It is possible to find where it is always true — A1 (AO 2.4): States that it is false when "
       r"$9.25<x<9.5$ or $9.25<x<9.\dot{3}$ or $9.\dot{3}<x<9.5$"],
      False, 28),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", SEQ, "4.6, 4.5", 2, LATEX["11a"],
      [r"M1 (AO 3.4): Total time for 6 km = 24 minutes + $6\times1.05+6\times1.05^2$ minutes. Notes: For using model to "
       r"calculate the total time. Sight of 24 minutes + $6\times1.05+6\times1.05^2$ or equivalent is required. Eg "
       r"$24+6.3+6.615$",
       r"A1* (AO 1.1b): $=36.915$ minutes $=36$ minutes 55 seconds *. Notes: 36 minutes 55 seconds following 36.915, "
       r"$24+6.3+6.615$, $24+6\times1.05+6\times1.05^2$ or equivalent working in seconds",
       r"ALT: Alternatively in seconds — M1 (AO 3.4): Alternatively in seconds 24 minutes + 378 sec (6min 18 s) +396.9 "
       r"(6 min 37 s)"],
      False, 30),
    e("11b", "11(b)", SEQ, "4.5, 4.6", 1, LATEX["11b"],
      [r"B1 (AO 3.4): $5^{\text{th}}$ km is $6\times1.05=6\times1.05^1$ $6^{\text{th}}$ km is "
       r"$6\times1.05\times1.05=6\times1.05^2$ $7^{\text{th}}$ km is $6\times1.05\times1.05\times1.05=6\times1.05^3$ Hence "
       r"the time for the $r^{\text{th}}$ km is $6\times1.05^{r-4}$. Notes: (b) Must be seen in (b) As seen in scheme. For "
       r"making the link between the $r$ th km and the index of 1.05 Or for EXPLAINING that “the time taken per km (6 "
       r"mins) only starts to increase by 5% after the first 4 km”"],
      False, 30),
    e("11c", "11(c)", SEQ, "4.5, 4.6", 4, LATEX["11c"],
      [r"M1 (AO 3.1a): Attempts the total time for the race = Eg. 24 minutes + $\sum_{r=5}^{r=20}6\times1.05^{r-4}$ "
       r"minutes. Notes: The correct sum formula $\frac{a(r^n-1)}{r-1}$, if seen, must be correct in part (c) for all "
       r"relevant marks M1: For the overall strategy of finding the total time. Award for adding 18, 24, 30.3 or awrt 36.9 "
       r"and the sum of a geometric sequence So award the mark for expressions such as $6\times4+\sum6\times1.05^n$ or "
       r"$24+\frac{6(1.05^{20}-1)}{1.05-1}$ The geometric sequence formula, must be used with $r=1.05$ oe but condone "
       r"slips on $a$ and $n$",
       r"M1 (AO 3.4): Uses the series formula to find an allowable sum Eg. Time for 5 th to 20th km "
       r"$=\frac{6.3(1.05^{16}-1)}{1.05-1}=(149.04)$. Notes: For an attempt at using a correct sum formula for a GP to "
       r"find an allowable sum The value of $r$ must be 1.05 oe such as 105% but you should allow a slip on the value of "
       r"$n$ used for their value of $a$ (See below: We are going to allow the correct value of $n$ or one less) If you "
       r"don’t see a calculation it may be implied by sight of one of the values seen below Allow for $a=6$, $n=17$ or 16 "
       r"Eg. $\frac{6(1.05^{17}-1)}{1.05-1}=(155.0)$ or $\frac{6(1.05^{16}-1)}{1.05-1}=(141.9)$ Allow for $a=6.3,n=16$ or "
       r"15 Eg $\frac{6.3(1.05^{16}-1)}{1.05-1}=(149.0)$ or $\frac{6.3(1.05^{15}-1)}{1.05-1}=(135.9)$ Allow for "
       r"$a=6.615$, $n=15$ or 14 Eg $\frac{6.615(1.05^{15}-1)}{1.05-1}=(142.7)$ or "
       r"$\frac{6.615(1.05^{14}-1)}{1.05-1}=(129.6)$",
       r"A1 (AO 1.1b): Correct calculation that leads to the total time Eg. Total time "
       r"$=24+\frac{6.3(1.05^{16}-1)}{1.05-1}$. Notes: For a correct calculation that will find the total time. It does "
       r"not need to be processed Allow for example, amongst others, $24+\frac{6.3(1.05^{16}-1)}{1.05-1}$, "
       r"$18+\frac{6(1.05^{17}-1)}{1.05-1}$, $30.3+\frac{6.615(1.05^{15}-1)}{1.05-1}$",
       r"A1 (AO 1.1b): Total time = awrt 173 minutes and 3 seconds. Notes: For a total time of awrt 173 minutes and 3 "
       r"seconds This answer alone can be awarded 4 marks as long as there is some evidence of where it has come from.",
       r"ALT: Candidates that list values — M1: For a correct overall strategy which would involve adding four sixes "
       r"followed by at least 16 other values The values which may be written in the form $6\times1.05^2$ or as numbers "
       r"Can be implied by $6+6+6+6+(6\times1.05)+\ldots+(6\times1.05^{16})$ [The mark scheme gives a table of the time "
       r"per km and total time for each km, ending at 13.0972 and 173.0422 for the 20th km.]",
       r"ALT: Candidates that list values — M1: For an attempt to add the numbers from $(6\times1.05)$ to "
       r"$(6\times1.05^{16})$. This could be done on a calculator in which case expect to see awrt 149 Alternatively, if "
       r"written out, look for 16 values with 8 correct or follow through correct to 1 dp",
       r"ALT: Candidates that list values — A1: Awrt 173 minutes",
       r"ALT: Candidates that list values — A1: Awrt 173 minutes and 3 seconds"],
      False, 30),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", DIFF, "7.4", 4, LATEX["12a"],
      [r"M1 (AO 1.1b): $\Rightarrow\mathrm{f}'(x)=-2.5\mathrm{e}^{-0.25x}\sin x+10\mathrm{e}^{-0.25x}\cos x$ oe. Notes: For "
       r"attempting to differentiate using the product rule condoning slips, for example the power of e . So for example "
       r"score expressions of the form $\pm\ldots\mathrm{e}^{-0.25x}\sin x\pm\ldots\mathrm{e}^{-0.25x}\cos x$ M1 Sight of "
       r"$vdu-udv$ however is M0",
       r"A1 (AO 1.1b): $\Rightarrow\mathrm{f}'(x)=-2.5\mathrm{e}^{-0.25x}\sin x+10\mathrm{e}^{-0.25x}\cos x$ oe. Notes: "
       r"$\mathrm{f}'(x)=-2.5\mathrm{e}^{-0.25x}\sin x+10\mathrm{e}^{-0.25x}\cos x$ which may be unsimplified",
       r"M1 (AO 2.1): $\mathrm{f}'(x)=0\Rightarrow-2.5\mathrm{e}^{-0.25x}\sin x+10\mathrm{e}^{-0.25x}\cos x=0$ [the "
       r"$\mathrm{e}^{-0.25x}$ factors are struck through]. Notes: For clear reasoning in setting their $\mathrm{f}'(x)=0$, "
       r"factorising/ cancelling out the $\mathrm{e}^{-0.25x}$ term leading to a trigonometric equation in only $\sin x$ "
       r"and $\cos x$ Do not allow candidates to substitute $x=\arctan4$ into $\mathrm{f}'(x)$ to score this mark.",
       r"A1* (AO 1.1b): $\frac{\sin x}{\cos x}=\frac{10}{2.5}\Rightarrow\tan x=4$*. Notes: Shows the steps "
       r"$\frac{\sin x}{\cos x}=\frac{10}{2.5}$ or equivalent leading to $\Rightarrow\tan x=4$*. $\frac{\sin x}{\cos x}$ "
       r"must be seen."],
      False, 34),
    e("12b", "12(b)", ALG, "2.7, 2.9", 2, LATEX["12b"],
      [r"M1 (AO 1.1b): “Correct” shape for 2 loops [Sketch: $H$ against $t$, a row of arches sitting on the $t$-axis with "
       r"decreasing heights.] Notes: Draws at least two “loops”. The height of the second loop should be lower than the "
       r"first loop. Condone the sight of rounding where there should be cusps",
       r"A1 (AO 1.1b): Fully correct with decreasing heights. Notes: At least 4 loops with decreasing heights and no "
       r"rounding at the cusps. The intention should be that the graph should ‘sit’ on the $x$ -axis but be tolerant. It "
       r"is possible to overwrite Figure 3, but all loops must be clearly seen."],
      True, 34),
    e("12c", "12(c)", DIFF, "7.3, 2.11", 3, LATEX["12c"],
      [r"M1 (AO 3.1a): Solves $\tan x=4$ and substitutes answer into $H(t)$. Notes: Understands that to solve the problem "
       r"they are required to substitute an answer to $\tan t=4$ into $H(t)$ This can be awarded for an attempt to "
       r"substitute $t=$ awrt 1.33 or $t=$ awrt 4.47 into $H(t)$ $H(t)=6.96$ implies the use of $t=1.33$ Condone for this "
       r"mark only, an attempt to substitute $t=$ awrt $76^\circ$ or awrt $256^\circ$ into $H(t)$",
       r"M1 (AO 1.1b): $H(4.47)=\left|10\mathrm{e}^{-0.25\times4.47}\sin4.47\right|$. Notes: Substitutes $t=$ awrt 4.47 "
       r"into $H(t)=\left|10\mathrm{e}^{-0.25t}\sin t\right|$. Implied by awrt 3.2",
       r"A1 (AO 3.2a): awrt 3.18 (metres). Notes: Awrt 3.18 metres. Condone the lack of units. If two values are given the "
       r"correct one must be seen to have been chosen It is possible for candidates to sketch this on their graphical "
       r"calculators and gain this answer. If there is no incorrect working seen and 3.18 is given, then award 111 for "
       r"such an attempt."],
      True, 34),
    e("12d", "12(d)", ALG, "2.11", 1, LATEX["12d"],
      [r"B1 (AO 3.5b): The times between each bounce should not stay the same when the heights of each bounce is getting "
       r"smaller. Notes: Makes reference to the fact that the time between each bounce should not stay the same when the "
       r"heights of each bounce is getting smaller. Look for “ time (or gap) between the bounces will change” ‘bounces "
       r"would not be equal times apart’ ‘bounces would become more frequent’ But do not accept ‘the times between each "
       r"bounce would be longer or slower’ Do not accept explanations such as there are other factors that would affect "
       r"this such as “wind resistance”, friction etc"],
      True, 34),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", ALG, "2.7", 3, LATEX["13a"],
      [r"B1* (AO 2.4): (i) Explains $2x-q=0$ when $x=2$ oe Hence $q=4$ *. Notes: Is able to link $2x-q=0$ and $x=2$ to "
       r"explain why $q=4$ Eg “The asymptote $x=2$ is where $2x-q=0$ so $4-q=0\Rightarrow q=4$” “The curve is not defined "
       r"when $2\times2-q=0\Rightarrow q=4$” There must be some words explaining why $q=4$ and in most cases, you should "
       r"see a reference to either “the asymptote $x=2$”, “the curve is not defined at $x=2$”, ‘the denominator is 0 at "
       r"$x=2$’",
       r"M1 (AO 1.1b): (ii) Substitutes $\left(3,\frac{1}{2}\right)$ into $y=\frac{p-3x}{(2x-4)(x+3)}$ and solves. Notes: "
       r"Substitutes $\left(3,\frac{1}{2}\right)$ into $y=\frac{p-3x}{(2x-4)(x+3)}$ and solves",
       r"A1* (AO 2.1): $\frac{1}{2}=\frac{p-9}{(2)\times(6)}\Rightarrow p-9=6\Rightarrow p=15$*. Notes: Full proof showing "
       r"all necessary steps $\frac{1}{2}=\frac{p-9}{(2)\times(6)}\Rightarrow p-9=6\Rightarrow p=15$",
       r"ALT: Alternatively — M1 (AO 1.1b): Alternatively substitutes $\left(3,\frac{1}{2}\right)$ into "
       r"$y=\frac{15-3x}{(2x-4)(x+3)}$ and shows $\frac{1}{2}=\frac{6}{(2)\times(6)}$ oe",
       r"ALT: Alternatively — A1* (AO 2.1): In the alternative there would have to be some recognition that these are "
       r"equal eg ✓ hence $p=15$"],
      False, 38),
    e("13b", "13(b)", INT, "8.6, 2.10, 8.3", 8, LATEX["13b"],
      [r"M1 (AO 3.1a): Attempts to write $\frac{15-3x}{(2x-4)(x+3)}$ in PF’s and integrates using lns between 3 and "
       r"another value of $x$. Notes: Scored for an overall attempt at using PF’s and integrating with lns seen with "
       r"sight of limits 3 and another value of $x$.",
       r"M1 (AO 1.1b): $\frac{15-3x}{(2x-4)(x+3)}=\frac{A}{(2x-4)}+\frac{B}{(x+3)}$ leading to $A$ and $B$. Notes: "
       r"$\frac{15-3x}{(2x-4)(x+3)}=\frac{A}{(2x-4)}+\frac{B}{(x+3)}$ leading to $A$ and $B$",
       r"A1 (AO 1.1b): $\frac{15-3x}{(2x-4)(x+3)}=\frac{1.8}{(2x-4)}-\frac{2.4}{(x+3)}$ or "
       r"$\frac{0.9}{(x-2)}-\frac{2.4}{(x+3)}$ oe. Notes: $\frac{15-3x}{(2x-4)(x+3)}=\frac{1.8}{(2x-4)}-"
       r"\frac{2.4}{(x+3)}$, or for example $\frac{0.9}{(x-2)}-\frac{2.4}{(x+3)}$, $\frac{9}{(10x-20)}-\frac{12}{(5x+15)}$ "
       r"oe Must be written in PF form, not just for correct $A$ and $B$",
       rf"M1 (AO 1.1b): $\mathrm{{I}}=\int\frac{{15-3x}}{{(2x-4)(x+3)}}{DX}=m\ln(2x-4)+n\ln(x+3)+(c)$. Notes: Area "
       rf"$R=\int\frac{{15-3x}}{{(2x-4)(x+3)}}{DX}=m\ln(2x-4)+n\ln(x+3)$ OR $\int\frac{{15-3x}}{{(2x-4)(x+3)}}{DX}="
       rf"m\ln(x-2)+n\ln(x+3)$ Note that $\int\frac{{l}}{{(x-2)}}{DX}\to l\ln(kx-2k)$ and $\int\frac{{m}}{{(x+3)}}{DX}"
       rf"\to m\ln(nx+3n)$",
       rf"A1ft (AO 1.1b): $\mathrm{{I}}=\int\frac{{15-3x}}{{(2x-4)(x+3)}}{DX}=0.9\ln(2x-4)-2.4\ln(x+3)$ oe. Notes: "
       rf"$=\int\frac{{15-3x}}{{(2x-4)(x+3)}}{DX}=0.9\ln(2x-4)-2.4\ln(x+3)$ oe. FT on their $A$ and $B$",
       rf"B1 (AO 2.2a): Deduces that Area Either $\int_3^5\frac{{15-3x}}{{(2x-4)(x+3)}}{DX}$ Or $[\ldots\ldots]_3^5$. "
       rf"Notes: Deduces that the limits for the integral are 3 and 5. It cannot be awarded from 5 being marked on "
       rf"Figure 4. So award for sight of $\int_3^5\frac{{15-3x}}{{(2x-4)(x+3)}}(\mathrm{{d}}x)$ or $[\ldots\ldots]_3^5$ "
       rf"having performed an integral which may be incorrect",
       r"dM1 (AO 2.1): Uses correct ln work seen at least once for $\ln6=\ln2+\ln3$ or $\ln8=3\ln2$ "
       r"$[0.9\ln(6)-2.4\ln(8)]-[0.9\ln(2)-2.4\ln(6)]=3.3\ln6-7.2\ln2-0.9\ln2$. Notes: Uses correct ln work seen at least "
       r"once eg $\ln6=\ln2+\ln3$, $\ln8=3\ln2$ or $m\ln6k-m\ln2k=m\ln3$ This is an attempt to get either of the above "
       r"ln’s in terms of ln2 and/or ln3 It is dependent upon the correct limits and having achieved "
       r"$m\ln(2x-4)+n\ln(x+3)$ oe",
       r"A1 (AO 1.1b): $=3.3\ln3-4.8\ln2$. Notes: $=3.3\ln3-4.8\ln2$ oe"],
      True, 38),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", DIFF, "7.2, 7.4", 2, LATEX["14a"],
      [rf"M1 (AO 1.1b): Attempts to differentiate $x=4\sin2y$ and inverts ${DXY}=8\cos2y\Rightarrow{DY}="
       rf"\frac{{1}}{{8\cos2y}}$. Notes: Attempts to differentiate $x=4\sin2y$ and inverts. Allow for "
       rf"${DXY}=k\cos2y\Rightarrow{DY}=\frac{{1}}{{k\cos2y}}$ or $1=k\cos2y{DY}\Rightarrow{DY}=\frac{{1}}{{k\cos2y}}$ It "
       rf"is possible to approach this from $x=8\sin y\cos y\Rightarrow{DXY}=\pm8\sin^2y\pm8\cos^2y$ before inverting",
       rf"A1 (AO 1.1b): At (0,0) ${DY}=\frac{{1}}{{8}}$. Notes: ${DY}=\frac{{1}}{{8}}$ Allow both marks for sight of this "
       rf"answer as long as no incorrect working is seen (See below) Watch for candidates who reach this answer via "
       rf"${DXY}=8\cos2x\Rightarrow{DY}=\frac{{1}}{{8\cos2x}}$ This is M0 A0",
       rf"ALT: Alternatively — M1 (AO 1.1b): Alternatively, changes the subject and differentiates "
       rf"$x=4\sin2y\to y=\ldots\arcsin\left(\frac{{x}}{{4}}\right)\to{DY}=\frac{{\ldots}}{{\sqrt{{1-\left(\frac{{x}}{{4}}"
       rf"\right)^2}}}}$"],
      False, 42),
    e("14b", "14(b)", TRIG, "5.2", 2, LATEX["14b"],
      [r"B1 (AO 1.1b): (i) Uses $\sin2y\approx2y$ when $y$ is small to obtain $x\approx8y$. Notes: Uses $\sin2y\approx2y$ "
       r"when $y$ is small to obtain $x=8y$ oe such as $x=4(2y)$. Do not allow $\sin2y\approx2\theta$ to get $x=8\theta$ "
       r"but allow recovery in (b)(i) or (b)(ii) Double angle formula is B0 as it does not satisfy the demands of the "
       r"question.",
       rf"B1 (AO 2.4): (ii) The value found in (a) is the gradient of the line found in (b)(i). Notes: Explains the "
       rf"relationship between the answers to (a) and (b) (i). For this to be scored the first three marks, in almost all "
       rf"cases, must have been awarded and the statement must refer to both answers Allow for example “The gradients are "
       rf"the same $\left(=\frac{{1}}{{8}}\right)$” ‘both have $m=\frac{{1}}{{8}}$’ Do not accept the statement that 8 and "
       rf"$\frac{{1}}{{8}}$ are reciprocals of each other unless further correct work explains the relationship in terms "
       rf"of ${DXY}$ and ${DY}$"],
      False, 42),
    e("14c", "14(c)", DIFF, "7.4, 5.5", 3, LATEX["14c"],
      [rf"M1 (AO 2.1): Uses their ${DY}$ as a function of $y$ and, using both $\sin^22y+\cos^22y=1$ and $x=4\sin2y$ in an "
       rf"attempt to write ${DY}$ or ${DXY}$ as a function of $x$ Allow for ${DY}=k\frac{{1}}{{\cos2y}}=\ldots"
       rf"\frac{{1}}{{\sqrt{{1-(\ldots x)^2}}}}$. Notes: Uses their ${DY}$ as a function of $y$ and, using both "
       rf"$\sin^22y+\cos^22y=1$ and $x=4\sin2y$, attempts to write ${DY}$ or ${DXY}$ as a function of $x$. The ${DY}$ may "
       rf"not be seen and may be implied by their calculation.",
       rf"A1 (AO 1.1b): A correct answer ${DY}=\frac{{1}}{{8\sqrt{{1-\left(\frac{{x}}{{4}}\right)^2}}}}$ or "
       rf"${DXY}=8\sqrt{{1-\left(\frac{{x}}{{4}}\right)^2}}$. Notes: A correct (un-simplified) answer for ${DY}$ or "
       rf"${DXY}$ Eg. ${DY}=\frac{{1}}{{8\sqrt{{1-\left(\frac{{x}}{{4}}\right)^2}}}}$",
       rf"A1 (AO 1.1b): and in the correct form ${DY}=\frac{{1}}{{2\sqrt{{16-x^2}}}}$. Notes: "
       rf"${DY}=\frac{{1}}{{2\sqrt{{16-x^2}}}}$ The ${DY}$ must be seen at least once in part (c) of this solution",
       rf"ALT: Alt to (c) using arcsin — M1: Alternatively, changes the subject and differentiates "
       rf"$x=4\sin2y\to y=\ldots\arcsin\left(\frac{{x}}{{4}}\right)\to{DY}=\frac{{\ldots}}{{\sqrt{{1-\left(\frac{{x}}{{4}}"
       rf"\right)^2}}}}$ Condone a lack of bracketing on the $\frac{{x}}{{4}}$ which may appear as $\frac{{x^2}}{{4}}$",
       rf"ALT: Alt to (c) using arcsin — A1: ${DY}=\frac{{1/8}}{{\sqrt{{1-\left(\frac{{x}}{{4}}\right)^2}}}}$ oe",
       rf"ALT: Alt to (c) using arcsin — A1: ${DY}=\frac{{1}}{{2\sqrt{{16-x^2}}}}$"],
      False, 42),
]

# Examiner report, sentence by sentence, in report order (the Introduction and
# the "(Mean Mark ...)" headings are not attached to any question). Bulleted
# lists are joined into the sentence that introduces them, with "; ".
W = None
NO = {"ref": False}
BACK = {"ref": True}
DYS = r"$\mathrm{d}y/\mathrm{d}x$"
REPORT = {
    "01": [
        (W, "This proved to be a very suitable start to the paper.", NO),
        (W, r"Most candidates used the factor theorem and produced an equation in $a$ by setting $\mathrm{f}(-3)=0$."),
        (W, "Most could then solve their linear equation in $a$ to find its value."),
        (W, "Candidates who used this method generally went on to score full marks.", BACK),
        (W, "Common mistakes tended to be arithmetic or sign errors, for example not cubing (-3) accurately in the first "
            "term."),
        (W, "Other methods were seen but were generally less efficient and not as effective."),
        (W, "Those candidates that started with $(x+3)(ax^2+bx+c)$ and equated coefficients were generally successful, "
            "however those candidates that tried to solve this problem using long division generally made errors and did "
            "not score highly.", NO),
        (W, "It was rare to see students scoring zero on this question.", NO),
    ],
    "02": [
        (W, "This question proved to be more challenging for a number of candidates although many were still able to "
            "score full marks."),
        ({"a"}, "In part (a) it was important for candidates to pay attention to the scale of the graph.", NO),
        ({"a"}, "Most candidates who did draw a straight-line graph were able to make the link between one point of "
                "intersection and one real root to the equation, however, a significant minority of these were unable "
                "to construct the correct straight-line graph with enough accuracy to gain both marks for this part of "
                "the question.", NO),
        ({"b"}, r"In part (b) almost all candidates were able to write down the small angle approximation for $\cos x$ "
                r"even if they were unable to use it in order to answer the question.", NO),
        ({"b"}, "Most candidates did substitute correctly into the equation in order to gain a quadratic equation, "
                "although some did contain a mixture of variables."),
        ({"b"}, "Sign errors sometimes occurred at this stage and the weakest candidates were unable to deal correctly "
                "with resulting fractions in order to simplify the equation.", BACK),
        ({"b"}, "Many candidates appear to be using calculators in order to solve quadratics and in this question, this "
                "usually resulted in full marks.", NO),
        ({"b"}, "The final mark was lost by some candidates who correctly solved the quadratic equation but gave both "
                "roots as their final answer."),
    ],
    "03": [
        ({"a"}, "This was an accessible question for most students, but the second half of part (a) did discriminate at "
                "all levels.", NO),
        ({"a"}, "In part (a) students generally recognised the need to use the quotient or product rule and were "
                "successful at differentiating for the first 2 marks."),
        ({"a"}, "The most common mistake was forgetting to square the denominator, with incorrect order of terms in the "
                "numerator being less common."),
        ({"a"}, "Students should also be reminded to quote a formula before attempting to use it, as they may still gain "
                "method marks for this, even if there are slips in its application.", NO),
        ({"a"}, "Omission of brackets in terms in the numerator was also common, but often recovered in working."),
        ({"a"}, "However, it would benefit students to be careful in the use of brackets.", NO),
        ({"a"}, "Having achieved a derivative, attempting to simplify to the required form proved difficult for many "
                "students."),
        ({"a"}, "Many did not realise that they could factorise the $(x+1)$ out early and instead expanded fully, "
                "simplified then factorised again to cancel in the last step."),
        ({"a"}, "This wasted valuable time and it was during this process that errors usually occurred.", BACK),
        ({"a"}, "The alternative method of simplifying the fraction before differentiating was less common, with usually "
                "poor attempts at partial fractions being applied leading to error."),
        ({"a"}, "Those who successfully simplified the fraction almost always went to achieve the correct answer.", NO),
        ({"b"}, "Nearly all students who were correct in part (a) achieved the mark for part (b), including many who had "
                "failed to cancel the $(x+1)$."),
        ({"b"}, "Indeed, there were many cases where a correct answer to part (b) was seen following incorrect work in "
                "(a), presumably due to the use of a calculator to plot and inspect the graph."),
    ],
    "04": [
        ({"a"}, "The vast majority of candidates did well in part (a), securing most or all of the marks available."),
        ({"a"}, "They appreciated the need to rewrite the expression with a negative power and dealt confidently with "
                "the factorisation."),
        ({"a"}, "The binomial expansion itself was also correctly executed and careful working ensured that there were "
                "relatively few slips in powers or signage."),
        ({"a"}, r"Common errors included bracketing errors seen with $-\frac{x^2}{4}$ in the third term rather than "
                r"$\left(-\frac{x}{4}\right)^2$; failing to correctly combine the factored out $4^{-\frac{1}{2}}$ with "
                r"the expansion $\left(1+\frac{x}{8}+\frac{3x^2}{128}\right)$"),
        ({"bi", "bii"}, "Part (b) caused more difficulty."),
        ({"bi"}, "In part (i), many candidates appeared to realise that the question was linked to the range of valid $x$ "
                 "values and the correct answer, $x=-14$, was selected most often."),
        ({"bi"}, "To gain this mark however, the correct answer and a valid reason needed to be given.", NO),
        ({"bi"}, r"Examples of valid reasons were “the expansion is only valid for $|x|<4$” , “the expansion is not valid "
                 r"for $x=-14$ as $|-14|>4$”."),
        ({"bii"}, "In part (ii), only a small proportion of the candidates realised that the expansion is more accurate "
                  "for values of $x$ closest to 0."),
        ({"bii"}, r"Many resorted to using the three values given and comparing the results to the exact value of "
                  r"$\sqrt{2}$ or else stating that the answer was 2 as it was the closest value to $\sqrt{2}$.", NO),
    ],
    "05": [
        (W, "This question on completing the square and the quadratic function was accessible to all, especially the "
            "first 6 marks."),
        ({"c"}, "Part (c) was more demanding but there were some excellent responses here."),
        ({"a"}, "Part (a) was very straightforward and many students were able to write down the answer without any "
                "difficulty."),
        ({"a"}, "Although errors were rare, one common incorrect answer was $2(x+1)^2+8$."),
        ({"b"}, "Part (b) was equally straightforward, even for candidates who did not achieve the correct result in "
                "part (a)."),
        ({"b"}, "Many used the form $a(x+b)^2+c$ or their graphical calculators to produce accurate and well drawn "
                "curves."),
        ({"b"}, "Marks were lost here when candidates drew V shaped curves or had incorrectly placed turning points."),
        ({"c"}, "As stated earlier, part (c) was a lot more demanding."),
        ({"c"}, "Rather strangely part (i) was found more accessible than part (ii)."),
        ({"c"}, "Many candidates sketched the new curve and compared the positions of the turning points noting that "
                "$(-1,7)$ had “moved” to $(1,3)$."),
        ({"c"}, "Disappointingly a rather sizeable majority could only describe this “movement” as a “transformation” "
                "rather than “translation” .", BACK),
        ({"c"}, r"Fewer students could use the form $\mathrm{h}(x)=\frac{21}{2(x+1)^2+7}$ to find the range of the "
                r"function."),
        ({"c"}, r"Many resorted to substituting $x=0$ producing a range with $y=\frac{21}{9}$ as one of the limits."),
        ({"c"}, r"Common incorrect answers for the range of h scoring one mark were $\mathrm{h}(x)\geqslant3$ or "
                r"$0<\mathrm{f}(x)\leqslant3$."),
    ],
    "06": [
        (W, "This was generally a well attempted question with most candidates able to score over half of the marks.",
         NO),
        ({"a"}, "In part (a) the correct identities were well known and efficiently used in order to obtain an equation "
                "in one function."),
        ({"a"}, "Almost all candidates who reached this stage were then able to proceed to find at least one correct "
                "angle.", BACK),
        ({"a"}, "It was clear from the graphs and diagrams sketched by most candidates that they had been taught to look "
                "for all angles in the required range and many were able to give all four of the angles needed.", NO),
        ({"a"}, r"Only a minority of candidates identified $0,\pm180$ as solutions to the equations."),
        ({"a"}, r"Most candidates divided through by $\sin\theta$ or $\cos\theta$ and failed to identify any of these "
                r"values.", BACK),
        ({"b"}, r"In part (b) a significant number used $2x-50=\theta$ rather than $x-25=\theta$."),
        ({"b"}, "Of those who used one of their solutions to part (a), the majority then proceeded to the correct answer, "
                "although a significant number did not give the smallest positive solution to the equation.", NO),
        ({"b"}, "This was usually due to the fact that they used their smallest positive solution to part (a) (i.e. "
                "18.4) in the equation, not realising that they needed to use – 18.4.", BACK),
    ],
    "07": [
        (W, "It was pleasing to see that most candidates attempted to form an exponential model using a suitable "
            "equation.", NO),
        (W, "This is one of the new topics in the specification and candidates who didn't gain any marks on this "
            "question, generally did so because they did not attempt it, or that they tried to use a non-exponential "
            "model.", BACK),
        ({"a"}, r"In part (a) $V=Ar^t$ or $V=A\mathrm{e}^{kt}$ were the most popular types of correct models that "
                r"candidates opted for."),
        ({"a"}, "However, some methods were often muddled or poorly shown, but many candidates who used a correct model "
                "were able to proceed to obtain correct values for their constants."),
        ({"a"}, r"Those candidates who used the model $V=A\mathrm{e}^{kt}$ frequently gave the constant $k$ as a log and "
                r"errors sometimes occurred with the sign of this constant.", NO),
        ({"a"}, "Errors in calculating constants with the model $V=Ar^t$ often occurred when candidates used "
                "$V=Ar^{t-1}$ instead."),
        ({"b"}, "In part (b) candidates who correctly answered part (a) usually understood that for this section they "
                "needed to substitute $t=10$ into their model, and most were able to do this.", NO),
        ({"b"}, "Many candidates then proceeded to make a sensible comparison of the value gained by their model with "
                "the actual value in order to comment on the model’s reliability (sometimes calculating and commenting "
                "on % error)."),
        ({"b"}, "The final mark, however, was frequently lost because answers were too vague, without a clear "
                "comparison or assessment of reliability being made."),
        ({"b"}, "Some candidates appeared to think that a model was only acceptable if it gave the exact real value.",
         NO),
        ({"c"}, "Most candidates who attempted part (c) understood which of their two constants would need to be "
                "altered, although marks were lost either because the answer given just said the constant needed to be "
                "changed or because they wrongly identified whether the constant needed to be decreased/increased."),
        ({"c"}, r"This was more of a difficulty for those candidates who had used the model $V=A\mathrm{e}^{kt}$, "
                r"because candidates were often dealing with negative constants and/or constants given as logs so the "
                r"phrases used were not always mathematically correct.", BACK),
        ({"c"}, "An example was often useful to convey what the candidate meant where there was ambiguity."),
        ({"c"}, "Candidates who had gone with model $V=Ar^t$ were less likely to make an error in judging whether their "
                "constant should increase or decrease."),
    ],
    "08": [
        (W, "The first six marks in this question relating the definite integral with the area under the curve were "
            "straightforward."),
        (W, "Only the best candidates were able to access the last four with many struggling to explain the "
            "significance of the root 5.442."),
        ({"a"}, "Most students gained all 4 marks in part (a)."),
        ({"a"}, "Some unnecessarily complicated their proof by attempting integration by parts but in the main, all "
                "calculations were accurately performed."),
        ({"b"}, "As with all proofs, part (b) proved to be very discriminating."),
        ({"b"}, r"Many candidates picked up the first mark for setting $\frac{1}{4}b^4-\frac{2}{3}b^3-4b^2="
                r"\pm\frac{20}{3}$ but there was much confusion as to the sign of $\frac{20}{3}$ on the right hand "
                r"side."),
        ({"b"}, "Most students attempted to proceed by the method shown in the scheme."),
        ({"b"}, "It should be noted that division by $b^2+4b+4$ was much easier and faster than dividing by $(b+2)$ "
                "twice.", NO),
        ({"b"}, "Fully correct solutions to (b) were rare with many picking up 2 out of the 4 marks."),
        ({"c"}, "In part (c) many candidates realised that 5.442 was to the right of 4 on the $x$- axis and shaded an "
                "appropriate area, scoring one mark."),
        ({"c"}, "Full explanations as to its significance were rare and confined to the best candidates.", BACK),
        ({"c"}, "Any suitable statement that alluded to the fact that the area above the curve is equal to the area "
                "below the curve (between $-2$ and 5.442) was acceptable."),
    ],
    "09": [
        ({"b"}, "There were many good attempts to this question, though complete answers to part (b) were achieved only "
                "by the very best."),
        ({"a"}, r"In part (a) most students gained the B mark by writing $\log a-\log b=\log\left(\frac{a}{b}\right)$, "
                r"though a few did attempt to rearrange first and used other equivalents."),
        ({"a"}, "Students who gained this mark generally were successful at ‘undoing’ the logs and making $a$ the "
                "subject.", BACK),
        ({"a"}, "Students who failed to recognise the logarithmic rule for subtraction or addition often made no "
                "progress with the question."),
        ({"b"}, "Part (b) was more challenging with many only scoring the first mark."),
        ({"b"}, "Many students focused solely on the exclusion of $b=1$ from the denominator and paid no heed to the "
                "condition that $a>0$."),
        ({"b"}, r"Few students were able to provide a full explanation including that as $a>0$, $\frac{b^2}{b-1}>0$ and "
                r"so $b>1$."),
        ({"b"}, "Most candidates knew that the denominator of a fraction cannot be zero, though few of them used the "
                "words “undefined” or “infinity” in their answers, but would more often refer to ‘math error’ or ‘can’t "
                "didide by 0’."),
    ],
    "10": [
        (W, "The idea of proof is another new one in this updated specification.", NO),
        (W, "It was not well known and a disproportionate number of blank or barely started solutions indicated a lack "
            "of expertise in this topic.", BACK),
        ({"i"}, "Candidates who scored full marks for part (i) most often did so via algebraic proof, letting $n=2m$ "
                "(for even numbers) and then $n=2m+1$ (for odd numbers), although several candidates missed out on the "
                "final accuracy mark as they failed to insert a conclusion for all $n$."),
        ({"i"}, "Weaker candidates tried to use $m+1$ instead of $2m+1$ to represent odd numbers."),
        ({"i"}, "Also many candidates only considered either odd or even numbers, but not both."),
        ({"i"}, "Candidates who set out to use proof via contradiction tended to score few marks as they did not show an "
                "understanding of how to use that method of proof."),
        ({"i"}, "Proofs via logic were rare and tended to appear as part of a mix of different methods where the "
                "candidates seemed to be unclear of the best way to proceed."),
        ({"i"}, "Some candidates seemed to think that using random numbers to show that the expression is not divisible "
                "by 4 amounted to proof (receiving 0 marks)."),
        ({"i"}, "Students need more practice on this style of proof.", NO),
        ({"ii"}, "In part (ii) more candidates approached the problem algebraically than graphically."),
        ({"ii"}, "They were generally able to set up the two equations / inequalities required, but errors often "
                 "occurred in their use of algebra when attempting to solve them."),
        ({"ii"}, "Some candidates only set up one of the two required inequalities."),
        ({"ii"}, "Many students attempted the question by just substituting numbers in to the expression, with most of "
                 "these deducing that the statement was always true.", NO),
        ({"ii"}, "Where candidates drew a graph, they often did not describe why their graph indicated that the "
                 "statement is sometimes true."),
        ({"ii"}, "Many graphs showed a line and a V shape but some were incorrect in the relative positioning of these "
                 "shapes.", NO),
    ],
    "11": [
        (W, "Overall very good attempts to this question were spoiled by a lack in accuracy ."),
        ({"a"}, "Part (a) was routine for most and candidates were thorough in showing their method."),
        ({"a"}, r"The most frequent and concise method involved calculations of the form "
                r"$24+6\times1.05+6\times1.05^2$."),
        ({"a"}, "Occasionally the work was overcomplicated by converting to seconds though the end result was generally "
                "satisfactory."),
        ({"b"}, "Part (b) was found to be challenging with some candidates choosing not to answer."),
        ({"b"}, "The most straightforward way was to use some values and spot the patterns."),
        ({"b"}, "This is a skill taught at GCSE yet seemed forgotten to many.", BACK),
        ({"b"}, r"Using the pattern on the left the time taken for the $r$ th kilometre would be $6\times1.05^{r-4}$"),
        ({"c"}, "Although most candidates knew that for part (c) they needed to sum a sequence of terms, errors were "
                "frequent and many."),
        ({"c"}, r"A sizeable minority lacked any appreciation of the model and resorted to the calculation "
                r"$\frac{6(1.05^{20}-1)}{1.05-1}$."),
        ({"c"}, "The majority of errors however were mainly due to a failure to link up the correct values for $a$ and "
                "$n$ in the formula for a geometric series."),
        ({"c"}, r"The most common of these was to use the strategy $24+\frac{6(1.05^{16}-1)}{1.05-1}$, forgetting that "
                r"the geometric sequence in this case should start at 6.3 instead of 6.", BACK),
        ({"c"}, "It is often a good idea in such a question to write out the first few terms to gain an appreciation of "
                "the model and how the sequence is formed. (See below)", NO),
        ({"c"}, r"From here it should be a fairly straightforward task to write down "
                r"$24+\frac{6.3(1.05^{16}-1)}{1.05-1}$", BACK),
    ],
    "12": [
        (W, "This question discriminated well between students of all abilities with part (a) and (b) more accessible "
            "to students compared to part (c) and (d)."),
        ({"a"}, rf"In part (a) most students were successful at using the product rule and setting {DYS} equal to 0 "
                rf"(though the latter was implied rather than being explicit in many cases)."),
        ({"a"}, r"Missing the $-0.25$ factor when differentiating the $\mathrm{e}^{(-0.25x)}$ was fairly common, but "
                r"the differentiation was mostly correctly carried out."),
        ({"a"}, "A few students failed to use the product rule correctly, instead multiplying the derivatives of each "
                "term, but these were in the minority.", NO),
        ({"a"}, "Having attempt the derivative the majority did set the result equal to zero (possibly implied) and "
                "proceeded to cancel the exponentials."),
        ({"a"}, "Reasoning for the cancellation was usually not given, but in this instance there was no requirement for "
                "such reasoning.", NO),
        ({"a"}, "However it might be well noted that such explanations may be required under the new specification.",
         NO),
        ({"a"}, r"Many students lost the final accuracy mark as they did not state or show division by $\cos x$."),
        ({"a"}, "Students need to be clear that in a ‘show that’ question all steps need to be shown."),
        ({"b"}, "Part (b) was the most successfully answered part of the question."),
        ({"b"}, r"Students realised that the graph of $|\mathrm{f}(x)|$ should be above the $x$-axis."),
        ({"b"}, "Where students did not gain full credit, this was usually due to poor drawing of loops (not decreasing "
                "heights, or rounding at the cusps).", NO),
        ({"b"}, "A few students chose to draw over the original figure which made it difficult in many cases to "
                "determine which pieces formed their graph.", NO),
        ({"b"}, "They would be well advised to sketch separate graphs in similar questions."),
        ({"c"}, "There was less success in part (c)."),
        ({"c"}, r"Attempts at this part were varied, with a sizeable proportion not making the connection with part (a) "
                r"at all and attempting to find the value of $H(t)$ at $\pi/2$ or some other value, or failing to "
                r"substitute into $H(t)$ at all."),
        ({"c"}, r"Many solved $\tan x=4$ to find the acute angle but did not then look for the further solution which "
                r"was needed for the height between the first and second bounces and so achieved only the first mark."),
        ({"c"}, "Also, use of degrees instead of radians was a common error, but this was allowed the first method "
                "mark.", NO),
        ({"c"}, "The magnitude of their resulting answer should have alerted them to the fact that something had gone "
                "very wrong."),
        ({"d"}, "Part (d) was another part with a varied array of answers."),
        ({"d"}, "Common incorrect responses referred to negative time, and the times between each bounce would be longer "
                "or that the ball would not bounce forever."),
        ({"d"}, "Many students gave a rote answer of “the effect of air resistance has not been taken into account” or "
                "“energy loss” or similar vague reasons rather than relate to the context of the question."),
        ({"d"}, "Since the model may have taken air resistance into account (the contributing factors to the model were "
                "not listed in the question), such an answer was unacceptable.", NO),
    ],
    "13": [
        (W, "Only the strongest candidates scored all 11 marks here, with the majority losing at least 1 mark, usually "
            "the first mark in (a) or the last mark in (b)."),
        ({"a"}, "In part (a) (i) many candidates realised that $x=2$ was linked to establishing that $q=4$ but they found "
                "difficulty explaining this by referencing the asymptote, or the denominator being zero.", NO),
        ({"a"}, "Almost all candidates provided good explanations in (a)(ii) even when they had provided inadequate "
                "explanations on part (i)"),
        ({"b"}, "In part (b) the vast majority of students knew they had to use partial fractions to attempt the "
                "question with many achieving the correct expression and correct integration."),
        ({"b"}, "The most common error was in simplifying the final logarithmic expression with many candidates leaving "
                "some of their answers in terms of ln (3/4) or ln (4/3) for example."),
        ({"b"}, "It was uncommon therefore to see a fully correct solution in the required form.", NO),
    ],
    "14": [
        (W, "A number of candidates did not attempt this question."),
        (W, "Whether this was due to lack of understanding or time constraints is unknown.", BACK),
        ({"a"}, "Part (a) was generally well done with a surprising proportion using implicit differentiation."),
        ({"a"}, rf"A good number who found ${DY}$ correctly failed to substitute in $y=0$ to find the value of ${DY}$ at "
                rf"the origin."),
        ({"a"}, r"Candidates who tried to expand $\sin2y$ using the double angle formulae and then differentiating using "
                r"the product rule often went wrong."),
        ({"b"}, "The small angle approximation in (b) part (i) was also well handled."),
        ({"b"}, "Most settled for the form $x=8y$ although some rearranged to $y=$ ."),
        ({"b"}, r"Marks were generally lost when $\sin2y$ was replaced by $2\theta$ instead of $2y$."),
        ({"b"}, "Many candidates failed to see the link between (a) and (b)(i) even though they had both answers "
                "correct."),
        ({"b"}, "They were unable to see that the gradients were the same or else failed to explain themselves "
                "coherently."),
        ({"c"}, "Only a small percentage of candidates were able to secure full marks for part (c) and it was not "
                "uncommon to see the whole question left unanswered.", NO),
        ({"c"}, "This type of question was common on Core 3 and usually well answered.", BACK),
    ],
}

# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
RATINGS = {
    "01": ("easy", ("01", 3)),
    "02a": ("medium", ("02", 2)),
    "02b": ("medium", ("02", 4)),
    "03a": ("medium", ("03", 6)),
    "03b": ("easy", ("03", 11)),
    "04a": ("easy", ("04", 0)),
    "04bi": ("medium", ("04", 5)),
    "04bii": ("hard", ("04", 8)),
    "05a": ("easy", ("05", 2)),
    "05b": ("easy", ("05", 4)),
    "05c": ("hard", ("05", 7)),
    "06a": ("medium", ("06", 4)),
    "06b": ("medium", ("06", 7)),
    "07a": ("medium", ("07", 3)),
    "07b": ("medium", ("07", 8)),
    "07c": ("medium", ("07", 10)),
    "08a": ("easy", ("08", 2)),
    "08b": ("hard", ("08", 8)),
    "08c": ("hard", ("08", 10)),
    "09a": ("easy", ("09", 2)),
    "09b": ("hard", ("09", 6)),
    "10i": ("hard", ("10", 1)),
    "10ii": ("hard", ("10", 12)),
    "11a": ("easy", ("11", 1)),
    "11b": ("hard", ("11", 4)),
    "11c": ("hard", ("11", 8)),
    "12a": ("medium", ("12", 7)),
    "12b": ("easy", ("12", 9)),
    "12c": ("hard", ("12", 16)),
    "12d": ("medium", ("12", 19)),
    "13a": ("medium", ("13", 1)),
    "13b": ("hard", ("13", 5)),
    "14a": ("easy", ("14", 2)),
    "14b": ("medium", ("14", 8)),
    "14c": ("hard", ("14", 10)),
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
