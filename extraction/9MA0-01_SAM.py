"""Draft builder for 9MA0-01 SAM (A level Pure Paper 1, sample assessment materials).

Run (from the project root, with the venv active):
    python extraction/9MA0-01_SAM.py        # writes out/drafts/9MA0-01_SAM.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-01_SAM.json

Everything here is transcribed from the source PDFs, read as page images (the
question paper's text layer is unreadable; figures at 200 dpi). There is no
examiner report for the SAM, so examiner_notes, difficulty and
difficulty_evidence are all null. Follow CLAUDE.md for every field.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report, part_key  # noqa: E402
from mark_codes import main_marks  # noqa: E402
from paths import ensure_out_dir  # noqa: E402

P, S = "9MA0-01", "SAM"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "13c"); label as printed (e.g. "13(c)")."""
    return {"id": f"{P}_{S}_Q{q}", "paper": P, "series": S, "question": label, "topic": topic,
            "spec_ref": spec, "marks": marks, "question_latex": latex, "mark_scheme": ms,
            "examiner_notes": None, "difficulty": None, "difficulty_evidence": None,
            "has_diagram": diagram, "source_page": page, "source_file": SRC}


ALG = "Algebra and functions"
COORD = "Coordinate geometry in the (x,y) plane"
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
D2Y = r"\frac{\mathrm{d}^2y}{\mathrm{d}x^2}"
I, J, K = r"\mathbf{i}", r"\mathbf{j}", r"\mathbf{k}"

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q1 = ["The curve $C$ has equation", "$$y=3x^4-8x^3-3$$"]
Q1A = [rf"(a) Find (i) ${DY}$", rf"(ii) ${D2Y}$"]
Q1B = "Verify that $C$ has a stationary point when $x=2$"
Q2 = [r"[Figure 1: the shape $ABCDOA$: $A$, $O$ and $D$ on a horizontal line with $AD$ labelled 12 cm; the shaded sector "
      r"$AOB$ on the left, its arc curving up from $A$ to $B$; the sector $COD$ on the right, with the arc $CD$ labelled "
      r"3 cm and the angle $0.4$ at $O$ between $OD$ and $OC$; $B$ lies on $OC$, and $OB$ is dashed.]",
      r"The shape $ABCDOA$, as shown in Figure 1, consists of a sector $COD$ of a circle centre $O$ joined to a sector "
      r"$AOB$ of a different circle, also centre $O$.",
      r"Given that arc length $CD=3$ cm, $\angle COD=0.4$ radians and $AOD$ is a straight line of length 12 cm,"]
Q2A = "find the length of $OD$,"
Q3 = ["A circle $C$ has equation", "$$x^2+y^2-4x+10y=k$$", "where $k$ is a constant."]
Q6 = ["A company plans to extract oil from an oil field.",
      "The daily volume of oil $V$, measured in barrels that the company will extract from this oil field depends upon "
      "the time, $t$ years, after the start of drilling.",
      "The company decides to use a model to estimate the daily volume of oil that will be extracted. The model includes "
      "the following assumptions:",
      "• The initial daily volume of oil extracted from the oil field will be 16 000 barrels.",
      "• The daily volume of oil that will be extracted exactly 4 years after the start of drilling will be 9000 barrels.",
      "• The daily volume of oil extracted will decrease over time.",
      "The diagram below shows the graphs of two possible models.",
      r"[Figure: two graphs of $V$ against $t$. Model $A$: a straight line from $(0, 16\,000)$ through $(4, 9000)$, "
      r"crossing the $t$-axis and continuing below it. Model $B$: a decreasing curve from $(0, 16\,000)$ through "
      r"$(4, 9000)$, flattening out above the $t$-axis.]"]
Q8 = [r"$$\mathrm{f}(x)=\ln(2x-5)+2x^2-30,\qquad x>2.5$$"]
Q8A = r"(a) Show that $\mathrm{f}(x)=0$ has a root $\alpha$ in the interval $[3.5, 4]$"
Q9A = ["(a) Prove that", r"$$\tan\theta+\cot\theta\equiv2\mathrm{cosec}\,2\theta,\qquad\theta\neq\frac{n\pi}{2},n\in\mathbb{Z}$$"]
Q11 = ["An archer shoots an arrow.", "The height, $H$ metres, of the arrow above the ground is modelled by the formula",
       r"$$H=1.8+0.4d-0.002d^2,\qquad d\geqslant0$$",
       "where $d$ is the horizontal distance of the arrow from the archer, measured in metres."]
Q11C = ["Write $1.8+0.4d-0.002d^2$ in the form", "$$A-B(d-C)^2$$", "where $A$, $B$ and $C$ are constants to be found."]
Q12 = ["In a controlled experiment, the number of microbes, $N$, present in a culture $T$ days after the start of the "
       "experiment were counted.", "$N$ and $T$ are expected to satisfy a relationship of the form",
       r"$$N=aT^b,\qquad\text{where }a\text{ and }b\text{ are constants}$$"]
Q12A = ["Show that this relationship can be expressed in the form", r"$$\log_{10}N=m\log_{10}T+c$$",
        "giving $m$ and $c$ in terms of the constants $a$ and/or $b$."]
Q12F = [r"[Figure 3: a graph of $\log_{10}N$ (0 to 5.0) against $\log_{10}T$ (0 to 1.4) on a grid, with six plotted "
        r"crosses and a straight line of best fit from about $(0, 1.8)$ rising to about $(1.2, 4.6)$.]",
        r"Figure 3 shows the line of best fit for values of $\log_{10}N$ plotted against values of $\log_{10}T$"]
Q13 = ["The curve $C$ has parametric equations", r"$$x=2\cos t,\quad y=\sqrt{3}\cos2t,\quad0\leqslant t\leqslant\pi$$"]
Q13A = rf"Find an expression for ${DY}$ in terms of $t$."
Q13P = [r"The point $P$ lies on $C$ where $t=\frac{2\pi}{3}$", "The line $l$ is the normal to $C$ at $P$."]
Q13B = ["Show that an equation for $l$ is", r"$$2x-2\sqrt{3}y-1=0$$"]
Q14 = [r"[Figure 4: the curve $C$ coming down from a positive intercept on the $y$-axis to a minimum above the $x$-axis "
       r"between $x=1$ and $x=3$, then rising steeply; the region $S$ under $C$ between the vertical lines $x=1$ and "
       r"$x=3$ is shaded.]",
       "Figure 4 shows a sketch of part of the curve $C$ with equation", r"$$y=\frac{x^2\ln x}{3}-2x+5,\quad x>0$$",
       "The finite region $S$, shown shaded in Figure 4, is bounded by the curve $C$, the line with equation $x=1$, the "
       "$x$-axis and the line with equation $x=3$"]
Q14T = ["The table below shows corresponding values of $x$ and $y$ with the values of $y$ given to 4 decimal places as "
        "appropriate.",
        r"$$\begin{array}{|c|c|c|c|c|c|}\hline x&1&1.5&2&2.5&3\\\hline y&3&2.3041&1.9242&1.9089&2.2958\\"
        r"\hline\end{array}$$"]
Q15 = [r"[Figure 5: the curve $y=\mathrm{f}(x)$ rising from $O$ to a maximum at $P$, falling through the $x$-axis to a "
       r"shallow minimum at $Q$ below the axis, then rising slowly back towards the $x$-axis.]",
       r"Figure 5 shows a sketch of the curve with equation $y=\mathrm{f}(x)$, where",
       r"$$\mathrm{f}(x)=\frac{4\sin2x}{\mathrm{e}^{\sqrt{2}x-1}},\quad0\leqslant x\leqslant\pi$$",
       "The curve has a maximum turning point at $P$ and a minimum turning point at $Q$ as shown in Figure 5."]
Q15A = ["Show that the $x$ coordinates of point $P$ and point $Q$ are solutions of the equation",
        r"$$\tan2x=\sqrt{2}$$"]

LATEX = {
    "01a": L(*Q1, *Q1A),
    "01b": L(*Q1, Q1B),
    "01c": L(*Q1, "(b) " + Q1B, "(c) Determine the nature of this stationary point, giving a reason for your answer."),
    "02a": L(*Q2, Q2A),
    "02b": L(*Q2, "(a) " + Q2A, "(b) find the area of the shaded sector $AOB$."),
    "03a": L(*Q3, "Find the coordinates of the centre of $C$."),
    "03b": L(*Q3, "State the range of possible values for $k$."),
    "04": L("Given that $a$ is a positive constant and", r"$$\int_a^{2a}\frac{t+1}{t}\,\mathrm{d}t=\ln7$$",
            r"show that $a=\ln k$, where $k$ is a constant to be found."),
    "05": L("A curve $C$ has parametric equations", r"$$x=2t-1,\quad y=4t-7+\frac{3}{t},\quad t\neq0$$",
            "Show that the Cartesian equation of the curve $C$ can be written in the form",
            r"$$y=\frac{2x^2+ax+b}{x+1},\quad x\neq-1$$", "where $a$ and $b$ are integers to be found."),
    "06a": L(*Q6, "(a) (i) Use model $A$ to estimate the daily volume of oil that will be extracted exactly 3 years "
                  "after the start of drilling.", "(ii) Write down a limitation of using model $A$."),
    "06b": L(*Q6, "(b) (i) Using an exponential model and the information given in the question, find a possible "
                  "equation for model $B$.",
             "(ii) Using your answer to (b)(i) estimate the daily volume of oil that will be extracted exactly 3 years "
             "after the start of drilling."),
    "07": L(r"[Figure 2: a triangle $ABC$ with $B$ at the top, $A$ to the left and below $B$, and $C$ at the bottom right.]",
            "Figure 2 shows a sketch of a triangle $ABC$.",
            rf"Given $\overrightarrow{{AB}}=2{I}+3{J}+{K}$ and $\overrightarrow{{BC}}={I}-9{J}+3{K}$,",
            r"show that $\angle BAC=105.9^\circ$ to one decimal place."),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, "A student takes 4 as the first approximation to $\\alpha$.",
             r"Given $\mathrm{f}(4)=3.099$ and $\mathrm{f}'(4)=16.67$ to 4 significant figures,",
             r"(b) apply the Newton-Raphson procedure once to obtain a second approximation for $\alpha$, giving your "
             r"answer to 3 significant figures."),
    "08c": L(*Q8, Q8A, r"(c) Show that $\alpha$ is the only root of $\mathrm{f}(x)=0$"),
    "09a": L(*Q9A),
    "09b": L(*Q9A, "(b) Hence explain why the equation", r"$$\tan\theta+\cot\theta=1$$",
             "does not have any real solutions."),
    "10": L(r"Given that $\theta$ is measured in radians, prove, from first principles, that the derivative of "
            r"$\sin\theta$ is $\cos\theta$",
            r"You may assume the formula for $\sin(A\pm B)$ and that as $h\to0$, $\frac{\sin h}{h}\to1$ and "
            r"$\frac{\cos h-1}{h}\to0$"),
    "11a": L(*Q11, "Given that the arrow travels in a vertical plane until it hits the ground,",
             "find the horizontal distance travelled by the arrow, as given by this model."),
    "11b": L(*Q11, "With reference to the model, interpret the significance of the constant 1.8 in the formula."),
    "11c": L(*Q11, *Q11C),
    "11d": L(*Q11, "(c) " + Q11C[0], *Q11C[1:], "It is decided that the model should be adapted for a different archer.",
             "The adapted formula for this archer is", r"$$H=2.1+0.4d-0.002d^2,\qquad d\geqslant0$$",
             "Hence or otherwise, find, for the adapted model", "(d) (i) the maximum height of the arrow above the ground.",
             "(ii) the horizontal distance, from the archer, of the arrow when it is at its maximum height."),
    "12a": L(*Q12, *Q12A),
    "12b": L(*Q12, "(a) " + Q12A[0], *Q12A[1:], *Q12F,
             "(b) Use the information provided to estimate the number of microbes present in the culture 3 days after "
             "the start of the experiment."),
    "12c": L(*Q12, *Q12F,
             "Explain why the information provided could not reliably be used to estimate the day when the number of "
             "microbes in the culture first exceeds 1 000 000."),
    "12d": L(*Q12, *Q12F, "With reference to the model, interpret the value of the constant $a$."),
    "13a": L(*Q13, Q13A),
    "13b": L(*Q13, "(a) " + Q13A, *Q13P, "(b) " + Q13B[0], Q13B[1]),
    "13c": L(*Q13, *Q13P, "(b) " + Q13B[0], Q13B[1], "The line $l$ intersects the curve $C$ again at the point $Q$.",
             "(c) Find the exact coordinates of $Q$.", "You must show clearly how you obtained your answers."),
    "14a": L(*Q14, *Q14T, "Use the trapezium rule, with all the values of $y$ in the table, to obtain an estimate for the "
                          "area of $S$, giving your answer to 3 decimal places."),
    "14b": L(*Q14, *Q14T, "Explain how the trapezium rule could be used to obtain a more accurate estimate for the area "
                          "of $S$."),
    "14c": L(*Q14, r"Show that the exact area of $S$ can be written in the form $\frac{a}{b}+\ln c$, where $a$, $b$ and $c$ "
                   r"are integers to be found.",
             "(In part c, solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "15a": L(*Q15, *Q15A),
    "15b": L(*Q15, "(a) " + Q15A[0], Q15A[1],
             "(b) Using your answer to part (a), find the $x$-coordinate of the minimum turning point on the curve with "
             "equation", r"(i) $y=\mathrm{f}(2x)$.", r"(ii) $y=3-2\mathrm{f}(x)$."),
}

ALT10 = "ALT: 10alt"
GR12 = "ALT: Alternative to (b) using a graphical approach"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", DIFF, "7.2", 3, LATEX["01a"],
      [rf"M1 (AO 1.1b): (i) ${DY}=12x^3-24x^2$. Notes: Differentiates to a cubic form",
       rf"A1 (AO 1.1b): (i) ${DY}=12x^3-24x^2$. Notes: ${DY}=12x^3-24x^2$",
       rf"A1ft (AO 1.1b): (ii) ${D2Y}=36x^2-48x$. Notes: Achieves a correct ${D2Y}$ for their ${DY}=36x^2-48x$"],
      False, 2),
    e("01b", "1(b)", DIFF, "7.3", 2, LATEX["01b"],
      [rf"M1 (AO 1.1b): Substitutes $x=2$ into their ${DY}=12\times2^3-24\times2^2$. Notes: Substitutes $x=2$ into their "
       rf"${DY}$",
       rf"A1 (AO 2.1): Shows ${DY}=0$ and states “hence there is a stationary point”. Notes: Shows ${DY}=0$ and states "
       rf"“hence there is a stationary point” All aspects of the proof must be correct"],
      False, 2),
    e("01c", "1(c)", DIFF, "7.3", 2, LATEX["01c"],
      [rf"M1 (AO 1.1b): Substitutes $x=2$ into their ${D2Y}=36\times2^2-48\times2$. Notes: Substitutes $x=2$ into their "
       rf"${D2Y}$ Alternatively calculates the gradient of $C$ either side of $x=2$",
       rf"A1ft (AO 2.2a): ${D2Y}=48>0$ and states “hence the stationary point is a minimum”. Notes: For a correct "
       rf"calculation, a valid reason and a correct conclusion. Follow through on an incorrect ${D2Y}$"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", TRIG, "5.1", 2, LATEX["02a"],
      [r"M1 (AO 1.2): Uses $s=r\theta\Rightarrow3=r\times0.4$. Notes: Attempts to use the correct formula $s=r\theta$ with "
       r"$s=3$ and $\theta=0.4$",
       r"A1 (AO 1.1b): $\Rightarrow OD=7.5$ cm. Notes: $OD=7.5$ cm (An answer of 7.5cm implies the use of a correct formula "
       r"and scores both marks)"],
      True, 4),
    e("02b", "2(b)", TRIG, "5.1", 3, LATEX["02b"],
      [r"M1 (AO 3.1a): Uses angle $AOB=(\pi-0.4)$ or uses radius is (12 – ‘7.5’) cm. Notes: $AOB=\pi-0.4$ may be implied "
       r"by the use of $AOB=$ awrt 2.74 or uses radius is (12 – their ‘7.5’)",
       r"M1 (AO 1.1b): Uses area of sector $=\frac{1}{2}r^2\theta=\frac{1}{2}\times(12-7.5)^2\times(\pi-0.4)$. Notes: Follow "
       r"through on their radius (12 – their $OD$) and their angle",
       r"A1ft (AO 1.1b): $=27.8$cm$^2$. Notes: Allow awrt 27.8 cm$^2$. (Answer 27.75862562). Follow through on their "
       r"(12 – their ‘7.5’) Note: Do not follow through on a radius that is negative."],
      True, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", COORD, "3.2", 2, LATEX["03a"],
      [r"M1 (AO 1.1b): Attempts $(x-2)^2+(y+5)^2=\ldots$ Notes: Attempts to complete the square so allow "
       r"$(x-2)^2+(y+5)^2=\ldots$",
       r"A1 (AO 1.1b): Centre $(2,-5)$. Notes: States the centre is at $(2,-5)$. Also allow written separately $x=2,y=-5$ "
       r"$(2,-5)$ implies both marks"],
      False, 5),
    e("03b", "3(b)", COORD, "3.2, 2.5", 2, LATEX["03b"],
      [r"M1 (AO 2.2a): Sets $k+2^2+5^2>0$. Notes: Deduces that the right hand side of their $(x\pm\ldots)^2+(y\pm\ldots)^2="
       r"\ldots$ is $>0$ or $\geqslant0$",
       r"A1ft (AO 1.1b): $\Rightarrow k>-29$. Notes: $k>-29$ Also allow $k\geqslant-29$ Follow through on their rhs of "
       r"$(x\pm\ldots)^2+(y\pm\ldots)^2=\ldots$"],
      False, 5),

    # ---------------- Q4 ----------------
    e("04", "4", INT, "8.3, 8.2, 6.4", 4, LATEX["04"],
      [r"M1 (AO 2.1): Writes $\int\frac{t+1}{t}\,\mathrm{d}t=\int1+\frac{1}{t}\,\mathrm{d}t$ and attempts to integrate. "
       r"Notes: Attempts to divide each term by $t$ or alternatively multiply each term by $t^{-1}$",
       r"M1 (AO 1.1b): $=t+\ln t\ (+c)$. Notes: Integrates each term and knows $\int\frac{1}{t}\,\mathrm{d}t=\ln t$. The "
       r"$+c$ is not required for this mark",
       r"M1 (AO 1.1b): $(2a+\ln2a)-(a+\ln a)=\ln7$. Notes: Substitutes in both limits, subtracts and sets equal to ln7",
       r"A1 (AO 1.1b): $a=\ln\frac{7}{2}$ with $k=\frac{7}{2}$. Notes: Proceeds to $a=\ln\frac{7}{2}$ and states "
       r"$k=\frac{7}{2}$ or exact equivalent such as 3.5"],
      False, 6),

    # ---------------- Q5 ----------------
    e("05", "5", COORD, "3.3, 2.6", 3, LATEX["05"],
      [r"M1 (AO 2.1): Attempts to substitute $=\frac{x+1}{2}$ into $y\Rightarrow y=4\left(\frac{x+1}{2}\right)-7+"
       r"\frac{6}{(x+1)}$. Notes: Score for an attempt at substituting $t=\frac{x+1}{2}$ or equivalent into "
       r"$y=4t-7+\frac{3}{t}$",
       r"M1 (AO 2.1): Attempts to write as a single fraction $y=\frac{(2x-5)(x+1)+6}{(x+1)}$. Notes: Award this for an "
       r"attempt at a single fraction with a correct common denominator. Their $4\left(\frac{x+1}{2}\right)-7$ term may be "
       r"simplified first",
       r"A1 (AO 1.1b): $y=\frac{2x^2-3x+1}{x+1}$ $a=-3,b=1$. Notes: Correct answer only $y=\frac{2x^2-3x+1}{x+1}$ "
       r"$a=-3,b=1$"],
      False, 7),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", ALG, "2.11, 3.1", 2, LATEX["06a"],
      [r"B1 (AO 3.4): (i) 10750 barrels. Notes: 10750 barrels",
       r"B1 (AO 3.5b): (ii) Gives a valid limitation, for example • The model shows that the daily volume of oil extracted "
       r"would become negative as $t$ increases, which is impossible • States when $t=10,V=-1500$ which is impossible • "
       r"States that the model will only work for $0\leqslant t\leqslant\frac{64}{7}$. Notes: See scheme"],
      True, 8),
    e("06b", "6(b)", EXP, "6.7, 6.5", 5, LATEX["06b"],
      [r"M1 (AO 3.3): (i) Suggests a suitable exponential model, for example $V=A\mathrm{e}^{kt}$. Notes: Suggests a "
       r"suitable exponential model, for example $V=A\mathrm{e}^{kt}$, $V=Ar^t$ or any other suitable function such as "
       r"$V=A\mathrm{e}^{kt}+b$ where the candidate chooses a value for $b$.",
       r"dM1 (AO 3.1b): Uses $(0,16000)$ and $(4,9000)$ in $\Rightarrow9000=16000\mathrm{e}^{4k}$. Notes: Uses both "
       r"$(0,16000)$ and $(4,9000)$ in their model. With $V=A\mathrm{e}^{kt}$ candidates need to proceed to "
       r"$9000=16000\mathrm{e}^{4k}$ With $V=Ar^t$ candidates need to proceed to $9000=16000r^4$ With "
       r"$V=A\mathrm{e}^{kt}+b$ candidates need to proceed to $9000=(16000-b)\mathrm{e}^{4k}+b$ where $b$ is given as a "
       r"positive constant and $A+b=16000$ .",
       r"M1 (AO 1.1b): $\Rightarrow k=\frac{1}{4}\ln\left(\frac{9}{16}\right)$ awrt $-0.144$. Notes: Uses a correct method "
       r"to find all constants in the model.",
       r"A1 (AO 1.1b): $V=16000\mathrm{e}^{\frac{1}{4}\ln\left(\frac{9}{16}\right)t}$ or $V=16000\mathrm{e}^{-0.144t}$. "
       r"Notes: Gives a suitable equation for the model passing through (or approximately through in the case of decimal "
       r"equivalents) both values $(0,16000)$ and $(4,9000)$. Possible equations for the model could be for example "
       r"$V=16000\mathrm{e}^{-0.144t}$ $V=16000\times(0.866)^t$ $V=15800\mathrm{e}^{-0.146t}+200$",
       r"B1ft (AO 3.4): (ii) Uses their exponential model with $t=3\Rightarrow V=$ awrt 10400 barrels. Notes: Follow "
       r"through on their exponential model"],
      True, 8),

    # ---------------- Q7 ----------------
    e("07", "7", VEC, "10.2, 10.3, 5.1", 5, LATEX["07"],
      [rf"M1 (AO 3.1a): Attempts $\overrightarrow{{AC}}=\overrightarrow{{AB}}+\overrightarrow{{BC}}=2{I}+3{J}+{K}+{I}-9{J}+"
       rf"3{K}=3{I}-6{J}+4{K}$. Notes: Attempts to find $\overrightarrow{{AC}}$ by using $\overrightarrow{{AC}}="
       rf"\overrightarrow{{AB}}+\overrightarrow{{BC}}$",
       r"M1 (AO 2.1): Attempts to find any one length using 3-d Pythagoras. Notes: Attempts to find any one length by use "
       r"of Pythagoras' Theorem",
       r"A1ft (AO 1.1b): Finds all of $\left|AB\right|=\sqrt{14}$, $\left|AC\right|=\sqrt{61}$, $\left|BC\right|=\sqrt{91}$. "
       r"Notes: Finds all three lengths in the triangle. Follow through on their $\left|AC\right|$",
       r"M1 (AO 2.1): $\cos BAC=\frac{14+61-91}{2\sqrt{14}\sqrt{61}}$. Notes: Attempts to find $BAC$ using "
       r"$\cos BAC=\frac{\left|AB\right|^2+\left|AC\right|^2-\left|BC\right|^2}{2\left|AB\right|\left|AC\right|}$ Allow this "
       r"to be scored for other methods such as $\cos BAC=\frac{\overrightarrow{AB}.\overrightarrow{AC}}{\left|AB\right|"
       r"\left|AC\right|}$",
       r"A1* (AO 1.1b): angle $BAC=105.9^\circ$ *. Notes: This is a show that and all aspects must be correct. Angle "
       r"$BAC=105.9^\circ$"],
      True, 10),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", NUM, "9.1", 2, LATEX["08a"],
      [r"M1 (AO 1.1b): $\mathrm{f}(3.5)=-4.8$, $\mathrm{f}(4)=(+)3.1$. Notes: Attempts $\mathrm{f}(x)$ at both $x=3.5$ and "
       r"$x=4$ with at least one correct to 1 significant figure",
       r"A1* (AO 2.4): Change of sign and function continuous in interval $[3.5,4]\Rightarrow$ Root *. Notes: $\mathrm{f}(3.5)$ "
       r"and $\mathrm{f}(4)$ correct to 1 sig figure (rounded or truncated) with a correct reason and conclusion. A reason "
       r"could be change of sign, or $\mathrm{f}(3.5)\times\mathrm{f}(4)<0$ or similar with $\mathrm{f}(x)$ being continuous "
       r"in this interval. A conclusion could be 'Hence root' or 'Therefore root in interval'"],
      False, 12),
    e("08b", "8(b)", NUM, "9.3", 2, LATEX["08b"],
      [r"M1 (AO 1.1b): Attempts $x_1=x_0-\frac{\mathrm{f}(x_0)}{\mathrm{f}'(x_0)}\Rightarrow x_1=4-\frac{3.099}{16.67}$. "
       r"Notes: Attempts $x_1=x_0-\frac{\mathrm{f}(x_0)}{\mathrm{f}'(x_0)}$ evidenced by $x_1=4-\frac{3.099}{16.67}$",
       r"A1 (AO 1.1b): $x_1=3.81$. Notes: Correct answer only $x_1=3.81$"],
      False, 12),
    e("08c", "8(c)", NUM, "9.1, 2.7", 2, LATEX["08c"],
      [r"M1 (AO 3.1a): Attempts to sketch both $y=\ln(2x-5)$ and $y=30-2x^2$ [the mark scheme shows a sketch of the "
       r"parabola $y=30-2x^2$ and the curve $y=\ln(2x-5)$ meeting once]. Notes: For a valid attempt at showing that there "
       r"is only one root. This can be achieved by • Sketching graphs of $y=\ln(2x-5)$ and $y=30-2x^2$ on the same axes • "
       r"Showing that $\mathrm{f}(x)=\ln(2x-5)+2x^2-30$ has no turning points • Sketching a graph of "
       r"$\mathrm{f}(x)=\ln(2x-5)+2x^2-30$",
       r"A1 (AO 2.4): States that $y=\ln(2x-5)$ meets $y=30-2x^2$ in just one place, therefore $y=\ln(2x-5)=30-2x$ has just "
       r"one root $\Rightarrow\mathrm{f}(x)=0$ has just one root. Notes: Scored for correct conclusion"],
      False, 12),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", TRIG, "5.8, 5.5, 5.6", 4, LATEX["09a"],
      [r"M1 (AO 2.1): $\tan\theta+\cot\theta\equiv\frac{\sin\theta}{\cos\theta}+\frac{\cos\theta}{\sin\theta}$. Notes: "
       r"Writes $\tan\theta=\frac{\sin\theta}{\cos\theta}$ and $\cot\theta=\frac{\cos\theta}{\sin\theta}$",
       r"A1 (AO 1.1b): $\equiv\frac{\sin^2\theta+\cos^2\theta}{\sin\theta\cos\theta}$. Notes: Achieves a correct "
       r"intermediate answer of $\frac{\sin^2\theta+\cos^2\theta}{\sin\theta\cos\theta}$",
       r"M1 (AO 2.1): $\equiv\frac{1}{\frac{1}{2}\sin2\theta}$. Notes: Uses the double angle formula "
       r"$\sin2\theta=2\sin\theta\cos\theta$",
       r"A1* (AO 1.1b): $\equiv2\mathrm{cosec}\,2\theta$ *. Notes: Completes proof with no errors. This is a given answer.",
       r"ALT: Note: There are many alternative methods. For example $\tan\theta+\cot\theta\equiv\tan\theta+"
       r"\frac{1}{\tan\theta}\equiv\frac{\tan^2\theta+1}{\tan\theta}\equiv\frac{\sec^2\theta}{\tan\theta}\equiv"
       r"\frac{1}{\cos^2\theta\times\frac{\sin\theta}{\cos\theta}}\equiv\frac{1}{\cos\theta\times\sin\theta}$ then as the "
       r"main scheme."],
      False, 14),
    e("09b", "9(b)", TRIG, "5.3, 5.6", 1, LATEX["09b"],
      [r"B1 (AO 2.4): States $\tan\theta+\cot\theta=1\Rightarrow\sin2\theta=2$ AND no real solutions as "
       r"$-1\leqslant\sin2\theta\leqslant1$. Notes: Scored for sight of $\sin2\theta=2$ and a reason as to why this equation "
       r"has no real solutions. Possible reasons could be $-1\leqslant\sin2\theta\leqslant1$........and therefore "
       r"$\sin2\theta\neq2$ or $\sin2\theta=2\Rightarrow2\theta=\arcsin2$ which has no answers as "
       r"$-1\leqslant\sin2\theta\leqslant1$"],
      False, 14),

    # ---------------- Q10 ----------------
    e("10", "10", DIFF, "7.1, 5.6", 5, LATEX["10"],
      [r"B1 (AO 2.1): Use of $\frac{\sin(\theta+h)-\sin\theta}{(\theta+h)-\theta}$. Notes: States or implies that the "
       r"gradient of the chord is $\frac{\sin(\theta+h)-\sin\theta}{h}$ or similar such as "
       r"$\frac{\sin(\theta+\delta\theta)-\sin\theta}{\theta+\delta\theta-\theta}$ for a small $h$ or $\delta\theta$",
       r"M1 (AO 1.1b): Uses the compound angle identity for $\sin(A+B)$ with $A=\theta,B=h$ $\Rightarrow\sin(\theta+h)="
       r"\sin\theta\cos h+\cos\theta\sin h$. Notes: Uses the compound angle identity for $\sin(A+B)$ with $A=\theta,B=h$ "
       r"or $\delta\theta$",
       r"A1 (AO 1.1b): Achieves $\frac{\sin(\theta+h)-\sin\theta}{h}=\frac{\sin\theta\cos h+\cos\theta\sin h-\sin\theta}{h}$. "
       r"Notes: Obtains $\frac{\sin\theta\cos h+\cos\theta\sin h-\sin\theta}{h}$ or equivalent",
       r"M1 (AO 2.1): $=\frac{\sin h}{h}\cos\theta+\left(\frac{\cos h-1}{h}\right)\sin\theta$. Notes: Writes their expression "
       r"in terms of $\frac{\sin h}{h}$ and $\frac{\cos h-1}{h}$",
       r"A1* (AO 2.5): Uses $h\to0$, $\frac{\sin h}{h}\to1$ and $\frac{\cos h-1}{h}\to0$ Hence the "
       r"$\lim_{h\to0}\frac{\sin(\theta+h)-\sin\theta}{(\theta+h)-\theta}=\cos\theta$ and the gradient of the chord "
       r"$\to$ gradient of the curve $\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}\theta}=\cos\theta$ *. Notes: Uses correct "
       r"language to explain that $\frac{\mathrm{d}y}{\mathrm{d}\theta}=\cos\theta$ For this method they should use all of "
       r"the given statements $h\to0$, $\frac{\sin h}{h}\to1$, $\frac{\cos h-1}{h}\to0$ meaning that the "
       r"$\lim_{h\to0}\frac{\sin(\theta+h)-\sin\theta}{(\theta+h)-\theta}=\cos\theta$ and therefore the gradient of the chord "
       r"$\to$ gradient of the curve $\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}\theta}=\cos\theta$",
       rf"{ALT10} — B1 (AO 2.1): Use of $\frac{{\sin(\theta+h)-\sin\theta}}{{(\theta+h)-\theta}}$",
       rf"{ALT10} — M1 (AO 1.1b): Sets $\frac{{\sin(\theta+h)-\sin\theta}}{{(\theta+h)-\theta}}=\frac{{\sin\left(\theta+"
       rf"\frac{{h}}{{2}}+\frac{{h}}{{2}}\right)-\sin\left(\theta+\frac{{h}}{{2}}-\frac{{h}}{{2}}\right)}}{{h}}$ and uses the "
       rf"compound angle identity for $\sin(A+B)$ and $\sin(A-B)$ with $A=\theta+\frac{{h}}{{2}}$, $B=\frac{{h}}{{2}}$",
       rf"{ALT10} — A1 (AO 1.1b): Achieves $\frac{{\sin(\theta+h)-\sin\theta}}{{h}}=\frac{{\left[\sin\left(\theta+\frac{{h}}{{2}}"
       rf"\right)\cos\left(\frac{{h}}{{2}}\right)+\cos\left(\theta+\frac{{h}}{{2}}\right)\sin\left(\frac{{h}}{{2}}\right)\right]-"
       rf"\left[\sin\left(\theta+\frac{{h}}{{2}}\right)\cos\left(\frac{{h}}{{2}}\right)-\cos\left(\theta+\frac{{h}}{{2}}\right)"
       rf"\sin\left(\frac{{h}}{{2}}\right)\right]}}{{h}}$",
       rf"{ALT10} — M1 (AO 2.1): $=\frac{{\sin\left(\frac{{h}}{{2}}\right)}}{{\frac{{h}}{{2}}}}\times\cos\left(\theta+"
       rf"\frac{{h}}{{2}}\right)$",
       rf"{ALT10} — A1* (AO 2.5): Uses $h\to0$, $\frac{{h}}{{2}}\to0$ hence $\frac{{\sin\left(\frac{{h}}{{2}}\right)}}"
       rf"{{\frac{{h}}{{2}}}}\to1$ and $\cos\left(\theta+\frac{{h}}{{2}}\right)\to\cos\theta$ Therefore the "
       rf"$\lim_{{h\to0}}\frac{{\sin(\theta+h)-\sin\theta}}{{(\theta+h)-\theta}}=\cos\theta$ and the gradient of the chord "
       rf"$\to$ gradient of the curve $\Rightarrow\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}\theta}}=\cos\theta$ *. Additional notes: "
       rf"Uses correct language to explain that $\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}\theta}}=\cos\theta$ . For this method "
       rf"they should use the (adapted) given statement $h\to0$, $\frac{{h}}{{2}}\to0$ hence "
       rf"$\frac{{\sin\left(\frac{{h}}{{2}}\right)}}{{\frac{{h}}{{2}}}}\to1$ with $\cos\left(\theta+\frac{{h}}{{2}}\right)\to"
       rf"\cos\theta$ meaning that the limit $=\cos\theta$ and therefore the gradient of the chord $\to$ gradient of the "
       rf"curve"],
      False, 15),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", ALG, "2.11, 2.3", 3, LATEX["11a"],
      [r"M1 (AO 3.4): Sets $H=0\Rightarrow1.8+0.4d-0.002d^2=0$. Notes: Sets $H=0\Rightarrow1.8+0.4d-0.002d^2=0$",
       r"dM1 (AO 1.1b): Solves using an appropriate method, for example $d=\frac{-0.4\pm\sqrt{(0.4)^2-4(-0.002)(1.8)}}"
       r"{2\times-0.002}$. Notes: Solves using formula, which if stated must be correct, by completing square (look for "
       r"$(d-100)^2=10900\Rightarrow d=..$) or even allow answers coming from a graphical calculator",
       r"A1 (AO 2.2a): Distance = awrt 204(m) only. Notes: Awrt 204 m only"],
      False, 16),
    e("11b", "11(b)", ALG, "2.11", 1, LATEX["11b"],
      [r"B1 (AO 3.4): States the initial height of the arrow above the ground. Notes: States it is the initial height of "
       r"the arrow above the ground. Do not allow “ it is the height of the archer”"],
      False, 16),
    e("11c", "11(c)", ALG, "2.3", 3, LATEX["11c"],
      [r"M1 (AO 1.1b): $1.8+0.4d-0.002d^2=-0.002(d^2-200d)+1.8$. Notes: Score for taking out a common factor of $-0.002$ "
       r"from at least the $d^2$ and $d$ terms",
       r"M1 (AO 1.1b): $=-0.002\left((d-100)^2-10000\right)+1.8$. Notes: For completing the square for their $(d^2-200d)$ "
       r"term",
       r"A1 (AO 1.1b): $=21.8-0.002(d-100)^2$. Notes: $=21.8-0.002(d-100)^2$ or exact equivalent"],
      False, 16),
    e("11d", "11(d)", ALG, "2.11, 2.3", 2, LATEX["11d"],
      [r"B1ft (AO 3.4): (i) 22.1 metres. Notes: For their ‘21.8+0.3’ =22.1m",
       r"B1ft (AO 3.4): (ii) 100 metres. Notes: For their 100m"],
      False, 16),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", EXP, "6.6, 6.4", 2, LATEX["12a"],
      [r"M1 (AO 2.1): $N=aT^b\Rightarrow\log_{10}N=\log_{10}a+\log_{10}T^b$. Notes: Takes logs of both sides and shows the "
       r"addition law",
       r"A1 (AO 1.1b): $\Rightarrow\log_{10}N=\log_{10}a+b\log_{10}T$ so $m=b$ and $c=\log_{10}a$. Notes: [labelled M1 in "
       r"the notes] Uses the power law, writes $\log_{10}N=\log_{10}a+b\log_{10}T$ and states $m=b$ and $c=\log_{10}a$"],
      False, 18),
    e("12b", "12(b)", EXP, "6.6", 4, LATEX["12b"],
      [r"M1 (AO 3.1b): Uses the graph to find either $a$ or $b$ $a=10^{\text{intercept}}$ or $b$ = gradient. Notes: Uses "
       r"the graph to find either $a$ or $b$ $a=10^{\text{intercept}}$ or $b$ = gradient. This would be implied by the "
       r"sight of $b=2.3$ or $a=10^{1.8}\approx63$",
       r"M1 (AO 1.1b): Uses the graph to find both $a$ and $b$ $a=10^{\text{intercept}}$ and $b$ = gradient. Notes: Uses "
       r"the graph to find both $a$ and $b$ $a=10^{\text{intercept}}$ and $b$ = gradient. This would be implied by the "
       r"sight of $b=2.3$ and $a=10^{1.8}\approx63$",
       r"M1 (AO 3.1b): Uses $T=3$ in $N=aT^b$ with their $a$ and $b$. Notes: Uses $T=3\Rightarrow N=aT^b$ with their $a$ "
       r"and $b$. This is implied by an attempt at $63\times3^{2.3}$",
       r"A1 (AO 1.1b): Number of microbes $\approx800$. Notes: Accept a number of microbes that are approximately 800. "
       r"Allow $800\pm150$ following correct work.",
       rf"{GR12} — M1: Finds the value of $\log_{{10}}T$ from $T$=3. Accept as $T=3\Rightarrow\log_{{10}}T\approx0.48$",
       rf"{GR12} — M1: Then using the line of best fit finds the value of $\log_{{10}}N$ from their “0.48” Accept "
       rf"$\log_{{10}}N\approx2.9$",
       rf"{GR12} — M1: Finds the value of $N$ from their value of $\log_{{10}}N$ $\log_{{10}}N\approx2.9\Rightarrow "
       rf"N=10^{{\text{{‘}}2.9\text{{’}}}}$",
       rf"{GR12} — A1: Accept a number of microbes that are approximately 800. Allow $800\pm150$ following correct work"],
      True, 18),
    e("12c", "12(c)", EXP, "6.6, 2.11", 2, LATEX["12c"],
      [r"M1 (AO 3.4): $N=1000000\Rightarrow\log_{10}N=6$. Notes: For using $N$ = 1000000 and stating that $\log_{10}N=6$",
       r"A1 (AO 3.5b): We cannot ‘extrapolate’ the graph and assume that the model still holds. Notes: Statement to the "
       r"effect that “we only have information for values of $\log N$ between 1.8 and 4.5 so we cannot be certain that the "
       r"relationship still holds”. “We cannot extrapolate with any certainty, we could only interpolate”",
       r"ALT: There is an alternative approach that uses the formula. — M1: Use $N$ = 1000000 in their "
       r"$N=63\times T^{2.3}\Rightarrow\log_{10}T=\frac{\log_{10}\left(\frac{1000000}{63}\right)}{2.3}\approx1.83$ .",
       r"ALT: Alternative approach using the formula — A1: The reason would be similar to the main scheme as we only have "
       r"$\log_{10}T$ values from 0 to 1.2. We cannot ‘extrapolate’ the graph and assume that the model still holds"],
      True, 18),
    e("12d", "12(d)", EXP, "6.6", 1, LATEX["12d"],
      [r"B1 (AO 3.2a): States that ‘$a$’ is the number of microbes 1 day after the start of the experiment. Notes: Allow a "
       r"numerical explanation $T=1\Rightarrow N=a1^b\Rightarrow N=a$ giving $a$ is the value of $N$ at $T$ =1"],
      True, 18),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", DIFF, "7.5, 3.3", 2, LATEX["13a"],
      [rf"M1 (AO 1.1b): Attempts ${DY}=\frac{{\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}t}}}}{{\frac{{\mathrm{{d}}x}}{{\mathrm{{d}}t}}}}$. "
       rf"Notes: Attempts ${DY}=\frac{{\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}t}}}}{{\frac{{\mathrm{{d}}x}}{{\mathrm{{d}}t}}}}$ and "
       rf"achieves a form $k\frac{{\sin2t}}{{\sin t}}$ Alternatively candidates may apply the double angle identity for "
       rf"$\cos2t$ and achieve a form $k\frac{{\sin t\cos t}}{{\sin t}}$",
       rf"A1 (AO 1.1b): ${DY}=\frac{{\sqrt{{3}}\sin2t}}{{\sin t}}$ $\left(=2\sqrt{{3}}\cos t\right)$. Notes: Scored for a correct "
       rf"answer, either $\frac{{\sqrt{{3}}\sin2t}}{{\sin t}}$ or $2\sqrt{{3}}\cos t$"],
      False, 22),
    e("13b", "13(b)", COORD, "3.3, 3.1, 7.5", 5, LATEX["13b"],
      [rf"M1 (AO 2.1): Substitutes $t=\frac{{2\pi}}{{3}}$ in ${DY}=\frac{{\sqrt{{3}}\sin2t}}{{\sin t}}=\left(-\sqrt{{3}}\right)$. "
       rf"Notes: For substituting $t=\frac{{2\pi}}{{3}}$ in their ${DY}$ which must be in terms of $t$",
       rf"M1 (AO 2.1): Uses gradient of normal $=-\frac{{1}}{{{DY}}}=\left(\frac{{1}}{{\sqrt{{3}}}}\right)$. Notes: Uses the "
       rf"gradient of the normal is the negative reciprocal of the value of ${DY}$. This may be seen in the equation of $l$.",
       r"B1 (AO 1.1b): Coordinates of $P=\left(-1,-\frac{\sqrt{3}}{2}\right)$. Notes: States or uses (in their tangent or "
       r"normal) that $P=\left(-1,-\frac{\sqrt{3}}{2}\right)$",
       rf"M1 (AO 2.1): Correct form of normal $y+\frac{{\sqrt{{3}}}}{{2}}=\frac{{1}}{{\sqrt{{3}}}}(x+1)$. Notes: Uses their "
       rf"numerical value of $-1/{DY}$ with their $\left(-1,-\frac{{\sqrt{{3}}}}{{2}}\right)$ to form an equation of the "
       rf"normal at $P$",
       r"A1* (AO 1.1b): Completes proof $\Rightarrow2x-2\sqrt{3}y-1=0$ *. Notes: This is a proof and all aspects need to "
       r"be correct. Correct answer only $2x-2\sqrt{3}y-1=0$"],
      False, 22),
    e("13c", "13(c)", COORD, "3.3, 5.6, 2.3", 6, LATEX["13c"],
      [r"M1 (AO 3.1a): Substitutes $x=2\cos t$ and $y=\sqrt{3}\cos2t$ into $2x-2\sqrt{3}y-1=0$. Notes: For substituting "
       r"$x=2\cos t$ and $y=\sqrt{3}\cos2t$ into $2x-2\sqrt{3}y-1=0$ to produce an equation in $t$. Alternatively candidates "
       r"could use $\cos2t=2\cos^2t-1$ to set up an equation of the form $y=Ax^2+B$.",
       r"M1 (AO 3.1a): Uses the identity $\cos2t=2\cos^2t-1$ to produce a quadratic in $\cos t$. Notes: Uses the identity "
       r"$\cos2t=2\cos^2t-1$ to produce a quadratic equation in $\cos t$ In the alternative method it is for combining their "
       r"$y=Ax^2+B$ with $2x-2\sqrt{3}y-1=0$ to get an equation in just one variable",
       r"A1 (AO 1.1b): $\Rightarrow12\cos^2t-4\cos t-5=0$. Notes: For the correct quadratic equation $12\cos^2t-4\cos t-5=0$ "
       r"Alternatively the equations in $x$ and $y$ are $3x^2-2x-5=0$ $12\sqrt{3}y^2+4y-7\sqrt{3}=0$",
       r"M1 (AO 2.4): Finds $\cos t=\frac{5}{6},\left(-\frac{1}{2}\right)$ [the $-\frac{1}{2}$ is crossed out]. Notes: "
       r"Solves the quadratic equation in $\cos t$ (or $x$ or $y$) and rejects the value corresponding to $P$.",
       r"M1 (AO 1.1b): Substitutes their $\cos t=\frac{5}{6}$ into $x=2\cos t$, $y=\sqrt{3}\cos2t$ ,. Notes: Substitutes "
       r"their $\cos t=\frac{5}{6}$ or their $t=\arccos\left(\frac{5}{6}\right)$ in $x=2\cos t$ and $y=\sqrt{3}\cos2t$ If a "
       r"value of $x$ or $y$ has been found it is for finding the other coordinate.",
       r"A1 (AO 1.1b): $Q=\left(\frac{5}{3},\frac{7}{18}\sqrt{3}\right)$. Notes: $Q=\left(\frac{5}{3},\frac{7}{18}"
       r"\sqrt{3}\right)$. Allow $x=\frac{5}{3},y=\frac{7}{18}\sqrt{3}$ but do not allow decimal equivalents."],
      False, 22),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", NUM, "9.4", 3, LATEX["14a"],
      [r"B1 (AO 1.1b): Uses or implies $h=0.5$. Notes: States or uses the strip width $h=0.5$. This can be implied by the "
       r"sight of $\frac{0.5}{2}\{\ldots\}$ in the trapezium rule",
       r"M1 (AO 1.1b): For correct form of the trapezium rule =. Notes: For the correct form of the bracket in the "
       r"trapezium rule. Must be $y$ values rather than $x$ values {first $y$ value + last $y$ value + 2×(sum of other $y$ "
       r"values)}",
       r"A1 (AO 1.1b): $\frac{0.5}{2}\{3+2.2958+2(2.3041+1.9242+1.9089)\}=4.393$. Notes: 4.393"],
      True, 26),
    e("14b", "14(b)", NUM, "9.4", 1, LATEX["14b"],
      [r"B1 (AO 2.4): Any valid statement reason, for example • Increase the number of strips • Decrease the width of the "
       r"strips • Use more trapezia. Notes: See scheme"],
      True, 26),
    e("14c", "14(c)", INT, "8.5, 8.3, 6.4", 6, LATEX["14c"],
      [r"M1 (AO 2.1): For integration by parts on $\int x^2\ln x\,\mathrm{d}x$. Notes: Uses integration by parts the right "
       r"way around. Look for $\int x^2\ln x\,\mathrm{d}x=Ax^3\ln x-\int Bx^2\,\mathrm{d}x$",
       r"A1 (AO 1.1b): $=\frac{x^3}{3}\ln x-\int\frac{x^2}{3}\,\mathrm{d}x$. Notes: $\frac{x^3}{3}\ln x-\int\frac{x^2}{3}\,"
       r"\mathrm{d}x$",
       r"B1 (AO 1.1b): $\int-2x+5\,\mathrm{d}x=-x^2+5x\ (+c)$. Notes: Integrates the $-2x+5$ term correctly $=-x^2+5x$",
       r"M1 (AO 2.1): All integration attempted and limits used Area of $S=\int_1^3\frac{x^2\ln x}{3}-2x+5\,\mathrm{d}x="
       r"\left[\frac{x^3}{9}\ln x-\frac{x^3}{27}-x^2+5x\right]_{x=1}^{x=3}$. Notes: All integration completed and limits used",
       r"M1 (AO 2.1): Uses correct ln laws, simplifies and writes in required form. Notes: Simplifies using ln law(s) to a "
       r"form $\frac{a}{b}+\ln c$",
       r"A1 (AO 1.1b): Area of $S=\frac{28}{27}+\ln27$ $(a=28,b=27,c=27)$. Notes: Correct answer only "
       r"$\frac{28}{27}+\ln27$"],
      True, 26),

    # ---------------- Q15 ----------------
    e("15a", "15(a)", DIFF, "7.4, 7.3, 5.5", 4, LATEX["15a"],
      [r"M1 (AO 2.1): Attempts to differentiate using the quotient rule or otherwise. Notes: Attempts to differentiate by "
       r"using the quotient rule with $u=4\sin2x$ and $v=\mathrm{e}^{\sqrt{2}x-1}$ or alternatively uses the product rule "
       r"with $u=4\sin2x$ and $v=\mathrm{e}^{1-\sqrt{2}x}$",
       r"A1 (AO 1.1b): $\mathrm{f}'(x)=\frac{\mathrm{e}^{\sqrt{2}x-1}\times8\cos2x-4\sin2x\times\sqrt{2}\mathrm{e}^{\sqrt{2}x-1}}"
       r"{\left(\mathrm{e}^{\sqrt{2}x-1}\right)^2}$. Notes: For achieving a correct $\mathrm{f}'(x)$ . For the product rule "
       r"$\mathrm{f}'(x)=\mathrm{e}^{1-\sqrt{2}x}\times8\cos2x+4\sin2x\times-\sqrt{2}\mathrm{e}^{1-\sqrt{2}x}$",
       r"M1 (AO 2.1): Sets $\mathrm{f}'(x)=0$ and divides/ factorises out the $\mathrm{e}^{\sqrt{2}x-1}$ terms. Notes: This "
       r"is scored for cancelling/ factorising out the exponential term. Look for an equation in just $\cos2x$ and "
       r"$\sin2x$",
       r"A1* (AO 1.1b): Proceeds via $\frac{\sin2x}{\cos2x}=\frac{8}{4\sqrt{2}}$ to $\Rightarrow\tan2x=\sqrt{2}$ *. Notes: "
       r"Proceeds to $\tan2x=\sqrt{2}$ . This is a given answer."],
      True, 30),
    e("15b", "15(b)", ALG, "2.9, 5.7", 4, LATEX["15b"],
      [r"M1 (AO 3.1a): (i) Solves $\tan4x=\sqrt{2}$ and attempts to find the 2nd solution. Notes: Solves $\tan4x=\sqrt{2}$ "
       r"attempts to find the 2nd solution. Look for $x=\frac{\pi+\arctan\sqrt{2}}{4}$ Alternatively finds the 2nd solution "
       r"of $\tan2x=\sqrt{2}$ and attempts to divide by 2",
       r"A1 (AO 1.1b): $x=1.02$. Notes: Allow awrt $x=1.02$ . The correct answer, with no incorrect working scores both "
       r"marks",
       r"M1 (AO 3.1a): (ii) Solves $\tan2x=\sqrt{2}$ and attempts to find the 1st solution. Notes: Solves "
       r"$\tan2x=\sqrt{2}$ attempts to find the 1st solution. Look for $x=\frac{\arctan\sqrt{2}}{2}$",
       r"A1 (AO 1.1b): $x=0.478$. Notes: Allow awrt $x=0.478$ . The correct answer, with no incorrect working scores both "
       r"marks"],
      True, 30),
]

# No examiner report is published for the SAM, so there is nothing to apply.
W = None
REPORT = {}

# No report, so no difficulty can be judged: every part is (None, None).
RATINGS = {q: (None, None) for q in
           ["01a", "01b", "01c", "02a", "02b", "03a", "03b", "04", "05", "06a", "06b", "07", "08a", "08b", "08c", "09a",
            "09b", "10", "11a", "11b", "11c", "11d", "12a", "12b", "12c", "12d", "13a", "13b", "13c", "14a", "14b",
            "14c", "15a", "15b"]}


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
