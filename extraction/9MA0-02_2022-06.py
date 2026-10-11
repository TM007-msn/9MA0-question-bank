"""Draft builder for 9MA0-02 2022-06 (A level Pure Paper 2, June 2022).

Run (from the project root, with the venv active):
    python extraction/9MA0-02_2022-06.py        # writes out/drafts/9MA0-02_2022-06.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-02_2022-06.json

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

P, S = "9MA0-02", "2022-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "12aii"); label as printed (e.g. "12(a)(ii)")."""
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


def V(x):
    """A vector arrow over two letters, e.g. V("OD")."""
    return r"\overrightarrow{" + x + "}"


DYDX = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
i_, j_, k_ = r"\mathbf{i}", r"\mathbf{j}", r"\mathbf{k}"
SHOW = "In this question you must show all stages of your working."
CALC1 = [SHOW, "Solutions relying entirely on calculator technology are not acceptable."]
CALC2 = [SHOW, "Solutions relying on calculator technology are not acceptable."]

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q3 = [r"A sequence of terms $a_1, a_2, a_3, \ldots$ is defined by",
      r"$$\begin{aligned}a_1&=3\\a_{n+1}&=8-a_n\end{aligned}$$"]
Q5 = [r"The table below shows corresponding values of $x$ and $y$ for $y=\log_32x$",
      r"The values of $y$ are given to 2 decimal places as appropriate.",
      r"$$\begin{array}{|c|c|c|c|c|c|}\hline x&3&4.5&6&7.5&9\\\hline y&1.63&2&2.26&2.46&2.63\\"
      r"\hline\end{array}$$"]
Q5A = [r"Using the trapezium rule with all the values of $y$ in the table, find an estimate for",
       r"$$\int_3^9\log_32x\,\mathrm{d}x$$"]
Q6 = [r"[Figure 2: part of the curve $y=\mathrm{f}(x)$ for $x>0$. It starts on the positive $y$-axis, rises a little "
      r"to a maximum, then falls steeply, crossing the positive $x$-axis at the point marked $\alpha$, down to a "
      r"minimum below the $x$-axis; it then rises to the local maximum point $P$, which is also below the $x$-axis, "
      r"and falls steeply again towards the bottom right.]",
      r"Figure 2 shows a sketch of part of the curve with equation $y=\mathrm{f}(x)$ where",
      r"$$\mathrm{f}(x)=8\sin\left(\frac{1}{2}x\right)-3x+9\qquad x>0$$",
      r"and $x$ is measured in radians.",
      r"The point $P$, shown in Figure 2, is a local maximum point on the curve."]
Q6B = [r"The curve crosses the $x$-axis at $x=\alpha$, as shown in Figure 2.",
       r"Given that, to 3 decimal places, $\mathrm{f}(4)=4.274$ and $\mathrm{f}(5)=-1.212$"]
Q7A = [r"Find the first four terms, in ascending powers of $x$, of the binomial expansion of", r"$$\sqrt{4-9x}$$",
       "writing each term in simplest form."]
Q9 = [r"[Figure 4: a Ferris wheel on an A-shaped support standing on horizontal ground; a vertical double-headed "
      r"arrow beside the wheel, from the ground upwards, is labelled $H$.]",
      r"[Figure 5: a graph of $H$ against $t$ with origin $O$. The curve starts at a small positive value on the "
      r"$H$-axis, rises to a single maximum, then falls to touch the $t$-axis, where a short piece of the curve "
      r"begins to rise again.]",
      "Figure 4 shows a sketch of a Ferris wheel.",
      r"The height above the ground, $H$ m, of a passenger on the Ferris wheel, $t$ seconds after the wheel starts "
      r"turning, is modelled by the equation",
      r"$$H=\left|A\sin(bt+\alpha)^\circ\right|$$",
      r"where $A$, $b$ and $\alpha$ are constants.",
      r"Figure 5 shows a sketch of the graph of $H$ against $t$, for one revolution of the wheel.",
      "Given that",
      "• the maximum height of the passenger above the ground is 50 m",
      "• the passenger is 1 m above the ground when the wheel starts turning",
      "• the wheel takes 720 seconds to complete one revolution"]
Q10 = ["The function f is defined by", r"$$\mathrm{f}(x)=\frac{8x+5}{2x+3}\qquad x>-\frac{3}{2}$$"]
Q10G = ["The function g is defined by", r"$$\mathrm{g}(x)=16-x^2\qquad0\leqslant x\leqslant4$$"]
Q12 = ["The function f is defined by", r"$$\mathrm{f}(x)=\frac{\mathrm{e}^{3x}}{4x^2+k}$$",
       r"where $k$ is a positive constant."]
Q12A = ["Show that", r"$$\mathrm{f}'(x)=(12x^2-8x+3k)\mathrm{g}(x)$$", r"where $\mathrm{g}(x)$ is a function to be found."]
Q13 = [r"Relative to a fixed origin $O$",
       r"• the point $A$ has position vector $4" + i_ + "-3" + j_ + "+5" + k_ + "$",
       r"• the point $B$ has position vector $4" + j_ + "+6" + k_ + "$",
       r"• the point $C$ has position vector $-16" + i_ + "+p" + j_ + "+10" + k_ + "$",
       r"where $p$ is a constant.",
       r"Given that $A$, $B$ and $C$ lie on a straight line,"]
Q14A = r"Express $\dfrac{3}{(2x-1)(x+1)}$ in partial fractions."
Q14 = [r"When chemical $A$ and chemical $B$ are mixed, oxygen is produced.",
       "A scientist mixed these two chemicals and measured the total volume of oxygen produced over a period of time.",
       r"The total volume of oxygen produced, $V$ m$^3$, $t$ hours after the chemicals were mixed, is modelled by the "
       r"differential equation",
       r"$$\frac{\mathrm{d}V}{\mathrm{d}t}=\frac{3V}{(2t-1)(t+1)}\qquad V\geqslant0\qquad t\geqslant k$$",
       r"where $k$ is a constant.",
       r"Given that exactly 2 hours after the chemicals were mixed, a total volume of 3 m$^3$ of oxygen had been "
       r"produced,"]
Q14B = ["solve the differential equation to show that", r"$$V=\frac{3(2t-1)}{(t+1)}$$"]
Q15 = [*CALC2, "Given that the first three terms of a geometric series are",
       r"$$12\cos\theta\qquad5+2\sin\theta\qquad\text{and}\qquad6\tan\theta$$"]
Q15A = ["show that", r"$$4\sin^2\theta-52\sin\theta+25=0$$"]
Q15G = r"Given that $\theta$ is an obtuse angle measured in radians,"
Q15B = r"solve the equation in part (a) to find the exact value of $\theta$"
Q16 = [r"[Figure 6: the curve $C$, a U-shaped arc above the $x$-axis: it starts just left of the $y$-axis, falls to a "
       r"minimum just right of the $y$-axis, then rises steeply to the top right. The point $P$ lies on the rising "
       r"part of $C$. The straight line $l$, with negative gradient, crosses the positive $y$-axis, passes through $P$ "
       r"and continues down to the right.]",
       r"Figure 6 shows a sketch of the curve $C$ with parametric equations",
       r"$$x=2\tan t+1\qquad y=2\sec^2t+3\qquad-\frac{\pi}{4}\leqslant t\leqslant\frac{\pi}{3}$$",
       r"The line $l$ is the normal to $C$ at the point $P$ where $t=\frac{\pi}{4}$"]
Q16B = [r"Show that all points on $C$ satisfy the equation", r"$$y=\frac{1}{2}(x-1)^2+5$$"]

LATEX = {
    "01": L(*CALC1,
            r"[Figure 1: the graph of $y=\left|3-2x\right|$, a V shape with its vertex on the positive $x$-axis just "
            r"to the right of $O$; the left branch crosses the positive $y$-axis and both branches rise to the top of "
            r"the diagram.]",
            r"Figure 1 shows a sketch of the graph with equation $y=\left|3-2x\right|$", "Solve",
            r"$$\left|3-2x\right|=7+x$$"),
    "02a": L("Sketch the curve with equation", r"$$y=4^x$$",
             "stating any points of intersection with the coordinate axes."),
    "02b": L("Solve", r"$$4^x=100$$", "giving your answer to 2 decimal places."),
    "03a": L(*Q3, "(i) Show that this sequence is periodic.", "(ii) State the order of this periodic sequence."),
    "03b": L(*Q3, "Find the value of", r"$$\sum_{n=1}^{85}a_n$$"),
    "04": L("Given that", r"$$y=2x^2$$", "use differentiation from first principles to show that",
            r"$$" + DYDX + "=4x$$"),
    "05a": L(*Q5, *Q5A),
    "05b": L(*Q5, "(a) " + Q5A[0], Q5A[1], "Using your answer to part (a) and making your method clear, estimate",
             r"(b) (i) $\displaystyle\int_3^9\log_3(2x)^{10}\,\mathrm{d}x$",
             r"(ii) $\displaystyle\int_3^9\log_318x\,\mathrm{d}x$"),
    "06a": L(*Q6, "Using calculus and the sketch in Figure 2,",
             r"find the $x$ coordinate of $P$, giving your answer to 3 significant figures."),
    "06b": L(*Q6, *Q6B, r"Explain why $\alpha$ must lie in the interval $[4, 5]$"),
    "06c": L(*Q6, *Q6B,
             r"Taking $x_0=5$ as a first approximation to $\alpha$, apply the Newton-Raphson method once to "
             r"$\mathrm{f}(x)$ to obtain a second approximation to $\alpha$.",
             "Show your method and give your answer to 3 significant figures."),
    "07a": L(*Q7A),
    "07b": L("(a) " + Q7A[0], *Q7A[1:],
             r"A student uses this expansion with $x=\frac{1}{9}$ to find an approximation for $\sqrt{3}$",
             "Using the answer to part (a) and without doing any calculations,",
             r"(b) state whether this approximation will be an overestimate or an underestimate of $\sqrt{3}$ giving "
             r"a brief reason for your answer."),
    "08": L(*CALC2,
            r"[Figure 3: a curve for $x>0$ that comes down steeply from high up near the positive $y$-axis, crosses "
            r"the positive $x$-axis, reaches a minimum below the $x$-axis, then rises to cross the $x$-axis again and "
            r"continues up to the top right; the region $R$ between the curve and the $x$-axis, below the axis, is "
            r"shaded.]",
            "Figure 3 shows a sketch of part of a curve with equation",
            r"$$y=\frac{(x-2)(x-4)}{4\sqrt{x}}\qquad x>0$$",
            r"The region $R$, shown shaded in Figure 3, is bounded by the curve and the $x$-axis.",
            r"Find the exact area of $R$, writing your answer in the form $a\sqrt{2}+b$, where $a$ and $b$ are "
            r"constants to be found."),
    "09a": L(*Q9, r"find a complete equation for the model, giving the exact value of $A$, the exact value of $b$ "
                  r"and the value of $\alpha$ to 3 significant figures."),
    "09b": L(*Q9, "Explain why an equation of the form", r"$$H=\left|A\sin(bt+\alpha)^\circ\right|+d$$",
             r"where $d$ is a positive constant, would be a more appropriate model."),
    "10a": L(*Q10, r"Find $\mathrm{f}^{-1}\left(\frac{3}{2}\right)$"),
    "10b": L(*Q10, "Show that", r"$$\mathrm{f}(x)=A+\frac{B}{2x+3}$$", r"where $A$ and $B$ are constants to be found."),
    "10c": L(*Q10, *Q10G, r"State the range of $\mathrm{g}^{-1}$"),
    "10d": L(*Q10, *Q10G, r"(c) State the range of $\mathrm{g}^{-1}$", r"(d) Find the range of $\mathrm{fg}^{-1}$"),
    "11": L("Prove, using algebra, that", r"$$n(n^2+5)$$", r"is even for all $n\in\mathbb{N}$."),
    "12a": L(*Q12, *Q12A),
    "12b": L(*Q12, "(a) " + Q12A[0], *Q12A[1:],
             r"Given that the curve with equation $y=\mathrm{f}(x)$ has at least one stationary point,",
             r"(b) find the range of possible values of $k$."),
    "13a": L(*Q13, r"find the value of $p$."),
    "13b": L(*Q13, r"(a) find the value of $p$.",
             r"The line segment $OB$ is extended to a point $D$ so that $" + V("CD") + "$ is parallel to $" + V("OA")
             + "$",
             r"(b) Find $\left|" + V("OD") + r"\right|$, writing your answer as a fully simplified surd."),
    "14a": L(Q14A),
    "14b": L("(a) " + Q14A, *Q14, "(b) " + Q14B[0], Q14B[1]),
    "14c": L("(a) " + Q14A, *Q14, "(b) " + Q14B[0], Q14B[1], "The scientist noticed that",
             "• there was a time delay between the chemicals being mixed and oxygen being produced",
             "• there was a limit to the total volume of oxygen produced",
             "Deduce from the model",
             "(c) (i) the time delay giving your answer in minutes,",
             r"(ii) the limit giving your answer in m$^3$"),
    "15a": L(*Q15, *Q15A),
    "15b": L(*Q15, "(a) " + Q15A[0], Q15A[1], Q15G, "(b) " + Q15B),
    "15c": L(*Q15, "(a) " + Q15A[0], Q15A[1], Q15G, "(b) " + Q15B,
             "(c) show that the sum to infinity of the series can be expressed in the form", r"$$k(1-\sqrt{3})$$",
             r"where $k$ is a constant to be found."),
    "16a": L(*Q16, "Using parametric differentiation, show that an equation for $l$ is",
             r"$$y=-\frac{1}{2}x+\frac{17}{2}$$"),
    "16b": L(*Q16, *Q16B),
    "16c": L(*Q16, "(b) " + Q16B[0], Q16B[1], "The straight line with equation",
             r"$$y=-\frac{1}{2}x+k\qquad\text{where }k\text{ is a constant}$$",
             r"intersects $C$ at two distinct points.", r"(c) Find the range of possible values for $k$."),
}

# Repeated mark-scheme pieces.
Q1A1 = (r"A1 (AO 1.1b): For $\textbf{both}$ $x=-\frac{4}{3}$ $\textbf{and}$ $x=10$ with no extra solutions. Notes: For "
        r"both $x=-\frac{4}{3}$ and $x=10$ with no extra solutions and neither clearly rejected but ignore any attempts "
        r"to find the $y$ coordinates whether correct or otherwise and ignore reference to e.g. $x=-7$ (from where "
        r"$y=7+x$ intersects the $x$-axis) or $x=1.5$ (from finding the value of $x$ at the vertex) as “extras”. Allow "
        r"exact equivalents for $-\frac{4}{3}$ e.g. $-1\frac{1}{3}$ or $-1.\dot{3}$ but not rounded e.g. $-1.33$ Isw if "
        r"necessary e.g. ignore subsequent attempts to put the values in an inequality e.g. $-\frac{4}{3}<x<10$ But if "
        r"e.g. $x=-\frac{4}{3}$ is obtained and a candidate states $x=\left|-\frac{4}{3}\right|$ then score A0")
Q7_ = r"\left(1-\frac{9x}{4}\right)^{\frac{1}{2}}"
Q7ANS = r"\sqrt{4-9x}=2-\frac{9x}{4}-\frac{81x^2}{64}-\frac{729x^3}{512}"
Q7A2 = (r"A1 (AO 1.1b): $" + Q7ANS + r"$. Notes: $" + Q7ANS + r"$ oe and condone e.g. $2+\frac{-9x}{4}-\frac{81x^2}{64}"
        r"-\frac{729x^3}{512}$ Allow equivalent mixed numbers and/or decimals for the coefficients e.g.: "
        r"$\left(\frac{9}{4},2\frac{1}{4},2.25\right)$, $\left(\frac{81}{64},1\frac{17}{64},1.265625\right)$, "
        r"$\left(\frac{729}{512},1\frac{217}{512},1.423828125\right)$ Ignore any extra terms if found. Allow terms to be "
        r"“listed” and apply isw once a correct expansion is seen. Allow recovery if applicable e.g. if an “$x$” is lost "
        r"then “reappears”.")
Q8M1L = (r"M1 (AO 2.2a): Deduces limits of integral are 2 and 4 and applies to their ")
Q8A1 = (r"A1 (AO 2.1): Area $R=\frac{12}{5}\sqrt{2}-\frac{16}{5}$ $\left(\text{or }\frac{16}{5}-\frac{12}{5}\sqrt{2}"
        r"\right)$. Notes: Correct working shown leading to $\frac{12}{5}\sqrt{2}-\frac{16}{5}$ but also allow "
        r"$\frac{16}{5}-\frac{12}{5}\sqrt{2}$ or exact equivalents Award this mark once one of these forms is reached "
        r"and isw")
FG = r"\mathrm{fg}^{-1}"
Q10DA1 = (r"A1 (AO 2.1): Range $\frac{5}{3}\leqslant" + FG + r"(x)\leqslant\frac{37}{11}$. Notes: Correct answer written "
          r"in the correct form. E.g. $\frac{5}{3}\leqslant" + FG + r"(x)\leqslant\frac{37}{11}$, $\frac{5}{3}\leqslant"
          r"\text{range}\leqslant\frac{37}{11}$, $\frac{5}{3}\leqslant y\leqslant\frac{37}{11}$, $" + FG
          + r"(x)\leqslant\frac{37}{11}$ and $" + FG + r"(x)\geqslant\frac{5}{3}$, $\frac{5}{3}\leqslant" + FG
          + r"\leqslant\frac{37}{11}$, $" + FG + r"(x)\leqslant\frac{37}{11}\cap" + FG + r"(x)\geqslant\frac{5}{3}$, "
          r"$\left[\frac{5}{3},\frac{37}{11}\right]$ but not e.g. $\frac{5}{3}\leqslant x\leqslant\frac{37}{11}$")
OD13 = r"$\left|" + V("OD") + r"\right|=5\times\sqrt{4^2+6^2}=10\sqrt{13}$"
Q14B1 = (r"B1 (AO 1.1a): $\int\frac{1}{V}\,\mathrm{d}V=\int\frac{3}{(2t-1)(t+1)}\,\mathrm{d}t$. Notes: Separates "
         r"variables $\int\frac{1}{V}\,\mathrm{d}V=\int\frac{3}{(2t-1)(t+1)}\,\mathrm{d}t$. May be implied by later "
         r"work. Condone omission of the integral signs but the $\mathrm{d}V$ and $\mathrm{d}t$ must be in the correct "
         r"positions if awarding this mark in isolation but they may be implied by subsequent work.")
Q14M1 = (r"Notes: Correct attempt at integration of the partial fractions. Look for $\ldots\ln(2t-1)+\ldots\ln(t+1)$ "
         r"where … are constants. Condone missing brackets around the $(2t-1)$ and/or the $(t+1)$ for this mark")
Q14A1F = (r"Notes: Fully correct equation following through their $A$ and $B$ $\textbf{only}$. No requirement for $+c$ "
          r"here. The brackets around the $(2t-1)$ and/or the $(t+1)$ must be seen or implied for this mark")
Q14M2 = (r"Notes: Attempts to find “$c$” or e.g. “$\ln k$” using $t=2$, $V=3$ following an attempt at integration. "
         r"Condone poor algebra as long as $t=2$, $V=3$ is used to find a value of their constant. Note that the "
         r"constant may be found immediately after integrating or e.g. after the ln’s have been combined.")
Q14A1S = r"Notes: Correct processing leading to the given answer $V=\frac{3(2t-1)}{(t+1)}$"
Q15A1 = (r"A1* (AO 2.1): Proceeds to given answer $25+20\sin\theta+4\sin^2\theta=72\sin\theta\Rightarrow4\sin^2\theta"
         r"-52\sin\theta+25=0$ *. Notes: Proceeds to the given answer including the “ = 0” with no errors and "
         r"sufficient working shown.")
Q16C = r"\frac{1}{2}(x-1)^2+5"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", ALG, "2.7", 4, LATEX["01"],
      [r"M1 (AO 1.1b): For an attempt to solve $\textbf{Either}$ $3-2x=7+x\Rightarrow x=\ldots$ or $2x-3=7+x\Rightarrow "
       r"x=\ldots$. Notes: $\textbf{Note this question requires working to be shown not}$ "
       r"$\underline{\textbf{just answers written down}}$. $\textbf{But correct equations seen followed by the correct "
       r"answers can score full marks.}$ Attempts to solve either correct equation. Allow equivalent equations e.g. "
       r"$3-2x=-7-x\Rightarrow x=\ldots$",
       r"A1 (AO 1.1b): $\textbf{Either}$ $x=-\frac{4}{3}$ or $x=10$. Notes: One correct solution. Allow exact "
       r"equivalents for $-\frac{4}{3}$ e.g. $-1\frac{1}{3}$ or $-1.\dot{3}$ but not e.g. $-1.33$",
       r"dM1 (AO 1.1b): For an attempt to solve $\textbf{Both}$ $3-2x=7+x\Rightarrow x=\ldots$ $\textbf{and}$ "
       r"$2x-3=7+x\Rightarrow x=\ldots$. Notes: Attempts to solve both correct equations. Allow equivalent equations "
       r"e.g. $3-2x=-7-x\Rightarrow x=\ldots$ $\textbf{Depends on the first method mark.}$",
       Q1A1,
       r"ALT: Alternative by squaring — M1 (AO 1.1b): $(3-2x)^2=(7+x)^2\Rightarrow9-12x+4x^2=49+14x+x^2$. Notes: "
       r"Attempts to square both sides. Condone poor squaring e.g. $(3-2x)^2=9\pm4x^2$ or $9\pm2x^2$",
       r"ALT: Alternative by squaring — A1 (AO 1.1b): $3x^2-26x-40=0$. Notes: Correct quadratic equation "
       r"$3x^2-26x-40=0$. The “= 0” may be implied by their attempt to solve. Terms must be collected but not "
       r"necessarily all on one side so allow e.g. $3x^2-26x=40$",
       r"ALT: Alternative by squaring — dM1 (AO 1.1b): $3x^2-26x-40=0\Rightarrow x=\ldots$. Notes: Correct attempt to "
       r"solve a $\textbf{3 term}$ quadratic. See general guidance for solving a quadratic equation. The roots can be "
       r"written down from a calculator so the method may be implied by their values. $\textbf{Depends on the first "
       r"method mark}$.",
       r"ALT: Alternative by squaring — " + Q1A1],
      True, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", EXP, "6.1", 2, LATEX["02a"],
      [r"B1 (AO 1.2): [Sketch: an exponential curve rising from the left, close to the negative $x$-axis, through "
       r"$(0,1)$, marked 1, and up steeply to the right] Correct shape or correct intercept – see notes. Notes: "
       r"$\textbf{Note that B0B1 is not possible in part (a)}$ (a) $\textbf{Axes do not need to be labelled. No sketch "
       r"is no marks.}$ Correct shape or correct intercept. Shape: A positive exponential curve in quadrants 1 and 2 "
       r"only, passing through a point on the positive $y$-axis. Must “level out” in quadrant 2 but not necessarily "
       r"asymptotic to the $x$-axis and allow if the curve bends up slightly for $x<0$ but do not allow a clear “U” "
       r"shape. It must not clearly “stop” on the $x$-axis to the left of the $y$-axis. $\textbf{OR}$ Intercept: The "
       r"intercept can be marked as 1 or $(0, 1)$ or $y=1$ or $(1, 0)$ as long as it is in the correct place. May also "
       r"be seen away from the sketch but must be seen as $(0, 1)$ or possibly these coordinates in a table but it "
       r"must correspond to the sketch. If there is any ambiguity, the sketch takes precedence.",
       r"B1 (AO 1.1b): Fully correct – see notes. Notes: Fully correct. Shape: A positive exponential curve in "
       r"quadrants 1 and 2 only, passing through a point on the positive $y$-axis. The curve must appear to be "
       r"asymptotic to the $x$-axis $\textbf{and it must level out at least half way below the intercept}$. Allow if "
       r"the curve bends up slightly for $x<0$ but do not allow a clear “U” shape. The curve must not bend back on "
       r"itself on the rhs of the $y$-axis. There must be no suggestion that the curve approaches another horizontal "
       r"asymptote other than the $x$-axis e.g. a horizontal dotted line that the curve approaches. $\textbf{AND}$ "
       r"Intercept: As above"],
      False, 4),
    e("02b", "2(b)", EXP, "6.5, 6.3", 2, LATEX["02b"],
      [r"M1 (AO 1.1b): $4^x=100\Rightarrow x=\log_4100$ or e.g. $x\log4=\log100\Rightarrow x=\frac{\log100}{\log4}$. "
       r"Notes: Uses logs in an attempt to solve the equation. E.g. takes log base 4 and obtains $x=\log_4100$ "
       r"Alternatively takes logs (any base) to obtain $x\log4=\log100$ and proceeds to $x=\frac{\log100}{\log4}$ "
       r"Allow if this subsequently becomes e.g. log 25 as long as $\frac{\log100}{\log4}$ is seen $\textbf{but}$ "
       r"$x\log4=\log100\Rightarrow x=\log25$ or $x\log4=\log100\Rightarrow x=\log100-\log4$ scores M0",
       r"A1 (AO 1.1b): $\Rightarrow(x=)$ awrt 3.32. Notes: awrt 3.32. A correct answer only of awrt 3.32 scores M1A1 "
       r"Note that a common incorrect answer is $x=3.218875\ldots$ and comes from ln 25 or ln 100 – ln4 and unless "
       r"$x=\frac{\ln100}{\ln4}$ is seen previously, this scores M0A0"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", SEQ, "4.2", 2, LATEX["03a"],
      [r"B1 (AO 1.1b): (i) $a_1=3$, $a_2=5$, $a_3=3\ldots$. Notes: (a)(i) Mark (a)(i) and (a)(ii) together. States the "
       r"values of at least $a_2=5$ and $a_3=3$. This is sufficient but if more terms are given they must be correct. "
       r"There is no need to see e.g. $a_2=\ldots$, $a_3=\ldots$ just look for values. Allow an algebraic approach "
       r"e.g. $a_{n+1}=8-a_n$, $a_{n+2}=8-(8-a_n)=a_n$ A conclusion is $\textbf{not}$ needed.",
       r"B1 (AO 1.1b): (ii) 2. Notes: States that the order of the periodic sequence is 2 Allow “second order”, “it "
       r"repeats every 2 numbers” or equivalent statements that convey the idea of the period being 2. Note that "
       r"$\pm2$ is B0"],
      False, 6),
    e("03b", "3(b)", SEQ, "4.3, 4.2", 2, LATEX["03b"],
      [r"M1 (AO 3.1a): $\sum_{n=1}^{85}a_n=42\times(3+5)+3$ o.e.. Notes: Attempts a $\underline{\textbf{correct}}$ "
       r"method to find $\sum_{n=1}^{85}a_n$ For example $\sum_{n=1}^{85}a_n=42\times(3+5)+3$, $\sum_{n=1}^{85}a_n="
       r"\frac{84}{2}\times3+42\times5+3$ or $\sum_{n=1}^{85}a_n=43\times(3+5)-5$ or $\sum_{n=1}^{85}a_n=43\times3+42"
       r"\times5$ or $\sum_{n=1}^{85}a_n=\frac{85}{2}\times8-1$ There may be other methods e.g. “Chunking”: "
       r"$5\times(3+5)=40$, $40\times8=320$, $320+3\times3+2\times5=339$",
       r"A1 (AO 1.1b): $=339$. Notes: 339. Correct answer only scores both marks. Attempts to use an AP formula score "
       r"M0"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04", "4", DIFF, "7.1", 3, LATEX["04"],
      [r"M1 (AO 2.1): $\frac{2(x+h)^2-2x^2}{h}=\ldots$. Notes: Throughout the question allow the use of $\delta x$ for "
       r"$h$ or any other letter e.g. $\alpha$ if used consistently. If $\delta x$ is used then you can condone e.g. "
       r"$\delta^2x$ for $\delta x^2$ as well as condoning e.g. poorly formed $\delta$'s Begins the process by writing "
       r"down the gradient of the chord and attempts to expand the correct bracket – you can condone “poor” squaring "
       r"e.g. $(x+h)^2=x^2+h^2$. Note that $\frac{2(x-h)^2-2x^2}{-h}=\ldots$ is also a possible approach.",
       r"A1 (AO 1.1b): $\frac{2(x+h)^2-2x^2}{h}=\frac{4xh+2h^2}{h}$. Notes: Reaches a correct fraction oe with the $x^2$ "
       r"terms cancelled out. E.g. $\frac{4xh+2h^2}{h}$, $\frac{\cancel{2x^2}+4xh+2h^2-\cancel{2x^2}}{h}$, $4x+2h$",
       r"A1* (AO 2.5): $" + DYDX + r"=\lim_{h\to0}\frac{4xh+2h^2}{h}=\lim_{h\to0}(4x+2h)=4x$*. Notes: Completes the "
       r"process by applying a limiting argument and deduces that $" + DYDX + r"=4x$ with no errors seen. The "
       r"“$" + DYDX + r"=$” doesn’t have to appear but there must be something equivalent e.g. “$\mathrm{f}'(x)=$” or "
       r"“Gradient =” which can appear anywhere in their working. If $\mathrm{f}'(x)$ is used then there is no "
       r"requirement to see f (x) defined first. Condone e.g. $" + DYDX + r"\to4x$ or $\mathrm{f}'(x)\to4x$. Condone "
       r"missing brackets so allow e.g. $" + DYDX + r"=\lim_{h\to0}\frac{4xh+2h^2}{h}=\lim_{h\to0}4x+2h=4x$ Do not "
       r"allow $h=0$ if there is never a reference to $h\to0$ e.g. $" + DYDX + r"=\lim_{h\to0}\frac{4xh+2h^2}{h}="
       r"\lim_{h\to0}4x+2(0)=4x$ is acceptable but e.g. $" + DYDX + r"=\frac{4xh+2h^2}{h}=4x+2h=4x+2(0)=4x$ is not if "
       r"there is no $h\to0$ seen. The $h\to0$ does not need to be present throughout the proof e.g. on every line. "
       r"They must reach $4x+2h$ at the end and not $\frac{4xh+2h^2}{h}$ (without the $h$’s cancelled) to complete the "
       r"limiting argument."],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", NUM, "9.4", 3, LATEX["05a"],
      [r"B1 (AO 1.1a): States or uses $h=1.5$. Notes: States or uses $h=1.5$",
       r"M1 (AO 1.1b): Full attempt at the trapezium rule $=\frac{\ldots}{2}\{1.63+2.63+2\times(2+2.26+2.46)\}$. Notes: "
       r"A full attempt at the trapezium rule. Look for $\frac{\text{their }h}{2}\{1.63+2.63+2\times(2+2.26+2.46)\}$ "
       r"but condone copying slips Note that $\frac{\text{their }h}{2}1.63+2.63+2\times(2+2.26+2.46)$ scores M0 unless "
       r"the missing brackets are recovered or implied by their answer. You may need to check. Allow this mark if they "
       r"add the areas of individual trapezia e.g. $\frac{\text{their }h}{2}\{1.63+2\}+\frac{\text{their }h}{2}\{2+2.26"
       r"\}+\frac{\text{their }h}{2}\{2.26+2.46\}+\frac{\text{their }h}{2}\{2.46+2.63\}$ Condone copying slips but must "
       r"be a complete method using all the trapezia.",
       r"A1 (AO 1.1b): $=$ awrt 13.3 or $\frac{531}{40}$. Notes: awrt 13.3 (Note full accuracy is 13.275) or exact "
       r"equivalent. $\textbf{Note that the calculator answer is 13.324 so you must see correct working to award awrt "
       r"13.3}$ Use of $h=-1.5$ leading to a negative area can score B1M1A0 but allow full marks if then stated as "
       r"positive."],
      False, 10),
    e("05b", "5(b)", NUM, "9.4, 6.4", 3, LATEX["05b"],
      [r"B1ft (AO 2.2a): (b)(i) $\int_3^9\log_3(2x)^{10}\,\mathrm{d}x=10\times\text{“}13.3\text{”}=$ awrt 133 or e.g. "
       r"$\frac{531}{4}$. Notes: Deduces that $\int_3^9\log_3(2x)^{10}\,\mathrm{d}x=10\times\text{“}13.3\text{”}=$ awrt "
       r"133 FT on their 13.3 look for 3sf accuracy but follow through on e.g. their rounded answer to part (a) so if "
       r"13 was their answer to part (a) then allow 130 here $\textbf{following a correct method}$. A correct method "
       r"must be seen here but a minimum is e.g. $10\times\text{“}13.3\text{”}=\text{“}133\text{”}$ Note that "
       r"$\int_3^9\log_3(2x)^{10}\,\mathrm{d}x=133.2414316\ldots$ so a correct method must be seen to award marks. "
       r"$\textbf{Attempts to apply the trapezium rule again in any way score M0 as the instruction in the question was "
       r"to use the}$ $\underline{\textbf{answer}}$ $\textbf{to part (a).}$",
       r"M1 (AO 3.1a): (ii) $\int_3^9\log_318x\,\mathrm{d}x=\int_3^9\log_3(9\times2x)\,\mathrm{d}x=\int_3^92+\log_32x"
       r"\,\mathrm{d}x$ $=[2x]_3^9+\int_3^9\log_32x\,\mathrm{d}x=18-6+\int_3^9\log_32x\,\mathrm{d}x=\ldots$. Notes: Shows "
       r"correct log work to relate the given question to part (a) Must reach as far as e.g. $[2x]_3^9+\int_3^9\log_32x"
       r"\,\mathrm{d}x=\ldots$ with correct use of limits on $[2x]_3^9$ which may be implied or equivalent work e.g. "
       r"finds the area of the rectangle as $2\times6$",
       r"A1ft (AO 1.1b): Awrt 25.3 or $\frac{1011}{40}$. Notes: $\textbf{Correct working}$ followed by awrt 25.3 but ft "
       r"on their 13.3 so allow for 12 + their answer to part (a) $\textbf{following correct work}$ as shown. Note that "
       r"$\int_3^9\log_318x\,\mathrm{d}x=25.32414\ldots$ $\textbf{so a correct method must be seen to award marks}$. "
       r"$\textbf{Some examples of an acceptable method are:}$ $\int_3^9\log_318x\,\mathrm{d}x=\int_3^9\log_3(9\times2x)"
       r"\,\mathrm{d}x=\int_3^92+\log_32x\,\mathrm{d}x=6\times2+\text{“}13.3\text{”}=25.3$ $\int_3^9\log_318x\,"
       r"\mathrm{d}x=\int_3^9\log_3(9\times2x)\,\mathrm{d}x=\int_3^92+\log_32x\,\mathrm{d}x=12+\text{“}13.3\text{”}="
       r"25.3$ $\int_3^9\log_318x\,\mathrm{d}x=\int_3^9\log_3(9\times2x)\,\mathrm{d}x=\int_3^92+\log_32x\,\mathrm{d}x="
       r"[2x]_3^9+\int_3^9\log_32x\,\mathrm{d}x=25.3$ $\textbf{BUT just}$ $12+\text{“}13.3\text{”}=25.3$ $\textbf{scores "
       r"M0}$ $\textbf{Attempts to apply the trapezium rule again in any way score M0 as the instruction in the "
       r"question was to use the}$ $\underline{\textbf{answer}}$ $\textbf{to part (a).}$"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", DIFF, "7.3, 7.2, 5.7", 4, LATEX["06a"],
      [r"M1 (AO 1.1b): $(\mathrm{f}'(x)=)4\cos\left(\frac{1}{2}x\right)-3$. Notes: Differentiates to obtain "
       r"$k\cos\left(\frac{1}{2}x\right)\pm\alpha$ where $\alpha$ is a constant which may be zero and no other terms. "
       r"The brackets are not required.",
       r"A1 (AO 1.1b): $(\mathrm{f}'(x)=)4\cos\left(\frac{1}{2}x\right)-3$. Notes: Correct derivative $\mathrm{f}'(x)="
       r"4\cos\left(\frac{1}{2}x\right)-3$. Allow unsimplified e.g. $\mathrm{f}'(x)=\frac{1}{2}\times8\cos\left("
       r"\frac{1}{2}x\right)-3x^0$ There is no need for $\mathrm{f}'(x)=\ldots$ or $" + DYDX + r"=\ldots$ just look for "
       r"the expression and the brackets are not required.",
       r"dM1 (AO 3.1a): Sets $\mathrm{f}'(x)=4\cos\left(\frac{1}{2}x\right)-3=0\Rightarrow x=$. Notes: For the complete "
       r"strategy of proceeding to a value for $x$. Look for • $\mathrm{f}'(x)=a\cos\left(\frac{1}{2}x\right)+b=0$, "
       r"$a,b\neq0$ • Correct method of finding a valid solution to $a\cos\left(\frac{1}{2}x\right)+b=0$ Allow for "
       r"$a\cos\left(\frac{1}{2}x\right)+b=0\Rightarrow\cos\left(\frac{1}{2}x\right)=\pm k\Rightarrow x=2\cos^{-1}"
       r"(\pm k)$ where $|k|<1$ If this working is not shown then you may need to check their value(s). For example "
       r"$4\cos\left(\frac{1}{2}x\right)-3=0\Rightarrow x=1.4\ldots$ or $11.1\ldots$ (or $82.8\ldots$ or $637.\ldots$ "
       r"or 803 in degrees) would indicate this method.",
       r"A1 (AO 3.2a): $x=14.0$ Cao. Notes: Selects the correct turning point $x=14.0$ and not just 14 or unrounded "
       r"e.g. $14.011\ldots$ Must be this value only and no other values unless they are clearly rejected or 14.0 "
       r"clearly selected. Ignore any attempts to find the $y$ coordinate. $\textbf{Correct answer with no working "
       r"scores no marks.}$"],
      True, 12),
    e("06b", "6(b)", NUM, "9.1", 1, LATEX["06b"],
      [r"B1 (AO 2.4): Explains that $\mathrm{f}(4)>0$, $\mathrm{f}(5)<0$ $\textbf{and}$ the function is continuous. "
       r"Notes: See scheme. Must be a full reason, (e.g. change of sign and continuous) Accept equivalent statements for "
       r"$\mathrm{f}(4)>0$, $\mathrm{f}(5)<0$ e.g. $\mathrm{f}(4)\times\mathrm{f}(5)<0$, ”there is a change of sign”, "
       r"“one negative one positive”. A minimum is “change of sign and continuous” but do $\textbf{not}$ allow this "
       r"mark if the comment about continuity is clearly incorrect e.g. “because $x$ is continuous” or “because the "
       r"interval is continuous”"],
      True, 12),
    e("06c", "6(c)", NUM, "9.3", 2, LATEX["06c"],
      [r"M1 (AO 1.1b): Attempts $x_1=5-\frac{8\sin2.5-15+9}{\text{“}4\cos2.5-3\text{”}}$ (NB $\mathrm{f}(5)=-1.212"
       r"\ldots$ and $\mathrm{f}'(5)=-6.204\ldots$). Notes: Attempts $x_1=5-\frac{\mathrm{f}(5)}{\mathrm{f}'(5)}$ to "
       r"obtain a value following through on their $\mathrm{f}'(x)$ as long as it is a “changed” function. Must be a "
       r"correct N-R formula used – may need to check their values. Allow if attempted in degrees. For reference in "
       r"degrees $\mathrm{f}(5)=-5.65\ldots$ and $\mathrm{f}'(5)=0.996\ldots$ and gives $x_1=10.67\ldots$ There must be "
       r"clear evidence that $5-\frac{\mathrm{f}(5)}{\mathrm{f}'(5)}$ is being attempted. so e.g. $x_{n+1}=x_n-"
       r"\frac{\mathrm{f}(x_n)}{\mathrm{f}'(x_n)}\Rightarrow x_1=4.80$ scores M0 as does e.g. $x_1=x-\frac{8\sin\left("
       r"\frac{1}{2}x\right)-3x+9}{4\cos\left(\frac{1}{2}x\right)-3}=4.80$ $\textbf{BUT}$ evidence may be provided by "
       r"the accuracy of their answer. Note that the full N-R accuracy is 4.804624337 so e.g. 4.805 or 4.804 "
       r"(truncated) with no evidence of incorrect work may imply the method.",
       r"A1 (AO 1.1b): $x_1=$ awrt 4.80. Notes: $x_1=$ awrt 4.80 not awrt 4.8 but isw if awrt 4.80 is seen. Ignore any "
       r"subsequent iterations. Note that work for part (a) cannot be recovered in part (c) Note also: $5-\frac{"
       r"\mathrm{f}(5)}{\mathrm{f}'(5)}=$ awrt 4.80 following a correct derivative scores M1A1 $5-\frac{\mathrm{f}(5)}"
       r"{\mathrm{f}'(5)}\neq$ awrt 4.80 with no evidence that $5-\frac{\mathrm{f}(5)}{\mathrm{f}'(5)}$ was attempted "
       r"scores M0"],
      True, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", SEQ, "4.1", 4, LATEX["07a"],
      [r"B1 (AO 1.1b): $\sqrt{4-9x}=2(1\pm\ldots)^{\frac{1}{2}}$. Notes: Takes out a factor of 4 and writes "
       r"$\sqrt{4-9x}=2(1\pm\ldots)^{\frac{1}{2}}$ or $\sqrt{4}(1\pm\ldots)^{\frac{1}{2}}$ or $4^{\frac{1}{2}}(1\pm"
       r"\ldots)^{\frac{1}{2}}$",
       r"M1 (AO 1.1b): $\left(1-\text{“}\frac{9x}{4}\text{”}\right)^{\frac{1}{2}}=\ldots+\frac{\frac{1}{2}\times\left("
       r"-\frac{1}{2}\right)\left(\text{“}-\frac{9x}{4}\text{”}\right)^2}{2!}$ or $\ldots+\frac{\frac{1}{2}\times\left("
       r"-\frac{1}{2}\right)\times\left(-\frac{3}{2}\right)\left(\text{“}-\frac{9x}{4}\text{”}\right)^3}{3!}$. Notes: "
       r"For an attempt at the binomial expansion of $(1+ax)^{\frac{1}{2}}$ $a\neq1$ to form term 3 or term 4 with the "
       r"correct structure. Look for the correct binomial coefficient multiplied by the corresponding power of $x$ e.g. "
       r"$\frac{\left(\frac{1}{2}\right)\left(\frac{1}{2}-1\right)}{2!}(\ldots x)^2$ $\textbf{or}$ $\frac{\left(\frac{1}"
       r"{2}\right)\left(\frac{1}{2}-1\right)\left(\frac{1}{2}-2\right)}{3!}(\ldots x)^3$ where $\ldots\neq1$ Condone "
       r"missing or incorrect brackets around the $x$ terms but the binomial coefficients must be correct. Allow 2! "
       r"and/or 3! or 2 and/or 6. Ignore attempts to find more terms. Do not allow notation such as "
       r"$\binom{\frac{1}{2}}{1}$, $\binom{\frac{1}{2}}{2}$ unless these are interpreted correctly.",
       r"A1 (AO 1.1b): $1+\frac{1}{2}\times\left(-\frac{9x}{4}\right)+\frac{\frac{1}{2}\times\left(-\frac{1}{2}\right)"
       r"\left(-\frac{9x}{4}\right)^2}{2!}+\frac{\frac{1}{2}\times\left(-\frac{1}{2}\right)\times\left(-\frac{3}{2}"
       r"\right)\left(-\frac{9x}{4}\right)^3}{3!}$. Notes: Correct expression for the expansion of $" + Q7_
       + r"$ e.g. $1+\frac{1}{2}\times\left(-\frac{9x}{4}\right)+\frac{\frac{1}{2}\times\left(\frac{1}{2}-1\right)"
       r"\left(\pm\frac{9x}{4}\right)^2}{2!}+\frac{\frac{1}{2}\times\left(\frac{1}{2}-1\right)\times\left(\frac{1}{2}"
       r"-2\right)\left(-\frac{9x}{4}\right)^3}{3!}$ which may be left unsimplified as shown but the bracketing must be "
       r"correct unless any missing brackets are implied by subsequent work. If the 2 outside this expansion is only "
       r"partially applied to this expansion then score A0 but if it is applied to all terms this A1 can be implied. "
       r"$\textbf{OR}$ at least 2 correct simplified terms $\textbf{for the final expansion}$ from, $-\frac{9x}{4}$, "
       r"$-\frac{81x^2}{64}$, $-\frac{729x^3}{512}$",
       Q7A2,
       r"ALT: Direct expansion in (a) can be marked in a similar way: $\sqrt{4-9x}=(4-9x)^{\frac{1}{2}}=4^{\frac{1}{2}}"
       r"+\left(\frac{1}{2}\right)4^{-\frac{1}{2}}\times(-9x)^1+\left(\frac{1}{2}\right)\left(\frac{1}{2}-1\right)"
       r"4^{-\frac{3}{2}}\times\frac{(-9x)^2}{2!}+\left(\frac{1}{2}\right)\left(\frac{1}{2}-1\right)\left(\frac{1}{2}"
       r"-2\right)4^{-\frac{5}{2}}\times\frac{(-9x)^3}{3!}$ — B1: For 2 or $\sqrt{4}$ or $4^{\frac{1}{2}}$ as the "
       r"constant term in the expansion.",
       r"ALT: Direct expansion — M1: Correct form for term 3 or term 4. E.g. $\left(\frac{1}{2}\right)\left(-\frac{1}"
       r"{2}\right)\times\frac{(\ldots x)^2}{2!}$ or $\left(\frac{1}{2}\right)\left(-\frac{1}{2}\right)\left(-\frac{3}"
       r"{2}\right)\times\frac{(\ldots x)^3}{3!}$ where $\ldots\neq1$ Condone missing brackets around the $x$ terms but "
       r"the binomial coefficients must be correct. Allow 2! and/or 3! or 2 and/or 6. Ignore attempts to find more "
       r"terms. Do not allow notation such as $\binom{\frac{1}{2}}{1}$, $\binom{\frac{1}{2}}{2}$ unless these are "
       r"interpreted correctly.",
       r"ALT: Direct expansion — A1: Correct expansion (unsimplified as above) $\textbf{OR}$ at least 2 correct "
       r"simplified terms from, $-\frac{9x}{4}$, $-\frac{81x^2}{64}$, $-\frac{729x^3}{512}$",
       r"ALT: Direct expansion — " + Q7A2],
      False, 16),
    e("07b", "7(b)", SEQ, "4.1", 1, LATEX["07b"],
      [r"B1 (AO 3.2b): States that the approximation will be an $\underline{\text{overestimate}}$ since all terms "
       r"(after the first one) in the expansion are negative (since $x>0$). Notes: States that the approximation will "
       r"be an $\underline{\textbf{overestimate}}$ due to the fact that all terms (after the first one) in the "
       r"expansion are negative or equivalent statements e.g. • Overestimate because the terms are negative • "
       r"Overestimate as the terms are being taken away (from 2) Condone “overestimate as every term is negative” If "
       r"you think a response is worthy of credit but are unsure then use Review. $\textbf{This mark depends on having "
       r"obtained an expansion in (a) of the form}$ $k-px-qx^2-rx^3$ $k,p,q,r>0$ but note that if e.g. one of the "
       r"algebraic terms is zero or was “lost” or there are extra negative terms this mark is still available."],
      False, 16),

    # ---------------- Q8 ----------------
    e("08", "8", INT, "8.3, 8.2, 2.1", 6, LATEX["08"],
      [r"M1 (AO 1.1b): $y=\frac{(x-2)(x-4)}{4\sqrt{x}}=\frac{x^2-6x+8}{4\sqrt{x}}=\frac{1}{4}x^{\frac{3}{2}}-\frac{3}{2}"
       r"x^{\frac{1}{2}}+2x^{-\frac{1}{2}}$. Notes: Correct attempt to write $\frac{(x-2)(x-4)}{4\sqrt{x}}$ as a sum of "
       r"terms with $\textbf{indices}$. Look for at least two different terms with the correct index e.g. two of "
       r"$x^{\frac{3}{2}}$, $x^{\frac{1}{2}}$, $x^{-\frac{1}{2}}$ which have come from the correct places. The correct "
       r"indices may be implied later when e.g. $\sqrt{x}$ becomes $x^{\frac{1}{2}}$ or $\frac{1}{\sqrt{x}}$ becomes "
       r"$x^{-\frac{1}{2}}$",
       r"A1 (AO 1.1b): $\frac{1}{4}x^{\frac{3}{2}}-\frac{3}{2}x^{\frac{1}{2}}+2x^{-\frac{1}{2}}$. Notes: $\frac{1}{4}"
       r"x^{\frac{3}{2}}-\frac{3}{2}x^{\frac{1}{2}}+2x^{-\frac{1}{2}}$ which can be left unsimplified e.g. $\frac{1}{4}"
       r"x^{2-\frac{1}{2}}-\frac{1}{2}x^{\frac{1}{2}}-x^{\frac{1}{2}}+2x^{-\frac{1}{2}}$ or as e.g. $\frac{1}{4}\left("
       r"x^{\frac{3}{2}}-6x^{\frac{1}{2}}+8x^{-\frac{1}{2}}\right)$ The correct indices may be implied later when e.g. "
       r"$\sqrt{x}$ becomes $x^{\frac{1}{2}}$ or $\frac{1}{\sqrt{x}}$ becomes $x^{-\frac{1}{2}}$",
       r"dM1 (AO 3.1a): $\int\frac{1}{4}x^{\frac{3}{2}}-\frac{3}{2}x^{\frac{1}{2}}+2x^{-\frac{1}{2}}\,\mathrm{d}x=\frac{1}"
       r"{10}x^{\frac{5}{2}}-x^{\frac{3}{2}}+4x^{\frac{1}{2}}(+c)$. Notes: Integrates $x^n\to x^{n+1}$ for at least 2 "
       r"correct indices i.e. at least 2 of $x^{\frac{3}{2}}\to x^{\frac{5}{2}}$, $x^{\frac{1}{2}}\to x^{\frac{3}{2}}$, "
       r"$x^{-\frac{1}{2}}\to x^{\frac{1}{2}}$ It is dependent upon the first M so at least two terms must have had a "
       r"correct index.",
       r"A1 (AO 1.1b): $\frac{1}{10}x^{\frac{5}{2}}-x^{\frac{3}{2}}+4x^{\frac{1}{2}}(+c)$. Notes: $\frac{1}{10}x^{\frac{5}"
       r"{2}}-x^{\frac{3}{2}}+4x^{\frac{1}{2}}(+c)$. Allow unsimplified e.g. $\frac{1}{4}\times\frac{2}{5}x^{\frac{3}{2}"
       r"+1}-\frac{1}{2}\times\frac{2}{3}x^{\frac{1}{2}+1}-\frac{2}{3}x^{\frac{1}{2}+1}+2\times2x^{\frac{1}{2}}$ or as "
       r"e.g. $\frac{1}{4}\left(\frac{2}{5}x^{\frac{5}{2}}-4x^{\frac{3}{2}}+16x^{\frac{1}{2}}\right)(+c)$.",
       Q8M1L + r"$\frac{1}{10}x^{\frac{5}{2}}-x^{\frac{3}{2}}+4x^{\frac{1}{2}}$. Notes: Substitutes the limits 4 and 2 to "
       r"their $\frac{1}{10}x^{\frac{5}{2}}-x^{\frac{3}{2}}+4x^{\frac{1}{2}}$ and subtracts either way round. There is "
       r"no requirement to evaluate but 4 and 2 must be substituted either way round with evidence of subtraction, "
       r"condoning omission of brackets. E.g. condone $\frac{1}{10}\times4^{\frac{5}{2}}-4^{\frac{3}{2}}+4\times4^{"
       r"\frac{1}{2}}-\frac{1}{10}\times2^{\frac{5}{2}}-2^{\frac{3}{2}}+4\times2^{\frac{1}{2}}$ This is an independent "
       r"mark but the limits must be applied to an expression that is not $y$ so they may even have differentiated.",
       r"A1 (AO 2.1): $\left(\frac{32}{10}-8+8\right)-\left(\frac{2}{5}\sqrt{2}-2\sqrt{2}+4\sqrt{2}\right)=\frac{16}{5}-"
       r"\frac{12}{5}\sqrt{2}$ Area $R=\frac{12}{5}\sqrt{2}-\frac{16}{5}$ $\left(\text{or }\frac{16}{5}-\frac{12}{5}"
       r"\sqrt{2}\right)$. Notes: Correct working shown leading to $\frac{12}{5}\sqrt{2}-\frac{16}{5}$ but also allow "
       r"$\frac{16}{5}-\frac{12}{5}\sqrt{2}$ or exact equivalents Award this mark once one of these forms is reached "
       r"and isw",
       r"ALT: Integration by parts — M1 (AO 1.1b): $\int\frac{(x-2)(x-4)}{4\sqrt{x}}\,\mathrm{d}x=\int\frac{1}{4}(x-2)"
       r"(x-4)x^{-\frac{1}{2}}\,\mathrm{d}x=\frac{1}{2}(x-2)(x-4)x^{\frac{1}{2}}-\int\frac{1}{2}(2x-6)x^{\frac{1}{2}}\,"
       r"\mathrm{d}x$. Notes: Applies integration by parts and reaches the form $\alpha(x-2)(x-4)x^{\frac{1}{2}}\pm\int"
       r"(px+q)x^{\frac{1}{2}}\,\mathrm{d}x$ $\alpha,p\neq0$ oe e.g. $\alpha(x^2-6x+8)x^{\frac{1}{2}}\pm\int(px+q)x^{"
       r"\frac{1}{2}}\,\mathrm{d}x$ $\alpha,p\neq0$",
       r"ALT: Integration by parts — A1 (AO 1.1b): Correct first application of parts in any form",
       r"ALT: Integration by parts — dM1 (AO 3.1a): $\frac{1}{2}(x-2)(x-4)x^{\frac{1}{2}}-\int\frac{1}{2}(2x-6)x^{\frac{1}"
       r"{2}}\,\mathrm{d}x=\frac{1}{2}(x-2)(x-4)x^{\frac{1}{2}}-\int x^{\frac{3}{2}}-3x^{\frac{1}{2}}\,\mathrm{d}x$. "
       r"Notes: Attempts their $\int(px+q)x^{\frac{1}{2}}\,\mathrm{d}x$ by expanding and integrating or may attempt "
       r"parts again. E.g. $\int(2x-6)x^{\frac{1}{2}}\,\mathrm{d}x=\int\left(2x^{\frac{3}{2}}-6x^{\frac{1}{2}}\right)"
       r"\mathrm{d}x=\ldots$ or e.g. $\int(2x-6)x^{\frac{1}{2}}\,\mathrm{d}x=\frac{2}{3}x^{\frac{3}{2}}(2x-6)-\frac{4}{3}"
       r"\int x^{\frac{3}{2}}\,\mathrm{d}x$ If they expand then at least one term requires $x^n\to x^{n+1}$ or if parts "
       r"is attempted again, the structure must be correct.",
       r"ALT: Integration by parts — A1 (AO 1.1b): $=\frac{1}{2}(x-2)(x-4)x^{\frac{1}{2}}-\frac{2}{5}x^{\frac{5}{2}}+2x^{"
       r"\frac{3}{2}}$ Or e.g. $=\frac{1}{2}(x-2)(x-4)x^{\frac{1}{2}}-\frac{1}{3}x^{\frac{3}{2}}(2x-6)+\frac{4}{15}x^{"
       r"\frac{5}{2}}$. Notes: Fully correct integration in any form",
       r"ALT: Integration by parts — " + Q8M1L + r"$\frac{1}{2}(x-2)(x-4)x^{\frac{1}{2}}-\frac{1}{3}x^{\frac{3}{2}}(2x-6)"
       r"+\frac{4}{15}x^{\frac{5}{2}}$. Notes: Substitutes the limits 4 and 2 to their $=\frac{1}{2}(x-2)(x-4)x^{\frac{1}"
       r"{2}}-\frac{2}{5}x^{\frac{5}{2}}+2x^{\frac{3}{2}}$ and subtracts either way round. There is no requirement to "
       r"evaluate but 4 and 2 must be substituted either way round with evidence of subtraction, condoning omission of "
       r"brackets. E.g. condone $0-\frac{16}{3}+\frac{128}{15}-0+\frac{4}{3}\sqrt{2}+\frac{16}{15}\sqrt{2}$ This is an "
       r"independent mark but the limits must be applied to a “changed” function.",
       r"ALT: Integration by parts — A1 (AO 2.1): $0-\frac{16}{3}+\frac{128}{15}-\left(0+\frac{4}{3}\sqrt{2}+\frac{16}"
       r"{15}\sqrt{2}\right)$ Area $R=\frac{12}{5}\sqrt{2}-\frac{16}{5}$ $\left(\text{or }\frac{16}{5}-\frac{12}{5}"
       r"\sqrt{2}\right)$. Notes: Correct working shown leading to $\frac{12}{5}\sqrt{2}-\frac{16}{5}$ but also allow "
       r"$\frac{16}{5}-\frac{12}{5}\sqrt{2}$ or exact equivalents $\textbf{Attempts at integration by parts “the other "
       r"way round” should be sent to review.}$",
       r"ALT: Integration by substitution example — M1 (AO 1.1b): $u=\sqrt{x}\ (x=u^2)\Rightarrow\int\frac{(x-2)(x-4)}"
       r"{4\sqrt{x}}\,\mathrm{d}x=\int\frac{(u^2-2)(u^2-4)}{4u}\frac{\mathrm{d}x}{\mathrm{d}u}\,\mathrm{d}u=\int\frac{"
       r"(u^2-2)(u^2-4)}{4u}2u\,\mathrm{d}u$. Notes: Applies the substitution e.g. $u=\sqrt{x}$ and attempts $k\int"
       r"\frac{(u^2-2)(u^2-4)}{u}\frac{\mathrm{d}x}{\mathrm{d}u}\,\mathrm{d}u$",
       r"ALT: Integration by substitution example — A1 (AO 1.1b): Fully correct integral in terms of $u$ in any form "
       r"e.g. $\frac{1}{2}\int(u^2-2)(u^2-4)\,\mathrm{d}u$",
       r"ALT: Integration by substitution example — dM1 (AO 3.1a): $=\frac{1}{2}\int(u^4-6u^2+8)\,\mathrm{d}u=\frac{1}"
       r"{2}\left(\frac{u^5}{5}-\frac{6u^3}{3}+8u\right)(+c)$. Notes: Expands the bracket and integrates $u^n\to "
       r"u^{n+1}$ for at least 2 correct indices i.e. at least 2 of $u^4\to u^5$, $u^2\to u^3$, $k\to ku$",
       r"ALT: Integration by substitution example — A1 (AO 1.1b): $\frac{1}{2}\left(\frac{u^5}{5}-\frac{6u^3}{3}+8u"
       r"\right)(+c)$. Allow unsimplified.",
       r"ALT: Integration by substitution example — M1 (AO 2.2a): Deduces limits of integral are $\sqrt{2}$ and 2 and "
       r"applies to their $\frac{1}{2}\left(\frac{u^5}{5}-\frac{6u^3}{3}+8u\right)$. Notes: Substitutes the limits 2 "
       r"and $\sqrt{2}$ to their $\frac{1}{2}\left(\frac{u^5}{5}-\frac{6u^3}{3}+8u\right)$ and subtracts either way "
       r"round. There is no requirement to evaluate but 2 and $\sqrt{2}$ must be substituted either way round with "
       r"evidence of subtraction, condoning omission of brackets. E.g. condone $\frac{1}{2}\left(\frac{32}{5}-16+16-"
       r"\frac{4\sqrt{2}}{5}-4\sqrt{2}+8\sqrt{2}\right)$ Alternatively reverses the substitution and applies the limits "
       r"4 and 2 with the same conditions.",
       r"ALT: Integration by substitution example — A1 (AO 2.1): $\frac{1}{2}\left(\frac{32}{5}-16+16-\left(\frac{4"
       r"\sqrt{2}}{5}-4\sqrt{2}+8\sqrt{2}\right)\right)$ Area $R=\frac{12}{5}\sqrt{2}-\frac{16}{5}$ $\left(\text{or }"
       r"\frac{16}{5}-\frac{12}{5}\sqrt{2}\right)$. Notes: Correct working shown leading to $\frac{12}{5}\sqrt{2}-\frac{"
       r"16}{5}$ but also allow $\frac{16}{5}-\frac{12}{5}\sqrt{2}$ or exact equivalents Award this mark once one of "
       r"these forms is reached and isw. $\textbf{There may be other substitutions seen and the same marking principles "
       r"apply.}$"],
      True, 18),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", TRIG, "5.9, 5.3, 2.7", 4, LATEX["09a"],
      [r"B1 (AO 3.4): Deduces that $A=\pm50$ $\textbf{or}$ $b=\frac{1}{4}$. Notes: (a) Note that B0B1 is not possible "
       r"Uses the equation of the given model to deduce that $A=\pm50$ $\textbf{or}$ $b=\frac{1}{4}$ o.e. May be seen "
       r"embedded within their equation.",
       r"B1 (AO 3.4): Deduces that $A=\pm50$ $\textbf{and}$ $b=\frac{1}{4}$. Notes: Uses the equation of the given model "
       r"to deduce that $A=\pm50$ $\textbf{and}$ $b=\frac{1}{4}$ o.e. May be seen embedded within their equation.",
       r"M1 (AO 3.4): Uses $t=0,H=1\Rightarrow\alpha=\ldots$ E.g. $1=\text{“}50\text{”}\sin(\alpha)^\circ\Rightarrow"
       r"\alpha=\ldots$. Notes: Uses $t=0$ and $H=1$ in the equation of the model to find a value for $\alpha$. Follow "
       r"through on their value for $A$. Allow for $\pm1=\text{“}50\text{”}\sin(\alpha)^\circ\Rightarrow\alpha=\ldots$ "
       r"where $\alpha$ is in degrees or radians. Note that in radians $\sin^{-1}\left(\frac{1}{50}\right)\approx\frac{1}"
       r"{50}$ $(0.0200\ldots)$ which may appear incorrect but is in fact ok. Also in degrees a value of e.g. 1.14 "
       r"(truncated) would indicate the method.",
       r"A1 (AO 3.3): $H=\left|\pm50\sin\left(\frac{1}{4}t+1.15\right)^\circ\right|$. Notes: Writes down the correct "
       r"full equation of the model: $H=\left|\text{“}\pm\text{”}50\sin\left(\frac{1}{4}t+1.15\right)^\circ\right|$ o.e. "
       r"Condone omission of degrees symbol and allow awrt 1.15 for $\alpha$. Allow if a correct equation is seen "
       r"anywhere in their solution."],
      True, 22),
    e("09b", "9(b)", TRIG, "5.9, 2.11", 1, LATEX["09b"],
      [r"B1 (AO 3.5b): E.g. the minimum height above the ground of the passenger on the original model was 0 m or "
       r"Adding “$d$” means the passenger does not touch the ground. Notes: Gives a suitable explanation with no "
       r"contradictory statements. Condone “so that pod/capsule/seat/passenger/ferris wheel/it etc. will not hit/touch "
       r"the ground” Responses that focus on the starting point of the model are likely to score B0"],
      True, 22),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", ALG, "2.8", 2, LATEX["10a"],
      [r"M1 (AO 3.1a): Attempts to solve $\frac{3}{2}=\frac{8x+5}{2x+3}\Rightarrow x=\ldots$ Or substitutes "
       r"$x=\frac{3}{2}$ into $\frac{5-3x}{2x-8}$. Notes: Attempts to solve $\frac{3}{2}=\frac{8x+5}{2x+3}\Rightarrow x="
       r"\ldots$ You can condone poor algebra as long as they reach a value for $x$. Alternatively attempt to substitute "
       r"$x=\frac{3}{2}$ into $\mathrm{f}^{-1}(x)=\frac{\pm5\pm3x}{\pm2x\pm8}$ or equivalent (may be in terms of $y$). "
       r"Note that attempts to find e.g. $\mathrm{f}'(x)$ or $\frac{1}{\mathrm{f}(x)}$ which may be implied by values "
       r"such as $\frac{6}{17},\frac{17}{6},\frac{7}{18},\frac{18}{7}$ score M0",
       r"A1 (AO 1.1b): $\left(\mathrm{f}^{-1}\left(\frac{3}{2}\right)=\right)-\frac{1}{10}$. Notes: Achieves $\left("
       r"\mathrm{f}^{-1}\left(\frac{3}{2}\right)=\right)-\frac{1}{10}$. Do not be concerned what they call it, just look "
       r"for the value e.g. $x=-\frac{1}{10}$ or just $-\frac{1}{10}$ is fine. Correct answer with no (or minimal) "
       r"working scores both marks."],
      False, 24),
    e("10b", "10(b)", ALG, "2.6", 2, LATEX["10b"],
      [r"M1 (AO 1.1b): $\left(\frac{8x+5}{2x+3}=\right)4\pm\frac{\ldots}{2x+3}$. Notes: Attempts to divide $8x+5$ by "
       r"$2x+3$ Look for $4\pm\frac{\ldots}{2x+3}$ where … is a constant or $8x+5=A(2x+3)+B$ with $A$ or $B$ correct "
       r"(which may be in a fraction) or in a long division attempt and obtains a quotient of 4 or attempts to express "
       r"the numerator in terms of the denominator e.g. $\frac{8x+5}{2x+3}=\frac{4(2x+3)+\ldots}{2x+3}$",
       r"A1 (AO 2.1): $\left(\frac{8x+5}{2x+3}=\right)4-\frac{7}{2x+3}$. Notes: A full and complete method showing "
       r"$\frac{8x+5}{2x+3}=4-\frac{7}{2x+3}$ or $\frac{8x+5}{2x+3}=4+\frac{-7}{2x+3}$ Also allow for correct values e.g. "
       r"$A=4$, $B=-7$ Do not isw here e.g. if they obtain $A=4$, $B=-7$ and then write $-7+\frac{4}{2x+3}$ score A0"],
      False, 24),
    e("10c", "10(c)", ALG, "2.8", 1, LATEX["10c"],
      [r"B1 (AO 2.2a): $0\leqslant\mathrm{g}^{-1}(x)\leqslant4$. Notes: Deduces $0\leqslant\mathrm{g}^{-1}(x)\leqslant4$ "
       r"o.e. E.g. $0\leqslant y\leqslant4$, $0\leqslant\text{range}\leqslant4$, $\mathrm{g}^{-1}(x)\leqslant4$ and "
       r"$\mathrm{g}^{-1}(x)\geqslant0$, $0\leqslant\mathrm{g}^{-1}\leqslant4$, $[0, 4]$ but not e.g. $0\leqslant x"
       r"\leqslant4$, $0\leqslant\mathrm{g}(x)\leqslant4$, $(0, 4)$"],
      False, 24),
    e("10d", "10(d)", ALG, "2.8", 3, LATEX["10d"],
      [r"M1 (AO 3.1a): Attempts either boundary $\mathrm{f}(0)=\frac{8\times0+5}{2\times0+3}$ or $\mathrm{f}(4)="
       r"\frac{8\times4+5}{2\times4+3}$. Notes: Attempts either boundary. Look for either $\mathrm{f}(0)=\frac{8\times0"
       r"+5}{2\times0+3}$ $\textbf{or}$ $\mathrm{f}(4)=\frac{8\times4+5}{2\times4+3}$ or uses (b) e.g. $\mathrm{f}(0)="
       r"4-\frac{7}{2\times0+3}$ $\textbf{or}$ $\mathrm{f}(4)=4-\frac{7}{2\times4+3}$",
       r"dM1 (AO 1.1b): Attempts both boundaries $\mathrm{f}(0)=\frac{8\times0+5}{2\times0+3}$ and $\mathrm{f}(4)="
       r"\frac{8\times4+5}{2\times4+3}$. Notes: Attempts both boundaries. Look for $\mathrm{f}(0)=\frac{8\times0+5}"
       r"{2\times0+3}$ $\textbf{and}$ $\mathrm{f}(4)=\frac{8\times4+5}{2\times4+3}$ or uses (b) e.g. $\mathrm{f}(0)="
       r"4-\frac{7}{2\times0+3}$ $\textbf{and}$ $\mathrm{f}(4)=4-\frac{7}{2\times4+3}$",
       Q10DA1,
       r"ALT: Alternative by attempting $" + FG + r"(x)$ — M1 (AO 3.1a): $\mathrm{g}^{-1}(x)=\sqrt{16-x}\Rightarrow" + FG
       + r"(x)=\frac{8\sqrt{16-x}+5}{2\sqrt{16-x}+3}$ $" + FG + r"(0)=\frac{8\times4+5}{2\times4+3}$ or $" + FG
       + r"(16)=\frac{8\times0+5}{2\times0+3}$. Notes: Attempts $" + FG + r"(x)$ and either boundary using $x=0$ or "
       r"$x=16$ Look for either $" + FG + r"(0)=\frac{8\times\mathrm{g}^{-1}(0)+5}{2\times\mathrm{g}^{-1}(0)+3}$ "
       r"$\textbf{or}$ $" + FG + r"(16)=\frac{8\times\mathrm{g}^{-1}(16)+5}{2\times\mathrm{g}^{-1}(16)+3}$ Or uses (b) "
       r"e.g. $" + FG + r"(0)=4-\frac{7}{2\times\mathrm{g}^{-1}(0)+3}$ $\textbf{or}$ $" + FG + r"(16)=4-\frac{7}{2\times"
       r"\mathrm{g}^{-1}(16)+3}$ The attempt at $" + FG + r"(x)$ requires an attempt to substitute $\sqrt{16-x}$ "
       r"(condone $\pm\sqrt{16-x}$) into f",
       r"ALT: Alternative by attempting $" + FG + r"(x)$ — dM1 (AO 1.1b): $" + FG + r"(0)=\frac{8\times4+5}{2\times4+3}$ "
       r"and $" + FG + r"(16)=\frac{8\times0+5}{2\times0+3}$. Notes: Attempts both boundaries. Look for $" + FG
       + r"(0)=\frac{8\times\mathrm{g}^{-1}(0)+5}{2\times\mathrm{g}^{-1}(0)+3}$ $\textbf{and}$ $" + FG + r"(16)=\frac{8"
       r"\times\mathrm{g}^{-1}(16)+5}{2\times\mathrm{g}^{-1}(16)+3}$ Or uses (b) e.g. $" + FG + r"(0)=4-\frac{7}{2\times"
       r"\mathrm{g}^{-1}(0)+3}$ $\textbf{and}$ $" + FG + r"(16)=4-\frac{7}{2\times\mathrm{g}^{-1}(16)+3}$ The attempt "
       r"at $" + FG + r"(x)$ requires an attempt to substitute $\sqrt{16-x}$ (condone $\pm\sqrt{16-x}$) into f",
       r"ALT: Alternative by attempting $" + FG + r"(x)$ — " + Q10DA1.replace("in the correct form.", "in the correct "
       r"form with exact values.") + r" Note that the $\frac{37}{11}$ is sometimes obtained fortuitously from incorrect "
       r"working so check working carefully."],
      False, 24),

    # ---------------- Q11 ----------------
    e("11", "11", PROOF, "1.1", 4, LATEX["11"],
      [r"M1 (AO 3.1a): $n(n^2+5)$ Attempts even $\textbf{or}$ odd numbers Sets $n=2k$ $\textbf{or}$ $n=2k\pm1$ oe and "
       r"attempts $n(n^2+5)$. Notes: For the key step attempting to find $n(n^2+5)$ when $n=2k$ $\textbf{or}$ "
       r"$n=2k\pm1$ or equivalent representation of odd or even e.g. $n=2k+2$ $\textbf{or}$ $n=2k\pm7$ Condone the use "
       r"of e.g. $n=2n$ and $n=2n\pm1$",
       r"A1 (AO 2.2a): Achieves $2k(4k^2+5)$ (for $n=2k$) and states “even” $\textbf{Or}$ achieves $(2k+1)(4k^2+4k+6)="
       r"2(2k+1)(2k^2+2k+3)$ (for $n=2k+1$) and states “even” Or e.g. achieves $(2k-1)(4k^2-4k+6)=2(2k-1)(2k^2-2k+3)$ "
       r"(for $n=2k-1$) and states “even”. Notes: Achieves $2k(4k^2+5)$ or e.g. $2(4k^3+5k)$ and deduces that this is "
       r"even at the appropriate time. Or achieves $(2k\pm1)(4k^2\pm4k+6)=2(2k\pm1)(2k^2\pm2k+3)$ oe e.g. $2(4k^3+6k^2"
       r"+8k+3)$ and deduces that this is even. Note that if the bracket is expanded to e.g. $8k^3+12k^2+16k+6$ then "
       r"stating “even” is insufficient – they would need to say e.g. even + even + even + even = even or equivalent "
       r"Note it is also acceptable to use a divisibility argument e.g. $\frac{8k^3+10k}{2}=4k^3+5k$ so $8k^3+10k$ must "
       r"be even. There should be no errors in the algebra but allow e.g. invisible brackets if they are “recovered”.",
       r"dM1 (AO 2.1): Attempts even $\textbf{and}$ odd numbers Sets $n=2k$ $\textbf{and}$ $n=2k\pm1$ oe and attempts "
       r"$n(n^2+5)$. Notes: Attempts $n(n^2+5)$ when $n=2k$ $\textbf{and}$ $n=2k\pm1$ or equivalent representation of "
       r"odd or even e.g. $n=2k+2$ $\textbf{and}$ $n=2k\pm7$",
       r"A1 (AO 2.4): Achieves $2k(4k^2+5)$ (for $n=2k$) and states “even” $\textbf{and}$ achieves $(2k\pm1)(4k^2\pm4k+6)"
       r"=2(2k\pm1)(2k^2\pm2k+3)$ (for $n=2k\pm1$) and states “even” Correct work and states even for both WITH a final "
       r"conclusion showing that true for all $n\,(\in\mathbb{N})$ or e.g. true for all even and odd numbers. Notes: "
       r"Correct work and states even for both WITH a final conclusion e.g. so true for all $n\,(\in\mathbb{N})$. There "
       r"should be no errors in the algebra but allow e.g. invisible brackets if they are “recovered”. "
       r"$\textbf{Attempts at proof by induction should be sent to review}$",
       r"ALT: A “solution” via just logic — SC 1010: E.g. If $n$ is odd, then $n(n^2+5)$ is odd×(odd + odd) = odd × "
       r"even = even If $n$ is even, then $n(n^2+5)$ is even×(even + odd) = even × odd = even Both cases must be "
       r"considered to score any marks and scores SC 1010 if fully correct $\textbf{OR}$ E.g. $n(n^2+5)=n^3+5n$ If $n$ "
       r"is odd, then $n^3$ is odd and $5n$ is odd, so $n^3+5n$ is odd + odd = even If $n$ is even, then $n^3$ is even "
       r"and $5n$ is even, so $n^3+5n$ is even + even = even Both cases must be considered to score any marks and scores "
       r"SC 1010 if fully correct",
       r"ALT: A solution via contradiction — M1 A1: There exists a number $n$ such that $n(n^2+5)$ is odd, and so "
       r"deduces that both $n$ and $n^2+5$ are odd. Note that M1A0 is not possible via this method.",
       r"ALT: A solution via contradiction — dM1: Sets $n^2+5=2k+1$ (for some integer $k$) $\Rightarrow n^2=2k-4="
       r"2(k-2)$ which is even Must use algebra here for this approach and not a “logic” argument.",
       r"ALT: A solution via contradiction — A1: States that “this is a contradiction as if $n^2$ is even, then $n$ is "
       r"even” and then concludes so “$n(n^2+5)$ is even for all $n$.”"],
      False, 28),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", DIFF, "7.4, 7.2", 3, LATEX["12a"],
      [r"M1 (AO 1.1b): $\mathrm{f}(x)=\frac{\mathrm{e}^{3x}}{4x^2+k}\Rightarrow\mathrm{f}'(x)=\frac{(4x^2+k)3\mathrm{e}^{"
       r"3x}-8x\mathrm{e}^{3x}}{(4x^2+k)^2}$ or $\mathrm{f}(x)=\mathrm{e}^{3x}(4x^2+k)^{-1}\Rightarrow\mathrm{f}'(x)="
       r"3\mathrm{e}^{3x}(4x^2+k)^{-1}-8x\mathrm{e}^{3x}(4x^2+k)^{-2}$. Notes: Attempts the quotient rule to obtain an "
       r"expression of the form $\frac{\alpha(4x^2+k)\mathrm{e}^{3x}-\beta x\mathrm{e}^{3x}}{(4x^2+k)^2}$, "
       r"$\alpha,\beta>0$ condoning bracketing errors/omissions as long as the intention is clear. If the quotient rule "
       r"formula is quoted it must be correct. Condone e.g. $\mathrm{f}'(x)=\frac{(4x^2+k)3\mathrm{e}^{3x}-8x\mathrm{e}^{"
       r"3x}}{(4x^2+k)}$ provided an incorrect formula is not quoted. May also see product rule applied to "
       r"$\mathrm{e}^{3x}(4x^2+k)^{-1}$ to obtain an expression of the form $\alpha\mathrm{e}^{3x}(4x^2+k)^{-1}+\beta x"
       r"\mathrm{e}^{3x}(4x^2+k)^{-2}$ $\alpha,\beta0<0$ condoning bracketing errors/omissions as long as the intention "
       r"is clear. If the product rule formula is quoted it must be correct.",
       r"A1 (AO 1.1b): (as above). Notes: Correct differentiation in any form with correct bracketing which may be "
       r"implied by subsequent work.",
       r"A1 (AO 2.1): $\mathrm{f}'(x)=\frac{(12x^2-8x+3k)\mathrm{e}^{3x}}{(4x^2+k)^2}$. Notes: Obtains $\mathrm{f}'(x)="
       r"(12x^2-8x+3k)\mathrm{g}(x)$ where $\mathrm{g}(x)=\frac{\mathrm{e}^{3x}}{(4x^2+k)^2}$ $\textbf{or equivalent}$ "
       r"e.g. $\mathrm{g}(x)=\mathrm{e}^{3x}(4x^2+k)^{-2}$ Allow recovery from “invisible” brackets earlier and apply "
       r"isw here once a correct answer is seen. Note that the complete form of the answer is not given so allow "
       r"candidates to go from e.g. $\frac{(4x^2+k)3\mathrm{e}^{3x}-8x\mathrm{e}^{3x}}{(4x^2+k)^2}$ or $3\mathrm{e}^{3x}"
       r"(4x^2+k)^{-1}-8x\mathrm{e}^{3x}(4x^2+k)^{-2}$ to $\frac{(12x^2-8x+3k)\mathrm{e}^{3x}}{(4x^2+k)^2}$ for the final "
       r"mark. The “$\mathrm{f}'(x)=$” must appear at some point but allow e.g. “$" + DYDX + r"=$”"],
      False, 30),
    e("12b", "12(b)", DIFF, "7.3, 2.3, 2.5", 3, LATEX["12b"],
      [r"B1 (AO 2.2a): If $y=\mathrm{f}(x)$ has at least one stationary point then $12x^2-8x+3k=0$ has at least one "
       r"root. Notes: (b) Note that B0M1A1 is not possible in (b) Deduces that if $y=\mathrm{f}(x)$ has at least one "
       r"stationary point then $12x^2-8x+3k=0$ has at least one root. There is no requirement to formally state "
       r"$\frac{\mathrm{e}^{3x}}{(4x^2+k)^2}>0$ This may be implied by an attempt at $b^2-4ac\geqslant0$ or "
       r"$b^2-4ac>0$ condoning slips.",
       r"M1 (AO 2.1): Applies $b^2-4ac\,(\geqslant)\,0$ with $a=12, b=-8, c=3k$. Notes: Attempts $b^2-4ac\ldots0$ with "
       r"$a=12$, $b=-8$, $c=3k$ where … is e.g. “=”, <, >, etc. Alternatively attempts to complete the square and sets "
       r"rhs …0 E.g. $12x^2-8x+3k=0\Rightarrow x^2-\frac{2}{3}x+\frac{1}{4}k=0\Rightarrow\left(x-\frac{1}{3}\right)^2="
       r"\frac{1}{9}-\frac{1}{4}k$ leading to $\frac{1}{9}-\frac{1}{4}k\geqslant0$",
       r"A1 (AO 1.1b): $0<k\leqslant\frac{4}{9}$. Notes: $0<k\leqslant\frac{4}{9}$ but condone $k\leqslant\frac{4}{9}$ "
       r"and condone $0\leqslant k\leqslant\frac{4}{9}$ Must be in terms of $k$ not $x$ so do not allow e.g. $0<x"
       r"\leqslant\frac{4}{9}$ but condone $\left(0,\frac{4}{9}\right]$ or $\left[0,\frac{4}{9}\right]$"],
      False, 30),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", VEC, "10.4, 10.3", 3, LATEX["13a"],
      [r"M1 (AO 3.1a): Attempts two of the relevant vectors $\pm" + V("AB") + r"=\pm(-4" + i_ + "+7" + j_ + "+" + k_
       + r")$ $\pm" + V("AC") + r"=\pm(-20" + i_ + "+(p+3)" + j_ + "+5" + k_ + r")$ $\pm" + V("BC") + r"=\pm(-16" + i_
       + "+(p-4)" + j_ + "+4" + k_ + r")$. Notes: Attempts two of the three relevant vectors by $\textbf{subtracting}$ "
       r"either way around. See scheme. Allow equivalent work e.g. $\pm" + V("AB") + r"=\pm(" + V("OB") + "+" + V("AO")
       + r")$ If no working is shown, method can be implied by 2 correct components.",
       r"dM1 (AO 2.1): Uses two of the three vectors in such a way as to find the value of $p$. E.g. $p+3=5\times7$. "
       r"Notes: For the key step in using the fact that if the vectors are parallel, they will be multiples of each "
       r"other (where the multiple is something other than 1) to find $p$. E.g. $p+3=5\times7$, $p-4=\frac{4}{5}(p+3)$, "
       r"$p-4=4\times7$",
       r"A1 (AO 1.1b): $p=32$. Notes: $p=32$ (Condone 32$" + j_ + r"$) $\textbf{For reference,}$ $" + V("BC") + "=4"
       + V("AB") + ", " + V("AC") + "=5" + V("AB") + ", " + V("BC") + r"=\frac{4}{5}" + V("AC") + ", " + V("AC")
       + r"=\frac{5}{4}" + V("BC") + r"$ $\textbf{Note that candidates generally only need to use 2 components to find}$ "
       r"$p$ $\textbf{and if the 3}^{\textbf{rd}}$ $\textbf{component has errors but is not used, full marks can be "
       r"awarded.}$ $\textbf{There will be other approaches e.g. using “gradients” and “ratios” and the method marks "
       r"can be implied – if you are unsure if such attempts deserve credit use Review}$",
       r"ALT: (a) Alternative — M1 (AO 3.1a): $r_{AB}=4" + i_ + "-3" + j_ + "+5" + k_ + r"+\lambda(-4" + i_ + "+7" + j_
       + "+" + k_ + r")$. Notes: Forms the vector equation using $A$ or $B$ as position and $\pm" + V("AB") + "$ as the "
       r"direction",
       r"ALT: (a) Alternative — dM1 (AO 2.1): $4" + i_ + "-3" + j_ + "+5" + k_ + r"+\lambda(-4" + i_ + "+7" + j_ + "+"
       + k_ + ")=-16" + i_ + "+p" + j_ + "+10" + k_ + r"\Rightarrow\lambda=5$ $4" + i_ + "-3" + j_ + "+5" + k_
       + r"+\lambda(-4" + i_ + "+7" + j_ + "+" + k_ + ")=-16" + i_ + "+p" + j_ + "+10" + k_ + r"\Rightarrow p=35-3$. "
       r"Notes: For the key step in using the fact that $C$ lies on the line to find $p$",
       r"ALT: (a) Alternative — A1 (AO 1.1b): $p=32$. Notes: $p=32$ (Condone 32$" + j_ + "$)"],
      False, 32),
    e("13b", "13(b)", VEC, "10.5, 10.2, 10.4", 3, LATEX["13b"],
      [r"M1 (AO 3.1a): Deduces that $" + V("OD") + r"=\lambda" + V("OB") + r"=4\lambda" + j_ + r"+6\lambda" + k_
       + r"$ and attempts $" + V("CD") + "=16" + i_ + r"+(4\lambda-\text{“}32\text{”})" + j_ + r"+(6\lambda-10)" + k_
       + r"$. Notes: (b) Vector approach Deduces that $" + V("OD") + r"=\lambda" + V("OB") + r"=4\lambda" + j_
       + r"+6\lambda" + k_ + r"$ and attempts $" + V("CD") + "=16" + i_ + r"+(4\lambda-\text{“}32\text{”})" + j_
       + r"+(6\lambda-10)" + k_ + "$",
       r"dM1 (AO 1.1b): Correct attempt at $\lambda$ using the fact that $" + V("CD") + "$ is parallel to $" + V("OA")
       + "$ $" + V("CD") + "=16" + i_ + r"+(4\lambda-\text{“}32\text{”})" + j_ + r"+(6\lambda-10)" + k_ + "$ $" + V("OA")
       + "=4" + i_ + "-3" + j_ + "+5" + k_ + r"$ $4\lambda-32=-12\Rightarrow\lambda=\ldots$ OR $6\lambda-10=20"
       r"\Rightarrow\lambda=\ldots$. Notes: Correct attempt at finding $\lambda$ using the fact that $" + V("CD")
       + "$ is parallel to $" + V("OA") + "$ E.g. $16" + i_ + r"+(4\lambda-\text{“}32\text{”})" + j_ + r"+(6\lambda-10)"
       + k_ + r"=4\alpha" + i_ + r"-3\alpha" + j_ + r"+5\alpha" + k_ + r"\Rightarrow\alpha=4\Rightarrow4\lambda-\text{“}"
       r"32\text{”}=-3\times\text{“}4\text{”}\Rightarrow\lambda=\ldots$",
       r"A1 (AO 1.1b): " + OD13 + r". Notes: $\left|" + V("OD") + r"\right|=10\sqrt{13}$",
       r"ALT: (b) Alternative — M1 (AO 3.1a): Deduces that $" + V("OD") + r"=\lambda" + V("OB") + r"=4\lambda" + j_
       + r"+6\lambda" + k_ + r"$ and attempts $" + V("OD") + "=" + V("OC") + r"+\mu" + V("OA") + "=-16" + i_ + "+32"
       + j_ + "+10" + k_ + r"+\mu(4" + i_ + "-3" + j_ + "+5" + k_ + ")$",
       r"ALT: (b) Alternative — dM1 (AO 1.1b): Correct attempt at $\lambda$ $\textbf{or}$ $\mu$ using the fact that "
       r"$\lambda" + V("OB") + "=" + V("OC") + r"+\mu" + V("OA") + r"$ E.g. $-16+4\mu=0\Rightarrow\mu=4$. Notes: E.g. "
       r"$(-16+4\mu)" + i_ + r"+(\text{“}32\text{”}-3\mu)" + j_ + r"+(10+5\mu)" + k_ + r"=4\lambda" + j_ + r"+6\lambda"
       + k_ + r"\Rightarrow-16+4\mu=0\Rightarrow\mu=\ldots$ May also solve simultaneously using $y$ and $z$ components "
       r"to find $\lambda$ or $\mu$",
       r"ALT: (b) Alternative — A1 (AO 1.1b): " + OD13 + r". Notes: $\left|" + V("OD") + r"\right|=10\sqrt{13}$ Note "
       r"that the correct vector is $20" + j_ + "+30" + k_ + "$",
       r"ALT: (b) Similar triangle approach — M1: For the key step in recognising that triangle $BCD$ and triangle "
       r"$BAO$ are similar with a ratio of lengths of 4:1",
       r"ALT: (b) Similar triangle approach — dM1: States or uses the fact that $\left|" + V("OD") + r"\right|=5\times"
       r"\left|" + V("OB") + r"\right|$ Stating this will score M1 dM1 provided there is no evidence of incorrect work "
       r"$\textbf{Note that they may establish this result using the work from (a) but must be used here to score.}$",
       r"ALT: (b) Similar triangle approach — A1: $\left|" + V("OD") + r"\right|=10\sqrt{13}$"],
      False, 32),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", ALG, "2.10", 3, LATEX["14a"],
      [r"M1 (AO 1.1b): $\frac{3}{(2x-1)(x+1)}=\frac{A}{2x-1}+\frac{B}{x+1}\Rightarrow A=\ldots, B=\ldots$. Notes: Correct "
       r"method of partial fractions leading to values for their $A$ and $B$ E.g. substitution: $\frac{3}{(2x-1)(x+1)}="
       r"\frac{A}{2x-1}+\frac{B}{x+1}\Rightarrow3=A(x+1)+B(2x-1)\Rightarrow A=\ldots,B=\ldots$ Or compare coefficients "
       r"$\frac{3}{(2x-1)(x+1)}=\frac{A}{2x-1}+\frac{B}{x+1}\Rightarrow3=x(A+2B)+A-B\Rightarrow A=\ldots,B=\ldots$ Note "
       r"that $\frac{3}{(2x-1)(x+1)}=\frac{A}{2x-1}+\frac{B}{x+1}\Rightarrow3=A(2x-1)+B(x+1)\Rightarrow A=\ldots,B="
       r"\ldots$ scores M0",
       r"A1 (AO 1.1b): Either $A=2$ or $B=-1$. Notes: Correct value for “$A$” or “$B$”",
       r"A1 (AO 1.1b): $\frac{3}{(2x-1)(x+1)}=\frac{2}{2x-1}-\frac{1}{x+1}$. Notes: Correct partial fractions not just "
       r"values for “$A$” and “$B$”. $\frac{2}{2x-1}-\frac{1}{x+1}$ or e.g. $\frac{2}{2x-1}+\frac{-1}{x+1}$ Must be seen "
       r"as $\textbf{fractions}$ but if not stated here, allow if the correct fractions appear later."],
      False, 36),
    e("14b", "14(b)", INT, "8.7, 8.6, 7.6", 5, LATEX["14b"],
      [Q14B1,
       r"M1 (AO 3.1a): $\int\frac{2}{2t-1}-\frac{1}{t+1}\,\mathrm{d}t=\ldots\ln(2t-1)-\ldots\ln(t+1)(+c)$. " + Q14M1,
       r"A1ft (AO 1.1b): $\ln V=\ln(2t-1)-\ln(t+1)(+c)$. " + Q14A1F,
       r"M1 (AO 3.4): Substitutes $t=2,V=3\Rightarrow c=(\ln3)$. " + Q14M2,
       r"A1* (AO 2.1): $\ln V=\ln(2t-1)-\ln(t+1)+\ln3$ $V=\frac{3(2t-1)}{(t+1)}$*. " + Q14A1S + r" $\textbf{Note that "
       r"B0M1A1M1A1 is not possible in (b) as the B1 must be implied if all the other marks have been awarded.}$ Note "
       r"also that some candidates may use different variables in (b) e.g. $" + DYDX + r"=\frac{3y}{(2x-1)(x+1)}"
       r"\Rightarrow\int\frac{1}{y}\,\mathrm{d}y=\int\frac{3}{(2x-1)(x+1)}\,\mathrm{d}x$ etc. In such cases you should "
       r"award marks for equivalent work but they must revert to the given variables at the end to score the final "
       r"mark. Also if e.g. a “$t$” becomes an “$x$” within their working but is recovered allow full marks.",
       r"ALT: (b) Alternative separation of variables — B1 (AO 1.1a): $\int\frac{1}{3V}\,\mathrm{d}V=\int\frac{1}{(2t-1)"
       r"(t+1)}\,\mathrm{d}t$. Notes: Separates variables $\int\frac{1}{3V}\,\mathrm{d}V=\int\frac{1}{(2t-1)(t+1)}\,"
       r"\mathrm{d}t$. May be implied by later work. Condone omission of the integral signs but the $\mathrm{d}V$ and "
       r"$\mathrm{d}t$ must be in the correct positions if awarding this mark in isolation but they may be implied by "
       r"subsequent work.",
       r"ALT: (b) Alternative separation of variables — M1 (AO 3.1a): $\frac{1}{3}\int\frac{2}{2t-1}-\frac{1}{t+1}\,"
       r"\mathrm{d}t=\ldots\ln(2t-1)-\ldots\ln(t+1)(+c)$. " + Q14M1,
       r"ALT: (b) Alternative separation of variables — A1ft (AO 1.1b): $\frac{1}{3}\ln3V=\frac{1}{3}\ln(2t-1)-\frac{1}"
       r"{3}\ln(t+1)(+c)$. " + Q14A1F,
       r"ALT: (b) Alternative separation of variables — M1 (AO 3.4): Substitutes $t=2,V=3\Rightarrow c=\left(\frac{1}{3}"
       r"\ln3\right)$. " + Q14M2,
       r"ALT: (b) Alternative separation of variables — A1* (AO 2.1): $\frac{1}{3}\ln V=\frac{1}{3}\ln(2t-1)-\frac{1}{3}"
       r"\ln(t+1)+\frac{1}{3}\ln3$ $V=\frac{3(2t-1)}{(t+1)}$*. " + Q14A1S + r" (Note the working may look like this: "
       r"$\frac{1}{3}\ln3V=\frac{1}{3}\ln(2t-1)-\frac{1}{3}\ln(t+1)+c$, $\frac{1}{3}\ln9=\frac{1}{3}\ln(3)-\frac{1}{3}"
       r"\ln3+c$, $c=\frac{1}{3}\ln9$ $\ln3V=\ln\frac{9(2t-1)}{(t+1)}\Rightarrow3V=\frac{9(2t-1)}{(t+1)}\Rightarrow V="
       r"\frac{3(2t-1)}{(t+1)}$*)"],
      False, 36),
    e("14c", "14(c)", INT, "8.8", 2, LATEX["14c"],
      [r"B1 (AO 3.2a): (i) 30 (minutes). Notes: Deduces 30 minutes. Units not required so just look for 30 but allow "
       r"equivalents e.g. ½ an hour. If units are given they must be correct so do not allow e.g. 30 hours.",
       r"B1 (AO 3.4): (ii) 6 (m$^3$). Notes: Deduces 6 m$^3$. Units not required so just look for 6. Condone $V<6$ or "
       r"$V\leqslant6$ If units are given they must be correct so do not allow e.g. 6 m."],
      False, 36),

    # ---------------- Q15 ----------------
    e("15a", "15(a)", SEQ, "4.5, 5.5", 3, LATEX["15a"],
      [r"M1 (AO 3.1a): Uses the common ratio $\frac{5+2\sin\theta}{12\cos\theta}=\frac{6\tan\theta}{5+2\sin\theta}$ o.e.. "
       r"Notes: For the key step in using the ratio of $\frac{a_2}{a_1}=\frac{a_3}{a_2}$",
       r"dM1 (AO 1.1b): Cross multiplies and uses $\tan\theta\times\cos\theta=\sin\theta$ $(5+2\sin\theta)^2=6\times12"
       r"\sin\theta$. Notes: Cross multiplies and uses $\tan\theta\times\cos\theta=\sin\theta$",
       Q15A1,
       r"ALT: (a) Alternative example — M1 (AO 3.1a): Uses the common ratio $12r\cos\theta=5+2\sin\theta$, $12r^2\cos"
       r"\theta=6\tan\theta$ $\Rightarrow12\cos\theta\left(\frac{5+2\sin\theta}{12\cos\theta}\right)^2=6\tan\theta$. "
       r"Notes: Expresses the 2$^{\text{nd}}$ and 3$^{\text{rd}}$ terms in terms of the first term and the common ratio "
       r"and eliminates “r”",
       r"ALT: (a) Alternative example — dM1 (AO 1.1b): Multiplies up and uses $\tan\theta\times\cos\theta=\sin\theta$ "
       r"$(5+2\sin\theta)^2=6\tan\theta\times12\cos\theta=72\sin\theta$. Notes: Multiplies up and uses $\tan\theta"
       r"\times\cos\theta=\sin\theta$",
       r"ALT: (a) Alternative example — " + Q15A1 + r" Other approaches may be seen in (a) and can be marked in a "
       r"similar way e.g. M1 for correctly obtaining an equation in $\theta$ using the GP, M1 for applying $\tan\theta"
       r"\times\cos\theta=\sin\theta$ or equivalent and eliminating fractions, A1 as above Example: $u_2=\frac{u_1\times "
       r"u_3}{u_2}\Rightarrow5+2\sin\theta=\frac{12\cos\theta\times6\tan\theta}{5+2\sin\theta}$ M1 $\Rightarrow(5+2\sin"
       r"\theta)^2=72\sin\theta$ dM1 $25+20\sin\theta+4\sin^2\theta=72\sin\theta$ $\Rightarrow4\sin^2\theta-52\sin\theta"
       r"+25=0$ * A1"],
      False, 40),
    e("15b", "15(b)", TRIG, "5.7, 2.3", 2, LATEX["15b"],
      [r"M1 (AO 1.1b): $4\sin^2\theta-52\sin\theta+25=0\Rightarrow\sin\theta=\frac{1}{2}\left(,\frac{25}{2}\right)$. "
       r"Notes: Attempts to solve $4\sin^2\theta-52\sin\theta+25=0$. Must be clear they have found $\sin\theta$ and not "
       r"e.g. just $x$ from $4x^2-52x+25=0$. Working does not need to be seen but see general guidance for solving a 3TQ "
       r"if necessary. Note that the $\frac{25}{2}$ does not need to be seen.",
       r"A1 (AO 1.2): $\theta=\frac{5\pi}{6}$. Notes: $\theta=\frac{5\pi}{6}$ and no other values unless they are "
       r"rejected or the $\frac{5\pi}{6}$ clearly selected here and not in (c) A minimum requirement in (b) is e.g. "
       r"$\sin\theta=\frac{1}{2}$, $\theta=\frac{5\pi}{6}$ Do $\textbf{not}$ allow $150^\circ$ for $\frac{5\pi}{6}$"],
      False, 40),
    e("15c", "15(c)", SEQ, "4.5, 2.2, 5.3", 5, LATEX["15c"],
      [r"M1 (AO 3.1a): Attempts a value for either $a$ or $r$ e.g. $a=12\cos\theta=12\times-\frac{\sqrt{3}}{2}$ "
       r"$\textbf{or}$ $r=\frac{5+2\sin\theta}{12\cos\theta}=\frac{5+2\times\frac{1}{2}}{12\times-\frac{\sqrt{3}}{2}}$. "
       r"Notes: (c) Allow full marks in (c) if e.g. $\theta=\frac{\pi}{6}$ is their answer to (b) but $\theta=\frac{5"
       r"\pi}{6}$ is used here. or if e.g. $\theta=\frac{5\pi}{6}$ is their answer to (b) but $\theta=\frac{\pi}{6}$ is "
       r"used here allow the M marks only. For attempting a value (exact or decimal) for either $a$ or $r$ using "
       r"$\textbf{their}$ $\theta$ E.g. $a=12\cos\theta=\left(12\times-\frac{\sqrt{3}}{2}\right)$ or $r=\frac{5+2\sin"
       r"\theta}{12\cos\theta}=\left(\frac{5+2\times\frac{1}{2}}{12\times-\frac{\sqrt{3}}{2}}\right)$ oe e.g. $r="
       r"\frac{6\tan\theta}{5+2\sin\theta}=\left(\frac{6\times-\frac{1}{\sqrt{3}}}{5+2\times\frac{1}{2}}\right)$",
       r"A1 (AO 1.1b): $\text{“}a\text{”}=-6\sqrt{3}$ $\textbf{and}$ $\text{“}r\text{”}=-\frac{1}{\sqrt{3}}$ o.e.. "
       r"Notes: Finds both $a=-6\sqrt{3}$ and $r=-\frac{1}{\sqrt{3}}$ which can be left unsimplified but $\sin\theta="
       r"\frac{1}{2}$, $\cos\theta=-\frac{\sqrt{3}}{2}$ and $\tan\theta=-\frac{\sqrt{3}}{3}$ (if required) must have "
       r"been used.",
       r"dM1 (AO 2.1): Uses $S_\infty=\frac{a}{1-r}=\frac{-6\sqrt{3}}{1+\frac{1}{\sqrt{3}}}$. Notes: Uses both "
       r"$\textbf{values}$ of “$a$” and “$r$” with the equation $S_\infty=\frac{a}{1-r}=\frac{-6\sqrt{3}}{1+\frac{1}"
       r"{\sqrt{3}}}$ to create an expression involving surds where $a$ and $r$ have come from appropriate work and "
       r"$|r|<1$ Depends on the first method mark.",
       r"ddM1 (AO 1.1b): Rationalises denominator $S_\infty=\frac{-6\sqrt{3}}{1+\frac{1}{\sqrt{3}}}=\frac{-18}{\sqrt{3}"
       r"+1}\times\frac{\sqrt{3}-1}{\sqrt{3}-1}$. Notes: Rationalises denominator. The denominator must be of the form "
       r"$p\pm q\sqrt{3}$ oe e.g. $p+\frac{q}{\sqrt{3}}$ Depends on both previous method marks. Note that stating e.g. "
       r"$\frac{k}{p+q\sqrt{3}}\times\frac{p-q\sqrt{3}}{p-q\sqrt{3}}$ or $\frac{k}{p+\frac{q}{\sqrt{3}}}\times\frac{p-"
       r"\frac{q}{\sqrt{3}}}{p-\frac{q}{\sqrt{3}}}$ is sufficient.",
       r"A1 (AO 2.1): $(S_\infty=)\,9(1-\sqrt{3})$. Notes: Obtains $(S_\infty=)\,9(1-\sqrt{3})$ Note that full marks are "
       r"available in (c) for the use of $\theta=150^\circ$ Note also that marks may be implied in (c) by e.g. "
       r"$S_\infty=\frac{a}{1-r}=\frac{12\cos\theta}{1-\frac{5+2\sin\theta}{12\cos\theta}}=\frac{144\cos^2\theta}{12\cos"
       r"\theta-5-2\sin\theta}=\frac{144\cos^2\frac{5\pi}{6}}{12\cos\frac{5\pi}{6}-5-2\sin\frac{5\pi}{6}}$ $=\frac{108}"
       r"{-6-6\sqrt{3}}=\frac{108}{-6-6\sqrt{3}}\times\frac{-6+6\sqrt{3}}{-6+6\sqrt{3}}=\frac{-648+648\sqrt{3}}{-72}="
       r"9(1-\sqrt{3})$ Scores M1A1 implied dM1 ddM1 A1 $\textbf{Some other cases in (c) and how to mark them:}$ "
       r"$S_\infty=\frac{a}{1-r}=\frac{12\cos\frac{5\pi}{6}}{1-\frac{5+2\sin\frac{5\pi}{6}}{12\cos\frac{5\pi}{6}}}$ or "
       r"e.g. $S_\infty=\frac{a}{1-r}=\frac{12\cos\frac{\pi}{6}}{1-\frac{5+2\sin\frac{\pi}{6}}{12\cos\frac{\pi}{6}}}$ And "
       r"nothing else scores M1A0dM1ddM0A0; $S_\infty=\frac{a}{1-r}=\frac{12\cos\frac{5\pi}{6}}{1-\frac{5+2\sin\frac{5"
       r"\pi}{6}}{12\cos\frac{5\pi}{6}}}=9(1-\sqrt{3})$ Scores M1A1dM1ddM0A0; $S_\infty=\frac{a}{1-r}=\frac{12\cos\frac{"
       r"\pi}{6}}{1-\frac{5+2\sin\frac{\pi}{6}}{12\cos\frac{\pi}{6}}}=9(1+\sqrt{3})$ Scores M1A0dM1ddM0A0; $S_\infty="
       r"9(1-\sqrt{3})$ with no working scores no marks"],
      False, 40),

    # ---------------- Q16 ----------------
    e("16a", "16(a)", COORD, "3.3, 7.5, 3.1", 5, LATEX["16a"],
      [r"M1 (AO 1.1b): Attempts $" + DYDX + r"=\frac{\frac{\mathrm{d}y}{\mathrm{d}t}}{\frac{\mathrm{d}x}{\mathrm{d}t}}="
       r"\frac{4\sec^2t\tan t}{2\sec^2t}(=2\tan t)$. Notes: (a) $\underline{\textbf{Must use parametric differentiation "
       r"to score any marks in this part and not e.g. Cartesian form}}$ For the key step of attempting $" + DYDX
       + r"=\frac{\frac{\mathrm{d}y}{\mathrm{d}t}}{\frac{\mathrm{d}x}{\mathrm{d}t}}$. There must be some attempt to "
       r"differentiate both parameters however poor and divide the right way round so using $" + DYDX + r"=\frac{y}{x}$ "
       r"scores M0. This may be implied by e.g. $\frac{\mathrm{d}x}{\mathrm{d}t}=2\sec^2t$, $\frac{\mathrm{d}y}{\mathrm{d}"
       r"t}=4\sec^2t\tan t$, $t=\frac{\pi}{4}\Rightarrow\frac{\mathrm{d}x}{\mathrm{d}t}=4$, $\frac{\mathrm{d}y}{\mathrm{d}"
       r"t}=8\Rightarrow" + DYDX + "=2$",
       r"A1 (AO 1.1b): $" + DYDX + r"=\frac{4\sec^2t\tan t}{2\sec^2t}$. Notes: Correct expression in any form. May be "
       r"implied as above. Condone the confusion with variables as long as the intention is clear e.g. $" + DYDX
       + r"=\frac{\frac{\mathrm{d}y}{\mathrm{d}t}}{\frac{\mathrm{d}x}{\mathrm{d}t}}=\frac{4\sec^2x\tan x}{2\sec^2x}"
       r"(=2\tan x)$ and allow subsequent marks if this is interpreted correctly",
       r"M1 (AO 2.1): At $t=\frac{\pi}{4}$, $" + DYDX + r"=2, x=3, y=7$. Notes: For attempting to find the values of $x$, "
       r"$y$ and the gradient at $t=\frac{\pi}{4}$ $\textbf{AND}$ getting at least two correct. Follow through on their "
       r"$" + DYDX + r"$ so allow for any two of $x=3$, $y=7$, $" + DYDX + r"=2$ (or their $" + DYDX + r"$ at $t=\frac{"
       r"\pi}{4}$) Note that the $x=3$, $y=7$ may be seen as e.g. (3, 7) on the diagram. There must be a non-trivial "
       r"$" + DYDX + r"$ for this mark e.g. they must have a $" + DYDX + "$ to substitute into.",
       r"M1 (AO 1.1b): Attempts equation of normal $y-7=-\frac{1}{2}(x-3)$. Notes: For a correct attempt at the normal "
       r"equation using their $x$ and $y$ at $t=\frac{\pi}{4}$ with the negative reciprocal of their $" + DYDX
       + r"$ at $t=\frac{\pi}{4}$ having made some attempt at $" + DYDX + r"$ and all correctly placed. For attempts "
       r"using $y=mx+c$ they must reach as far as a value for $c$ using their $x$ and $y$ at $t=\frac{\pi}{4}$ with the "
       r"negative reciprocal of their $" + DYDX + r"$ at $t=\frac{\pi}{4}$ all correctly placed.",
       r"A1* (AO 2.1): $y=-\frac{1}{2}x+\frac{17}{2}$ *. Notes: Proceeds with a clear argument to the given answer with "
       r"no errors."],
      True, 44),
    e("16b", "16(b)", COORD, "3.3, 5.5", 2, LATEX["16b"],
      [r"M1 (AO 3.1a): Attempts to use $\sec^2t=1+\tan^2t\Rightarrow\frac{y-3}{2}=1+\left(\frac{x-1}{2}\right)^2$. "
       r"Notes: Attempts to use $\sec^2t=1+\tan^2t$ oe to obtain an equation involving $y$ and $(x-1)^2$ E.g. as above "
       r"or e.g. $y=2\sec^2t+3=2(1+\tan^2t)+3=2\left(1+\left(\frac{x-1}{2}\right)^2\right)+3$ for M1 and then $y="
       + Q16C + r"$* for A1",
       r"A1* (AO 2.1): $\Rightarrow y-3=2+\frac{(x-1)^2}{2}\Rightarrow y=" + Q16C + r"$ *. Notes: Proceeds with a clear "
       r"argument to the given answer with no errors $\textbf{Allow the marks for (b) to score anywhere in their "
       r"solution e.g. if they find the Cartesian equation in part (a)}$",
       r"ALT: (b) Alternative 1 — M1 (AO 3.1a): $y=" + Q16C + r"=\frac{1}{2}(2\tan t+1-1)^2+5=\frac{1}{2}4\tan^2t+5=2("
       r"\sec^2t-1)+5$. Notes: Uses the given result, substitutes for $x$ and attempts to use $\sec^2t=1+\tan^2t$ oe",
       r"ALT: (b) Alternative 1 — A1 (AO 2.1): $=2\sec^2t+3=y$*. Notes: Proceeds with a clear argument to the $y$ "
       r"parameter and makes a (minimal) conclusion e.g. “ = $y$” QED, hence proven etc.",
       r"ALT: (b) Alternative 2 — M1 (AO 3.1a): $x=2\tan t+1\Rightarrow t=\tan^{-1}\left(\frac{x-1}{2}\right)\Rightarrow "
       r"y=2\sec^2\left(\tan^{-1}\left(\frac{x-1}{2}\right)\right)+3$ $\Rightarrow y=2\left(1+\tan^2\left(\tan^{-1}\left("
       r"\frac{x-1}{2}\right)\right)\right)+3$. Notes: Uses the $x$ parameter to obtain $t$ in terms of arctan, "
       r"substitutes into $y$ and attempts to use $\sec^2t=1+\tan^2t$ oe",
       r"ALT: (b) Alternative 2 — A1 (AO 2.1): $\Rightarrow y=2\left(1+\left(\frac{x-1}{2}\right)^2\right)+3=" + Q16C
       + r"$*. Notes: Proceeds with a clear argument to the given answer with no errors",
       r"ALT: (b) Alternative 3 — M1 (AO 3.1a): $" + DYDX + r"=2\tan t=x-1\Rightarrow y=\int(x-1)\,\mathrm{d}x=\frac{x^2}"
       r"{2}-x+c$ $(3,7)\to7=\frac{3^2}{2}-3+c\Rightarrow c=\frac{11}{2}$. Notes: Uses $" + DYDX + r"$ from part (a) to "
       r"express $" + DYDX + r"$ in terms of $x$, integrates and uses (3, 7) to find “$c$” to reach a Cartesian "
       r"equation.",
       r"ALT: (b) Alternative 3 — A1 (AO 2.1): $\frac{x^2}{2}-x+\frac{11}{2}=\frac{1}{2}(x^2-2x)+\frac{11}{2}=\frac{1}{2}"
       r"(x-1)^2-\frac{1}{2}+\frac{11}{2}=" + Q16C + r"$*. Notes: Proceeds with a clear argument to the given answer "
       r"with no errors"],
      True, 44),
    e("16c", "16(c)", COORD, "3.3, 2.3, 2.5", 5, LATEX["16c"],
      [r"M1 (AO 2.1): Attempts the lower limit for $k$: $" + Q16C + r"=-\frac{1}{2}x+k\Rightarrow x^2-x+(11-2k)=0$ "
       r"$b^2-4ac=1-4(11-2k)=0\Rightarrow k=\ldots$. Notes: A full attempt to find the $\textbf{lower}$ limit for $k$. "
       r"Score $\textbf{M1}$ for setting $" + Q16C + r"=-\frac{1}{2}x+k$, rearranging to 3TQ form and attempts "
       r"$b^2-4ac\ldots0$ e.g. $b^2-4ac>0$ or e.g. $b^2-4ac<0$ correctly to find a value for $k$.",
       r"A1 (AO 1.1b): $(k=)\frac{43}{8}$. Notes: $k=\frac{43}{8}$ oe. Look for this $\textbf{value}$ e.g. may appear "
       r"in an inequality e.g. $k>\frac{43}{8}$, $k<\frac{43}{8}$",
       r"M1 (AO 2.1): Attempts the upper limit for $k$: $(x,y)_{t=-\frac{\pi}{4}}:t=-\frac{\pi}{4}\Rightarrow x=2\tan"
       r"\left(-\frac{\pi}{4}\right)+1=-1$, $y=2\sec^2\left(-\frac{\pi}{4}\right)+3=7$ $(-1, 7)$, $y=-\frac{1}{2}x+k"
       r"\Rightarrow7=\frac{1}{2}+k\Rightarrow k=\ldots$. Notes: A full attempt to find the $\textbf{upper}$ limit for "
       r"$k$. This requires an attempt to find the value of $x$ and the value of $y$ using $t=-\frac{\pi}{4}$, the "
       r"substitution of these values into $y=-\frac{1}{2}x+k$ and solves for $k$.",
       r"A1 (AO 1.1b): $(k=)\frac{13}{2}$. Notes: $k=\frac{13}{2}$. Look for this value e.g. may appear in an "
       r"inequality.",
       r"A1 (AO 2.2a): $\frac{43}{8}<k\leqslant\frac{13}{2}$. Notes: Deduces the correct range for $k$: $\frac{43}{8}<k"
       r"\leqslant\frac{13}{2}$ Allow equivalent notation e.g. $\left(k\leqslant\frac{13}{2}\text{ and }k>\frac{43}{8}"
       r"\right)$, $\left(k\leqslant\frac{13}{2}\cap k>\frac{43}{8}\right)$, $\left(\frac{43}{8},\frac{13}{2}\right]$ "
       r"But not e.g. $\left(k\leqslant\frac{13}{2}, k>\frac{43}{8}\right)$, $\left(k\leqslant\frac{13}{2}\cup k>\frac{"
       r"43}{8}\right)$, $\left(k\leqslant\frac{13}{2}\text{ or }k>\frac{43}{8}\right)$ and do not allow if in terms of "
       r"$x$. Allow equivalent exact values for $\frac{43}{8}$, $\frac{13}{2}$ $\textbf{There may be other methods for "
       r"finding the upper limit which are valid. If you are in any doubt if a method deserves credit then use "
       r"Review.}$",
       r"ALT: An alternative method using calculus for lower limit — M1: $y=" + Q16C + r"\Rightarrow" + DYDX + r"=x-1$, "
       r"$x-1=-\frac{1}{2}\Rightarrow x=\frac{1}{2}$ $x=\frac{1}{2}\Rightarrow y=\frac{1}{2}\left(\frac{1}{2}-1\right)^2"
       r"+5=\frac{41}{8}$ $y=-\frac{1}{2}x+k\Rightarrow\frac{41}{8}=-\frac{1}{4}+k\Rightarrow k=\ldots$. Notes: Score "
       r"$\textbf{M1}$ for $" + DYDX + r"=$”a linear expression in $x$”, sets $=-\frac{1}{2}$, solves a linear equation "
       r"to find $x$ and then substitutes into the given result in (b) to find $y$ and then uses $y=-\frac{1}{2}x+k$ to "
       r"find a value for $k$.",
       r"ALT: An alternative method using calculus for lower limit — A1: $k=\frac{43}{8}$ oe. Look for this "
       r"$\textbf{value}$ e.g. may appear in an inequality e.g. $k>\frac{43}{8}$, $k<\frac{43}{8}$",
       r"ALT: An alternative method using parameters for lower limit — M1: $y=-\frac{1}{2}x+k\Rightarrow2\sec^2t+3=-"
       r"\frac{1}{2}(2\tan t+1)+k$ $\Rightarrow2(1+\tan^2t)+3=-\frac{1}{2}(2\tan t+1)+k\Rightarrow2\tan^2t+\tan t+5.5-k="
       r"0$ $b^2-4ac=0\Rightarrow1-4\times2(5.5-k)=0\Rightarrow k=\frac{43}{8}$. Notes: Score $\textbf{M1}$ for "
       r"substituting parametric form of $x$ and $y$ into $y=-\frac{1}{2}x+k$, uses $\sec^2t=1+\tan^2t$ rearranges to "
       r"3TQ form and attempts $b^2-4ac\ldots0$ or e.g. $b^2-4ac>0$ or $b^2-4ac<0$ correctly to find a value for $k$.",
       r"ALT: An alternative method using parameters for lower limit — A1: $k=\frac{43}{8}$ oe. Look for this "
       r"$\textbf{value}$ e.g. may appear in an inequality e.g. $k>\frac{43}{8}$, $k<\frac{43}{8}$"],
      True, 44),
]

W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "The early questions were intended to be accessible to candidates of all abilities and indeed the modal "
            "mark for the first 4 questions was full marks."),
        (W, "The first question on the paper provided a good start for many candidates who were able to score full "
            "marks."),
        (W, "A fairly small minority solved by squaring both sides of the equation."),
        (W, "This method was generally very accurate when used.", BACK),
        (W, "Most candidates however, attempted the alternative strategy of setting up two separate equations."),
        (W, r"Of those who did not get full marks, most were able to identify that they should be solving $3-2x=7+x$ "
            r"but a common error was in the incorrect manipulation of the equation to get $x=-3/4$."),
        (W, "Others lost minus signs along the way or deliberately removed them, perhaps because this was a question "
            "involving modulus signs and they held the misconception that values should therefore be positive.", NO),
        (W, r"Many candidates were also able to identify that a second solution came from $2x-3=7+x$ but some "
            r"incorrectly assumed no negatives were permitted and instead used $2x+3=7+x$."),
        (W, r"As with the first solution, the most common error, once identifying the right equation, was due to "
            r"incorrect rearrangement to give $x=4$."),
        (W, "Some students however, only set up and solved one equation failing to recognise that two would be "
            "required."),
        (W, r"Although not required by the question, some candidates annotated their graphs; clearly constructing the "
            r"line $y=7+x$ to “show” the 2 solutions."),
        (W, r"Others unnecessarily calculated $y$ coordinates, perhaps misunderstanding what was required by a "
            r"‘solution’."),
        (W, r"A small number of candidates obtained the correct answers, but then rejected $x=-4/3$."),
        (W, "Other candidates incorrectly gave two positive solutions."),
        (W, "Candidates should be advised to refer back to the graph provided in the question as a means of checking "
            "the validity of their solutions."),
        (W, "In this case that one was clearly positive and one negative.", BACK),
        (W, "A substantial minority of candidates demonstrated a lack of understanding of the modulus function and "
            "simply changed negative signs to positive signs or assumed that the modulus function is distributive "
            "i.e. |a + b| = |a| + |b|."),
        (W, "A small number of candidates included inequalities in every step of their attempt and others maintained "
            "the presence of modulus signs throughout their entire attempt."),
    ],
    "02": [
        (W, "The early questions were intended to be accessible to candidates of all abilities and indeed the modal "
            "mark for the first 4 questions was full marks."),
        (W, "This question on an exponential function saw full marks for most."),
        ({"a"}, r"Of the small number of errors that were seen in part (a), a common one was an incorrect intercept of "
                r"$(0, 4)$ from replacing $4^0$ with 4 instead of 1."),
        ({"a"}, r"The intercept was occasionally seen as $(1, 0)$ although this was condoned if it was positioned "
                r"correctly on the sketch.", NO),
        ({"a"}, "A few graphs did not go into the second quadrant and others were not carefully drawn – some did not "
                r"get close enough to the asymptote of $y=0$, sometimes due to a poor choice of scale."),
        ({"a"}, "Other graphs bent back on themselves in the first quadrant."),
        ({"a"}, "Some students offered an incorrect or extra horizontal or even a vertical asymptote."),
        ({"a"}, "Although almost all knew the correct shape, a few responses had a straight line graph."),
        ({"b"}, r"Part (b) was similarly well-answered and most used logarithms correctly to obtain a correct "
                r"numerical expression for $x$."),
        ({"b"}, r"Those who did not use $x=\log_4100$ and arrived at $x=\frac{\log100}{\log4}$ sometimes processed "
                r"this incorrectly, arriving at log 96, log 25 or even 25.", NO),
        ({"b"}, "Some candidates who did not know how to solve the equation resorted to trial and improvement with "
                "varied success and is not a recommended strategy."),
    ],
    "03": [
        (W, "The early questions were intended to be accessible to candidates of all abilities and indeed the modal "
            "mark for the first 4 questions was full marks."),
        (W, "This question proved to be successful for many candidates and many scored full marks here."),
        ({"a"}, "In part (a)(i), the vast majority were able to successfully write down the sequence of terms and "
                "hence demonstrate that the sequence was periodic."),
        ({"a"}, "An algebraic proof was not required here, and one was only rarely seen."),
        ({"a"}, "Perhaps surprisingly having identified the pattern in the sequence in (a)(i), not all were able to "
                "identify the order of the sequence as ‘2’ in (a)(ii)."),
        ({"a"}, "This perhaps highlights a lack of awareness of what is meant by “order” of a sequence.", BACK),
        ({"a"}, r"Common incorrect answers here were: ‘first order’; ‘order 3, 5’; ‘$\pm2$’or just a re-writing of "
                r"their sequence from part (a)(i)."),
        ({"b"}, "In part b), candidates were most successful when they considered the nature of the sequence rather "
                "than trying to resort to a formula."),
        ({"b"}, "A fairly common first step was to divide 85 by 2 to give 42 with remainder 1."),
        ({"b"}, r"Many students then correctly broke down the sum into either $42\times3+43\times5$ or equivalently "
                r"$(42\times8)+3$.",
         {"note": "the 85 terms are 43 terms equal to 3 and 42 equal to 5; the mark scheme has 43 × 3 + 42 × 5"}),
        ({"b"}, r"Errors occurred when candidates struggled with the odd number of terms and believed they should "
                r"calculate $42.5\times5+42.5\times3$ resulting in an answer of 340, or when candidates mistakenly "
                r"thought that the 85th term was ‘5’ rather than ‘3’ resulting in an answer of 341."),
        ({"b"}, r"Other errors included summing only 84 terms $(42\times8=336)$ or attempts to ‘chunk’ incorrectly "
                r"into blocks of e.g. size 5: in such attempts the sum of the first five terms was obtained "
                r"$(3+5+3+5+3=19)$ followed by deduction that $\frac{85}{5}=17$ leading to an incorrect answer of "
                r"$19\times17=323$.", NO),
        ({"b"}, "A sizeable number of incorrect attempts involving use of the sum of arithmetic or geometric series "
                "were also commonly seen."),
        ({"b"}, "Perhaps most surprising was the significant minority who were able to set up a correct approach and "
                "write down a correct method but who then made arithmetical errors to write down an incorrect total "
                "which cost them the final A mark."),
    ],
    "04": [
        (W, "The early questions were intended to be accessible to candidates of all abilities and indeed the modal "
            "mark for the first 4 questions was full marks."),
        (W, "This question on differentiation from first principles saw good scoring and the method was widely "
            "recalled."),
        (W, r"A small number of slips with the algebra were seen and some replaced $\mathrm{f}(x+h)$ with $2x^2+h$ or "
            r"$(2x+h)^2$ or $2(x^2+h)$ instead of $2(x+h)^2$."),
        (W, r"There was the occasional poor squaring and mishandling of the “2”s e.g. expanding $2(x+h)^2$ to get "
            r"$2x^2+2xh+h^2$ was surprisingly common."),
        (W, r"Some leeway was afforded to the students with notation here although use of $h=0$ instead of $h\to0$ "
            r"was penalised if no indication of the limiting process was seen."),
        (W, r"A small number of responses did not have an “$\mathrm{f}'(x)=$” or equivalent and so forfeited the "
            r"final mark."),
    ],
    "05": [
        ({"a"}, "Part (a) of this question required candidates to use a given table of function values in an "
                "application of the Trapezium Rule."),
        ({"a"}, "This was generally done very well with candidates knowing how to apply the rule.", NO),
        ({"a"}, r"Most achieved $h=1.5$ although a common mistake was for students to think that the number of strips "
                r"was the same as the number of $x$ values instead of being one less."),
        ({"a"}, r"Thus dividing by 5 instead of 4 resulting in $h=1.2$."),
        ({"a"}, "Most knew how to apply the trapezium rule and had the bracketing correct and so achieved the correct "
                "answer."),
        ({"a"}, r"A few left out some of the brackets followed by an incorrect calculation. $\frac{1.5}{2}(1.63+2.63)"
                r"+2(2+2.26+2.46)$"),
        ({"a"}, r"With or without an outer bracket either at the beginning or end – would lead them to then calculate "
                r"the expression as it is written, often leading to an answer like: - $\frac{1.5}{2}(4.26)+13.44="
                r"3.195+13.44=16.635$"),
        ({"a"}, "There were a few who worked out the areas of individual trapezia and then summed the areas achieving "
                "a correct answer."),
        ({"a"}, "A minority didn’t know how to apply the rule"),
        ({"b"}, "Part (b) of the question clearly stated that the result from part (a) was to be used and that the "
                "method used was to be made clear."),
        ({"b"}, "Thus, candidates who proceeded to use the Trapezium Rule again with revised values of y received no "
                "credit."),
        ({"b"}, "In (b)(i) many realised that the power law of logs had to be used and realised that their answer to "
                "part (a) had to be multiplied by 10, so achieving a correct answer."),
        ({"b"}, "Many on the other hand unfortunately raised their answer to part (a) by a power of 10."),
        ({"b"}, "Most of those who attempted (b)(ii) didn’t realise that they had to split the expression into two "
                "parts applying log laws.", NO),
        ({"b"}, "Part of the expression then had to be integrated and added to their answer to part (a)."),
        ({"b"}, r"Often seen was the calculation $9\log_3(2x)$ or $9\times13.275$."),
        ({"b"}, r"Some seemed to think that $\log_3(18x)$ meant that the graph/function had been subjected to a "
                r"stretch of either 9 or 1/9."),
        ({"b"}, "Some didn’t show sufficient working to be sure that they were applying the correct method whilst "
                "others showed the correct use of logs but then just added 2 to their part (a) answer, not "
                "integrating this between the limits.", NO),
        ({"b"}, r"Even when a correct relationship of $\log_318x=\log_32x+\log_39$ was established, the subsequent "
                r"argument often did not have sufficient detail to show where their final answer came from."),
        ({"b"}, "The question clearly stated “making your method clear”."),
        ({"b"}, "Very few achieved full marks on this part."),
    ],
    "06": [
        ({"c"}, "For example, in question 6(c) where an application of the Newton Raphson process was required, there "
                "was a clear demand for students to show their method and yet many candidates just wrote down an "
                "answer."),
        ({"a"}, "Part (a) was generally well done with many candidates scoring 3 out of 4 but very few scoring 4 out "
                "of 4."),
        ({"a"}, r"Candidates generally understood that the question required an initial differentiation and this was "
                r"done correctly on the whole.", NO),
        ({"a"}, r"However, incorrect attempts at differentiation included: • $16\cos\left(\frac{1}{2}x\right)-3$ • "
                r"$8\cos\left(\frac{1}{2}x\right)-3$ • $-4\cos\left(\frac{1}{2}x\right)-3$"),
        ({"a"}, "Candidates also understood that they had to set their derivative to zero which required a combination "
                "of manipulating the algebra, applying arccos, and doubling their answer."),
        ({"a"}, "The difficulty encountered in this part was the recognition that it was the 3rd solution which was "
                "required and most gave either the 1st or 2nd turning point."),
        ({"a"}, "As a diagram was given in the question, candidates should use this to help them understand what is "
                "required.", NO),
        ({"a"}, "Some students who gave the 1st turning point also checked by further differentiation that their point "
                "was a maximum."),
        ({"a"}, r"A few candidates unnecessarily found the corresponding $y$ value for their $x$ value."),
        ({"a"}, r"In establishing their value of $x$, it was disappointing to see all of the following: • candidates "
                r"halving instead of doubling • using degrees • arriving at a correct answer but leaving it as 14.01 "
                r"instead of 14.0"),
        ({"b"}, "In part (b), most candidates only referred to the change of sign and didn’t mention continuity."),
        ({"b"}, "Occasionally a candidate wanted to allude to continuity but was unable to articulate this correctly.",
         NO),
        ({"b"}, "For example incorrect wording including referring to the graph as “constant”."),
        ({"b"}, "Some candidates who referred to continuity used incorrect statements such as “because x is continuous” "
                "or “because the interval (or data) is continuous”."),
        ({"c"}, "Part (c) was answered well with many candidates scoring full marks."),
        ({"c"}, "Amongst those who didn’t score full marks, many did not heed the demand in the question to “Show your "
                "method” and just quoted their calculator’s solution without any explanation whilst others just wrote "
                "down a formula but did not show an application with values embedded."),
        ({"c"}, "Others made rounding mistakes such as giving a final answer of 4.805 or 4.81."),
        ({"c"}, r"Premature rounding of $\mathrm{f}(5)$ and $\mathrm{f}'(5)$ also led to a final answer of 4.81."),
        ({"c"}, "A significant number of candidates erroneously used degrees but could score the method mark if "
                "appropriate working was shown."),
        ({"c"}, "Some candidates were able to “recover” minimal working due to the accuracy of their answer 4.804...., "
                "and gained the two marks."),
        ({"c"}, r"Some candidates also evaluated $\mathrm{f}(5)$ incorrectly even though it was given in the "
                r"question.", NO),
        ({"c"}, r"It was disappointing to see students misquoting The Newton-Raphson formula, typically with "
                r"$\mathrm{f}(x)$ and $\mathrm{f}'(x)$ the wrong way round, even though the formula was given in the "
                r"formula book.", NO),
    ],
    "07": [
        (W, "This question on binomial expansion was well attempted and generally well answered by most candidates."),
        ({"a"}, r"In part (a), almost all candidates achieved at least 1 mark, either by extracting the factor of "
                r"$4^{1/2}$ correctly, or for having a correct binomial coefficient multiplied by the corresponding "
                r"power of $x$ on their 3rd or 4th term."),
        ({"a"}, r"A few candidates omitted the $-9/4$ and wrote $\frac{\left(\frac{1}{2}\right)\left(\frac{1}{2}-1"
                r"\right)}{2!}x^2$ as their 3rd term, which was not awarded the method mark."),
        ({"a"}, r"Some candidates used $9/4$ erroneously, instead of $-9/4$ in their expansion, and this could still "
                r"gain the method mark but meant the two accuracy marks were lost.", NO),
        ({"a"}, "Candidates bracketing was sometimes incorrect but often recovered by later work."),
        ({"a"}, r"A common response seen was a correct expansion of $\left(1-\frac{9x}{4}\right)^{1/2}$ but failure "
                r"to multiply this by the “2” they had factorised outside the bracket at the beginning.", NO),
        ({"a"}, "A minority of candidates attempted a direct expansion method, and many of these achieved the first "
                "mark only for a correct first term, as they often did not find the correct binomial coefficients.",
         NO),
        ({"a"}, "Unfortunately, several candidates made number of slips, or omitted an exponent, in their final line "
                "and did not write the correct answer following correct working and so lost the final accuracy mark."),
        ({"b"}, "In part (b) very few could articulate correctly why this was an overestimate.", NO),
        ({"b"}, "Many left this part out or just wrote overestimate or underestimate with no explanation.", NO),
        ({"b"}, "Some were very inventive in their reasons."),
        ({"b"}, "Poor wording/clarity on subtracting terms, such as ‘decreasing trend’, or ‘terms decreased’ but not "
                "specifically stated to be subtracted from the leading 2."),
        ({"b"}, "Many tried substituting in values to show it was smaller which was not sufficient.", NO),
        ({"b"}, "The majority did not relate the reasoning back to the binomial expansion directly."),
        ({"b"}, r"Some went on to evaluate the binomial using $x=1/9$."),
        ({"b"}, "Some said the terms were getting smaller rather than pointing out that they were negative."),
        ({"b"}, "Some, however, gave a very clear reasoned argument."),
        ({"b"}, r"Several students answered part (b) with an explanation about the validity of the expansion using "
                r"$|x|<1$."),
        ({"b"}, "Some students thought the overestimation was due to the fact that the expansion had only used 4 terms "
                "and that the approximation would be better if more terms were used, with no reference to the fact "
                "that they should be subtracted from 2."),
        ({"b"}, r"A common mistake was stating that $x<\left[\frac{4}{9}\right]$ which in their opinion meant that the "
                r"approximation was over/underestimation due to the fact that $\frac{4}{9}<\frac{1}{9}$ or the other "
                r"way round."),
    ],
    "08": [
        (W, "Most students knew that this question was to be solved by integration although a very small number "
            "thought that the question was about partial fractions, differentiation or a mixture of differentiation "
            "with integration."),
        (W, "There were multiple approaches to solving this question including integrating a function with simplified "
            "indices, integrating by parts and integrating by substitution."),
        (W, "The most common and the simplest method seen was multiplying out and simplifying indices."),
        (W, r"For the candidates who recognised that $4\sqrt{x}$ in the denominator should be rewritten as $\frac{1}"
            r"{4}x^{-\frac{1}{2}}$ in the numerator there was a lot of success on this question."),
        (W, "However, there were many candidates who brought the 4 to the top and left it as 4 rather than ¼ and "
            "earned a maximum of 3/6."),
        (W, r"Some wrote $4x^{\frac{1}{2}}$ in the numerator multiplying out to give incorrect powers and losing the "
            r"first two method marks."),
        (W, "Finding the correct limits and substituting them in a changed function was done by most leading to quite "
            "a few correct answers."),
        (W, r"Quite a few gave part or all of the final answer as a decimal, this was not surprising as most were "
            r"using their calculators to do the final evaluation and calculator use did not leave the result of e.g. "
            r"$(\sqrt{2})^5$ as a surd.", NO),
        (W, "Some candidates recognised that the area needed to be positive, however the final answer was permissible "
            "even with a negative area."),
        (W, "There were often errors in solutions constructed using integration by parts."),
        (W, "There were mistakes made using the formula correctly, some bracketing errors, and some attempted parts "
            "the other way round getting harder expressions in the integral which mostly resulted for them a maximum "
            "of 1 mark (3rd M mark) obtained."),
        (W, r"There were a few incorrect substitutions selected for integration by substitution approaches, however "
            r"candidates who chose $u=\sqrt{x}$ or $u=4\sqrt{x}$ were generally successful."),
        (W, r"A few candidates who set e.g. $u=x-2$ in a substitution method scored few marks, if any, as such "
            r"attempts did not progress the candidate towards a function they could integrate.", NO),
        (W, "In substitution method a few candidates made arithmetic errors in finding the new limits or did not "
            "attempt to change them at all.", NO),
    ],
    "09": [
        ({"a"}, "This was a challenging question for the majority of the candidates with very few scoring all four of "
                "the marks in part (a)."),
        ({"a"}, "For those that attempted the question, most scored at most 1 or 2 marks.", NO),
        ({"a"}, r"These were the initial B1 mark for realising that $A=50$, however many wrote that $H=50$ and did not "
                r"relate that $H$ meant $A$.", BACK),
        ({"a"}, r"The second B mark for finding a value for $b$ was very poorly answered, with many not realising a "
                r"simple calculation of $\frac{180}{720}$ was needed and attempted to use an ‘$R-\alpha$’ method or "
                r"failed to take into account transformations of the sine function, showing a lack of understanding "
                r"of the properties of the sine wave."),
        ({"a"}, r"Some also tried to use $\frac{\mathrm{d}H}{\mathrm{d}t}$ with very limited success."),
        ({"a"}, r"A small minority of students achieved $b=1/4$."),
        ({"a"}, r"The best answers tended to use transformation arguments, recognising that the full cycle depicted "
                r"must represent a scale factor of 4 though many students attempting this approach did not "
                r"appreciate the effect of the modulus in determining the value of $b$, obtaining instead a value of "
                r"$b=\frac{1}{2}$.", NO),
        ({"a"}, r"A common incorrect method came from consideration of the wheel taking 720 seconds to complete 1 "
                r"revolution leading candidates to solve the equation $720b+1.15=180$ or from thinking that the "
                r"maximum occurs at $t=360$ leading to $360b+1.15=90$."),
        ({"a"}, r"Of those that managed to access the question, few mixed radians with degrees and managed to give an "
                r"answer as $\frac{\pi}{720}$ or $\frac{2\pi}{720}$, which scored no marks.", NO),
        ({"a"}, r"1010 was the most common mark profile for this question, as a significant number of students went "
                r"on to find $\alpha$ correctly (albeit occasionally in radians) as they were able to spot that at "
                r"$t=0$, $H=1$."),
        ({"a"}, "Sadly, a few that did achieve all three elements did not conclude with an equation of the model and "
                "so lost the (easy) last mark, with this final mark being scored very rarely, at less than 5% of the "
                "cohort (the second least commonly scored mark in the paper).", NO),
        ({"b"}, r"In part (b), many candidates incorrectly referred to the fact that the passenger was 1 m above the "
                r"ground and related the value of $d$ to this fact, for the most part because they had not "
                r"appreciated that the original model already took this into account.", NO),
        ({"b"}, "Some responses referred to the fact that the height needed to be a positive value or could not be "
                "negative, again missing that the modulus signs in the original model accounted for this.", NO),
        ({"b"}, "Some responses did not refer to the context of the model in their explanation."),
        ({"b"}, r"Overall, around a fifth of candidates understood that the passenger would touch the ground without "
                r"adding the constant ‘$d$.’"),
        ({"b"}, "There were also a few illogical answers referring to air resistance, etc."),
        ({"b"}, r"A few students also incorrectly though that ‘+ $d$’ was in reference to the different heights of the "
                r"passengers."),
        ({"b"}, r"A small number of candidates seemed to think that the graph showed the path of the position of the "
                r"passenger, referencing that the passenger “bounced off the ground” and that the ‘+ $d$’ had the "
                r"effect of smoothing out the ride."),
        ({"b"}, r"When students were successful in this part the most common responses were that ‘+ $d$’ meant that: "
                r"the Ferris wheel would not touch/scrape the ground, the passenger/seat cannot touch the ground or "
                r"there needed to be a minimum gap between the passenger/wheel and the ground."),
        ({"b"}, "There were many attempts at part (b) without any attempt at part (a)."),
        ({"b"}, "It was unfortunately quite common that responses to this part were very difficult to read and centres "
                "need to stress to candidates that work cannot be awarded marks if it is illegible.", NO),
    ],
    "10": [
        (W, "Parts (a) and (b) were generally answered well by most candidates, however parts (c) and (d) proved to be "
            "good discriminators with many failing to score any marks."),
        ({"a"}, r"Part (a) required candidates to find $\mathrm{f}^{-1}\left(\frac{3}{2}\right)$."),
        ({"a"}, r"The most common approach seen was finding the inverse function then substituting in $x=\frac{3}{2}$."),
        ({"a"}, "This was usually carried out successfully with a few candidates losing a mark for arithmetic slips "
                "when rearranging.", BACK),
        ({"a"}, r"Very few attempted the more straightforward method of solving $\mathrm{f}(x)=\frac{3}{2}$."),
        ({"a"}, r"Of those gaining no marks, the common misconception was substituting $x=\frac{3}{2}$ into the "
                r"reciprocal of the function or evaluating $\mathrm{f}\left(\frac{3}{2}\right)$."),
        ({"a"}, r"Several substituted $x=\frac{3}{2}$ into $\mathrm{f}'(x)$."),
        ({"b"}, "In part (b) most students seemed confident about how to start and the majority of those who attempted "
                "it achieved both marks.", NO),
        ({"b"}, r"Candidates either equated the numerator to achieve $8x+5=A(2x+3)+B$ or used the long division "
                r"method."),
        ({"b"}, r"There were some errors in calculating $A$ after finding the correct value for $B$."),
        ({"b"}, "Those who used the long division method made fewer mistakes than those who compared coefficients."),
        ({"b"}, "A few candidates attempted to manipulate the numerator and expressed it in terms of the denominator "
                "with a good rate of success.", NO),
        ({"b"}, r"A few candidates lost the final accuracy mark due to substituting the correct $A$ and $B$ into the "
                r"wrong place to give $-7+4/(2x+3)$"),
        ({"c"}, "In part (c) it was common to see the correct boundary values given but many lost the mark by using "
                "incorrect notation."),
        ({"c"}, r"Common errors seen were $0\leqslant x\leqslant4$, $0\leqslant\mathrm{g}(x)\leqslant4$, or even "
                r"$0\leqslant\mathrm{f}(x)\leqslant4$; using < instead of $\leqslant$; or missing out the lower "
                r"boundary value altogether."),
        ({"c"}, r"Many did not realise that the values of the range of $\mathrm{g}^{-1}(x)$ are the same as the domain "
                r"of $\mathrm{g}(x)$ and found $\mathrm{g}^{-1}(x)$ first but then failed to give the correct range, "
                r"gaining no marks."),
        ({"c"}, "Giving the range as 0 to 16, instead of 0 to 4 was a common incorrect answer."),
        ({"c"}, "A significant number obtained only one of the correct values."),
        ({"d"}, "Part (d) proved to be demanding for most candidates."),
        ({"d"}, r"Some candidates realised they could simply evaluate $\mathrm{f}(0)$ and $\mathrm{f}(4)$ to find the "
                r"boundary values but most started by trying to find an expression for $" + FG + r"(x)$."),
        ({"d"}, r"Many were able to find $\mathrm{g}^{-1}(x)=\sqrt{(16-x)}$ and used this to obtain $" + FG
                + r"(x)=(8\sqrt{(16-x)}+5)/(2\sqrt{(16-x)}+3)$ or $" + FG + r"(x)=4-7/(2\sqrt{(16-x)}+3)$ (using "
                r"their answer to (b)).", NO),
        ({"d"}, "Some made no further progress from here and thus scored no marks."),
        ({"d"}, r"Of those that did carry on, common errors from this point included using 4 as the upper value rather "
                r"than 16 or changing $\sqrt{(16-x)}$ to an incorrect expression such as $4-\sqrt{x}$.", NO),
        ({"d"}, "Since one of the boundary values was 0 some candidates found 37/11 from incorrect work and did not "
                "score the method mark."),
        ({"d"}, r"Some candidates, who did find the correct values, lost the final mark by using < instead of "
                r"$\leqslant$ in their inequality."),
        ({"d"}, "It was not uncommon to see part (d) left blank."),
    ],
    "11": [
        (W, "The formal proof question, Question 11, saw more success than in previous series as students become more "
            "familiar with this type of question."),
        (W, "Most students made some attempt at this proof question, and there was a mixture of responses that "
            "achieved the full range of possible marks."),
        (W, "It was striking that a number of students attempted to answer the question without doing any algebra, "
            "despite the clear instruction within the question.", NO),
        (W, r"Most candidates who used algebra recognised that a strategy of considering odd and even numbers could be "
            r"used to prove the statement with most using $n=2k$ and $n=2k+1$, although a minority only attempted one "
            r"of these.", NO),
        (W, r"Within the algebra, a common misconception was that $(2k)^2=2k^2$."),
        (W, r"Occasionally there were a few candidates that tried to consider the cases of $3k-1$, $3k$, and $3k+1$ "
            r"which caused those candidates difficulty in progressing the proof.", NO),
        (W, "Although students knew that they needed to show the expression was a multiple of 2 to conclude that it "
            "was even, few seemed to be looking for the earliest opportunity to do this, and therefore did more "
            "algebraic manipulation than was necessary.", NO),
        (W, r"Some also presented expressions like $8k^3+12k^2+16k+6$ and declared them to be even without explaining "
            r"why this is the case.", NO),
        (W, r"A handful used $n=2n+2$ for the even case, again having to do more algebraic manipulation than was "
            r"needed."),
        (W, "Most candidates who attempted this approach gained the method marks but the accuracy marks were sometimes "
            "lost for algebraic slips or more commonly for failing to give a final statement that the result was "
            "even for both odd and even cases, or simply stating that the statement was a multiple of 2 without "
            "concluding that it was therefore even.", {"ref": "Most candidates who used algebra"}),
        (W, r"It was surprising for the odd case how many candidates had a preference for fully expanding their "
            r"expressions into a cubic before factorising, i.e. $8k^3+12k^2+16k+6=2(4k^3+6k^2+8k+3)$ rather than "
            r"simply factoring $(2k+1)(4k^2+4k+6)$ into $2(2k+1)(2k^2+2k+3)$ for example which is algebraically "
            r"easier to achieve.", NO),
        (W, "Where algebra was not used, the most common approach was to use a logic argument involving the rules of "
            "combining odd and even numbers."),
        (W, "Where the argument was convincing students were sometimes able to gain the method marks."),
        (W, "A few candidates attempted a proof by contradiction or by induction, but usually produced an argument "
            "that was incomplete and made little progress."),
    ],
    "12": [
        ({"a"}, "Part (a) was generally well answered."),
        ({"a"}, "The quotient rule was usually applied correctly for the first two marks and, given the quadratic "
                r"factor was given, most candidates were able to arrive at the correct expression for $\mathrm{g}(x)$."),
        ({"a"}, "Some used the product rule instead and usually gained the first two marks although it was a little "
                "more difficult to get the final answer and some algebraic errors were made.", NO),
        ({"a"}, "Although most candidates gained the M mark in (a) their brackets were very often incorrect or "
                "missing."),
        ({"a"}, "This was usually recovered in later steps allowing full marks to be obtained.", BACK),
        ({"a"}, r"When differentiating $4x^2+k$, some candidates left $k$ in the answer, or differentiated to $8x+1$, "
                r"gaining no marks."),
        ({"a"}, "Occasionally the terms on the numerator were reversed and these attempts gained no marks in (a) as in "
                "incorrect method was implied.", BACK),
        ({"a"}, r"Some missed the 3 when differentiating $\mathrm{e}^{3x}$ using the chain rule."),
        ({"a"}, "Most candidates understood there was no need to expand the denominator."),
        ({"a"}, "Where they did so, they generally did it correctly and no marks were lost.", BACK),
        ({"a"}, r"This was a “Show that” question so “$\mathrm{f}'(x)=$” or “$" + DYDX + r"=$” needed to be seen and "
                r"was sometimes missing, losing the final A mark.", NO),
        ({"b"}, "Candidates found part (b) more challenging."),
        ({"b"}, r"Although most knew to set $\mathrm{f}'(x)$ to zero for stationary points, there were many marks lost "
                r"due to insufficient rigour in the presentation of method when looking for one or more roots."),
        ({"b"}, r"Generally candidates understood that it was the quadratic expression that needed to be used and not "
                r"any part of $\mathrm{g}(x)$.", NO),
        ({"b"}, "Overall, most realised that the number of solutions for a quadratic was determined by the "
                "discriminant although a significant number did not."),
        ({"b"}, r"The majority attempted $b^2-4ac$ with the appropriate values but candidates often set $b^2-4ac=0$ "
                r"rather than $b^2-4ac\geqslant0$."),
        ({"b"}, r"The B mark was usually gained by the use of the discriminant > or $\geqslant0$, it was rarely gained "
                r"by making an appropriate statement.", NO),
        ({"b"}, r"Some stated $\mathrm{g}(x)\neq0$ and a few $\mathrm{g}(x)>0$ which may have been required if full "
                r"justification had been required."),
        ({"b"}, r"Most candidates gained the M mark for calculating the value of the discriminant using the correct "
                r"values for $a$, $b$ and $c$."),
        ({"b"}, r"Other methods included completing the square to find the least value of the quadratic and then "
                r"considering the $y$ coordinate."),
        ({"b"}, r"Some differentiated the quadratic to find the minimum turning point and again considered the $y$ "
                r"value."),
        ({"b"}, "These alternative methods were often incomplete and unsuccessful in most cases seen.", BACK),
        ({"b"}, r"Few realized the range had a lower limit, but this was condoned for the A mark as the $k$ was "
                r"defined as positive in the question.", NO),
        ({"b"}, r"A common error was to give the final inequality as $k<\frac{4}{9}$."),
    ],
    "13": [
        (W, "This question was a good differentiator, with the majority of candidates gaining some credit, but only "
            "the strongest achieving full marks."),
        (W, "Overall, candidates often demonstrated good reasoning skills and were rewarded with good marks on this "
            "question but a significant number of candidates struggled with this topic."),
        (W, "Throughout, methods of solution were many and varied, and often involved non vector approaches that were "
            "sometimes difficult to follow."),
        ({"a"}, r"In part (a) candidates using a vector method often attempted to subtract the given position vectors "
                r"to form at least two of the vectors $\pm" + V("AB") + r"$, $\pm" + V("AC") + r"$ or $\pm" + V("BC")
                + r"$ although errors in their components were common."),
        ({"a"}, r"Candidates unfortunately often misread $" + V("OB") + r"$ as $\begin{pmatrix}4\\0\\6\end{pmatrix}$ or "
                r"$\begin{pmatrix}4\\6\\0\end{pmatrix}$."),
        ({"a"}, r"This was as far as many candidates reached, but some were able to successfully complete this "
                r"approach by establishing $" + V("BC") + "=4" + V("AB") + "$, $" + V("AC") + "=5" + V("AB") + r"$ or "
                r"$5" + V("BC") + "=4" + V("AC") + r"$ and reached $p=32$.", BACK),
        ({"a"}, r"Some candidates incorrectly used methods like $" + V("AC") + "=" + V("AB") + r"$ or assumed that the "
                r"original position vectors were parallel."),
        ({"a"}, "Candidates attempting to work out the magnitudes of vectors usually gained no marks."),
        ({"a"}, r"Others who made progress with vector methods, established the vector equation of the straight line "
                r"through $A$, $B$ and $C$ and used this to find $p$.", NO),
        ({"a"}, r"Candidates often used non vector methods as well."),
        ({"a"}, r"A common approach was to ignore one component and compare ‘gradients’ using the other two e.g. "
                r"$\frac{4-(-3)}{0-4}=\frac{p-4}{-16-0}$."),
        ({"a"}, "This was judged to be an acceptable approach, although errors with the substitution of values were "
                "common.", BACK),
        ({"a"}, r"Some even established an ‘equation’ such as $y=-\frac{7}{4}x+4$ and then substituted in $x=-16$ to "
                r"find $p$, which, again, was acceptable, but it was a shame that so many candidates resorted to such "
                r"methods and seemed to lack confidence in their ability to construct a solution using vectors.", NO),
        ({"a"}, r"In some cases where the first method mark was awarded, candidates went on to an incorrect equation "
                r"such as $p=4\times7$ and were much less likely to be awarded the second method mark, as it was often "
                r"unclear which vector they were working with for this step.", NO),
        ({"a"}, "Many fully correct answers for (a) were seen, sometimes with minimal working."),
        ({"a"}, "It should be noted here that candidates should try to make their intention clear, as there were many "
                "occasions where examiners struggled to follow the structure of candidates’ work and were unable to "
                "award marks as a result.", NO),
        ({"b"}, "Part (b) was found to be challenging by most candidates, with few gaining any marks and with many not "
                "attempting it.", NO),
        ({"b"}, "Many candidates again worked with magnitudes of vectors and made no progress."),
        ({"b"}, r"Those candidates who did gain credit usually used the fact that $k" + V("OB") + "-" + V("OC")
                + r"=\begin{pmatrix}16\\4k-p\\6k-10\end{pmatrix}$ was parallel to $" + V("OA") + r"$ to find $k=5$ "
                r"giving $" + V("OD") + r"=\begin{pmatrix}0\\20\\30\end{pmatrix}$.", NO),
        ({"b"}, r"Many candidates failed to realise that $" + V("OD") + r"=k\begin{pmatrix}0\\4\\6\end{pmatrix}$, and "
                r"made no progress, whilst others incorrectly assumed that $\begin{pmatrix}16\\4k-p\\6k-10"
                r"\end{pmatrix}=" + V("OA") + "$."),
        ({"b"}, "Candidates often drew diagrams to visualise the problem but full marks in this part were rarely "
                "awarded."),
        ({"b"}, "A significant number of candidates who had found the correct vector, failed to find its magnitude.",
         NO),
    ],
    "14": [
        ({"a"}, "In part (a) a large proportion of candidates demonstrated a good understanding of how to find the "
                "partial fractions and the methods seen were often very clear."),
        ({"a"}, r"Substitution of $x=-1$ and $x=1/2$ was much more common than comparing coefficients."),
        ({"a"}, "Generally the only mistakes made on this part of the question were arithmetic."),
        ({"a"}, "A small number lost the final mark for failing to write out the complete partial fractions."),
        ({"a"}, r"A minority of candidates used $A+B(x+1)+C(2x-1)$ thinking it was an improper fraction but many "
                r"proceeded correctly to found $A=0$.", NO),
        ({"b"}, "The most challenging aspect of part (b) for the candidates was to separate the variables correctly."),
        ({"b"}, r"A large proportion of candidates did not make the link to part (a) and often divided both sides by "
                r"$3V$ as a starting point, i.e. $\int\frac{1}{3V}.\,\mathrm{d}V=\int\frac{1}{(2t-1)(t+1)}.\,"
                r"\mathrm{d}t$"),
        ({"b"}, "Where candidates did this they often would incorrectly replace the right hand side with the partial "
                "fraction they had found in part (a).", BACK),
        ({"b"}, "For the candidates that got as far as this, the integration of the partial fractions they put in "
                r"place was generally completed well with the key $\ldots\ln(2t-1)-\ldots\ln(t+1)$ being found more "
                r"often than not although a common error was leaving a multiplier of 2 when integrating the first "
                r"fraction to give $2\ln(2t-1)$.", BACK),
        ({"b"}, "Regardless of the integration a candidate had achieved, there were a large number of candidates that "
                "did not consider the constant of integration and tried to jump straight to the answer at this "
                "stage."),
        ({"b"}, r"Generally, if a candidate remembered their integration constant, they were more often than not "
                r"successful in using the given limits to obtain a value which they could use to find an equation for "
                r"$V$."),
        ({"b"}, "A few attempts at solving the first order linear differential equation using an Integrating Factor "
                "were seen."),
        ({"b"}, "Those employing this method were usually reasonably successful.", BACK),
        ({"c"}, "In part (c) the solution of 30mins was only obtained by the strongest candidates although many did "
                "not attempt this part of the question or possibly failed to see it.", NO),
        ({"c"}, "Of those that did attempt this part, a common answer was to obtain ½ but not recognise the units of "
                "the question were in hours, some giving it incorrectly as 0.5 minutes", NO),
        ({"c"}, "As the equation for the volume was a given in this question most candidates were able to attempt this "
                "in spite of their attempt at part (b).", NO),
        ({"c"}, r"Candidates gave the correct 6m$^3$ although a substantial number thought that 3m$^3$ was the "
                r"answer."),
        ({"c"}, r"Although candidates were not required to provide units, many did so correctly and marks were rarely "
                r"lost for stating incorrect units although a few instances of mm$^3$ were seen."),
    ],
    "15": [
        (W, "The majority of candidates found this question accessible and were able to score consistently "
            "throughout."),
        (W, "Where marks were lost they were usually in parts (b) and (c)."),
        ({"a"}, r"Part (a) was attempted successfully by most candidates, starting usually with $\frac{5+2\sin\theta}"
                r"{12\cos\theta}=\frac{6\tan\theta}{5+2\sin\theta}$."),
        ({"a"}, "Candidates then successfully cross multiplied and used the appropriate identity to reach the required "
                "result."),
        ({"a"}, r"Another starting point regularly seen was $6\tan\theta=12\cos\theta\left(\frac{5+2\sin\theta}{12\cos"
                r"\theta}\right)^2$."),
        ({"a"}, "Errors in the proof were rare if candidates started from a correct statement."),
        ({"a"}, "Occasionally the “ = 0” was carelessly missing."),
        ({"b"}, r"In part (b) most candidates correctly solved the equation either by factorising or using calculator "
                r"technology, but many reached the acute angle $\frac{\pi}{6}$ rather than the required obtuse angle "
                r"of $\frac{5\pi}{6}$."),
        ({"b"}, r"Others found a number of solutions but failed to identify $\frac{5\pi}{6}$ as the required answer."),
        ({"b"}, "A few candidates worked in degrees and again lost the accuracy mark."),
        ({"c"}, r"Those who had obtained an angle of $\frac{\pi}{6}$ in (b) then usually carried this error into (c) "
                r"and were in a position only to earn the method marks.", NO),
        ({"c"}, r"Candidates using $\frac{\pi}{6}$ in (c) often would reach $9(1+\sqrt{3})$, but did not seem to worry "
                r"that this did not match the required answer format given in the question.", NO),
        ({"c"}, "There were many attempts, however, to use the correct formula for the sum to infinity with "
                "appropriate values for the first term and the common ratio."),
        ({"c"}, r"Some candidates unfortunately put effort into finding and rearranging (often incorrectly) algebraic "
                r"expressions for the sum to infinity involving $\theta$, without substituting an angle in, gaining no "
                r"credit, and others used $\frac{a}{1+r}$ incorrectly as the formula for the sum to infinity."),
        ({"c"}, "The most common mistake in (c) was failure to show the steps where the denominator was rationalised."),
        ({"c"}, r"Many candidates clearly typed an expression like $\frac{-6\sqrt{3}}{1-\left(-\frac{\sqrt{3}}{3}"
                r"\right)}$ straight into their calculators to obtain $9-9\sqrt{3}$ losing the last two marks in the "
                r"question."),
    ],
    "16": [
        (W, "This question proved to be a good differentiator between candidates."),
        (W, "It provided a challenge for many candidates but equally there were a number of accessible marks here.",
         NO),
        (W, r"Most candidates attempted part (a), many attempted part (b) and at least partially attempted part (c), "
            r"usually attempting to find the lower limit for $k$."),
        (W, "There were, however, very few completely correct answers to this question and a substantial minority made "
            "no attempt at any part, perhaps having run out of time by the time they reached the last question on the "
            "paper."),
        ({"a"}, "Part (a) was mostly approached correctly with a good number scoring full marks."),
        ({"a"}, "Candidates generally noticed the instruction to use parametric differentiation."),
        ({"a"}, r"Whilst $\frac{\mathrm{d}x}{\mathrm{d}t}$ was most often correct, $\frac{\mathrm{d}y}{\mathrm{d}t}$ "
                r"proved a challenge for many who struggled to differentiate $\sec2t$.",
         {"note": "the curve has y = 2sec²t + 3, so the function to differentiate is sec²t"}),
        ({"a"}, "Many did not seem to know that these functions were standard derivatives presented in the formula "
                "booklet and instead there were some long-winded and overly complex attempts to convert to sine or "
                "cosine functions and such approaches often led to errors.", BACK),
        ({"a"}, r"However, even some of the most inefficient approaches managed to persevere through lengthy algebra "
                r"to obtain a correct $" + DYDX + r"$ eventually."),
        ({"a"}, r"Almost all who attempted $\frac{\mathrm{d}x}{\mathrm{d}t}$ and $\frac{\mathrm{d}y}{\mathrm{d}t}$ knew "
                r"and attempted $" + DYDX + r"=\frac{\mathrm{d}y}{\mathrm{d}t}\div\frac{\mathrm{d}x}{\mathrm{d}t}$."),
        ({"a"}, r"Those who made errors when determining $" + DYDX + r"$ often exhibited an over-reliance on trying to "
                r"match the printed result and thus ‘adjusted’ their $" + DYDX + r"$ in an attempt to obtain the "
                r"required value for the normal gradient.", NO),
        ({"a"}, "Often this meant the loss of a method mark.", BACK),
        ({"a"}, "Candidates would be better advised to utilise a correct method rather than incorrectly manipulating "
                "their answers to match the result they are attempting to achieve and caution should always be advised "
                "when working backwards from a given answer.", NO),
        ({"a"}, "Nonetheless, application of negative reciprocals and equations of lines was generally successfully "
                "attempted, and candidates were clearly confident in these areas.", NO),
        ({"a"}, "There were a few attempts at a Cartesian approach in part (a) which gained zero marks as the question "
                "had specified the use of parametric differentiation."),
        ({"b"}, "In part (b), there were a multitude of approaches seen and candidates were often at least partially "
                "successful."),
        ({"b"}, r"Most candidates recognised the need to begin with a trigonometric identity, usually $\sec^2t=1+\tan^2"
                r"t$ and rearranged the expressions for $x$ and $y$ to obtain expression for $\sec^2t$ and $\tan^2t$ "
                r"before substituting into the identity to obtain an equation in $x$ and $y$ which could in turn be "
                r"rearranged to the required form."),
        ({"b"}, r"However, sometimes candidates took a far lengthier approach, beginning with e.g. $\sin^2t+\cos^2t=1$ "
                r"and using $x$ and $y$ to find expressions for $\sin t$ and $\cos t$."),
        ({"b"}, r"An alternative and popular, though inelegant, method was to start from the target Cartesian equation "
                r"and substitute in the trigonometric forms for $x$ and $y$ before rearranging to obtain an identity."),
        ({"b"}, "Provided a conclusion was given, this approach was credited with both marks.", BACK),
        ({"b"}, r"Occasionally candidates used the equation for $x$ to obtain an expression for $t$ in terms of "
                r"arctangent before substituting into the expression for $y$ which, if correctly done, was an "
                r"acceptable approach."),
        ({"b"}, r"Several students just substituted the coordinates of points such as $P$ into the given Cartesian "
                r"equation, stating that they satisfied the equation."),
        ({"b"}, "Such attempts did not constitute a proof and so gained no marks.", BACK),
        ({"c"}, "Part (c) provided a particular challenge and usually only the lower limit was attempted."),
        ({"c"}, "Most candidates appeared to completely miss the need to find an upper limit."),
        ({"c"}, "Of those who did manage to find both limits, only a small minority of candidates got to the final "
                "solution with correct inequality interpretation."),
        ({"c"}, "It is worth noting that candidates achieving full marks for this part very often had clear "
                "construction lines on their graph that enabled them to see the correct approach.", NO),
        ({"c"}, r"Most often though, candidates gained the method mark for the lower limit, $\frac{43}{8}$, for "
                r"identifying that two intersections were required and set up a correct inequality for the "
                r"discriminant for the quadratic equation obtained by equating the equations of the line and the "
                r"curve."),
        ({"c"}, r"Common errors in manipulation, particularly of the coefficient of ½ from the quadratic meant that a "
                r"number of candidates did not earn the accuracy mark for 43/8."),
        ({"c"}, r"Many candidates stopped after obtaining a lower limit for $k$, but others explored the parameter "
                r"limits at $t=-\frac{\pi}{4}$ and $t=\frac{\pi}{3}$ to identify $k$ values of $\frac{13}{2}$ and "
                r"$\frac{23}{2}-\sqrt{3}$ for the line passing through the associated points.",
         {"note": "at t = π/3 the point is (2√3 + 1, 11), which gives k = 23/2 + √3"}),
        ({"c"}, r"Very few, however, recognised $\frac{13}{2}$ as an upper limit and a number of candidates assumed "
                r"incorrectly that $\frac{13}{2}<k<\frac{23}{2}-\sqrt{3}$.",
         {"note": "at t = π/3 the point is (2√3 + 1, 11), which gives k = 23/2 + √3"}),
        ({"c"}, r"A minority of candidates incorrectly thought that setting $" + DYDX + r"=0$ or $" + DYDX + r"=-"
                r"\frac{1}{2}$ would provide limiting criterion for $k$ values."),
        (W, "In summary this was an interesting question which gave rise to a wide variety of responses in all three "
            "parts."),
        (W, "There were instances of both succinct and ingenious approaches seen, particularly in part (c) and it was "
            "pleasing to see tenacity in some response where candidates had inadvertently opted for less efficient "
            "approaches but had persevered nonetheless to obtain the required results.", NO),
    ],
}

# Ref marks for sentences whose source lines above end without one: (question, sentence index) -> option.
# Each was checked: "those"/"it"/"such"/"this" here doesn't point back, except where BACK is given.
LATE_REFS = {
    ("01", 5): NO, ("05", 6): BACK, ("06", 5): NO, ("06", 9): NO, ("06", 13): NO, ("06", 15): NO, ("06", 16): NO,
    ("07", 11): NO, ("08", 4): NO, ("09", 0): NO, ("10", 5): NO, ("10", 10): NO, ("10", 13): NO, ("10", 25): NO,
    ("11", 1): NO, ("14", 9): NO, ("16", 21): NO, ("16", 25): NO, ("16", 32): NO,
}
for (q, i), option in LATE_REFS.items():
    REPORT[q][i] = (*REPORT[q][i][:2], option)

RATINGS = {
    "01": ("medium", ("01", 1)),
    "02a": ("easy", ("02", 1)),
    "02b": ("easy", ("02", 8)),
    "03a": ("easy", ("03", 2)),
    "03b": ("medium", ("03", 1)),
    "04": ("easy", ("04", 1)),
    "05a": ("easy", ("05", 1)),
    "05b": ("hard", ("05", 20)),
    "06a": ("medium", ("06", 1)),
    "06b": ("hard", ("06", 10)),
    "06c": ("medium", ("06", 14)),
    "07a": ("easy", ("07", 0)),
    "07b": ("hard", ("07", 8)),
    "08": ("medium", ("08", 6)),
    "09a": ("hard", ("09", 0)),
    "09b": ("hard", ("09", 14)),
    "10a": ("easy", ("10", 3)),
    "10b": ("easy", ("10", 7)),
    "10c": ("hard", ("10", 13)),
    "10d": ("hard", ("10", 18)),
    "11": ("medium", ("11", 1)),
    "12a": ("easy", ("12", 0)),
    "12b": ("medium", ("12", 11)),
    "13a": ("medium", ("13", 14)),
    "13b": ("hard", ("13", 16)),
    "14a": ("easy", ("14", 0)),
    "14b": ("hard", ("14", 9)),
    "14c": ("hard", ("14", 13)),
    "15a": ("easy", ("15", 2)),
    "15b": ("medium", ("15", 7)),
    "15c": ("medium", ("15", 15)),
    "16a": ("medium", ("16", 4)),
    "16b": ("medium", ("16", 15)),
    "16c": ("hard", ("16", 23)),
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
