"""Draft builder for 9MA0-02 2018-06 (A level Pure Paper 2, June 2018).

Run (from the project root, with the venv active):
    python extraction/9MA0-02_2018-06.py        # writes out/drafts/9MA0-02_2018-06.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-02_2018-06.json

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

P, S = "9MA0-02", "2018-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "07ii"); label as printed (e.g. "7(ii)")."""
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
NUM = "Numerical methods"
VEC = "Vectors"


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


I, J, K = r"\mathbf{i}", r"\mathbf{j}", r"\mathbf{k}"
NUMONLY = r"(Solutions based entirely on graphical or numerical methods are not acceptable.)"

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q1 = [r"$$\mathrm{g}(x)=\frac{2x+5}{x-3}\qquad x\geqslant5$$"]
Q2 = ["Relative to a fixed origin $O$,",
      rf"the point $A$ has position vector $(2{I}+3{J}-4{K})$,",
      rf"the point $B$ has position vector $(4{I}-2{J}+3{K})$,",
      rf"and the point $C$ has position vector $(a{I}+5{J}-2{K})$, where $a$ is a constant and $a<0$",
      r"$D$ is the point such that $\overrightarrow{AB}=\overrightarrow{BD}$."]
Q5 = [r"The equation $2x^3+x^2-1=0$ has exactly one real root."]
Q5A = [r"Show that, for this equation, the Newton-Raphson formula can be written",
       r"$$x_{n+1}=\frac{4x_n^3+x_n^2+1}{6x_n^2+2x_n}$$"]
Q6 = [r"$$\mathrm{f}(x)=-3x^3+8x^2-9x+10,\quad x\in\mathbb{R}$$"]
Q6A = [r"(a) (i) Calculate $\mathrm{f}(2)$", r"(ii) Write $\mathrm{f}(x)$ as a product of two algebraic factors."]
Q8 = [r"[Figure 1: a graph of $H$ (vertical axis) against $x$ (horizontal axis), with origin $O$; the trajectory is a "
      r"single arch-shaped curve rising from $O$ to a maximum and falling back to meet the positive $x$-axis.]",
      "Figure 1 is a graph showing the trajectory of a rugby ball.",
      r"The height of the ball above the ground, $H$ metres, has been plotted against the horizontal distance, $x$ metres, "
      r"measured from the point where the ball was kicked.",
      "The ball travels in a vertical plane.",
      "The ball reaches a maximum height of 12 metres and hits the ground at a point 40 metres from where it was kicked."]
Q8A = r"Find a quadratic equation linking $H$ with $x$ that models this situation."
Q8BAR = ("The ball passes over the horizontal bar of a set of rugby posts that is perpendicular to the path of the ball. "
         "The bar is 3 metres above the ground.")
Q10 = ["A spherical mint of radius 5 mm is placed in the mouth and sucked. Four minutes later, the radius of the mint is "
       "3 mm.",
       "In a simple model, the rate of decrease of the radius of the mint is inversely proportional to the square of the "
       "radius."]
Q10A = ["Using this model and all the information given,",
        "(a) find an equation linking the radius of the mint and the time. (You should define the variables that you "
        "use.)"]
Q11 = [r"$$\frac{1+11x-6x^2}{(x-3)(1-2x)}\equiv A+\frac{B}{(x-3)}+\frac{C}{(1-2x)}$$"]
Q12A = [r"Prove that", r"$$1-\cos2\theta\equiv\tan\theta\sin2\theta,\quad\theta\neq\frac{(2n+1)\pi}{2},\quad n\in\mathbb{Z}$$"]
Q14 = ["A scientist is studying a population of mice on an island.",
       r"The number of mice, $N$, in the population, $t$ months after the start of the study, is modelled by the equation",
       r"$$N=\frac{900}{3+7\mathrm{e}^{-0.25t}},\quad t\in\mathbb{R},\quad t\geqslant0$$"]
Q14B = (r"Show that the rate of growth $\frac{\mathrm{d}N}{\mathrm{d}t}$ is given by "
        r"$\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{N(300-N)}{1200}$")
Q14T = "The rate of growth is a maximum after $T$ months."

LATEX = {
    "01a": L(*Q1, r"Find $\mathrm{gg}(5)$."),
    "01b": L(*Q1, r"State the range of g."),
    "01c": L(*Q1, r"Find $\mathrm{g}^{-1}(x)$, stating its domain."),
    "02a": L(*Q2, "Find the position vector of $D$."),
    "02b": L(*Q2, r"Given $|\overrightarrow{AC}|=4$", "find the value of $a$."),
    "03a": L(r"“If $m$ and $n$ are irrational numbers, where $m\neq n$, then $mn$ is also irrational.”",
             "Disprove this statement by means of a counter example."),
    "03b": L(r"(i) Sketch the graph of $y=|x|+3$",
             r"(ii) Explain why $|x|+3\geqslant|x+3|$ for all real values of $x$."),
    "04i": L(r"Show that $\displaystyle\sum_{r=1}^{16}(3+5r+2^r)=131\,798$"),
    "04ii": L(r"A sequence $u_1, u_2, u_3, \ldots$ is defined by",
              r"$$u_{n+1}=\frac{1}{u_n},\quad u_1=\frac{2}{3}$$",
              r"Find the exact value of $\displaystyle\sum_{r=1}^{100}u_r$"),
    "05a": L(*Q5, *Q5A),
    "05b": L(*Q5, "(a) " + Q5A[0], Q5A[1], r"Using the formula given in part (a) with $x_1=1$",
             r"(b) find the values of $x_2$ and $x_3$"),
    "05c": L(*Q5, r"Explain why, for this question, the Newton-Raphson method cannot be used with $x_1=0$"),
    "06a": L(*Q6, Q6A[0][4:], Q6A[1]),
    "06b": L(*Q6, *Q6A, "Using the answer to (a)(ii),",
             "(b) prove that there are exactly two real solutions to the equation", r"$$-3y^6+8y^4-9y^2+10=0$$"),
    "06c": L(*Q6, *Q6A, "Using the answer to (a)(ii),",
             r"(c) deduce the number of real solutions, for $7\pi\leqslant\theta<10\pi$, to the equation",
             r"$$3\tan^3\theta-8\tan^2\theta+9\tan\theta-10=0$$"),
    "07i": L(r"Solve, for $0\leqslant x<\frac{\pi}{2}$, the equation", r"$$4\sin x=\sec x$$"),
    "07ii": L(r"Solve, for $0\leqslant\theta<360^\circ$, the equation", r"$$5\sin\theta-5\cos\theta=2$$",
              "giving your answers to one decimal place.", NUMONLY),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, "(a) " + Q8A, Q8BAR,
             "(b) Use your equation to find the greatest horizontal distance of the bar from $O$."),
    "08c": L(*Q8, Q8BAR, "Give one limitation of the model."),
    "09": L(r"Given that $\theta$ is measured in radians, prove, from first principles, that",
            r"$$\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)=-\sin\theta$$",
            r"You may assume the formula for $\cos(A\pm B)$ and that as $h\to0$, $\frac{\sin h}{h}\to1$ and "
            r"$\frac{\cos h-1}{h}\to0$"),
    "10a": L(*Q10, Q10A[0], Q10A[1][4:]),
    "10b": L(*Q10, *Q10A,
             "(b) Hence find the total time taken for the mint to completely dissolve. Give your answer in minutes and "
             "seconds to the nearest second."),
    "10c": L(*Q10, "Suggest a limitation of the model."),
    "11a": L(*Q11, "Find the values of the constants $A$, $B$ and $C$."),
    "11b": L(*Q11, r"$$\mathrm{f}(x)=\frac{1+11x-6x^2}{(x-3)(1-2x)}\qquad x>3$$",
             r"Prove that $\mathrm{f}(x)$ is a decreasing function."),
    "12a": L(*Q12A),
    "12b": L("(a) " + Q12A[0], Q12A[1],
             r"(b) Hence solve, for $-\frac{\pi}{2}<x<\frac{\pi}{2}$, the equation",
             r"$$(\sec^2x-5)(1-\cos2x)=3\tan^2x\sin2x$$",
             "Give any non-exact answer to 3 decimal places where appropriate."),
    "13": L(r"[Figure 2: the curve $C$ starts at $O$, dips just below the $x$-axis, crosses the positive $x$-axis and "
            r"rises steeply; the straight line $l$, with negative gradient, crosses the positive $y$-axis, meets $C$ at "
            r"$P(\mathrm{e}, \mathrm{e})$ and crosses the positive $x$-axis to the right of where $C$ does; the region $R$, "
            r"below $P$ between $C$, $l$ and the $x$-axis, is shaded.]",
            r"Figure 2 shows a sketch of part of the curve $C$ with equation $y=x\ln x,\quad x>0$",
            r"The line $l$ is the normal to $C$ at the point $P(\mathrm{e}, \mathrm{e})$",
            r"The region $R$, shown shaded in Figure 2, is bounded by the curve $C$, the line $l$ and the $x$-axis.",
            r"Show that the exact area of $R$ is $A\mathrm{e}^2+B$ where $A$ and $B$ are rational numbers to be found."),
    "14a": L(*Q14, "Find the number of mice in the population at the start of the study."),
    "14b": L(*Q14, Q14B),
    "14c": L(*Q14, "(b) " + Q14B, Q14T, "(c) Find, according to the model, the value of $T$."),
    "14d": L(*Q14, Q14T, "According to the model, the maximum number of mice on the island is $P$.",
             "State the value of $P$."),
}

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", ALG, "2.8", 2, LATEX["01a"],
      [r"M1 (AO 1.1b): $\mathrm{g}(5)=\frac{2(5)+5}{5-3}=7.5\Rightarrow\mathrm{gg}(5)=\frac{2(\text{“}7.5\text{”})+5}"
       r"{\text{“}7.5\text{”}-3}$. Notes: Full method of attempting $\mathrm{g}(5)$ and substituting the result into g",
       r"A1 (AO 1.1b): $\mathrm{gg}(5)=\frac{40}{9}$ $\left(\text{or }4\frac{4}{9}\text{ or }4.\dot{4}\right)$. Notes: "
       r"Obtains $\frac{40}{9}$ or $4\frac{4}{9}$ or $4.\dot{4}$ or an exact equivalent. Note: Give A0 for 4.4 or 4.444... "
       r"without reference to $\frac{40}{9}$ or $4\frac{4}{9}$ or $4.\dot{4}$",
       r"ALT: (a) Way 2 — M1 (AO 1.1b): $\mathrm{gg}(x)=\frac{2\left(\frac{2x+5}{x-3}\right)+5}{\left(\frac{2x+5}{x-3}"
       r"\right)-3}\Rightarrow\mathrm{gg}(5)=\frac{2\left(\frac{2(5)+5}{(5)-3}\right)+5}{\left(\frac{2(5)+5}{(5)-3}\right)"
       r"-3}$. Notes: Way 2: Attempts to substitute $x=5$ into $\frac{2\left(\frac{2x+5}{x-3}\right)+5}{\left("
       r"\frac{2x+5}{x-3}\right)-3}$, o.e. Note that $\mathrm{gg}(x)=\frac{9x-5}{14-x}$",
       r"ALT: (a) Way 2 — A1 (AO 1.1b): $\mathrm{gg}(5)=\frac{40}{9}$ $\left(\text{or }4\frac{4}{9}\text{ or }4.\dot{4}"
       r"\right)$"],
      False, 2),
    e("01b", "1(b)", ALG, "2.8", 1, LATEX["01b"],
      [r"B1 (AO 1.1b): {Range:} $2<y\leqslant\frac{15}{2}$. Notes: States $2<y\leqslant\frac{15}{2}$ Accept any of "
       r"$2<\mathrm{g}\leqslant\frac{15}{2}$, $2<\mathrm{g}(x)\leqslant\frac{15}{2}$, $\left(2,\frac{15}{2}\right]$. "
       r"Note: Accept $\mathrm{g}(x)>2$ $\textbf{and}$ $\mathrm{g}(x)\leqslant\frac{15}{2}$ o.e."],
      False, 2),
    e("01c", "1(c)", ALG, "2.8", 3, LATEX["01c"],
      [r"M1 (AO 1.1b): $y=\frac{2x+5}{x-3}\Rightarrow yx-3y=2x+5\Rightarrow yx-2x=3y+5$. Notes: Correct method of cross "
       r"multiplication followed by an attempt to collect terms in $x$ or terms in a swapped $y$",
       r"M1 (AO 2.1): $x(y-2)=3y+5\Rightarrow x=\frac{3y+5}{y-2}$ $\left\{\text{or }y=\frac{3x+5}{x-2}\right\}$. Notes: A "
       r"complete method (i.e. as above and also factorising and dividing) to find the inverse",
       r"A1ft (AO 2.5): $\mathrm{g}^{-1}(x)=\frac{3x+5}{x-2},\quad2<x\leqslant\frac{15}{2}$. Notes: Uses correct notation to "
       r"correctly define the inverse function $\mathrm{g}^{-1}$, where the domain of $\mathrm{g}^{-1}$ stated correctly or "
       r"correctly followed through (using correct notation) on the values shown in their range in part (b). Allow "
       r"$\mathrm{g}^{-1}:x\to$. Condone $\mathrm{g}^{-1}=\ldots$ Do not accept $y=\ldots$ Note: Correct notation is required "
       r"when stating the domain of $\mathrm{g}^{-1}(x)$. Allow $2<x\leqslant\frac{15}{2}$ or $\left(2,\frac{15}{2}\right]$ "
       r"Do not allow any of e.g. $2<\mathrm{g}\leqslant\frac{15}{2}$, $2<\mathrm{g}^{-1}(x)\leqslant\frac{15}{2}$ Note: Do "
       r"not allow A1ft for following through their range in (b) to give a domain for $\mathrm{g}^{-1}$ as "
       r"$x\in\mathbb{R}$ Note: If a candidate scores no marks in part (c), but • states the domain of $\mathrm{g}^{-1}$ "
       r"correctly, $\textbf{or}$ • states a domain of $\mathrm{g}^{-1}$ which is correctly followed through on the values "
       r"shown in their range in part (b) then give special case (SC) M1 M0 A0",
       r"ALT: (c) Way 2 — M1 (AO 1.1b): $y=\frac{2x-6+11}{x-3}\Rightarrow y=2+\frac{11}{x-3}\Rightarrow y-2=\frac{11}{x-3}$. "
       r"Notes: Writes $y=\frac{2x+5}{x-3}$ in the form $y=2\pm\frac{k}{x-3}$, $k\neq0$ and rearranges to isolate $y$ and 2 "
       r"on one side of their equation. Note: Allow the equivalent method with $x$ swapped with $y$",
       r"ALT: (c) Way 2 — M1 (AO 2.1): $x-3=\frac{11}{y-2}\Rightarrow x=\frac{11}{y-2}+3$ $\left\{\text{or }y=\frac{11}{x-2}"
       r"+3\right\}$. Notes: A complete method to find the inverse",
       r"ALT: (c) Way 2 — A1ft (AO 2.5): $\mathrm{g}^{-1}(x)=\frac{11}{x-2}+3,\quad2<x\leqslant\frac{15}{2}$. Notes: As in "
       r"Way 1"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", VEC, "10.4, 10.3", 2, LATEX["02a"],
      [r"M1 (AO 3.1a): E.g. $\overrightarrow{OD}=\overrightarrow{OB}+\overrightarrow{BD}=\overrightarrow{OB}+"
       r"\overrightarrow{AB}$ or $\overrightarrow{OD}=\overrightarrow{OB}+\overrightarrow{BD}=\overrightarrow{OB}+"
       r"\overrightarrow{AB}=\overrightarrow{OB}+\overrightarrow{OB}-\overrightarrow{OA}=2\overrightarrow{OB}-"
       r"\overrightarrow{OA}$ or $\overrightarrow{OD}=\overrightarrow{OB}+\overrightarrow{BD}=\overrightarrow{OB}+"
       r"\overrightarrow{AB}=\overrightarrow{OA}+\overrightarrow{AB}+\overrightarrow{AB}=\overrightarrow{OA}+"
       r"2\overrightarrow{AB}$ $=\begin{pmatrix}4\\-2\\3\end{pmatrix}+\begin{pmatrix}4\\-2\\3\end{pmatrix}-"
       r"\begin{pmatrix}2\\3\\-4\end{pmatrix}$ $\left\{=\begin{pmatrix}4\\-2\\3\end{pmatrix}+\begin{pmatrix}2\\-5\\7"
       r"\end{pmatrix}\right\}$ or $=\begin{pmatrix}2\\3\\-4\end{pmatrix}+2\left(\begin{pmatrix}4\\-2\\3\end{pmatrix}-"
       r"\begin{pmatrix}2\\3\\-4\end{pmatrix}\right)$ $\left\{=\begin{pmatrix}2\\3\\-4\end{pmatrix}+2\begin{pmatrix}2\\-5"
       r"\\7\end{pmatrix}\right\}$. Notes: Complete $\textbf{applied}$ strategy to find a vector expression for "
       r"$\overrightarrow{OD}$ Note: Give M0 for subtracting the wrong way wrong to give e.g. $(4" + I + r"-2" + J + r"+3"
       + K + r")+(2" + I + r"+3" + J + r"-4" + K + r")-(4" + I + r"-2" + J + r"+3" + K + r")=(4" + I + r"-2" + J + r"+3"
       + K + r")+(-2" + I + r"+5" + J + r"-7" + K + r")=(2" + I + r"+3" + J + r"-4" + K + r")$ Note: Writing e.g. "
       r"$\overrightarrow{OD}=\overrightarrow{OB}+\overrightarrow{AB}$ or $\overrightarrow{OD}=2\overrightarrow{OB}-"
       r"\overrightarrow{OA}$ with no other work is M0 Note: M1 can be implied for at least two correct components in "
       r"their position vector of $D$",
       r"A1 (AO 1.1b): $=\begin{pmatrix}6\\-7\\10\end{pmatrix}$ or $6" + I + r"-7" + J + r"+10" + K + r"$. Notes: See "
       r"scheme Note: Finding $\textit{coordinates}$, i.e. $(6,-7,10)$ without reference to the correct position vectors "
       r"is A0 Note: Allow M1A1 for writing down $6" + I + r"-7" + J + r"+10" + K + r"$ with no working"],
      False, 4),
    e("02b", "2(b)", VEC, "10.4, 10.2", 3, LATEX["02b"],
      [r"M1 (AO 1.1b): $(a-2)^2+(5-3)^2+(-2--4)^2$. Notes: Finds the difference between $\overrightarrow{OA}$ and "
       r"$\overrightarrow{OC}$, then squares and adds each of the 3 components Note: Ignore labelling",
       r"dM1 (AO 2.1): $\left\{|\overrightarrow{AC}|=4\Rightarrow\right\}(a-2)^2+(5-3)^2+(-2--4)^2=(4)^2$ "
       r"$\Rightarrow(a-2)^2=8\Rightarrow a=\ldots$ or $\Rightarrow a^2-4a-4=0\Rightarrow a=\ldots$. Notes: Complete method "
       r"of $\textit{correctly}$ applying Pythagoras’ Theorem on $|\overrightarrow{AC}|=4$ and using a correct method of "
       r"solving their resulting quadratic equation to find at least one of $a=\ldots$ Note: Condone at least one of "
       r"either awrt 4.8 or awrt $-0.83$ for the dM mark",
       r"A1 (AO 1.1b): (as $a<0\Rightarrow$) $a=2-2\sqrt{2}$ (or $a=2-\sqrt{8}$). Notes: Obtains $\textbf{only one}$ exact "
       r"value, $a=2-2\sqrt{2}$ Note: Writing $a=2\pm2\sqrt{2}$, without evidence of rejecting $a=2+2\sqrt{2}$ is A0 Note: "
       r"Allow exact alternatives such as $2-\sqrt{8}$ or $\frac{4-\sqrt{32}}{2}$ for A1, and isw can be applied Note: "
       r"Writing $a=-0.828\ldots$, without reference to a correct exact value is A0"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", PROOF, "1.1", 2, LATEX["03a"],
      [r"M1 (AO 1.1b): E.g. $m=\sqrt{3}$, $n=\sqrt{12}$. Notes: States or uses any pair of $\textit{different}$ numbers "
       r"that will disprove the statement. E.g. $\sqrt{3}$, $\sqrt{12}$; $\sqrt{2}$, $\sqrt{8}$; $\sqrt{5}$, $-\sqrt{5}$; "
       r"$\frac{1}{\pi}$, $2\pi$; $3\mathrm{e}$, $\frac{4}{5\mathrm{e}}$;",
       r"A1 (AO 2.4): $\{mn=\}\left(\sqrt{3}\right)\left(\sqrt{12}\right)=6$ $\Rightarrow$ statement untrue $\textbf{or}$ 6 "
       r"is not irrational or 6 is rational. Notes: Uses correct reasoning to disprove the given statement, with a correct "
       r"conclusion Note: Writing $(3\mathrm{e})\left(\frac{4}{5\mathrm{e}}\right)=\frac{12}{5}\Rightarrow$ untrue is "
       r"sufficient for M1A1"],
      False, 6),
    e("03b", "3(b)", ALG, "2.7, 1.1", 3, LATEX["03b"],
      [r"B1 (AO 1.1b): (b)(i), (ii) Way 1: [sketch of $y=|x|+3$, with $y=|x+3|$ superimposed, meeting the $x$-axis at "
       r"$\{-3\}$; the graphs meet at 3 on the $y$-axis] V shaped graph {reasonably} symmetrical about the $y$-axis with "
       r"vertical interpret $(0, 3)$ or 3 stated or marked on the positive $y$-axis. Notes: See scheme",
       r"M1 (AO 3.1a): Superimposes the graph of $y=|x+3|$ on top of the graph of $y=|x|+3$. Notes: For constructing a "
       r"method of comparing $|x|+3$ with $|x+3|$. See scheme. Note: Allow M1A1 for $x>0$, $|x|+3=|x+3|$ and for "
       r"$x\leqslant0$, $|x|+3\geqslant|x+3|\geqslant$ Note: Allow M1 for any of • $x$ is positive, $|x|+3=|x+3|$ • $x$ is "
       r"negative, $|x|+3>|x+3|$ • $x>0$, $|x|+3=|x+3|$ • $x\leqslant0$, $|x|+3\geqslant|x+3|$ • $x>0$, $|x|+3$ and $|x+3|$ "
       r"are equal • $x\geqslant0$, $|x|+3$ and $|x+3|$ are equal • when $x\geqslant0$, both graphs are equal • for "
       r"positive values $|x|+3$ and $|x+3|$ are the same Condone for M1 • $x\leqslant0$, $|x|+3>|x+3|$ • $x<0$, "
       r"$|x|+3\geqslant|x+3|$",
       r"A1 (AO 2.4): the graph of $y=|x|+3$ is either the same or above the graph of $y=|x+3|$ {for corresponding values "
       r"of $x$} $\textbf{or}$ when $x\geqslant0$, both graphs are equal (or the same) when $x<0$, the graph of $y=|x|+3$ "
       r"is above the graph of $y=|x+3|$. Notes: Explains fully why $|x|+3\geqslant|x+3|$. See scheme. Note: Do not allow "
       r"either $x>0$, $|x|+3\geqslant|x+3|$ or $x\geqslant0$, $|x|+3\geqslant|x+3|$ as a valid reason Note: $x=0$ (or "
       r"where necessary $x=-3$) need to be considered in their solutions for A1 Note: Do not allow an incorrect "
       r"statement such as $x\leqslant0$, $|x|+3>|x+3|$ for A1",
       r"ALT: (b)(ii) Way 2 — M1 (AO 3.1a): Reason 1: When $x\geqslant0$, $|x|+3=|x+3|$; Reason 2: When $x<0$, "
       r"$|x|+3>|x+3|$. Any one of Reason 1 or Reason 2",
       r"ALT: (b)(ii) Way 2 — A1 (AO 2.4): Both Reason 1 and Reason 2",
       r"ALT: (b)(ii) Way 3 — M1 (AO 3.1a): • For $x>0$, $|x|+3=|x+3|$ • For $-3<x<0$, as $|x|+3>3$ and "
       r"$\{0<\}|x+3|<3$, then $|x|+3>|x+3|$",
       r"ALT: (b)(ii) Way 3 — A1 (AO 2.4): • For $x\leqslant-3$, as $|x|+3=-x+3$ and $|x+3|=-x-3$, then "
       r"$|x|+3>|x+3|$"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04i", "4(i)", SEQ, "4.3, 4.4, 4.5", 4, LATEX["04i"],
      [r"M1 (AO 3.1a): $\left\{\sum_{r=1}^{16}(3+5r+2^r)=\right\}\sum_{r=1}^{16}(3+5r)+\sum_{r=1}^{16}(2^r)$. Notes: Uses "
       r"a correct methodical strategy to enable the given sum, $\sum_{r=1}^{16}(3+5r+2^r)$ to be found Allow M1 for any of "
       r"the following: • expressing the given sum as either $\sum_{r=1}^{16}(3+5r)+\sum_{r=1}^{16}(2^r)$, "
       r"$\sum_{r=1}^{16}3+\sum_{r=1}^{16}(5r)+\sum_{r=1}^{16}(2^r)$ or $\sum_{r=1}^{16}3+5\sum_{r=1}^{16}r+"
       r"\sum_{r=1}^{16}(2^r)$ • attempting to find both $\sum_{r=1}^{16}(3+5r)$ and $\sum_{r=1}^{16}(2^r)$ separately • "
       r"$(3\times16)$ and attempting to find both $\sum_{r=1}^{16}(5r)$ and $\sum_{r=1}^{16}(2^r)$ separately",
       r"M1 (AO 1.1b): $=\frac{16}{2}(2(8)+15(5))$. Notes: Way 1: Correct method for finding the sum of an AP with $a=8$, "
       r"$d=5$, $n=16$ Note: Way 1: Give 2nd M1 for writing $\sum_{r=1}^{16}(3+5r)$ as $\frac{16}{2}(8+83)$",
       r"M1 (AO 1.1b): $+\frac{2(2^{16}-1)}{2-1}$. Notes: Correct method for finding the sum of a GP with $a=2$, $r=2$, "
       r"$n=16$ Note: Give 3rd M1 for writing $\sum_{r=1}^{16}(2^r)$ as $\frac{2(1-2^{16})}{1-2}$ or $2(2^{16}-1)$ or "
       r"$(2^{17}-2)$",
       r"A1* (AO 2.1): $=728+131\,070=131\,798$ *. Notes: For all steps fully shown (with correct formulae used) leading "
       r"to $131\,798$",
       r"ALT: (i) Way 2 — M1 (AO 3.1a): $\left\{\sum_{r=1}^{16}(3+5r+2^r)=\right\}\sum_{r=1}^{16}3+\sum_{r=1}^{16}(5r)+"
       r"\sum_{r=1}^{16}(2^r)$",
       r"ALT: (i) Way 2 — M1 (AO 1.1b): $=(3\times16)+\frac{16}{2}(2(5)+15(5))$. Notes: Way 2: $(3\times16)$ and a correct "
       r"method for finding the sum of an AP Note: Way 2: Give 2nd M1 for writing $\sum_{r=1}^{16}3+\sum_{r=1}^{16}(5r)$ "
       r"as $48+\frac{16}{2}(5+80)$ or $48+680$",
       r"ALT: (i) Way 2 — M1 (AO 1.1b): $+\frac{2(2^{16}-1)}{2-1}$",
       r"ALT: (i) Way 2 — A1* (AO 2.1): $=48+680+131\,070=131\,798$ *",
       r"ALT: (i) Way 3 — M1 (AO 3.1a): Sum $=10+17+26+39+60+97+166+299+560+1077+2106+4159+8260+16457+32846+65619="
       r"131\,798$ *. Notes: At least 6 correct terms $\textbf{and}$ 16 terms shown",
       r"ALT: (i) Way 3 — M1 (AO 1.1b): At least 10 correct terms (may not be 16 terms)",
       r"ALT: (i) Way 3 — M1 (AO 1.1b): At least 15 correct terms (may not be 16 terms)",
       r"ALT: (i) Way 3 — A1* (AO 2.1): All 16 terms correct $\textbf{and}$ an indication that the sum is $131\,798$"],
      False, 8),
    e("04ii", "4(ii)", SEQ, "4.2, 4.3", 3, LATEX["04ii"],
      [r"M1 (AO 1.1b): $\left\{u_1=\frac{2}{3}\right\}$, $u_2=\frac{3}{2}$, $u_3=\frac{2}{3}$, ... $\textit{(can be implied by "
       r"later working)}$. Notes: For some indication that the next two terms of this sequence are $\frac{3}{2}$, "
       r"$\frac{2}{3}$ Note: Allow 1st M1 for $u_2=\frac{3}{2}$ (or equivalent) $\textbf{and}$ $u_3=\frac{2}{3}$ (or "
       r"equivalent) Note: Allow 1st M1 for the first 3 terms written as $\frac{2}{3},\frac{3}{2},\frac{2}{3},\ldots$ Note: "
       r"Allow 1st M1 for the 2nd and 3rd terms written as $\frac{3}{2},\frac{2}{3},\ldots$ in the correct order Note: "
       r"Condone $\frac{2}{3}$ written as 0.66 or awrt 0.67 for the 1st M1 mark",
       r"M1 (AO 2.2a): $\left\{\sum_{r=1}^{100}u_r=\right\}50\left(\frac{2}{3}\right)+50\left(\frac{3}{2}\right)$ or "
       r"$50\left(\frac{2}{3}+\frac{3}{2}\right)$. Notes: For deducing that the sum can be found by applying "
       r"$50\left(\frac{2}{3}\right)+50\left(\frac{3}{2}\right)$ or $50\left(\frac{2}{3}+\frac{3}{2}\right)$, o.e.",
       r"A1 (AO 1.1b): $=\frac{325}{3}$ $\left(\text{or }108\frac{1}{3}\text{ or }108.\dot{3}\text{ or }\frac{1300}{12}"
       r"\text{ or }\frac{650}{6}\right)$. Notes: Obtains $\frac{325}{3}$ or $108\frac{1}{3}$ or $108.\dot{3}$ or an exact "
       r"equivalent Note: Give A0 for 108.3 or 108.333... without reference to $\frac{325}{3}$ or $108\frac{1}{3}$ or "
       r"$108.\dot{3}$"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", NUM, "9.3, 7.2", 3, LATEX["05a"],
      [r"B1 (AO 1.1b): $\left\{\mathrm{f}(x)=2x^3+x^2-1\Rightarrow\right\}\mathrm{f}'(x)=6x^2+2x$. Notes: States that "
       r"$\mathrm{f}'(x)=6x^2+2x$ or states that $\mathrm{f}'(x_n)=6x_n^2+2x_n$ (Condone $\frac{\mathrm{d}y}{\mathrm{d}x}="
       r"6x^2+2x$) Note: Allow B1 if $\mathrm{f}'(x)=6x^2+2x$ is applied as $\mathrm{f}'(x_n)$ (or $\mathrm{f}'(x)$) in the "
       r"NR formula $\{x_{n+1}=\}x_n-\frac{\mathrm{f}(x_n)}{\mathrm{f}'(x_n)}$",
       r"M1 (AO 1.1b): $\left\{x_{n+1}=x_n-\frac{\mathrm{f}(x_n)}{\mathrm{f}'(x_n)}\Rightarrow\right\}\{x_{n+1}\}=x_n-"
       r"\frac{2x_n^3+x_n^2-1}{6x_n^2+2x_n}$. Notes: Substitutes $\mathrm{f}(x_n)=2x_n^3+x_n^2-1$ and their "
       r"$\mathrm{f}'(x_n)$ into $x_{n+1}=x_n-\frac{\mathrm{f}(x_n)}{\mathrm{f}'(x_n)}$ Note: Condone "
       r"$x=x-\frac{2x^3+x^2-1}{\text{“}6x^2+2x\text{”}}$ for M1 Note: Condone $x_n-\frac{2x_n^3+x_n^2-1}{\text{“}6x_n^2+"
       r"2x_n\text{”}}$ or $x-\frac{2x^3+x^2-1}{\text{“}6x^2+2x\text{”}}$ (i.e. no $x_{n+1}=\ldots$) for M1 Note: Give M0 "
       r"for $x_{n+1}=x_n-\frac{\mathrm{f}(x_n)}{\mathrm{f}'(x_n)}$ followed by $x_{n+1}=2x_n^3+x_n^2-1-"
       r"\frac{2x_n^3+x_n^2-1}{6x_n^2+2x_n}$",
       r"A1* (AO 2.1): $=\frac{x_n(6x_n^2+2x_n)-(2x_n^3+x_n^2-1)}{6x_n^2+2x_n}\Rightarrow x_{n+1}=\frac{4x_n^3+x_n^2+1}"
       r"{6x_n^2+2x_n}$ *. Notes: A correct intermediate step of making a common denominator which leads to the given "
       r"answer Note: Allow M1A1 for • $x_{n+1}=x-\frac{2x^3+x^2-1}{6x^2+2x}=\frac{x(6x^2+2x)-(2x^3+x^2-1)}{6x^2+2x}"
       r"\Rightarrow x_{n+1}=\frac{4x_n^3+x_n^2+1}{6x_n^2+2x_n}$ Note: Correct notation, i.e. $x_{n+1}$ and $x_n$ must be "
       r"seen in their final answer for A1*"],
      False, 10),
    e("05b", "5(b)", NUM, "9.3", 2, LATEX["05b"],
      [r"M1 (AO 1.1b): $\{x_1=1\Rightarrow\}$ $x_2=\frac{4(1)^3+(1)^2+1}{6(1)^2+2(1)}$ or $x_2=1-\frac{2(1)^3+(1)^2-1}"
       r"{6(1)^2+2(1)}$. Notes: An attempt to use the given or their formula once. Can be implied by "
       r"$\frac{4(1)^3+(1)^2+1}{6(1)^2+2(1)}$ or 0.75 o.e. Note: Allow one slip in substituting $x_1=1$",
       r"A1 (AO 1.1b): $\Rightarrow x_2=\frac{3}{4}$, $x_3=\frac{2}{3}$. Notes: $x_2=\frac{3}{4}$ and $x_3=\frac{2}{3}$ "
       r"Note: Condone $x_2=\frac{3}{4}$ and $x_3=$ awrt 0.667 for A1 Note: Condone $\frac{3}{4},\frac{2}{3}$ listed in a "
       r"correct order ignoring subscripts"],
      False, 10),
    e("05c", "5(c)", NUM, "9.3", 1, LATEX["05c"],
      [r"B1 (AO 2.3): Accept any reasons why the Newton-Raphson $\textbf{method}$ cannot be used with $x_1=0$ which refer "
       r"or $\textit{allude}$ to either the stationary point or the tangent. E.g. • There is a stationary point at $x=0$ • "
       r"Tangent to the curve (or $y=2x^3+x^2-1$) would not meet the $x$-axis • Tangent to the curve (or $y=2x^3+x^2-1$) "
       r"is horizontal. Notes: See scheme Note: Give B0 for the following isolated reasons: e.g. • You cannot divide by 0 "
       r"• The fraction (or the NR formula) is undefined at $x=0$ • At $x=0$, $\mathrm{f}'(x_1)=0$ • $x_1$ cannot be 0 • "
       r"$6x^2+2x$ cannot be 0 • the denominator is 0 which cannot happen • if $x_1=0$, $6x^2+2x=0$"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", ALG, "2.6", 3, LATEX["06a"],
      [r"B1 (AO 1.1b): (i) $\{\mathrm{f}(2)=-24+32-18+10\Rightarrow\}$ $\mathrm{f}(2)=0$. Notes: $\mathrm{f}(2)=0$ or 0 "
       r"stated by itself in part (a)(i)",
       r"M1 (AO 2.2a): (ii) $\{\mathrm{f}(x)=\}$ $(x-2)(-3x^2+2x-5)$ or $(2-x)(3x^2-2x+5)$. Notes: Deduces that $(x-2)$ or "
       r"$(2-x)$ is a factor and attempts to find the other quadratic factor by • using long division to obtain either "
       r"$\pm3x^2\pm kx+\ldots$, $k=$ value $\neq0$ or $\pm3x^2\pm\alpha x+\beta$, $\beta=$ value $\neq0$, $\alpha$ can be 0 "
       r"• factorising to obtain their quadratic factor in the form $(\pm3x^2\pm kx\pm c)$, $k=$ value $\neq0$, $c$ can be "
       r"0, or in the form $(\pm3x^2\pm\alpha x\pm\beta)$, $\beta=$ value $\neq0$, $\alpha$ can be 0",
       r"A1 (AO 1.1b): (ii) $(x-2)(-3x^2+2x-5)$ or $(2-x)(3x^2-2x+5)$. Notes: $(x-2)(-3x^2+2x-5)$, $(2-x)(3x^2-2x+5)$ or "
       r"$-(x-2)(3x^2-2x+5)$ stated together as a product"],
      False, 12),
    e("06b", "6(b)", ALG, "2.3, 2.6, 1.1", 2, LATEX["06b"],
      [r"M1 (AO 2.4): $-3y^6+8y^4-9y^2+10=0\Rightarrow(y^2-2)(-3y^4+2y^2-5)=0$ Gives a partial explanation by • explaining "
       r"that $-3y^4+2y^2-5=0$ has no {real} solutions with a reason, e.g. $b^2-4ac=(2)^2-4(-3)(-5)=-56<0$ • or stating "
       r"that $y^2=2$ has 2 {real} solutions or $y=\pm\sqrt{2}$ {only}. Notes: See scheme Note: Correct calculation e.g. "
       r"$(2)^2-4(-3)(-5)$, $4-60$ or $-56$ must be given for the first explanation Note: Note that M1 can be allowed for • "
       r"a correct follow through calculation for the discriminant of their “$-3y^4+2y^2-5$” which would lead to a value "
       r"$<0$ together with an explanation that $-3y^4+2y^2-5=0$ has no {real} solutions • $\textbf{or}$ for the omission "
       r"of $<0$ Note: $y^2=2\Rightarrow y=\pm2$, so 2 solutions is not allowed for A1, but can be condoned for M1 Note: "
       r"Using the formula on $-3y^4+2y^2-5=0$ or $-3x^2+2x-5=0$ gives $y^2$ or $x=\frac{-2\pm\sqrt{-56}}{-6}$ or "
       r"$\frac{-1\pm\sqrt{-14}}{-3}$ Note: Completing the square on $-3x^2+2x-5=0$ gives $x^2-\frac{2}{3}x+\frac{5}{3}=0"
       r"\Rightarrow\left(x-\frac{1}{3}\right)^2-\frac{1}{9}+\frac{5}{3}=0\Rightarrow x=\frac{1}{3}\pm\sqrt{\frac{-14}{9}}$",
       r"A1 (AO 2.1): Complete proof that the given equation has exactly two {real} solutions. Notes: See scheme. Proof "
       r"must be correct $\textit{with no errors}$, e.g. giving an incorrect discriminant value Note: $<0$ must also been "
       r"stated in a discriminant method for A1 Note: Do not allow A1 for incorrect working, e.g. "
       r"$(2)^2-4(-3)(-5)=-54<0$ Note: Do not recover work for part (b) in part (c)"],
      False, 12),
    e("06c", "6(c)", TRIG, "5.7, 5.3, 2.6", 1, LATEX["06c"],
      [r"B1 (AO 2.2a): $3\tan^3\theta-8\tan^2\theta+9\tan\theta-10=0$; $7\pi\leqslant\theta<10\pi$ {Deduces that} there "
       r"are 3 solutions. Notes: See scheme Note: Give B0 for stating $\theta=$ awrt 23.1, awrt 26.2, awrt 29.4 "
       r"$\textbf{without}$ reference to 3 solutions"],
      False, 12),

    # ---------------- Q7 ----------------
    e("07i", "7(i)", TRIG, "5.7, 5.4, 5.6", 4, LATEX["07i"],
      [r"B1 (AO 1.2): For $\sec x=\frac{1}{\cos x}$. Notes: For recalling that $\sec x=\frac{1}{\cos x}$",
       r"M1 (AO 3.1a): $\{4\sin x=\sec x\Rightarrow\}$ $4\sin x\cos x=1\Rightarrow2\sin2x=1\Rightarrow\sin2x=\frac{1}{2}$. "
       r"Notes: Correct strategy of • Way 1: applying $\sin2x=2\sin x\cos x$ and proceeding to $\sin2x=k$, $|k|\leqslant1$, "
       r"$k\neq0$",
       r"dM1 (AO 1.1b): $x=\frac{1}{2}\arcsin\left(\frac{1}{2}\right)$ or $\frac{1}{2}\left(\pi-\arcsin\left(\frac{1}{2}"
       r"\right)\right)$. Notes: Uses the correct order of operations to find at least one value for $x$ in either radians "
       r"or degrees Note: Give dM1 for $\sin2x=\frac{1}{2}\Rightarrow$ any of $\frac{\pi}{12},\frac{5\pi}{12}$, $15^\circ$, "
       r"$75^\circ$, awrt 0.26 or awrt 1.3",
       r"A1 (AO 1.1b): $\Rightarrow x=\frac{\pi}{12},\frac{5\pi}{12}$. Notes: Clear reasoning to achieve both "
       r"$x=\frac{\pi}{12},\frac{5\pi}{12}$ and no other values in the range $0\leqslant x<\frac{\pi}{2}$ Note: Give "
       r"special case, SC B1M0M0A0 for writing down any of $\frac{\pi}{12},\frac{5\pi}{12}$, $15^\circ$ or $75^\circ$ with "
       r"no working",
       r"ALT: (i) Way 2 — B1 (AO 1.2): For $\sec x=\frac{1}{\cos x}$",
       r"ALT: (i) Way 2 — M1 (AO 3.1a): $\{4\sin x=\sec x\Rightarrow\}$ $4\sin x\cos x=1\Rightarrow16\sin^2x\cos^2x=1$; "
       r"$16\sin^2x(1-\sin^2x)=1$ | $16(1-\cos^2x)\cos^2x=1$; $16\sin^4x-16\sin^2x+1=0$ | $16\cos^4x-16\cos^2x+1=0$; "
       r"$\sin^2x$ or $\cos^2x=\frac{16\pm\sqrt{192}}{32}$ $\left\{=\frac{2\pm\sqrt{3}}{4}\text{ or }0.933\ldots,"
       r"0.066\ldots\right\}$. Notes: Way 2: squaring both sides, applying $\cos^2x+\sin^2x=1$ and solving a quadratic "
       r"equation in either $\sin^2x$ or $\cos^2x$ to give $\sin^2x=k$ or $\cos^2x=k$, $|k|\leqslant1$, $k\neq0$",
       r"ALT: (i) Way 2 — dM1 (AO 1.1b): $x=\arcsin\left(\sqrt{\frac{2\pm\sqrt{3}}{4}}\right)$ or $x=\arccos\left("
       r"\sqrt{\frac{2\pm\sqrt{3}}{4}}\right)$",
       r"ALT: (i) Way 2 — A1 (AO 1.1b): $\Rightarrow x=\frac{\pi}{12},\frac{5\pi}{12}$"],
      False, 16),
    e("07ii", "7(ii)", TRIG, "5.7, 5.6, 5.5", 5, LATEX["07ii"],
      [r"M1 (AO 3.1a): Complete strategy, i.e. • Expresses $5\sin\theta-5\cos\theta=2$ in the form "
       r"$R\sin(\theta-\alpha)=2$, finds both $R$ and $\alpha$, and proceeds to $\sin(\theta-\alpha)=k$, $|k|<1$, $k\neq0$ "
       r"• Applies $(5\sin\theta-5\cos\theta)^2=2^2$, followed by applying both $\cos^2\theta+\sin^2\theta=1$ and "
       r"$\sin2\theta=2\sin\theta\cos\theta$ to proceed to $\sin2\theta=k$, $|k|<1$, $k\neq0$. Notes: See scheme Note: "
       r"Alternative strategy: Expresses $5\sin\theta-5\cos\theta=2$ in the form $R\cos(\theta+\alpha)=-2$, finds both $R$ "
       r"and $\alpha$, and proceeds to $\cos(\theta+\alpha)=k$, $|k|<1$, $k\neq0$",
       r"M1 (AO 1.1b): $R=\sqrt{50}$; $\tan\alpha=1\Rightarrow\alpha=45^\circ$. Notes: Either • uses $R\sin(\theta-\alpha)$ "
       r"to find the values of both $R$ and $\alpha$ • attempts to apply $(5\sin\theta-5\cos\theta)^2=2^2$, uses "
       r"$\cos^2\theta+\sin^2\theta=1$ and proceeds to find an equation of the form $\pm\lambda\pm\mu\sin2\theta=\pm\beta$ "
       r"or $\pm\mu\sin2\theta=\pm\beta$; $\mu\neq0$ • attempts to apply $(5\sin\theta)^2=(2+5\cos\theta)^2$ or "
       r"$(5\sin\theta-2)^2=(5\cos\theta)^2$ and uses $\cos^2\theta+\sin^2\theta=1$ to form an equation in $\cos\theta$ "
       r"only or $\sin\theta$ only",
       r"A1 (AO 1.1b): $\sin(\theta-45^\circ)=\frac{2}{\sqrt{50}}$. Notes: For $\sin(\theta-45^\circ)=\frac{2}{\sqrt{50}}$, "
       r"o.e., $\cos(\theta+45^\circ)=-\frac{2}{\sqrt{50}}$, o.e. or $\sin2\theta=\frac{21}{25}$, o.e. or "
       r"$\cos\theta=\frac{-20\pm\sqrt{4600}}{100}$, o.e. or $\cos\theta=$ awrt 0.48, awrt $-0.88$ or "
       r"$\sin\theta=\frac{20\pm\sqrt{4600}}{100}$, o.e., or $\sin\theta=$ awrt 0.88, awrt $-0.48$ Note: "
       r"$\sin(\theta-45^\circ)$, $\cos(\theta+45^\circ)$, $\sin2\theta$ must be made the subject for A1",
       r"dM1 (AO 1.1b): dependent on the first M mark e.g. $\theta=\arcsin\left(\frac{2}{\sqrt{50}}\right)+45^\circ$. "
       r"Notes: dependent on the first M mark Uses the correct order of operations to find at least one value for $x$ in "
       r"either degrees or radians Note: dM1 can also be given for $\theta=180^\circ-\arcsin\left(\frac{2}{\sqrt{50}}"
       r"\right)+45^\circ$ or $\theta=\frac{1}{2}\left(180^\circ-\arcsin\left(\frac{21}{25}\right)\right)$",
       r"A1 (AO 2.1): $\theta=$ awrt $61.4^\circ$, awrt $208.6^\circ$. Notes: Clear reasoning to achieve both $\theta=$ awrt "
       r"$61.4^\circ$, awrt $208.6^\circ$ and no other values in the range $0\leqslant\theta<360^\circ$ Note: Give "
       r"M0M0A0M0A0 for writing down any of $\theta=$ awrt $61.4^\circ$, awrt $208.6^\circ$ with no working Note: Working "
       r"in radians does not affect any of the first 4 marks",
       r"ALT: (ii) second column — M1 (AO 1.1b): $(5\sin\theta-5\cos\theta)^2=2^2\Rightarrow25\sin^2\theta+25\cos^2\theta"
       r"-50\sin\theta\cos\theta=4\Rightarrow25-25\sin2\theta=4$",
       r"ALT: (ii) second column — A1 (AO 1.1b): $\sin2\theta=\frac{21}{25}$",
       r"ALT: (ii) second column — dM1 (AO 1.1b): dependent on the first M mark e.g. "
       r"$\theta=\frac{1}{2}\left(\arcsin\left(\frac{21}{25}\right)\right)$",
       r"ALT: (ii) Alt 1 — M1 (AO 3.1a): Complete strategy, i.e. • Attempts to apply $(5\sin\theta)^2=(2+5\cos\theta)^2$ "
       r"or $(5\sin\theta-2)^2=(5\cos\theta)^2$ followed by applying $\cos^2\theta+\sin^2\theta=1$ and solving a quadratic "
       r"equation in either $\sin\theta$ or $\cos\theta$ to give at least one of $\sin\theta=k$ or $\cos\theta=k$, "
       r"$|k|<1$, $k\neq0$",
       r"ALT: (ii) Alt 1 — M1 (AO 1.1b): e.g. $25\sin^2\theta=4+20\cos\theta+25\cos^2\theta\Rightarrow25(1-\cos^2\theta)="
       r"4+20\cos\theta+25\cos^2\theta$ $\textbf{or}$ e.g. $25\sin^2\theta-20\sin\theta+4=25\cos^2\theta\Rightarrow"
       r"25\sin^2\theta-20\sin\theta+4=25(1-\sin^2\theta)$; $50\cos^2\theta+20\cos\theta-21=0$ | "
       r"$50\sin^2\theta-20\sin\theta-21=0$",
       r"ALT: (ii) Alt 1 — A1 (AO 1.1b): $\cos\theta=\frac{-20\pm\sqrt{4600}}{100}$, o.e. | "
       r"$\sin\theta=\frac{20\pm\sqrt{4600}}{100}$, o.e.",
       r"ALT: (ii) Alt 1 — dM1 (AO 1.1b): dependent on the first M mark e.g. $\theta=\arccos\left(\frac{-2+\sqrt{46}}{10}"
       r"\right)$ | e.g. $\theta=\arcsin\left(\frac{2+\sqrt{46}}{10}\right)$",
       r"ALT: (ii) Alt 1 — A1 (AO 2.1): $\theta=$ awrt $61.4^\circ$, awrt $208.6^\circ$",
       r"ALT: Alternative solutions (to be marked in the same way as Alt 1): $5\sin\theta-5\cos\theta=2\Rightarrow"
       r"5\tan\theta-5=2\sec\theta\Rightarrow(5\tan\theta-5)^2=(2\sec\theta)^2\Rightarrow25\tan^2\theta-50\tan\theta+25="
       r"4\sec^2\theta\Rightarrow25\tan^2\theta-50\tan\theta+25=4(1+\tan^2\theta)\Rightarrow21\tan^2\theta-50\tan\theta+21"
       r"=0\Rightarrow\tan\theta=\frac{50\pm\sqrt{736}}{42}=\frac{25\pm2\sqrt{46}}{21}=1.8364\ldots,0.5445\ldots\Rightarrow"
       r"\theta=$ awrt $61.4^\circ$, awrt $208.6^\circ$ only",
       r"ALT: Alternative solutions (to be marked in the same way as Alt 1): $5\sin\theta-5\cos\theta=2\Rightarrow"
       r"5-5\cot\theta=2\operatorname{cosec}\theta\Rightarrow(5-5\cot\theta)^2=(2\operatorname{cosec}\theta)^2\Rightarrow"
       r"25-50\cot\theta+25\cot^2\theta=4\operatorname{cosec}^2\theta\Rightarrow25-50\cot\theta+25\cot^2\theta="
       r"4(1+\cot^2\theta)\Rightarrow21\cot^2\theta-50\cot\theta+21=0\Rightarrow\cot\theta=\frac{50\pm\sqrt{736}}{42}="
       r"\frac{25\pm2\sqrt{46}}{21}=1.8364\ldots,0.5445\ldots\Rightarrow\theta=$ awrt $61.4^\circ$, awrt $208.6^\circ$ "
       r"only"],
      False, 16),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", ALG, "2.11, 2.3", 3, LATEX["08a"],
      [r"M1 (AO 3.3): $H=Ax(40-x)$ {or $H=Ax(x-40)$}. Notes: Translates the situation given into a suitable equation for "
       r"the model. E.g. Way 1: {Uses $(0, 0)$ and $(40, 0)$ to write} $H=Ax(40-x)$ o.e. {or $H=Ax(x-40)$} Note: Condone "
       r"writing $y$ in place of $H$ for the M1 and dM1 marks. Note: Give special case M1dM0A0 for writing down any of "
       r"$H=12-(x-20)^2$ or $H=x(40-x)$ or $H=x(x-40)$",
       r"dM1 (AO 3.1b): $x=20$, $H=12\Rightarrow12=A(20)(40-20)\Rightarrow A=\frac{3}{100}$. Notes: Applies a complete "
       r"strategy with appropriate constraints to find all constants in their model. Way 1: Uses $(20, 12)$ on their model "
       r"and finds $A=\ldots$ Note: Give M1 dM1 for finding $-0.03x^2+1.2x$ or $a=-0.03$, $b=1.2$, $c=0$ in an implied "
       r"$ax^2+bx$ or $ax^2+bx+c$ (with no indication of $H=\ldots$)",
       r"A1 (AO 1.1b): $H=\frac{3}{100}x(40-x)$ or $H=-\frac{3}{100}x(x-40)$. Notes: Finds a correct equation linking $H$ to "
       r"$x$ E.g. $H=\frac{3}{100}x(40-x)$, $H=12-\frac{3}{100}(x-20)^2$ or $H=-0.03x^2+1.2x$ Note: Give final A0 for "
       r"$y=-0.03x^2+1.2x$",
       r"ALT: (a) Way 2 — M1 (AO 3.3): $H=12-\lambda(x-20)^2$ {or $H=12+\lambda(x-20)^2$}. Notes: Way 2: {Uses $(20, 12)$ "
       r"to write} $H=12-\lambda(x-20)^2$ or $H=12+\lambda(x-20)^2$",
       r"ALT: (a) Way 2 — dM1 (AO 3.1b): $x=40$, $H=0\Rightarrow0=12-\lambda(40-20)^2\Rightarrow\lambda=\frac{3}{100}$. "
       r"Notes: Way 2: Uses either $(40, 0)$ or $(0, 0)$ on their model to find $\lambda=\ldots$",
       r"ALT: (a) Way 2 — A1 (AO 1.1b): $H=12-\frac{3}{100}(x-20)^2$",
       r"ALT: (a) Way 3 — M1 (AO 3.3): $H=ax^2+bx+c$ (or deduces $H=ax^2+bx$) $\textbf{Both}$ $x=0$, $H=0\Rightarrow0=0+0+c"
       r"\Rightarrow c=0$ $\textbf{and either}$ $x=40$, $H=0\Rightarrow0=1600a+40b$ $\textbf{or}$ $x=20$, $H=12\Rightarrow"
       r"12=400a+20b$ $\textbf{or}$ $\frac{-b}{2a}=20$ $\{\Rightarrow b=-40a\}$. Notes: Way 3: Writes $H=ax^2+bx+c$, "
       r"$\textbf{and}$ uses $(0, 0)$ to deduce $c=0$ $\textbf{and}$ an attempt at using either $(40, 0)$ or $(20, 12)$ "
       r"Special Case: Allow SC M1dM0A0 for not deducing $c=0$ but attempting to apply both $(40, 0)$ and $(20, 12)$",
       r"ALT: (a) Way 3 — dM1 (AO 3.1b): $b=-40a\Rightarrow12=400a+20(-40a)\Rightarrow a=-0.03$ so $b=-40(-0.03)=1.2$. "
       r"Notes: Way 3: Uses $(40, 0)$ and $(20, 12)$ on their model to find $a=\ldots$ and $b=\ldots$",
       r"ALT: (a) Way 3 — A1 (AO 1.1b): $H=-0.03x^2+1.2x$"],
      True, 20),
    e("08b", "8(b)", ALG, "2.11, 2.3", 3, LATEX["08b"],
      [r"M1 (AO 3.4): $\{H=3\Rightarrow\}$ $3=\frac{3}{100}x(40-x)\Rightarrow x^2-40x+100=0$ or $\{H=3\Rightarrow\}$ "
       r"$3=12-\frac{3}{100}(x-20)^2\Rightarrow(x-20)^2=300$. Notes: Substitutes $H=3$ into their quadratic equation and "
       r"proceeds to obtain a 3TQ or a quadratic in the form $(x\pm\alpha)^2=\beta$; $\alpha,\beta\neq0$ Note: E.g. "
       r"$1.2x-0.03x^2=3$ or $40x-x^2=100$ are acceptable for the 1st M mark Note: Give M0 dM0 A0 for (their "
       r"$A)x^2=3\Rightarrow x=\ldots$ or their (their $A)x^2+(\text{their }k)=3\Rightarrow x=\ldots$ Note: Condone the use "
       r"of inequalities for the method marks in part (b)",
       r"dM1 (AO 1.1b): e.g. $x=\frac{40\pm\sqrt{1600-4(1)(100)}}{2(1)}$ or $x=20\pm\sqrt{300}$. Notes: Correct method of "
       r"solving their quadratic equation to give $\textit{at least one solution}$",
       r"A1 (AO 3.2a): $\left\{\text{chooses }20+\sqrt{300}\Rightarrow\right\}$ greatest distance $=$ awrt 37.3 m. Notes: "
       r"Interprets their solution in the original context by selecting the larger correct value $\textit{and states correct "
       r"units for their value}$. E.g. Accept awrt 37.3 m or $\left(20+\sqrt{300}\right)$ m or $\left(20+10\sqrt{3}\right)$ "
       r"m"],
      True, 20),
    e("08c", "8(c)", ALG, "2.11", 1, LATEX["08c"],
      [r"B1 (AO 3.5b): Gives a limitation of the model. Accept e.g. • the ground is horizontal • the ball needs to be kicked "
       r"from the ground • the ball is modelled as a particle • the horizontal bar needs to be modelled as a line • there "
       r"is no wind or air resistance on the ball • there is no spin on the ball • no obstacles in the trajectory (or path) "
       r"of the ball • the trajectory of the ball is a perfect parabola. Notes: See scheme Note: Give no credit for the "
       r"following reasons • $H$ (or the height of ball) is negative when $x>40$ • Bounce of the ball should be considered "
       r"after hitting the ground • Model will not be true for a different rugby ball • Ball may not be kicked in the same "
       r"way each time"],
      True, 20),

    # ---------------- Q9 ----------------
    e("09", "9", DIFF, "7.1, 5.6", 5, LATEX["09"],
      [r"B1 (AO 2.1): $\frac{\cos(\theta+h)-\cos\theta}{h}$. Notes: Gives the correct fraction such as "
       r"$\frac{\cos(\theta+h)-\cos\theta}{h}$ or $\frac{\cos(\theta+\delta\theta)-\cos\theta}{\delta\theta}$ Allow "
       r"$\frac{\cos(\theta+h)-\cos\theta}{(\theta+h)-\theta}$ o.e. Note: $\cos(\theta+h)$ or $\cos(\theta+\delta\theta)$ "
       r"may be expanded Note: In this question $\delta\theta$ may be used in place of $h$ Note: Condone "
       r"$\mathrm{f}'(\theta)$ where $\mathrm{f}(\theta)=\cos\theta$ or $\frac{\mathrm{d}y}{\mathrm{d}\theta}$ where "
       r"$y=\cos\theta$ used in place of $\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)$ Note: Condone $x$ used in place "
       r"of $\theta$ if this is done consistently",
       r"M1 (AO 1.1b): $=\frac{\cos\theta\cos h-\sin\theta\sin h-\cos\theta}{h}$. Notes: Uses the compound angle formula for "
       r"$\cos(\theta+h)$ to give $\cos\theta\cos h\pm\sin\theta\sin h$",
       r"A1 (AO 1.1b): $=\frac{\cos\theta\cos h-\sin\theta\sin h-\cos\theta}{h}$ $\left\{=-\frac{\sin h}{h}\sin\theta+"
       r"\left(\frac{\cos h-1}{h}\right)\cos\theta\right\}$. Notes: Achieves $\frac{\cos\theta\cos h-\sin\theta\sin h-"
       r"\cos\theta}{h}$ or equivalent",
       r"dM1 (AO 2.1): As $h\to0$, $-\frac{\sin h}{h}\sin\theta+\left(\frac{\cos h-1}{h}\right)\cos\theta\to-1\sin\theta+"
       r"0\cos\theta$. Notes: $\textbf{dependent on both the B and M marks being awarded}$ Complete attempt to apply the "
       r"given limits to the gradient of their chord Note: They must isolate $\frac{\sin h}{h}$ and "
       r"$\left(\frac{\cos h-1}{h}\right)$, and replace $\frac{\sin h}{h}$ with 1 and replace "
       r"$\left(\frac{\cos h-1}{h}\right)$ with 0",
       r"A1* (AO 2.5): so $\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)=-\sin\theta$ *. Notes: cso. Uses correct "
       r"mathematical language of limiting arguments to prove $\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)=-\sin\theta$ "
       r"Note: Acceptable responses for the final A mark include: • $\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)="
       r"\lim_{h\to0}\left(-\frac{\sin h}{h}\sin\theta+\left(\frac{\cos h-1}{h}\right)\cos\theta\right)=-1\sin\theta+"
       r"0\cos\theta=-\sin\theta$ • Gradient of chord $=-\frac{\sin h}{h}\sin\theta+\left(\frac{\cos h-1}{h}\right)"
       r"\cos\theta$. As $h\to0$, gradient of chord tends to the gradient of the curve, so derivative is $-\sin\theta$ • "
       r"Gradient of chord $=-\frac{\sin h}{h}\sin\theta+\left(\frac{\cos h-1}{h}\right)\cos\theta$. As $h\to0$, gradient "
       r"of $\textit{curve}$ is $-\sin\theta$ Note: Give final A0 for the following example which shows $\textit{no limiting "
       r"arguments}$: when $h=0$, $\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)=-\frac{\sin h}{h}\sin\theta+\left("
       r"\frac{\cos h-1}{h}\right)\cos\theta=-1\sin\theta+0\cos\theta=-\sin\theta$ Note: Do not allow the final A1 for "
       r"stating $\frac{\sin h}{h}=1$ or $\left(\frac{\cos h-1}{h}\right)=0$ and attempting to apply these Note: Give final "
       r"A0 for • $\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos x)=\lim_{h\to0}\left(-\frac{\sin h}{h}\sin\theta+\left("
       r"\frac{\cos h-1}{h}\right)\cos\theta\right)=-1\sin\theta+0\cos\theta=-\sin\theta$ • "
       r"$\frac{\mathrm{d}}{\mathrm{d}\theta}=\ldots$ • Defining $\mathrm{f}(x)=\cos\theta$ and applying "
       r"$\mathrm{f}'(x)=\ldots$ • $\frac{\mathrm{d}}{\mathrm{d}x}(\cos\theta)$ Note: Give final A1 for a correct limiting "
       r"argument in $x$, followed by $\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)=-\sin\theta$ e.g. "
       r"$\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos x)=\lim_{h\to0}\left(-\frac{\sin h}{h}\sin x+\left(\frac{\cos h-1}{h}"
       r"\right)\cos x\right)=-1\sin x+0\cos x=-\sin x\Rightarrow\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)="
       r"-\sin\theta$ Note: Applying $h\to0$, $\sin h\to h$, $\cos h\to1$ to give e.g. $\lim_{h\to0}\left(\frac{\cos\theta"
       r"\cos h-\sin\theta\sin h-\cos\theta}{h}\right)=\left(\frac{\cos\theta(1)-\sin\theta(h)-\cos\theta}{h}\right)="
       r"\frac{-\sin\theta(h)}{h}=-\sin\theta$ is final M0 A0 for incorrect application of limits Note: "
       r"$\lim_{h\to0}\left(\frac{\cos\theta\cos h-\sin\theta\sin h-\cos\theta}{h}\right)=\lim_{h\to0}\left(-\frac{\sin h}"
       r"{h}\sin\theta+\left(\frac{\cos h-1}{h}\right)\cos\theta\right)=\lim_{h\to0}(-(1)\sin\theta+0\cos\theta)="
       r"-\sin\theta$. So for not removing $\lim_{h\to0}$ when the limit was taken is final A0",
       r"ALT: Alternative Method: Considers $\frac{\cos(\theta+h)-\cos(\theta-h)}{(\theta+h)-(\theta-h)}$ which simplifies "
       r"to $\frac{-2\sin\theta\sin h}{2h}$"],
      False, 24),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", DIFF, "7.6, 8.7", 5, LATEX["10a"],
      [r"M1 (AO 3.3): $\frac{\mathrm{d}r}{\mathrm{d}t}\propto\pm\frac{1}{r^2}$ or $\frac{\mathrm{d}r}{\mathrm{d}t}="
       r"\pm\frac{k}{r^2}$ (for $k$ or a numerical $k$). Notes: Translates the description of the model into mathematics. "
       r"See scheme. Note: A numerical value of $k$ (e.g. $k=\pm1$) is allowed for the first two M marks",
       r"M1 (AO 2.1): $\int r^2\,\mathrm{d}r=\int\pm k\,\mathrm{d}t\Rightarrow\ldots$ (for $k$ or a numerical $k$). Notes: "
       r"Separates the variables of their differential equation which is in the form $\frac{\mathrm{d}r}{\mathrm{d}t}="
       r"\mathrm{f}(r)$ and some attempt at integration. (e.g. attempts to integrate at least one side). e.g. "
       r"$\int r^2\,\mathrm{d}r=\int\pm k\,\mathrm{d}t$ and some attempt at integration. Condone the lack of integral signs "
       r"Note: You can imply the M1 mark for $r^2dr=-k\,\mathrm{d}t\Rightarrow\frac{1}{3}r^3=-kt$",
       r"A1 (AO 1.1b): $\frac{1}{3}r^3=\pm kt$ $\{+c\}$. Notes: Correct integration to give $\frac{1}{3}r^3=\pm kt$ with or "
       r"without a constant of integration, $c$",
       r"M1 (AO 3.1a): $t=0$, $r=5$ and $t=4$, $r=3$ gives $\frac{1}{3}r^3=-\frac{49}{6}t+\frac{125}{3}$,. Notes: For a "
       r"complete process of using the boundary conditions to find both their unknown constants and finds an equation "
       r"linking $r$ and $t$ So applies either • $t=0$, $r=5$ and $t=4$, $r=3$, or • $t=0$, $r=5$ and $t=240$, $r=3$, "
       r"$\textbf{on their integrated equation}$ to find their constants $k$ and $c$ $\textbf{and}$ obtains an equation "
       r"linking $r$ and $t$",
       r"A1 (AO 1.1b): where $r$, in mm, is the radius {of the mint} and $t$, in minutes, is the time from when it {the mint} "
       r"was placed in the mouth. Notes: Correct equation, with variables $r$ and $t$ fully defined including correct "
       r"reference to units. • $\frac{1}{3}r^3=-\frac{49}{6}t+\frac{125}{3}$, {or an equivalent equation,} where $r$, in mm, "
       r"is the radius {of the mint} and $t$, in minutes, is the time from when it {the mint} was placed in the mouth • "
       r"$\frac{1}{3}r^3=-\frac{49}{360}t+\frac{125}{3}$, {or an equivalent equation,} where $r$, in mm, is the radius {of "
       r"the mint} and $t$, in seconds, is the time from when it {the mint} was placed in the mouth Note: Allow correct "
       r"equations such as • in minutes, $r=\sqrt[3]{\frac{250-49t}{2}}$, $r^3=-\frac{49}{2}t+125$ or "
       r"$t=\frac{250-2r^3}{49}$ • in seconds, $r=\sqrt[3]{\frac{15000-49t}{120}}$, $r^3=-\frac{49}{120}t+125$ or "
       r"$t=\frac{15000-120r^3}{49}$ Note: $t$ defined as “the time from the start” is not sufficient for the final A1",
       r"ALT: (a) second column — M1 (AO 3.1a): $t=0$, $r=5$ and $t=240$, $r=3$ gives $\frac{1}{3}r^3=-\frac{49}{360}t+"
       r"\frac{125}{3}$,",
       r"ALT: (a) second column — A1 (AO 1.1b): where $r$, in mm, is the radius {of the mint} and $t$, in seconds, is the "
       r"time from when it {the mint} was placed in the mouth"],
      False, 26),
    e("10b", "10(b)", INT, "8.8, 8.7", 2, LATEX["10b"],
      [r"M1 (AO 3.4): $r=0\Rightarrow0=-\frac{49}{6}t+\frac{125}{3}\Rightarrow0=-49t+250\Rightarrow t=\ldots$. Notes: Sets "
       r"$r=0$ in their part (a) equation which links $r$ with $t$ and rearranges to make $t=\ldots$ Note: Give M0 if their "
       r"equation would solve to give a negative time or a negative time is found Note: You can mark part (a) and part (b) "
       r"together",
       r"A1 (AO 1.1b): time $=5$ minutes 6 seconds. Notes: 5 minutes 6 seconds cao ($\textbf{Note:}$ 306 seconds with no "
       r"reference to 5 minutes 6 seconds is A0)"],
      False, 26),
    e("10c", "10(c)", INT, "8.8", 1, LATEX["10c"],
      [r"B1 (AO 3.5b): Suggests a suitable limitation of the model. E.g. • Model does not consider how the mint is sucked • "
       r"Model does not consider whether the mint is bitten • Model is limited for times up to 5 minutes 6 seconds, o.e. • "
       r"Not valid for times greater than 5 minutes 6 seconds, o.e. • Mint may not retain the shape of a sphere (or have "
       r"uniform radius) as it is being sucked • The model indicates that the radius of the mint is negative after it "
       r"dissolves • Model does not consider the temperature in the mouth • Model does not consider rate of saliva "
       r"production • Mint could be swallowed before it dissolves in the mouth. Notes: See scheme Note: Do not accept by "
       r"itself • mint may not dissolve at a constant rate • rate of decrease of mint must be constant • "
       r"$0\leqslant t<\frac{250}{49}$, $r\geqslant0$; without any written explanation • reference to a mint having $r>5$"],
      False, 26),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", ALG, "2.10, 2.6", 4, LATEX["11a"],
      [r"M1 (AO 2.1): $1+11x-6x^2\equiv A(1-2x)(x-3)+B(1-2x)+C(x-3)\Rightarrow B=\ldots,C=\ldots$. Notes: Way 1: Uses a "
       r"correct identity $1+11x-6x^2\equiv A(1-2x)(x-3)+B(1-2x)+C(x-3)$ in a complete method to find values for $B$ and "
       r"$C$. Note: Allow one slip in copying $1+11x-6x^2$ Note: Way 1: You can imply a correct identity "
       r"$1+11x-6x^2\equiv A(1-2x)(x-3)+B(1-2x)+C(x-3)$ from seeing $\frac{1+11x-6x^2}{(x-3)(1-2x)}\equiv"
       r"\frac{A(1-2x)(x-3)+B(1-2x)+C(x-3)}{(x-3)(1-2x)}$ Note: Writing $1+11x-6x^2\equiv B(1-2x)+C(x-3)\Rightarrow B=4$, "
       r"$C=-2$ will get 1st M0, 2nd M1, 1st A0",
       r"B1 (AO 1.1b): $A=3$. Notes: $A=3$",
       r"M1 (AO 1.1b): Uses substitution or compares terms to find either $B=\ldots$ or $C=\ldots$. Notes: Attempts to find "
       r"the value of either $B$ or $C$ from their identity This can be achieved by $\textit{either}$ substituting values "
       r"into their identity $\textit{or}$ by comparing coefficients and solving the resulting equations simultaneously "
       r"Note: Way 1: Comparing terms: $x^2$: $-6=-2A$; $x$: $11=7A-2B+C$; constant: $1=-3A+B-3C$ Way 1: Substituting: "
       r"$x=3$: $-20=-5B\Rightarrow B=4$; $x=\frac{1}{2}$: $5=-\frac{5}{2}C\Rightarrow C=-2$",
       r"A1 (AO 1.1b): $B=4$ and $C=-2$ which have been found using a correct identity. Notes: See scheme Note: $A=3$, "
       r"$B=4$, $C=-2$ from no working scores M1B1M1A1 Note: The final A1 mark is effectively dependent upon both M marks",
       r"ALT: (a) Way 2 — {long division gives} $\frac{1+11x-6x^2}{(x-3)(1-2x)}\equiv3+\frac{-10x+10}{(x-3)(1-2x)}$; M1 "
       r"(AO 2.1): $-10x+10\equiv B(1-2x)+C(x-3)\Rightarrow B=\ldots,C=\ldots$. Notes: Way 2: Uses a correct identity "
       r"$-10x+10\equiv B(1-2x)+C(x-3)$ (which has been found from long division) in a complete method to find values for "
       r"$B$ and $C$ Note: Way 2: You can imply a correct identity $-10x+10\equiv B(1-2x)+C(x-3)$ from seeing "
       r"$\frac{-10x+10}{(x-3)(1-2x)}\equiv\frac{B(1-2x)+C(x-3)}{(x-3)(1-2x)}$",
       r"ALT: (a) Way 2 — B1 (AO 1.1b): $A=3$",
       r"ALT: (a) Way 2 — M1 (AO 1.1b): Uses substitution or compares terms to find either $B=\ldots$ or $C=\ldots$. Notes: "
       r"Way 2: Comparing terms: $x$: $-10=-2B+C$; constant: $10=B-3C$ Way 2: Substituting: $x=3$: $-20=-5B\Rightarrow "
       r"B=4$; $x=\frac{1}{2}$: $5=-\frac{5}{2}C\Rightarrow C=-2$",
       r"ALT: (a) Way 2 — A1 (AO 1.1b): $B=4$ and $C=-2$ which have been found using $-10x+10\equiv B(1-2x)+C(x-3)$",
       r"ALT: (a) alternative solutions, by initially dividing by “$(x-3)$” or “$(1-2x)$”: "
       r"$\frac{1+11x-6x^2}{\text{“}(x-3)\text{”}(1-2x)}\equiv\frac{-6x-7}{(1-2x)}-\frac{20}{(x-3)(1-2x)}\equiv3-"
       r"\frac{10}{(1-2x)}-\frac{20}{(x-3)(1-2x)}$; $\frac{20}{(x-3)(1-2x)}\equiv\frac{D}{(x-3)}+\frac{E}{(1-2x)}\Rightarrow"
       r"20\equiv D(1-2x)+E(x-3)\Rightarrow D=-4,E=-8$; $\Rightarrow3-\frac{10}{(1-2x)}-\left(\frac{-4}{(x-3)}+"
       r"\frac{-8}{(1-2x)}\right)\equiv3+\frac{4}{(x-3)}-\frac{2}{(1-2x)}$; $A=3,B=4,C=-2$",
       r"ALT: (a) alternative solutions, by initially dividing by “$(x-3)$” or “$(1-2x)$”: "
       r"$\frac{1+11x-6x^2}{(x-3)\text{“}(1-2x)\text{”}}\equiv\frac{3x-4}{(x-3)}+\frac{5}{(x-3)(1-2x)}\equiv3+"
       r"\frac{5}{(x-3)}+\frac{5}{(x-3)(1-2x)}$; $\frac{5}{(x-3)(1-2x)}\equiv\frac{D}{(x-3)}+\frac{E}{(1-2x)}\Rightarrow"
       r"5\equiv D(1-2x)+E(x-3)\Rightarrow D=-1,E=-2$; $\Rightarrow3+\frac{5}{(x-3)}+\left(\frac{-1}{(x-3)}+"
       r"\frac{-2}{(1-2x)}\right)\equiv3+\frac{4}{(x-3)}-\frac{2}{(1-2x)}$; $A=3,B=4,C=-2$"],
      False, 30),
    e("11b", "11(b)", DIFF, "7.3, 7.4", 3, LATEX["11b"],
      [r"M1 (AO 2.1): $\mathrm{f}(x)=3+\frac{4}{(x-3)}-\frac{2}{(1-2x)}$ $\{=3+4(x-3)^{-1}-2(1-2x)^{-1}\}$; $x>3$ "
       r"$\mathrm{f}'(x)=-4(x-3)^{-2}-4(1-2x)^{-2}$ $\left\{=-\frac{4}{(x-3)^2}-\frac{4}{(1-2x)^2}\right\}$. Notes: "
       r"Differentiates to give $\{\mathrm{f}'(x)=\}\pm\lambda(x-3)^{-2}\pm\mu(1-2x)^{-2}$; $\lambda,\mu\neq0$",
       r"A1ft (AO 1.1b): $\mathrm{f}'(x)=-4(x-3)^{-2}-4(1-2x)^{-2}$. Notes: $\mathrm{f}'(x)=-4(x-3)^{-2}-4(1-2x)^{-2}$, "
       r"which can be simplified or un-simplified Note: Allow A1ft for $\mathrm{f}'(x)=-(\text{their }B)(x-3)^{-2}+"
       r"(2)(\text{their }C)(1-2x)^{-2}$; $(\text{their }B),(\text{their }C)\neq0$",
       r"A1 (AO 2.4): Correct $\mathrm{f}'(x)$ $\textbf{and}$ as $(x-3)^2>0$ and $(1-2x)^2>0$, then "
       r"$\mathrm{f}'(x)=-(+\text{ve})-(+\text{ve})<0$, so $\mathrm{f}(x)$ is a decreasing function. Notes: "
       r"$\mathrm{f}'(x)=-4(x-3)^{-2}-4(1-2x)^{-2}$ or $\mathrm{f}'(x)=-\frac{4}{(x-3)^2}-\frac{4}{(1-2x)^2}$ $\textbf{and}$ "
       r"a correct explanation e.g. $\mathrm{f}'(x)=-(+\text{ve})-(+\text{ve})<0$, so $\mathrm{f}(x)$ is a decreasing "
       r"{function} Note: The final A mark can be scored in part (b) from an incorrect $A=\ldots$ or from $A=0$ or no value "
       r"of $A$ found in part (a)",
       r"ALT: (b) Alternative Method 1: $\mathrm{f}(x)=\frac{1+11x-6x^2}{(x-3)(1-2x)}$, $x>3\Rightarrow\mathrm{f}(x)="
       r"\frac{1+11x-6x^2}{-2x^2+7x-3}$; $\left\{\begin{matrix}u=1+11x-6x^2&v=-2x^2+7x-3\\u'=11-12x&v'=-4x+7"
       r"\end{matrix}\right\}$ — M1: $\mathrm{f}'(x)=\frac{(-2x^2+7x-3)(11-12x)-(1+11x-6x^2)(-4x+7)}{(-2x^2+7x-3)^2}$ Uses "
       r"quotient rule to find $\mathrm{f}'(x)$",
       r"ALT: (b) Alternative Method 1 — A1: Correct differentiation",
       r"ALT: (b) Alternative Method 1 — A1: $\mathrm{f}'(x)=\frac{-20((x-1)^2+1)}{(-2x^2+7x-3)^2}$ and a correct "
       r"explanation, e.g. $\mathrm{f}'(x)=-\frac{(+\text{ve})}{(+\text{ve})}<0$, so $\mathrm{f}(x)$ is a decreasing "
       r"{function}",
       r"ALT: (b) Alternative Method 2: Allow M1A1A1 for the following solution: Given $\mathrm{f}(x)=3+\frac{4}{(x-3)}-"
       r"\frac{2}{(1-2x)}=3+\frac{4}{(x-3)}+\frac{2}{(2x-1)}$ as $\frac{4}{(x-3)}$ decreases when $x>3$ and "
       r"$\frac{2}{(2x-1)}$ decreases when $x>3$ then $\mathrm{f}(x)$ is a decreasing {function}"],
      False, 30),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", TRIG, "5.8, 5.5, 5.6", 3, LATEX["12a"],
      [r"M1 (AO 1.1b): $\tan\theta\sin2\theta=\left(\frac{\sin\theta}{\cos\theta}\right)(2\sin\theta\cos\theta)$. Notes: "
       r"Way 1 Applies $\tan\theta=\frac{\sin\theta}{\cos\theta}$ and $\sin2\theta=2\sin\theta\cos\theta$ to "
       r"$\tan\theta\sin2\theta$",
       r"M1 (AO 1.1b): $=\left(\frac{\sin\theta}{\cancel{\cos\theta}}\right)(2\sin\theta\cancel{\cos\theta})=2\sin^2\theta"
       r"=1-\cos2\theta$ *. Notes: Cancels as scheme (may be implied) and attempts to use $\cos2\theta=1-2\sin^2\theta$",
       r"A1* (AO 2.1): $=2\sin^2\theta=1-\cos2\theta$ *. Notes: For a correct proof showing all steps of the argument "
       r"Note: If a proof meets in the middle; e.g. they show LHS $=2\sin^2\theta$ and RHS $=2\sin^2\theta$; then some "
       r"indication must be given that the proof is complete. E.g. $1-\cos2\theta\equiv\tan\theta\sin2\theta$, QED, box",
       r"ALT: (a) Way 2 — M1 (AO 1.1b): $1-\cos2\theta=1-(1-2\sin^2\theta)=2\sin^2\theta$. Notes: For using "
       r"$\cos2\theta=1-2\sin^2\theta$ Note: If the form $\cos2\theta=\cos^2\theta-\sin^2\theta$ or "
       r"$\cos2\theta=2\cos^2\theta-1$ is used, the mark cannot be awarded until $\cos^2\theta$ has been replaced by "
       r"$1-\sin^2\theta$",
       r"ALT: (a) Way 2 — M1 (AO 1.1b): $=\left(\frac{\sin\theta}{\cos\theta}\right)(2\sin\theta\cos\theta)="
       r"\tan\theta\sin2\theta$ *. Notes: Attempts to write their $2\sin^2\theta$ in terms of $\tan\theta$ and "
       r"$\sin2\theta$ using $\tan\theta=\frac{\sin\theta}{\cos\theta}$ and $\sin2\theta=2\sin\theta\cos\theta$ within the "
       r"given expression",
       r"ALT: (a) Way 2 — A1* (AO 2.1): For a correct proof showing all steps of the argument"],
      False, 34),
    e("12b", "12(b)", TRIG, "5.7, 5.5, 5.6", 6, LATEX["12b"],
      [r"B1 (AO 2.2a): $(\sec^2x-5)\tan x\sin2x=3\tan^2x\sin2x$ or $(\sec^2x-5)(1-\cos2x)=3\tan x(1-\cos2x)$; Deduces "
       r"$x=0$. Notes: Deduces that the given equation yields a solution $x=0$",
       r"M1 (AO 2.1): Uses $\sec^2x=1+\tan^2x$ and cancels/factorises out $\tan x$ or $(1-\cos2x)$ e.g. "
       r"$(1+\tan^2x-3\tan x-5)\tan x=0$ $\textbf{or}$ $(1+\tan^2x-3\tan x-5)(1-\cos2x)=0$ $\textbf{or}$ "
       r"$1+\tan^2x-5=3\tan x$. Notes: For using the key step of $\sec^2x=1+\tan^2x$ and cancels/factorises out $\tan x$ or "
       r"$(1-\cos2x)$ or $\sin2x$ to produce a quadratic factor or quadratic equation in just $\tan x$ Note: Allow the use "
       r"of $\pm\sec^2x=\pm1\pm\tan^2x$ for M1",
       r"A1 (AO 1.1b): $\tan^2x-3\tan x-4=0$. Notes: Correct 3TQ in $\tan x$. E.g. $\tan^2x-3\tan x-4=0$ Note: E.g. "
       r"$\tan^2x-4=3\tan x$ or $\tan^2x-3\tan x=4$ are acceptable for A1",
       r"M1 (AO 1.1b): $(\tan x-4)(\tan x+1)=0\Rightarrow\tan x=\ldots$. Notes: For a correct method of solving their 3TQ in "
       r"$\tan x$",
       r"A1 (AO 1.1b): $x=-\frac{\pi}{4},1.326$. Notes: Any one of $-\frac{\pi}{4}$, awrt $-0.785$, awrt 1.326, $-45^\circ$, "
       r"awrt $75.964^\circ$",
       r"A1 (AO 1.1b): $x=-\frac{\pi}{4},1.326$. Notes: Only $x=-\frac{\pi}{4},1.326$ $\textbf{cao}$ stated in the range "
       r"$-\frac{\pi}{2}<x<\frac{\pi}{2}$",
       r"ALT: (b) Alternative Method (Alt 1) — B1 (AO 2.2a): $(\sec^2x-5)\tan x\sin2x=3\tan^2x\sin2x$ $\textbf{or}$ "
       r"$(\sec^2x-5)(1-\cos2x)=3\tan x(1-\cos2x)$; Deduces $x=0$",
       r"ALT: (b) Alternative Method (Alt 1) — M1 (AO 2.1): $\sec^2x-5=3\tan x\Rightarrow\frac{1}{\cos^2x}-5=3\left("
       r"\frac{\sin x}{\cos x}\right)$; $1-5\cos^2x=3\sin x\cos x$; $1-5\left(\frac{1+\cos2x}{2}\right)=\frac{3}{2}\sin2x$. "
       r"Complete process (as shown) of using the identities for $\sin2x$ and $\cos2x$ to proceed as far as "
       r"$\pm A\pm B\cos2x=\pm C\sin2x$",
       r"ALT: (b) Alternative Method (Alt 1) — A1 (AO 1.1b): $-\frac{3}{2}-\frac{5}{2}\cos2x=\frac{3}{2}\sin2x$ "
       r"$\{3\sin2x+5\cos2x=-3\}$ o.e.",
       r"ALT: (b) Alternative Method (Alt 1) — M1 (AO 1.1b): $\sqrt{34}\sin(2x+1.03)=-3$. Expresses their answer in the "
       r"form $R\sin(2x+\alpha)=k$; $k\neq0$ with values for $R$ and $\alpha$; $\sin(2x+1.03)=-\frac{3}{\sqrt{34}}$",
       r"ALT: (b) Alternative Method (Alt 1) — A1 (AO 1.1b): $x=-\frac{\pi}{4},1.326$",
       r"ALT: (b) Alternative Method (Alt 1) — A1 (AO 1.1b): $x=-\frac{\pi}{4},1.326$"],
      False, 34),

    # ---------------- Q13 ----------------
    e("13", "13", INT, "8.3, 8.5, 7.3, 7.4", 10, LATEX["13"],
      [r"M1 (AO 2.1): $\frac{\mathrm{d}y}{\mathrm{d}x}=\ln x+x\left(\frac{1}{x}\right)$ $\{=1+\ln x\}$. Notes: "
       r"Differentiates by using the product rule to give $\ln x+x(\text{their }\mathrm{g}'(x))$, where "
       r"$\mathrm{g}(x)=\ln x$",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}y}{\mathrm{d}x}=\ln x+x\left(\frac{1}{x}\right)$ $\{=1+\ln x\}$. Notes: Correct "
       r"differentiation of $y=x\ln x$, which can be un-simplified or simplified",
       r"M1 (AO 3.1a): $x=\mathrm{e}$, $m_T=2\Rightarrow m_N=-\frac{1}{2}\Rightarrow y-\mathrm{e}=-\frac{1}{2}(x-\mathrm{e})$; "
       r"$y=0\Rightarrow-\mathrm{e}=-\frac{1}{2}(x-\mathrm{e})\Rightarrow x=\ldots$. Notes: Complete strategy to find the "
       r"$x$ coordinate where their normal to $C$ at $P(\mathrm{e},\mathrm{e})$ meets the $x$-axis i.e. Sets $y=0$ in "
       r"$y-\mathrm{e}=m_N(x-\mathrm{e})$ to find $x=\ldots$ Note: $m_T$ is found by using calculus and $m_N\neq m_T$ "
       r"(Let $x_A$ be the $x$-coordinate of where $l$ cuts the $x$-axis)",
       r"A1 (AO 1.1b): $l$ meets $x$-axis at $x=3\mathrm{e}$ (allow $x=2\mathrm{e}+\mathrm{e}\ln\mathrm{e}$). Notes: $l$ "
       r"meets $x$-axis at $x=3\mathrm{e}$, allowing un-simplified values for $x$ such as $x=2\mathrm{e}+\mathrm{e}\ln"
       r"\mathrm{e}$ Note: Allow $x=$ awrt 8.15",
       r"M1 (AO 2.1): {Areas:} $\textbf{either}$ $\int_1^{\mathrm{e}}x\ln x\,\mathrm{d}x=[\ldots]_1^{\mathrm{e}}=\ldots$ "
       r"$\textbf{or}$ $\frac{1}{2}((\text{their }x_A)-\mathrm{e})\mathrm{e}$. Notes: Scored for either • Area under curve "
       r"$=\int_1^{\mathrm{e}}x\ln x\,\mathrm{d}x=[\ldots]_1^{\mathrm{e}}=\ldots$, with limits of e and 1 and some attempt "
       r"to substitute these and subtract • $\textbf{or}$ Area under line $=\frac{1}{2}((\text{their }x_A)-\mathrm{e})"
       r"\mathrm{e}$, with a valid attempt to find $x_A$",
       r"M1 (AO 2.1): $\left\{\int x\ln x\,\mathrm{d}x=\right\}\frac{1}{2}x^2\ln x-\int\frac{1}{x}\cdot\left(\frac{x^2}{2}"
       r"\right)\{\mathrm{d}x\}$. Notes: Integration by parts the correct way around to give $Ax^2\ln x-\int B\left("
       r"\frac{x^2}{x}\right)\{\mathrm{d}x\}$; $A\neq0$, $B>0$",
       r"dM1 (AO 1.1b): $\left\{=\frac{1}{2}x^2\ln x-\int\frac{1}{2}x\{\mathrm{d}x\}\right\}=\frac{1}{2}x^2\ln x-"
       r"\frac{1}{4}x^2$. Notes: dependent on the previous M mark Integrates the second term to give $\pm\lambda x^2$; "
       r"$\lambda\neq0$",
       r"A1 (AO 1.1b): $=\frac{1}{2}x^2\ln x-\frac{1}{4}x^2$. Notes: $\frac{1}{2}x^2\ln x-\frac{1}{4}x^2$",
       r"M1 (AO 3.1a): $\text{Area}(R_1)=\int_1^{\mathrm{e}}x\ln x\,\mathrm{d}x=[\ldots]_1^{\mathrm{e}}=\ldots$; "
       r"$\text{Area}(R_2)=\frac{1}{2}((\text{their }x_A)-\mathrm{e})\mathrm{e}$ and so, $\text{Area}(R)=\text{Area}(R_1)+"
       r"\text{Area}(R_2)$ $\left\{=\frac{1}{4}\mathrm{e}^2+\frac{1}{4}+\mathrm{e}^2\right\}$. Notes: Complete strategy of "
       r"finding the area of $R$ by finding the sum of two key areas. See scheme. Note: $\text{Area}(R_2)$ can also be found "
       r"by integrating the line $l$ between limits of e and their $x_A$ i.e. $\text{Area}(R_2)=\int_{\mathrm{e}}^{\text{their "
       r"}x_A}\left(-\frac{1}{2}x+\frac{3}{2}\mathrm{e}\right)\mathrm{d}x=[\ldots]_{\mathrm{e}}^{\text{their }x_A}=\ldots$",
       r"A1 (AO 1.1b): $\text{Area}(R)=\frac{5}{4}\mathrm{e}^2+\frac{1}{4}$. Notes: $\frac{5}{4}\mathrm{e}^2+\frac{1}{4}$ "
       r"Note: Calculator approach with no algebra, differentiation or integration seen: • Finding $l$ cuts through the "
       r"$x$-axis at awrt 8.15 is 2nd M1 2nd A1 • Finding area between curve and the $x$-axis between $x=1$ and "
       r"$x=\mathrm{e}$ to give awrt 2.10 is 3rd M1 • Using the above information (must be seen) to apply "
       r"$\text{Area}(R)=2.0972\ldots+7.3890\ldots=9.4862\ldots$ is final M1 Therefore, a maximum of 4 marks out of the 10 "
       r"available."],
      True, 38),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", EXP, "6.7", 1, LATEX["14a"],
      [r"B1 (AO 3.4): 90"],
      False, 42),
    e("14b", "14(b)", DIFF, "7.4, 6.7", 4, LATEX["14b"],
      [r"M1 (AO 2.1): $\frac{\mathrm{d}N}{\mathrm{d}t}=-900(3+7\mathrm{e}^{-0.25t})^{-2}\left(7(-0.25)\mathrm{e}^{-0.25t}"
       r"\right)$ $\left\{=\frac{900(0.25)(7)\mathrm{e}^{-0.25t}}{(3+7\mathrm{e}^{-0.25t})^2}\right\}$. Notes: Attempts to "
       r"differentiate using • the chain rule to give $\frac{\mathrm{d}N}{\mathrm{d}t}=\pm A\mathrm{e}^{-0.25t}(3+7"
       r"\mathrm{e}^{-0.25t})^{-2}$ or $\frac{\pm A\mathrm{e}^{-0.25t}}{(3+7\mathrm{e}^{-0.25t})^2}$ o.e. • the quotient "
       r"rule to give $\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{(3+7\mathrm{e}^{-0.25t})(0)\pm A\mathrm{e}^{-0.25t}}{(3+7"
       r"\mathrm{e}^{-0.25t})^2}$ • implicit differentiation to give $N(3+7\mathrm{e}^{-0.25t})=900\Rightarrow(3+7"
       r"\mathrm{e}^{-0.25t})\frac{\mathrm{d}N}{\mathrm{d}t}\pm AN\mathrm{e}^{-0.25t}=0$, o.e. where $A\neq0$ Note: Condone "
       r"a slip in copying $(3+7\mathrm{e}^{-0.25t})$ for the M mark",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}N}{\mathrm{d}t}=-900(3+7\mathrm{e}^{-0.25t})^{-2}\left(7(-0.25)\mathrm{e}^{-0.25t}"
       r"\right)$. Notes: A correct differentiation statement Note: Implicit differentiation gives "
       r"$(3+7\mathrm{e}^{-0.25t})\frac{\mathrm{d}N}{\mathrm{d}t}-1.75N\mathrm{e}^{-0.25t}=0$",
       r"dM1 (AO 2.1): $\Rightarrow\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{900(0.25)\left(\left(\frac{900}{N}-3\right)\right)}"
       r"{\left(\frac{900}{N}\right)^2}$. Notes: Way 1: Complete attempt, by eliminating $t$, to form an equation linking "
       r"$\frac{\mathrm{d}N}{\mathrm{d}t}$ and $N$ only Note: Way 1: e.g. substitutes $3+7\mathrm{e}^{-0.25t}="
       r"\frac{900}{N}$ and $\mathrm{e}^{-0.25t}=\frac{900}{N}$ or substitutes $\mathrm{e}^{-0.25t}=\frac{\frac{900}{N}-3}"
       r"{7}$ into their $\frac{\mathrm{d}N}{\mathrm{d}t}=\ldots$ to form an equation linking "
       r"$\frac{\mathrm{d}N}{\mathrm{d}t}$ and $N$",
       r"A1* (AO 1.1b): correct algebra leading to $\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{N(300-N)}{1200}$ *. Notes: Way 1: "
       r"Correct algebra leading to $\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{N(300-N)}{1200}$ *",
       r"ALT: (b) Way 2 — M1 (AO 2.1): $\frac{\mathrm{d}N}{\mathrm{d}t}=-900(3+7\mathrm{e}^{-0.25t})^{-2}\left(7(-0.25)"
       r"\mathrm{e}^{-0.25t}\right)$ $\left\{=\frac{900(0.25)(7)\mathrm{e}^{-0.25t}}{(3+7\mathrm{e}^{-0.25t})^2}\right\}$",
       r"ALT: (b) Way 2 — A1 (AO 1.1b): $\frac{\mathrm{d}N}{\mathrm{d}t}=-900(3+7\mathrm{e}^{-0.25t})^{-2}\left(7(-0.25)"
       r"\mathrm{e}^{-0.25t}\right)$ $\left\{=\frac{900(0.25)(7)\mathrm{e}^{-0.25t}}{(3+7\mathrm{e}^{-0.25t})^2}\right\}$",
       r"ALT: (b) Way 2 — dM1 (AO 2.1): $\frac{N(300-N)}{1200}=\frac{\left(\frac{900}{3+7\mathrm{e}^{-0.25t}}\right)\left("
       r"300-\frac{900}{3+7\mathrm{e}^{-0.25t}}\right)}{1200}$. Notes: Way 2: Complete substitution of "
       r"$N=\frac{900}{3+7\mathrm{e}^{-0.25t}}$ into $\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{N(300-N)}{1200}$",
       r"ALT: (b) Way 2 — A1* (AO 1.1b): LHS $=\frac{1575\mathrm{e}^{-0..25t}}{(3+7\mathrm{e}^{-0.25t})^2}$ o.e., RHS $="
       r"\frac{900(300(3+7\mathrm{e}^{-0.25t})-900)}{1200(3+7\mathrm{e}^{-0.25t})^2}=\frac{1575\mathrm{e}^{-0..25t}}{(3+7"
       r"\mathrm{e}^{-0.25t})^2}$ o.e. and states hence $\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{N(300-N)}{1200}$ (or LHS $=$ "
       r"RHS) *. Notes: Way 2: See scheme",
       r"ALT: (b) Way 3 — M1 (AO 2.1): $\int\frac{1}{N(300-N)}\mathrm{d}N=\int\frac{1}{1200}\,\mathrm{d}t$; "
       r"$\int\frac{1}{300}\left(\frac{1}{N}+\frac{1}{300-N}\right)\mathrm{d}N=\int\frac{1}{1200}\,\mathrm{d}t$. Notes: "
       r"Separates the variables, an attempt to form and apply partial fractions and integrates to give ln terms "
       r"$=kt$ $\{+c\}$, $k\neq0$, with or without a constant of integration $c$",
       r"ALT: (b) Way 3 — A1 (AO 1.1b): $\frac{1}{300}\ln N-\frac{1}{300}\ln(300-N)=\frac{1}{1200}t$ $\{+c\}$. Notes: "
       r"$\frac{1}{300}\ln N-\frac{1}{300}\ln(300-N)=\frac{1}{1200}t$ $\{+c\}$ or equivalent with or without a constant of "
       r"integration $c$",
       r"ALT: (b) Way 3 — dM1 (AO 2.1): $\{t=0,N=90\Rightarrow\}$ $c=\frac{1}{300}\ln(90)-\frac{1}{300}\ln(210)\Rightarrow "
       r"c=\frac{1}{300}\ln\left(\frac{3}{7}\right)$; $\frac{1}{300}\ln N-\frac{1}{300}\ln(300-N)=\frac{1}{1200}t+"
       r"\frac{1}{300}\ln\left(\frac{3}{7}\right)$; $\ln N-\ln(300-N)=\frac{1}{4}t+\ln\left(\frac{3}{7}\right)$; "
       r"$\ln\left(\frac{N}{300-N}\right)=\frac{1}{4}t+\ln\left(\frac{3}{7}\right)\Rightarrow\frac{N}{300-N}=\frac{3}{7}"
       r"\mathrm{e}^{\frac{1}{4}t}$. Notes: Uses $t=0$, $N=90$ to find their constant of integration and obtains an "
       r"expression of the form $\lambda\mathrm{e}^{\frac{1}{4}t}=\mathrm{f}(N)$; $\lambda\neq0$ or "
       r"$\lambda\mathrm{e}^{-\frac{1}{4}t}=\mathrm{f}(N)$; $\lambda\neq0$",
       r"ALT: (b) Way 3 — A1* (AO 1.1b): $7N=3\mathrm{e}^{\frac{1}{4}t}(300-N)\Rightarrow7N+3N\mathrm{e}^{\frac{1}{4}t}="
       r"900\mathrm{e}^{\frac{1}{4}t}$; $N(7+3\mathrm{e}^{\frac{1}{4}t})=900\mathrm{e}^{\frac{1}{4}t}\Rightarrow N="
       r"\frac{900\mathrm{e}^{\frac{1}{4}t}}{7+3\mathrm{e}^{\frac{1}{4}t}}\Rightarrow N=\frac{900}{3+7\mathrm{e}^{-0.25t}}$ "
       r"*. Notes: Correct manipulation leading to $N=\frac{900}{3+7\mathrm{e}^{-0.25t}}$ *",
       r"ALT: (b) Way 4 — M1 (AO 2.1): $N(3+7\mathrm{e}^{-0.25t})=900\Rightarrow\mathrm{e}^{-0.25t}=\frac{1}{7}\left("
       r"\frac{900}{N}-3\right)\Rightarrow\mathrm{e}^{-0.25t}=\frac{900-3N}{7N}$; $\Rightarrow t=-4(\ln(900-3N)-\ln(7N))$. "
       r"Notes: Valid attempt to make $t$ the subject, followed by an attempt to find two ln derivatives, condoning sign "
       r"errors and constant errors.",
       r"ALT: (b) Way 4 — A1 (AO 1.1b): $\Rightarrow\frac{\mathrm{d}t}{\mathrm{d}N}=-4\left(\frac{-3}{900-3N}-\frac{7}{7N}"
       r"\right)$. Notes: $\frac{\mathrm{d}t}{\mathrm{d}N}=-4\left(\frac{-3}{900-3N}-\frac{7}{7N}\right)$ or equivalent",
       r"ALT: (b) Way 4 — dM1 (AO 2.1): $\frac{\mathrm{d}t}{\mathrm{d}N}=4\left(\frac{1}{300-N}+\frac{1}{N}\right)"
       r"\Rightarrow\frac{\mathrm{d}t}{\mathrm{d}N}=4\left(\frac{N+300-N}{N(300-N)}\right)$. Notes: Forms a common "
       r"denominator to combine their fractions",
       r"ALT: (b) Way 4 — A1* (AO 1.1b): $\frac{\mathrm{d}t}{\mathrm{d}N}=\left(\frac{1200}{N(300-N)}\right)\Rightarrow"
       r"\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{N(300-N)}{1200}$ *. Notes: Correct algebra leading to "
       r"$\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{N(300-N)}{1200}$ *"],
      False, 42),
    e("14c", "14(c)", DIFF, "7.3, 6.7", 4, LATEX["14c"],
      [r"B1 (AO 2.2a): Deduces $N=150$ (can be implied). Notes: Deduces or shows that $\frac{\mathrm{d}N}{\mathrm{d}t}$ is "
       r"maximised when $N=150$ Note: $\frac{\mathrm{d}^2N}{\mathrm{d}t^2}=\frac{\mathrm{d}N}{\mathrm{d}t}\left("
       r"\frac{300}{1200}-\frac{2N}{1200}\right)=0\Rightarrow N=150$ is acceptable for B1",
       r"M1 (AO 3.4): so $150=\frac{900}{3+7\mathrm{e}^{-0.25T}}\Rightarrow\mathrm{e}^{-0.25T}=\frac{3}{7}$. Notes: Uses "
       r"the model $N=\frac{900}{3+7\mathrm{e}^{-0.25t}}$ with their $N=150$ and proceeds as far as "
       r"$\mathrm{e}^{-0.25T}=k$, $k>0$ or $\mathrm{e}^{0.25T}=k$, $k>0$. Condone $t\equiv T$ Note: Applying "
       r"$300=\frac{900}{3+7\mathrm{e}^{-0.25t}}\Rightarrow t=\ldots$ or $0=\frac{900}{3+7\mathrm{e}^{-0.25t}}\Rightarrow "
       r"t=\ldots$ is M0 dM0 A0 Note: M1 dM1 can only be gained in (c) by using an $N$ value in the range $90<N<300$",
       r"dM1 (AO 1.1b): $T=-4\ln\left(\frac{3}{7}\right)$ or $T=$ awrt 3.4 (months). Notes: Correct method of using "
       r"logarithms to find a value for $T$. Condone $t\equiv T$",
       r"A1 (AO 1.1b): $T=-4\ln\left(\frac{3}{7}\right)$ or $T=$ awrt 3.4 (months). Notes: see scheme Note: Ignore units for "
       r"$T$"],
      False, 42),
    e("14d", "14(d)", EXP, "6.7", 1, LATEX["14d"],
      [r"B1 (AO 3.4): either one of 299 or 300. Notes: 300 (or accept 299)"],
      False, 42),
]

# Examiner report, sentence by sentence, in report order (the Introduction is not
# attached to any question). A sentence that only mentions using an earlier part
# goes on the part it is about.
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "This question proved accessible to all, but only the most able students scored full marks."),
        ({"a"}, r"In part (a), most students found the value of $\mathrm{g}(5)$ and substituted this value back into "
                r"$\mathrm{g}(x)$, with nearly all of them being successful in finding the correct "
                r"$\mathrm{gg}(5)=\frac{40}{9}$."),
        ({"a"}, r"A minority found $\mathrm{gg}(x)$ algebraically and substituted $x=5$ into the result."),
        ({"b"}, r"In part (b), only a few students stated the correct range $2<\mathrm{g}(x)\leqslant\frac{15}{2}$."),
        ({"b"}, r"The most common incorrect answers included $\mathrm{g}(x)\leqslant\frac{15}{2}$, "
                r"$\mathrm{g}(x)<\frac{15}{2}$, $\mathrm{g}(x)>\frac{15}{2}$ and $2<x\leqslant\frac{15}{2}$."),
        ({"c"}, r"In part (c), most students used a correct process to find $y=\frac{3x+5}{x-2}$ with some finding "
                r"$y=\frac{11}{x-2}+3$."),
        ({"c"}, r"A few students, who misunderstood the notation $\mathrm{g}^{-1}$, tried to either differentiate "
                r"$\mathrm{g}(x)$ or write down the reciprocal of $\mathrm{g}(x)$."),
        ({"c"}, r"Some students lost the final mark by stating neither $\mathrm{g}^{-1}(x)=\frac{3x+5}{x-2}$ nor its "
                r"domain in correct notation."),
        ({"c"}, r"Some students made no attempt to write down the domain of $\mathrm{g}^{-1}$."),
    ],
    "02": [
        (W, "This was a well-answered question with most students scoring at least 4 of the 5 marks available.", NO),
        ({"a"}, "Part (a) was often completed successfully."),
        ({"a"}, r"Most students found $\overrightarrow{AB}$ and used the given result $\overrightarrow{AB}="
                r"\overrightarrow{BD}$ to deduce and apply $\overrightarrow{OD}=\overrightarrow{OB}+\overrightarrow{AB}$."),
        ({"a"}, r"A few students applied $\overrightarrow{OD}=\overrightarrow{OA}+2\overrightarrow{AB}$."),
        ({"a"}, r"There were some sign, manipulation and bracketing errors seen in this part and students who used column "
                r"vectors were generally more successful than those who used the $\mathbf{i},\mathbf{j},\mathbf{k}$ "
                r"notation.", NO),
        ({"b"}, r"In part (b), most students found the difference between $\overrightarrow{OC}$ and "
                r"$\overrightarrow{OA}$, and applied Pythagoras’ Theorem to $|\overrightarrow{AC}|=4$ to give the "
                r"correct $(a-2)^2+(2)^2+(2)^2=(4)^2$."),
        ({"b"}, "The resulting quadratic equation was generally solved correctly but not always efficiently."),
        ({"b"}, "Too often, students expanded to form a 3-term quadratic rather than spotting that their quadratic was "
                "already in a ‘completed square’ form."),
        ({"b"}, r"Despite the question stating that $a<0$, some students gave both solutions $a=2\pm2\sqrt{2}$ as their "
                r"final answer, while others mistakenly rejected $a=2-2\sqrt{2}$ to leave $a=2+2\sqrt{2}$."),
    ],
    "03": [
        ({"b"}, "This question discriminated well between students of all abilities with some students struggling to "
                "access the final mark in part (b)."),
        ({"a"}, "In part (a), most students provided a complete solution to disprove the statement given in the "
                "question."),
        ({"a"}, r"Common errors included: choosing inappropriate values for $m,n$ (e.g. $\sqrt{2}$ and $\sqrt{3}$ which "
                r"were sometimes seen); choosing two rational numbers; attempting to disprove the general statement by "
                r"using algebra; and not giving a conclusion, despite choosing appropriate values for $m,n$."),
        ({"b"}, r"In part (b)(i), most students drew a V-shaped graph in the correct position with many labelling 3 or "
                r"$(0, 3)$ as the $y$-intercept."),
        ({"b"}, r"In part (b)(ii), those students who superimposed the graph of $y=|x+3|$ over the graph of $y=|x|+3$ "
                r"were usually more successful in explaining why $|x|+3\geqslant|x+3|$ for all real values of $x$.", NO),
        ({"b"}, "Otherwise, a variety of explanations were seen, of which some were detailed, usually containing at "
                "least one correct statement."),
        ({"b"}, r"Common errors included explanations which did not consider the case $x=0$ or explanations including "
                r"the statement that the graphs of $y=|x|+3$ and $y=|x+3|$ were parallel for all $x<0$."),
        ({"b"}, r"A significant number of students who only tested the statement $|x|+3\geqslant|x+3|$ for specific "
                r"values of $x$ (usually one positive and one negative) did not receive any credit in this part."),
    ],
    "04": [
        ({"i", "ii"}, "This was an accessible question with part (ii) more successfully answered than part (i).", NO),
        ({"i"}, r"In part (i), some students attempted to find $\sum_{r=1}^{16}(3+5r+2^r)$ by applying the strategy "
                r"$(3\times16)+\sum_{r=1}^{16}5r+\sum_{r=1}^{16}2^r$, while other students applied the strategy "
                r"$\sum_{r=1}^{16}(3+5r)+\sum_{r=1}^{16}2^r$."),
        ({"i"}, r"Most students applied the sum formula for an arithmetic series with $a=5$, $d=5$ to "
                r"$(3\times16)+\sum_{r=1}^{16}5r$ to give $(3\times16)+\frac{16}{2}(2(5)+15(5))$ while some applied "
                r"$a=8$, $d=5$ to $\sum_{r=1}^{16}(3+5r)$ to give $\frac{16}{2}(2(8)+15(5))$."),
        ({"i"}, r"A few students used $\sum_{r=1}^{n}r=\frac{1}{2}n(n+1)$ to help them to evaluate "
                r"$5\sum_{r=1}^{16}r$."),
        ({"i"}, r"Students were generally less successful with using the formula for the sum of a geometric series to "
                r"find $\sum_{r=1}^{16}2^r$."),
        ({"i"}, "Common errors included assuming the first term, $a$, was 1 or writing down the value 131070 with no "
                "method (perhaps by working back from the given answer)."),
        ({"i"}, "A significant number of students listed all 16 terms and added them to achieve the given result."),
        ({"i"}, r"Those students who did not list all the terms, but just wrote e.g. $10+17+26+39+60+\ldots+65619="
                r"131798$, did not receive any credit.", NO),
        ({"i"}, r"Some students, who attempted to find the first, second and third differences between the terms of the "
                r"series $10, 17, 26, 39, 60,\ldots$, usually made no creditable progress."),
        ({"ii"}, "Part (ii) was very well attempted, even by those who failed to gain any credit in part (i).", NO),
        ({"ii"}, "Almost all students wrote down the next two terms $u_2$, $u_3$ correctly."),
        ({"ii"}, r"Many deduced that they were working with an alternating sequence and found the correct exact value "
                 r"for $\sum_{r=1}^{100}u_r$."),
        ({"ii"}, "Some students attempted to round their answer, usually to 108.3."),
        ({"ii"}, r"A few students attempted to find $\sum_{r=1}^{100}u_r$ by using the formula for the sum of an "
                 r"arithmetic series or the formula for the sum of a geometric series."),
    ],
    "05": [
        ({"a", "c"}, "This was a well-answered question with part (a) and part (c) providing most of the "
                     "discrimination.", NO),
        ({"a"}, r"In part (a), most students substituted a defined $\mathrm{f}(x_n)=2x_n^3+x_n^2-1$ and a correct "
                r"$\mathrm{f}'(x_n)=6x_n^2+2x_n$ into the Newton-Raphson formula $x_{n+1}=x_n-\frac{\mathrm{f}(x_n)}"
                r"{\mathrm{f}'(x_n)}$."),
        ({"a"}, "Many students used correct algebra to arrive at the given result."),
        ({"a"}, r"Some students moved directly from $x_{n+1}=x_n-\frac{2x_n^3+x_n^2-1}{6x_n^2+2x_n}$ to "
                r"$x_{n+1}=\frac{4x_n^3+x_n^2+1}{6x_n^2+2x_n}$ without showing the correct intermediate step of "
                r"rationalising the denominator."),
        ({"a"}, r"There were bracketing errors, sign errors and the error of omitting ‘$x_{n+1}=$’ to write only the "
                r"right-hand side of the Newton-Raphson formula."),
        ({"b"}, r"In part (b), nearly all students wrote down a correct $x_2=\frac{3}{4}$, $x_3=\frac{2}{3}$."),
        ({"c"}, "In part (c), only a few students gave an acceptable explanation that detailed why the Newton-Raphson "
                "method did not work for this question."),
        ({"c"}, r"Some of these students stated ‘because there is a stationary point at $x=0$, then the method could "
                r"not work’ while others explained that a tangent to the curve at $x=0$ would never meet the $x$-axis.",
         BACK),
        ({"c"}, "The explanation, ‘not being able to divide by zero in the formula’, by itself, was not sufficient to "
                "gain credit in part (c)."),
    ],
    "06": [
        ({"b", "c"}, "This was a well-answered question with part (b) and part (c) providing most of the "
                     "discrimination.", NO),
        ({"a"}, r"In part (a), nearly all students found $\mathrm{f}(2)=0$ and many used this result to deduce that "
                r"$(x-2)$ was a factor of $\mathrm{f}(x)$.", NO),
        ({"a"}, r"The method of long division was the most popular and successful method to find the quadratic factor "
                r"of $\mathrm{f}(x)$."),
        ({"a"}, "Those who used the more time-efficient method of comparing coefficients were slightly more prone to "
                "making sign or manipulation errors.", NO),
        ({"a"}, r"Most students arrived at the correct answer $\mathrm{f}(x)=(x-2)(-3x^2+2x-5)$, with some writing the "
                r"equivalent $\mathrm{f}(x)=(2-x)(3x^2-2x+5)$."),
        ({"a"}, "There were a few students who found both correct factors but did not express their final answer as a "
                "product of two algebraic factors."),
        ({"b"}, r"In part (b), many students used part (a) to write down $(y^2-2)(-3y^4+2y^2-5)=0$ and most deduced the "
                r"two real solutions $y=\pm\sqrt{2}$."),
        ({"b"}, r"Surprisingly a few students solved $y^2=2$ to give $y=\pm2$."),
        ({"b"}, r"A significant number of students stated, without proof, that $(-3x^2+2x-5)$ or $(-3y^4+2y^2-5)$ where "
                r"$x=y^2$, had no real solutions."),
        ({"b"}, r"Some students applied ‘$b^2-4ac=(2)^2-4(-3)(-5)=-56<0$’ with an appropriate conclusion to show that "
                r"$(-3y^4+2y^2-5)=0$ had no real solutions."),
        ({"b"}, r"Common errors included just stating ‘$b^2-4ac<0$’ with no reference to a discriminant calculation or "
                r"the omission of ‘$<0$’ after a correct discriminant calculation."),
        ({"b"}, "Only a minority of students were able to bring the two strands of the proof together to show that the "
                "given equation had only two real solutions."),
        ({"c"}, r"In part (c), some students correctly deduced that the given equation had 3 real solutions for "
                r"$7\pi\leqslant\theta<10\pi$, with a few students incorrectly deducing that there were 6 real "
                r"solutions."),
        ({"c"}, r"Most students misunderstood the requirement of the question by finding $\theta=23.1, 26.2, 29.4$, with "
                r"those students who did not go on to state that there were 3 real solutions losing the mark for this "
                r"part.", NO),
    ],
    "07": [
        ({"i", "ii"}, "Part (i) was accessible to most students, whereas some students struggled to gain access to part "
                      "(ii)."),
        ({"i"}, r"In part (i), many students replaced $\sec x$ with $\frac{1}{\cos x}$ and arrived at "
                r"$4\sin x\cos x=1$."),
        ({"i"}, r"A few students replaced $4\sin x\cos x$ with $\sin4x$, but most used the identity "
                r"$\sin2x\equiv2\sin x\cos x$ to give the correct $\sin2x=\frac{1}{2}$."),
        ({"i"}, r"Many students obtained both correct exact solutions in radians, with only a few omitting the second "
                r"solution $\frac{5\pi}{12}$."),
        ({"ii"}, r"Some students made no attempt at part (ii) while a significant number of other students did not "
                 r"employ a correct strategy for solving $5\sin\theta-5\cos\theta=2$."),
        ({"ii"}, "The majority of students, however, attempted one of several correct strategies."),
        ({"ii"}, r"The most popular strategy was to square both sides of the given equation and apply the identities "
                 r"$\cos^2\theta+\sin^2\theta\equiv1$ and $\sin2\theta\equiv2\sin\theta\cos\theta$ to achieve "
                 r"$\sin2\theta=\frac{21}{25}$."),
        ({"ii"}, r"A second strategy was to square both sides of $5\sin\theta=2+5\cos\theta$ and apply the identity "
                 r"$\cos^2\theta+\sin^2\theta\equiv1$ to achieve a quadratic equation in either $\cos\theta$ or "
                 r"$\sin\theta$."),
        ({"ii"}, "In both of these strategies, extra (incorrect) solutions were generated as a result of squaring both "
                 "sides of their equation.", BACK),
        ({"ii"}, r"Only a few students rejected these extra solutions to leave the correct solutions "
                 r"$\theta=61.4^\circ, 208.6^\circ$.", BACK),
        ({"ii"}, r"A third strategy was to rewrite the given equation as $\sqrt{50}\sin(\theta-45^\circ)=2$ or even "
                 r"$\sqrt{50}\cos(\theta+45^\circ)=-2$, which were usually solved to give "
                 r"$\theta=61.4^\circ, 208.6^\circ$."),
        ({"ii"}, r"A few students applied other correct strategies which led to solving quadratic equations in either "
                 r"$\tan\theta$ or $\cot\theta$."),
    ],
    "08": [
        (W, "This question discriminated well between the average and more able students."),
        (W, "There was a significant minority of students, however, that made no creditable progress."),
        ({"a"}, "In part (a), a minority of students struggled to write down a suitable form of the quadratic model."),
        ({"a"}, r"Some students, who tried to model the height of the rugby ball as a negative quadratic cutting the "
                r"$x$-axis at $x=0$ and $x=40$, wrote down either $H=-x(x-40)$ or $H=x(40-x)$, but struggled, due to the "
                r"lack of a constant, to fit the condition $(20, 12)$ to their model."),
        ({"a"}, r"Those who wrote $H=Ax(40-x)$ usually applied $(20, 12)$ to their model to give the correct "
                r"$H=\frac{3}{100}x(40-x)$.", NO),
        ({"a"}, r"Other students who adopted a model of the form $H=ax^2+bx+c$ were usually successful in using the "
                r"conditions $(0, 0)$, $(40, 0)$ and $(20, 12)$ to give the correct $H=-0.03x^2+1.2x$."),
        ({"a"}, r"Only a few students used the model $H=12-\lambda(x-20)^2$ with condition $(40, 0)$ to find a correct "
                r"$H=12-\frac{3}{100}(x-20)^2$."),
        ({"a"}, r"A few other elaborate methods were seen, including one where $(40, 0)$ and "
                r"$\left(\frac{-b}{2a}, 12\right)$ were applied to $H=ax^2+bx$, which usually resulted in a correct "
                r"$H=-0.03x^2+1.2x$."),
        ({"b"}, r"In part (b), many students substituted $H=3$ into their quadratic model and most applied a correct "
                r"method for solving their resulting 3-term quadratic equation or their quadratic equation of the form "
                r"$(x-20)^2=k$, $k\neq0$."),
        ({"b"}, "Many students found the largest solution in the range $(0, 40)$ and gave their answer, usually to 3 "
                "significant figures, in metres."),
        ({"c"}, "Students gave a variety of acceptable limitations for the model in part (c) with many stating that "
                "‘the model assumes that there is no wind or air resistance acting on the ball’."),
        ({"c"}, "No credit was given for answers that discussed what might have happened to the rugby ball after it "
                "had hit the ground.", NO),
    ],
    "09": [
        (W, "This was a well-answered question considering that this was the first time that differentiation from "
            "first principles has been tested on the new specification.", NO),
        (W, r"Most students wrote down a correct expression for the gradient of the chord joining the points "
            r"$(\theta, \cos\theta)$ and $(\theta+h, \cos(\theta+h))$ for a small value $h$."),
        (W, r"Many students simplified their gradient expression to give a correct $-\frac{\sin h}{h}\sin\theta+\left("
            r"\frac{\cos h-1}{h}\right)\cos\theta$ and applied the limiting arguments given in the question to deduce "
            r"that $\frac{\mathrm{d}}{\mathrm{d}\theta}(\cos\theta)=-\sin\theta$."),
        (W, "Some students lost the final mark for not applying limiting arguments correctly."),
        (W, r"Common errors included: stating that $\frac{\sin h}{h}=1$, $\frac{\cos h-1}{h}=0$; not using a limiting "
            r"argument; or applying the limiting argument inconsistently."),
        (W, "Other students lost the final mark for the use of inconsistent notation in their proof."),
        (W, r"These students, who usually referred to both $x$ and $\theta$ in their proof, wrote incorrect statements "
            r"such as $\frac{\mathrm{d}}{\mathrm{d}x}(\cos\theta)=-\sin\theta$ or $\mathrm{f}(x)=\cos\theta$.", BACK),
    ],
    "10": [
        (W, "This question discriminated well between the average and more able students."),
        (W, "There waere a significant minority of students, however, that made no creditable progress."),
        ({"a"}, "In part (a), many students struggled to translate the description of the model into a mathematical "
                "statement."),
        ({"a"}, r"Some incorrect statements, such as $\frac{\mathrm{d}r}{\mathrm{d}t}=\frac{1}{r^2}$, "
                r"$\frac{\mathrm{d}r}{\mathrm{d}t}=r^2$ or $\frac{\mathrm{d}r}{\mathrm{d}t}=\frac{1}{r}$, did not "
                r"contain a constant of proportionality; while other incorrect statements "
                r"$\frac{\mathrm{d}r}{\mathrm{d}t}=kr^2$, $\frac{\mathrm{d}r}{\mathrm{d}t}=\frac{r^2}{k}$ or "
                r"$\frac{\mathrm{d}r}{\mathrm{d}t}=\frac{k}{r}$ contained a constant of proportionality.", NO),
        ({"a"}, r"Many students used a correct method to separate the variables and most proceeded to integrate their "
                r"$\int r^2\,\mathrm{d}r=\int k\,\mathrm{d}t$ to give an equation linking $r$ and $t$ which contained a "
                r"constant of integration."),
        ({"a"}, r"At this stage, some students incorrectly integrated $r^2$ to give $2r$.", BACK),
        ({"a"}, r"The majority of students applied the boundary conditions $t=0, r=5$ and $t=4, r=3$ (or "
                r"$t=240, r=3$) to find both constants and proceeded to give an equation linking $r$ with $t$."),
        ({"a"}, r"Some students who worked in minutes obtained correct answers of either "
                r"$r=\sqrt[3]{\frac{250-49t}{2}}$, $r^3=-\frac{49}{2}t+125$ or $t=\frac{250-2r^3}{49}$."),
        ({"a"}, r"A few students who worked in seconds obtained correct answers of either "
                r"$r=\sqrt[3]{\frac{15000-49t}{120}}$, $r^3=-\frac{49}{120}t+125$ or $t=\frac{15000-120r^3}{49}$."),
        ({"a"}, "Many students lost the final mark in this part by not including sufficient detail in their definition "
                "of their variables."),
        ({"a"}, "Some students defined $r$ as the radius of the mint, in mm, but it was rare to see the time, $t$, "
                "defined from a correct starting point (i.e. from when the mint was placed in the mouth) and with the "
                "correct unit of time used.", NO),
        ({"b"}, r"In part (b), many students substituted $r=0$ in their equation from part (a) and rearranged to find a "
                r"value for $t$, with a significant number obtaining the correct answer, 5 minutes 6 seconds."),
        ({"b"}, r"Some students lost the final mark by giving their final answer as either 5.10 minutes, "
                r"$\frac{250}{49}$ minutes or 306 seconds."),
        ({"c"}, "Part (c) was generally well-answered with a variety of valid limitations given."),
        ({"c"}, "Students commented on the shape of the mint while it was being sucked; on how the mint was sucked; or "
                "that the model predicted a negative radius for the mint after a time of 5 minutes 6 seconds after the "
                "mint was placed in the mouth.", NO),
        ({"c"}, "Some students who stated that ‘the radius of the mint may not decrease at a constant rate’ did not "
                "receive any credit because the radius of the mint in the original model was not decreasing at a "
                "constant rate."),
    ],
    "11": [
        ({"a", "b"}, "Part (a) was accessible to most students, whereas some students struggled to gain access to part "
                     "(b)."),
        ({"a"}, r"In part (a), most students used the given $\frac{1+11x-6x^2}{(x-3)(1-2x)}\equiv A+\frac{B}{(x-3)}+"
                r"\frac{C}{(1-2x)}$ to write down a correct identity $1+11x-6x^2\equiv A(1-2x)(x-3)+B(1-2x)+C(x-3)$."),
        ({"a"}, r"Some students used a method of long division to deduce that $A=3$ and formulated the correct identity "
                r"$-10x+10\equiv B(1-2x)+C(x-3)$."),
        ({"a"}, r"Only a few students wrote down the incorrect identity $1+11x-6x^2\equiv B(1-2x)+C(x-3)$."),
        ({"a"}, "Most students used either a method of substituting values into their identity or a method of comparing "
                "coefficients with most finding the correct values for $A$, $B$ and $C$."),
        ({"b"}, "In part (b), a minority of students struggled to make any creditable progress."),
        ({"b"}, r"These students usually evaluated $\mathrm{f}(x)$ for increasing $x$-values and concluded that the "
                r"corresponding values for $\mathrm{f}(x)$ were continually decreasing.", BACK),
        ({"b"}, r"The majority used the chain rule to differentiate $\mathrm{f}(x)$."),
        ({"b"}, r"A common error at this stage was for students to differentiate $-2(1-2x)^{-1}$ to give "
                r"$-2(1-2x)^{-2}$, while other students tried to apply an incorrect method of showing "
                r"$\mathrm{f}''(x)<0$.", BACK),
        ({"b"}, r"Only a few of the students who obtained a correct $\mathrm{f}'(x)=-4(x-3)^{-2}-4(1-2x)^{-2}$ provided "
                r"an acceptable explanation detailing why $\mathrm{f}'(x)<0$."),
    ],
    "12": [
        ({"a", "b"}, "This question discriminated well between students of all abilities with part (a) more accessible "
                     "to students than part (b)."),
        ({"a"}, "In part (a), most students provided a proof which progressed from one side of the identity to the "
                "other by using methodical steps and correct trigonometric identities."),
        ({"a"}, "There was no preference seen for starting their proof on a particular side of the identity."),
        ({"a"}, r"Some students manipulated both sides of the identity to give a common expression $2\sin^2\theta$, with "
                r"many providing some indication that their proof was complete."),
        ({"b"}, "Part (b) proved to be discriminating, with some students not realising that they could use the result "
                "from part (a)."),
        ({"b"}, r"Some students substituted $1-\cos2x$ with $\tan x\sin2x$ and then proceeded to cancel $\tan x\sin2x$ "
                r"from both sides, while other students substituted $\tan x\sin2x$ with $1-\cos2x$ and then proceeded "
                r"to cancel $1-\cos2x$ from both sides."),
        ({"b"}, r"These two strategies together with applying the identity $\sec^2x\equiv1+\tan^2x$ usually led to a "
                r"3-term quadratic in $\tan x$.", BACK),
        ({"b"}, r"Most students used a correct method, usually by factorising, to solve their quadratic equation in "
                r"$\tan x$ but only a few stated all three correct solutions."),
        ({"b"}, r"As a result of cancelling either $\tan x\sin2x$ or $1-\cos2x$ from both sides of their equation, many "
                r"students missed out the correct solution $x=0$."),
        ({"b"}, r"Those students who factorised out these terms were usually more successful in finding $x=0$.", BACK),
        ({"b"}, r"Some students did not give their other two solutions in the required form of the exact "
                r"$x=-\frac{\pi}{4}$ and $x=1.326$ to 3 decimal places."),
    ],
    "13": [
        (W, "This question, despite being unstructured, proved accessible, with many students scoring at least 7 out of "
            "the 10 marks available."),
        (W, "Those students who annotated the diagram were generally more successful in formulating a correct strategy "
            "to find the area of the region $R$.", NO),
        (W, r"Most students differentiated $y=x\ln x$ by using the product rule to give the correct "
            r"$\frac{\mathrm{d}y}{\mathrm{d}x}=1+\ln x$."),
        (W, r"A few students found the correct $\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{x}{x}+\ln x$ and simplified this "
            r"incorrectly to give $\frac{\mathrm{d}y}{\mathrm{d}x}=\ln x$.", NO),
        (W, r"Many students used a complete method to find the $x$-value where the normal to $C$ at "
            r"$(\mathrm{e}, \mathrm{e})$ cuts through the $x$-axis, with the majority finding the correct "
            r"$x=3\mathrm{e}$."),
        (W, r"Most students integrated $y=x\ln x$ correctly by using integration by parts to give "
            r"$\frac{1}{2}x^2\ln x-\frac{1}{4}x^2$."),
        (W, r"Many students applied the correct limits of e and 1 to obtain a correct $\frac{1}{4}\mathrm{e}^2+"
            r"\frac{1}{4}$ with some making a bracketing error when applying the limit of 1 to obtain the incorrect "
            r"$\frac{1}{4}\mathrm{e}^2-\frac{1}{4}$."),
        (W, r"The majority of students attempted to find the area of the triangle by using the formula "
            r"$\frac{1}{2}(\text{base})(\text{height})$."),
        (W, r"While some students applied the formula correctly to give $\frac{1}{2}(3\mathrm{e}-\mathrm{e})(\mathrm{e})$, "
            r"there was a considerable number that applied a base length of $3\mathrm{e}$ by writing "
            r"$\frac{1}{2}(3\mathrm{e})(\mathrm{e})$."),
        (W, r"A few students used the equation of the normal to find the area of the triangle by applying the correct "
            r"$\int_{\mathrm{e}}^{3\mathrm{e}}\left(-\frac{1}{2}x+\frac{3}{2}\mathrm{e}\right)\mathrm{d}x$, but not many "
            r"evaluated this to arrive at the correct answer of $\mathrm{e}^2$.", NO),
        (W, r"Several incorrect strategies were seen such as trying to evaluate $\int_0^{\mathrm{e}}x\ln x\,\mathrm{d}x$, "
            r"$\int_1^{3\mathrm{e}}x\ln x\,\mathrm{d}x$ or even $\int_1^{3\mathrm{e}}\left(x\ln x-\left(-\frac{1}{2}x+"
            r"\frac{3}{2}\mathrm{e}\right)\right)\mathrm{d}x$.", NO),
        (W, r"Only a minority of students applied the calculation $\frac{1}{4}\mathrm{e}^2+\frac{1}{4}+\mathrm{e}^2$ to "
            r"achieve the correct $\frac{5}{4}\mathrm{e}^2+\frac{1}{4}$."),
    ],
    "14": [
        (W, "This was the most demanding question on the paper.", NO),
        ({"a", "d"}, "Parts (a) and (d) were accessible to many students."),
        ({"b", "c"}, "Most students made some creditable progress in part (b), but many students found it difficult to "
                     "access the demanding material in part (c).", NO),
        ({"a"}, "In part (a), most students evaluated or deduced that there were 90 mice at the start of the study."),
        ({"b"}, r"In part (b), most students used either the chain rule or the quotient rule in their attempt to find an "
                r"expression for $\frac{\mathrm{d}N}{\mathrm{d}t}$."),
        ({"b"}, r"There were many incorrect attempts at the chain rule such as $\frac{\mathrm{d}N}{\mathrm{d}t}=-6300"
                r"\mathrm{e}^{-0.25t}(3+7\mathrm{e}^{-0.25t})^{-2}$ or $\frac{\mathrm{d}N}{\mathrm{d}t}=1575(3+7"
                r"\mathrm{e}^{-0.25t})^{-2}$ while the most common incorrect attempt at the quotient rule was "
                r"$\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{(3+7\mathrm{e}^{-0.25t})(1)+1575\mathrm{e}^{-0.25t}}{(3+7"
                r"\mathrm{e}^{-0.25t})^2}$.", NO),
        ({"b"}, r"Although some impressive algebra was seen in manipulating a correct $\frac{\mathrm{d}N}{\mathrm{d}t}="
                r"\frac{1575\mathrm{e}^{-0.25t}}{(3+7\mathrm{e}^{-0.25t})^2}$ to achieve $\frac{\mathrm{d}N}{\mathrm{d}t}="
                r"\frac{N(300-N)}{1200}$, many students were unsuccessful in their attempts at eliminating $t$ or the "
                r"$\mathrm{e}^{-0.25t}$ term."),
        ({"b"}, r"Some students substituted $N=\frac{900}{3+7\mathrm{e}^{-0.25t}}$ into $\frac{\mathrm{d}N}{\mathrm{d}t}="
                r"\frac{N(300-N)}{1200}$ and used algebra to give $\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{1575"
                r"\mathrm{e}^{-0.25t}}{(3+7\mathrm{e}^{-0.25t})^2}$, and provided some indication that their proof was "
                r"complete."),
        ({"b"}, r"Some students differentiated $N$ by using implicit differentiation while other students attempted to "
                r"rearrange the given equation for $N$ to make $t$ the subject before finding an expression for "
                r"$\frac{\mathrm{d}t}{\mathrm{d}N}$."),
        ({"b"}, r"A few students were successful in applying an alternative method of solving the differential equation "
                r"$\frac{\mathrm{d}N}{\mathrm{d}t}=\frac{N(300-N)}{1200}$ to give $N=\frac{900}{3+7\mathrm{e}^{-0.25t}}$."),
        ({"c"}, r"In part (c), most students misinterpreted the question and instead applied a method to find the time "
                r"$T$ for the maximum value of $N$, rather than the time $T$ at which the rate of growth "
                r"$\frac{\mathrm{d}N}{\mathrm{d}t}$ was a maximum."),
        ({"c"}, r"Many students, therefore, used $N=300$ and manipulated $300=\frac{900}{3+7\mathrm{e}^{-0.25T}}$ to give "
                r"$\mathrm{e}^{-0.25T}=0$."),
        ({"c"}, r"A few students differentiated $\frac{\mathrm{d}N}{\mathrm{d}t}$, with most writing "
                r"$\frac{\mathrm{d}^2N}{\mathrm{d}t^2}$, which was condoned, and solved the equation "
                r"$\frac{1}{1200}(300-2N)$ to give $N=150$."),
        ({"c"}, r"It was rare to see students using the symmetry of the quadratic function $\frac{N(300-N)}{1200}$ to "
                r"deduce that $N=150$.", NO),
        ({"c"}, r"Although some students gave their answer to part (c) as $T=150$, most students who progressed this far "
                r"solved the equation $150=\frac{900}{3+7\mathrm{e}^{-0.25T}}$ to give the correct value for $T$.", BACK),
        ({"d"}, r"In part (d), many students deduced $P=300$ with only a few students deducing $P=299$, which was also "
                r"accepted."),
    ],
}

# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
RATINGS = {
    "01a": ("easy", ("01", 1)),
    "01b": ("hard", ("01", 3)),
    "01c": ("easy", ("01", 5)),
    "02a": ("easy", ("02", 1)),
    "02b": ("easy", ("02", 6)),
    "03a": ("easy", ("03", 1)),
    "03b": ("medium", ("03", 0)),
    "04i": ("medium", ("04", 4)),
    "04ii": ("medium", ("04", 11)),
    "05a": ("medium", ("05", 2)),
    "05b": ("easy", ("05", 5)),
    "05c": ("hard", ("05", 6)),
    "06a": ("easy", ("06", 4)),
    "06b": ("hard", ("06", 11)),
    "06c": ("medium", ("06", 12)),
    "07i": ("easy", ("07", 0)),
    "07ii": ("medium", ("07", 0)),
    "08a": ("easy", ("08", 2)),
    "08b": ("medium", ("08", 9)),
    "08c": ("medium", ("08", 10)),
    "09": ("easy", ("09", 0)),
    "10a": ("hard", ("10", 2)),
    "10b": ("medium", ("10", 11)),
    "10c": ("easy", ("10", 13)),
    "11a": ("easy", ("11", 4)),
    "11b": ("hard", ("11", 9)),
    "12a": ("easy", ("12", 1)),
    "12b": ("hard", ("12", 7)),
    "13": ("hard", ("13", 11)),
    "14a": ("easy", ("14", 3)),
    "14b": ("hard", ("14", 6)),
    "14c": ("hard", ("14", 10)),
    "14d": ("medium", ("14", 15)),
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
