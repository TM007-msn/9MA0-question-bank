"""Draft builder for 8MA0-01 2023-06 (AS Pure, June 2023).

Run (from the project root, with the venv active):
    python extraction/8MA0-01_2023-06.py        # writes out/drafts/8MA0-01_2023-06.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-01_2023-06.json

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

P, S = "8MA0-01", "2023-06"
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
        "Solutions relying on calculator technology are not acceptable."]
SHOWR = ["In this question you must show detailed reasoning.",
         "Solutions relying entirely on calculator technology are not acceptable."]
Q1 = ["A curve has equation", r"$$y=\frac{2}{3}x^3-\frac{7}{2}x^2-4x+5$$"]
Q1A = r"Find $\frac{\mathrm{d}y}{\mathrm{d}x}$ writing your answer in simplest form."
Q3 = [r"[Figure 1: sketch of three phone masts: $C$ at the bottom with a North arrow drawn upwards from it, $A$ to "
      r"the north-east of $C$, and $B$ further from $C$, north-east of $C$ and north of $A$.]",
      "Figure 1 is a sketch showing the position of three phone masts, $A$, $B$ and $C$.",
      "The masts are identical and their bases are assumed to lie in the same horizontal plane.",
      "From mast $C$",
      r"• mast $A$ is 8.2 km away on a bearing of $072^\circ$",
      r"• mast $B$ is 15.6 km away on a bearing of $039^\circ$"]
Q3A = "Find the distance between masts $A$ and $B$, giving your answer in km to one decimal place."
Q4A = ["Sketch the curve with equation", r"$$y=\frac{k}{x}\qquad x\neq0$$", "where $k$ is a positive constant."]
Q6 = ["The circle $C$ has equation", "$$x^2+y^2-6x+10y+k=0$$", "where $k$ is a constant."]
Q7 = ["The distance a particular car can travel in a journey starting with a full tank of fuel was investigated.",
      "• From a full tank of fuel, 40 litres remained in the car’s fuel tank after the car had travelled 80 km",
      "• From a full tank of fuel, 25 litres remained in the car’s fuel tank after the car had travelled 200 km",
      "Using a linear model, with $V$ litres being the volume of fuel remaining in the car’s fuel tank and $d$ km "
      "being the distance the car had travelled,"]
Q7A = "find an equation linking $V$ with $d$."
Q7B = ["Given that, on a particular journey", "• the fuel tank of the car was initially full",
       "• the car continued until it ran out of fuel", "find, according to the model,",
       "(b) (i) the initial volume of fuel that was in the fuel tank of the car,",
       "(ii) the distance that the car travelled on this journey."]
Q10 = [r"[Figure 4: the line $l_1$ with positive gradient crossing the negative $x$-axis at $A$, and the line $l_2$ with "
       r"negative gradient crossing the positive $x$-axis at $B$; the lines meet at $C$, above the $x$-axis and to the "
       r"right of the $y$-axis.]",
       r"The line $l_1$ has equation $y=\frac{3}{5}x+6$",
       "The line $l_2$ is perpendicular to $l_1$ and passes through the point $B(8,0)$, as shown in the sketch in "
       "Figure 4."]
Q10A = ["Show that an equation for line $l_2$ is", "$$5x+3y=40$$"]
Q11 = ["The height, $h$ metres, of a plant, $t$ years after it was first measured, is modelled by the equation",
       r"$$h=2.3-1.7\mathrm{e}^{-0.2t}\qquad t\in\mathbb{R}\quad t\geqslant0$$"]
Q12A = ["Show that the equation", r"$$4\tan x=5\cos x$$", "can be written as", r"$$5\sin^2x+4\sin x-5=0$$"]
Q12B = [r"Hence solve, for $0<x\leqslant360^\circ$", r"$$4\tan x=5\cos x$$", "giving your answers to one decimal place."]
Q13 = ["Relative to a fixed origin $O$",
       r"• point $A$ has position vector $10\mathbf{i}-3\mathbf{j}$",
       r"• point $B$ has position vector $-8\mathbf{i}+9\mathbf{j}$",
       r"• point $C$ has position vector $-2\mathbf{i}+p\mathbf{j}$ where $p$ is a constant"]
Q15 = ["In this question you must show detailed reasoning.",
       "Solutions relying on calculator technology are not acceptable.",
       "The curve $C_1$ has equation $y=8-10x+6x^2-x^3$",
       "The curve $C_2$ has equation $y=x^2-12x+14$"]
Q15A = "Verify that when $x=1$ the curves $C_1$ and $C_2$ intersect."
Q17 = ["In this question $p$ and $q$ are positive integers with $q>p$",
       "Statement 1: $q^3-p^3$ is never a multiple of 5"]

LATEX = {
    "01a": L(*Q1, Q1A),
    "01b": L(*Q1, "(a) " + Q1A, "(b) Hence find the range of values of $x$ for which $y$ is decreasing."),
    "02": L(*SHOW, r"Using the substitution $u=\sqrt{x}$ or otherwise, solve", r"$$6x+7\sqrt{x}-20=0$$"),
    "03a": L(*Q3, Q3A),
    "03b": L(*Q3, "(a) " + Q3A, "An engineer needs to travel from mast $A$ to mast $B$.",
             "(b) Give a reason why the answer to part (a) is unlikely to be an accurate value for the distance the "
             "engineer travels."),
    "04a": L(*Q4A),
    "04b": L("(a) " + Q4A[0], *Q4A[1:], "(b) Hence or otherwise, solve", r"$$\frac{16}{x}\leqslant2$$"),
    "05": L(*SHOW,
            r"[Figure 2: part of the curve $y=4x^2+3$ for $x\geqslant0$, meeting the $y$-axis above $O$; the horizontal "
            r"line $y=23$ meets the $y$-axis at 23 and meets the curve; the region $R$ between the $y$-axis, the curve and "
            r"the line $y=23$ is shaded.]",
            "The finite region $R$, shown shaded in Figure 2, is bounded by the curve with equation $y=4x^2+3$, the "
            "$y$-axis and the line with equation $y=23$",
            r"Show that the exact area of $R$ is $k\sqrt{5}$ where $k$ is a rational constant to be found."),
    "06a": L(*Q6, "Find the coordinates of the centre of $C$."),
    "06b": L(*Q6, "Given that $C$ does not cut or touch the $x$-axis,", "find the range of possible values for $k$."),
    "07a": L(*Q7, Q7A),
    "07b": L(*Q7, "(a) " + Q7A, *Q7B),
    "07c": L(*Q7, "(a) " + Q7A, *Q7B, "In fact the car travelled 320 km on this journey.",
             "(c) Evaluate the model in light of this information."),
    "08": L(r"[Figure 3: a U-shaped curve $C$ crossing the $x$-axis at $O$ and 6, with its minimum below the $x$-axis; "
            r"the straight line $l$, with positive gradient, crosses the $y$-axis at 60 and meets $C$ at $(10, 80)$ and at "
            r"a point to the left of the $y$-axis; the region $R$ between $l$ and $C$ is shaded.]",
            "Figure 3 shows a sketch of a curve $C$ and a straight line $l$.",
            "Given that",
            r"• $C$ has equation $y=\mathrm{f}(x)$ where $\mathrm{f}(x)$ is a quadratic expression in $x$",
            "• $C$ cuts the $x$-axis at 0 and 6",
            "• $l$ cuts the $y$-axis at 60 and intersects $C$ at the point $(10, 80)$",
            "use inequalities to define the region $R$ shown shaded in Figure 3."),
    "09": L("Using the laws of logarithms, solve the equation", r"$$2\log_5(3x-2)-\log_5x=2$$"),
    "10a": L(*Q10, *Q10A),
    "10b": L(*Q10, "(a) " + Q10A[0], Q10A[1], "Given that", "• lines $l_1$ and $l_2$ intersect at the point $C$",
             "• line $l_1$ crosses the $x$-axis at the point $A$",
             r"(b) find the exact area of triangle $ABC$, giving your answer as a fully simplified fraction in the form "
             r"$\frac{p}{q}$"),
    "11a": L(*Q11, "Using the model,", "find the height of the plant when it was first measured,"),
    "11b": L(*Q11, "Show that, exactly 4 years after it was first measured, the plant was growing at approximately "
             "15.3 cm per year."),
    "11c": L(*Q11, "According to the model, there is a limit to the height to which this plant can grow.",
             "Deduce the value of this limit."),
    "12a": L(*SHOWR, *Q12A),
    "12b": L(*SHOWR, "(a) " + Q12A[0], *Q12A[1:], "(b) " + Q12B[0], *Q12B[1:]),
    "12c": L(*SHOWR, "(a) " + Q12A[0], *Q12A[1:], "(b) " + Q12B[0], *Q12B[1:],
             "(c) Hence find the number of solutions of the equation", r"$$4\tan3x=5\cos3x$$",
             r"in the interval $0<x\leqslant1800^\circ$, explaining briefly the reason for your answer."),
    "13a": L(*Q13, r"Find $\overrightarrow{AB}$"),
    "13b": L(*Q13, r"Find $\left|\overrightarrow{AB}\right|$ giving your answer as a fully simplified surd."),
    "13c": L(*Q13, "Given that points $A$, $B$ and $C$ lie on a straight line,", "(i) find the value of $p$,",
             "(ii) state the ratio of the area of triangle $AOC$ to the area of triangle $AOB$."),
    "14": L("Find, in simplest form, the coefficient of $x^5$ in the expansion of",
            r"$$\left(5+8x^2\right)\left(3-\frac{1}{2}x\right)^6$$"),
    "15a": L(*Q15, Q15A),
    "15b": L(*Q15, "(a) " + Q15A, "The curves also intersect when $x=k$.", "Given that $k<0$",
             "(b) use algebra to find the exact value of $k$."),
    "16": L(r"A curve has equation $y=\mathrm{f}(x)$, $x\geqslant0$", "Given that",
            r"• $\mathrm{f}'(x)=4x+a\sqrt{x}+b$, where $a$ and $b$ are constants",
            "• the curve has a stationary point at $(4,3)$", "• the curve meets the $y$-axis at $-5$",
            r"find $\mathrm{f}(x)$, giving your answer in simplest form."),
    "17a": L(*Q17, r"Show, by means of a counter example, that Statement 1 is $\textbf{not}$ true."),
    "17b": L(*Q17, r"Statement 2: When $p$ and $q$ are consecutive $\textbf{even}$ integers $q^3-p^3$ is a multiple of 8",
             "Prove, using algebra, that Statement 2 is true."),
}

# Earlier parts shown where a part needs their result (standalone sweep, 2026-10-10).
LATEX.update({
    "06b": L(
        r"The circle $C$ has equation",
        r"$$x^2+y^2-6x+10y+k=0$$",
        r"where $k$ is a constant.",
        r"(a) Find the coordinates of the centre of $C$.",
        r"Given that $C$ does not cut or touch the $x$-axis,",
        r"(b) find the range of possible values for $k$.",
    ),
    "13b": L(
        r"Relative to a fixed origin $O$",
        r"• point $A$ has position vector $10\mathbf{i}-3\mathbf{j}$",
        r"• point $B$ has position vector $-8\mathbf{i}+9\mathbf{j}$",
        r"• point $C$ has position vector $-2\mathbf{i}+p\mathbf{j}$ where $p$ is a constant",
        r"(a) Find $\overrightarrow{AB}$",
        r"(b) Find $\left|\overrightarrow{AB}\right|$ giving your answer as a fully simplified surd.",
    ),
    "13c": L(
        r"Relative to a fixed origin $O$",
        r"• point $A$ has position vector $10\mathbf{i}-3\mathbf{j}$",
        r"• point $B$ has position vector $-8\mathbf{i}+9\mathbf{j}$",
        r"• point $C$ has position vector $-2\mathbf{i}+p\mathbf{j}$ where $p$ is a constant",
        r"(a) Find $\overrightarrow{AB}$",
        r"Given that points $A$, $B$ and $C$ lie on a straight line,",
        r"(c) (i) find the value of $p$,",
        r"(ii) state the ratio of the area of triangle $AOC$ to the area of triangle $AOB$.",
    ),
})

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", DIFF, "7.2", 2, LATEX["01a"],
      [r"M1 (AO 1.1b): $\left\{\frac{\mathrm{d}y}{\mathrm{d}x}=\right\}2x^2-7x-4$. Notes: Decreases the power of $x$ by one "
       r"for at least one of their terms. Look for $x^n\to\ldots x^{n-1}$ Allow for $5\to0$",
       r"A1 (AO 1.1b): $\left\{\frac{\mathrm{d}y}{\mathrm{d}x}=\right\}2x^2-7x-4$. Notes: "
       r"$\left\{\frac{\mathrm{d}y}{\mathrm{d}x}=\right\}2x^2-7x-4$"],
      False, 2),
    e("01b", "1(b)", DIFF, "7.3, 2.5", 4, LATEX["01b"],
      [r"M1 (AO 1.1b): Attempts to solve $\left\{\frac{\mathrm{d}y}{\mathrm{d}x}=\right\}2x^2-7x-4\ldots0$ e.g., "
       r"$(2x+1)(x-4)=0$ leading to $x=\ldots$ and $x=\ldots$ Notes: Sets their $\frac{\mathrm{d}y}{\mathrm{d}x}\ldots0$ "
       r"where $\ldots$ may be an equality or an inequality and proceeds to find two values for $x$ from a 3TQ using the "
       r"usual rules. This may be implied by their critical values.",
       r"A1 (AO 1.1b): Correct critical values $x=-\frac{1}{2},4$. Notes: Correct critical values $x\ldots-\frac{1}{2},4$ "
       r"These may come directly from a calculator and might only be seen on a sketch.",
       r"dM1 (AO 1.1b): Chooses inside region for their critical values. Notes: Chooses the inside region for their "
       r"critical values.",
       r"A1 (AO 1.1b): Accept either $-\frac{1}{2}<x<4$ or $-\frac{1}{2}\leqslant x\leqslant4$. Notes: Accept either "
       r"$-\frac{1}{2}<x<4$ or $-\frac{1}{2}\leqslant x\leqslant4$ but not, e.g., $-\frac{1}{2}<x\leqslant4$. Condone, "
       r"e.g., $x>-\frac{1}{2},\ x<4$ or $x>-\frac{1}{2}$ and $x<4$ or $\left\{x:x>-\frac{1}{2}\right\}\cap\{x:x<4\}$ or "
       r"$x\in\left(-\frac{1}{2},4\right)$ or $x\in\left[-\frac{1}{2},4\right]$. Note: You may see $x<-\frac{1}{2},x<4$ in "
       r"their initial work before $-\frac{1}{2}<x<4$. Condone this so long as it is clear that the $-\frac{1}{2}<x<4$ is "
       r"their final answer."],
      False, 2),

    # ---------------- Q2 ----------------
    e("02", "2", ALG, "2.3, 2.1", 4, LATEX["02"],
      [r"M1 (AO 1.1b): Let $u=\sqrt{x}$: $6x+7\sqrt{x}-20=0\Rightarrow6u^2+7u-20=0\Rightarrow(3u-4)(2u+5)\{=0\}$. Notes: "
       r"Attempts a valid method that enables the problem to be solved. See General Principles for Pure Mathematics "
       r"Marking at the front of the mark scheme for guidance. Score for either letting $u=\sqrt{x}$ and attempting to "
       r"factorise to $(au\pm c)(bu\pm d)$ with $ab=6, cd=20$ or making $7\sqrt{x}$ the subject and attempting to square "
       r"both sides. or attempting to factorise to $(a\sqrt{x}\pm c)(b\sqrt{x}\pm d)$ with $ab=6, cd=20$ or by quadratic "
       r"formula or completing the square following usual rules.",
       r"A1 (AO 1.1b): $(3u-4)(2u+5)\{=0\}$. Notes: $(3u-4)(2u+5)\{=0\}$ or $36x^2-289x+400\{=0\}$ or "
       r"$(3\sqrt{x}-4)(2\sqrt{x}+5)\{=0\}$. If they use the formula, it must be correct e.g., "
       r"$u\{\text{or }\sqrt{x}\}=\frac{-7\pm\sqrt{7^2-4(6)(-20)}}{12}$ followed by $u\{\text{or }\sqrt{x}\}=\frac{4}{3}$ or "
       r"equivalent e.g., $\frac{16}{12}$. Ignore if they have $u\{\text{or }\sqrt{x}\}=-\frac{5}{2}$ or not. If they "
       r"complete the square, they must have $\left(u+\frac{7}{12}\right)^2=\frac{529}{144}$ followed by "
       r"$u\{\text{or }\sqrt{x}\}=\frac{4}{3}$ or equivalent e.g., $\frac{16}{12}$. Ignore if they have "
       r"$u\{\text{or }\sqrt{x}\}=-\frac{5}{2}$ or not.",
       r"M1 (AO 1.1b): Attempts $\sqrt{x}=\text{“}\frac{4}{3}\text{”},\text{“}-\frac{5}{2}\text{”}\Rightarrow x=\ldots$ "
       r"Notes: Correct method from $p\sqrt{x}\pm q=0$ leading to $x=\ldots$ by squaring. In Alt 1, it is for solving their "
       r"quadratic using the General Principles for Pure Mathematics Marking. There must be a method shown, i.e., the "
       r"solutions should not come straight from a calculator. If attempting to factorise, it must be to "
       r"$(ax\pm c)(bx\pm d)$ with $ab=36, cd=400$. In Alt 2, it is for squaring their value(s) for $u$ to get $x=\ldots$",
       r"A1 cso (AO 2.3): $x=\frac{16}{9}$ only. Notes: cso $x=\frac{16}{9}$ only. $x=\frac{25}{4}$ must be discarded. "
       r"Note 0011 is not possible. Allow “incorrect” $x=-\frac{16}{9}$ or $x=-\frac{25}{4}$ to be seen as long as they "
       r"are discarded. Ignore any reason they give for rejecting solutions. Note that a method to solve their quadratic "
       r"must be seen – solutions must not come directly from a calculator. Simply stating the quadratic formula (without "
       r"substitution) is insufficient.",
       r"ALT: Alt 1 — M1 (AO 1.1b): $6x+7\sqrt{x}-20=0\Rightarrow7\sqrt{x}=20-6x\Rightarrow49x=(20-6x)^2"
       r"\Rightarrow49x=400-240x+36x^2$",
       r"ALT: Alt 1 — A1 (AO 1.1b): $36x^2-289x+400\{=0\}$",
       r"ALT: Alt 1 — M1 (AO 1.1b): $(9x-16)(4x-25)=0$",
       r"ALT: Alt 1 — A1 cso (AO 2.3): $x=\frac{16}{9}$ only",
       r"ALT: Alt 2 — M1 A1 (AO 1.1b, 1.1b): $6x+7\sqrt{x}-20=0\Rightarrow(3\sqrt{x}-4)(2\sqrt{x}+5)=0$",
       r"ALT: Alt 2 — M1 (AO 1.1b): Attempts $\sqrt{x}=\text{“}\frac{4}{3}\text{”},\text{“}-\frac{5}{2}\text{”}"
       r"\Rightarrow x=\ldots$",
       r"ALT: Alt 2 — A1 cso (AO 2.3): $x=\frac{16}{9}$ only"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", TRIG, "5.1", 3, LATEX["03a"],
      [r"B1 (AO 1.1b): Angle $ACB=33^\circ$. Notes: 33 seen anywhere but allow $72-39$. May be indicated on a diagram "
       r"(including incorrectly) or on the given Figure 1 and it might be named incorrectly.",
       r"M1 (AO 1.1b): Attempts $\left\{AB^2=\right\}8.2^2+15.6^2-2\times8.2\times15.6\cos33^\circ$. Notes: Uses the given "
       r"model and attempts to use the cosine rule to find the distance or distance$^2$. Award for "
       r"$8.2^2+15.6^2-2\times8.2\times15.6\cos\ldots$ where $\ldots$ must be a value.",
       r"A1 (AO 1.1b): Distance = awrt 9.8 {km}. Notes: awrt 9.8 {km} isw",
       r"ALT: (a) Alternative — B1: $\left\{\overrightarrow{AB}=\right\}\pm\begin{pmatrix}15.6\cos51-8.2\cos18\\"
       r"15.6\sin51-8.2\sin18\end{pmatrix}$ or $\pm\begin{pmatrix}15.6\sin39-8.2\sin72\\15.6\cos39-8.2\cos72"
       r"\end{pmatrix}$ o.e. May be implied by calculation that leads to $\begin{pmatrix}\text{awrt}\pm2.0\\"
       r"\text{awrt}\pm9.6\end{pmatrix}$ e.g. $\begin{pmatrix}9.8\\12.1\end{pmatrix}-\begin{pmatrix}7.8\\2.5"
       r"\end{pmatrix}$. Note: they may find components separately and condone, e.g., $\begin{pmatrix}\text{awrt}\pm9.6\\"
       r"\text{awrt}\pm2.0\end{pmatrix}$",
       r"ALT: (a) Alternative — M1: Attempts to find $\overrightarrow{AB}$ (as above) and uses Pythagoras to find distance "
       r"or distance$^2$",
       r"ALT: (a) Alternative — A1: awrt 9.8 {km} isw"],
      True, 6),
    e("03b", "3(b)", TRIG, "5.1", 1, LATEX["03b"],
      [r"B1 (AO 3.2b): • Explains that the road is not likely to be straight {and therefore the distance will be greater}. "
       r"• Explains that there are likely to be objects in the way {that they must go around and therefore the distance "
       r"travelled will be greater}. • The {bases of the} masts are not likely to lie in the same {horizontal} plane {and "
       r"so the distance will be greater}. Notes: A valid reason based on the assumptions, i.e., the plane is not really "
       r"horizontal or the journey not being in a straight line. Do not accept answers referencing the accuracy of the "
       r"answer to part (a) being to 1d.p. or the accuracy of the values given in the question, but ignore if there is a "
       r"separate, valid reason. Some examples: “Because it is unlikely the bearings are exact” – B0 see above. “Because "
       r"they may not walk in a straight line because they could take another longer or shorter route as their route "
       r"could be more curved” – B0 – incorrect comment about there being a shorter route. “Because they won’t travel in "
       r"one direction due to the roads” – B1 BOD. “Impossible and unrealistic to walk in a straight line” – B1"],
      True, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", ALG, "2.7", 2, LATEX["04a"],
      [r"M1 (AO 1.1b): Shape in quadrant 1 or 3 (beside the mark scheme's sketch of $y=\frac{k}{x}$ with branches in "
       r"quadrants 1 and 3). Notes: For the correct shape in quadrant 1 or 3. Do not be concerned about position but it "
       r"must not cross either axis. Ignore incorrect asymptotes for this mark.",
       r"A1 (AO 1.1b): Shape and Position. Notes: Correct shape and position. There should be no curve in either quadrant "
       r"2 or quadrant 4. The curve must not clearly bend back on itself but condone slips of the pen."],
      False, 8),
    e("04b", "4(b)", ALG, "2.5, 2.7", 3, LATEX["04b"],
      [r"B1 (AO 2.2a): Deduces that $x<0$. Notes: Deduces that $x<0$ but condone $x\leqslant0$ for this mark.",
       r"M1 (AO 1.1b): Attempts $\frac{16}{x}\ldots2\Rightarrow x\ldots\pm\frac{16}{2}$. Notes: Attempts "
       r"$\frac{16}{x}\ldots2\Rightarrow x\ldots\pm\frac{16}{2}$ where the $\ldots$ means any equality or inequality.",
       r"A1 cso (AO 2.2a): $x<0$ or $x\geqslant8$. Notes: cso $x<0$ or $x\geqslant8$ (Both required). Set notation may be "
       r"seen $\{x:x<0\}\cup\{x:x\geqslant8\}$ o.e. $x\in(-\infty,0)\cup[8,\infty)$. Accept $x<0$, $x\geqslant8$ but not "
       r"$x<0$ and $x\geqslant8$. Must not be combined incorrectly, e.g., $8\leqslant x<0$ or "
       r"$\{x:x<0\}\cap\{x:x\geqslant8\}$"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05", "5", INT, "8.3, 8.2", 5, LATEX["05"],
      [r"B1 (AO 1.1b): States or uses the upper limit is $\sqrt{5}$. Notes: States or uses the upper limit $\sqrt{5}$ "
       r"Score when seen as the solution $x=\sqrt{5}$",
       r"M1 (AO 1.1b): $\int4x^2+3\,\mathrm{d}x=\frac{4}{3}x^3+3x$. Notes: Attempts to integrate $4x^2+3$ or "
       r"$\pm(23-(4x^2+3))$ which may be simplified. Look for one term from $4x^2+3$ with $x^n\to x^{n+1}$ It is not "
       r"sufficient just to integrate 23.",
       r"A1 (AO 1.1b): $\int4x^2+3\,\mathrm{d}x=\frac{4}{3}x^3+3x$. Notes: Correct integration. Ignore any $+c$ or spurious "
       r"integral signs. Indices must be processed. Look for $\int4x^2+3\,\{\mathrm{d}x\}=\frac{4}{3}x^3+3x$ or "
       r"$\pm\int20-4x^2\,\{\mathrm{d}x\}=\pm\left(20x-\frac{4}{3}x^3\right)$ if (line $-$ curve) or (curve $-$ line) used.",
       r"M1 (AO 2.1): Full method of finding the area of $R$ e.g. $23\sqrt{5}-\left[\frac{4}{3}x^3+3x\right]_0^{\sqrt{5}}"
       r"=\ldots$ e.g. $\left[20x-\frac{4}{3}x^3\right]_0^{\sqrt{5}}=\ldots$ Notes: Full and complete method to find the area "
       r"of $R$ including the substitution of their upper limit. The upper limit must come from an attempt to solve "
       r"$4x^2+3=23$. The lower limit might not be seen but if seen it should be 0. See scheme for two possible ways. "
       r"Condone a sign slip if (line $-$curve) or (curve $-$ line) used.",
       r"A1 (AO 1.1b): $\Rightarrow$ Area $R=\frac{40}{3}\sqrt{5}$. Notes: $\frac{40}{3}\sqrt{5}$ following correct "
       r"algebraic integration. If using (curve $-$ line) then allow recovery but they must make the "
       r"$-\frac{40}{3}\sqrt{5}$ positive.",
       r"ALT: Alternative using $\int x\,\mathrm{d}y$ — B1: States or uses limits 3 and 23. It must be for a clear attempt "
       r"to integrate with respect to $y$",
       r"ALT: Alternative using $\int x\,\mathrm{d}y$ — M1: Attempts to rearrange to $x=$ and integrate "
       r"$\sqrt{\frac{y-3}{4}}$ condoning slips on the rearrangement. Look for $\ldots(y\pm3)^{\frac{1}{2}}\to"
       r"\ldots(y\pm3)^{\frac{3}{2}}$",
       r"ALT: Alternative using $\int x\,\mathrm{d}y$ — A1: Correct integration $\int\frac{(y-3)^{\frac{1}{2}}}{2}\,"
       r"\{\mathrm{d}y\}=\frac{1}{3}(y-3)^{\frac{3}{2}}$ Ignore any $+c$ or spurious integral signs.",
       r"ALT: Alternative using $\int x\,\mathrm{d}y$ — M1: Full and complete method to find the area of $R$ including the "
       r"substitution of their limits. In this case it would be for substituting 23 and 3 and subtracting either way "
       r"round into their changed expression in terms of $y$",
       r"ALT: Alternative using $\int x\,\mathrm{d}y$ — A1: $\frac{40}{3}\sqrt{5}$ following correct algebraic "
       r"integration."],
      True, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", COORD, "3.2", 2, LATEX["06a"],
      [r"M1 (AO 1.1b): $(x-3)^2+(y+5)^2\pm\ldots=\ldots$ Notes: For sight of $(x\pm3)^2\pm(y\pm5)^2\pm\ldots=\ldots$ or one "
       r"coordinate for centre from $(\pm3,\pm5)$",
       r"A1 (AO 1.1b): Centre $(3,-5)$. Notes: Centre $(3,-5)$"],
      False, 12),
    e("06b", "6(b)", COORD, "3.2, 2.5", 3, LATEX["06b"],
      [r"B1ft (AO 2.2a): Deduces that $k=9$ is a critical point. Notes: Deduces that $k\ldots9$ is a critical point. Allow "
       r"this to come from their $(\text{“}5\text{”})^2$ Condone $\frac{36}{4}$. Note that this might come from setting "
       r"$y=0$ and using the discriminant on $x^2-6x+k=0$",
       r"M1 (AO 3.1a): Recognises that radius $>0$: $\text{“}9\text{”}+\text{“}25\text{”}-k>0$. Notes: "
       r"$(x\pm3)^2+(y\pm5)^2=(\text{“}3\text{”})^2+(\text{“}5\text{”})^2-k$ and recognises that the radius$^2$ must be "
       r"positive so $(\text{“}3\text{”})^2+(\text{“}5\text{”})^2-k>0$ but condone "
       r"$(\text{“}3\text{”})^2+(\text{“}5\text{”})^2-k\geqslant0$. $k<34$ or $k\leqslant34$ would imply this method mark. "
       r"Note: they may have incorrectly calculated $(\text{“}3\text{”})^2+(\text{“}5\text{”})^2$ in (a) so allow their "
       r"value for this in place of $(\text{“}3\text{”})^2+(\text{“}5\text{”})^2$ as long as the intention is clear.",
       r"A1 (AO 1.1b): $9<k<34$. Notes: $9<k<34$ but condone $9<k\leqslant34$. Allow inequalities to be separate, i.e., "
       r"$k>9$, $k<34$. Set notation may be seen $\{k:k>9\}\cap\{k:k<34\}$ or $k\in(9,34)$. Condone "
       r"$\{k:k>9\}\cap\{k:k\leqslant34\}$ or $k\in(9,34]$ or $k>9$ and $k\leqslant34$. Must not be combined incorrectly, "
       r"e.g., $\{k:k>9\}\cup\{k:k<34\}$"],
      False, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", COORD, "3.1", 4, LATEX["07a"],
      [r"B1 (AO 3.3): Uses or implies that $V=ad+b$. Notes: Attempts a linear model, i.e., uses or implies that $V=ad+b$ "
       r"or $d=mV+c$ which may be in terms of, e.g., $y$ and $x$",
       r"M1 (AO 3.1b): Uses both $40=80a+b$ and $25=200a+b$ to get either $a$ or $b$. Notes: Awarded for translating the "
       r"problem in context and starting to solve. It is scored when both $40=80a+b$ and $25=200a+b$ are written down and "
       r"the candidate proceeds to find either $a$ or $b$. Alternatively, scored when both $200=25m+c$ and $80=40m+c$ are "
       r"written down and the candidate proceeds to find either $m$ or $c$. You may just see $\pm\frac{25-40}{200-80}$ or "
       r"$\pm\frac{200-80}{25-40}$ or 8km for every litre o.e. so check carefully for attempts at the gradient.",
       r"dM1 (AO 1.1b): Uses both $40=80a+b$ and $25=200a+b$ to get both $a$ and $b$. Notes: Uses $40=80a+b$ and "
       r"$25=200a+b$ to find both $a$ and $b$ (or $m$ and $c$). Alternatively, if the gradient is found, proceeds to use one "
       r"of the bullet points to find $c$, with the usual rules applying for straight line (coordinates must be used the "
       r"correct way round, i.e., they would lead to the correct answer).",
       r"A1 (AO 1.1b): $\Rightarrow V=-\frac{1}{8}d+50$ o.e. Notes: $V=-\frac{1}{8}d+50$ or exact equivalent, e.g., "
       r"$d=400-8V$ or $d+8V=400$ etc. Withhold this mark if their answer is not stated in terms of $V$ and $d$"],
      False, 14),
    e("07b", "7(b)", COORD, "3.1", 3, LATEX["07b"],
      [r"B1 ft (AO 3.4): States either that the initial volume was 50 {litres} or that the distance travelled was 400 {km}. "
       r"Notes: Mark parts (b)(i) and (b)(ii) together. Note that they may restart and not use an equation. States either "
       r"the initial volume was 50 {litres} or the distance travelled was 400 {km} but it must be clearly for the correct "
       r"part, e.g., $V=50$. Follow through on their $a$ and $b$ (or $m$ and $c$). This may be scored from "
       r"$40+\frac{80}{8}$ or $\frac{400}{8}$",
       r"M1 (AO 3.4): Attempts to find both answers by solving $0=-\frac{1}{8}d+50$ and $0=400-8V$. Notes: Complete attempt "
       r"to find both answers. Must be from a linear model. Substitutes $V=0$ and finds $d$ by attempting to solve their "
       r"$0=-\frac{1}{8}d+50$ and substitutes $d=0$ and finds $V$ by attempting to solve their $0=400-8V$. Note that one "
       r"(or both) of these attempts may be implied by correct values ft their equations.",
       r"A1 (AO 3.2b): States both that the initial volume was 50 litres and that the distance travelled was 400 km. Notes: "
       r"States both 50 litres and 400 km. Units are required to be correct for both values. It must be clear which answer "
       r"applies to each part, which may be simply by correct units. Accept $l$ or $L$ for litres."],
      False, 14),
    e("07c", "7(c)", COORD, "3.1", 1, LATEX["07c"],
      [r"B1ft (AO 3.5a): States, e.g., “Poor model” as 320km is significantly less than 400 km. Notes: Main Scheme "
       r"(comparing (b)(ii) with 320). This mark is only available for answers from (b)(ii) if they are $<290$ or $>350$. "
       r"Concludes poor model (o.e.) and states that 320 is significantly less than “400” (o.e.). Note that $320\ll400$ so "
       r"it is a poor model is acceptable. It is not sufficient to say $320\neq400$ or $320<400$ so it is a poor model. "
       r"Condone “the 400 is too far away from 320”.",
       r"ALT: Alternative (finding remaining fuel after 320 km) — B1ft: States poor model (o.e.) because after 320 km the "
       r"model predicts there will be 10 litres left, which is significantly more than an empty tank / much too high "
       r"compared to an empty tank (o.e.)."],
      False, 14),

    # ---------------- Q8 ----------------
    e("08", "8", ALG, "2.5, 2.3, 3.1", 5, LATEX["08"],
      [r"M1 (AO 1.1b): Complete method to find the RHS of an equation for $l$ e.g., Attempts gradient "
       r"$=\frac{80-60}{10}\{=2\}$ and uses intercept $=60$. Notes: Complete attempt to use the given information to find an "
       r"equation or inequality for $l$, which may be $l=$ or have no LHS. $y-80=2(x-10)$ is acceptable for this mark.",
       r"A1 (AO 1.1b): $\{y=\}2x+60$. Notes: $\{y=\}2x+60$ This is not scored by $y-80=2(x-10)$",
       r"M1 (AO 3.1a): Deduces the RHS of the equation for $C$ is $\{y=\}ax(x-6)$ and attempts to use $(10,80)$ to find the "
       r"value of $a$. Notes: Deduces the RHS of the equation of $C$ is $\{y=\}ax(x-6)$, $a\neq1$, and attempts to use "
       r"$(10,80)$ to find the value of $a$ which may be implied. Again, there may be no LHS.",
       r"A1 (AO 1.1b): Equation of $C$ is $\{y=\}2x(x-6)$. Notes: $\{y=\}2x(x-6)$ or alternative such as "
       r"$\{y=\}2(x-3)^2-18$ or $\{y=\}2x^2-12x$. This may be implied by an inequality $y\ldots2x(x-6)$ and may be seen as, "
       r"e.g., $C=2x(x-6)$",
       r"B1ft (AO 2.5): $2x(x-6)\leqslant y\leqslant2x+60$. Notes: $\text{“}2x(x-6)\text{”}\leqslant y\leqslant"
       r"\text{“}2x+60\text{”}$ o.e. must follow from their $l$ and $C$ and apply isw. Follow through only on a quadratic "
       r"for $C$ and a straight line for $l$. Do not allow a mixture of inequalities, i.e., $<$ with $\leqslant$. Allow "
       r"$2x^2-12x<y<2x+60$ or as separate inequalities $y>2x(x-6)$, $y<2x+60$. Do not allow $2x(x-6)<R<2x+60$ or "
       r"$2x(x-6)<\mathrm{f}(x)<2x+60$ or $2x(x-6)<2x+60$. Ignore any reference to $-3<x<10$. Note: $y=2x+60$ and "
       r"$y=2x(x-6)$ incorrectly expanded to $y=2x^2-12$ followed by $2x^2-12\leqslant y\leqslant2x+60$ would score 11110",
       r"ALT: Other possible and more lengthy alternatives (M1 for $C$) — 1) Setting the RHS to be $\{y=\}a(x-3)^2+b$ and "
       r"using $(0,0)$ and $(10,80)$ to find $a$ and $b$",
       r"ALT: Other possible and more lengthy alternatives (M1 for $C$) — 2) Setting the RHS to be $\{y=\}px^2+qx$ and using "
       r"$(6,0)$ and $(10,80)$ to find $p$ and $q$"],
      True, 16),

    # ---------------- Q9 ----------------
    e("09", "9", EXP, "6.4, 2.3", 5, LATEX["09"],
      [r"B1 (AO 1.1a): Uses one correct law e.g. $2\log_5(3x-2)\to\log_5(3x-2)^2$ or $2\to\log_525$ or "
       r"$\log_5\ldots=2\to\ldots=5^2$. Notes: Uses one correct log law. The base does not need to be seen for this mark. "
       r"This mark is independent of any other errors they make.",
       r"M1 (AO 3.1a): Uses two correct log laws: either $2\log_5(3x-2)\to\log_5(3x-2)^2$ and $2\to\log_525$ or "
       r"$2\log_5(3x-2)-\log_5x\to\log_5\frac{(3x-2)^2}{x}$ leading to an equation without logs. Notes: This can be awarded "
       r"for the overall strategy leading to an equation in $x$ not involving logs. It requires the correct use of two log "
       r"laws as in the main scheme to reach an equation in $x$. This mark may not be awarded for correct application of two "
       r"laws following incorrect log work, but numerical slips are condoned.",
       r"A1 (AO 1.1b): Correct equation without logs, usually $\frac{(3x-2)^2}{x}=25$. Notes: For a correct unsimplified "
       r"equation with logs removed and no incorrect work seen. Ignore any incorrect simplification of their equation. "
       r"Allow recovery on missing brackets, e.g., $\log_5\frac{3x-2^2}{x}=2\to\frac{9x^2-12x+4}{x}=25$. Correct equations "
       r"are likely to be $\frac{(3x-2)^2}{x}=25$ or, e.g., $(3x-2)^2=25x$ but you might see $9x-12+\frac{4}{x}=25$. Sight "
       r"of a correct equation does not imply either the previous M1 or the A1. Note: "
       r"$\frac{\log_5(3x-2)^2}{\log_5x}=2\to\frac{(3x-2)^2}{x}=25$ may be seen and scores B1M0A0.",
       r"dM1 (AO 1.1b): $\frac{(3x-2)^2}{x}=25\Rightarrow9x^2-37x+4=0\Rightarrow(9x-1)(x-4)=0\Rightarrow x=\ldots$ Notes: For "
       r"a correct method to solve their equation, via a 3TQ set $=0$. The 3TQ may be solved by calculator - you may need to "
       r"check their value(s). Can be implied by one correct value for their 3TQ set $=0$ correct to 1d.p.",
       r"A1 cso (AO 3.2a): $x=4$ only. Notes: cso $x=4$ only. If $x=\frac{1}{9}$ is also given it must be rejected. $x=0$ "
       r"might also be seen and must be rejected. Ignore any reasoning for rejecting any values. Note that calculators can "
       r"solve the equation at any stage and so full log work must be shown leading to a 3TQ set $=0$."],
      False, 18),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", COORD, "3.1", 3, LATEX["10a"],
      [r"B1 (AO 1.1b): Deduces that the gradient of line $l_2$ is $-\frac{5}{3}$. Notes: Deduces that the gradient of line "
       r"$l_2$ is $-\frac{5}{3}$ (accept $-\frac{5}{3}x$)",
       r"M1 (AO 1.1b): Complete attempt to find the equation of line $l_2$ e.g., $y-0=-\frac{1}{\text{“}m_1\text{”}}(x-8)$. "
       r"Notes: Complete attempt to find the equation of line $l_2$ using $B(8,0)$ and a changed gradient. If using "
       r"$y=mx+c$ they must be using a changed gradient and proceed as far as $c=\ldots$",
       r"A1* (AO 2.1): $5x+3y=40$ *. Notes: Clear work leading to the given answer of $5x+3y=40$ with no errors seen. There "
       r"is a requirement to “show that” so the must be at least one intermediate line between "
       r"$y-0=-\frac{5}{3}(x-8)$ or finding $c$ (e.g., $y=-\frac{5}{3}x+\frac{40}{3}$) and the answer. Condone $3y+5x=40$",
       r"ALT: (a) Alternative — B1: Rearranges $5x+3y=40$ to $y=-\frac{5}{3}x+\ldots$",
       r"ALT: (a) Alternative — M1: Complete attempt to show that the equation of line $l_2$ is perpendicular to $l_1$ and "
       r"that it passes through $B(8,0)$. Requires: either $-\frac{5}{3}$ is the negative reciprocal of $\frac{3}{5}$ or "
       r"shows $-\frac{5}{3}\times\frac{3}{5}=-1$; evidence that $l_2$ passes through $(8,0)$, e.g., $5(8)+3(0)=40$ or "
       r"$y=-\frac{5}{3}(8)+\frac{40}{3}=0$",
       r"ALT: (a) Alternative — A1*: Clear work showing all elements of $5x+3y=40$ being perpendicular to $l_1$ and that "
       r"$(8,0)$ lies on $5x+3y=40$, as above, with no errors seen and a minimal conclusion."],
      True, 20),
    e("10b", "10(b)", COORD, "3.1, 2.4", 5, LATEX["10b"],
      [r"B1 (AO 2.2a): Deduces $A(-10,0)$. Notes: Deduces $A(-10,0)$ May be awarded on the diagram as -10 or within a "
       r"calculation.",
       r"M1 (AO 1.1b): Attempts to solve $y=\frac{3}{5}x+6$ and $5x+3y=40$ simultaneously to find the $y$ coordinate of their "
       r"point of intersection. Notes: For the attempt to solve $y=\frac{3}{5}x+6$ (or e.g., $5y-3x=30$) and $5x+3y=40$ "
       r"simultaneously to find the $y$ coordinate of their point of intersection. May be implied, i.e., from a calculator "
       r"solution which must be correct to 1d.p. They should be using the given equations but allow slips in rearranging.",
       r"A1 (AO 1.1b): $y$ coordinate of $C$ is $\frac{135}{17}$ o.e. Notes: $y$ coordinate of $C$ is $\frac{135}{17}$ "
       r"(Accept awrt 7.9 for this mark)",
       r"dM1 (AO 2.1): Complete attempt at area $ABC=\frac{1}{2}\times(8+\text{“}10\text{”})\times\text{“}\frac{135}{17}"
       r"\text{”}$. Notes: Scored for a complete and correct attempt to find the exact area of triangle $ABC$. There may be "
       r"numerical slips, e.g., in finding the $x$ coordinates of $A$, but, e.g., the $x$ and $y$ coordinates should not be "
       r"used the wrong way round. Do not allow the use of decimals in place of exact values as they cannot meet the demand "
       r"of the question. See scheme using just the $y$ coordinate of $C$. Another option is to use Pythagoras' theorem to "
       r"find $AC$ and $BC$ lengths using $A(-10,0)$, $B(8,0)$ and their $C\left(\frac{55}{17},\frac{135}{17}\right)$ Note: "
       r"$AC=\frac{45\sqrt{34}}{17}$ and $BC=\frac{27\sqrt{34}}{17}$",
       r"A1 (AO 1.1b): $=\frac{1215}{17}$. Notes: Proceeds correctly to area $ABC=\frac{1215}{17}$",
       r"ALT: (b) Alternative – you might see the following from Further Maths candidates (B1M1A1 as above) — dM1: "
       r"$\frac{1}{2}\begin{vmatrix}8&\text{“}\frac{55}{17}\text{”}&\text{“}-10\text{”}&8\\0&\text{“}\frac{135}{17}"
       r"\text{”}&0&0\end{vmatrix}=\frac{1}{2}\left(8\times\text{“}\frac{135}{17}\text{”}-\text{“}-10\text{”}\times"
       r"\text{“}\frac{135}{17}\text{”}\right)$ or $\frac{1}{2}\begin{vmatrix}8&0&1\\\text{“}\frac{55}{17}\text{”}&"
       r"\text{“}\frac{135}{17}\text{”}&1\\\text{“}-10\text{”}&0&1\end{vmatrix}=\frac{1}{2}\left(8\times\text{“}"
       r"\frac{135}{17}\text{”}-\text{“}-10\text{”}\times\text{“}\frac{135}{17}\text{”}\right)$",
       r"ALT: (b) Alternative (Further Maths candidates) — A1: Proceeds correctly to area $ABC=\frac{1215}{17}$"],
      True, 20),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", EXP, "6.7", 2, LATEX["11a"],
      [r"M1 (AO 3.4): $h=2.3-1.7\mathrm{e}^0$. Notes: Substitutes $t=0$ into $h=2.3-1.7\mathrm{e}^{-0.2t}$ Implied by e.g., "
       r"$h=2.3-1.7\mathrm{e}^{-0}$ or $h=0.6$",
       r"A1 (AO 1.1b): Either 0.6 {m} or 60 cm. Notes: Allow 0.6, 0.6 m, or 60 cm and isw after a correct height. Allow "
       r"$\frac{3}{5}$. The M mark may be implied by A1."],
      False, 24),
    e("11b", "11(b)", EXP, "6.2, 6.7", 3, LATEX["11b"],
      [r"M1 (AO 3.1b): $\left\{\frac{\mathrm{d}h}{\mathrm{d}t}=\right\}0.34\mathrm{e}^{-0.2t}$. Notes: Links rate of change "
       r"to gradient and differentiates $h=2.3-1.7\mathrm{e}^{-0.2t}$ to $k\mathrm{e}^{-0.2t}$, $k\neq-1.7$ Accept, e.g., "
       r"$-0.2\times-1.7\mathrm{e}^{-0.2t}$ Must be seen in (b).",
       r"dM1 (AO 3.4): At $t=4\Rightarrow$ Rate of growth is $0.34\mathrm{e}^{-0.2\times4}=0.15277\ldots"
       r"\{\text{m / year}\}$. Notes: Substitutes $t=4$ into $k\mathrm{e}^{-0.2t}$, $k\neq-1.7$ and calculates its value.",
       r"A1* (AO 1.1b): 0.153 {m per year} = 15.3 cm {per year} *. Notes: Fully correct. Requires: sight of "
       r"$\left\{\frac{\mathrm{d}h}{\mathrm{d}t}=\right\}0.34\mathrm{e}^{-0.2t}$ o.e., e.g., "
       r"$\left\{\frac{\mathrm{d}h}{\mathrm{d}t}=\right\}\frac{17}{50}\mathrm{e}^{-0.2t}$ or "
       r"$\left\{\frac{\mathrm{d}h}{\mathrm{d}t}=\right\}-0.2\times-1.7\mathrm{e}^{-0.2t}$; "
       r"$\left\{\frac{\mathrm{d}h}{\mathrm{d}t}=\right\}$ awrt 0.153 {metres per year}; changing to awrt 15.3 cm {per "
       r"year}. Note: Substituting $t=4$ into $h=2.3-1.7\mathrm{e}^{-0.2t}$ gives $h=1.536\ldots$ scores M0dM0A0 unless "
       r"differentiation and further correct work is seen separately."],
      False, 24),
    e("11c", "11(c)", EXP, "6.7, 6.1", 1, LATEX["11c"],
      [r"B1 (AO 2.2a): 2.3 (m). Notes: Allow 2.3, 2.3 m, or 230 cm. $2.2\dot{9}$ and $2.2999\ldots$ which clearly continues "
       r"are both acceptable, but 2.29999999 is not."],
      False, 24),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", TRIG, "5.3", 3, LATEX["12a"],
      [r"B1 (AO 1.2): States or uses $\tan x=\frac{\sin x}{\cos x}$. Notes: Allow use of e.g. $\theta$ but the final mark "
       r"requires the equation to be in terms of $x$. States or uses $\tan x=\frac{\sin x}{\cos x}$ e.g., $4\tan x=5\cos x"
       r"\Rightarrow4\frac{\sin x}{\cos x}=5\cos x$ Allow e.g. $\tan x=\frac{\sin\theta}{\cos\theta}$",
       r"M1 (AO 1.1b): $4\sin x=5\cos^2x\Rightarrow4\sin x=5\left(1-\sin^2x\right)$. Notes: Multiplies by $\cos x$ and uses "
       r"$\cos^2x=1-\sin^2x$ to set up a quadratic equation in just $\sin x$. Condone mixed arguments here.",
       r"A1* (AO 2.1): $5\sin^2x+4\sin x-5=0$ *. Notes: Proceeds to $5\sin^2x+4\sin x-5=0$ with correct notation and "
       r"algebra, showing all key steps. The $=0$ must be present in the final answer line. Condone a single slip in "
       r"notation, e.g., $\sin x^2$ or $\sin\theta$ seen once."],
      False, 26),
    e("12b", "12(b)", TRIG, "5.4, 5.3", 4, LATEX["12b"],
      [r"M1 (AO 1.1b): Attempts to solve $5\sin^2x+4\sin x-5=0\Rightarrow\sin x=\ldots$ Notes: Attempts to solve "
       r"$5\sin^2x+4\sin x-5=0\Rightarrow\sin x=\ldots$ using the usual rules. $\sin x=$ may be implied later. Allow "
       r"solution(s) from a calculator but one must be correct (0.6 or 0.7 or –1.4 or –1.5)",
       r"A1 (AO 1.1b): $\sin x=\frac{-2\pm\sqrt{29}}{5}$ ($\sin x=$ awrt 0.677). Notes: Achieves "
       r"$\sin x=\frac{-4\pm\sqrt{116}}{10}$ ($\sin x=$ awrt 0.677) $\sin x=$ may be implied later.",
       r"dM1 (AO 1.1b): Takes $\sin^{-1}$ leading to at least one answer in the range. Notes: Finds one value of $x$ in the "
       r"range 0 to $360^\circ$ from their $\sin x=$ May be scored for working in radians. If using $\sin x=0.677$ they "
       r"should have awrt 0.744 or awrt 2.40. If they have made a slip in solving the quadratic, e.g., by the formula, then "
       r"their values will need checking both in degrees and radians to see if this mark can be implied.",
       r"A1 (AO 1.1b): $x=$ awrt $42.6\{^\circ\}$ and $x=$ awrt $137.4\{^\circ\}$ only. Notes: $x=$ awrt $42.6\{^\circ\}$ and "
       r"$x=$ awrt $137.4\{^\circ\}$ only. Ignore any values outside of 0 to $360^\circ$. isw if they round their values to "
       r"e.g., 3sf after stating acceptable answers. There must be some evidence that the quadratic has been solved."],
      False, 26),
    e("12c", "12(c)", TRIG, "5.4, 5.2", 2, LATEX["12c"],
      [r"B1ft (AO 2.2a): $15\times\text{“}2\text{”}=30$ following through on their “2”. Notes: Follow through on 15 "
       r"multiplied by the number of solutions in (b) in the range 0 to $360^\circ$. If working in radians in (b), they must "
       r"state 30 (solutions).",
       r"B1ft (AO 2.4): Explains either “mathematically” by stating $3\times5\times$ their number in range 0 to $360^\circ$ "
       r"or ‘in words’ e.g., stating $3\times\text{“}2\text{”}$ values every $360^\circ$ and 5 lots of $360^\circ$. Notes: "
       r"Explains either mathematically or in words. See scheme. Note that you might see arguments expanding the range from "
       r"1800 to 5400 to account for the stretch parallel to the $x$ axis. $\frac{5400}{360}=15$ and $15\times2=30$ which is "
       r"also acceptable. Note: If candidates list 30 values and conclude that there are 30 solutions, score B1ftB1ft. "
       r"There is no need to check their 30 values are correct, but there must be 30."],
      False, 26),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", VEC, "9.3", 2, LATEX["13a"],
      [r"M1 (AO 1.1b): $\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}=(-8\mathbf{i}+9\mathbf{j})-"
       r"(10\mathbf{i}-3\mathbf{j})$. Notes: Must be seen in (a). Attempts subtraction either way round. This cannot be "
       r"awarded for adding the two vectors. If no method shown it may be implied by one correct component. Allow as "
       r"coordinates for this mark. Condone missing brackets, e.g., $-8\mathbf{i}+9\mathbf{j}-10\mathbf{i}-3\mathbf{j}$",
       r"A1 (AO 1.1b): $=-18\mathbf{i}+12\mathbf{j}$. Notes: cao $-18\mathbf{i}+12\mathbf{j}$ o.e. "
       r"$\begin{pmatrix}-18\\12\end{pmatrix}$ Condone $\begin{matrix}-18\\12\end{matrix}$. Do not allow "
       r"$\begin{pmatrix}-18\mathbf{i}\\12\mathbf{j}\end{pmatrix}$ or $(-18,12)$ or $\begin{pmatrix}-18\\12\end{pmatrix}$ "
       r"for the A1."],
      False, 30),
    e("13b", "13(b)", VEC, "9.2, 2.2", 2, LATEX["13b"],
      [r"M1 (AO 1.1b): $\left|\overrightarrow{AB}\right|=\sqrt{\text{“}18\text{”}^2+\text{“}12\text{”}^2}"
       r"\left\{=\sqrt{468}\right\}$. Notes: Attempts to use Pythagoras' theorem on their vector from part (a). Allow "
       r"restarts. Note that -18 will commonly be squared as 18. May be implied by awrt 21.6 This will need checking if (a) "
       r"is incorrect.",
       r"A1 (AO 1.1b): $=6\sqrt{13}$. Notes: cao $6\sqrt{13}$ May come from $\begin{pmatrix}\pm18\\\pm12\end{pmatrix}$"],
      False, 30),
    e("13c", "13(c)", VEC, "9.5, 9.3", 3, LATEX["13c"],
      [r"M1 (AO 2.1): For the key step in using the fact that $BCA$ forms a straight line in an attempt to find “$p$” "
       r"$\overrightarrow{AB}=\lambda\overrightarrow{BC}\Rightarrow-18\mathbf{i}+12\mathbf{j}=6\lambda\mathbf{i}+"
       r"\lambda(p-9)\mathbf{j}$ with components equated leading to a value for $\lambda$ and to $p=\ldots$ Notes: For the "
       r"key step in using the fact that $BCA$ forms a straight line in an attempt to find “$p$”. Condone sign slips. "
       r"Award, for example, for $\pm\frac{p-9}{6}=\pm\frac{2}{3}$ leading to $p=\ldots$ It is implied by $p=5$ unless it "
       r"comes directly from work that is clearly incorrect. e.g., award for an attempt to use: "
       r"$\overrightarrow{AB}=\alpha\overrightarrow{AC}\Rightarrow-18\mathbf{i}+12\mathbf{j}=-12\alpha\mathbf{i}+"
       r"\alpha(p+3)\mathbf{j}$ with components equated leading to a value for $\alpha$ and to $p=\ldots$; gradient "
       r"$BC=$ gradient $BA=-\frac{2}{3}$ e.g., $\frac{p-9}{6}=\frac{9--3}{-8-10}$ leading to $p=\ldots$; triangles $BCM$ "
       r"and $BAN$ are similar with lengths in a ratio 1:3. e.g., $p=9-\frac{1}{3}\times12$ or $p=-3+\frac{2}{3}\times12$; "
       r"attempt to find the equation of line $AB$ using both points (FYI line $AB$ has equation "
       r"$y=-\frac{2}{3}x+\frac{11}{3}$) and then sub in $x=-2$ leading to $p=\ldots$; $\frac{p+3}{12}=\frac{2}{3}$ or "
       r"$\frac{p+3}{2}=9-p$ leading to $p=\ldots$",
       r"A1 (AO 1.1b): (i) $p=5$. Notes: $p=5$ Correct answer implies both marks, unless it comes directly from work that "
       r"is clearly incorrect.",
       r"B1 (A1 on EPEN) (AO 2.2a): (ii) ratio $=2:3$. Notes: States ratio $=2:3$ or equivalent such as $1:1.5$ or "
       r"$22:33$. Note that $3:2$ is incorrect but condone {Area}$AOB$ : {Area}$AOC=3:2$. This might follow incorrect work "
       r"or even incorrect $p$. For reference, area $AOC=22$, area $AOB=33$ and area $BOC=11$"],
      False, 30),

    # ---------------- Q14 ----------------
    e("14", "14", SEQ, "4.1", 5, LATEX["14"],
      [r"M1 (AO 3.1a): Attempts the term in $x^3$ or the term in $x^5$ of $\left(3-\frac{1}{2}x\right)^6$. Look for "
       r"${}^6C_3\,3^3\left(-\frac{1}{2}x\right)^3$ or ${}^6C_5\,3^1\left(-\frac{1}{2}x\right)^5$. Notes: For the key step "
       r"in attempting to find one of the required terms in the expansion of $\left(3-\frac{1}{2}x\right)^6$ to enable the "
       r"problem to be solved. Look for ${}^6C_3\,3^3\left(-\frac{1}{2}x\right)^3$ or "
       r"${}^6C_5\,3^1\left(-\frac{1}{2}x\right)^5$ but condone missing brackets and slips in signs. May be part of a "
       r"complete expansion but only one of the required terms needs to be of the correct form.",
       r"A1 (AO 1.1b): Correct term in $x^3$ or correct term in $x^5$ of $\left(3-\frac{1}{2}x\right)^6$: "
       r"$-\frac{135}{2}x^3$ or $-\frac{9}{16}x^5$. Notes: For $-\frac{135}{2}\{x^3\}$ or $-\frac{9}{16}\{x^5\}$ which may "
       r"be unsimplified but the ${}^6C_3$ or ${}^6C_5$ must be processed. May be implied by $-540\{x^5\}$ or "
       r"$-\frac{45}{16}\{x^5\}$",
       r"M1 (AO 1.1b): Attempts one of the required terms in $x^5$ of $\left(5+8x^2\right)\left(3-\frac{1}{2}x\right)^6$: "
       r"Either $5\times{}^6C_5\,3^1\left(-\frac{1}{2}x\right)^5$ or $8x^2\times{}^6C_3\,3^3\left(-\frac{1}{2}x\right)^3$. "
       r"Notes: Look for $5\times{}^6C_5\,3^1\left(-\frac{1}{2}x\right)^5$ or $8x^2\times{}^6C_3\,3^3\left(-\frac{1}{2}x"
       r"\right)^3$ which would also imply the previous M. The $x^5$ may be missing as just the coefficient is required. May "
       r"be implied by $-540\{x^5\}$ or $-\frac{45}{16}\{x^5\}$. Condone missing brackets and signs. You might see "
       r"candidates make a slip in, e.g., their binomial coefficients, but have an (essentially) correct method to solve the "
       r"problem. Note that this M mark is not dependent on the first, so you may be able to award it even if they have "
       r"made a slip in finding their $x^3$ or $x^5$ term in the expansion.",
       r"dM1 (AO 2.1): Attempts the sum of $5\times{}^6C_5\,3^1\left(-\frac{1}{2}x\right)^5$ and $8x^2\times{}^6C_3\,3^3"
       r"\left(-\frac{1}{2}x\right)^3$. Notes: Dependent on the previous M but may be scored at the same time. The $x^5$ may "
       r"be missing as just the coefficients are required. Condone missing brackets and signs.",
       r"A1 (AO 1.1b): Coefficient of $x^5=-\frac{45}{16}-540=-\frac{8685}{16}$. Notes: $-\frac{8685}{16}$ or exact "
       r"equivalent, -542.8125 and apply isw. Condone $-\frac{8685}{16}x^5$ for A1. Note that rounded decimals, e.g., "
       r"-542.81 will not score the last mark. Note that full marks can be scored for concise solutions such as: "
       r"$5\times{}^6C_5\times3\times\left(-\frac{1}{2}\right)^5+8\times{}^6C_3\times3^3\times\left(-\frac{1}{2}\right)^3"
       r"=-\frac{8685}{16}$",
       r"ALT: Alternative (taking out the common factor; score the remaining marks as per the main scheme) — M1 A1: "
       r"$\left(3-\frac{1}{2}x\right)^6=3^6\left\{1+6\times\left(-\frac{1}{6}x\right)+\ldots\right\}$; for M1 A1 look for "
       r"$3^6\times\frac{6\times5\times4}{3!}\left(-\frac{1}{6}x\right)^3$ or $3^6\times\frac{6\times5\times4\times3\times2}"
       r"{5!}\left(-\frac{1}{6}x\right)^5$"],
      False, 34),

    # ---------------- Q15 ----------------
    e("15a", "15(a)", ALG, "2.4", 2, LATEX["15a"],
      [r"M1 (AO 1.1b): Attempts both $y=8-10\times1+6\times1^2-1^3$ and $y=1^2-12\times1+14$. Notes: Must be seen in (a). "
       r"As scheme. For M1 A0, allow a statement that $(1,3)$ lies on both curves without sight of the calculation.",
       r"A1 (AO 1.1b): Achieves $y=3$ for both equations and gives a minimal conclusion / statement, e.g., $(1,3)$ lies on "
       r"both curves so they intersect at $x=1$. Notes: For the complete mathematical argument. Requires both correct "
       r"calculations with a minimal conclusion, which may be as a preamble. e.g., in the alternatives: as "
       r"$1^3-5\times1^2-2\times1+6=0$, hence curves meet when $x=1$; $x^3-5x^2-2x+6=(x-1)\left(x^2-4x-6\right)$ so the "
       r"curves intersect when $x=1$",
       r"ALT: Amongst various alternatives — M1: Setting $x^2-12x+14=8-10x+6x^2-x^3$ and attempting to rearrange to "
       r"$x^3-5x^2-2x+6=0$ before substituting in $x=1$",
       r"ALT: Amongst various alternatives — M1: Setting $x^2-12x+14=8-10x+6x^2-x^3$ and attempting to divide "
       r"$x^3-5x^2-2x+6$ by $(x-1)$ either by long division or inspection"],
      False, 36),
    e("15b", "15(b)", ALG, "2.6, 2.4, 2.3", 5, LATEX["15b"],
      [r"M1 (AO 1.1b): (Curves intersect when) $x^2-12x+14=8-10x+6x^2-x^3\Rightarrow x^3-5x^2-2x+6=0$. Notes: Allow the use "
       r"of $x$ or $k$ throughout this part. Sets $x^2-12x+14=8-10x+6x^2-x^3$ and proceeds to a cubic equation set $=0$. "
       r"Must be seen or used in (b)",
       r"dM1 (AO 3.1a): For the key step in dividing by $(x-1)$: $x^3-5x^2-2x+6=(x-1)\left(x^2+px\pm6\right)$. Notes: For "
       r"the key step in realising that $(x-1)$ is a factor of the cubic. It is for dividing by $(x-1)$ to get the quadratic "
       r"factor. For division look for their first two terms, i.e., $x^2\pm4x$ (This will need checking if they have made "
       r"an error in rearranging the cubic.) By inspection look for the first and last term "
       r"$x^3-5x^2-2x+6=(x-1)\left(x^2+px\pm6\right)$",
       r"A1 (AO 1.1b): $x^3-5x^2-2x+6=(x-1)\left(x^2-4x-6\right)$. Notes: $x^3-5x^2-2x+6=(x-1)\left(x^2-4x-6\right)$ or just "
       r"$x^2-4x-6$ or $k^2-4k-6$ as their quadratic factor following algebraic division.",
       r"ddM1 (AO 1.1b): Solves $x^2-4x-6=0$: $(x-2)^2=10\Rightarrow x=\ldots$ Notes: Attempts to solve their "
       r"$x^2-4x-6=0$, which must be a 3TQ, by completing the square or the quadratic formula, leading to an exact solution. "
       r"Their quadratic factor must not factorise. Their quadratic “factor” may come from algebraic division that has a "
       r"remainder but we will still allow them to score this mark. If using the quadratic formula, they need to have, "
       r"e.g., $\frac{4-\sqrt{4^2-4(-6)}}{2}$ or $\frac{4-\sqrt{40}}{2}$ as a minimum (i.e., they must not jump straight to "
       r"$2-\sqrt{10}$ from a calculator).",
       r"A1 (AO 1.1b): $x=2-\sqrt{10}$ only. Notes: $k=2-\sqrt{10}$ or exact equivalent but allow the use of $x$ e.g., "
       r"$x=\frac{4-\sqrt{40}}{2}$. If using the quadratic formula, the discriminant must be processed. Must come from a "
       r"correct quadratic factor. They must have discarded $2+\sqrt{10}$ if seen."],
      False, 36),

    # ---------------- Q16 ----------------
    e("16", "16", INT, "8.2, 7.3", 6, LATEX["16"],
      [r"M1 (AO 2.1): Sets $\mathrm{f}'(4)=0\Rightarrow16+2a+b=0$. Notes: For the key step in setting "
       r"$\mathrm{f}'(4)=0\Rightarrow16+2a+b=0$ to set up an equation in $a$ and $b$. Condone slips.",
       r"M1 (AO 1.1b): Integrates $\mathrm{f}'(x)=4x+a\sqrt{x}+b\Rightarrow\{\mathrm{f}(x)=\}2x^2+\frac{2}{3}ax^{\frac{3}{2}}"
       r"+bx\,\{+c\}$. Notes: For attempting to integrate $\mathrm{f}'(x)$. Award for $x^n\to x^{n+1}$ or $b\to bx$. This "
       r"may come after finding values for $a$ or $b$ or both.",
       r"A1ft (AO 1.1b): $\{\mathrm{f}(x)=\}2x^2+\frac{2}{3}ax^{\frac{3}{2}}+bx\,\{+c\}$. Notes: "
       r"$\{\mathrm{f}(x)=\}2x^2+\frac{2}{3}ax^{\frac{3}{2}}+bx\,\{+c\}$ or, e.g., $\{\mathrm{f}(x)=\}2x^2+\frac{2}{3}"
       r"ax^{\frac{3}{2}}+(-16-2a)x\,\{+c\}$. Allow ft on their $b$ in terms of $a$ if they substituted in from their "
       r"$\mathrm{f}'(4)=0\Rightarrow16+2a+b=0$. Do not ft if they have a value(s) for $a$ or $b$. This may be left "
       r"unsimplified but the indices must be processed. isw once the mark is awarded. Condone the omission of the $+c$. "
       r"This accuracy mark requires only the previous M mark to be scored.",
       r"B1 (AO 2.2a): Deduces that $c=-5$. Notes: Deduces that the constant term in $\mathrm{f}(x)$ is $-5$. Note that "
       r"deducing $b=-5$ is B0. It must be the constant in a changed function.",
       r"ddM1 (AO 3.1a): Full and complete method using the given information $\mathrm{f}'(4)=0$ and $\mathrm{f}(4)=3$ in "
       r"order to find values for $a$ and $b$. Note: $a=-15$ and $b=14$. Notes: For a complete strategy to find values for "
       r"both $a$ and $b$. Do not be concerned about the logistics of how they solve the simultaneous equations – this may "
       r"be done on a calculator. Note: $a=-15$ and $b=14$. This is dependent on both previous method marks and so must "
       r"include use of both: $\mathrm{f}'(4)=0$ (their $16+2a+b=0$ o.e.); $\mathrm{f}(4)=3$ (their "
       r"$32+\frac{16}{3}a+4b-5=3$ o.e.)",
       r"A1 (AO 1.1b): $\{\mathrm{f}(x)=\}2x^2-10x^{\frac{3}{2}}+14x-5$. Notes: "
       r"$\{\mathrm{f}(x)=\}2x^2-10x^{\frac{3}{2}}+14x-5$ or exact simplified equivalent, e.g., use of $x\sqrt{x}$ in place "
       r"of $x^{\frac{3}{2}}$. Apply isw once a correct expression is seen."],
      False, 40),

    # ---------------- Q17 ----------------
    e("17a", "17(a)", PROOF, "1.1", 1, LATEX["17a"],
      [r"B1 (AO 2.4): Provides a counter example with a reason. e.g., $6^3-1^3=215$ which is a multiple of 5. Notes: "
       r"Provides a counter example with a reason. There is no need to state “not true”. e.g., $7^3-2^3=335$ which divides "
       r"by 5 {exactly}. It is sufficient to have, e.g., $9^3-4^3=665$ and $\frac{665}{5}=133$. Here $q$ must be greater "
       r"than $p$ and both must be natural numbers, not 0 or negatives. Note that any pair of positive integers $n$ and "
       r"$n+5k$ will provide a counter example, but $q^3-p^3$ must be evaluated correctly, and if they divide by 5 this also "
       r"needs to be correct."],
      False, 42),
    e("17b", "17(b)", PROOF, "1.1, 2.6", 4, LATEX["17b"],
      [r"M1 (AO 2.1): States or uses, e.g., $2n$ and $2n+2$ or $2n+2$ and $2n+4$. Notes: For the key step in stating the "
       r"algebraic form of consecutive even numbers. See main scheme for examples. They might be used either way round for "
       r"this mark.",
       r"dM1 (AO 1.1b): Attempts $(2n+2)^3-(2n)^3=8n^3+24n^2+24n+8-8n^3$ leading to a quadratic. Notes: Attempts "
       r"$(2n+2)^3-(2n)^3=\ldots$ condoning slips but must lead to a quadratic. Alternatively, "
       r"$(2n+2)^3-(2n)^3=2^3\left\{(n+1)^3-n^3\right\}$. May be subtracted the wrong way round for this mark as below. "
       r"$(2n)^3-(2n+2)^3=\ldots$ but this will score M1dM1A0A0",
       r"A1 (AO 1.1b): $=24n^2+24n+8$. Notes: e.g., $(2n+2)^3-(2n)^3=24n^2+24n+8$ or $(2n+4)^3-(2n+2)^3=24n^2+72n+56$ or "
       r"$(2n+2)^3-(2n)^3=8\left\{(n+1)^3-n^3\right\}$ or $(2n)^3-(2n-2)^3=24n^2-24n+8$ etc. Must come from correct work and "
       r"the algebra will need checking carefully.",
       r"A1 (AO 2.1): $24n^2+24n+8=8\left(3n^2+3n+1\right)$ So $q^3-p^3$ is a multiple of 8. Notes: For a full and rigorous "
       r"proof showing all necessary steps including: correct quadratic expression for $q^3-p^3$ for their even numbers, "
       r"e.g., $24n^2+24n+8$; reason e.g., $24n^2+24n+8=8\left(3n^2+3n+1\right)$ or, e.g., in $24n^2+24n+8$ the "
       r"coefficients are all multiples of 8; minimal conclusion, “hence true”",
       r"ALT: Alt 1 (if the even numbers are set as $n$ and $n+2$ there must be sufficient work seen before marks can be "
       r"awarded) — M1dM1: e.g., $n=2k\Rightarrow(n+2)^3-n^3=\ldots n^2+\ldots n+\ldots=\ldots(2k)^2+\ldots(2k)+\ldots$",
       r"ALT: Alt 1 — A1: $=24k^2+24k+8$",
       r"ALT: Alt 1 — A1: $=8\left(3k^2+3k+1\right)$ so $q^3-p^3$ is a multiple of 8",
       r"ALT: Alt 2 (if they just use any two even numbers, e.g., $2a$ and $2b$, or $2m$ and $2n+2$) — M1: $(2a)^3-(2b)^3$ "
       r"Condone missing brackets if recovered.",
       r"ALT: Alt 2 — dM1: $=\ldots a^3-\ldots b^3$",
       r"ALT: Alt 2 — A1: $=8a^3-8b^3$ Note $8\left(a^3-b^3\right)$ would imply this mark.",
       r"ALT: Alt 2 — A1: $=8\left(a^3-b^3\right)$ so $q^3-p^3$ is a multiple of 8 if $q$ and $p$ are {any two} even "
       r"{numbers} and hence $q^3-p^3$ is a multiple of 8 if $q$ and $p$ are consecutive even numbers"],
      False, 42),
]

# Examiner report, sentence by sentence, in report order (the General Comments
# introduction is not attached to any question). A sentence that mentions
# another part only in passing is tagged with the part it is about.
W = None
NO = {"ref": False}
BACK = {"ref": True}
DY = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
REPORT = {
    "01": [
        (W, "This question was a friendly and well-attempted start to the paper.", NO),
        (W, "Most candidates were able to score a high proportion of the marks available here."),
        ({"a"}, "In part (a), most candidates scored both marks for a correct differentiation."),
        ({"a"}, "Occasionally a persisting ‘$+5$’ or an introduced ‘$+c$’ led to the loss of a mark here."),
        ({"a"}, "The most common error, however, arose in the coefficients of $x^2$ or $x$: with the fractional "
                "coefficients causing something of a challenge to some candidates."),
        ({"a"}, "It was rare that attempts to integrate were seen.", NO),
        ({"b"}, r"In part (b), a significant minority of candidates were unclear on the correct way to identify the correct "
                r"critical values and, as a result, some attempted to solve $\frac{\mathrm{d}^2y}{\mathrm{d}x^2}=0$ in "
                r"pursuit of a ‘critical value’."),
        ({"b"}, "Perhaps because the question had asked where $y$ was decreasing, an occasional misconception led "
                f"candidates to find $y$ values corresponding to the $x$ values resulting from ${DY}=0$ followed by an "
                "attempt to use these $y$ coordinates to define a range rather than using the values of $x$.", NO),
        ({"b"}, f"Nonetheless, most candidates recognised the need to set ${DY}=0$ to find the turning points of the curve "
                "and most were able to solve the three-term-quadratic set equal to zero."),
        ({"b"}, "Commonly, the use of calculators was apparent."),
        ({"b"}, "But many others took an algebraic approach with sometimes mixed results."),
        ({"b"}, "Factorisation was the most successful of these, with errors mainly occurring with the signs within the "
                "linear factors.", BACK),
        ({"b"}, "The quadratic formula was sometimes inaccurately applied and omissions of the – sign in front of ‘$b$’ in "
                "the numerator, or the use of ‘$2ac$’ in the denominator, caused issues and the resulting loss of the M "
                "mark."),
        ({"b"}, "Completing the square was seen but it seemed to be a fairly unreliable approach for the candidates that "
                "chose to use it.", NO),
        ({"b"}, "A significant minority of candidates did not write down their critical values clearly, instead "
                f"confining them to being labelled only on a graph of the ${DY}$ curve."),
        ({"b"}, "A significant number of candidates who had found critical values appeared to believe that stating them "
                "was sufficient to define the required range, or perhaps they were unable to make further progress in "
                "stating the range and so stopped short by simply stating the two values of $x$."),
        ({"b"}, "Those candidates who did realise, however, that an interval needed more careful definition, usually did "
                "so correctly.", NO),
        ({"b"}, "This was most often achieved using standard inequality notation.", BACK),
        ({"b"}, "The most successful candidates were those who drew a sketch of the quadratic to accompany their "
                r"determination of the range for $x$, but some candidates determined "
                r"$\frac{\mathrm{d}^2y}{\mathrm{d}x^2}$ as a means to identifying the correct region.", NO),
        ({"b"}, r"A minority of candidates lost a mark for inconsistent use of inequalities by mixing, for example, $<$ "
                r"and $\leqslant$ in their statement of the range."),
        ({"b"}, r"Only a relatively small proportion of candidates defined the outside region; a small number of whom "
                r"wrote non-sensical inequalities such as $-\frac{1}{2}>x>4$.", NO),
        ({"b"}, r"Answers such as $x<-\frac{1}{2},x<4$ were also not uncommon.", NO),
        ({"b"}, "The use of set notation tended to be more problematic for those that used it as there was sometimes "
                "some confusion between the union and the intersection symbols.", NO),
    ],
    "02": [
        (W, "This question was generally not particularly well answered, especially as it appeared early in the paper, "
            "with the majority scoring two or fewer marks out of the available four marks.", NO),
        (W, "The majority of candidates identified that a quadratic equation needed to be solved to progress, although "
            "some struggled to reach a suitable equation."),
        (W, "It was notable that significant proportion of candidates ignored the question’s requirement to show all "
            "stages of their work, directly solving their quadratic in $u$ with their calculator.", NO),
        (W, "They immediately, therefore, forfeited the first two marks which required candidates to demonstrate that "
            "they can solve a quadratic without reliance on a calculator."),
        (W, "Those who did show their method and attempted to factorise, generally did so successfully and reached "
            "solutions in terms of $u$.", NO),
        (W, "Another common error, however, was then to forget to square their values of $u$ so they did not reach "
            "values of $x$."),
        (W, r"Furthermore, candidates very often also did not reject the invalid $x=\frac{25}{4}$, which resulted from "
            r"$\sqrt{x}=-\frac{5}{2}$, so that the majority of candidates did not score the final mark."),
        (W, "While factorising was by far the most common approach to solve the quadratic, other approaches included use "
            "of completing the square or the quadratic formula, and a very few squared the original equation and "
            "attempted to solve $36x^2-289x+400=0$."),
    ],
    "03": [
        ({"a"}, "Part (a) of this question required the use of the cosine rule in combinations with bearings."),
        ({"a"}, "The vast majority of candidates recognised the need to use the cosine rule, but were unsuccessful in "
                "labelling their diagram correctly, usually labelling the 72 or the 39 in the wrong place."),
        ({"a"}, "This resulted in an incorrect attempt at applying the cosine rule and limited them to the method mark in "
                "part (a).", BACK),
        ({"a"}, "A small proportion of candidates attempted to use the sine rule or Pythagoras, which were ultimately "
                "invalid approaches, but a further small proportion attempted this part using a vector approach with a "
                "good success rate."),
        ({"b"}, "Part (b) was generally well answered, with the most common, concise, explanation referring to it being "
                "unlikely that the engineer would be able to travel in a perfect straight line (either because of "
                "obstacles or because the road would not be straight).", NO),
        ({"b"}, "Other successful responses included challenging the assumption that the base of the masts was on the "
                "same horizontal plane."),
        ({"b"}, "For those who did not score the mark, it was often because they were talking about the numbers being "
                "rounded or the bearings being inexact.", NO),
        ({"b"}, "Some candidates focused on speed and having to stop, i.e., referring to time rather than distance and "
                "appeared to misunderstand the requirement of the question."),
    ],
    "04": [
        ({"a"}, "In part (a), most candidates appeared to know what the reciprocal graph should look like, and the "
                "majority positioned it in the correct quadrants.", NO),
        ({"a"}, "There were a few, though in the minority, who only sketched the section of the graph in the first "
                "quadrant."),
        ({"a"}, "Some candidates actually worked out values and plotted the graph."),
        ({"a"}, "Often the two asymptotes appeared to be quite adrift of the two axes and occasionally the ends of the "
                "curves drifted away from the axes, but it was usually apparent what the candidate’s intention was.", NO),
        ({"a"}, "There were many candidates who ignored the blank space and sketched their graphs on the lined page."),
        ({"b"}, "In part (b), most candidates only scored 1 mark out of 3 as they did not consider the section of the "
                "graph where $x$ was negative."),
        ({"b"}, r"Those who sketched the line $y=2$ on the graph were far more likely to identify the region $x<0$, "
                r"although this was often given as $x\leqslant0$ despite the curve being undefined at $x=0$.", NO),
        ({"b"}, "As such, fully correct answers were few and far between.", BACK),
    ],
    "05": [
        (W, r"Most candidates recognised the need and were able to solve the equation $4x^2+3=23$ to determine the upper "
            r"limit, $x=\sqrt{5}$, although some candidates did not use the diagram to discard the $x=-\sqrt{5}$ and ended "
            r"up integrating between the incorrect limits."),
        (W, "It was also very common to see the limits 3 and 23 being used, with these candidates unclear about the area "
            "that is found through an integration strategy.", NO),
        (W, r"The most successful strategy for finding the area under the curve was through finding "
            r"$\int_0^{\sqrt{5}}(4x^2+3)\,\mathrm{d}x$ and then subtracting that from the area of the rectangle."),
        (W, r"However, there were plenty of candidates that failed to subtract the area under the curve "
            r"$\frac{29\sqrt{5}}{3}$ from the rectangle, and these candidates generally scored 3 marks out of 5.", NO),
        (W, r"Those candidates that elected to find the difference between the curve function and the line $y=23$ and "
            r"then integrated their expression were more likely to have slips in their working: some failed to subtract "
            r"correctly, resulting in $\int_0^{\sqrt{5}}(23-4x^2+3)\,\mathrm{d}x$; while others subtracted the wrong way "
            r"round, leading to a negative answer that some failed to recover to a positive answer.", NO),
        (W, "However, in both cases, once the integrand was determined, the majority of candidates using this strategy "
            "were able to achieve method mark for being able to perform integration of at least a term in the "
            "integrand.", BACK),
        (W, "There were very few candidates that tried to integrate the function bounded by the $y$-axis and those that "
            "did were generally unsuccessful: often their rearrangement to make $x$ the subject was poorly done and in "
            "these cases they often lacked the experience of Year 2 integration to be able to integrate function of the "
            "form $(ax+b)^n$, where $n$ is a fraction.", NO),
    ],
    "06": [
        ({"a"}, "Part (a) of this question was well answered as candidates appeared to be able to complete the square to "
                "determine the coordinates of the centre as being $(3,-5)$."),
        ({"b"}, "However, part (b) appeared to be inaccessible to the majority of candidates as they failed to interpret "
                "and/or apply the information given in the question."),
        ({"b"}, "The majority failed to determine the lower limit of $k$, $k>9$, which arose from the requirement that "
                "the circle did not touch the $x$-axis."),
        ({"b"}, "Here, the most common mistake was in assuming the circle must not touch the $x$-axis, resulting in "
                "$k>25$.", {"note": "the mark scheme's answer is $9<k<34$, so the $x$-axis condition gives $k>9$"}),
        ({"b"}, "Some candidates approached this part of the question by substituting the coordinates of their centre "
                "and then using the discriminant involving $k$, while those who drew a decent sketch used the far simpler "
                "geometric approach and arrived at the result in a far more concise fashion.", NO),
        ({"b"}, r"In contrast, a good number were able to determine the upper limit of $k$, $k\leqslant34$."),
        ({"b"}, "However, a good number of candidates did not attempt this part of the question, illustrating the "
                "candidates’ struggle with circle geometry and that, for many centres, it would be worth investing more "
                "time into developing deeper understanding of the various types of problems that can arise in circle "
                "geometry.", NO),
    ],
    "07": [
        (W, "Most candidates attempted this question, with only a small number leaving it blank.", NO),
        ({"c"}, "Most candidates achieved at least one mark overall, but few candidates achieved full marks due to part "
                "(c)."),
        ({"a"}, "In part (a), candidates who set up a linear model correctly tended to go on to get the correct linear "
                "model required and performed well in the rest of the question."),
        ({"a"}, "Those who were successful tended to use the gradient and $y-y_1=m(x-x_1)$ rather than attempting to use "
                "simultaneous equations.", NO),
        ({"a"}, r"The most common error was to use the coordinates the wrong way round, which resulted in candidates’ "
                r"incorrectly calculating the gradient as $-8$ instead of $-\frac{1}{8}$."),
        ({"a"}, "However, a good proportion of candidates recovered by using the gradient of $-8$ to achieve a formula in "
                "terms of $V$ (i.e., $d=400-8V$ or equivalent)."),
        ({"a"}, "There were a few candidates who did not include the ‘$+c$’ part of a linear model and instead seem to "
                "think the relationship was proportional."),
        ({"a"}, "These candidates were often limited to one mark in this question for correctly identifying the link of "
                "1 litre = 8km.", BACK),
        ({"a"}, "Where a linear equation was not recognised an exponential was the most common alternative."),
        ({"b"}, "Candidates who achieved a formula in part (a) generally continued onto part (b) and used their formula "
                "to attempt the question correctly."),
        ({"b"}, "A common error was to omit the units, which cost just the final mark in part (b)."),
        ({"b"}, "Of the candidates who had $V$ and $d$ the wrong way round in their linear model, none seemed to realise "
                "that their answers of 400L and 50km were unrealistic."),
        ({"b"}, "In part b(ii) a small number of candidates used their answer to part (i) 50 as the new value for $V$, "
                "rather than set $V=0$ and rearrange."),
        ({"c"}, "Very few candidates achieved the mark for part (c)."),
        ({"c"}, "Most candidates recognised it was not acceptable but failed to comment on the significance of the "
                "difference.", NO),
        ({"c"}, "Centres must be clear with candidates that models do not have to be perfect to be appropriate, and so "
                "it is only if the model is significantly out that it becomes unviable to use.", NO),
        ({"c"}, "A small number of candidates calculated percentage difference, which was acceptable."),
        ({"c"}, "Some candidates focussed incorrectly on practical reasons (e.g., different routes, fuel consumption, "
                "more accelerating and breaking, etc.)."),
        ({"c"}, "A small number of candidates worked out the remaining fuel (10L) but often did not correctly conclude "
                "the significance of this amount.", NO),
    ],
    "08": [
        (W, "Very few candidates achieved full marks on this question."),
        (W, "The vast majority of candidates were able to find the linear equation successfully, with a significant "
            "proportion making no further attempt at the question."),
        (W, "While the majority did recognise the form of the quadratic equation using the two $x$-intercepts, most "
            "simply stated $y=x^2-6x$ or equivalent and did not use the coordinates on the graph to find the coefficient "
            "of the $x^2$ term."),
        (W, "There were a lot of candidates who did not understand what the final part of the question required as they "
            "were trying to find intercepts (often assuming that the region needs to be defined as $-3<x<10$) or find "
            "the area between the curves."),
        (W, "Very few candidates seemed to understand what the regions were and how to use the inequalities to determine "
            "the region."),
        (W, "Incorrect use of notation was also seen here with $R$ used instead of $y$ linking the two equations."),
    ],
    "09": [
        (W, "This question was an effective discriminator between candidates."),
        (W, "There was evidence of log misconceptions in a substantial proportion of candidates’ work and there were a "
            "number of completely blank scripts seen."),
        (W, "Often though, even weaker candidates were able to pick up the first mark for evidence of a log law correctly "
            "applied, albeit amidst otherwise erroneous work which limited them to the first mark only."),
        (W, r"Most commonly this was earned in isolation either for use of the power law "
            r"$2\log_5(3x-2)\to\log_5(3x-2)^2$ or for $2\to5^2$ when both sides of the equation were raised to base 5 in "
            r"an attempt to remove logs.", BACK),
        (W, "It was not uncommon, however, to see the right-hand side become $2^5$ rather than $5^2$.", NO),
        (W, r"Another common error involved a misapplication of the log law for subtraction whereby $\log A-\log B$ was "
            r"believed to be equal to $\frac{\log A}{\log B}$ with the log terms on numerator and denominator subsequently "
            r"‘cancelled’."),
        (W, "In contrast, however, there were a large number of candidates who were well-prepared for this question and "
            "were able to demonstrate clear understanding and apply their log knowledge accurately to gain the first "
            "three marks."),
        (W, "Following a successful removal of logs, most were able to rearrange their equation into a solvable form and "
            "gain the final method mark for solving the resulting quadratic equation."),
        (W, r"There was a surprising proportion of candidates who chose to attempt to simplify the algebraic fraction "
            r"$\frac{9x^2-12x+4}{x}$, often correctly, to $9x-12+\frac{4}{x}$."),
        (W, "Of these, a good proportion managed to recover, but many candidates simply used an equation solver on their "
            "calculator to arrive at the two solutions, and thus forfeited the final two marks.", BACK),
        (W, "Similar errors to those observed in question 1 were also apparent here in the solving of a quadratic "
            "equation and factorisation proved again to be the most successful algebraic method.", NO),
        (W, r"The final mark was a particularly good discriminator as only a minority of stronger candidates checked the "
            r"viability of each root in the original equation and so most candidates failed to reject the "
            r"$x=\frac{1}{9}$ root."),
        (W, r"It was again disappointing to see the number of attempts that jumped straight to $x=\frac{1}{9}$ without "
            r"showing sufficient log work to achieve an equation without logs.", NO),
        (W, "Candidates must be clear that using calculators to solve equations must be treated with caution and that "
            "they risk losing a substantial number of marks."),
    ],
    "10": [
        (W, "This question on straight-line coordinate geometry was well attempted by the vast majority of candidates and "
            "there was a good proportion of candidates scoring full marks."),
        ({"a"}, "This “show that” question in part (a) was generally very well done, with clear work to find the "
                "negative reciprocal gradient and then form a correct equation.", NO),
        ({"a"}, "The majority were able to manipulate this to the given form without errors, but the occasional slip in "
                "their processing resulted in the loss of the final accuracy mark.", BACK),
        ({"a"}, "Those who took the alternative approach, which was essentially a verification process, candidates "
                "generally showed that the given line was perpendicular to the original line but very few verified that "
                "it went through the required point and hence only scored 1 mark out of 3.", NO),
        ({"b"}, "Part (b) was also very well attempted, with the vast majority of candidates obtaining the correct "
                "coordinates for $A$ and $C$."),
        ({"b"}, "However, many failed to recognise that the base of the triangle was 18 and the height was simply the $y$ "
                "coordinate of $C$ and instead focused on the fact that $AC$ and $BC$ were perpendicular and used "
                "Pythagoras to find the lengths of $AC$ and $BC$."),
        ({"b"}, "Sometimes they lost the accuracy with this rather laborious method by using decimal answers, although "
                "some very accurate candidates were able to proceed using this method to the exact answer.", BACK),
        ({"b"}, "Quite often candidates only obtained the $x$ coordinate of $C$ and were thus unable to proceed further."),
        ({"b"}, "Very few attempts were seen that used discriminant approaches to find the required area.",
         {"note": "the mark scheme's alternative uses determinants"}),
    ],
    "11": [
        ({"b"}, "This question on exponential functions caused problems for the majority in part (b), as they failed to "
                "recognise that differentiation was required."),
        ({"a", "c"}, "However, generally parts (a) and (c) were answered well."),
        ({"a"}, r"In part (a), most candidates identified that they needed to substitute $t=0$ into the given equation and "
                r"successfully reached $h=0.6$ metres, which was often seen as 60cm or $\frac{3}{5}$, both of which were "
                r"allowed."),
        ({"a"}, r"A few failed to use $\mathrm{e}^0=1$ and as a result arrived at an incorrect answer."),
        ({"b"}, "In part (b), the majority of candidates failed to recognise that the 15.3 cm per year meant that they "
                "were required to differentiate to obtain a rate of change, and attempted instead to substitute $t=4$ "
                "into the expression for $h$."),
        ({"b"}, "This answer resembled 15.3 cm, so many incorrectly assumed that they had answered the question, even "
                "though the subsequent conversion from metres to cm made no sense.", BACK),
        ({"b"}, "Some attempted to divide this value by 4, showing some appreciation for the units given in the "
                "question, but lacking an appreciation that the information given provided an instantaneous rate of "
                "change and not an average rate over the four years.", BACK),
        ({"b"}, "Without an attempt at differentiation no marks could be scored in (b) but those candidates who did "
                "differentiate generally successfully answered this part of the question.", NO),
        ({"c"}, "In part (c), most candidates identified that the limiting value was 2.3 m, although a number missed this "
                "part out, especially after a poor attempt at part (b)."),
    ],
    "12": [
        (W, "This question involving the use of trigonometric identities and solving a trigonometric equation was "
            "generally very well answered with the exception of part (c)."),
        (W, "There were very few blank scripts."),
        ({"a"}, "Part (a) was generally well answered."),
        ({"a"}, r"The majority of candidates scored the first mark for correctly identifying "
                r"$\tan x=\frac{\sin x}{\cos x}$."),
        ({"a"}, r"Two common errors were to either use $\sin x=1-\cos x$, or to include the number 4 in the denominator "
                r"$\left(\text{i.e., }4\tan x=\frac{4\sin x}{4\cos x}\right)$."),
        ({"a"}, r"Some candidates made errors in their notation (which was only penalised if it occurred more than once) "
                r"with a few using $\sin x^2$.", NO),
        ({"a"}, "A small number started with the answer to try to work backwards, but this approach rarely scored full "
                "marks."),
        ({"b"}, "Part (b) was attempted by the majority of candidates with some good success."),
        ({"b"}, "Calculators will solve this equation directly, and as a result there were some candidates (although a "
                "minority) who were unable to work out the correct answer using a clear written method combining the "
                "quadratic formula and using the inverse sine function.", NO),
        ({"b"}, "As mentioned earlier, candidates must be careful to show sufficient working."),
        ({"b"}, "However, most candidates were able to solve the equation and find at least one value of $x$ (usually "
                "awrt 42.6)."),
        ({"b"}, "Generally, where candidates understood the requirements of the question, both angles were found to the "
                "required accuracy."),
        ({"b"}, "Some candidates stated additional incorrect answers inside the given range and so lost the final "
                "accuracy mark."),
        ({"b"}, "It was surprisingly common to see candidates rounding their values from the quadratic equation (i.e., to "
                "0.7) which resulted in inaccurate angles and as a result they lost the final accuracy mark.", NO),
        ({"c"}, "Part (c) was much less successful, with only a small number of candidates gaining any marks."),
        ({"c"}, "Most candidates only identified one of the adaptations to the question: either the stretch or the "
                "increase in the range."),
        ({"c"}, "The most common incorrect answer resulted from them multiplying their number of solutions by 5 to "
                "achieve a total of 10 solutions."),
        ({"c"}, "Of those candidates who realised there were 30 solutions nearly all were able to give a satisfactory "
                "explanation.", NO),
    ],
    "13": [
        ({"a", "b", "c"}, "Given that candidates often find vector problems quite challenging, this question proved to "
                          "be quite accessible, and most candidates made good progress through parts (a) and (b) of this "
                          "question, with part (c) more mixed."),
        ({"a"}, r"In part (a), most candidates successfully reached $-18\mathbf{i}+12\mathbf{j}$ although a few subtracted "
                r"the vectors the wrong way round or added the position vectors of $A$ and $B$ instead."),
        ({"b"}, r"Most were then able to calculate $|AB|$ in (b) using their answer from (a), and many correctly reached "
                r"$6\sqrt{13}$, which was allowed even if candidates had achieved an incorrect vector in (a), e.g., "
                r"$18\mathbf{i}+12\mathbf{j}$"),
        ({"c"}, "Attempted methods in (c)(i) were many and varied but most did not use vectors."),
        ({"c"}, "The most common method was to establish the equation of the straight line through $A$ and $B$, and this "
                "was then used with $x=-2$ to find $p=5$.", NO),
        ({"c"}, r"Other methods simply looked logically at the information given and found the appropriate scaling factor "
                r"between, for example, the vectors $\overrightarrow{AB}$ and $\overrightarrow{BC}$."),
        ({"c"}, "Methods like this were often poorly written down but were clearly correct and gained full marks.", BACK),
        ({"c"}, "Many candidates did not successfully reach $p=5$."),
        ({"c"}, r"Typical errors in (c)(i) were assuming $\overrightarrow{AB}=\overrightarrow{BC}$, setting the sum of the "
                r"position vectors of $A$, $B$ and $C$ equal to zero or assuming that "
                r"$-18\mathbf{i}+12\mathbf{j}=k(-2\mathbf{i}+p\mathbf{j})$."),
        ({"c"}, "A significant number of candidates omitted (c)(ii) after an unsuccessful attempt at (c)(i), and when "
                "responses were seen they were often lengthy and involved unnecessary attempts at calculating the areas "
                "of the triangles $AOC$ and $AOB$."),
        ({"c"}, "A common incorrect answer was $4:9$, reached after assuming incorrectly that the two triangles were "
                "similar."),
        ({"c"}, "Some candidates did, however, successfully reach a ratio of $2:3$ either after area calculations, or by, "
                "for example, examining the relative lengths of $AB$ and $AC$."),
        ({"c"}, "Part (ii) did not rely on an answer to part (i) and so a reasonable number of candidates scored the final "
                "mark having been unable to find $p$, with some doing so very concisely."),
        ({"c"}, "It was notable that many of the concise solutions to both parts came from a simple, well-constructed and "
                "clear diagram.", NO),
    ],
    "14": [
        (W, r"This question required candidates to isolate the required terms from the binomial expansion of "
            r"$\left(3-\frac{1}{2}x\right)^6$ and is a reasonably familiar question from previous papers, but this was "
            r"less structured to those that candidates have seen before.", NO),
        (W, r"Many candidates elected to attempt the first few terms of the binomial expansion of "
            r"$\left(3-\frac{1}{2}x\right)^6$ despite there being no requirement to do so, probably due to it being the "
            r"most common first step of these questions.", NO),
        (W, r"For those that took this approach, most candidates managed to begin the expansion correctly, but there were "
            r"a lot of instances where the brackets were missing around $-\frac{1}{2}$.", NO),
        (W, "Often this was recovered and either one or both of the required terms were found correctly.", BACK),
        (W, "A significant proportion of the candidates who got so far progressed either to multiply the $x^5$ term by 5 "
            "and/or the $x^3$ term by 8 and gained the second method mark, but often only one of the two required terms "
            "were found, scoring a maximum of 3 out of 5."),
        (W, "Many candidates who achieved a ‘correct’ answer had left in the $x^5$ and were only able to achieve full "
            "marks because the mark scheme condoned this.", NO),
        (W, "Candidates in future series must ensure that they fulfil the demand of the question and select the "
            "coefficient required."),
        (W, "There were, however, a pleasing number of concise solutions in which candidates decided which terms were "
            "needed at the outset and elected only to find those that were required.", NO),
        (W, "These were often fully correct.", BACK),
    ],
    "15": [
        (W, "This question began with the familiar calculator warning which was unfortunately ignored by a significant "
            "proportion of candidates."),
        (W, "As mentioned previously, candidates must be clear on what is allowed when these warnings are stated, or they "
            "risk losing a number or marks.", NO),
        ({"a"}, "In part (a), the majority of the candidates were able to gain the first mark by either substituting 1 "
                "into the two equations separately (and almost always achieving $y=3$ in both cases) or by setting the "
                "two equations equal to each other and then substituting in 1 as required."),
        ({"a"}, "The majority of candidates, having achieved the point of intersection, drew the correct conclusion but "
                "there were many candidates who did not make any suitable comment."),
        ({"b"}, "In part (b), the vast majority of candidates achieved the cubic equation required by equating the two "
                "given equations and rearranging to set equal to 0, but a significant proportion ignored the guidance at "
                "the top of the question and proceeded to solve the question directly on their calculator, resulting in a "
                "maximum mark of 1 out of 5."),
        ({"b"}, "For those that proceeded further, many used inspection to factorise the cubic using the given factor "
                "$(x-1)$, while others attempted algebraic division, generally very successfully, achieving the correct "
                "quadratic $x^2-4x-6$.", NO),
        ({"b"}, "Occasionally, the rearrangements that candidates used resulted in a negative cubic, but despite making "
                "the division more challenging it was pleasing that candidates were still generally able to complete "
                "this part successfully.", NO),
        ({"b"}, "However, having arrived at a suitable quadratic, another significant proportion relied on their "
                "calculator to solve the resulting equation (set equal to 0) and forfeited the final two marks."),
        ({"b"}, r"For those that showed full working, many assumed that $k>0$ and chose the incorrect solution, despite "
                r"often writing $k<0$ as their justification for rejecting (the correct) $2-\sqrt{10}$.", NO),
        ({"b"}, "As a result, there were very few candidates who achieved full marks for this question."),
    ],
    "16": [
        (W, "Generally, the candidates that made a full attempt at this question did very well by achieving full marks "
            "or at least 4 out of 6."),
        (W, "However, many failed to use the information in the second bullet point fully (that the curve has a "
            "stationary point at $(4,3)$)."),
        (W, "The majority of the candidates achieved the first mark by understanding that the stationary point at "
            "$(4,3)$ meant that the first derivative must be equal to zero at $x=4$, arriving at $16+2a+b=0$."),
        (W, r"Again, the majority went on to perform the integration of the gradient function "
            r"$\int(4x+a\sqrt{x}+b)\,\mathrm{d}x$ to achieve $\mathrm{f}(x)=2x^2+\frac{2}{3}ax^{\frac{3}{2}}+bx+c$ with "
            r"the majority able to determine that $c=-5$."),
        (W, r"A common error was to achieve $\frac{3}{2}ax^{\frac{3}{2}}$ following integration, although those who had "
            r"written the unsimplified $\frac{ax^{\frac{3}{2}}}{\left(\frac{3}{2}\right)}$ were still able to access the "
            r"intermediate accuracy mark.", NO),
        (W, r"Common problems were for candidates to misinterpret the information about the stationary point, either "
            r"using $\mathrm{f}'(4)=3$ or $\mathrm{f}(4)=0$, or to miss out a constant of integration, which often "
            r"resulted in concluding that $b$ was $-5$."),
        (W, r"It was fairly common to see candidates substitute a rearranged $16+2a+b=0$ into their integrated expression "
            r"(usually for $b$) and this typically did not hinder further progress, although it did result in some sign "
            r"errors that meant their final expression $\mathrm{f}(x)$ was incorrect.", NO),
    ],
    "17": [
        (W, "This was a relatively accessible proof question and gave candidates two opportunities to demonstrate their "
            "knowledge and understanding of proof.", NO),
        (W, "It was pleasing to see that the general standard of response to this proof question was good, and it is "
            "clear that candidates’ confidence in and experience of tackling proof questions has improved over recent "
            "sessions.", NO),
        ({"a"}, "In part (a), most candidates understood what was meant by a counter example and many successfully found "
                "a pair of suitable numbers."),
        ({"a"}, "The mark here was often lost only due to insufficient reasoning."),
        ({"a"}, "Candidates should be reminded that when showing a falsehood via counter-example it is necessary to "
                "provide accompanying minimal reasoning.", NO),
        ({"a"}, "It was a shame that a significant number of candidates did not notice, or forgot, that the question "
                "specified that $p$ and $q$ were positive and that $q>p$ and it was not uncommon to see candidates chose "
                "numbers that broke these constraints which meant they were ineligible for this mark.", NO),
        ({"a"}, "A small proportion of candidates misunderstood or perhaps misread the question and believed they were "
                "being asked to demonstrate instead that $q^3-p^3$ is a multiple of 5."),
        ({"b"}, "Part (b) was more challenging and weaker candidates spent time here testing specific values for $p$ and "
                "$q$, but in general it provided good access for the majority of candidates.", NO),
        ({"b"}, "Most candidates pursued general forms for $p$ and $q$ as consecutive even numbers and most of these "
                "chosen forms had merit (usually $2n$ and $2n+2$ but sometimes $2n+2$ and $2n+4$).", NO),
        ({"b"}, "Incorrect forms included $n$ and $n+2$ (without consideration of $n$ as an even number), or sometimes $n$ "
                "and $m$ which were neither consecutive nor even."),
        ({"b"}, "The issue of failing to recognise that $q>p$ persisted into part (b) and a number of candidates lost "
                "marks for selecting $p$ as the larger even number and subtracting the two terms the wrong way around."),
        ({"b"}, "Expanding $(2n+2)^3$ also proved problematic for many candidates and so it was common for candidates to "
                "lose the accuracy marks.", NO),
        ({"b"}, "It was also common for poor subtraction to result in a cubic expression rather a quadratic which was "
                "even more costly in terms of marks.", NO),
        ({"b"}, "Unfortunately, many candidates failed to give even a minimal conclusion following impeccable algebra and "
                "so lost the final mark."),
        ({"b"}, "Again, candidates should be reminded of the importance of a final statement in proof such as this.", NO),
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
    "01a": ("easy", at("01", "In part (a), most candidates scored both marks")),
    "01b": ("medium", at("01", "A significant number of candidates who had found critical values")),
    "02": ("hard", at("02", "Furthermore, candidates very often")),
    "03a": ("hard", at("03", "The vast majority of candidates recognised")),
    "03b": ("easy", at("03", "Part (b) was generally well answered")),
    "04a": ("easy", at("04", "In part (a), most candidates appeared")),
    "04b": ("hard", at("04", "In part (b), most candidates only scored 1 mark")),
    "05": ("medium", at("05", "However, there were plenty of candidates")),
    "06a": ("easy", at("06", "Part (a) of this question was well answered")),
    "06b": ("hard", at("06", "However, part (b) appeared to be inaccessible")),
    "07a": ("medium", at("07", "The most common error was to use the coordinates")),
    "07b": ("medium", at("07", "A common error was to omit the units")),
    "07c": ("hard", at("07", "Very few candidates achieved the mark for part (c)")),
    "08": ("hard", at("08", "Very few candidates achieved full marks")),
    "09": ("hard", at("09", "The final mark was a particularly good discriminator")),
    "10a": ("easy", at("10", "This “show that” question in part (a)")),
    "10b": ("medium", at("10", "However, many failed to recognise that the base")),
    "11a": ("easy", at("11", "In part (a), most candidates identified")),
    "11b": ("hard", at("11", "In part (b), the majority of candidates failed")),
    "11c": ("easy", at("11", "In part (c), most candidates identified")),
    "12a": ("easy", at("12", "Part (a) was generally well answered")),
    "12b": ("medium", at("12", "Part (b) was attempted by the majority")),
    "12c": ("hard", at("12", "Part (c) was much less successful")),
    "13a": ("easy", at("13", "In part (a), most candidates successfully reached")),
    "13b": ("easy", at("13", "Most were then able to calculate")),
    "13c": ("medium", at("13", "Many candidates did not successfully reach")),
    "14": ("medium", at("14", "A significant proportion of the candidates who got so far")),
    "15a": ("easy", at("15", "The majority of candidates, having achieved")),
    "15b": ("hard", at("15", "As a result, there were very few candidates")),
    "16": ("medium", at("16", "However, many failed to use the information")),
    "17a": ("medium", at("17", "The mark here was often lost")),
    "17b": ("medium", at("17", "Unfortunately, many candidates failed")),
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
