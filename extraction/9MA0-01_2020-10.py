"""Draft builder for 9MA0-01 2020-10 (A level Pure Paper 1, October 2020).

Run (from the project root, with the venv active):
    python extraction/9MA0-01_2020-10.py        # writes out/drafts/9MA0-01_2020-10.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-01_2020-10.json

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

P, S = "9MA0-01", "2020-10"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "09c"); label as printed (e.g. "9(c)")."""
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


DY = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
D2Y = r"\frac{\mathrm{d}^2y}{\mathrm{d}x^2}"
DX = r"\,\mathrm{d}x"
I, J, K = r"\mathbf{i}", r"\mathbf{j}", r"\mathbf{k}"

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q1A = ["Find the first four terms, in ascending powers of $x$, of the binomial expansion of",
       r"$$(1+8x)^{\frac{1}{2}}$$", "giving each term in simplest form."]
Q3 = ["Relative to a fixed origin $O$", rf"• point $A$ has position vector $2{I}+5{J}-6{K}$",
      rf"• point $B$ has position vector $3{I}-3{J}-4{K}$", rf"• point $C$ has position vector $2{I}-16{J}+4{K}$"]
Q3A = r"Find $\overrightarrow{AB}$"
Q4 = [r"The function f is defined by", r"$$\mathrm{f}(x)=\frac{3x-7}{x-2}\qquad x\in\mathbb{R},x\neq2$$"]
Q5 = ["A car has six forward gears.", "The fastest speed of the car", r"• in 1st gear is 28 km h$^{-1}$",
      r"• in 6th gear is 115 km h$^{-1}$"]
Q6A = [r"Express $\sin x+2\cos x$ in the form $R\sin(x+\alpha)$ where $R$ and $\alpha$ are constants, $R>0$ and "
       r"$0<\alpha<\frac{\pi}{2}$",
       r"Give the exact value of $R$ and give the value of $\alpha$ in radians to 3 decimal places."]
Q6M = [r"The temperature, $\theta^\circ$C, inside a room on a given day is modelled by the equation",
       r"$$\theta=5+\sin\left(\frac{\pi t}{12}-3\right)+2\cos\left(\frac{\pi t}{12}-3\right)\qquad0\leqslant t<24$$",
       "where $t$ is the number of hours after midnight.",
       "Using the equation of the model and your answer to part (a),"]
Q9 = [r"[Figure 2: the curve $C$, coming down very steeply from high up just left of the $y$-axis, crossing the negative "
      r"$x$-axis, reaching a minimum below the $x$-axis just left of the $y$-axis, rising steeply through the negative "
      r"$y$-axis and crossing the positive $x$-axis, reaching a low maximum, then decreasing towards the $x$-axis as $x$ "
      r"increases.]",
      r"Figure 2 shows a sketch of the curve $C$ with equation $y=\mathrm{f}(x)$ where",
      r"$$\mathrm{f}(x)=4(x^2-2)\mathrm{e}^{-2x}\qquad x\in\mathbb{R}$$"]
Q9A = r"Show that $\mathrm{f}'(x)=8(2+x-x^2)\mathrm{e}^{-2x}$"
Q9B = "Hence find, in simplest form, the exact coordinates of the stationary points of $C$."
Q10A = ["Use the substitution $x=u^2+1$ to show that",
        r"$$\int_5^{10}\frac{3\,\mathrm{d}x}{(x-1)\left(3+2\sqrt{x-1}\right)}=\int_p^q\frac{6\,\mathrm{d}u}{u(3+2u)}$$",
        "where $p$ and $q$ are positive constants to be found."]
Q11 = [r"[Figure 3: the circle $C_1$ with centre $O$ and a smaller circle $C_2$ to its right, centred on the positive "
       r"$x$-axis; the circles meet at $A$ (above the $x$-axis) and $B$ (below it), with the chord $AB$ dashed; the region "
       r"made up of both discs is shaded.]",
       "Circle $C_1$ has equation $x^2+y^2=100$", "Circle $C_2$ has equation $(x-15)^2+y^2=40$",
       "The circles meet at points $A$ and $B$ as shown in Figure 3."]
Q12 = ["In this question you must show all stages of your working.",
       "Solutions relying entirely on calculator technology are not acceptable."]
Q12A = ["Show that", r"$$\mathrm{cosec}\,\theta-\sin\theta\equiv\cos\theta\cot\theta\qquad\theta\neq(180n)^\circ\quad "
        r"n\in\mathbb{Z}$$"]
Q13 = [r"A sequence of numbers $a_1,a_2,a_3,\ldots$ is defined by",
       r"$$a_{n+1}=\frac{k(a_n+2)}{a_n}\qquad n\in\mathbb{N}$$", "where $k$ is a constant.", "Given that",
       "• the sequence is a periodic sequence of order 3", "• $a_1=2$"]
Q14 = ["A large spherical balloon is deflating.",
       "At time $t$ seconds the balloon has radius $r$ cm and volume $V$ cm$^3$",
       "The volume of the balloon is modelled as decreasing at a constant rate."]
Q14A = ["Using this model, show that", r"$$\frac{\mathrm{d}r}{\mathrm{d}t}=-\frac{k}{r^2}$$",
        "where $k$ is a positive constant."]
Q14G = ["Given that", "• the initial radius of the balloon is 40 cm", "• after 5 seconds the radius of the balloon is 20 cm",
        "• the volume of the balloon continues to decrease at a constant rate until the balloon is empty"]
Q14B = "solve the differential equation to find a complete equation linking $r$ and $t$."
Q15 = ["The curve $C$ has equation", r"$$x^2\tan y=9\qquad0<y<\frac{\pi}{2}$$"]
Q15A = ["Show that", rf"$${DY}=\frac{{-18x}}{{x^4+81}}$$"]

LATEX = {
    "01a": L(*Q1A),
    "01b": L("(a) " + Q1A[0], *Q1A[1:],
             r"(b) Explain how you could use $x=\frac{1}{32}$ in the expansion to find an approximation for $\sqrt{5}$",
             "There is no need to carry out the calculation."),
    "02": L("By taking logarithms of both sides, solve the equation", "$$4^{3p-1}=5^{210}$$",
            "giving the value of $p$ to one decimal place."),
    "03a": L(*Q3, Q3A),
    "03b": L(*Q3, "(a) " + Q3A, "(b) Show that quadrilateral $OABC$ is a trapezium, giving reasons for your answer."),
    "04a": L(*Q4, r"Find $\mathrm{f}^{-1}(7)$"),
    "04b": L(*Q4, r"Show that $\mathrm{ff}(x)=\frac{ax+b}{x-3}$ where $a$ and $b$ are integers to be found."),
    "05a": L(*Q5, "Given that the fastest speed of the car in successive gears is modelled by an "
                  r"$\textbf{arithmetic sequence}$,", "find the fastest speed of the car in 3rd gear."),
    "05b": L(*Q5, "Given that the fastest speed of the car in successive gears is modelled by a "
                  r"$\textbf{geometric sequence}$,", "find the fastest speed of the car in 5th gear."),
    "06a": L(*Q6A),
    "06b": L("(a) " + Q6A[0], Q6A[1], *Q6M, "(b) deduce the maximum temperature of the room during this day,"),
    "06c": L("(a) " + Q6A[0], Q6A[1], *Q6M,
             "(c) find the time of day when the maximum temperature occurs, giving your answer to the nearest minute."),
    "07": L(r"[Figure 1: a U-shaped curve $C$ with its minimum point at $(-2, 13)$, and a straight line $l$ with positive "
            r"gradient through $(-2, 13)$ and through the point 25 on the $y$-axis, where $C$ also crosses the $y$-axis; "
            r"the region $R$ between $l$ (above) and $C$ (below), from $x=-2$ to the $y$-axis, is shaded.]",
            r"Figure 1 shows a sketch of a curve $C$ with equation $y=\mathrm{f}(x)$ and a straight line $l$.",
            "The curve $C$ meets $l$ at the points $(-2, 13)$ and $(0, 25)$ as shown.",
            "The shaded region $R$ is bounded by $C$ and $l$ as shown in Figure 1.", "Given that",
            r"• $\mathrm{f}(x)$ is a quadratic function in $x$",
            r"• $(-2, 13)$ is the minimum turning point of $y=\mathrm{f}(x)$", "use inequalities to define $R$."),
    "08": L("A new smartphone was released by a company.",
            "The company monitored the total number of phones sold, $n$, at time $t$ days after the phone was released.",
            "The company observed that, during this time,", "the rate of increase of $n$ was proportional to $n$",
            "Use this information to write down a suitable equation for $n$ in terms of $t$.",
            "(You do not need to evaluate any unknown constants in your equation.)"),
    "09a": L(*Q9, Q9A),
    "09b": L(*Q9, "(a) " + Q9A, "(b) " + Q9B),
    "09c": L(*Q9, "(a) " + Q9A, "(b) " + Q9B, "The function g and the function h are defined by",
             r"$$\mathrm{g}(x)=2\mathrm{f}(x)\qquad x\in\mathbb{R}$$",
             r"$$\mathrm{h}(x)=2\mathrm{f}(x)-3\qquad x\geqslant0$$", "(c) Find (i) the range of g",
             "(ii) the range of h"),
    "10a": L(*Q10A),
    "10b": L("(a) " + Q10A[0], *Q10A[1:], "(b) Hence, using algebraic integration, show that",
             r"$$\int_5^{10}\frac{3\,\mathrm{d}x}{(x-1)\left(3+2\sqrt{x-1}\right)}=\ln a$$",
             "where $a$ is a rational constant to be found."),
    "11a": L(*Q11, "Show that angle $AOB=0.635$ radians to 3 significant figures, where $O$ is the origin."),
    "11b": L(*Q11, "(a) Show that angle $AOB=0.635$ radians to 3 significant figures, where $O$ is the origin.",
             "The region shown shaded in Figure 3 is bounded by $C_1$ and $C_2$",
             "(b) Find the perimeter of the shaded region, giving your answer to one decimal place."),
    "12a": L(*Q12, *Q12A),
    "12b": L(*Q12, "(a) " + Q12A[0], Q12A[1], r"(b) Hence, or otherwise, solve for $0<x<180^\circ$",
             r"$$\mathrm{cosec}\,x-\sin x=\cos x\cot(3x-50^\circ)$$"),
    "13a": L(*Q13, "show that", "$$k^2+k-2=0$$"),
    "13b": L(*Q13, r"For this sequence explain why $k\neq1$"),
    "13c": L(*Q13, "Find the value of", r"$$\sum_{r=1}^{80}a_r$$"),
    "14a": L(*Q14, *Q14A),
    "14b": L(*Q14, "(a) " + Q14A[0], *Q14A[1:], *Q14G, "(b) " + Q14B),
    "14c": L(*Q14, "(a) " + Q14A[0], *Q14A[1:], *Q14G, "(b) " + Q14B,
             "(c) Find the limitation on the values of $t$ for which the equation in part (b) is valid."),
    "15a": L(*Q15, *Q15A),
    "15b": L(*Q15, "(a) " + Q15A[0], Q15A[1], r"(b) Prove that $C$ has a point of inflection at $x=\sqrt[4]{27}$"),
    "16": L("Prove by contradiction that there are no positive integers $p$ and $q$ such that", "$$4p^2-q^2=25$$"),
}

BIN = (r"(1+8x)^{\frac{1}{2}}=1+\frac{1}{2}\times8x+\frac{\frac{1}{2}\times-\frac{1}{2}}{2!}\times(8x)^2+"
       r"\frac{\frac{1}{2}\times-\frac{1}{2}\times-\frac{3}{2}}{3!}\times(8x)^3")
FF = (r"\mathrm{ff}(x)=\frac{3\times\left(\frac{3x-7}{x-2}\right)-7}{\left(\frac{3x-7}{x-2}\right)-2}="
      r"\frac{3\times(3x-7)-7(x-2)}{3x-7-2(x-2)}")
DV = r"\frac{\mathrm{d}V}{\mathrm{d}t}"
DVR = r"\frac{\mathrm{d}V}{\mathrm{d}r}"
DRT = r"\frac{\mathrm{d}r}{\mathrm{d}t}"
A12 = "ALT: Alt 1- Right hand side to left hand side"
B12 = "ALT: Alt 2- Works on both sides"
C12 = "ALT: Alt (b)"
Q16A = "ALT: 16 Alt 1"
Q16B = "ALT: Alt 2 (odd and even numbers)"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", SEQ, "4.1", 3, LATEX["01a"],
      [rf"M1 (AO 1.1b): ${BIN}$. Notes: Attempts the binomial expansion with $n=\frac{{1}}{{2}}$ and obtains the correct "
       rf"structure for term 3 or term 4. Award for the correct coefficient with the correct power of $x$. Do not accept "
       rf"${{}}^nC_r$ notation for coefficients. For example look for term 3 in the form "
       rf"$\frac{{\frac{{1}}{{2}}\times-\frac{{1}}{{2}}}}{{2!}}\times(*x)^2$ or "
       rf"$\frac{{\frac{{1}}{{2}}\times-\frac{{1}}{{2}}\times-\frac{{3}}{{2}}}}{{3!}}\times(*x)^3$",
       rf"A1 (AO 1.1b): ${BIN}$. Notes: Correct (unsimplified) expression. May be implied by correct simplified "
       rf"expression",
       r"A1 (AO 1.1b): $=1+4x-8x^2+32x^3+\ldots$ Notes: $1+4x-8x^2+32x^3$ Award if there are extra terms (even if "
       r"incorrect). Award if the terms are listed $1,4x,-8x^2,32x^3$"],
      False, 2),
    e("01b", "1(b)", SEQ, "4.1", 2, LATEX["01b"],
      [r"M1 (AO 1.1b): Substitutes $x=\frac{1}{32}$ into $(1+8x)^{\frac{1}{2}}$ to give $\frac{\sqrt{5}}{2}$. Notes: Score "
       r"for substituting $x=\frac{1}{32}$ into $(1+8x)^{\frac{1}{2}}$ to obtain $\frac{\sqrt{5}}{2}$ or equivalent such "
       r"as $\sqrt{\frac{5}{4}}$ Alternatively award for substituting $x=\frac{1}{32}$ into both sides and making a "
       r"connection between the two sides by use of an = or ≈ . E.g. $\left(1+\frac{8}{32}\right)^{\frac{1}{2}}=1+4\times"
       r"\frac{1}{32}-8\times\left(\frac{1}{32}\right)^2+32\times\left(\frac{1}{32}\right)^3$ following through on their "
       r"expansion Also implied by $\frac{\sqrt{5}}{2}=\frac{1145}{1024}$ for a correct expansion It is not enough to "
       r"state substitute $x=\frac{1}{32}$ into “ the expansion” or just the rhs “$1+4x-8x^2+32x^3$”",
       r"A1ft (AO 2.4): Explains that $x=\frac{1}{32}$ is substituted into $1+4x-8x^2+32x^3$ and you multiply the result "
       r"by 2. Notes: Requires a full (and correct) explanation as to how the expansion can be used to estimate "
       r"$\sqrt{5}$ E.g. Calculates $1+4\times\frac{1}{32}-8\times\left(\frac{1}{32}\right)^2+32\times"
       r"\left(\frac{1}{32}\right)^3$ and multiplies by 2. This can be scored from an incorrect binomial expansion or a "
       r"binomial expansion with more terms. The explanation could be mathematical. So "
       r"$\frac{\sqrt{5}}{2}=\frac{1145}{1024}\to\sqrt{5}=\frac{1145}{512}$ is acceptable. SC: For 1 mark, M1,A0 score for "
       r"a statement such as “substitute $x=\frac{1}{32}$ into both sides of part (a) and make $\sqrt{5}$ the subject”"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02", "2", EXP, "6.5, 6.4", 3, LATEX["02"],
      [r"M1 (AO 1.1b): $4^{3p-1}=5^{210}\Rightarrow(3p-1)\log4=210\log5$. Notes: Takes logs of both sides and uses the "
       r"power law on each side. Condone a missing bracket on lhs and slips. Award for any base including ln but the "
       r"logs must be the same base.",
       r"dM1 (AO 2.1): $\Rightarrow3p=\frac{210\log5}{\log4}+1\Rightarrow p=\ldots$ Notes: A full method leading to a value "
       r"for $p$. It is dependent upon the previous M mark and there must be an attempt to change the subject of the "
       r"equation in the correct order. Look for $(3p-1)\log4=210\log5\Rightarrow3p=\frac{210\log5}{\log4}\pm1\Rightarrow "
       r"p=\ldots$ condoning slips. You may see numerical versions E.g. $(3p-1)\times0.60=210\times0.7\Rightarrow"
       r"1.8p-0.6=147\Rightarrow p=82$ Use of incorrect log laws would be dM0. E.g $(3p-1)\log4=210\log5\Rightarrow "
       r"3p=210\log\frac{5}{4}\pm1$",
       r"A1 (AO 1.1b): $p=$ awrt 81.6. Notes: awrt 81.6 following a correct method. Bracketing errors can be recovered "
       r"for full marks A correct answer with no working scores 0 marks. The demand in the question is clear.",
       r"ALT: There are alternatives: E.g. A starting point could be $4^{3p-1}=5^{210}\Rightarrow\frac{4^{3p}}{4}=5^{210}$ "
       r"— M1: the first M mark is still for using the power law correctly on each side",
       r"ALT: There are alternatives: starting from $\frac{4^{3p}}{4}=5^{210}$ — dM1: In such a method the dM1 mark is for "
       r"using all log rules correctly and proceeding to a value for $p$.",
       r"ALT: Using base 4 or 5 E.g. $4^{3p-1}=5^{210}\Rightarrow(3p-1)=\log_45^{210}$ — M1: The M mark is not scored "
       r"until $(3p-1)=210\log_45$"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", VEC, "10.3, 10.4", 2, LATEX["03a"],
      [rf"M1 (AO 1.1b): $\overrightarrow{{AB}}=(3{I}-3{J}-4{K})-(2{I}+5{J}-6{K})$. Notes: Attempts to subtract either way "
       rf"around. If no method is seen it is implied by two of $\pm1{I}\pm8{J}\pm2{K}$.",
       rf"A1 (AO 1.1b): $={I}-8{J}+2{K}$. Notes: ${I}-8{J}+2{K}$ or $\begin{{pmatrix}}1\\-8\\2\end{{pmatrix}}$ but not "
       rf"$(1,-8,2)$"],
      False, 6),
    e("03b", "3(b)", VEC, "10.5, 10.3", 2, LATEX["03b"],
      [rf"M1 (AO 1.1b): States $\overrightarrow{{OC}}=2\times\overrightarrow{{AB}}$. Notes: Compares their ${I}-8{J}+2{K}$ "
       rf"with $2{I}-16{J}+4{K}$ by stating any one of • $\overrightarrow{{OC}}=2\times\overrightarrow{{AB}}$ • "
       rf"$\begin{{pmatrix}}2\\-16\\4\end{{pmatrix}}=2\times\begin{{pmatrix}}1\\-8\\2\end{{pmatrix}}$ • "
       rf"$\overrightarrow{{OC}}=\lambda\times\overrightarrow{{AB}}$ or vice versa This may be awarded if $AB$ was "
       rf"subtracted “the wrong way around” or if there was one numerical slip",
       rf"A1 (AO 2.4): Explains that as $OC$ is parallel to $AB$, so $OABC$ is a trapezium. Notes: A full explanation as "
       rf"to why $OABC$ is a trapezium. Requires fully correct calculations, so part (a) must be "
       rf"$\overrightarrow{{AB}}=({I}-8{J}+2{K})$ It requires a reason and minimal conclusion. Example 1: "
       rf"$\overrightarrow{{OC}}=2\times\overrightarrow{{AB}}$, therefore $OC$ is parallel to $AB$ so $OABC$ is a trapezium "
       rf"Example 2: A trapezium has one pair of parallel sides. As $\overrightarrow{{OC}}=2\times\overrightarrow{{AB}}$, "
       rf"they are parallel, so ✓. Example 3 As $\begin{{pmatrix}}2\\-16\\4\end{{pmatrix}}=2\times\begin{{pmatrix}}1\\-8\\2"
       rf"\end{{pmatrix}}$, $OC$ and $AB$ are parallel, so proven Example 4 Accept as "
       rf"$\overrightarrow{{OC}}=\lambda\times\overrightarrow{{AB}}$, they are parallel so true Note: There are two "
       rf"definitions for a trapezium. One stating that it is a shape with one pair of parallel sides, the other with only "
       rf"one pair of parallel sides. Any calculations to do with sides $OA$ and $CB$ in this question may be ignored, "
       rf"even if incorrect."],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", ALG, "2.8", 2, LATEX["04a"],
      [r"M1 (AO 3.1a): Either attempts $\frac{3x-7}{x-2}=7\Rightarrow x=\ldots$ Or attempts $\mathrm{f}^{-1}(x)$ and "
       r"substitutes in $x=7$. Notes: For either attempting to solve $\frac{3x-7}{x-2}=7$. Look for an attempt to multiply "
       r"by the $(x-2)$ leading to a value for $x$. Or score for substituting in $x=7$ in $\mathrm{f}^{-1}(x)$. FYI "
       r"$\mathrm{f}^{-1}(x)=\frac{2x-7}{x-3}$ The method for finding $\mathrm{f}^{-1}(x)$ should be sound, but you can "
       r"condone slips.",
       r"A1 (AO 1.1b): $\frac{7}{4}$ oe. Notes: $\frac{7}{4}$"],
      False, 8),
    e("04b", "4(b)", ALG, "2.8, 2.10", 3, LATEX["04b"],
      [rf"M1 (AO 1.1b): Attempts ${FF}$. Notes: For an attempt at fully substituting $\frac{{3x-7}}{{x-2}}$ into "
       rf"$\mathrm{{f}}(x)$. Condone slips but the expression must have a correct form. E.g. "
       rf"$\frac{{3\times\left(\frac{{*-*}}{{*-*}}\right)-a}}{{\left(\frac{{*-*}}{{*-*}}\right)-b}}$ where $a$ and $b$ are "
       rf"positive constants.",
       rf"dM1 (AO 1.1b): Attempts ${FF}$. Notes: Attempts to multiply all terms on the numerator and denominator by "
       rf"$(x-2)$ to create a fraction $\frac{{P(x)}}{{Q(x)}}$ where both $P(x)$ and $Q(x)$ are linear expressions. Condone "
       rf"$\frac{{P(x)}}{{Q(x)}}\times\frac{{x-2}}{{x-2}}$",
       r"A1 (AO 2.1): $=\frac{2x-7}{x-3}$. Notes: Reaches $\frac{2x-7}{x-3}$ via careful and accurate work. Implied by "
       r"$a=2,b=-7$ following correct work.",
       r"ALT: Methods involving $\frac{3x-7}{x-2}\equiv a+\frac{b}{x-2}$ may be seen. The scheme can be applied in a "
       r"similar way FYI $\frac{3x-7}{x-2}\equiv3-\frac{1}{x-2}$"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", SEQ, "4.4, 4.6", 3, LATEX["05a"],
      [r"M1 (AO 3.1b): Uses $115=28+5d\Rightarrow d=(17.4)$. Notes: Translates the problem into maths using $n^{\text{th}}$ "
       r"term $=a+(n-1)d$ and attempts to find $d$ Look for either $115=28+5d\Rightarrow d=\ldots$ or an attempt at "
       r"$\frac{115-28}{5}$ condoning slips It is implied by use of $d=17.4$ Note that $115=28+6d\Rightarrow d=\ldots$ is M0",
       r"M1 (AO 3.4): Uses $28+2\times\text{“}17.4\text{”}=\ldots$ Notes: Uses the model to find the fastest speed the car "
       r"can go in 3rd gear using $28+2\text{“}d\text{”}$ or equivalent. This can be awarded following an incorrect method "
       r"of finding “$d$”",
       r"A1 (AO 1.1b): $=62.8$ (km h$^{-1}$ ). Notes: 62.8 km/ h Lack of units are condoned. Allow exact alternatives such "
       r"as $\frac{314}{5}$"],
      False, 10),
    e("05b", "5(b)", SEQ, "4.5, 4.6", 3, LATEX["05b"],
      [r"M1 (AO 3.1b): Uses $115=28r^5\Rightarrow r=(1.3265)$. Notes: Translates the problem into maths using $n^{\text{th}}$ "
       r"term $=ar^{n-1}$ and attempts to find $r$ It must use the 1st and 6th gear and not the 3rd gear found in part (a) "
       r"Look for either $115=28r^5\Rightarrow r=\ldots$ o.e. or $\sqrt[5]{\frac{115}{28}}$ condoning slips. It is implied "
       r"by stating or using $r=$ awrt 1.33",
       r"M1 (AO 3.4): Uses $28\times\text{“}1.3265^4\text{”}=\ldots$ or $\frac{115}{\text{“}1.3265\text{”}}$. Notes: Uses "
       r"the model to find the fastest speed the car can go in 5th gear using $28\times\text{“}r^4\text{”}$ or "
       r"$\frac{115}{\text{“}r\text{”}}$ o.e. This can be awarded following an incorrect method of finding “$r$” A common "
       r"misread seems to be finding the fastest speed the car can go in 3rd gear as in (a). Providing it is clear what "
       r"has been done, e.g. $u_3=28\times\text{“}r^2\text{”}$ it can be awarded this mark.",
       r"A1 (AO 1.1b): $=86.7$ (km h$^{-1}$ ). Notes: awrt 86.7 km/h Lack of units are condoned. Expressions must be "
       r"evaluated."],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", TRIG, "5.6", 3, LATEX["06a"],
      [r"B1 (AO 1.1b): $R=\sqrt{5}$. Notes: $R=\sqrt{5}$ only.",
       r"M1 (AO 1.1b): $\tan\alpha=2\Rightarrow\alpha=\ldots$ Notes: Proceeds to a value of $\alpha$ from $\tan\alpha=\pm2$, "
       r"$\tan\alpha=\pm\frac{1}{2}$, $\sin\alpha=\pm\frac{2}{\text{“}R\text{”}}$ OR $\cos\alpha=\pm\frac{1}{\text{“}R"
       r"\text{”}}$ It is implied by either awrt 1.11 (radians) or 63.4 (degrees)",
       r"A1 (AO 1.1b): $\alpha=1.107$. Notes: $\alpha=$ awrt 1.107"],
      False, 12),
    e("06b", "6(b)", TRIG, "5.9, 5.6", 1, LATEX["06b"],
      [r"B1ft (AO 2.2a): $\theta=5+\sqrt{5}\sin\left(\frac{\pi t}{12}+1.107-3\right)$ $\left(5+\sqrt{5}\right)^\circ$C or "
       r"awrt $7.24^\circ$C. Notes: Deduces that the maximum temperature is $\left(5+\sqrt{5}\right)^\circ$C or awrt "
       r"$7.24^\circ$C Remember to isw Condone a lack of units. Follow through on their value of $R$ so allow "
       r"$(5+\text{“}R\text{”})^\circ$C"],
      False, 12),
    e("06c", "6(c)", TRIG, "5.9, 5.7", 3, LATEX["06c"],
      [r"M1 (AO 3.1b): $\frac{\pi t}{12}+1.107-3=\frac{\pi}{2}\Rightarrow t=$ Notes: An complete strategy to find $t$ from "
       r"$\frac{\pi t}{12}\pm1.107-3=\frac{\pi}{2}$. Follow through on their 1.107 but the angle must be in radians. It is "
       r"possible via degrees but only using $15t\pm63.4-171.9=90$",
       r"A1 (AO 1.1b): $t=$ awrt 13.2. Notes: awrt $t=13.2$",
       r"A1 (AO 3.2a): Either 13:14 or 1:14 pm or 13 hours 14 minutes after midnight. Notes: The question asks for the "
       r"time of day so accept either 13:14, 1:14 pm, 13 hours 14 minutes after midnight, 13h 14, or 1 hour 14 minutes "
       r"after midday. If in doubt use review",
       r"ALT: It is possible to attempt parts (b) and (c) via differentiation but it is unlikely to yield correct "
       r"results. — M1 A1 A1: $\frac{\mathrm{d}\theta}{\mathrm{d}t}=\frac{\pi}{12}\cos\left(\frac{\pi t}{12}"
       r"-3\right)-\frac{2\pi}{12}\sin\left(\frac{\pi t}{12}-3\right)=0\Rightarrow\tan\left(\frac{\pi t}{12}-3\right)="
       r"\frac{1}{2}\Rightarrow t=13.23=13:14$ scores M1 A1 A1",
       r"ALT: Via differentiation — M1 A0 A1 (SC): $\frac{\mathrm{d}\theta}{\mathrm{d}t}=\cos\left(\frac{\pi t}{12}-3\right)"
       r"-2\sin\left(\frac{\pi t}{12}-3\right)=0\Rightarrow\tan\left(\frac{\pi t}{12}-3\right)=\frac{1}{2}\Rightarrow "
       r"t=13.23=13:14$ they can score M1 A0 A1 (SC) A value of $t=1.23$ implies the minimum value has been found and "
       r"therefore incorrect method M0."],
      False, 12),

    # ---------------- Q7 ----------------
    e("07", "7", ALG, "2.5, 2.3, 3.1", 5, LATEX["07"],
      [r"M1 (AO 1.1b): Attempts equation of line Eg Substitutes $(-2,13)$ into $y=mx+25$ and finds $m$. Notes: The first "
       r"two marks are awarded for finding the equation of the line M1: Uses the information in an attempt to find an "
       r"equation for the line $l$. E.g. Attempt using two points: Finds $m=\pm\frac{25-13}{2}$ and uses of one of the "
       r"points in their $y=mx+c$ or equivalent to find $c$. Alternatively uses the intercept as shown in main scheme.",
       r"A1 (AO 1.1b): Equation of $l$ is $y=6x+25$. Notes: $y=6x+25$ seen or implied. This alone scores the first two "
       r"marks. Do not accept $l=6x+25$ It must be in the form $y=\ldots$ but the correct equation can be implied from an "
       r"inequality. E.g. $\ldots<y<6x+25$ .",
       r"M1 (AO 3.1a): Attempts equation of $C$ Eg Attempts to use the intercept $(0,25)$ within the equation "
       r"$y=a(x\pm2)^2+13$, in order to find $a$. Notes: The next two marks are awarded for finding the equation of the "
       r"curve M1: A complete method to find the constant $a$ in $y=a(x\pm2)^2+13$ or the constants $a$, $b$ in "
       r"$y=ax^2+bx+25$. An alternative to the main scheme is deducing equation is of the form $y=ax^2+bx+25$ and setting "
       r"and solving a pair of simultaneous equations in $a$ and $b$ using the point ( $-2$, 13) the gradient being 0 at "
       r"$x=-2$. Condone slips. Implied by $C=3x^2+12x+25$ or $3x^2+12x+25$ FYI the correct equations are "
       r"$13=4a-2b+25$ $(2a-b=-6)$ and $-4a+b=0$",
       r"A1 (AO 1.1b): Equation of $C$ is $y=3(x+2)^2+13$ or $y=3x^2+12x+25$. Notes: $y=3(x+2)^2+13$ or equivalent such as "
       r"$y=3x^2+12x+25$, $\mathrm{f}(x)=3(x+2)^2+13$. Do not accept $C=3x^2+12x+25$ or just $3x^2+12x+25$ for the A1 but "
       r"may be implied from an inequality or from an attempt at the area, E.g. $\int3x^2+12x+25\,\mathrm{d}x$",
       r"B1ft (AO 2.5): Region $R$ is defined by $3(x+2)^2+13<y<6x+25$ o.e. Notes: Fully defines the region $R$. Follow "
       r"through on their equations for $l$ and $C$. Allow strict or non -strict inequalities as long as they are used "
       r"consistently. E.g. Allow for example “$3(x+2)^2+13<y<6x+25$” “$3(x+2)^2+13\leqslant y\leqslant6x+25$” Allow the "
       r"inequalities to be given separately, e.g. $y<6x+25$, $y>3(x+2)^2+13$. Set notation may be used so "
       r"$\left\{(x,y):y>3(x+2)^2+13\right\}\cap\left\{(x,y):y<6x+25\right\}$ is fine but condone with or without any of "
       r"$(x,y)\leftrightarrow y\leftrightarrow x$ Incorrect examples include “$y<6x+25$ or $y>3(x+2)^2+13$”, "
       r"$\left\{(x,y):y>3(x+2)^2+13\right\}\cup\left\{(x,y):y<6x+25\right\}$ Values of $x$ could be included but they "
       r"must be correct. So $3(x+2)^2+13<y<6x+25,x<0$ is fine If there are multiple solutions mark the final one."],
      True, 16),

    # ---------------- Q8 ----------------
    e("08", "8", DIFF, "7.6, 6.7", 2, LATEX["08"],
      [r"M1 (AO 3.1b): Any equation involving an exponential of the correct form. See notes. Notes: Any equation of the "
       r"correct form, involving $n$ and an exponential in $t$. So allow for example $n=\mathrm{e}^{\pm t}$, "
       r"$n=A\mathrm{e}^{\pm t}$, $n=A\mathrm{e}^{\pm kt}$ condoning $n=A+B\mathrm{e}^{\pm t}$ Condone an intermediate form "
       r"where $n$ has not been made the subject. E.g Allow $\ln n=kt+c$ but also condone $\ln n=kt$",
       r"A1 (AO 1.1b): $n=A\mathrm{e}^{kt}$ (where $A$ and $k$ are positive constants). Notes: E.g. $n=A\mathrm{e}^{kt}$, "
       r"$n=\mathrm{e}^{kt+c}$, $n=\mathrm{e}^{kt}\mathrm{e}^c$ There is no requirement to state that $A$ and $k$ are "
       r"positive constants Note that the two constants need to be different. Mark the final answer so "
       r"$n=\mathrm{e}^{kt+c}$ followed by $n=\mathrm{e}^{kt}+\mathrm{e}^c$ o.e. $n=\mathrm{e}^{kt}+A$ such as is M1 A0",
       r"ALT: You may see solutions that don’t include “e”. These are fine so you can include versions of $n=Ak^t$ using "
       r"the same marking criteria as above FYI $\frac{\mathrm{d}n}{\mathrm{d}t}=Ak^t\times\ln k=\ln k\times n$ so "
       r"$\frac{\mathrm{d}n}{\mathrm{d}t}\propto n$"],
      False, 20),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", DIFF, "7.4", 3, LATEX["09a"],
      [r"M1 (AO 1.1b): $\mathrm{f}(x)=4(x^2-2)\mathrm{e}^{-2x}$ Differentiates to $\mathrm{e}^{-2x}\times8x+4(x^2-2)\times"
       r"-2\mathrm{e}^{-2x}$. Notes: Attempts the product rule and uses $\mathrm{e}^{-2x}\to k\mathrm{e}^{-2x}$, $k\neq0$ "
       r"If candidate states $u=4(x^2-2),v=\mathrm{e}^{-2x}$ with $u'=\ldots,v'=\ldots\mathrm{e}^{-2x}$ it can be implied "
       r"by their $vu'+uv'$ If they just write down an answer without working award for "
       r"$\mathrm{f}'(x)=px\mathrm{e}^{-2x}\pm q(x^2-2)\mathrm{e}^{-2x}$ They may multiply out first "
       r"$\mathrm{f}(x)=4x^2\mathrm{e}^{-2x}-8\mathrm{e}^{-2x}$. Apply in the same way condoning slips Alternatively "
       r"attempts the quotient rule on $\mathrm{f}(x)=\frac{u}{v}=\frac{4(x^2-2)}{\mathrm{e}^{2x}}$ with "
       r"$v'=k\mathrm{e}^{2x}$ and $\mathrm{f}'(x)=\frac{vu'-uv'}{v^2}$",
       r"A1 (AO 1.1b): Differentiates to $\mathrm{e}^{-2x}\times8x+4(x^2-2)\times-2\mathrm{e}^{-2x}$. Notes: A correct "
       r"$\mathrm{f}'(x)$ which may be unsimplified. Via the quotient rule you can award for "
       r"$\mathrm{f}'(x)=\frac{8x\mathrm{e}^{2x}-8(x^2-2)\mathrm{e}^{2x}}{\mathrm{e}^{4x}}$ o.e.",
       r"A1* (AO 2.1): $\mathrm{f}'(x)=8\mathrm{e}^{-2x}\{x-(x^2-2)\}=8(2+x-x^2)\mathrm{e}^{-2x}$ *. Notes: Proceeds "
       r"correctly to given answer showing all necessary steps. The $\mathrm{f}'(x)$ or $\frac{\mathrm{d}y}{\mathrm{d}x}$ "
       r"must be present at some point in the solution This is a “show that” question and there must not be any errors. "
       r"All bracketing must be correct. Allow a candidate to move from the simplified unfactorised answer of "
       r"$\mathrm{f}'(x)=8x\mathrm{e}^{-2x}-8(x^2-2)\mathrm{e}^{-2x}$ to the given answer in one step. Do not allow it from "
       r"an unsimplified $\mathrm{f}'(x)=4\times2x\mathrm{e}^{-2x}+4(x^2-2)\times-2\mathrm{e}^{-2x}$ Allow the expression / "
       r"bracketed expression to be written in a different order. So, for example, $8(x-x^2+2)\mathrm{e}^{-2x}$ is OK"],
      True, 22),
    e("09b", "9(b)", DIFF, "7.3, 7.4", 3, LATEX["09b"],
      [r"B1 (AO 1.1b): States roots of $\mathrm{f}'(x)=0$ $x=-1,2$. Notes: States or implies $x=-1,2$ (as the roots of "
       r"$\mathrm{f}'(x)=0$)",
       r"M1 (AO 1.1b): Substitutes one $x$ value to find a $y$ value. Notes: Substitutes one $x$ value of their solution to "
       r"$\mathrm{f}'(x)=0$ in $\mathrm{f}(x)$ to find a $y$ value. Allow decimals here (3sf). FYI, to 3 sf, "
       r"$-4\mathrm{e}^2=-29.6$ and $8\mathrm{e}^{-4}=0.147$ Some candidates just write down the $x$ coordinates but then "
       r"go on in part (c) to find the ranges using the $y$ coordinates. Allow this mark to be scored from work in part (c)",
       r"A1 (AO 1.1b): Stationary points are $(-1,-4\mathrm{e}^2)$ and $(2,8\mathrm{e}^{-4})$. Notes: Obtains "
       r"$(-1,-4\mathrm{e}^2)$ and $(2,8\mathrm{e}^{-4})$ as the stationary points. This must be scored in (b). Remember to "
       r"isw after a correct answer. Allow these to be written separately. E.g. $x=-1$, $y=-4\mathrm{e}^2$ Extra "
       r"solutions, e.g. from $x=0$ will be penalised on this mark."],
      True, 22),
    e("09c", "9(c)", ALG, "2.9, 2.8", 3, LATEX["09c"],
      [r"B1ft (AO 2.5): (i) Range $[-8\mathrm{e}^2,\infty)$ o.e. such as $\mathrm{g}(x)\geqslant-8\mathrm{e}^2$. Notes: For "
       r"a correct range written using correct notation. Follow through on $2\times$their minimum “$y$” value from part "
       r"(b), providing it is negative. Condone a decimal answer if this is consistent with their answer in (b) to 3sf or "
       r"better. Examples of correct responses are $[-8\mathrm{e}^2,\infty)$, $\mathrm{g}\geqslant-8\mathrm{e}^2$, "
       r"$y\geqslant-8\mathrm{e}^2$, $\left\{q\in\mathbb{R},q\geqslant-8\mathrm{e}^2\right\}$",
       r"M1 (AO 3.1a): (ii) For • Either attempting to find $2\mathrm{f}(0)-3=2\times-8-3=(-19)$ and identifying this as "
       r"the lower bound • Or attempting to find $2\times\text{“}8\mathrm{e}^{-4}\text{”}-3$ and identifying this as the "
       r"upper bound. Notes: See main scheme. Follow through on $2\times$their “$8\mathrm{e}^{-4}$”$-3$ for the upper "
       r"bound.",
       r"A1 (AO 1.1b): Range $[-19,16\mathrm{e}^{-4}-3]$. Notes: Range $[-19,16\mathrm{e}^{-4}-3]$ o.e. such as "
       r"$-19\leqslant y\leqslant16\mathrm{e}^{-4}-3$ but must be exact"],
      True, 22),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", INT, "8.5", 4, LATEX["10a"],
      [r"B1 (AO 1.1b): $x=u^2+1\Rightarrow\mathrm{d}x=2u\,\mathrm{d}u$ oe. Notes: Mark (a) and (b) together as one complete "
       r"question $\mathrm{d}x=2u\,\mathrm{d}u$ or exact equivalent. E.g. $\frac{\mathrm{d}x}{\mathrm{d}u}=2u$, "
       r"$\frac{\mathrm{d}u}{\mathrm{d}x}=\frac{1}{2}(x-1)^{-\frac{1}{2}}$",
       r"M1 (AO 1.1b): Full substitution $\int\frac{3\,\mathrm{d}x}{(x-1)\left(3+2\sqrt{x-1}\right)}=\int\frac{3\times2u\,"
       r"\mathrm{d}u}{(u^2+1-1)(3+2u)}$. Notes: Attempts a full substitution of $x=u^2+1$, including "
       r"$\mathrm{d}x\to\ldots u\,\mathrm{d}u$ to form an integrand in terms of $u$. Condone slips but there should be an "
       r"attempt to use the correct substitution on the denominator.",
       r"B1 (AO 1.1b): Finds correct limits e.g. $p=2,q=3$. Notes: Finds correct limits either states $p=2,q=3$ or sight of "
       r"embedded values as limits to the integral",
       r"A1* (AO 2.1): $=\int\frac{3\times2u\,\mathrm{d}u}{u^2(3+2u)}=\int\frac{6\,\mathrm{d}u}{u(3+2u)}$ *. Notes: Clear "
       r"reasoning including one fully correct intermediate line, including the integral signs, leading to the given "
       r"expression ignoring limits. So B1, M1, B0, A1 is possible if the limits are incorrect, omitted or left as 5 and "
       r"10."],
      False, 26),
    e("10b", "10(b)", INT, "8.6, 2.10, 6.4", 6, LATEX["10b"],
      [r"M1 (AO 1.1b): $\frac{6}{u(3+2u)}=\frac{A}{u}+\frac{B}{3+2u}\Rightarrow A=\ldots,B=\ldots$ Notes: Uses correct form "
       r"of PF leading to values of $A$ and $B$.",
       r"A1 (AO 1.1b): Correct PF. $\frac{6}{u(3+2u)}=\frac{2}{u}-\frac{4}{3+2u}$. Notes: Correct PF "
       r"$\frac{6}{u(3+2u)}=\frac{2}{u}-\frac{4}{3+2u}$ (Not scored for just the correct values of $A$ and $B$)",
       r"dM1 (AO 3.1a): $\int\frac{6\,\mathrm{d}u}{u(3+2u)}=2\ln u-2\ln(3+2u)$ $(+c)$. Notes: This is an overall problem "
       r"solving mark. It is for using the correct PF form and integrating using lns. Look for $P\ln u+Q\ln(3+2u)$",
       r"A1ft (AO 1.1b): $\int\frac{6\,\mathrm{d}u}{u(3+2u)}=2\ln u-2\ln(3+2u)$ $(+c)$. Notes: Correct integration for "
       r"their $\frac{A}{u}+\frac{B}{3+2u}\to A\ln u+\frac{B}{2}\ln(3+2u)$ with or without modulus signs",
       r"M1 (AO 1.1b): Uses limits $u=\text{“}3\text{”},u=\text{“}2\text{”}$ with some correct ln work leading to $k\ln b$ "
       r"E.g. $(2\ln3-2\ln9)-(2\ln2-2\ln7)=2\ln\frac{7}{6}$. Notes: Uses their 2 and 3 as limits, with at least one correct "
       r"application of the addition law or subtraction law leading to the form $k\ln b$ or $\ln a$. PF’s must have been "
       r"attempted. Condone bracketing slips. Alternatively changing the $u$’s back to $x$’s and use limits of 5 and 10.",
       r"A1 (AO 2.1): $\ln\frac{49}{36}$. Notes: Proceeds to $\ln\frac{49}{36}$. Answers without working please send to "
       r"review."],
      False, 26),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", COORD, "3.2, 5.1, 2.4", 4, LATEX["11a"],
      [r"M1 (AO 3.1a): Solves $x^2+y^2=100$ and $(x-15)^2+y^2=40$ simultaneously to find $x$ or $y$ E.g. "
       r"$(x-15)^2+100-x^2=40\Rightarrow x=\ldots$ Notes: For the key step in an attempt to find either coordinate for "
       r"where the two circles meet. Look for an attempt to set up an equation in a single variable leading to a value for "
       r"$x$ or $y$.",
       r"A1 (AO 1.1b): Either $\Rightarrow-30x+325=40\Rightarrow x=9.5$ Or $y=\frac{\sqrt{39}}{2}=$ awrt $\pm3.12$. Notes: "
       r"$x=9.5$ (or $y=\frac{\sqrt{39}}{2}=$ awrt $\pm3.12$ )",
       r"M1 (AO 3.1a): Attempts to find the angle $AOB$ in circle $C_1$ Eg Attempts $\cos\alpha=\frac{\text{“}9.5\text{”}}"
       r"{10}$ to find $\alpha$ then $\times2$. Notes: Uses the radius of the circle and correct trigonometry in an attempt "
       r"to find angle $AOB$ in circle $C_1$ E.g. Attempts $\cos\alpha=\frac{\text{“}9.5\text{”}}{10}$ to find $\alpha$ "
       r"then $\times2$ Alternatives include $\tan\alpha=\frac{\sqrt{100-\text{“}9.5\text{”}^2}}{\text{“}9.5\text{”}}="
       r"(0.3286\ldots)$ to find $\alpha$ then $\times2$ And $\cos AOB=\frac{10^2+10^2-\left(\sqrt{39}\right)^2}{2\times10"
       r"\times10}=\frac{161}{200}$",
       r"A1* (AO 2.1): Angle $AOB=2\times\arccos\left(\frac{9.5}{10}\right)=0.635$ rads (3sf) *. Notes: Correct and "
       r"careful work in proceeding to the given answer. Condone an answer with greater accuracy. Condone a solution where "
       r"the intermediate value has been truncated, provided the trig equation is correct. E.g. "
       r"$\sin\alpha=\frac{\sqrt{39}}{20}\Rightarrow\alpha=0.317\Rightarrow AOB=2\alpha=0.635$ Condone a solution written "
       r"down from awrt $36.4^\circ$ (without the need to shown any calculation.) E",
       r"ALT: Alternative (a) using triangle $OAX$ (the mark scheme's diagram shows $OA=10$, $AX=\sqrt{40}$, $OX=15$, "
       r"angles $\alpha$ at $O$ and $\beta$ at $X$) — M1: For the key step in attempting to find all lengths in triangle "
       r"$OAX$, condoning slips",
       r"ALT: Alternative (a) using triangle $OAX$ — A1: All three lengths correct",
       r"ALT: Alternative (a) using triangle $OAX$ — M1: Attempts cosine rule to find $\alpha$ then $\times2$",
       r"ALT: Alternative (a) using triangle $OAX$ — A1*: Correct and careful work in proceeding to the given answer"],
      True, 30),
    e("11b", "11(b)", TRIG, "5.1, 3.2", 4, LATEX["11b"],
      [r"M1 (AO 1.1b): Attempts $10\times(2\pi-0.635)=56.48$. Notes: Attempts to use the formula $s=r\theta$ with $r=10$ "
       r"and $\theta=2\pi-0.635$ The formula may be embedded. You may see $2\pi10+2\pi\sqrt{40}-10\times0.635\ldots$ which "
       r"is fine for this M1",
       r"M1 (AO 3.1a): Attempts to find angle $AXB$ or $AXO$ in circle $C_2$ (see diagram) E.g. "
       r"$\cos\beta=\frac{15-\text{“}9.5\text{”}}{\sqrt{40}}\Rightarrow\beta=\ldots$ (Note $AXB=1.03$ rads). Notes: Attempts "
       r"to use a correct method in order to find angle $AXB$ or $AXO$ in circle $C_2$ Amongst many other methods are "
       r"$\tan\beta=\frac{\text{“}3.12\text{”}}{15-9.5}$ and $\cos AXB=\frac{40+40-\left(\sqrt{39}\right)^2}{2\times"
       r"\sqrt{40}\times\sqrt{40}}=\frac{41}{80}$ Note that many candidates believe this to be 0.635. This scores M0 dM0 "
       r"A0 [The mark scheme's diagram shows $OA=10$, $AX=\sqrt{40}$, the chord $AB$ meeting $OX$ with lengths 9.5 and 5.5, "
       r"angle $AOB=0.635$* and angle $AXB=1.03$.]",
       r"dM1 (AO 2.1): Attempts $10\times(2\pi-0.635)+\sqrt{40}\times(2\pi-2\beta)$. Notes: A full and complete attempt to "
       r"find the perimeter of the region. It is dependent upon having scored both M’s.",
       r"A1 (AO 1.1b): $=89.7$. Notes: awrt 89.7"],
      True, 30),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", TRIG, "5.8, 5.4, 5.5", 3, LATEX["12a"],
      [r"B1 (AO 1.2): States or uses $\mathrm{cosec}\,\theta=\frac{1}{\sin\theta}$. Notes: (a) Condone a full proof in $x$ "
       r"(or other variable) instead of $\theta$’s here States or uses $\mathrm{cosec}\,\theta=\frac{1}{\sin\theta}$ Do not "
       r"accept $\mathrm{cosec}\,\theta=\frac{1}{\sin}$ with the $\theta$ missing",
       r"M1 (AO 2.1): $\mathrm{cosec}\,\theta-\sin\theta=\frac{1}{\sin\theta}-\sin\theta=\frac{1-\sin^2\theta}{\sin\theta}$. "
       r"Notes: For the key step in forming a single fraction/common denominator E.g. $\mathrm{cosec}\,\theta-\sin\theta="
       r"\frac{1}{\sin\theta}-\sin\theta=\frac{1-\sin^2\theta}{\sin\theta}$. Allow if written separately "
       r"$\frac{1}{\sin\theta}-\sin\theta=\frac{1}{\sin\theta}-\frac{\sin^2\theta}{\sin\theta}$ Condone missing variables "
       r"for this M mark",
       r"A1* (AO 2.1): $=\frac{\cos^2\theta}{\sin\theta}=\cos\theta\times\frac{\cos\theta}{\sin\theta}=\cos\theta\cot\theta$ "
       r"*. Notes: Shows careful work with all necessary steps shown leading to given answer. See scheme for necessary "
       r"steps. There should not be any notational or bracketing errors.",
       rf"{A12} — B1 (AO 1.2): States or uses $\cot\theta=\frac{{\cos\theta}}{{\sin\theta}}$",
       rf"{A12} — M1 (AO 2.1): $\cos\theta\cot\theta=\frac{{\cos^2\theta}}{{\sin\theta}}=\frac{{1-\sin^2\theta}}"
       rf"{{\sin\theta}}$",
       rf"{A12} — A1* (AO 2.1): $=\frac{{1}}{{\sin\theta}}-\sin\theta=\mathrm{{cosec}}\,\theta-\sin\theta$ *",
       rf"{B12} — B1 (AO 1.2): States or uses $\cot\theta=\frac{{\cos\theta}}{{\sin\theta}}$ or "
       rf"$\mathrm{{cosec}}\,\theta=\frac{{1}}{{\sin\theta}}$",
       rf"{B12} — M1 (AO 2.1): $LHS=\frac{{1}}{{\sin\theta}}-\sin\theta=\frac{{1-\sin^2\theta}}{{\sin\theta}}="
       rf"\frac{{\cos^2\theta}}{{\sin\theta}}$ $RHS=\cos\theta\cot\theta=\frac{{\cos^2\theta}}{{\sin\theta}}$",
       rf"{B12} — A1* (AO 2.1): States a conclusion E.g. “HENCE TRUE”, “QED” or $\mathrm{{cosec}}\,\theta-\sin\theta\equiv"
       rf"\cos\theta\cot\theta$ o.e. (condone = for ≡)"],
      False, 34),
    e("12b", "12(b)", TRIG, "5.7, 5.4", 5, LATEX["12b"],
      [r"M1 (AO 3.1a): $\mathrm{cosec}\,x-\sin x=\cos x\cot(3x-50^\circ)\Rightarrow\cos x\cot x=\cos x\cot(3x-50^\circ)$ "
       r"$\cot x=\cot(3x-50^\circ)\Rightarrow x=3x-50^\circ$. Notes: (b) Condone $\theta$’s instead of $x$’s here Uses part "
       r"(a), cancels or factorises out the $\cos x$ term, to establish that one solution is found when $x=3x-50^\circ$. "
       r"You may see solutions where $\cot A-\cot B=0\Rightarrow\cot(A-B)=0$ or $\tan A-\tan B=0\Rightarrow\tan(A-B)=0$. "
       r"As long as they don’t state $\cot A-\cot B=\cot(A-B)$ or $\tan A-\tan B=\tan(A-B)$ this is acceptable",
       r"A1 (AO 1.1b): $x=25^\circ$. Notes: $x=25^\circ$",
       r"M1 (AO 2.1): Also $\cot x=\cot(3x-50^\circ)\Rightarrow x+180^\circ=3x-50^\circ$. Notes: For the key step in "
       r"realising that $\cot x$ has a period of $180^\circ$ and a second solution can be found by solving "
       r"$x+180^\circ=3x-50^\circ$. The sight of $x=115^\circ$ can imply this mark provided the step $x=3x-50^\circ$ has "
       r"been seen. Using reciprocal functions it is for realising that $\tan x$ has a period of $180^\circ$",
       r"A1 (AO 1.1b): $x=115^\circ$. Notes: $x=115^\circ$ Withhold this mark if there are additional values in the range "
       r"(0,180) but ignore values outside.",
       r"B1 (AO 2.2a): Deduces $x=90^\circ$. Notes: Deduces that a solution can be found from "
       r"$\cos x=0\Rightarrow x=90^\circ$. Ignore additional values here. Solutions with limited working. The question "
       r"demands that candidates show all stages of working. SC: $\cos x\cot x=\cos x\cot(3x-50^\circ)\Rightarrow\cot x="
       r"\cot(3x-50^\circ)\Rightarrow x=25^\circ,115^\circ$ They have shown some working so can score B1, B1 marked on epen "
       r"as 11000",
       rf"{C12} — M1 (AO 3.1a): $\cot x=\cot(3x-50^\circ)\Rightarrow\frac{{\cos x}}{{\sin x}}=\frac{{\cos(3x-50^\circ)}}"
       rf"{{\sin(3x-50^\circ)}}$ $\sin(3x-50^\circ)\cos x-\cos(3x-50^\circ)\sin x=0$ $\sin((3x-50^\circ)-x)=0$ "
       rf"$2x-50^\circ=0$",
       rf"{C12} — A1 (AO 1.1b): $x=25^\circ$",
       rf"{C12} — M1 (AO 2.1): Also $2x-50^\circ=180^\circ$",
       rf"{C12} — A1 (AO 1.1b): $x=115^\circ$",
       rf"{C12} — B1 (AO 2.2a): Deduces $\cos x=0\Rightarrow x=90^\circ$"],
      False, 34),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", SEQ, "4.2", 3, LATEX["13a"],
      [r"M1 (AO 1.1b): Uses the sequence formula $a_{n+1}=\frac{k(a_n+2)}{a_n}$ once with $a_1=2$. Notes: Applies the "
       r"sequence formula $a_{n+1}=\frac{k(a_n+2)}{a_n}$ seen once. This is usually scored in attempting to find the second "
       r"term. E.g. for $a_2=2k$ or $a_{1+1}=\frac{k(2+2)}{2}$",
       r"M1 (AO 3.1a): $(a_1=2),a_2=2k,a_3=k+1,a_4=\frac{k(k+3)}{k+1}$ Finds four consecutive terms and sets $a_4$ equal to "
       r"$a_1$ (oe). Notes: Attempts to find $a_1\to a_4$ and sets $a_1=a_4$. Condone slips. Other methods are available. "
       r"E.g. Set $a_4=2$, work backwards to find $a_3$ and equate to $k+1$ There is no requirement to see either $a_1$ or "
       r"any of the labels. Look for the correct terms in the correct order. There is no requirement for the terms to be "
       r"simplified FYI $a_1=2$, $a_2=2k$, $a_3=k+1$, $a_4=\frac{k(k+3)}{k+1}$ and so $2=\frac{k(k+3)}{k+1}$",
       r"A1* (AO 2.1): $\frac{k(k+3)}{k+1}=2\Rightarrow k^2+3k=2k+2\Rightarrow k^2+k-2=0$ *. Notes: Proceeds to the given "
       r"answer with accurate work showing all necessary lines. See MS for minimum"],
      False, 38),
    e("13b", "13(b)", SEQ, "4.2", 1, LATEX["13b"],
      [r"B1 (AO 2.3): States that when $k=1$, all terms are the same and concludes that the sequence does not have a "
       r"period of order 3. Notes: States that when $k=1$, all terms are the same and concludes that the sequence does not "
       r"have a period of order 3. Do not accept “the terms just repeat” or “it would mean all the terms of the sequence "
       r"are 2” There must be some reference to the fact that it does not have order 3. Accept it has order 1. It is "
       r"acceptable to state $a_2=a_1=2$ and state that the sequence does not have order 3"],
      False, 38),
    e("13c", "13(c)", SEQ, "4.3, 4.2", 3, LATEX["13c"],
      [r"B1 (AO 2.2a): Deduces the repeating terms are $a_{1/4}=2,a_{2/5}=-4,a_{3/6}=-1$,. Notes: Deduces the repeating "
       r"terms are $a_{1/4}=2,a_{2/5}=-4,a_{3/6}=-1$,",
       r"M1 (AO 3.1a): $\sum_{n=1}^{80}a_k=26\times(2+-4+-1)+2+-4$. Notes: Uses a clear strategy to find the sum to 80 "
       r"terms. This will usually be found using multiples of the first three terms. For example you may see "
       r"$\sum_{r=1}^{80}a_r=\left(\sum_{r=1}^{78}a_r\right)+a_{79}+a_{80}=26\times(2+-4+-1)+2+-4$ or "
       r"$\sum_{r=1}^{80}a_r=\left(\sum_{r=1}^{81}a_r\right)-a_{81}=27\times(2+-4+-1)-(-1)$ For candidates who find in terms "
       r"of $k$ award for $27\times2+27\times(2k)+26\times(k+1)$ or $80k+80$ If candidates proceed and substitute $k=-2$ "
       r"into $80k+80$ to get $-80$ then all 3 marks are scored.",
       r"A1 (AO 1.1b): $=-80$. Notes: $-80$ Note: Be aware that we have seen candidates who find the first three terms "
       r"correctly, but then find $26\frac{2}{3}\times(2+-4+-1)=26\frac{2}{3}\times-3$ which gives the correct answer but "
       r"it is an incorrect method and should be scored B1 M0 A0"],
      False, 38),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", DIFF, "7.6, 7.4", 3, LATEX["14a"],
      [rf"B1 (AO 3.1b): Uses the model to state ${DV}=-c$ (for positive constant $c$). Notes: Uses the model to state "
       rf"${DV}=-c$ (for positive constant $c$). Any “letter” is acceptable here including $k$. Note that ${DV}=c$ is B0 "
       rf"unless they state that $c$ is a negative constant.",
       rf"M1 (AO 2.1): Uses ${DV}={DVR}\times{DRT}$ with their ${DV}=-c$ and ${DVR}=4\pi r^2$. Notes: For an attempt to "
       rf"use ${DV}={DVR}\times{DRT}$ with their ${DV}$ and ${DVR}=4\pi r^2$ Allow for an attempt to use "
       rf"${DV}={DVR}\times{DRT}$ with their ${DV}$ and ${DVR}=\lambda r^2$ (Any constant is fine) There is no requirement "
       rf"to use the correct formula for the volume of a sphere for this mark.",
       rf"A1* (AO 2.2a): $-c=4\pi r^2\times{DRT}\Rightarrow{DRT}=-\frac{{c}}{{4\pi r^2}}=-\frac{{k}}{{r^2}}$ *. Notes: "
       rf"Proceeds to the given answer with an intermediate line equivalent to ${DRT}=-\frac{{c}}{{4\pi r^2}}$ If candidate "
       rf"started with ${DV}=-k$ they must provide a minimal explanation how ${DRT}=-\frac{{k}}{{4\pi r^2}}\to{DRT}="
       rf"-\frac{{k}}{{r^2}}$. E.g $\frac{{1}}{{4\pi}}$ is a constant so replace $\frac{{k}}{{4\pi}}$ with $k$ It is not "
       rf"necessary to use the full formula for the volume of a sphere, eg allow $V=\kappa r^3$ but if it has been quoted "
       rf"it must be correct. So using $V=4r^3$ can potentially score 2 of the 3 marks."],
      False, 42),
    e("14b", "14(b)", INT, "8.7, 8.8", 5, LATEX["14b"],
      [rf"M1 (AO 2.1): ${DRT}=-\frac{{k}}{{r^2}}\Rightarrow\int r^2\,\mathrm{{d}}r=\int-k\,\mathrm{{d}}t$ and integrates "
       rf"with one side “correct”. Notes: For the key step of separating the variables correctly AND integrating one side "
       rf"with at least one index correct. The integral signs do not need to be seen.",
       r"A1 (AO 1.1b): $\frac{r^3}{3}=-kt(+\alpha)$. Notes: Correct integration E.g. $\frac{r^3}{3}=-kt(+\alpha)$ or "
       r"equivalent. The $+\alpha$ is not required for this mark. This may be awarded if $k$ has been given a value.",
       r"M1 (AO 1.1b): Uses $t=0,r=40\Rightarrow\alpha=\ldots$ $\alpha=\frac{64000}{3}$. Notes: Uses the initial "
       r"conditions to find a value for the constant of integration $\alpha$ If a constant of integration is not present, "
       r"or $k$ has been given a pre defined value, then only the first two marks can be awarded in part (b) The mark may "
       r"be awarded if the equation has been adapted incorrectly. E.g. each term cube rooted.",
       r"M1 (AO 3.4): Uses $t=5,r=20$ & $\alpha=\ldots\Rightarrow k=\ldots$ Notes: Uses the second set of conditions with "
       r"their value of $\alpha$ to find $k$ This may be awarded if the equation has been adapted incorrectly. E.g. each "
       r"term cube rooted.",
       r"A1 (AO 3.3): $r^3=64000-11200t$ or exact equivalent. Notes: Obtains any correct equation for the model. E.g. "
       r"$r^3=64000-11200t$ or exact equivalent such as $\frac{r^3}{3}=\frac{64000}{3}-\frac{11200}{3}t$. ISW after sight "
       r"of a correct answer. Condone recurring decimals e.g. $21333.\dot{3}$ for $\frac{64000}{3}$ Do not award if only "
       r"the rounded/truncated decimal equivalents to say $\frac{64000}{3}$ is used."],
      False, 42),
    e("14c", "14(c)", INT, "8.8", 2, LATEX["14c"],
      [r"M1 (AO 3.4): Uses the equation of their model and proceeds to a limiting value for $t$ E.g. "
       r"“$64000-11200t$”$\ldots0\Rightarrow t\ldots$ Notes: Recognises that the model is only valid when $r\geqslant0$ and "
       r"uses this to find $t$. Condone $r>0$ Award for an attempt to find the value of $t$ when $r=0$. See scheme. It must "
       r"be from an equation of the form $ar^n=b-ct$, $a,b,c>0$ which give + ve values of $t$.",
       r"A1ft (AO 3.5b): For times up to and including $\frac{40}{7}$ seconds. Notes: Allow valid for times up to (and "
       r"including) $\frac{40}{7}$ seconds, 5.71 seconds. Allow $t<\frac{40}{7}$ or $t\leqslant\frac{40}{7}$ There is no "
       r"requirement for the left hand side of the inequality, 0 States invalid for times greater than $\frac{40}{7}$ "
       r"seconds, 5.71 seconds. Follow through on their equation so allow $t<$ their “$\frac{64000}{11200}$” as long as "
       r"this value is greater than 5 ( $t=5$ is one of the values in the question)"],
      False, 42),

    # ---------------- Q15 ----------------
    e("15a", "15(a)", DIFF, "7.5, 5.5", 4, LATEX["15a"],
      [rf"M1 (AO 3.1a): $x^2\tan y=9\Rightarrow2x\tan y+x^2\sec^2y{DY}=0$. Notes: Attempts to differentiate $\tan y$ "
       rf"implicitly. Eg. $\tan y\to\sec^2y{DY}$ or $\cot y\to-\mathrm{{cosec}}^2y{DY}$ You may well see an attempt "
       rf"$\tan y=\frac{{9}}{{x^2}}\Rightarrow\sec^2y{DY}=\ldots$ When a candidate writes $x^2\tan y=9\Rightarrow "
       rf"x=3\tan^{{-\frac{{1}}{{2}}}}y$ the mark is scored for $\tan^{{-\frac{{1}}{{2}}}}y\to\ldots\tan^{{-\frac{{3}}{{2}}}}y"
       rf"\sec^2y$",
       rf"A1 (AO 1.1b): $x^2\tan y=9\Rightarrow2x\tan y+x^2\sec^2y{DY}=0$. Notes: Correct differentiation "
       rf"$2x\tan y+x^2\sec^2y{DY}=0$ Allow also $\sec^2y{DY}=-\frac{{18}}{{x^3}}$ or $2x=-9\mathrm{{cosec}}^2y{DY}$ amongst "
       rf"others",
       rf"M1 (AO 1.1b): Full method to get ${DY}$ in terms of $x$ using $\sec^2y=1+\tan^2y=1+\mathrm{{f}}(x)$. Notes: Full "
       rf"method to get ${DY}$ in terms of $x$ using $\sec^2y=1+\tan^2y=1+\mathrm{{f}}(x)$",
       rf"A1* (AO 2.1): ${DY}=\frac{{-2x\times\frac{{9}}{{x^2}}}}{{x^2\left(1+\frac{{81}}{{x^4}}\right)}}="
       rf"\frac{{-18x}}{{x^4+81}}$ *. Notes: Proceeds correctly to the given answer of ${DY}=\frac{{-18x}}{{x^4+81}}$",
       rf"ALT: Alternative part (a) using arctan — M1: Sets $y=\arctan\frac{{9}}{{x^2}}\to{DY}=\frac{{1}}{{1+"
       rf"\left(\frac{{9}}{{x^2}}\right)^2}}\times\ldots$ where ... could be 1",
       rf"ALT: Alternative part (a) using arctan — A2: $y=\arctan\frac{{9}}{{x^2}}\to{DY}=\frac{{1}}{{1+\left(\frac{{9}}"
       rf"{{x^2}}\right)^2}}\times-\frac{{18}}{{x^3}}$",
       rf"ALT: Alternative part (a) using arctan — A1*: ${DY}=\frac{{1}}{{1+\frac{{81}}{{x^4}}}}\times-\frac{{18}}{{x^3}}="
       rf"\frac{{-18x}}{{x^4+1}}$ [sic: the question and main scheme have $x^4+81$] showing correct intermediate step and "
       rf"no errors."],
      False, 46),
    e("15b", "15(b)", DIFF, "7.3", 3, LATEX["15b"],
      [rf"M1 (AO 1.1b): ${DY}=\frac{{-18x}}{{x^4+81}}\Rightarrow{D2Y}=\frac{{-18\times(x^4+81)-(-18x)(4x^3)}}{{(x^4+81)^2}}"
       rf"=\frac{{54(x^4-27)}}{{(x^4+81)^2}}$ o.e. Notes: Attempts to differentiate the given expression using the product "
       rf"or quotient rule. For example look for a correct attempt at $\frac{{vu'-uv'}}{{v^2}}$ with "
       rf"$u=-18x,v=x^4+81,u'=\pm18,v'=\ldots x^3$ If no method is seen or implied award for "
       rf"$\frac{{\pm18\times(x^4+81)\pm18x(ax^3)}}{{(x^4+81)^2}}$ Using the product rule award for "
       rf"$\pm18(x^4+81)^{{-1}}\pm18x(x^4+81)^{{-2}}\times cx^3$",
       rf"A1 (AO 1.1b): ${D2Y}=\frac{{54(x^4-27)}}{{(x^4+81)^2}}$ o.e. Notes: Correct simplified "
       rf"${D2Y}=\frac{{54(x^4-27)}}{{(x^4+81)^2}}$ o.e. such as ${D2Y}=\frac{{54x^4-1458}}{{(x^4+81)^2}}$ Alternatively score "
       rf"for showing that when a correct (unsimplified) ${D2Y}=0\Rightarrow x^4=27\Rightarrow x=\sqrt[4]{{27}}$ Or for "
       rf"substituting $x=\sqrt[4]{{27}}$ into an unsimplified but correct ${D2Y}$ and showing that it is 0",
       rf"A1 (AO 2.4): States that when $x<\sqrt[4]{{27}}\Rightarrow{D2Y}<0$ when $x=\sqrt[4]{{27}}\Rightarrow{D2Y}=0$ AND "
       rf"when $x>\sqrt[4]{{27}}\Rightarrow{D2Y}>0$ giving a point of inflection when $x=\sqrt[4]{{27}}$. Notes: Correct "
       rf"explanation with a minimal conclusion and correct second derivative. See scheme. It can be also be argued from "
       rf"$x^4<27$, $x^4=27$ and $x^4>27$ provided the conclusion states that the point of inflection is at "
       rf"$x=\sqrt[4]{{27}}$ Alternatively substitutes values of $x$ either side of $\sqrt[4]{{27}}$ and at "
       rf"$\sqrt[4]{{27}}$, into ${D2Y}$, finds all three values and makes a minimal conclusion. A different method "
       rf"involves finding $\frac{{\mathrm{{d}}^3y}}{{\mathrm{{d}}x^3}}$ and showing that "
       rf"$\frac{{\mathrm{{d}}^3y}}{{\mathrm{{d}}x^3}}\neq0$ and ${D2Y}=0$ when $x=\sqrt[4]{{27}}$ FYI "
       rf"$\frac{{\mathrm{{d}}^3y}}{{\mathrm{{d}}x^3}}=\frac{{23328x^3}}{{(x^4+81)^3}}=0.219$ when $x=\sqrt[4]{{27}}$"],
      False, 46),

    # ---------------- Q16 ----------------
    e("16", "16", PROOF, "1.1, 2.6", 4, LATEX["16"],
      [r"M1 (AO 2.1): Sets up the contradiction and factorises: There are positive integers $p$ and $q$ such that "
       r"$(2p+q)(2p-q)=25$. Notes: For the key step in setting up the contradiction and factorising",
       r"M1 (AO 2.2a): If true then $2p+q=25$, $2p-q=1$ or $2p+q=5$, $2p-q=5$ Award for deducing either of the above "
       r"statements. Notes: For deducing that for $p$ and $q$ to be integers then either $2p+q=25$, $2p-q=1$ or $2p+q=5$, "
       r"$2p-q=5$ must be true. Award for deducing either of the above statements. You can ignore any reference to "
       r"$2p+q=1$, $2p-q=25$ as this could not occur for positive $p$ and $q$.",
       r"A1 (AO 1.1b): Solutions are $p=6.5,q=12$ or $p=2.5,q=0$ Award for one of these. Notes: For correctly solving one "
       r"of the given statements, For $2p+q=25$, $2p-q=1$ candidates only really need to proceed as far as $p=6.5$ to show "
       r"the contradiction. For $2p+q=5$, $2p-q=5$ candidates only really need to find either $p$ or $q$ to show the "
       r"contradiction. Alt for $2p+q=5$, $2p-q=5$ candidates could state that $2p+q\neq2p-q$ if $p,q$ are positive "
       r"integers.",
       r"A1 (AO 2.1): This is a contradiction as there are no integer solutions hence there are no positive integers $p$ "
       r"and $q$ such that $4p^2-q^2=25$. Notes: For a complete and rigorous argument with both possibilities and a "
       r"correct conclusion.",
       rf"{Q16A} — M1 (AO 2.1): Sets up the contradiction, attempts to make $q^2$ or $4p^2$ the subject and states that "
       rf"either $4p^2$ is even(*) , or that $q^2$ (or $q$) is odd (**) Either There are positive integers $p$ and $q$ such "
       rf"that $4p^2-q^2=25\Rightarrow q^2=4p^2-25$ with * or ** Or There are positive integers $p$ and $q$ such that "
       rf"$4p^2-q^2=25\Rightarrow4p^2=q^2+25$ with * or **",
       rf"{Q16A} — M1 (AO 2.2a): Sets $q=2n\pm1$ and expands $(2n\pm1)^2=4p^2-25$",
       rf"{Q16A} — A1 (AO 1.1b): Proceeds to an expression such as $4p^2=4n^2+4n+26=4(n^2+n+6)+2$ "
       rf"$4p^2=4n^2+4n+26=4(n^2+n)+\frac{{13}}{{2}}$ $p^2=n^2+n+\frac{{13}}{{2}}$",
       rf"{Q16A} — A1 (AO 2.1): States This is a contradiction as $4p^2$ must be a multiple of 4 Or $p^2$ must be an "
       rf"integer And concludes there are no positive integers $p$ and $q$ such that $4p^2-q^2=25$",
       rf"{Q16B} — M1: An approach using odd and even numbers is unlikely to score marks. To make this consistent with the "
       rf"Alt method, score M1: Set up the contradiction and start to consider one of the cases below where $q$ is odd, "
       rf"$m\neq n$. Solutions using the same variable will score no marks. [Cases: $p$ (even) $q$ (odd): "
       rf"$4p^2-q^2=4\times(2m)^2-(2n+1)^2=16m^2-4n^2-4n-1$, one less than a multiple of 4 so cannot equal 25; $p$ (odd) "
       rf"$q$ (odd): $4p^2-q^2=4\times(2m+1)^2-(2n+1)^2=16m^2+16m-4n^2-4n+3$, three more than a multiple of 4 so cannot "
       rf"equal 25]",
       rf"{Q16B} — M1: Set up the contradiction and start to consider BOTH cases below where $q$ is odd, $m\neq n$. No "
       rf"requirement for evens",
       rf"{Q16B} — A1: Correct work and deduction for one of the two scenarios where $q$ is odd",
       rf"{Q16B} — A1: Correct work and deductions for both scenarios where $q$ is odd with a final conclusion"],
      False, 50),
]

# Examiner report, sentence by sentence, in report order (the opening section on
# the 2020 paper changes is not attached to any question). Bulleted lists are
# joined into the sentence that introduces them, with "; ".
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "As hoped for, this proved to be a gentle and accessible start to the paper.", NO),
        ({"a"}, "The majority of prepared candidates scored all available marks in part (a)."),
        ({"a"}, "Errors, although rare, were mainly seen in the failure not to square the 8 of $(8x)^2$."),
        ({"b"}, "Part (b) was found to be more demanding."),
        ({"b"}, r"Successful students substituted $x=\frac{1}{32}$ into $(1+8x)^{\frac{1}{2}}$ and noted that the result "
                r"was $\frac{\sqrt{5}}{2}$."),
        ({"b"}, r"It then became a simple task of stating that you merely needed to substitute $x=\frac{1}{32}$ into the "
                r"expansion in (a) and multiply the result by 2.", NO),
        ({"b"}, "Concise explanations are still a weakness in the early years of this specification.", NO),
    ],
    "02": [
        (W, "As with question 1 there were many fully correct answers here."),
        (W, "Of these, most took logs or lns of both sides, then used the power law on each side and the correct order "
            "of operations before proceeding to the correct answer of 81.6.", BACK),
        (W, "There were a few candidates who failed to put brackets around $(3p-1)$ but they were usually able to "
            "recover."),
        (W, "There were several cases of candidates failing to apply the power rule to both sides, usually not dealing "
            "with the ‘210’."),
        (W, "Some candidates misapplied the power rule, multiplying first for example by 3, rather than $3p-1$."),
        (W, r"Common errors were after applying the power rule correctly changing $\log5/\log4$ to $\log(5/4)$; taking "
            r"either $\log_4$ of one side or $\log_5$ of the other without any application of the power law"),
    ],
    "03": [
        ({"a"}, "In part (a) most candidates were able to successfully subtract vectors the correct way round gaining "
                "both marks."),
        ({"a"}, "Very few candidates added the two vectors together."),
        ({"b"}, "In (b) those who gained both marks were able to compare the two vectors $AB$ and $OC$ to show that they "
                "were parallel and conclude that $OABC$ is a trapezium.", NO),
        ({"b"}, "Usually candidates made a sketch of a trapezium so they could visualize which vectors or sides they "
                "would compare."),
        ({"b"}, "This is a very good idea and should be encouraged by centres.", BACK),
        ({"b"}, r"Marks were lost when candidates did not give a minimal conclusion after finding $OC$ and $AB$ were "
                r"parallel; candidates incorrectly stating that $\overrightarrow{AB}=2\times\overrightarrow{OC}$; "
                r"candidates finding the length of each side $OABC$ rather than their directions"),
    ],
    "04": [
        (W, "This was a relatively straightforward test on function notation.", NO),
        ({"a"}, r"In part (a) most candidates opted to find the inverse function $\mathrm{f}^{-1}(x)$ before substituting "
                r"in $x=7$."),
        ({"a"}, r"Very few attempted the more straightforward method of solving $\mathrm{f}(x)=7$."),
        ({"a"}, r"Most candidates achieved some success, with some slips being made by those attempting to find "
                r"$\mathrm{f}^{-1}(x)$.", NO),
        ({"a"}, r"Of those gaining no marks, the majority came from a misunderstanding of the notation with some "
                r"substituting $x=7$ into $\mathrm{f}'(x)$ and others into $[\mathrm{f}(x)]^{-1}$", NO),
        ({"b"}, "In part (b) most candidates understood the notation and gained the first mark by forming an expression "
                "of the correct form."),
        ({"b"}, "Many were then able to multiply both numerator and denominator by $(x-2)$ to form a single fraction of "
                "the required form."),
        ({"b"}, "This part is where most errors crept in; some having problems with the bracketing but most with the "
                "process of multiplying all terms on both numerator and denominator by the $(x-2)$ term.", NO),
    ],
    "05": [
        (W, "This question on modelling the speed of a car using arithmetic and geometric sequences proved popular.",
         NO),
        (W, "Many candidates answered both parts well and gained full marks."),
        ({"a"}, "In (a) the most common errors were to divide $(115-28)$ by 6 in finding $d$."),
        ({"b"}, "In part (b) errors were mainly due to a lack of accuracy and prematurely rounding their value for $r$."),
        (W, "A small number of candidates used the sum formula in both (a) and (b) and as a result scored no marks."),
        ({"b"}, "Additionally other candidates used their answer from (a) as one of the terms in (b), leading to an "
                "incorrect value of $r$."),
        ({"b"}, "The second method mark was made available to these candidates.", BACK),
    ],
    "06": [
        (W, "This was the second modelling question on the paper.", NO),
        ({"a"}, "Part (a) was generally well done, with few errors on giving the exact value of $R$ or the angle in "
                "radians to the required degree of accuracy."),
        ({"a"}, "A very small number of candidates gave $R$ as a decimal or the angle in degrees."),
        ({"b"}, "Part (b) was also well done with most of those candidates giving the exact answer for the temperature.", NO),
        ({"b"}, r"Occasionally candidates obtained an answer of $8^\circ$ C from 5 + 1 + 2, which they obtained from "
                r"taking the maximum values of sin and cos."),
        ({"c"}, "Part (c) was more challenging."),
        ({"c"}, r"The correct answer could be obtained fairly quickly by solving $\frac{\pi t}{12}+1.107-3="
                r"\frac{\pi}{2}$ but often the 1.107 and/or the 3 were omitted."),
        ({"c"}, "Stating the time in an acceptable format also proved surprisingly difficult."),
    ],
    "07": [
        (W, "A very significant majority of the candidates did not seem to know how to define a region using "
            "inequalities."),
        (W, "It was common to see a response where the area of region $R$ was attempted using integration.", NO),
        (W, "It was only a small minority of candidates who made a correct inequality statement at the end, even with "
            "the allowance of follow through on their quadratic curve and their line equations.", NO),
        (W, "It was often the case that this final mark was lost due to a candidate using the letter $R$ rather than $y$ "
            "in their inequality.", NO),
        (W, "Finding the equations of the boundaries of the region is essential when defining the inequalities, so "
            "candidates who went on to find an area were mostly still trying to do this and if successful would have "
            "only lost the final mark.", BACK),
        (W, "A very small minority of candidates found the area below the line by using a trapezium area formula and so "
            "did not manage to gain the marks for the line equation."),
        (W, "Finding the line equation correctly was achieved by a majority of candidates, although a slip with the line "
            "gradient did occur occasionally even if the diagram showed a convincingly positive gradient."),
        (W, r"Finding the equation of the quadratic curve was found to be more difficult, with a common error being "
            r"$\mathrm{f}(x)=(x+2)^2+13$."),
        (W, "Occasionally a candidate spotted that this was not consistent with the curve going through (0,25) and "
            "tried to adjust their answer, but not often in a correct way.", BACK),
        (W, r"Attempts at using $\mathrm{f}(x)=a(x+2)^2+13$ were often successful at finding a, whilst attempts at "
            r"using $\mathrm{f}(x)=ax^2+bx+c$ were much less often correct."),
    ],
    "08": [
        (W, "Candidates were expected to realise that “when the rate of change is proportional to the $y$ value, an "
            "exponential model should be used.”"),
        (W, "The question seemed to take a great many candidates by surprise and many assumed that ‘$n$ was "
            "proportional to $n$’ or that ‘$n$ was proportional to $t$’, not that the rate of growth of ‘$n$ was "
            "proportional to $n$’.", NO),
        (W, "Those that did interpret the situation correctly could write down an equation very quickly whereas others "
            "attempted to solve a differential equation.", NO),
        (W, r"Equations scoring one of two marks were common and included $n=A\mathrm{e}^t$, $n=\mathrm{e}^{kt}$ and "
            r"$n=A\mathrm{e}^{kt}+b$"),
    ],
    "09": [
        ({"a", "b"}, "Parts (a) and (b) of question 9 were standard bookwork involving the product rule of "
                     "differentiation using an exponential function."),
        ({"a", "b"}, "Well rehearsed candidates were very successful here scoring the majority of marks."),
        ({"b"}, "The diagram should have helped in determining the maximum and minimum points of the function."),
        ({"c"}, "Unsurprisingly candidates found part (c) more challenging, especially (c) (ii) where the significance "
                "of $x=0$ was rarely understood."),
        ({"c"}, "It was however a good discriminator for stronger candidates.", BACK),
    ],
    "10": [
        ({"b"}, "This question proved to be more discriminating than expected with many failing to notice the partial "
                "fractions in part (b), thereby losing 6 marks.", NO),
        ({"a"}, r"Part (a) was well answered by many candidates, particularly those who opted to calculate "
                r"$\mathrm{d}x/\mathrm{d}u$ rather than $\mathrm{d}u/\mathrm{d}x$, as the latter proved harder to "
                r"substitute correctly into the expression in terms of $u$.", NO),
        ({"a"}, "Some students lost the final accuracy mark for not showing a correct intermediate line with integral "
                "signs and some did not finish their working with an expression showing the given integral."),
        ({"a"}, "A few candidates made arithmetic slips in finding the limits or did not attempt to change them at all."),
        ({"b"}, "Of those who did use partial fractions in part (b), most found the values of “$A$” and “$B$” correctly.", NO),
        ({"b"}, r"Unfortunately many integrated $B/(3+2u)$ to $B\ln(3+2u)$, failing to divide the coefficient by 2."),
        ({"b"}, "The final Method mark was still available for these candidates, but a number failed to simplify their "
                "numerical logs to an expression of the required form and so did not gain this mark.", BACK),
        (W, "A pleasing number of well prepared candidates did gain full marks in this question.", NO),
    ],
    "11": [
        (W, "This proved to be a challenging question with very few candidates achieving full marks overall, and with "
            "many more difficulties encountered in (b) rather than (a).", NO),
        ({"a"}, "(a) Candidates used a variety of approaches."),
        ({"a"}, "The most common started by using algebra to find the coordinates of the points where the circles meet."),
        ({"a"}, "This was achieved correctly by a majority of those who did the question this way.", BACK),
        ({"a"}, "Then the required angle was found either by trigonometry in a right angled triangle and doubling an "
                "angle, or by the cosine rule in triangle $AOB$."),
        ({"a"}, "Errors in this approach included processing $x^2+y^2=100$ into $x+y=10$.", BACK),
        ({"a"}, "Although a minority of candidates’ answers stopped after finding coordinates for $A$ or B, there were a "
                "significant number who went on to score the remaining 2 marks."),
        ({"a"}, "However, some did not seem to realise that length $OA=10$ as it is a radius of $C_1$, and had to use "
                "the distance formula to find this length.", NO),
        ({"a"}, "Another approach that was seen, but not so frequently was to use knowledge of circle equations in "
                "finding the radii and centres, to establish the lengths of the sides of triangle $OAX$, with $X$ being "
                "the centre of circle $C_2$."),
        ({"a"}, "Using the cosine rule then led to half of the required angle.", NO),
        ({"a"}, "When used, this method often gained all four marks. (See relevant diagram below)", BACK),
        ({"b"}, "(b) It was very common to see just the first mark scored in this part.", NO),
        ({"b"}, "This was due to many candidates wrongly assuming that the given angle $AOB=0.635$ was the same size as "
                "the angle $AXB$ at the centre of circle $C_2$.", BACK),
        ({"b"}, "For the minority of candidates who tried a correct method to find the size of angle $AXB$, or half of "
                "it, most of these achieved the correct values of either 1.03 or 0.516.", NO),
        ({"b"}, "Even for the minority of candidates who found one of these angles correctly, getting the final answer "
                "correct proved a challenge and only a very small minority managed this.", NO),
        ({"b"}, "Note that it was possible to do part (b) even if (a) was not attempted.", NO),
        ({"b"}, "However, it seemed that failure to find a way to do (a), led in nearly every case to no valid attempt at "
                "(b).", NO),
    ],
    "12": [
        ({"a"}, "Part (a) was generally answered well and there were remarkably few solutions containing missing "
                "variables."),
        ({"a"}, r"On this occasion, candidates who started with the RHS fared better as those who worked from the LHS "
                r"occasionally missed the required step between $\cos^2\theta/\sin\theta$ and $\cos\theta\cot\theta$, "
                r"while those who worked from both sides would often get confused or, if they progressed correctly they "
                r"simply failed to make the necessary conclusion.", NO),
        ({"b"}, "Part (b), however was very often left completely blank."),
        ({"b"}, "Many who attempted it failed to see the connection with (a) and got lost in complicated trig expansions "
                "which led nowhere.", NO),
        ({"b"}, r"Of those who did use part (a) to answer part (b), the most common solution was simply $x=25$ after "
                r"$\cos x$ had been cancelled, thus losing the solution given by $\cos x=0$.", NO),
        ({"b"}, "Only a small minority of the most able found all 3 solutions."),
    ],
    "13": [
        (W, "This question on sequences proved very discriminating, with weaker candidates scoring only the first "
            "mark.", NO),
        (W, "As with many questions on this paper however, there were some excellent and well written responses."),
        ({"a"}, "In part (a) applying the iterative formula to find $a_2$ was achieved by almost every candidate."),
        ({"a"}, r"A significant number then attempted to find $a_3$ and also $a_4$ in many cases but failed to simplify "
                r"expressions for $a_2=\frac{4k}{2}$ and $a_3=\frac{k(2k+2)}{2k}$."),
        ({"a"}, "Setting $a_4=a_1$ was often seen but fully correct proofs were rare."),
        ({"b"}, "In part (b) only a very small minority of candidates gave a correct and sufficient reason why $k$ "
                "cannot be equal to 1."),
        ({"b"}, "Although a larger minority did state the sequence would be 2,2,2, … only a small number of these "
                "pointed out that this is not a periodic sequence with order 3.", BACK),
        ({"c"}, "Part (c) could be done independently to (a) and (b), and many candidates took advantage of this.", NO),
        ({"c"}, "It was not uncommon to see the terms $2,-4,-1$ in (c) where only the first mark in (a) had been "
                "scored.", NO),
        ({"c"}, "Methods of finding the sum to 80 terms generally revolved around the calculation "
                "$26\\times(2+-4+-1)+(2)+(-4)$ ."),
        ({"c"}, "Incorrect attempts involved uses of both arithmetic or geometric sum formula or ones involving an "
                "average of the terms."),
    ],
    "14": [
        (W, "Students found aspects of this question difficult despite the fact that the differential equation to be "
            "solved in (b) was not too demanding.", NO),
        (W, "Only high scoring candidates tended to make any significant progress in this question.", NO),
        ({"a"}, r"In part (a) many candidates failed to use the chain rule $\frac{\mathrm{d}V}{\mathrm{d}t}="
                r"\frac{\mathrm{d}V}{\mathrm{d}r}\times\frac{\mathrm{d}r}{\mathrm{d}t}$ with an acceptable "
                r"$\frac{\mathrm{d}V}{\mathrm{d}t}$ and $\frac{\mathrm{d}V}{\mathrm{d}r}$."),
        ({"a"}, r"It was possible to proceed to the given answer without knowing the formula for a sphere, using "
                r"$V=\lambda r^3$ but errors and blank solutions were common.", NO),
        ({"a"}, r"Common errors were; stating $\frac{\mathrm{d}V}{\mathrm{d}t}=-k$, and then failing to provide a minimal "
                r"explanation of how their $k/4\pi$ was replaced with $k$; quoting an incorrect formula for the volume "
                r"of a sphere. Attempts included $V=\pi r^3$ , $2\pi r^3$ , $4\pi r^3$ and even $4\pi r^2$."),
        ({"b"}, "In (b) students who attempted to solve the given differential equation often separated the variables "
                "correctly and integrated both sides with both indices correct."),
        ({"b"}, "Marks were lost when students failed to give a constant of integration and as a result could not apply "
                "the given conditions correctly to their equation in $r$ and $t$."),
        ({"c"}, "In part (c) many students were confused by the wording and did not realise that a limiting value for "
                "$t$ was required."),
        ({"c"}, "Many attempts merely stated that $t$ could not be negative or that $t$ >0."),
        ({"c"}, "Those candidates who did proceed to a limiting value for $t$ generally had the right idea and most of "
                "these obtained a value of $t$ >5 and gained the A mark when their equation form part (b) was followed "
                "through.", NO),
    ],
    "15": [
        (W, "Although fully correct solutions to this question were very rare, many candidates were able to score marks "
            "from both parts.", NO),
        ({"a"}, "In part (a) the first two marks for the implicit differentiation were very accessible for the prepared "
                "candidate."),
        ({"a"}, "Proceeding to the required result for the second two marks proved a little more challenging."),
        ({"a"}, r"Only high achieving students noticed the relationship could be proven via the trigonometric identity "
                r"$1+\tan^2y=\sec^2y$."),
        ({"b"}, rf"In (b) candidates often scored the M1 for an unsimplified second derivative or a correct structure "
                rf"with a sign incorrect."),
        ({"b"}, rf"Where the first A1 was scored in (b), it was usually awarded for a correct simplified ${D2Y}$, or "
                rf"solving ${D2Y}=0$ to get $x=\sqrt[4]{{27}}$", NO),
        ({"b"}, rf"Very few candidates seemed aware that they needed to show a change in sign of ${D2Y}$ either side of "
                rf"$x=\sqrt[4]{{27}}$ to show a point of inflection."),
    ],
    "16": [
        (W, "Marks on this question were only scored by above average candidates and many made little or no progress "
            "towards a proof.", NO),
        (W, "There were many blank responses."),
        (W, "Candidates who attempted to factorise $4p^2-q^2$ were more successful than by other methods, although the "
            "large majority of these scored only the first mark, by stating the assumption and factorising to "
            "$(2p+q)(2p-q)$, but making no further progress.", BACK),
        (W, "Of those that did consider the factors of 25, many did set up and solve two relevant equations "
            "simultaneously, and so gained 3 marks, but very few considered both of the required pairs of equations "
            "and so did not all marks.", NO),
        (W, "There were many discussions of odd/even integers but this was commonly followed by working in the same "
            "variable for $p$ and $q$, which gained no marks", NO),
    ],
}

# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
RATINGS = {
    "01a": ("easy", ("01", 1)),
    "01b": ("medium", ("01", 3)),
    "02": ("easy", ("02", 0)),
    "03a": ("easy", ("03", 0)),
    "03b": ("medium", ("03", 2)),
    "04a": ("medium", ("04", 3)),
    "04b": ("medium", ("04", 7)),
    "05a": ("easy", ("05", 1)),
    "05b": ("easy", ("05", 1)),
    "06a": ("easy", ("06", 1)),
    "06b": ("easy", ("06", 3)),
    "06c": ("hard", ("06", 5)),
    "07": ("hard", ("07", 0)),
    "08": ("hard", ("08", 1)),
    "09a": ("easy", ("09", 1)),
    "09b": ("easy", ("09", 1)),
    "09c": ("hard", ("09", 3)),
    "10a": ("medium", ("10", 1)),
    "10b": ("hard", ("10", 0)),
    "11a": ("medium", ("11", 6)),
    "11b": ("hard", ("11", 11)),
    "12a": ("easy", ("12", 0)),
    "12b": ("hard", ("12", 2)),
    "13a": ("hard", ("13", 4)),
    "13b": ("hard", ("13", 5)),
    "13c": ("medium", ("13", 7)),
    "14a": ("hard", ("14", 3)),
    "14b": ("medium", ("14", 6)),
    "14c": ("hard", ("14", 7)),
    "15a": ("medium", ("15", 2)),
    "15b": ("hard", ("15", 6)),
    "16": ("hard", ("16", 0)),
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
