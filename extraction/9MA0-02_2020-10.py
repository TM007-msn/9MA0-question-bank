"""Draft builder for 9MA0-02 2020-10 (A level Pure Paper 2, October 2020).

Run (from the project root, with the venv active):
    python extraction/9MA0-02_2020-10.py        # writes out/drafts/9MA0-02_2020-10.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-02_2020-10.json

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

P, S = "9MA0-02", "2020-10"
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
    """A vector arrow over two letters, e.g. V("PQ")."""
    return r"\overrightarrow{" + x + "}"


p_, q_, r_ = r"\mathbf{p}", r"\mathbf{q}", r"\mathbf{r}"
CALC = ["In this question you must show all stages of your working.",
        "Solutions relying entirely on calculator technology are not acceptable."]

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q1 = [r"The table below shows corresponding values of $x$ and $y$ for $y=\sqrt{\frac{x}{1+x}}$",
      r"The values of $y$ are given to 4 significant figures.",
      r"$$\begin{array}{|c|c|c|c|c|c|}\hline x&0.5&1&1.5&2&2.5\\\hline y&0.5774&0.7071&0.7746&0.8165&0.8452\\"
      r"\hline\end{array}$$"]
Q1A = [r"Use the trapezium rule, with all the values of $y$ in the table, to find an estimate for",
       r"$$\int_{0.5}^{2.5}\sqrt{\frac{x}{1+x}}\,\mathrm{d}x$$",
       "giving your answer to 3 significant figures."]
Q1B = (r"(b) Using your answer to part (a), deduce an estimate for $\displaystyle\int_{0.5}^{2.5}\sqrt{\frac{9x}{1+x}}"
       r"\,\mathrm{d}x$")
Q3A = ["Given that", r"$$2\log(4-x)=\log(x+8)$$", "show that", r"$$x^2-9x+8=0$$"]
Q6A = ["Given that",
       r"$$\frac{x^2+8x-3}{x+2}\equiv Ax+B+\frac{C}{x+2}\qquad x\in\mathbb{R}\ \ x\neq-2$$",
       r"find the values of the constants $A$, $B$ and $C$"]
Q7 = [r"[Figure 1: the curve $C$ for $x>0$: it comes down steeply from high up beside the positive $y$-axis to a "
      r"minimum point $P$ in the first quadrant, then rises steadily to the top right; the whole curve lies above the "
      r"$x$-axis.]",
      r"Figure 1 shows a sketch of the curve $C$ with equation",
      r"$$y=\frac{4x^2+x}{2\sqrt{x}}-4\ln x\qquad x>0$$"]
Q7A = ["Show that", r"$$\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{12x^2+x-16\sqrt{x}}{4x\sqrt{x}}$$"]
Q7P = r"The point $P$, shown in Figure 1, is the minimum turning point on $C$."
Q9 = ["A quantity of ethanol was heated until it reached boiling point.",
      r"The temperature of the ethanol, $\theta^\circ$C, at time $t$ seconds after heating began, is modelled by the "
      r"equation",
      r"$$\theta=A-B\mathrm{e}^{-0.07t}$$",
      r"where $A$ and $B$ are positive constants.",
      "Given that",
      r"• the initial temperature of the ethanol was $18^\circ$C",
      r"• after 10 seconds the temperature of the ethanol was $44^\circ$C"]
Q10A = ["Show that", r"$$\cos3A\equiv4\cos^3A-3\cos A$$"]
Q11 = [r"[Figure 2: a V-shaped graph with its vertex $P$ below the $x$-axis, to the left of the $y$-axis; the left "
       r"branch crosses the negative $x$-axis and rises to the top left; the right branch crosses the negative "
       r"$x$-axis, then the positive $y$-axis, and rises to the top right.]",
       "Figure 2 shows a sketch of the graph with equation",
       r"$$y=2\left|x+4\right|-5$$",
       r"The vertex of the graph is at the point $P$, shown in Figure 2."]
Q12 = [r"[Figure 3: a curve starting at $O$, rising to a maximum and then falling steeply to meet the positive "
       r"$x$-axis; the region $R$ between the curve and the $x$-axis is shaded.]",
       "The curve shown in Figure 3 has parametric equations",
       r"$$x=6\sin t\qquad y=5\sin2t\qquad0\leqslant t\leqslant\frac{\pi}{2}$$",
       r"The region $R$, shown shaded in Figure 3, is bounded by the curve and the $x$-axis."]
Q12AI = (r"Show that the area of $R$ is given by $\displaystyle\int_0^{\frac{\pi}{2}}60\sin t\cos^2t\,"
         r"\mathrm{d}t$")
Q13 = ["The function g is defined by",
       r"$$\mathrm{g}(x)=\frac{3\ln(x)-7}{\ln(x)-2}\qquad x>0\qquad x\neq k$$",
       r"where $k$ is a constant."]
Q14 = [r"A circle $C$ with radius $r$",
       "• lies only in the 1st quadrant",
       r"• touches the $x$-axis and touches the $y$-axis",
       r"The line $l$ has equation $2x+y=12$"]
Q14A = [r"Show that the $x$ coordinates of the points of intersection of $l$ with $C$ satisfy",
        r"$$5x^2+(2r-48)x+(r^2-24r+144)=0$$"]
Q15 = [*CALC, r"A geometric series has common ratio $r$ and first term $a$.", r"Given $r\neq1$ and $a\neq0$"]
Q15A = ["prove that", r"$$S_n=\frac{a(1-r^n)}{1-r}$$"]

LATEX = {
    "01a": L(*Q1, *Q1A),
    "01b": L(*Q1, "(a) " + Q1A[0], *Q1A[1:], Q1B),
    "01c": L(*Q1, "(a) " + Q1A[0], *Q1A[1:], Q1B, "Given that",
             r"$$\int_{0.5}^{2.5}\sqrt{\frac{9x}{1+x}}\,\mathrm{d}x=4.535\ \text{ to 4 significant figures}$$",
             "(c) comment on the accuracy of your answer to part (b)."),
    "02": L(r"Relative to a fixed origin, points $P$, $Q$ and $R$ have position vectors $" + p_ + "$, $" + q_
            + "$ and $" + r_ + "$ respectively.",
            "Given that",
            r"• $P$, $Q$ and $R$ lie on a straight line",
            r"• $Q$ lies one third of the way from $P$ to $R$",
            "show that",
            r"$$" + q_ + r"=\frac{1}{3}(" + r_ + "+2" + p_ + ")$$"),
    "03a": L(*Q3A),
    "03b": L("(i) Write down the roots of the equation", r"$$x^2-9x+8=0$$",
             r"(ii) State which of the roots in (b)(i) is $\textbf{not}$ a solution of", r"$$2\log(4-x)=\log(x+8)$$",
             "giving a reason for your answer."),
    "04": L("In the binomial expansion of", r"$$(a+2x)^7\qquad\text{where }a\text{ is a constant}$$",
            r"the coefficient of $x^4$ is $15\,120$", r"Find the value of $a$."),
    "05": L(r"The curve with equation $y=3\times2^x$ meets the curve with equation $y=15-2^{x+1}$ at the point $P$.",
            r"Find, using algebra, the exact $x$ coordinate of $P$."),
    "06a": L(*Q6A),
    "06b": L("(a) " + Q6A[0], *Q6A[1:], "(b) Hence, using algebraic integration, find the exact value of",
             r"$$\int_0^6\frac{x^2+8x-3}{x+2}\,\mathrm{d}x$$",
             r"giving your answer in the form $a+b\ln2$ where $a$ and $b$ are integers to be found."),
    "07a": L(*Q7, *Q7A),
    "07b": L(*Q7, "(a) " + Q7A[0], Q7A[1], Q7P, "(b) Show that the $x$ coordinate of $P$ is a solution of",
             r"$$x=\left(\frac{4}{3}-\frac{\sqrt{x}}{12}\right)^{\frac{2}{3}}$$"),
    "07c": L(*Q7, Q7P, "Use the iteration formula",
             r"$$x_{n+1}=\left(\frac{4}{3}-\frac{\sqrt{x_n}}{12}\right)^{\frac{2}{3}}\qquad\text{with }x_1=2$$",
             r"to find (i) the value of $x_2$ to 5 decimal places,",
             r"(ii) the $x$ coordinate of $P$ to 5 decimal places."),
    "08": L(r"A curve $C$ has equation $y=\mathrm{f}(x)$", "Given that",
            r"• $\mathrm{f}'(x)=6x^2+ax-23$ where $a$ is a constant",
            r"• the $y$ intercept of $C$ is $-12$",
            r"• $(x+4)$ is a factor of $\mathrm{f}(x)$",
            r"find, in simplest form, $\mathrm{f}(x)$"),
    "09a": L(*Q9, r"find a complete equation for the model, giving the values of $A$ and $B$ to 3 significant figures."),
    "09b": L(*Q9, r"Ethanol has a boiling point of approximately $78^\circ$C", "Use this information to evaluate the model."),
    "10a": L(*CALC, *Q10A),
    "10b": L(*CALC, "(a) " + Q10A[0], Q10A[1],
             r"(b) Hence solve, for $-90^\circ\leqslant x\leqslant180^\circ$, the equation", r"$$1-\cos3x=\sin^2x$$"),
    "11a": L(*Q11, r"Find the coordinates of $P$."),
    "11b": L(*Q11, "Solve the equation", r"$$3x+40=2\left|x+4\right|-5$$"),
    "11c": L(*Q11, r"A line $l$ has equation $y=ax$, where $a$ is a constant.",
             r"Given that $l$ intersects $y=2\left|x+4\right|-5$ at least once,",
             r"find the range of possible values of $a$, writing your answer in set notation."),
    "12ai": L(*Q12, Q12AI),
    "12aii": L(*Q12, "(a) (i) " + Q12AI, r"(ii) Hence show, by algebraic integration, that the area of $R$ is exactly 20"),
    "12b": L(*Q12,
             r"[Figure 4: the same curve, drawn dashed where it is not part of the dam; the dam, shaded, is bounded by "
             r"the curve from $O$ up to the point $M$, a horizontal top from $M$ across to the point $N$ on the "
             r"curve, a vertical wall from $N$ down to the $x$-axis, marked 4.2, and the $x$-axis; the dashed curve "
             r"rises above $MN$ between $M$ and $N$ and meets the $x$-axis just beyond the wall.]",
             "Part of the curve is used to model the profile of a small dam, shown shaded in Figure 4.",
             "Using the model and given that",
             r"• $x$ and $y$ are in metres",
             "• the vertical wall of the dam is 4.2 metres high",
             r"• there is a horizontal walkway of width $MN$ along the top of the dam",
             "calculate the width of the walkway."),
    "13a": L(*Q13, r"Deduce the value of $k$."),
    "13b": L(*Q13, "Prove that", r"$$\mathrm{g}'(x)>0$$", r"for all values of $x$ in the domain of g."),
    "13c": L(*Q13, r"Find the range of values of $a$ for which", r"$$\mathrm{g}(a)>0$$"),
    "14a": L(*Q14, *Q14A),
    "14b": L(*Q14, "(a) " + Q14A[0], Q14A[1], r"Given also that $l$ is a tangent to $C$,",
             r"(b) find the two possible values of $r$, giving your answers as fully simplified surds."),
    "15a": L(*Q15, *Q15A),
    "15b": L(*Q15, "(a) " + Q15A[0], Q15A[1], r"Given also that $S_{10}$ is four times $S_5$",
             r"(b) find the exact value of $r$."),
    "16": L(r"Use algebra to prove that the square of any natural number is $\textbf{either}$ a multiple of 3 "
            r"$\textbf{or}$ one more than a multiple of 3"),
}

Y = r"0.5774+0.8452+2(0.7071+0.7746+0.8165)"
Q5LOGS = (r"Uses logs correctly and proceeds to a value for $x$ from an equation of the form $2^x=k$ where $k>1$ e.g. "
          r"$2^x=k\Rightarrow x=\log_2k$ $\textbf{or}$ $2^x=k\Rightarrow\log2^x=\log k\Rightarrow x\log2=\log k"
          r"\Rightarrow x=\ldots$ $\textbf{or}$ $2^x=k\Rightarrow\ln2^x=\ln k\Rightarrow x\ln2=\ln k\Rightarrow "
          r"x=\ldots$ $\textbf{Depends on the first method mark}$ $\textbf{This may be implied if they go straight to "
          r"decimals e.g.}$ $2^x=3$ $\textbf{so}$ $x=1.584..$ $\textbf{but you may need to check}$")
Q5ANS = (r"$x=\log_23$. Notes: $x=\log_23$ or $\frac{\log3}{\log2}$ or $\frac{\ln3}{\ln2}$ Ignore any attempts to "
         r"find the $y$-coordinate")
DEG = r"(^\circ\text{C})"
FOURSOL = r"$-90^\circ, 0, 90^\circ$, awrt $139^\circ$"
H12 = r"\mathrm{d}t"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", NUM, "9.4", 3, LATEX["01a"],
      [r"B1 (AO 1.1a): $h=0.5$. Notes: States or uses $h=0.5$. May be implied by $\frac{1}{4}\times\{\ldots$ below.",
       r"M1 (AO 1.1b): $A\approx\frac{0.5}{2}\{" + Y + r"\}$. Notes: Correct attempt at the trapezium rule. Look for "
       r"$\frac{1}{2}h\times\{" + Y + r"\}$ condoning slips on the terms but must use all $y$ values with no repeats. "
       r"There must be a clear attempt at $\frac{1}{2}h\times$(first $y$ + last $y$ + $2\times$“sum of the rest”) Give "
       r"M0 for $\frac{1}{2}\times\frac{1}{2}" + Y + r"$ unless the missing brackets are implied. NB this incorrect "
       r"method gives 5.85… May be awarded for separate trapezia e.g. $\frac{1}{4}(0.5774+0.7071)+\frac{1}{4}"
       r"(0.7071+0.7746)+\frac{1}{4}(0.7746+0.8165)+\frac{1}{4}(0.8165+0.8452)$ May be awarded for using the function "
       r"e.g. $\frac{1}{2}h\times\left\{\sqrt{\frac{0.5}{1+0.5}}+\sqrt{\frac{2.5}{1+2.5}}+2\left(\sqrt{\frac{1}{1+1}}"
       r"+\sqrt{\frac{1.5}{1+1.5}}+\sqrt{\frac{2}{1+2}}\right)\right\}$",
       r"A1 (AO 1.1b): $=$ awrt 1.50 $\textbf{For reference: The integration on a calculator gives 1.511549071 The "
       r"full accuracy for}$ $y$ $\textbf{values gives 1.504726147 The accuracy from the table gives 1.50475}$. Notes: "
       r"Awrt 1.50 (Apply isw if necessary) $\textbf{Correct answers with no working}$ – send to review"],
      False, 2),
    e("01b", "1(b)", NUM, "9.4", 1, LATEX["01b"],
      [r"B1ft (AO 2.2a): $3\times$ their (a) If (a) is correct, allow awrt 4.50 or awrt 4.51 even with no working. "
       r"Only allow 4.5 if (a) is correct and working is shown e.g. $3\times1.5$ If (a) is incorrect allow $3\times$ "
       r"their (a) given to at least 3sf but do not be too concerned about the accuracy (as they may use rounded or "
       r"rounded value from (a)) $\textbf{For reference the integration on a calculator gives 4.534647213}$. Notes: "
       r"See main scheme. Must be considering $3\times$(a) and not e.g. attempting trapezium rule again."],
      False, 2),
    e("01c", "1(c)", NUM, "9.4", 1, LATEX["01c"],
      [r"B1 (AO 3.2b): $\underline{\textbf{This mark depends on the B1 having been awarded in part (b) with awrt "
       r"4.5}}$ Look for a sensible comment. Some examples: • The answer is accurate to 2 sf or one decimal place • "
       r"Answer to (b) is accurate as $4.535\approx4.50$ • Very accurate as 4.535 to 2 sf is 4.5 • $4.51425<4.535$ so "
       r"my answer is underestimate but not too far off • It is an underestimate but quite close • It is a very good "
       r"estimate • High accuracy • (Quite) accurate • It is less than 1% out • $4.535-4.5=0.035$ so not far out But "
       r"$\textbf{not}$ just “it is an underestimate” or Calculates percentage error correctly using awrt 4.50 or awrt "
       r"4.51 or 4.5 (No comment is necessary in these cases although one may be given) Examples: "
       r"$\left|\frac{4.535-4.50}{4.535}\right|\times100=0.77\%$ or $\left|\frac{4.535-4.51}{4.535}\right|\times100="
       r"0.55\%$ or $\left|\frac{4.535-4.51425}{4.535}\right|\times100=0.46\%$ or $\left|\frac{4.50}{4.535}\right|"
       r"\times100=99\%$ In these cases don’t be too concerned about accuracy e.g. allow 1sf. $\textbf{This mark should "
       r"be withheld if there are any contradictory statements}$. Notes: See scheme"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02", "2", VEC, "10.3, 10.4", 3, LATEX["02"],
      [r"M1 (AO 1.1b): Attempts any one of $(\pm" + V("PQ") + r"=)\pm(" + q_ + "-" + p_ + r")$, $(\pm" + V("PR")
       + r"=)\pm(" + r_ + "-" + p_ + r")$, $(\pm" + V("QR") + r"=)\pm(" + r_ + "-" + q_ + r")$ Or e.g. $(\pm"
       + V("PQ") + r"=)\pm(" + V("OQ") + "-" + V("OP") + r")$, $(\pm" + V("PR") + r"=)\pm(" + V("OR") + "-" + V("OP")
       + r")$, $(\pm" + V("QR") + r"=)\pm(" + V("OR") + "-" + V("OQ") + r")$. Notes: Attempts any of the relevant "
       r"vectors by subtracting either way around. This may be implied by sight of any one of $\pm(" + q_ + "-" + p_
       + r"), \pm(" + r_ + "-" + p_ + r"), \pm(" + r_ + "-" + q_ + r")$ ignoring how they are labelled In the working "
       r"allow use of P instead of $" + p_ + "$ and Q instead of $" + q_ + "$ as long as the intention is clear.",
       r"dM1 (AO 3.1a): Attempts e.g. $" + r_ + "-" + q_ + "=2(" + q_ + "-" + p_ + ")$ $" + r_ + "-" + p_ + "=3(" + q_
       + "-" + p_ + r")$ $\frac{2}{3}(" + q_ + "-" + p_ + r")=\frac{1}{3}(" + r_ + "-" + q_ + ")$ $" + q_ + "=" + p_
       + r"+\frac{1}{3}(" + r_ + "-" + p_ + ")$ $" + q_ + "=" + r_ + r"+\frac{2}{3}(" + p_ + "-" + r_ + r")$. Notes: "
       r"Uses the given information and writes it correctly in vector form that if rearranged would give the printed "
       r"answer",
       r"A1* (AO 2.1): E.g. $\Rightarrow" + r_ + "-" + q_ + "=2" + q_ + "-2" + p_ + r"\Rightarrow2" + p_ + "+" + r_
       + "=3" + q_ + r"\Rightarrow" + q_ + r"=\frac{1}{3}(" + r_ + "+2" + p_ + r")$ *. Notes: Fully correct work "
       r"leading to the given answer. Allow OQ = … as long as OQ has been defined as $" + q_ + "$ earlier."],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", EXP, "6.4", 3, LATEX["03a"],
      [r"B1 (AO 1.2): $2\log(4-x)=\log(4-x)^2$. Notes: States or uses $2\log(4-x)=\log(4-x)^2$",
       r"M1 (AO 1.1b): $2\log(4-x)=\log(x+8)\Rightarrow\log(4-x)^2=\log(x+8)$ $(4-x)^2=(x+8)$ $\textbf{or}$ "
       r"$2\log(4-x)=\log(x+8)\Rightarrow\log(4-x)^2-\log(x+8)=0$ $\frac{(4-x)^2}{(x+8)}=1$. Notes: Correct attempt at "
       r"eliminating the logs to form a quadratic equation in $x$. Note that this may be implied by e.g. "
       r"$\log\frac{(4-x)^2}{(x+8)}=0\Rightarrow(4-x)^2=x+8$",
       r"A1* (AO 2.1): $16-8x+x^2=x+8\Rightarrow x^2-9x+8=0$ *. Notes: Proceeds to the given answer with at least one "
       r"line where the $(4-x)^2$ has been multiplied out. There must be no errors or omissions but condone invisible "
       r"brackets around the arguments of the logs e.g. allow $\log16-8x+x^2$ for $\log(16-8x+x^2)$ and $\log x+8$ for "
       r"$\log(x+8)$ Note we will allow a start of $(4-x)^2=x+8$ with no previous work for full marks. "
       r"$\underline{\textbf{Some examples of how to mark (a) in particular cases:}}$ [first example box, cut off at "
       r"the foot of the page: $2\log(4-x)=\log(x+8)\Rightarrow\log(4-x)^2=\log(x+8)\Rightarrow\frac{\log(4-x)^2}"
       r"{\log(x+8)}=1$ followed by a line beginning $\frac{(4-x)^2}{\ldots}$; the rest of the box, including its score, "
       r"is not printed] $2\log(4-x)=\log(x+8)\Rightarrow\log(4-x)^2-\log(x+8)=0\Rightarrow(4-x)^2-x-8=0$ "
       r"$\Rightarrow16-8x+x^2-x-8\Rightarrow x^2-9x+8=0$ $\textbf{Scores B1M1A1}$ "
       r"$2\log(4-x)=\log(x+8)\Rightarrow\log(4-x)^2-\log(x+8)=0\Rightarrow\frac{\log(4-x)^2}{\log(x+8)}=0$ "
       r"$\Rightarrow\frac{(4-x)^2}{(x+8)}=1\Rightarrow16-8x+x^2=x+8\Rightarrow x^2-9x+8=0$ $\textbf{Scores B1M0A0}$",
       r"ALT: (a) Alternative - working backwards — B1 (AO 1.2): $x^2-9x+8=0\Rightarrow(4-x)^2-x-8=0$. Notes: Writes "
       r"$x^2-9x+8=0$ as $(4-x)^2-x-8=0$ or equivalent",
       r"ALT: (a) Alternative - working backwards — M1 (AO 1.1b): $\Rightarrow(4-x)^2=x+8$ $\Rightarrow\log(4-x)^2="
       r"\log(x+8)$. Notes: Proceeds correctly to reach $\log(4-x)^2=\log(x+8)$",
       r"ALT: (a) Alternative - working backwards — A1 (AO 2.1): $\Rightarrow2\log(4-x)=\log(x+8)$ * Hence proved. "
       r"Notes: Obtains $2\log(4-x)=\log(x+8)$ and makes a (minimal) conclusion e.g. hence proved, QED, #, square "
       r"etc."],
      False, 6),
    e("03b", "3(b)", EXP, "6.3, 2.3", 2, LATEX["03b"],
      [r"B1 (AO 1.1b): (i) $(x=)$ 1, 8. Notes: Writes down $(x=)$ 1, 8",
       r"B1 (AO 2.3): (ii) 8 is $\textbf{not}$ a solution as $\log(4-8)$ cannot be found. Notes: Chooses 8 (no follow "
       r"through here) and gives a reason why it should be rejected by referring to logs and which log it is. They "
       r"must refer to the 8 as the required value but allow e.g. $x\neq8$ and there must be a reference to "
       r"$\log(4-x)$ or log of lhs or $\log(-4)$ or the $4-8$. Some acceptable reasons are: $\log(-4)$ can’t be "
       r"found/worked out/is undefined, $\log(-4)$ gives math error, $\log(-4)=$ n/a, lhs is log(negative) so reject, "
       r"you can’t do the log of a negative number which would happen with $4-8$ Do $\textbf{not}$ allow “you can’t "
       r"have a negative log” unless this is clarified further and do $\textbf{not}$ allow “you get a math error” in "
       r"isolation $\textbf{There must be no contradictory statements.}$ Note that this is an independent mark but "
       r"must have $x=8$ (i.e. may have solved to get $x=-1, 8$ for first B mark)"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04", "4", SEQ, "4.1", 3, LATEX["04"],
      [r"M1 (AO 1.1b): ${}^7\mathrm{C}_4a^3(2x)^4$. Notes: For an attempt at the correct coefficient of $x^4$. The "
       r"coefficient must have • the correct binomial coefficient • the correct power of $a$ • 2 or $2^4$ (may be "
       r"implied) May be seen within a full or partial expansion. Accept ${}^7\mathrm{C}_4a^3(2x)^4$, "
       r"$\frac{7!}{4!3!}a^3(2x)^4$, $\binom{7}{4}a^3(2x)^4$, $35a^3(2x)^4$, $560a^3x^4$, $\binom{7}{4}a^316x^4$ etc. "
       r"or ${}^7\mathrm{C}_4a^32^4$, $\frac{7!}{4!3!}a^32^4$, $\binom{7}{4}a^32^4$, $35a^32^4$, $560a^3$ etc. or "
       r"${}^7\mathrm{C}_3a^3(2x)^4$, $\frac{7!}{4!3!}a^3(2x)^4$, $\binom{7}{3}a^3(2x)^4$, $35a^3(2x)^4$, $560a^3x^4$, "
       r"$\binom{7}{3}a^316x^4$ etc. or ${}^7\mathrm{C}_3a^32^4$, $\frac{7!}{4!3!}a^32^4$, $\binom{7}{3}a^32^4$, "
       r"$35a^32^4$, $560a^3$ You can condone missing brackets around the “$2x$” so allow e.g. "
       r"$\frac{7!}{4!3!}a^32x^4$ An alternative is to attempt to expand $a^7\left(1+\frac{2x}{a}\right)^7$ to give "
       r"$a^7\left(\ldots\frac{7\times6\times5\times4}{4!}\left(\frac{2x}{a}\right)^4\ldots\right)$ Allow M1 for e.g. "
       r"$a^7\left(\ldots\frac{7\times6\times5\times4}{4!}\left(\frac{2x}{a}\right)^4\ldots\right)$, "
       r"$a^7\left(\ldots\binom{7}{4}\left(\frac{2x}{a}\right)^4\ldots\right)$, $a^7\left(\ldots35\left(\frac{2x}{a}"
       r"\right)^4\ldots\right)$ etc. but condone missing brackets around the $\frac{2x}{a}$ Note that "
       r"${}^7\mathrm{C}_3$, $\binom{7}{3}$ etc. are equivalent to ${}^7\mathrm{C}_4$, $\binom{7}{4}$ etc. and are "
       r"equally acceptable. If the candidate attempts $(a+2x)(a+2x)(a+2x)\ldots$ etc. then it must be a complete "
       r"method to reach the required term. Send to review if necessary.",
       r"dM1 (AO 2.1): $\frac{7!}{4!3!}a^3\times2^4=15120\Rightarrow a=\ldots$. Notes: For $\text{“}560\text{”}a^3="
       r"15120\Rightarrow a=\ldots$ Condone slips on copying the 15120 but their “560” must be an attempt at "
       r"${}^7\mathrm{C}_4\times2$ or ${}^7\mathrm{C}_4\times2^4$ and must be attempting the $\underline{\text{cube "
       r"root}}$ of $\frac{15120}{\text{“}560\text{”}}$. $\textbf{Depends on the first mark.}$",
       r"A1 (AO 1.1b): $a=3$. Notes: $a=3$ and no other values i.e. $\pm3$ scores A0 $\textbf{Note that this is fairly "
       r"common:}$ ${}^7\mathrm{C}_4a^32x^4=70a^3x^4\Rightarrow70a^3=15120\Rightarrow a^3=216\Rightarrow a=6$ "
       r"$\textbf{and scores M1 dM1 A0}$"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05", "5", EXP, "6.5, 2.1", 4, LATEX["05"],
      [r"B1 (AO 1.1b): $15-2^{x+1}=3\times2^x$. Notes: Combines the equations to reach $15-2^{x+1}=3\times2^x$ or "
       r"equivalent e.g. $15-2^{x+1}-3\times2^x=0$",
       r"M1 (AO 1.1b): $\Rightarrow15-2\times2^x=3\times2^x\Rightarrow2^x=3$ or e.g. $\Rightarrow\frac{15}{2^x}-2=3"
       r"\Rightarrow2^x=3$. Notes: Uses $2^{x+1}=2\times2^x$ oe e.g. $\frac{2^{x+1}}{2^x}=2$ to obtain an equation in "
       r"$2^x$ and attempts to make $2^x$ the subject. See scheme but e.g. $y=2^x\Rightarrow3\times2^x=15-2^{x+1}"
       r"\Rightarrow3y=15-2y\Rightarrow y=\ldots$ is also possible",
       r"dM1 (AO 1.1b): $2^x=3\Rightarrow x=\ldots$. Notes: " + Q5LOGS,
       r"A1cso (AO 1.1b): " + Q5ANS,
       r"ALT: Alternative — B1 (AO 1.1b): $y=3\times2^x\Rightarrow2^x=\frac{y}{3}\Rightarrow y=15-2\times\frac{y}{3}$. "
       r"Notes: Correct equation in $y$",
       r"ALT: Alternative — M1 (AO 1.1b): $3y+2y=45\Rightarrow y=9\Rightarrow3\times2^x=9\Rightarrow2^x=3$. Notes: "
       r"Solves their equation in $y$ and attempts to make $2^x$ the subject.",
       r"ALT: Alternative — dM1 (AO 1.1b): $2^x=3\Rightarrow x=\ldots$. Notes: " + Q5LOGS,
       r"ALT: Alternative — A1cso (AO 1.1b): " + Q5ANS],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", ALG, "2.6, 2.10", 3, LATEX["06a"],
      [r"M1 (AO 1.1b): $x^2+8x-3=(Ax+B)(x+2)+C$ or $Ax(x+2)+B(x+2)+C$ $\Rightarrow A=\ldots, B=\ldots, C=\ldots$ "
       r"$\textbf{or}$ [long division of $x^2+8x-3$ by $x+2$: quotient $x+6$; $x^2+2x$; $6x-3$; $6x+12$; remainder "
       r"$-15$]. Notes: Multiplies by $(x+2)$ and attempts to find values for $A$, $B$ and $C$ e.g. by comparing "
       r"coefficients or substituting values for $x$. If the method is unclear, at least 2 terms must be correct on "
       r"rhs. $\textbf{Or}$ attempts to divide $x^2+8x-3$ by $x+2$ and obtains a linear quotient and a constant "
       r"remainder. This mark may be implied by 2 correct values for $A$, $B$ or $C$",
       r"A1 (AO 1.1b): Two of $A=1, B=6, C=-15$. Notes: Two of $A=1$, $B=6$, $C=-15$. But note that "
       r"$\underline{\textbf{just}}$ performing the division correctly is insufficient and they must clearly identify "
       r"their $A$, $B$, $C$ to score any accuracy marks.",
       r"A1 (AO 1.1b): All three of $A=1, B=6, C=-15$. Notes: All three of $A=1$, $B=6$, $C=-15$ This is implied by "
       r"stating $\frac{x^2+8x-3}{x+2}=x+6-\frac{15}{x+2}$ or within the integral in (b)"],
      False, 12),
    e("06b", "6(b)", INT, "8.2, 8.3, 6.4", 4, LATEX["06b"],
      [r"M1 (AO 1.1b): $\int\frac{x^2+8x-3}{x+2}\,\mathrm{d}x=\int x+6-\frac{15}{x+2}\,\mathrm{d}x=\ldots-15\ln(x+2)$. "
       r"Notes: Integrates an expression of the form $\frac{C}{x+2}$ to obtain $k\ln(x+2)$. Condone the omission of "
       r"brackets around the “$x+2$”",
       r"A1ft (AO 1.1b): $=\frac{1}{2}x^2+6x-15\ln(x+2)\quad(+c)$. Notes: Correct integration ft on their "
       r"$Ax+B+\frac{C}{x+2}$, $(A,B,C\neq0)$ The brackets should be present around the “$x+2$” unless they are "
       r"implied by subsequent work.",
       r"M1 (AO 2.1): $\int_0^6\frac{x^2+8x-3}{x+2}\,\mathrm{d}x=\left[\frac{1}{2}x^2+6x-15\ln(x+2)\right]_0^6$ "
       r"$=(18+36-15\ln8)-(0+0-15\ln2)$ $=18+36-(15-45)\ln2$ or e.g. $18+36+15\ln\left(\frac{2}{8}\right)$. Notes: "
       r"Substitutes both limits 0 and 6 into an expression that contains an $x$ or $x^2$ term or both and a ln term "
       r"and subtracts either way round $\textbf{WITH}$ fully correct log work to combine two log terms (but allow sign "
       r"errors when removing brackets) leading to an answer of the form $a+b\ln c$ ($a$, $b$ and $c$ not necessarily "
       r"integers) e.g. if they expand to get $-15\ln8-15\ln2$ followed by $-15\ln16$ and reach $a+b\ln c$ then allow "
       r"the M mark",
       r"A1 (AO 1.1b): $=54-30\ln2$. Notes: $54-30\ln2$ (Apply isw once a correct answer is seen)"],
      False, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", DIFF, "7.4, 7.2", 4, LATEX["07a"],
      [r"B1 (AO 1.1a): $\ln x\to\frac{1}{x}$. Notes: Differentiates $\ln x\to\frac{1}{x}$ seen or implied",
       r"M1 (AO 1.1b): Method to differentiate $\frac{4x^2+x}{2\sqrt{x}}$ – see notes. Notes: Correct method to "
       r"differentiate $\frac{4x^2+x}{2\sqrt{x}}$: Look for $\frac{4x^2+x}{2\sqrt{x}}\to\ldots x^{\frac{3}{2}}+\ldots "
       r"x^{\frac{1}{2}}$ being then differentiated to $Px^{\frac{1}{2}}+\ldots$ $\textbf{or}$ $\ldots+Qx^{-\frac{1}{2}}$ "
       r"Alternatively uses the quotient rule on $\frac{4x^2+x}{2\sqrt{x}}$. Condone slips but if rule is not quoted "
       r"expect $\left(\frac{\mathrm{d}y}{\mathrm{d}x}\right)=\frac{2\sqrt{x}(Ax+B)-(4x^2+x)Cx^{-\frac{1}{2}}}"
       r"{(2\sqrt{x})^2}$ $(A,B,C>0)$ $\textbf{But a correct rule may be implied by their}$ $u$, $v$, $u'$, $v'$ "
       r"$\textbf{followed by applying}$ $\frac{vu'-uv'}{v^2}$ $\textbf{etc.}$ Alternatively uses the product rule on "
       r"$(4x^2+x)(2\sqrt{x})^{-1}$ Condone slips but expect $\left(\frac{\mathrm{d}y}{\mathrm{d}x}\right)="
       r"Ax^{-\frac{1}{2}}(Bx+C)+D(4x^2+x)x^{-\frac{3}{2}}$ $(A,B,C>0)$ $\textbf{In general condone missing brackets "
       r"for the M mark. If they quote}$ $u=4x^2+x$ $\textbf{and}$ $v=2\sqrt{x}$ $\textbf{and don’t make the "
       r"differentiation easier, they can be awarded this mark for applying the correct rule. Also allow this mark if "
       r"they quote the correct quotient rule but only have}$ $v$ $\textbf{rather than}$ $v^2$ $\textbf{in the "
       r"denominator.}$",
       r"A1 (AO 1.1b): E.g. $2\times\frac{3}{2}x^{\frac{1}{2}}+\frac{1}{2}\times\frac{1}{2}x^{-\frac{1}{2}}$. Notes: "
       r"Correct differentiation of $\frac{4x^2+x}{2\sqrt{x}}$ although may not be simplified. Examples: "
       r"$\left(\frac{\mathrm{d}y}{\mathrm{d}x}\right)=\frac{2\sqrt{x}(8x+1)-(4x^2+x)x^{-\frac{1}{2}}}{(2\sqrt{x})^2}$, "
       r"$\frac{1}{2}x^{-\frac{1}{2}}(8x+1)-\frac{1}{4}(4x^2+x)x^{-\frac{3}{2}}$, $2\times\frac{3}{2}x^{\frac{1}{2}}+"
       r"\frac{1}{2}\times\frac{1}{2}x^{-\frac{1}{2}}$",
       r"A1* (AO 2.1): $\frac{\mathrm{d}y}{\mathrm{d}x}=3\sqrt{x}+\frac{1}{4\sqrt{x}}-\frac{4}{x}=\frac{12x^2+x-16"
       r"\sqrt{x}}{4x\sqrt{x}}$ *. Notes: Obtains $\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{12x^2+x-16\sqrt{x}}"
       r"{4x\sqrt{x}}$ via $3\sqrt{x}+\frac{1}{4\sqrt{x}}-\frac{4}{x}$ or a correct application of the quotient or "
       r"product rule and with sufficient working shown to reach the printed answer. $\underline{\textbf{There must be "
       r"no errors e.g. missing brackets.}}$"],
      True, 16),
    e("07b", "7(b)", DIFF, "7.3, 2.1", 3, LATEX["07b"],
      [r"M1 (AO 1.1b): $12x^2+x-16\sqrt{x}=0\Rightarrow12x^{\frac{3}{2}}+x^{\frac{1}{2}}-16=0$. Notes: Sets "
       r"$12x^2+x-16\sqrt{x}=0$ and divides by $\sqrt{x}$ or equivalent e.g. divides by $x$ and multiplies by "
       r"$\sqrt{x}$",
       r"dM1 (AO 1.1b): E.g. $12x^{\frac{3}{2}}=16-\sqrt{x}$. Notes: Makes the term in $x^{\frac{3}{2}}$ the subject "
       r"of the formula",
       r"A1* (AO 2.1): $x^{\frac{3}{2}}=\frac{4}{3}-\frac{\sqrt{x}}{12}\Rightarrow x=\left(\frac{4}{3}-\frac{\sqrt{x}}"
       r"{12}\right)^{\frac{2}{3}}$ *. Notes: A correct and rigorous argument leading to the given solution.",
       r"ALT: (b) Alternative - working backwards — M1: $x=\left(\frac{4}{3}-\frac{\sqrt{x}}{12}\right)^{\frac{2}{3}}"
       r"\Rightarrow x^{\frac{3}{2}}=\frac{4}{3}-\frac{\sqrt{x}}{12}\Rightarrow12x^{\frac{3}{2}}=16-\sqrt{x}\Rightarrow"
       r"12x^2=16\sqrt{x}-x\Rightarrow12x^2-16\sqrt{x}+x=0$. Notes: For raising to power of 3/2 both sides.",
       r"ALT: (b) Alternative - working backwards — dM1: Multiplies through by $\sqrt{x}$.",
       r"ALT: (b) Alternative - working backwards — A1: Achieves printed answer and makes a minimal comment e.g. tick, "
       r"#, QED, true etc."],
      True, 16),
    e("07c", "7(c)", NUM, "9.2", 3, LATEX["07c"],
      [r"M1 (AO 1.1b): $x_2=\sqrt[3]{\left(\frac{4}{3}-\frac{\sqrt{2}}{12}\right)^2}$. Notes: Attempts to use the "
       r"iterative formula with $x_1=2$. This is implied by sight of $x_2=\left(\frac{4}{3}-\frac{\sqrt{2}}{12}\right)"
       r"^{\frac{2}{3}}$ or awrt 1.14",
       r"A1 (AO 1.1b): $x_2=$ awrt 1.13894. Notes: $x_2=$ awrt 1.13894",
       r"A1 (AO 2.2a): $x=1.15650$. Notes: Deduces that $x=1.15650$"],
      True, 16),

    # ---------------- Q8 ----------------
    e("08", "8", INT, "8.2, 2.6", 6, LATEX["08"],
      [r"M1 (AO 1.1b): Via firstly integrating: $\mathrm{f}'(x)=6x^2+ax-23\Rightarrow\mathrm{f}(x)=2x^3+\frac{1}{2}ax^2"
       r"-23x+c$. Notes: Integrates $\mathrm{f}'(x)$ with two correct indices. There is no requirement for the $+c$",
       r"A1 (AO 1.1b): $\mathrm{f}(x)=2x^3+\frac{1}{2}ax^2-23x+c$. Notes: Fully correct integration (may be "
       r"unsimplified). The $+c$ must be seen (or implied by the $-12$)",
       r"B1 (AO 2.2a): $\text{“}c\text{”}=-12$. Notes: Deduces that the constant term is $-12$",
       r"dM1 (AO 3.1a): $\mathrm{f}(-4)=0\Rightarrow2\times(-4)^3+\frac{1}{2}a(-4)^2-23(-4)-12=0$. Notes: Dependent upon "
       r"having done some integration. It is for setting up a linear equation in $a$ by using $\mathrm{f}(-4)=0$ May "
       r"also see long division attempted for this mark. Need to see a complete method leading to a remainder in terms "
       r"of $a$ which is then set $=0$. For reference, the quotient is $2x^2+\left(\frac{a}{2}-8\right)x+9-2a$ and the "
       r"remainder is $8a-48$ May also use $(x+4)(px^2+qx+r)=2x^3+\frac{1}{2}ax^2-23x-12$ and compare coefficients to "
       r"find $p$, $q$ and $r$ and hence $a$. Allow this mark if they solve for $p$, $q$ and $r$ $\textbf{Note that "
       r"some candidates use 2f(x) which is acceptable and gives the same result if executed correctly.}$",
       r"dM1 (AO 1.1b): $a=\ldots$ (6). Notes: Solves the linear equation in $a$ or uses $p$, $q$ and $r$ to find $a$. "
       r"It is dependent upon having attempted some integration and used $\mathrm{f}(\pm4)=0$ or long "
       r"division/comparing coefficients with $(x+4)$ as a factor.",
       r"A1cso (AO 2.1): $(\mathrm{f}(x)=)2x^3+3x^2-23x-12$ Or Equivalent e.g. $(\mathrm{f}(x)=)(x+4)(2x^2-5x-3)$ "
       r"$(\mathrm{f}(x)=)(x+4)(2x+1)(x-3)$. Notes: For $(\mathrm{f}(x)=)2x^3+3x^2-23x-12$ oe. Note that "
       r"“$\mathrm{f}(x)=$” does not need to be seen and ignore any “$=0$”",
       r"ALT: 8 Alt (Via firstly using factor) — M1 (AO 1.1b): $\mathrm{f}(x)=(x+4)(Ax^2+Bx+C)$. Notes: Uses the fact "
       r"that $\mathrm{f}(x)$ is a cubic expression with a factor of $(x+4)$",
       r"ALT: 8 Alt (Via firstly using factor) — A1 (AO 1.1b): $\mathrm{f}(x)=(x+4)(Ax^2+Bx+C)$. Notes: For "
       r"$\mathrm{f}(x)=(x+4)(Ax^2+Bx+C)$",
       r"ALT: 8 Alt (Via firstly using factor) — B1 (AO 2.2a): $\mathrm{f}(x)=Ax^3+(4A+B)x^2+(4B+C)x+4C\Rightarrow "
       r"C=-3$. Notes: Deduces that $C=-3$",
       r"ALT: 8 Alt (Via firstly using factor) — dM1 (AO 3.1a): $\mathrm{f}'(x)=3Ax^2+2(4A+B)x+(4B+C)$ and "
       r"$\mathrm{f}'(x)=6x^2+ax-23$ $\Rightarrow A=\ldots$. Notes: Attempts to differentiate either by product rule "
       r"or via multiplication and compares to $\mathrm{f}'(x)=6x^2+ax-23$ to find $A$.",
       r"ALT: 8 Alt (Via firstly using factor) — dM1 (AO 1.1b): Full method to get $A$, $B$ and $C$. Notes: Full "
       r"method to get $A$, $B$ and $C$",
       r"ALT: 8 Alt (Via firstly using factor) — A1cso (AO 2.1): $\mathrm{f}(x)=(x+4)(2x^2-5x-3)$. Notes: "
       r"$\mathrm{f}(x)=(x+4)(2x^2-5x-3)$ or $\mathrm{f}(x)=(x+4)(2x+1)(x-3)$"],
      False, 20),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", EXP, "6.7", 4, LATEX["09a"],
      [r"M1 (AO 3.1b): $t=0, \theta=18\Rightarrow18=A-B$ $\textbf{or}$ $t=10, \theta=44\Rightarrow44=A-B"
       r"\mathrm{e}^{-0.7}$. Notes: Makes the first key step in the solution of the problem. Substitutes $t=0$ and "
       r"$\theta=18$ $\textbf{or}$ $t=10$ and $\theta=44$ into the equation of the model to obtain an equation "
       r"connecting $A$ and $B$. Note that $18=A-B\mathrm{e}^0$ scores M0 unless $18=A-B$ is seen or implied later. If "
       r"they do not obtain an equation in $A$ and $B$ using the first conditions e.g. they have $18=A-1$ then they can "
       r"score this mark if they substitute $A=19$ directly into $44=A-B\mathrm{e}^{-0.7}$ as an equation in $A$ and "
       r"$B$ is implied.",
       r"M1 (AO 3.1a): $t=0, \theta=18\Rightarrow18=A-B$ $\textbf{and}$ $t=10, \theta=44\Rightarrow44=A-B"
       r"\mathrm{e}^{-0.7}$ $\textbf{and}$ $\Rightarrow A=\ldots, B=\ldots$. Notes: Substitutes $t=0$ and $\theta=18$ "
       r"$\textbf{and}$ $t=10$ and $\theta=44$ to obtain 2 equations connecting $A$ and $B$ $\textbf{and}$ then "
       r"proceeds to solves their equations in $A$ and $B$ simultaneously to obtain values for both constants. Do not "
       r"be too concerned with the processing as long as values for $A$ and $B$ are obtained.",
       r"A1 (AO 1.1b): At least one of: $A=69.6$, $B=51.6$ but allow awrt 70/awrt 52 [M1 on EPEN]. Notes: A1(M1 on "
       r"EPEN): For $A=$ awrt 70 $\textbf{or}$ $B=$ awrt 52",
       r"A1 (AO 3.3): $\theta=69.6-51.6\mathrm{e}^{-0.07t}$. Notes: For $\theta=69.6-51.6\mathrm{e}^{-0.07t}$ "
       r"$\textbf{Must be a}$ $\underline{\textbf{fully correct equation as shown}}$ $\textbf{but allow recovery if seen "
       r"in (b).}$ Note that some candidates evaluate $\mathrm{e}^0$ as 0 and so obtain $A=18$ and then write "
       r"$44=18-B\mathrm{e}^{-0.7}$ and solve for $B$. Such attempts can score M1M0A0A0 only."],
      False, 24),
    e("09b", "9(b)", EXP, "6.7", 2, LATEX["09b"],
      [r"B1ft (AO 3.4): The maximum temperature is $\text{“}69.6\text{”}" + DEG + r"$ (according to the model) (The "
       r"model has an) upper limit of $\text{“}69.6\text{”}" + DEG + r"$ (The model suggests that) the boiling point is "
       r"$\text{“}69.6\text{”}" + DEG + r"$. Notes: Identifies $A$ as the boiling point/maximum temperature in the "
       r"model. Follow through their $A$.",
       r"B1ft (AO 3.5a): Model is not appropriate as $69.6" + DEG + r"$ is much lower than $78" + DEG + r"$. Notes: "
       r"Makes a valid conclusion (valid/not valid, good/not good etc.) that refers to the 78 and includes a reference "
       r"to a significant/large difference $\textbf{Minimum for both marks:}$ The model is not appropriate as "
       r"$\text{“}69.6\text{”}" + DEG + r"$ is much lower than $78" + DEG + r"$ $\textbf{Note that these marks are not "
       r"available if their equation is solvable. Note also that B0B1 is not possible.}$",
       r"ALT: (b) Alternative provided their $A<78$ — B1ft: $\theta=69.6-51.6\mathrm{e}^{-0.07t}=78\Rightarrow51.6"
       r"\mathrm{e}^{-0.07t}=69.6-78=-8.4$ $\Rightarrow\mathrm{e}^{-0.07t}=-\frac{7}{43}$ and $\ln\left(-\frac{7}{43}"
       r"\right)$ and makes a reference to the fact that the equation cannot be solved or e.g. cannot take log of a "
       r"negative number. You can condone numerical slips in the calculation.",
       r"ALT: (b) Alternative provided their $A<78$ — B1ft: Model is not appropriate as $69.6" + DEG + r"$ is much "
       r"lower than $78" + DEG + "$"],
      False, 24),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", TRIG, "5.8, 5.6", 4, LATEX["10a"],
      [r"M1 (AO 3.1a): $\cos3A=\cos(2A+A)=\cos2A\cos A-\sin2A\sin A$. Notes: $\textbf{Allow a proof in terms of}$ $x$ "
       r"$\textbf{rather than A}$ Attempts to use the compound angle formula for $\cos(2A+A)$ or $\cos(A+2A)$ Condone a "
       r"slip in sign",
       r"dM1 (AO 1.1b): $=(2\cos^2A-1)\cos A-(2\sin A\cos A)\sin A$. Notes: Uses correct double angle identities for "
       r"$\cos2A$ and $\sin2A$ $\cos2A=2\cos^2A-1$ must be used. If either of the other two versions are used expect to "
       r"see an attempt to replace $\sin^2A$ by $1-\cos^2A$ at a later stage. $\textbf{Depends on previous mark}$.",
       r"ddM1 (AO 2.1): $=(2\cos^2A-1)\cos A-2\cos A(1-\cos^2A)$. Notes: Attempts to get all terms in terms of "
       r"$\cos A$ using correct and appropriate identities. $\textbf{Depends on both previous marks}$.",
       r"A1* (AO 1.1b): $=4\cos^3A-3\cos A$ *. Notes: A completely correct and rigorous proof including correct "
       r"notation, no mixed variables, missing brackets etc.",
       r"ALT: (a) Alternative right to left — M1: $4\cos^3A-3\cos A=\cos A(4\cos^2A-3)=\cos A(2\cos^2A-1+2(1-\sin^2A)"
       r"-2)=\cos A(\cos2A-2\sin^2A)$ $=\cos A\cos2A-2\sin A\cos A\sin A=\cos A\cos2A-\sin2A\sin A=\cos(2A+A)=\cos3A$. "
       r"Score M1: For $4\cos^3A-3\cos A=\cos A(4\cos^2A-3)$",
       r"ALT: (a) Alternative right to left — dM1: For $\cos A(2\cos^2A-1+2(1-\sin^2A)-2)$ (Replaces $4\cos^2A-1$ by "
       r"$2\cos^2A-1$ and $2(1-\sin^2A)$)",
       r"ALT: (a) Alternative right to left — ddM1: Reaches $\cos A\cos2A-\sin2A\sin A$",
       r"ALT: (a) Alternative right to left — A1: $\cos(2A+A)=\cos3A$"],
      False, 26),
    e("10b", "10(b)", TRIG, "5.7, 5.6", 4, LATEX["10b"],
      [r"M1 (AO 1.1b): $1-\cos3x=\sin^2x\Rightarrow\cos^2x+3\cos x-4\cos^3x=0$. Notes: For an attempt to produce an "
       r"equation just in $\cos x$ using both part (a) and the identity $\sin^2x=1-\cos^2x$ Allow one slip in sign or "
       r"coefficient when copying the result from part (a)",
       r"dM1 (AO 3.1a): $\Rightarrow\cos x(4\cos^2x-\cos x-3)=0$ $\Rightarrow\cos x(4\cos x+3)(\cos x-1)=0$ "
       r"$\Rightarrow\cos x=\ldots$. Notes: $\textbf{Dependent upon the preceding mark}$. It is for taking the cubic "
       r"equation in $\cos x$ and making a valid attempt to solve. This could include factorisation or division of a "
       r"$\cos x$ term followed by an attempt to solve the 3 term quadratic equation in $\cos x$ to reach at least one "
       r"non zero value for $\cos x$. May also be scored for solving the cubic equation in $\cos x$ to reach at least "
       r"one non zero value for $\cos x$.",
       r"A1 (AO 1.1b): Two of " + FOURSOL + r". Notes: Two of " + FOURSOL + r" $\textbf{Depends on the}$ "
       r"$\underline{\textbf{first}}$ $\textbf{method mark}$.",
       r"A1 (AO 2.1): All four of " + FOURSOL + r". Notes: All four of " + FOURSOL + r" with no extra solutions offered "
       r"within the range.",
       r"ALT: (b) Note that this is an alternative approach for obtaining the cubic equation in (b) — M1: "
       r"$1-\cos3x=\sin^2x\Rightarrow1-\cos3x=\frac{1}{2}(1-\cos2x)$ $\Rightarrow2-2\cos3x=1-\cos2x$ "
       r"$\Rightarrow1=2\cos3x-\cos2x$ $\Rightarrow1=2(4\cos^3x-3\cos x)-(2\cos^2x-1)$ $\Rightarrow0=4\cos^3x-3\cos x"
       r"-\cos^2x$ The M1 will be scored on the penultimate line when they use part (a) and use the correct identity "
       r"for $\cos2x$"],
      False, 26),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", ALG, "2.7", 2, LATEX["11a"],
      [r"B1 (AO 1.1b): $x=-4$ $\textbf{or}$ $y=-5$. Notes: One correct coordinate. Either $x=-4$ or $y=-5$ or "
       r"$(-4, \ldots)$ or $(\ldots, -5)$ seen.",
       r"B1 (AO 2.2a): $P(-4, -5)$. Notes: Deduces that $P(-4, -5)$ Accept written separately e.g. $x=-4$, $y=-5$"],
      True, 30),
    e("11b", "11(b)", ALG, "2.7, 2.5", 2, LATEX["11b"],
      [r"M1 (AO 1.1b): $3x+40=-2(x+4)-5\Rightarrow x=\ldots$. Notes: Attempts to solve $3x+40=-2(x+4)-5\Rightarrow "
       r"x=\ldots$ Must reach a value for $x$. You may see the attempt crossed out but you can still take this as an "
       r"attempt to solve the required equation.",
       r"A1 (AO 2.1): $x=-10.6$. Notes: $x=-10.6$ oe e.g. $-\frac{53}{5}$ only. If other values are given, e.g. "
       r"$x=-37$ they must be rejected or the $-\frac{53}{5}$ clearly chosen as their answer. Ignore any attempts to "
       r"find $y$. Correct answer with no working scores both marks.",
       r"ALT: (b) Alternative by squaring — M1: $3x+40=2\left|x+4\right|-5\Rightarrow3x+45=2\left|x+4\right|"
       r"\Rightarrow9x^2+270x+2025=4(x^2+8x+16)$ $\Rightarrow5x^2+238x+1961=0\Rightarrow x=-37, -\frac{53}{5}$ M1 for "
       r"isolating the $\left|x+4\right|$, squaring both sides and solving the resulting quadratic",
       r"ALT: (b) Alternative by squaring — A1: for selecting the $-\frac{53}{5}$"],
      True, 30),
    e("11c", "11(c)", ALG, "2.7, 2.5", 3, LATEX["11c"],
      [r"B1 (AO 2.2a): $a>2$. Notes: Deduces that $a>2$",
       r"M1 (AO 3.1a): $y=ax\Rightarrow-5=-4a\Rightarrow a=\frac{5}{4}$. Notes: Attempts to find a value for $a$ using "
       r"their $P(-4, -5)$ Alternatively attempts to solve $ax=2(x+4)-5$ and $ax=2(x+4)-5$ to obtain a value for $a$.",
       r"A1 (AO 2.5): $\{a:a\leqslant1.25\}\cup\{a:a>2\}$. Notes: Correct range in acceptable set notation. Examples: "
       r"$\{a:a\leqslant1.25\}\cup\{a:a>2\}$ $\{a:a\leqslant1.25\}, \{a:a>2\}$ $\{a:a\leqslant1.25\text{ or }a>2\}$ "
       r"$\{a:a\leqslant1.25, a>2\}$ $(-\infty,1.25]\cup(2,\infty)$ $(-\infty,1.25], (2,\infty)$"],
      True, 30),

    # ---------------- Q12 ----------------
    e("12ai", "12(a)(i)", INT, "8.3, 5.6", 3, LATEX["12ai"],
      [r"M1 (AO 1.2): $y\times\frac{\mathrm{d}x}{\mathrm{d}t}=5\sin2t\times6\cos t$ or $5\times2\sin t\cos t\times6"
       r"\cos t$. Notes: Attempts to multiply $y$ by $\frac{\mathrm{d}x}{\mathrm{d}t}$ to obtain $A\sin2t\cos t$ but may "
       r"apply $\sin2t=2\sin t\cos t$ here",
       r"dM1 (AO 1.1b): (Area $=$) $\int5\sin2t\times6\cos t\," + H12 + r"=\int5\times2\sin t\cos t\times6\cos t\,"
       + H12 + r"$ or $\int5\sin2t\times6\cos t\," + H12 + r"=\int60\sin t\cos^2t\," + H12 + r"$. Notes: Attempts to "
       r"use $\sin2t=2\sin t\cos t$ within an integral which may be implied by e.g. $A\int\sin2t\times\cos t\," + H12
       + r"=\int k\sin t\cos^2t\," + H12 + "$",
       r"A1* (AO 2.1*): (Area $=$) $\int_0^{\frac{\pi}{2}}60\sin t\cos^2t\," + H12 + r"$ *. Notes: Fully correct work "
       r"leading to the given answer. $\textbf{This must include}$ $\sin2t=2\sin t\cos t$ or e.g. $5\sin2t=10\sin t"
       r"\cos t$ seen $\underline{\text{explicitly}}$ in their proof and a correct intermediate line that includes an "
       r"integral sign and the “$" + H12 + r"$” $\textbf{Allow the limits to just “appear” in the final answer e.g. "
       r"working need not be shown for the limits.}$"],
      True, 34),
    e("12aii", "12(a)(ii)", INT, "8.5, 8.3", 3, LATEX["12aii"],
      [r"M1 (AO 1.1b): $\int60\sin t\cos^2t\," + H12 + r"=-20\cos^3t$. Notes: Obtains $\int60\sin t\cos^2t\," + H12
       + r"=k\cos^3t$. This may be attempted via a substitution of $u=\cos t$ to obtain $\int60\sin t\cos^2t\," + H12
       + "=ku^3$",
       r"A1 (AO 1.1b): $\int60\sin t\cos^2t\," + H12 + r"=-20\cos^3t$. Notes: Correct integration $-20\cos^3t$ or "
       r"equivalent e.g. $-20u^3$",
       r"A1* (AO 2.1): Area $=\left[-20\cos^3t\right]_0^{\frac{\pi}{2}}=0-(-20)=20$ *. Notes: Rigorous proof with all "
       r"aspects correct including the correct limits and the $0-(-20)$ and not $\underline{\text{just}}$: "
       r"$-20\cos^3\frac{\pi}{2}-(-20\cos^30)=20$"],
      True, 34),
    e("12b", "12(b)", COORD, "3.4, 5.7", 5, LATEX["12b"],
      [r"M1 (AO 3.4): $5\sin2t=4.2\Rightarrow\sin2t=\frac{4.2}{5}$. Notes: Uses the given model and attempts to find "
       r"value(s) of $t$ when $\sin2t=\frac{4.2}{5}$. Look for $2t=\sin^{-1}\frac{4.2}{5}\Rightarrow t=\ldots$",
       r"A1 (AO 1.1b): $t=0.4986\ldots, 1.072\ldots$. Notes: At least one correct value for $t$, correct to 2 dp. FYI "
       r"$t=0.4986\ldots, 1.072\ldots$ or in degrees $t=28.57\ldots, 61.42\ldots$",
       r"dM1 (AO 3.4): Attempts to finds the $x$ values at both $t$ values. Notes: Attempts to find $\textbf{TWO}$ "
       r"distinct values of $x$ when $\sin2t=\frac{4.2}{5}$. Condone poor trig work and allow this mark if 2 values of "
       r"$x$ are attempted from 2 values of $t$.",
       r"A1 (AO 1.1b): $t=0.4986\ldots\Rightarrow x=2.869\ldots$ $t=1.072\Rightarrow x=5.269\ldots$. Notes: Both values "
       r"correct to 2 dp. NB $x=2.869\ldots, 5.269\ldots$",
       r"A1 (AO 3.2a): Width of path $=2.40$ metres. Notes: 2.40 metres or 240 cm Allow awrt 2.40 m or allow 2.4m (not "
       r"awrt 2.4 m) and allow awrt 240 cm. $\textbf{Units are required}$.",
       r"ALT: (b) Or may take Cartesian approach — M1: $5\sin2t=4.2\Rightarrow10\sin t\cos t=4.2\Rightarrow10\frac{x}{6}"
       r"\sqrt{1-\frac{x^2}{36}}=4.2\Rightarrow x^4-36x^2+228.6144=0\Rightarrow x=2.869\ldots, 5.269\ldots$ M1: For "
       r"converting to Cartesian form",
       r"ALT: (b) Or may take Cartesian approach — A1: Correct quartic",
       r"ALT: (b) Or may take Cartesian approach — M1: Solves quartic",
       r"ALT: (b) Or may take Cartesian approach — A1: Correct values"],
      True, 34),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", EXP, "6.3", 1, LATEX["13a"],
      [r"B1 (AO 2.2a): $k=\mathrm{e}^2$ $\textbf{or}$ $x\neq\mathrm{e}^2$. Notes: Deduces $k=\mathrm{e}^2$ "
       r"$\textbf{or}$ $x\neq\mathrm{e}^2$ Condone $k=$ awrt 7.39 or $x\neq$ awrt 7.39"],
      False, 38),
    e("13b", "13(b)", DIFF, "7.4, 7.3", 3, LATEX["13b"],
      [r"M1 (AO 1.1b): $\mathrm{g}'(x)=\frac{(\ln x-2)\times\frac{3}{x}-(3\ln x-7)\times\frac{1}{x}}{(\ln x-2)^2}="
       r"\frac{1}{x(\ln x-2)^2}$ or $\mathrm{g}'(x)=\frac{\mathrm{d}}{\mathrm{d}x}\left(3-(\ln(x)-2)^{-1}\right)="
       r"(\ln x-2)^{-2}\times\frac{1}{x}=\frac{1}{x(\ln x-2)^2}$ or $\mathrm{g}'(x)=(\ln x-2)^{-1}\times\frac{3}{x}-"
       r"(3\ln x-7)(\ln x-2)^{-2}\times\frac{1}{x}=\frac{1}{x(\ln x-2)^2}$. Notes: Attempts to differentiate via the "
       r"quotient rule and with $\ln x\to\frac{1}{x}$ so allow for: $\frac{\mathrm{d}}{\mathrm{d}x}(\mathrm{g}(x))="
       r"\frac{(\ln x-2)\times\frac{\alpha}{x}-(3\ln x-7)\times\frac{\beta}{x}}{(\ln x-2)^2}$, $\beta>0$ $\textbf{But a "
       r"correct rule may be implied by their}$ $u$, $v$, $u'$, $v'$ $\textbf{followed by applying}$ "
       r"$\frac{vu'-uv'}{v^2}$ $\textbf{etc.}$ Alternatively attempts to write $\mathrm{g}(x)=\frac{3\ln(x)-7}"
       r"{\ln(x)-2}=3-(\ln(x)-2)^{-1}$ and attempts the chain rule so allow for: $3-(\ln(x)-2)^{-1}\to(\ln(x)-2)^{-2}"
       r"\times\frac{\alpha}{x}$ Alternatively writes $\mathrm{g}(x)=(3\ln(x)-7)(\ln(x)-2)^{-1}$ and attempts the "
       r"product rule so allow for: $\mathrm{g}'(x)=(\ln x-2)^{-1}\times\frac{\alpha}{x}-(3\ln x-7)(\ln x-2)^{-2}\times"
       r"\frac{\beta}{x}$ $\textbf{In general condone missing brackets for the M mark. E.g. if they quote}$ "
       r"$u=3\ln x-7$ $\textbf{and}$ $v=\ln x-2$ $\textbf{and don’t make the differentiation easier, they can be "
       r"awarded this mark for applying the correct rule. Also allow this mark if they quote the correct quotient rule "
       r"but only have}$ $v$ $\textbf{rather than}$ $v^2$ $\textbf{in the denominator.}$",
       r"A1 (AO 2.1): $=\frac{1}{x(\ln x-2)^2}$. Notes: $\frac{1}{x(\ln x-2)^2}$ Allow $\frac{\frac{1}{x}}"
       r"{(\ln x-2)^2}$ $\textbf{i.e. we need to see the numerator simplified to 1/x}$ Note that some candidates "
       r"establish the correct numerator and correct denominator independently and provided they obtain the correct "
       r"expressions, this mark can be awarded. But allow a correctly expanded denominator.",
       r"A1cso (AO 2.4): As $x>0$ (or $1/x>0$) $\textbf{AND}$ $\ln x-2$ is squared so $\mathrm{g}'(x)>0$. Notes: "
       r"States that as $x>0$ $\textbf{AND}$ $\ln x-2$ is squared so $\mathrm{g}'(x)>0$"],
      False, 38),
    e("13c", "13(c)", ALG, "2.5, 6.3", 2, LATEX["13c"],
      [r"M1 (AO 3.1a): Attempts to solve either $3\ln x-7\ldots0$ or $\ln x-2\ldots0$ or $3\ln a-7\ldots0$ or "
       r"$\ln a-2\ldots0$ where … is “=” or “>” to reach a value for $x$ or $a$ but may be seen as an inequality e.g. "
       r"$x>\ldots$ or $a>\ldots$. Notes: Attempts to solve either $3\ln x-7=0$ or $\ln x-2=0$ or using inequalities "
       r"e.g. $3\ln x-7>0$",
       r"A1 (AO 2.2a): $0<a<\mathrm{e}^2$, $a>\mathrm{e}^{\frac{7}{3}}$. Notes: $0<a<\mathrm{e}^2$, "
       r"$a>\mathrm{e}^{\frac{7}{3}}$"],
      False, 38),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", COORD, "3.2, 3.1", 3, LATEX["14a"],
      [r"B1 (AO 2.2a): $C$ is $(x-r)^2+(y-r)^2=r^2$ or $x^2+y^2-2rx-2ry+r^2=0$. Notes: Deduces the correct equation of "
       r"the circle",
       r"M1 (AO 1.1b): $y=12-2x$, $x^2+y^2-2rx-2ry+r^2=0$ $\Rightarrow x^2+(12-2x)^2-2rx-2r(12-2x)+r^2=0$ or "
       r"$y=12-2x$, $(x-r)^2+(y-r)^2=r^2$ $\Rightarrow(x-r)^2+(12-2x-r)^2=r^2$. Notes: Attempts to form an equation with "
       r"terms of the form $x^2$, $x$, $r^2$, and $xr$ $\underline{\textbf{only}}$ using $y=12\pm2x$ and their circle "
       r"equation which must be of an appropriate form. I.e. includes or implies an $x^2$, $y^2$, $r^2$ such as "
       r"$x^2+y^2=r^2$ If their circle equation starts off as e.g. $(x\pm a)^2+(y\pm b)^2=r^2$ then the B mark and the "
       r"M mark can be awarded when the “$a$” and “$b$” are replaced by $r$ or $-r$ as appropriate for their circle "
       r"equation.",
       r"A1* (AO 2.1): $x^2+144-48x+4x^2-2rx-24r+4rx+r^2=0$ $\Rightarrow5x^2+(2r-48)x+(r^2-24r+144)=0$ *. Notes: Uses "
       r"correct and accurate algebra leading to the given solution."],
      False, 42),
    e("14b", "14(b)", COORD, "3.2, 2.3", 4, LATEX["14b"],
      [r"M1 (AO 3.1a): $b^2-4ac=0\Rightarrow(2r-48)^2-4\times5\times(r^2-24r+144)=0$. Notes: Attempts to use "
       r"$b^2-4ac\ldots0$ o.e. with $a=5, b=2r-48, c=r^2-24r+144$ and where ... is “=” or any inequality Allow minor "
       r"slips when copying the $a$, $b$ and $c$ provided it does not make the work easier and allow $\textbf{their}$ "
       r"$a$, $b$ and $c$ if they are similar expressions. FYI $(2r-48)^2-4\times5\times(r^2-24r+144)=4r^2-192r+2304-"
       r"20r^2+480r-2880=-16r^2+288r-576$",
       r"A1 (AO 1.1b): $r^2-18r+36=0$ or any multiple of this equation. Notes: Correct quadratic $\textbf{equation}$ in "
       r"$r$ (or inequality). Terms need not be all one side but must be collected. E.g. allow $r^2-18r=-36$ and allow "
       r"any multiple of this equation (or inequality).",
       r"dM1 (AO 1.1b): $\Rightarrow(r-9)^2-81+36=0\Rightarrow r=\ldots$. Notes: Correct attempt to solve their 3TQ in "
       r"$r$. Dependent upon previous M",
       r"A1 (AO 1.1b): $r=9\pm3\sqrt{5}$. Notes: Careful and accurate work leading to both answers in the required form "
       r"(must be simplified surds)"],
      False, 42),

    # ---------------- Q15 ----------------
    e("15a", "15(a)", SEQ, "4.5", 4, LATEX["15a"],
      [r"B1 (AO 1.2): $S_n=a+ar+ar^2+\ldots\ldots+ar^{n-1}$. Notes: Writes out the sum or lists terms. Condone the "
       r"omission of $S$. The sum must include the first and last terms and (at least) two other correct terms and no "
       r"incorrect terms e.g. $ar^n$ Note that the sum may be seen embedded within their working.",
       r"M1 (AO 2.1): $rS_n=ar+ar^2+ar^3+\ldots\ldots+ar^n\Rightarrow S_n-rS_n=\ldots$. Notes: For the key step in "
       r"attempting to multiply the first series by $r$ and subtracting.",
       r"A1 (AO 1.1b): $S_n-rS_n=a-ar^n$. Notes: $S_n-rS_n=a-ar^n$ either way around but condone one side being "
       r"prematurely factorised (but not both) $\textbf{following correct work but this could follow B0 if "
       r"insufficient terms were shown.}$",
       r"A1* (AO 2.1): $S_n(1-r)=a(1-r^n)\Rightarrow S_n=\frac{a(1-r^n)}{(1-r)}$ *. Notes: $\textbf{Depends on all "
       r"previous marks.}$ Proceeds to given result showing all steps including seeing both sides unfactorised at some "
       r"point in their working. $\textbf{Note: If terms are}$ $\underline{\textbf{listed}}$ $\textbf{rather than}$ "
       r"$\underline{\textbf{added}}$ $\textbf{then allow the first 3 marks if otherwise correct but withhold the final "
       r"mark.}$ Example for (a): [handwritten working: $S_n=a+ar+ar^2+ar^3\ldots ar^{n-2}+ar^{n-1}$; "
       r"$rS_n=ar+ar^2+ar^3+ar^4\ldots ar^{n-1}+ar^n$; $S_n-rS_n=a(1-r^n)$; $S_n(1-r)=a(1-r^n)$; then a last line cut "
       r"off at the foot of the page] $\textbf{This scores B1M1A1A0:}$ $\textbf{B1: Writes down the sum including first "
       r"and last terms and at least 2 other correct terms and no incorrect terms}$ $\textbf{M1: Multiplies by}$ $r$ "
       r"$\textbf{and subtracts}$ $\textbf{A1: Correct equation (we allow one side to be prematurely factorised)}$ "
       r"$\textbf{A0: One side was prematurely factorised}$"],
      False, 46),
    e("15b", "15(b)", SEQ, "4.5, 2.3", 4, LATEX["15b"],
      [r"M1 (AO 3.1a): $\frac{a(1-r^{10})}{1-r}=4\times\frac{a(1-r^5)}{1-r}$ or $4\times\frac{a(1-r^{10})}{1-r}="
       r"\frac{a(1-r^5)}{1-r}$ Equation in $r^{10}$ and $r^5$ (and possibly $1-r$). Notes: For the correct strategy of "
       r"producing an equation in just $r^{10}$ and $r^5$ (and possibly $(1-r)$) with the “4” on either side using the "
       r"result from part (a) and makes progress to at least cancel through by $a$ Some candidates retain the “$1-r$” "
       r"and start multiplying out e.g. $(1-r)(1-r^{10})$ and this mark is still available as long as there is progress "
       r"in cancelling the “$a$”. (b) Note: For candidates who use $S_5=4S_{10}$ expect to see: $4\times\frac{a(1-"
       r"r^{10})}{1-r}=\frac{a(1-r^5)}{1-r}\Rightarrow4(1-r^{10})=(1-r^5)$ M1A0 $4r^{10}-r^5-3=0\Rightarrow(4r^5+3)"
       r"(r^5-1)=0\Rightarrow r^5=\ldots$ or $4(1-r^5)(1+r^5)=(1-r^5)\Rightarrow r^5=\ldots$ dM1A0",
       r"A1 (AO 1.1b): $1-r^{10}=4(1-r^5)$. Notes: Correct equation with the $a$ and the $1-r$ cancelled. Allow any "
       r"correct equation in just $r^5$ and $r^{10}$",
       r"dM1 (AO 2.1): $r^{10}-4r^5+3=0\Rightarrow(r^5-1)(r^5-3)=0\Rightarrow r^5=\ldots$ or e.g. $1-r^{10}=4(1-r^5)"
       r"\Rightarrow(1-r^5)(1+r^5)=4(1-r^5)\Rightarrow r^5=\ldots$. Notes: Depends on the first M. Solves as far as "
       r"$r^5=\ldots$ by solving a 3 term quadratic in $r^5$ by a valid method – see general guidance or by difference "
       r"of 2 squares – see above",
       r"A1 (AO 1.1b): $r=\sqrt[5]{3}$ oe only. Notes: $r=\sqrt[5]{3}$ oe only. The solution $r=1$ if found must be "
       r"rejected here."],
      False, 46),

    # ---------------- Q16 ----------------
    e("16", "16", PROOF, "1.1", 4, LATEX["16"],
      [r"M1 (AO 3.1a): NB any natural number can be expressed in the form: $3k$, $3k+1$, $3k+2$ or equivalent e.g. "
       r"$3k-1$, $3k$, $3k+1$ Attempts to square $\textbf{any two}$ distinct cases of the above. Notes: Makes the key "
       r"step of attempting to write the natural numbers in any 2 of the 3 distinct forms or equivalent expressions, as "
       r"shown in the mark scheme, and attempts to square these expressions.",
       r"A1 (AO 1.1b): Achieves accurate results and makes a valid comment for $\textbf{any two}$ of the possible three "
       r"cases: E.g. $(3k)^2=9k^2(=3\times3k^2)$ is a multiple of 3 $(3k+1)^2=9k^2+6k+1=3\times(3k^2+2k)+1$ is one more "
       r"than a multiple of 3 $(3k+2)^2=9k^2+12k+4=3\times(3k^2+4k+1)+1$ $\left(\text{or }(3k-1)^2=9k^2-6k+1=3\times"
       r"(3k^2-2k)+1\right)$ is one more than a multiple of 3 [M1 on EPEN]. Notes: A1(M1 on EPEN): Successfully shows "
       r"for 2 cases that the squares are either a multiple of 3 or 1 more than a multiple of 3 "
       r"$\underline{\text{using algebra}}$. This must be made explicit e.g. reaches $3\times(3k^2+2k)+1$ and makes a "
       r"statement that this is one more than a multiple of 3 but also allow other rigorous arguments that reason why "
       r"$9k^2+6k+1$ is one more than a multiple of 3 e.g. “$9k^2$ is a multiple of 3 and $6k$ is a multiple of 3 so "
       r"$9k^2+6k+1$ is one more than a multiple of 3”",
       r"M1 (AO 2.1): Attempts to square in all 3 distinct cases. E.g. attempts to square $3k$, $3k+1$, $3k+2$ or e.g. "
       r"$3k-1$, $3k$, $3k+1$ [A1 on EPEN]. Notes: M1(A1 on EPEN): Recognises that all natural numbers can be written "
       r"in one of the 3 distinct forms or equivalent expressions, as shown in the mark scheme, and attempts to square "
       r"in all 3 cases.",
       r"A1 (AO 2.4): Achieves accurate results for all three cases and gives a minimal conclusion (allow tick, QED "
       r"etc.). Notes: Successfully shows for all 3 cases that the squares are either a multiple of 3 or 1 more than a "
       r"multiple of 3 using algebra and makes a conclusion"],
      False, 50),
]

W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        ({"a"}, r"Part (a) was generally answered well, with the majority of candidates using $h=0.5$ and finding an "
                r"area rounding to 1.50, but a number completed it with a final answer of 1.505… and consequently lost "
                r"the final A mark for part (a).", NO),
        ({"a"}, r"The most common error seen was the use of $h=\frac{2}{5}$ which candidates are arriving at because of "
                r"a misunderstanding in the ‘n’ seen in the formula in $\frac{b-a}{n}$, they presumably think n is the "
                r"number of entries in a row of the table ignoring that the first column represents $x_0$ and $y_0$."),
        ({"a"}, r"Those candidates who calculated the width of the trapezia independent of the formula $\frac{b-a}{n}$ "
                r"were usually more successful.", NO),
        ({"a"}, "The formula was set up correctly on most occasions, with the most common error being the lack of "
                "exterior brackets, often resulting in 4.95 as an answer."),
        ({"a"}, r"There were some candidates using a variation of the formula, with the $\frac{1}{2}$ absorbed into the "
                r"brackets, and a few worked out the areas of four separate trapezia, usually successfully."),
        ({"b"}, "Success in part (b) was mixed, with around half the candidates multiplying their answer by 3 and the "
                "others multiplying by 9."),
        ({"b"}, "A minority of candidates restarted, losing access to marks in this question."),
        ({"c"}, "In part (c), the mark was only available to those who arrived at an answer rounding to 4.5 in part "
                "(b).", NO),
        ({"c"}, "Answers were often concise and clear, stating that their answer was correct to 2s.f. or 1d.p. and "
                "therefore quite accurate."),
        ({"c"}, "Others went for a percentage error approach, which was also acceptable and usually completed "
                "successfully."),
        ({"c"}, "The main error in this part was that candidates misunderstood what was being asked of them, and "
                "instead arguing that the answer was an underestimate, confusing this with another common trapezium "
                "rule question.", NO),
    ],
    "02": [
        (W, "This proved to be a demanding question for many candidates, with false starts and seemingly random "
            "statements.", NO),
        (W, "Those who were able to make some progress generally gained the initial method mark for expressing one of "
            "the line segments in terms of the difference of two position vectors, but many candidates were unable to "
            "make further progress.", NO),
        (W, "Unfortunately, the addition of two position vectors was a common error."),
        (W, "Diagrams helped with some responses, but they frequently depicted OP, OQ and OR as collinear, which tended "
            "to cause more confusion."),
        (W, r"The most common approach amongst those who were able to make further progress were either $" + V("PQ")
            + r"=\frac{1}{3}" + V("PR") + "$ or $" + V("OQ") + "=" + V("OP") + r"+\frac{1}{3}" + V("PR") + "$.", NO),
        (W, "Vector notation was often poor, for example Q being used to denote a vector rather than a point, leading "
            "to such confused statements as Q = 1/3 PR.", NO),
    ],
    "03": [
        (W, "This was a fairly accessible question for prepared candidates and provided an early source of marks for "
            "many.", NO),
        ({"a"}, r"Generally, most candidates recognised the need to use the power law for logs and correctly obtained "
                r"$2\log(4-x)=\log(4-x)^2$, then proceeded to remove the logs."),
        ({"a"}, r"In fact, many candidates jumped immediately to $(4-x)^2=(x+8)$ with no sign of logs whatsoever in "
                r"their solution."),
        ({"a"}, "This was condoned although it must be noted that combining steps of working in a ‘show that’ question "
                "can be risky.", BACK),
        ({"a"}, r"Some candidates diligently wrote out $10^{\log(4-x)^2}=10^{\log(x+8)}$ before removing logs, others "
                r"subtracted $\log(4-x)^2$ from both sides and used the log subtraction law to combine the log terms "
                r"before removing the log."),
        ({"a"}, r"Both approaches were often successful although the latter tended to be the riskier of the two as some "
                r"candidates forgot that $10^0=1$ and instead obtained $\frac{(4-x)}{(x+8)}=0$ which was then fudged to "
                r"give the required solution."),
        ({"a"}, "Those candidates that did not recognise the need to employ the power law for logs early on in their "
                "solution made very little progress.", NO),
        ({"a"}, "Disappointingly, some candidates failed to earn the final mark in part (a) as their final line was "
                "missing the “= 0”."),
        ({"a"}, "Candidates should take care to check their final line matches the printed answer in a ‘show that’ "
                "question."),
        ({"b"}, "The first part of part (b) was straightforward and gave an opportunity to re-enter the question for "
                "those who had come unstuck in part (a).", NO),
        ({"b"}, "Indeed, for some candidates this was the only mark attained in this question.", BACK),
        ({"b"}, r"It was surprising that a number of candidates left their ‘solution’ as $(x-1)(x-8)$ or gave "
                r"‘solutions’: $(x-1)$ and $(x-8)$.", NO),
        ({"b"}, r"Only a very small number of candidates incorrectly obtained $x=-1$ or $x=-8$."),
        ({"b"}, "The second part of part (b) was more discriminating and a careful explanation was required here."),
        ({"b"}, r"Most candidates were able to identify $x=8$ as the value which was not a solution."),
        ({"b"}, r"However, in order to gain credit, it was also necessary for candidates to make specific reference to "
                r"the fact that $\log(4-8)$ is undefined.", NO),
        ({"b"}, "Too many candidates simply stated ‘logs can’t be negative’ which was incorrect and quite different to "
                "‘you can’t take logs of a negative number’."),
        ({"b"}, "Candidates should be reminded that reasoning should be precise and specific."),
    ],
    "04": [
        (W, "This was generally well done, and most candidates scored full marks.", NO),
        (W, r"A few candidates missed out the brackets around the $2x$ which usually led to $a=6$."),
        (W, r"Several candidates made a mistake when finding the correct coefficient of $x^4$ and scored no marks."),
        (W, r"This was either because the power of $a$ was incorrect or the binomial coefficient was incorrect or "
            r"occasionally completely missing.", BACK),
        (W, r"The most common error was having the wrong power of $a$, usually as $a^4$ or sometimes $a$ or $a^7$"),
        (W, r"Several candidates used $a^7(1+2x/a)^7$ and errors with the power of $a$ were also common with this "
            r"method."),
        (W, r"Some candidates forgot to multiply by $a^7$ and some forgot to divide the $2x$ by $a$."),
    ],
    "05": [
        (W, "Nearly all candidates combined the equations correctly and gained the first mark."),
        (W, "Many then struggled to progress further."),
        (W, r"A few made mistakes with the indices such as changing $3(2^x)$ into $6^x$ but the most common mistake was "
            r"attempting to take logs incorrectly, usually $\log15-\log(2(2^x))$ or $\log(15-2^{x+1})$ being wrongly "
            r"expanded to arrive at $\log15-(x+1)\log2$.", NO),
        (W, r"Those who realised $2^{x+1}=2(2^x)$ usually went on to solve correctly, giving a correct exact answer and "
            r"therefore gain full marks.", NO),
        (W, "Candidates need to understand that seeing an equation with an unknown index does not automatically mean "
            "that it is a question involving logarithms.", NO),
    ],
    "06": [
        (W, "As would be hoped, most candidates scored some marks on this question."),
        ({"a"}, "Many found part (a) quite straightforward and there were a good proportion of candidates who gained "
                "full marks."),
        ({"a"}, r"Candidates used various approaches to find $A$, $B$ and $C$, but the most common tended to be long "
                r"division."),
        ({"a"}, r"There were a significant number of candidates who performed a completely correct division, but were "
                r"unable to relate their answer to $A$, $B$ and $C$ and so lost the accuracy marks."),
        ({"a"}, r"There were many more errors seen when students attempted to multiply $(Ax+B)$ by $(x+2)$ and compare "
                r"the numerators, and when candidates selected values of $x$ to substitute in, any errors usually cost "
                r"both accuracy marks."),
        ({"a"}, r"In comparison, those who used long division were more likely to make an error only in the remainder "
                r"($-3\ -+12=9$ being a common slip) and so secure the first accuracy mark.", NO),
        ({"b"}, r"In part (b), a pleasingly high number of candidates who had found values for $A$, $B$ and $C$ were "
                r"able to successfully integrate to gain the first two marks, often aided by the follow through mark "
                r"that was available."),
        ({"b"}, "Candidates generally substituted the limits correctly and there was also a relatively good use of the "
                "laws of logarithms to combine their terms, albeit with occasional sign errors."),
        ({"b"}, r"The most common being “$-15\ln8-(-15\ln2)=-15\ln8-15\ln2$”."),
        ({"b"}, r"It was not uncommon for a candidate to then incorrectly combine this to get “$-15\ln\frac{8}{2}$”.",
         BACK),
        ({"b"}, r"Most success was seen where candidates changed the $\ln(8)$ into $\ln(2^3)$ and then $3\ln(2)$ before "
                r"combining the two $\ln2$ terms."),
    ],
    "07": [
        ({"a"}, "In part (a), most candidates used a correct method to differentiate, the majority using the quotient "
                "rule."),
        ({"a"}, r"A few applied the rule the wrong way round $(uv'-vu')/v^2$."),
        ({"a"}, r"Candidates who initially wrote the quotient as $2x^{\frac{3}{2}}+\frac{1}{2}x^{\frac{1}{2}}$ were "
                r"often more successful with the differentiation."),
        ({"a"}, "A few candidates forgot about the 4lnx term but most dealt with this correctly.", NO),
        ({"a"}, "Errors from missing brackets or when simplifying their differentiated expression, in particular "
                "dealing with the powers, meant that many did not gain full marks in this part."),
        ({"b"}, r"In part (b), although almost all candidates made dy/dx = 0 and reached $12x^2+x-16\sqrt{x}=0$ the "
                r"majority then failed to make progress and did not gain any marks."),
        ({"b"}, r"Several made no attempt to rearrange this equation and others made $x^2$, $x$ or $\sqrt{x}$ the "
                r"subject but did not make the key step of dividing by $\sqrt{x}$ first.", BACK),
        ({"c"}, "Part (c) was generally well done, with most candidates getting part (i) correct."),
        ({"c"}, "Some candidates left out part (ii) and a few made an error with their accuracy here, 1.15651 and "
                "1.1565 being seen a few times."),
    ],
    "08": [
        (W, "This question was very well answered, with many candidates gaining full marks."),
        (W, r"Candidates who used the factor theorem (solving $\mathrm{f}(-4)=0$ to find $a=6$, as in the main scheme) "
            r"were more successful than those who attempted long division, which invariably went wrong and in some "
            r"cases resulted in a remainder containing ‘$x$’.", NO),
        (W, r"Typical mistakes included: solving $\mathrm{f}(4)=0$ instead of $\mathrm{f}(-4)=0$ (usually forfeiting 2 "
            r"marks), mistakes in integrating the ‘$ax$’ term and forgetting the constant of integration or adding it "
            r"in at the end.", NO),
        (W, r"It was noted that some candidates were able to score full marks in this question without explicitly "
            r"finding $a$ i.e. by considering $(x+4)(2x^2\ldots\ldots-3)$ and deducing the $x$ coefficient of the "
            r"quadratic directly.", NO),
    ],
    "09": [
        (W, "This question proved to be quite challenging for many candidates and awarding full marks was rare."),
        ({"a"}, "Nonetheless, most candidates recognised the need to set up simultaneous equations in A and B and were "
                "often able to use the information provided in the question to establish at least one equation linking "
                "A and B."),
        ({"a"}, r"Usually problems arose initially with the $18=A-Be^0$ which was frequently incorrectly simplified to "
                r"$18=A$ or sometimes $18=A-1$."),
        ({"a"}, "Indeed, some candidates assumed immediately that A = initial temperature = 18 as is sometimes the case "
                "in modelling questions."),
        ({"a"}, "Such errors proved costly as candidates were then limited to one mark from four in part (a).", BACK),
        ({"a"}, r"It was pleasing to see that most candidates who managed to set up the two equations correctly were "
                r"often unphased by the presence of $e^{-0.7}$ as a coefficient of B.", NO),
        ({"a"}, "Often this was rewritten as a decimal approximation before solving for B.", BACK),
        ({"a"}, "This was acceptable although some candidates did not provide sufficiently accurate approximations and "
                "so lost a mark for values of A and B that were not accurate to 3sf (51.7 and 69.7 were sometimes "
                "seen).", BACK),
        ({"a"}, "Candidates also lost a mark here for being too accurate and giving their final values of A and B to "
                "3dp for example."),
        ({"a"}, "Candidates should be advised to check the question carefully for the required degree of accuracy."),
        ({"a"}, "Unfortunately, it was quite common for candidates to find correct values for A and B but then fail to "
                "state the equation of the model in full which led to the loss of one mark.", NO),
        ({"b"}, "Part (b) was quite discriminating."),
        ({"b"}, r"Occasionally, candidates noted that the maximum temperature according to the model is $69.6^\circ$C "
                r"but the most common approach taken by candidates was to set $\theta(t)=78$ and attempt to solve for "
                r"$t$."),
        ({"b"}, "Some candidates were unable to solve the equation but allowed their work to peter out without "
                "comment."),
        ({"b"}, "However, a good number of candidates correctly noted that a solution was not possible - recognising "
                "that the model would not reach the boiling point of ethanol which was sufficient for one mark."),
        ({"b"}, r"It was also common however to see minus signs conveniently disappear in order to obtain a solution "
                r"for $t$ at all costs.", NO),
        ({"b"}, r"Such candidates usually obtained $t=25.9$ and concluded that the model would be appropriate up to "
                r"this time; or obtained $t=-25.9$ noting that ‘time cannot be negative’.", BACK),
        ({"b"}, "A significant number of responses gave general comments relating to the model being inappropriate once "
                "ethanol’s boiling point was reached - such responses were not creditworthy.", NO),
        ({"b"}, r"Unfortunately, errors in the calculation of A and B from part (a) sometimes resulted in a version of "
                r"$\theta(t)=78$ which could legitimately be solved which precluded the marks in (b)."),
        ({"b"}, r"It was extremely rare to award the second mark in part (b) as candidates almost always failed to "
                r"acknowledge that the model was inappropriate because the maximum value of $69.6^\circ$C is "
                r"significantly lower than the boiling point of $78^\circ$C.", NO),
    ],
    "10": [
        ({"a"}, "Many students were able to get started in part (a) with correct use of cos(2A + A) alongside the "
                "addition formula."),
        ({"a"}, "Candidates who managed this, regularly went on to apply the double angle formulae correctly to achieve "
                "an expression in cosA only.", BACK),
        ({"a"}, r"Often circuitous routes were taken, most notably with the use of cos2A = cos$^2$A - sin$^2$A and then "
                r"making a second substitution for sin$^2$A (this sometimes resulted in bracketing and/or sign "
                r"errors).", NO),
        ({"a"}, "A small number of candidates added a proof for the double angle formulae from the addition formulae "
                "even though this was unnecessary.", NO),
        ({"a"}, "A high proportion of students who managed to get the first mark went on to get at least 3 if not 4 "
                "marks in this part of the question."),
        ({"a"}, "It was very much an all or nothing question with many only getting the first mark.", NO),
        ({"a"}, "A significant number presented their work in a way that was sometimes difficult to follow even if "
                "they did manage to score full marks."),
        ({"a", "b"}, "In part (b), it was common for candidates to achieve no marks for part (a) and then full marks "
                     "for this part.", NO),
        ({"b"}, "Most of the students gained the first method mark and managed to produce an equation in cosx only."),
        ({"b"}, "Mistakes were made with signs and brackets."),
        ({"b"}, "In particular, candidates failed to write brackets around 4cos3x – 3cosx and hence would obtain an "
                "incorrect quadratic equation to solve."),
        ({"b"}, "Several candidates ‘solved’ the cubic/quadratic equation using the polynomial equation function on "
                "their calculator and did not show any evidence of their working."),
        ({"b"}, "Some incorrect equations led to complex solutions but most of these candidates still did not realise "
                "that they had made an error.", NO),
        ({"b"}, "A large number of candidates divided by cosx to simplify their expression but they failed to "
                "recognise this lost a solution and therefore were not awarded the final mark.", NO),
        ({"b"}, "A small number of candidates failed to gain any marks on this part as they replaced the right hand "
                "side with cosx but left the left hand side with cos3x and then proceeded to treat this as a "
                "cubic/quadratic.", NO),
        ({"b"}, "When candidates had identified the correct equation and solutions they were very good at finding all "
                "the solutions in the range."),
        ({"b"}, r"A large number who did get solutions did not include $-90^\circ$ or included $180^\circ$ and "
                r"therefore lost the final mark."),
    ],
    "11": [
        ({"a"}, r"Part (a) of this question was generally well answered, with most candidates being able locate $P$ "
                r"correctly."),
        ({"a"}, r"A few candidates launched into some lengthy algebra, in some cases resulting in values for $x$ and "
                r"$y$ bearing no relation to the position of $P$ on the diagram."),
        ({"b"}, "Answers to part (b) from this cohort of candidates were very disappointing and displayed an "
                "overreliance on algebra and poor understand of modulus graphs.", NO),
        ({"b"}, r"Very few candidates identified $x=-10.6$ as the solution to the equation."),
        ({"b"}, r"Instead most answers wrote down the solution to $3x+40=2(x+4)-5$ $\{x=-37\}$ as well as $x=-10.6$, "
                r"scoring M1A0."),
        ({"b"}, r"A few candidates used a calculator to directly write down the correct value of $x$ to gain both marks "
                r"– perhaps not a bad strategy for students who are weak at modulus graphs."),
        ({"b"}, r"A simple check on a calculator would also have established that only $x=-10.6$ was a solution to the "
                r"printed equation."),
        ({"c"}, "Part [c] of this question was one of the most challenging parts of this paper, with hardly any "
                "candidates gaining all 3 marks."),
        ({"c"}, r"Candidates seemed unable to ‘visualise’ the question and see directly that there would be an "
                r"intersection if $a$ was greater than 2, so the B mark was hardly ever gained (and consequently the A "
                r"mark was immediately lost)."),
        ({"c"}, r"The M mark for considering $P$ and attempting $a=5/4$ was occasionally gained, although as above this "
                r"often entailed long winded algebraic methods e.g. solving simultaneous equations to find $a$.", NO),
    ],
    "12": [
        (W, "Many candidates left the entire question or parts of this question completely blank and clearly found it "
            "difficult to access the content being assessed here, perhaps due to a lack of familiarity with integration "
            "using parametric equations.", NO),
        (W, "Many tried to establish the Cartesian equation to answer various parts."),
        (W, "That said, there were many candidates who provided clear and concise solutions to each part."),
        ({"ai"}, r"In part (a)(i), most candidates recalled the formula for integrating parametric equations and knew "
                 r"to find $\frac{dx}{dt}$."),
        ({"ai"}, "Awareness of the double angle formula for sin2t was good."),
        ({"ai"}, "The main problem caused for these candidates was a lack of “dt” throughout their work, and only "
                 "included this in the final line, losing the final accuracy mark.", BACK),
        ({"ai"}, r"There was a significant proportion of candidates who attempt ed some differentiation using the chain "
                 r"rule: $\frac{dy}{dx}=\frac{dy}{dt}$ x $\frac{dt}{dx}$, scoring no marks."),
        ({"aii"}, r"In part (a)(ii), many knew that the integral was a multiple of $\cos^3t$ but had trouble getting to "
                  r"the printed answer of 20 with correct steps."),
        ({"aii"}, "As the answer was given, it was a requirement to see the limits calculated separately as 0 – ( -20 ) "
                  "= 20.", NO),
        ({"aii"}, "Integration by parts was a common approach for unsuccessful candidates, while others attempted to "
                  "use a substitution, often not using the necessary u = cosx.",
         {"note": r"the mark scheme’s substitution is $u=\cos t$"}),
        ({"aii"}, r"Those candidates with an understanding of the integration of $\mathrm{f}'(x)[\mathrm{f}(x)]^n$ were "
                  r"generally very successful here.", NO),
        ({"aii"}, "Some lost the penultimate accuracy mark usually due to a sign error."),
        ({"b"}, "In part (b) many candidates who had found part (a) difficult gave up and lost the opportunity of "
                "scoring some easier marks."),
        ({"b"}, r"Many candidates who scored no marks elsewhere were still able to access at least the first two marks "
                r"in part (b) by setting $\sin2t=\frac{4.2}{5}$ and solving, frequently getting at least one correct "
                r"angle; but too many of these found their second value of $t$ by subtracting their first value from "
                r"$\pi$ instead of calculating $\pi-\sin^{-1}(0.84)$ before dividing by 2.", NO),
        ({"b"}, "The following mark was for finding two values of x, but many simply substituted their first value in "
                "to find x, thinking that this gave them the width of the walkway.", NO),
        ({"b"}, "Too many marks were lost by approximating too soon and hence not having values with the required "
                "accuracy."),
        ({"b"}, "A few lost the last mark because they omitted the units."),
    ],
    "13": [
        ({"a"}, r"Part (a) was often answered correctly and candidates knew to set the denominator equal to zero and "
                r"solve to obtain a value for $k$."),
        ({"a"}, r"Unfortunately, candidates sometimes left their answer as $x=\mathrm{e}^2$ which was, of course, "
                r"incorrect."),
        ({"a"}, r"Some candidates gave the inexact answer of $k=7.39$ which was condoned."),
        ({"a"}, r"Commonly seen incorrect answers included $k=0$, or $k=1$."),
        ({"a"}, r"A number of candidates gave the value $k=3$ suggesting that the expression in the denominator had "
                r"been incorrectly interpreted as $\ln(x-2)$ rather than $\ln(x)-2$ as was stated."),
        ({"a"}, r"A small number of candidates wrote “there is no $k$ in the question” perhaps failing to spot its "
                r"presence in the domain."),
        ({"b"}, r"Part (b) was attempted by most candidates although it was not uncommon to see attempts to find the "
                r"inverse of $\mathrm{g}(x)$ instead of differentiating.", NO),
        ({"b"}, "The differentiation in part (b) was however correctly carried out by many candidates, with the "
                "majority using the quotient rule."),
        ({"b"}, "Those who stated the correct formula and the individual components of u, v, u’ and v’ were often more "
                "successful.", NO),
        ({"b"}, r"A few used $\left(\frac{dv}{dx}\right)^2$ instead of $v^2$ in the denominator, while others made "
                r"slips on expanding the bracket $3(\ln(x)-2)$."),
        ({"b"}, "Some attempted the product rule, usually with less success."),
        ({"b"}, r"Many candidates did not attempt to simplify the numerator of $\mathrm{g}'(x)$."),
        ({"b"}, "Often those that did made slips and it was frustrating to see candidates losing marks due to missing "
                "brackets and sign errors when expanding.", BACK),
        ({"b"}, r"It was common to see numerators incorrectly simplified to $\frac{-13}{x}$ or $\frac{5}{x}$ although "
                r"many did manage the correct simplification to $\frac{1}{x}$.", NO),
        ({"b"}, r"Some candidates unnecessarily expanded the denominator, sometimes incorrectly writing $\ln(x^2)$ "
                r"instead of $(\ln x)^2$."),
        ({"b"}, r"Candidates who managed to correctly simplify their expression for $\mathrm{g}'(x)$ argued correctly "
                r"why $\mathrm{g}'(x)>0$ for all $x$ in the domain, but some simply stated this with no reason or gave "
                r"an incomplete argument of “$x>0$ so $\mathrm{g}'(x)>0$” and lost the final mark in this part.", NO),
        ({"c"}, r"In part (c), most candidates only gained one out of two available marks as they usually considered "
                r"only the set of values of $a$ for which the numerator is positive by solving $3\ln x-7=0$ to obtain "
                r"$a>e^{\frac{7}{3}}$."),
        ({"c"}, r"Usually no consideration was given to the case where the numerator and denominator are both negative "
                r"and the few that did solve $\ln x=2$ usually failed to state $0<a<e^2$."),
    ],
    "14": [
        ({"a"}, "Part (a) presented some thinking challenges for many candidates, in particular spotting that a = b = r "
                "in their equation for the circle."),
        ({"a"}, "About half of the candidates were not able to deduce the correct equation of the circle."),
        ({"a"}, r"The most commonly seen incorrect equations were $x^2+y^2=r^2$, $(x+r)^2+(y+r)^2=r^2$ and "
                r"$(x\pm a)^2+(y\pm b)^2=r^2$."),
        ({"a"}, r"Some of these candidates managed to gain the method mark for using $y=12-2x$, but a disappointingly "
                r"high number didn’t progress.", BACK),
        ({"a"}, r"Relatively few candidates who initially used $a$ and $b$, correctly replaced them with $r$ to attain "
                r"at least one mark."),
        ({"a"}, "Some candidates tried to use a sketch to help them."),
        ({"a"}, r"This did allow some to identify the centre as $(r, r)$, but many put the circle in the wrong quadrant "
                r"and proceeded to use $(r, -r)$ or $(-r, r)$.", BACK),
        ({"a"}, r"The majority of candidates who gained the B1 and M1 expanded their expressions correctly to give the "
                r"correct equation and attain the A1, although the algebra involved in squaring the 3-term expression "
                r"$(r^2-24r+144)$was not always carried out correctly."),
        ({"a"}, r"Candidates were generally more successful when they expanded $(y-r)^2$ first before substituting "
                r"$y=12-2x$."),
        ({"b"}, "Part (b) proved to be more accessible to most candidates."),
        ({"b"}, "Many recognised the need to use the discriminant and equate to zero, though poor algebraic "
                "manipulation often cost them the accuracy marks."),
        ({"b"}, "Almost all candidates used a calculator to solve the quadratic, though there were examples of the "
                "quadratic formula being used, mainly correctly."),
        ({"b"}, r"A small number resorted to calculus to find a gradient, but very few successfully attempted to "
                r"differentiate their equation and set the gradient to $-2$."),
        ({"b"}, r"A few tried to use the idea of gradient or even equate the equation with $12-2x$."),
    ],
    "15": [
        (W, "A number of the responses were completely blank suggesting perhaps that candidates had run out of time to "
            "complete this question."),
        ({"a"}, "In part (a), very high proportion of the candidates had some idea what the layout of the proof looked "
                "like yet only around 50% were able to complete it accurately and rigorously.", NO),
        ({"a"}, r"There were many solutions containing the final the term of $S_n$ as $ar^n$ rather than $ar^{n-1}$."),
        ({"a"}, "Candidates who had the correct initial sequence regularly went on to complete the proof correctly."),
        ({"a"}, "Only a small number prematurely factorised."),
        ({"a"}, "Some were trying to apply the method of proving the sum of an arithmetic series instead, hence losing "
                "the majority of the marks."),
        ({"b"}, "In part (b), the first method mark was gained by the majority of students."),
        ({"b"}, r"Some didn’t divide by “a” or wrongly cancelled $r^{10}$ and $r^5$ in their equation, so lost the first "
                r"accuracy mark."),
        ({"b"}, "However, many of the students who gained the first two marks continued to gain the last two marks by "
                "dealing with the quadratic and achieving the correct solution for “r”."),
        ({"b"}, "A few candidates used (n - 1) in the formula rather than n and a number of candidates got confused "
                "with n and r, replacing r = 10 and 5 in the denominator of each fraction."),
        ({"b"}, r"Only around 50% realised that they had ended up with a quadratic equation in $r^5$ and candidates "
                r"who did not cancel the “a” out early often ended up with an overcomplicated equation which they "
                r"could not solve."),
        ({"b"}, "Very few did not eliminate r = 1 if they found it, although a few solved the quadratic and then forgot "
                "to cube root the answer and so had r = 3.",
         {"ref": False, "note": r"the quadratic is in $r^5$, so the root needed is a fifth root: the mark scheme’s answer is "
                  r"$r=3^{\frac{1}{5}}$, printed as the fifth root of 3"}),
    ],
    "16": [
        (W, "This was a very poorly answered question, with the majority of candidates not writing anything at all.",
         NO),
        (W, r"A fairly common attempt was to only split the natural numbers into odd/even cases and square $2n$, "
            r"$2n+1$, which gained no marks."),
        (W, "Many students who obtained any marks on this question seemed to stumble on these more by chance than by "
            "considering the problem.", NO),
        (W, r"The problem mentioned that the square was to be a multiple of 3 or one more than a multiple of 3 and many "
            r"students were able to write this as $3n$ and $3n+1$.", NO),
        (W, "Some went on to square these and show that the result was also a multiple of 3 or one more than a "
            "multiple of 3.", BACK),
        (W, r"Few students realised that they needed a third case (e.g. $3n-1$ or $3n+2$) to cover all integers, and as "
            r"a result two marks was the most that could be achieved."),
        (W, "It was very rare to see full marks scored in this question.", NO),
        (W, "Candidates who did gain full marks typically presented model solutions with thorough explanations and "
            "conclusions."),
    ],
}

# Difficulty: (rating, (question, index of the REPORT sentence it rests on)).
RATINGS = {
    "01a": ("easy", ("01", 0)),
    "01b": ("medium", ("01", 5)),
    "01c": ("medium", ("01", 8)),
    "02": ("hard", ("02", 0)),
    "03a": ("easy", ("03", 1)),
    "03b": ("medium", ("03", 13)),
    "04": ("easy", ("04", 0)),
    "05": ("hard", ("05", 1)),
    "06a": ("medium", ("06", 1)),
    "06b": ("easy", ("06", 7)),
    "07a": ("medium", ("07", 4)),
    "07b": ("hard", ("07", 5)),
    "07c": ("easy", ("07", 7)),
    "08": ("easy", ("08", 0)),
    "09a": ("medium", ("09", 10)),
    "09b": ("hard", ("09", 19)),
    "10a": ("medium", ("10", 5)),
    "10b": ("medium", ("10", 16)),
    "11a": ("easy", ("11", 0)),
    "11b": ("hard", ("11", 3)),
    "11c": ("hard", ("11", 7)),
    "12ai": ("medium", ("12", 5)),
    "12aii": ("medium", ("12", 7)),
    "12b": ("hard", ("12", 14)),
    "13a": ("medium", ("13", 0)),
    "13b": ("medium", ("13", 7)),
    "13c": ("medium", ("13", 16)),
    "14a": ("medium", ("14", 1)),
    "14b": ("medium", ("14", 10)),
    "15a": ("medium", ("15", 1)),
    "15b": ("medium", ("15", 8)),
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
