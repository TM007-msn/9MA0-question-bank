"""Draft builder for 8MA0-01 2019-06 (AS Pure, June 2019).

Run (from the project root, with the venv active):
    python extraction/8MA0-01_2019-06.py        # writes out/drafts/8MA0-01_2019-06.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-01_2019-06.json

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

P, S = "8MA0-01", "2019-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "04bii"); label as printed (e.g. "4(b)(ii)")."""
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


# Notes shared by several marks.
TONNES = "Only withhold the mark for a lack of tonnes, once, the first time that it occurs. "

def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q1 = ["The line $l_1$ has equation $2x+4y-3=0$", "The line $l_2$ has equation $y=mx+7$, where $m$ is a constant.",
      "Given that $l_1$ and $l_2$ are perpendicular,"]
Q3A = ["Given that $k$ is a constant, find", r"$$\int\left(\frac{4}{x^3}+kx\right)\mathrm{d}x$$", "simplifying your answer."]
Q4 = ["A tree was planted in the ground.", "Its height, $H$ metres, was measured $t$ years after planting.",
      "Exactly 3 years after planting, the height of the tree was 2.35 metres.",
      "Exactly 6 years after planting, the height of the tree was 3.28 metres.",
      "Using a linear model,"]
Q5 = ["A curve has equation", r"$$y=3x^2+\frac{24}{x}+2\qquad x>0$$"]
Q5A = r"Find, in simplest form, $\frac{\mathrm{d}y}{\mathrm{d}x}$"
Q6 = [r"[Figure 1: triangle $ABC$ with $AB=3x$ cm as the base, $AC=2x$ cm, and the angle of $60^\circ$ at $A$ marked.]",
      r"Figure 1 shows a sketch of a triangle $ABC$ with $AB=3x$ cm, $AC=2x$ cm and angle $CAB=60^\circ$",
      r"Given that the area of triangle $ABC$ is $18\sqrt{3}$ cm$^2$"]
Q7 = ["The curve $C$ has equation", r"$$y=\frac{k^2}{x}+1\qquad x\in\mathbb{R},\ x\neq0$$", "where $k$ is a constant."]
Q7L = "The line $l$ has equation $y=-2x+5$"
Q7B = ["Show that the $x$ coordinate of any point of intersection of $l$ with $C$ is given by a solution of the equation",
       "$$2x^2-4x+k^2=0$$"]
Q8A = ["Find the first 3 terms, in ascending powers of $x$, of the binomial expansion of",
       r"$$\left(2+\frac{3x}{4}\right)^6$$", "giving each term in its simplest form."]
Q9 = ["A company started mining tin in Riverdale on 1st January 2019.",
      "A model to find the total mass of tin that will be mined by the company in Riverdale is given by the equation",
      "$$T=1200-3(n-20)^2$$",
      "where $T$ tonnes is the total mass of tin mined in the $n$ years after the start of mining.",
      "Using this model,"]
Q10 = ["A circle $C$ has equation", "$$x^2+y^2-4x+8y-8=0$$"]
Q11 = [r"$$\mathrm{f}(x)=2x^3-13x^2+8x+48$$"]
Q11A = r"Prove that $(x-4)$ is a factor of $\mathrm{f}(x)$."
Q11F = [r"[Figure 2: sketch of part of the curve $y=\mathrm{f}(x)$: a positive cubic crossing the negative $x$-axis once, "
        r"with a maximum just to the right of the $y$-axis and touching the positive $x$-axis at a minimum.]",
        r"Figure 2 shows a sketch of part of the curve with equation $y=\mathrm{f}(x)$."]
Q12A = ["Show that", r"$$\frac{10\sin^2\theta-7\cos\theta+2}{3+2\cos\theta}\equiv4-5\cos\theta$$"]
Q14 = [r"The value of a car, £$V$, can be modelled by the equation",
       r"$$V=15\,700\mathrm{e}^{-0.25t}+2300\qquad t\in\mathbb{R},\ t\geqslant0$$",
       "where the age of the car is $t$ years.", "Using the model,"]
Q14B = "Given the model predicts that the value of the car is decreasing at a rate of £500 per year at the instant when $t=T$,"
Q14A = "The model predicts that the value of the car approaches, but does not fall below, £$A$."

LATEX = {
    "01a": L(*Q1, "find the value of $m$."),
    "01b": L(*Q1, "The lines $l_1$ and $l_2$ meet at the point $P$.", "Find the $x$ coordinate of $P$."),
    "02i": L("Find, using algebra, all real solutions to the equation", r"$16a^2=2\sqrt{a}$"),
    "02ii": L("Find, using algebra, all real solutions to the equation", "$b^4+7b^2-18=0$"),
    "03a": L(*Q3A),
    "03b": L("(a) " + Q3A[0], *Q3A[1:], "(b) Hence find the value of $k$ such that",
             r"$$\int_{0.5}^{2}\left(\frac{4}{x^3}+kx\right)\mathrm{d}x=8$$"),
    "04a": L(*Q4, "find an equation linking $H$ with $t$."),
    "04b": L(*Q4, "(a) find an equation linking $H$ with $t$.",
             "The height of the tree was approximately 140 cm when it was planted.",
             "(b) Explain whether or not this fact supports the use of the linear model in part (a)."),
    "05a": L(*Q5, Q5A),
    "05b": L(*Q5, "(a) " + Q5A, "(b) Hence find the exact range of values of $x$ for which the curve is increasing."),
    "06a": L(*Q6, r"show that $x=2\sqrt{3}$"),
    "06b": L(*Q6, r"(a) show that $x=2\sqrt{3}$",
             "(b) Hence find the exact length of $BC$, giving your answer as a simplified surd."),
    "07a": L(*Q7, "Sketch $C$ stating the equation of the horizontal asymptote."),
    "07b": L(*Q7, Q7L, *Q7B),
    "07c": L(*Q7, Q7L, "(b) " + Q7B[0], Q7B[1], "(c) Hence find the exact values of $k$ for which $l$ is a tangent to $C$."),
    "08a": L(*Q8A),
    "08b": L("(a) " + Q8A[0], *Q8A[1:],
             "(b) Explain how you could use your expansion to estimate the value of $1.925^6$",
             "You do not need to perform the calculation."),
    "09a": L(*Q9, "calculate the mass of tin that will be mined up to 1st January 2020,"),
    "09b": L(*Q9[:-1], "Deduce the maximum total mass of tin that could be mined,"),
    "09c": L(*Q9[:-1], "Calculate the mass of tin that will be mined in 2023."),
    "09d": L(*Q9[:-1], "State, giving reasons, the limitation on the values of $n$."),
    "10a": L(*Q10, "Find", "(i) the coordinates of the centre of $C$,", "(ii) the exact radius of $C$."),
    "10b": L(*Q10, "The straight line with equation $x=k$, where $k$ is a constant, is a tangent to $C$.",
             "Find the possible values for $k$."),
    "11a": L(*Q11, Q11A),
    "11b": L(*Q11, "(a) " + Q11A,
             r"(b) Hence, using algebra, show that the equation $\mathrm{f}(x)=0$ has only two distinct roots."),
    "11c": L(*Q11, *Q11F, "Deduce, giving reasons for your answer, the number of real roots of the equation",
             "$$2x^3-13x^2+8x+46=0$$"),
    "11d": L(*Q11, *Q11F,
             r"Given that $k$ is a constant and the curve with equation $y=\mathrm{f}(x+k)$ passes through the origin,",
             "find the two possible values of $k$."),
    "12a": L(*Q12A),
    "12b": L("(a) " + Q12A[0], Q12A[1], r"(b) Hence, or otherwise, solve, for $0\leqslant x<360^\circ$, the equation",
             r"$$\frac{10\sin^2x-7\cos x+2}{3+2\cos x}=4+3\sin x$$"),
    "13": L(r"[Figure 3: sketch of part of the curve $y=2x^3-17x^2+40x$, passing through $O$, rising to a maximum and "
            r"falling to a minimum above the $x$-axis at $x=k$, then rising; the region $R$ between the curve, the "
            r"$x$-axis and the vertical line $x=k$ is shaded.]",
            "Figure 3 shows a sketch of part of the curve with equation", "$$y=2x^3-17x^2+40x$$",
            "The curve has a minimum turning point at $x=k$.",
            "The region $R$, shown shaded in Figure 3, is bounded by the curve, the $x$-axis and the line with equation "
            "$x=k$.",
            r"Show that the area of $R$ is $\frac{256}{3}$",
            "(Solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "14a": L(*Q14, "find the initial value of the car."),
    "14b": L(*Q14[:-1], Q14B, "(i) show that", r"$$3925\mathrm{e}^{-0.25T}=500$$",
             "(ii) Hence find the age of the car at this instant, giving your answer in years and months to the nearest "
             "month.",
             "(Solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "14c": L(*Q14[:-1], Q14B, Q14A, "State the value of $A$."),
    "14d": L(*Q14[:-1], Q14B, Q14A, "State a limitation of this model."),
    "15": L(r"Given $n\in\mathbb{N}$, prove that $n^3+2$ is not divisible by 8"),
    "16i": L(r"Two non-zero vectors, $\mathbf{a}$ and $\mathbf{b}$, are such that",
             r"$$|\mathbf{a}+\mathbf{b}|=|\mathbf{a}|+|\mathbf{b}|$$",
             "Explain, geometrically, the significance of this statement."),
    "16ii": L(r"Two different vectors, $\mathbf{m}$ and $\mathbf{n}$, are such that $|\mathbf{m}|=3$ and "
              r"$|\mathbf{m}-\mathbf{n}|=6$",
              r"The angle between vector $\mathbf{m}$ and vector $\mathbf{n}$ is $30^\circ$",
              r"Find the angle between vector $\mathbf{m}$ and vector $\mathbf{m}-\mathbf{n}$, giving your answer, in "
              r"degrees, to one decimal place."),
}

# Earlier parts shown where a part needs their result (standalone sweep, 2026-10-10).
LATEX.update({
    "01b": L(
        r"The line $l_1$ has equation $2x+4y-3=0$",
        r"The line $l_2$ has equation $y=mx+7$, where $m$ is a constant.",
        r"Given that $l_1$ and $l_2$ are perpendicular,",
        r"(a) find the value of $m$.",
        r"The lines $l_1$ and $l_2$ meet at the point $P$.",
        r"(b) Find the $x$ coordinate of $P$.",
    ),
    "10b": L(
        r"A circle $C$ has equation",
        r"$$x^2+y^2-4x+8y-8=0$$",
        r"(a) Find",
        r"(i) the coordinates of the centre of $C$,",
        r"(ii) the exact radius of $C$.",
        r"The straight line with equation $x=k$, where $k$ is a constant, is a tangent to $C$.",
        r"(b) Find the possible values for $k$.",
    ),
    "11d": L(
        r"$$\mathrm{f}(x)=2x^3-13x^2+8x+48$$",
        r"(a) Prove that $(x-4)$ is a factor of $\mathrm{f}(x)$.",
        r"(b) Hence, using algebra, show that the equation $\mathrm{f}(x)=0$ has only two distinct roots.",
        r"[Figure 2: sketch of part of the curve $y=\mathrm{f}(x)$: a positive cubic crossing the negative $x$-axis once, with a maximum just to the right of the $y$-axis and touching the positive $x$-axis at a minimum.]",
        r"Figure 2 shows a sketch of part of the curve with equation $y=\mathrm{f}(x)$.",
        r"Given that $k$ is a constant and the curve with equation $y=\mathrm{f}(x+k)$ passes through the origin,",
        r"(d) find the two possible values of $k$.",
    ),
})

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", COORD, "3.1", 2, LATEX["01a"],
      [r"M1 (AO 1.1b): $2x+4y-3=0\Rightarrow y=\mp\frac{2}{4}x+\ldots$; gradient of perpendicular $=\pm\frac{4}{2}$. "
       r"Notes: Attempts to set given equation in the form $y=ax+b$ with $a=\mp\frac{2}{4}$ oe such as $\mp\frac{1}{2}$ "
       r"AND deduces that $m=-\frac{1}{a}$. Condone errors on the “$+b$”.",
       r"A1 (AO 1.1b): Either $m=2$ or $y=2x+7$. Notes: Correct answer. Accept either $m=2$ or $y=2x+7$. "
       r"This must be simplified and not left as $m=\frac{4}{2}$ or $m=2x$ unless you see $y=2x+7$. "
       r"Watch: There may be candidates who look at $2x+4y-3=0$ and incorrectly state that the gradient is 2 and use "
       r"the perpendicular rule to get $m=-\frac{1}{2}$. They will score M0 A0 in (a) and also no marks in (b) as the "
       r"lines would be parallel. In a case like this don't allow an equation to be “altered”. Candidates who state "
       r"$m=2$ or $y=2x+7$ with no incorrect working can score both marks.",
       r"ALT: Alternative method (a) — M1 (AO 1.1b): An alternative method is to find both intercepts to get gradient "
       r"$l_1=\pm\frac{0.75}{1.5}$ and use the perpendicular gradient rule."],
      False, 2),
    e("01b", "1(b)", COORD, "3.1, 2.4", 2,
      LATEX["01b"],
      [r"M1 (AO 1.1b): Combines 'their' $y=2x+7$ with $2x+4y-3=0\Rightarrow2x+4(2x+7)-3=0\Rightarrow x=\ldots$ "
       r"Notes: Substitutes their $y=mx+7$ into $2x+4y-3=0$, condoning slips, in an attempt to form and solve an "
       r"equation in $x$. Don't be too concerned by the mechanics of the candidates attempt to solve. (E.g. allow "
       r"solutions from their calculators.) You may see $2x+4y-3=2x-y+7$ with $y$ being found before the value of $x$ "
       r"appears. It cannot be awarded from “unsolvable” equations (e.g. lines that are parallel).",
       r"A1 (AO 1.1b): $x=-2.5$ oe. Notes: $x=-2.5$. The answer alone can score both marks as long as both equations "
       r"are correct and no incorrect working is seen. Remember to isw after the correct answer and ignore any $y$ "
       r"coordinate.",
       r"ALT: Alternatively (b) — M1 (AO 1.1b): Alternatively equates their $y=-\frac{1}{2}x+\frac{3}{4}$ with their "
       r"$y=mx+7$ in an attempt to form and solve, condoning slips, an equation in $x$."],
      False, 2),

    # ---------------- Q2 ----------------
    e("02i", "2(i)", ALG, "2.1", 4, LATEX["02i"],
      [r"M1 (AO 1.1b): $16a^2=2\sqrt{a}\Rightarrow a^{\frac{3}{2}}=\frac{1}{8}$. Notes: Combines the two algebraic "
       r"terms to reach $a^{\pm\frac{3}{2}}=C$ or equivalent such as $(\sqrt{a})^3=C$ $(C\neq0)$. Allow for slips on "
       r"coefficients.",
       r"M1 (AO 1.1b): $\Rightarrow a=\left(\frac{1}{8}\right)^{\frac{2}{3}}$. Notes: Undoes the indices correctly for "
       r"their $a^{\frac{m}{n}}=C$ (So M0 M1 A0 is possible). You may even see logs used.",
       r"A1 (AO 1.1b): $\Rightarrow a=\frac{1}{4}$. Notes: $a=\frac{1}{4}$ and no other solutions apart from 0. "
       r"Accept exact equivalents Eg 0.25",
       r"B1 (AO 2.2a): Deduces that $a=0$ is a solution. Notes: Deduces that $a=0$ is a solution. Answers with minimal "
       r"or no working, in part (i): no working, just answer(s) with they can score the B1; if they square and proceed "
       r"to the quartic equation $256a^4=4a$ oe, and then write down the answers they can have access to all marks.",
       r"ALT: Second scheme column — M1 (AO 1.1b): $16a^2-2\sqrt{a}=0\Rightarrow2a^{\frac{1}{2}}\left(8a^{\frac{3}{2}}-1\right)=0"
       r"\Rightarrow a^{\frac{3}{2}}=\frac{1}{8}$",
       r"ALT: Second scheme column — M1 (AO 1.1b): $\Rightarrow a=\left(\frac{1}{8}\right)^{\frac{2}{3}}$",
       r"ALT: Second scheme column — A1 (AO 1.1b): $\Rightarrow a=\frac{1}{4}$",
       r"ALT: Second scheme column — B1 (AO 2.2a): Deduces that $a=0$ is a solution",
       r"ALT: Alternative via squaring (notes) — M1 (AO 1.1b): An alternative is via squaring and combining the "
       r"algebraic terms to reach $a^{\pm3}=k, k>0$. Eg. $\ldots a^4=\ldots a\Rightarrow a^{\pm3}=k$ or "
       r"$\ldots a^4=\ldots a\Rightarrow\ldots a^4-\ldots a=0\Rightarrow\ldots a\left(a^3-\ldots\right)=0\Rightarrow a^3=\ldots$"],
      False, 4),
    e("02ii", "2(ii)", ALG, "2.3", 4, LATEX["02ii"],
      [r"M1 (AO 1.1b): $b^4+7b^2-18=0\Rightarrow(b^2+9)(b^2-2)=0$. Notes: Attempts to solve as a quadratic equation "
       r"in $b^2$. Accept $(b^2+m)(b^2+n)=0$ with $mn=\pm18$ or solutions via the use of the quadratic formula. Also "
       r"allow candidates to substitute in another variable, say $u=b^2$ and solve for $u$",
       r"A1 (AO 1.1b): $b^2=-9, 2$. Notes: Correct solution. Allow for $b^2=2$ or $u=2$ with no incorrect solution "
       r"given. Candidates can choose to omit the solution $b^2=-9$ or $u=-9$ and so may not be seen",
       r"dM1 (AO 2.3): $b^2=k\Rightarrow b=\sqrt{k}, k>0$. Notes: Finds at least one solution from their "
       r"$b^2=k\Rightarrow b=\sqrt{k}, k>0$. Allow $b=1.414$",
       r"A1 (AO 1.1b): $b=\sqrt{2}, -\sqrt{2}$ only. Notes: $b=\sqrt{2}, -\sqrt{2}$ only. The solution asks for real "
       r"values so if $3i$ is given then score A0. Answers with minimal or no working, in part (ii): accept for 4 marks "
       r"$b^2=2\Rightarrow b=\pm\sqrt{2}$; no working, no marks."],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", INT, "8.2", 3,
      LATEX["03a"],
      [r"M1 (AO 1.1b): $x^n\to x^{n+1}$. Notes: Mark parts (a) and (b) as one. For $x^n\to x^{n+1}$ for either "
       r"$x^{-3}$ or $x^1$. This can be implied by the sight of either $x^{-2}$ or $x^2$. Condone “unprocessed” "
       r"values here. Eg. $x^{-3+1}$ and $x^{1+1}$",
       r"A1 (AO 1.1b): $\int\left(\frac{4}{x^3}+kx\right)\mathrm{d}x=-\frac{2}{x^2}+\frac{1}{2}kx^2+c$. Notes: Either "
       r"term correct (un simplified). Accept $4\times\frac{x^{-2}}{-2}$ or $k\frac{x^2}{2}$ with the indices processed.",
       r"A1 (AO 1.1b): $-\frac{2}{x^2}+\frac{1}{2}kx^2+c$. Notes: Correct (and simplified) with $+c$. Ignore spurious "
       r"notation e.g. answer appearing with an $\int$ sign or with $\mathrm{d}x$ on the end. Accept "
       r"$-\frac{2}{x^2}+\frac{1}{2}kx^2+c$ or exact simplified equivalent such as $-2x^{-2}+k\frac{x^2}{2}+c$"],
      False, 6),
    e("03b", "3(b)", INT, "8.3, 8.2", 3,
      LATEX["03b"],
      [r"M1 (AO 1.1b): $\left[-\frac{2}{x^2}+\frac{1}{2}kx^2\right]_{0.5}^{2}=\left(-\frac{2}{2^2}+\frac{1}{2}k\times4\right)"
       r"-\left(-\frac{2}{(0.5)^2}+\frac{1}{2}k\times(0.5)^2\right)=8$. Notes: Mark parts (a) and (b) as one. For "
       r"substituting both limits into their $-\frac{2}{x^2}+\frac{1}{2}kx^2$, subtracting either way around and setting "
       r"equal to 8. Allow this when using a changed function. (so the M in part (a) may not have been awarded). Condone "
       r"missing brackets. Take care here as substituting 2 into the original function gives the same result as the "
       r"integrated function so you will have to consider both limits.",
       r"dM1 (AO 1.1b): $7.5+\frac{15}{8}k=8\Rightarrow k=\ldots$ Notes: For solving a linear equation in $k$. It is "
       r"dependent upon the previous M only. Don't be too concerned by the mechanics here. Allow for a linear equation "
       r"in $k$ leading to $k=$",
       r"A1 (AO 1.1b): $k=\frac{4}{15}$ oe. Notes: $k=\frac{4}{15}$ or exact equivalent. Allow for $\frac{m}{n}$ where "
       r"$m$ and $n$ are integers and $\frac{m}{n}=\frac{4}{15}$. Condone the recurring decimal $0.2\dot{6}$ but not "
       r"0.266 or 0.267. Please remember to isw after a correct answer"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", COORD, "3.1", 3, LATEX["04a"],
      [r"M1 (AO 3.3): Attempts $H=mt+c$ with both $(3, 2.35)$ and $(6, 3.28)$. Notes: Mark parts (a) and (b) as one. "
       r"For creating a linear model with both pieces of information given. Eg. Accept sight of $2.35=3m+c$ and "
       r"$3.28=6m+c$. Condone slips on the 2.35 and 3.28. Allow for an attempt at the “gradient” "
       r"$m=\frac{3.28-2.35}{6-3}(=0.31)$ or the intercept. Allow for a pair of simultaneous in any variable even $x$ "
       r"and $y$",
       r"dM1 (AO 3.1a): Method to find both $m$ and $c$. Notes: A full method to find both constants. For simultaneous "
       r"equations award if they arrive at values for $m$ and $c$. If they attempted the gradient it would be for "
       r"attempting to find “$c$” using $y=mx+c$ with their $m$ and one of the points $(3, 2.35)$ or $(6, 3.28)$",
       r"A1 (AO 1.1b): $H=0.31t+1.42$ oe. Notes: A correct model using allowable/correct variables. $H=0.31t+1.42$. "
       r"Condone $h\leftrightarrow H, t\leftrightarrow T$. Allow equivalents such as $H=\frac{31}{100}t+\frac{142}{100}$, "
       r"$t=\frac{H-1.42}{0.31}$ but not $H=\frac{0.93}{3}t+1.42$. Do not allow $H=0.31t+1.42$ m (with the units)"],
      False, 8),
    e("04b", "4(b)", COORD, "3.1", 2,
      LATEX["04b"],
      [r"B1ft (AO 3.4): Uses the model and states that the initial height is their '$b$'. Notes: Mark parts (a) and "
       r"(b) as one. To score any marks in (b) the model must be of the form $H=mt+b$ where $m>0, b>0$. States or "
       r"implies that 1.42 (with or without units) or 142 cm (including the units) is the original height or the height "
       r"when $t=0$. You should allow statements such as $c=1.42$ or original height = 1.42 (m). Follow through on their "
       r"value of '$c$', so for $H=0.25t+1.60$ it is scored for stating the initial height is 1.60 (m) or 160 cm. Do "
       r"not follow through if $c\leqslant0$",
       r"B1ft (AO 3.5a): Compares 140 cm with their 1.42 (m) and makes a valid comment. In the case where "
       r"$H=0.31t+1.42$ it should be this fact supports the use of the linear model as the values are close. Notes: "
       r"Compares 140 cm with their 1.42 (m) and makes a valid comment. In the case where $H=0.31t+1.42$ it should be "
       r"this fact supports the use of the linear model as the values are close or approximately the same. Allow "
       r"$1.42\text{ m}\approx1.4\text{ m}$ or similar. In the case of $H=0.25t+1.60$ it would be for stating that the "
       r"fact that it does not support the use of the model as the values are too different. If they state "
       r"$1.60>1.40$ this is insufficient. They cannot just state that they are not the same. It must be implied that "
       r"there is a significant difference. As a rule of thumb use “good model” for between 135cm and 145 cm. This "
       r"requires a correct calculation for their $H$, a correct statement with an appreciation shown for the units and "
       r"a correct conclusion. SC B1 B0: Award SC for incomplete answers which suggest the candidate knows what to do. "
       r"Eg. In (b) $H=0.31t+1.42$ followed by in (c) It supports the model as when $t=0$ it is approximately 140 cm"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", DIFF, "7.2", 3, LATEX["05a"],
      [r"M1 (AO 1.1b): $x^n\to x^{n-1}$. Notes: $x^n\to x^{n-1}$ for any correct index of $x$. Score for $x^2\to x$ or "
       r"$x^{-1}\to x^{-2}$. Allow for unprocessed indices. $x^2\to x^{2-1}$ oe",
       r"A1 (AO 1.1b): $\left(\frac{\mathrm{d}y}{\mathrm{d}x}=\right)6x-\frac{24}{x^2}$. Notes: Sight of either $6x$ or "
       r"$-\frac{24}{x^2}$ which may be un simplified. Condone an additional term e.g. + 2 for this mark. The indices "
       r"now must have been processed",
       r"A1 (AO 1.1b): $\left(\frac{\mathrm{d}y}{\mathrm{d}x}=\right)6x-\frac{24}{x^2}$. Notes: "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}=6x-\frac{24}{x^2}$ or exact simplified equivalent. Eg accept "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}=6x^1-24x^{-2}$. You do not need to see the $\frac{\mathrm{d}y}{\mathrm{d}x}$ "
       r"and you should isw after a correct simplified answer."],
      False, 10),
    e("05b", "5(b)", DIFF, "7.3, 2.5", 2,
      LATEX["05b"],
      [r"M1 (AO 1.1b): Attempts $6x-\frac{24}{x^2}>0\Rightarrow x>$ Notes: Sets an allowable "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}\ldots0$ and proceeds to $x\ldots$ via an allowable intermediate equation. "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}$ must be in the form $Ax+Bx^{-2}$ where $A,B\neq0$ and the intermediate "
       r"equation must be of the form $x^p\ldots q$ oe. Do not be concerned by either the processing, an equality or a "
       r"different inequality. It may be implied by $x=$ awrt 1.59",
       r"A1 (AO 2.5): $x>\sqrt[3]{4}$ or $x\geqslant\sqrt[3]{4}$. Notes: $x>\sqrt[3]{4}$ or $x\geqslant\sqrt[3]{4}$ oe "
       r"such as $x>4^{\frac{1}{3}}$ or $x\geqslant2^{\frac{2}{3}}$"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", TRIG, "5.1, 2.2", 3, LATEX["06a"],
      [r"M1 (AO 1.1a): Uses $18\sqrt{3}=\frac{1}{2}\times2x\times3x\times\sin60^\circ$. Notes: Attempts to use the "
       r"formula $A=\frac{1}{2}ab\sin C$. If the candidate writes $18\sqrt{3}=\frac{1}{2}\times5x\times\sin60^\circ$ "
       r"without sight of a previous correct line then this would be M0",
       r"M1 (AO 1.1b): Sight of $\sin60^\circ=\frac{\sqrt{3}}{2}$ and proceeds to $x^2=k$ oe. Notes: Sight of "
       r"$\sin60^\circ=\frac{\sqrt{3}}{2}$ or awrt 0.866 and proceeds to $x^2=k$ oe such as $px^2=q$. This may be "
       r"awarded from the correct formula or $A=ab\sin C$",
       r"A1* (AO 2.1): $x=\sqrt{12}=2\sqrt{3}$ *. Notes: Look for $x^2=12\Rightarrow x=2\sqrt{3}$, "
       r"$x^2=4\times3\Rightarrow x=2\sqrt{3}$ or $x=\sqrt{12}=2\sqrt{3}$. This is a given answer and all aspects must "
       r"be correct including one of the above intermediate lines. It cannot be scored by using decimal equivalents to "
       r"$\sqrt{3}$",
       r"ALT: Alternative using the given answer of $x=2\sqrt{3}$ — M1: Attempts to use the formula "
       r"$A=\frac{1}{2}\times4\sqrt{3}\times6\sqrt{3}\sin60^\circ$ oe",
       r"ALT: Alternative using the given answer of $x=2\sqrt{3}$ — M1: Sight of $\sin60^\circ=\frac{\sqrt{3}}{2}$ and "
       r"proceeds to $A=18\sqrt{3}$",
       r"ALT: Alternative using the given answer of $x=2\sqrt{3}$ — A1*: Concludes that $x=2\sqrt{3}$"],
      True, 12),
    e("06b", "6(b)", TRIG, "5.1, 2.2", 3,
      LATEX["06b"],
      [r"M1 (AO 1.1b): Uses $BC^2=(6\sqrt{3})^2+(4\sqrt{3})^2-2\times6\sqrt{3}\times4\sqrt{3}\times\cos60^\circ$. Notes: "
       r"Attempts the cosine rule with the sides in the correct position. This can be scored from "
       r"$BC^2=(3x)^2+(2x)^2-2\times3x\times2x\times\cos60^\circ$ as long as there is some attempt to substitute $x$ in "
       r"later. Condone slips on the squaring",
       r"A1 (AO 1.1b): $BC^2=84$. Notes: $BC^2=84$. Accept $BC^2=7\times12$, $BC=\sqrt{84}$ or $BC=2\sqrt{21}$. If they "
       r"replace the surds with decimals they can score the A1 for $BC^2=$ awrt 84.0",
       r"A1 (AO 1.1b): $BC=2\sqrt{21}$ (cm). Notes: $BC=2\sqrt{21}$. Condone other variables, say $x=2\sqrt{21}$, but "
       r"it cannot be scored via decimals."],
      True, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", ALG, "2.7", 3, LATEX["07a"],
      [r"M1 (AO 1.1b): $\frac{1}{x}$ shape in 1st quadrant (shown on a sketch in the mark scheme). Notes: For the shape "
       r"of a $\frac{1}{x}$ type curve in Quadrant 1. It must not cross either axis and have acceptable curvature. Look "
       r"for a negative gradient changing from $-\infty$ to 0 condoning “slips of the pencil”. (See Practice and "
       r"Qualification for clarification)",
       r"A1 (AO 1.1b): Correct. Notes: Correct shape and position for both branches. It must lie in Quadrants 1, 2 and "
       r"3 and have the correct curvature including asymptotic behaviour",
       r"B1 (AO 1.2): Asymptote $y=1$. Notes: Asymptote given as $y=1$. This could appear on the diagram or within the "
       r"text. Note that the curve does not need to be asymptotic at $y=1$ but this must be the only horizontal "
       r"asymptote offered by the candidate."],
      False, 14),
    e("07b", "7(b)", ALG, "2.4", 2,
      LATEX["07b"],
      [r"M1 (AO 1.1b): Combines equations $\Rightarrow\frac{k^2}{x}+1=-2x+5$. Notes: Attempts to combine "
       r"$y=\frac{k^2}{x}+1$ with $y=-2x+5$ to form an equation in just $x$",
       r"A1* (AO 2.1): $(\times x)\Rightarrow k^2+1x=-2x^2+5x\Rightarrow2x^2-4x+k^2=0$ *. Notes: Multiplies by $x$ "
       r"(the processed line must be seen) and proceeds to given answer with no slips. Condone if the order of the terms "
       r"are different $2x^2+k^2-4x=0$"],
      False, 14),
    e("07c", "7(c)", ALG, "2.3, 2.4", 3,
      LATEX["07c"],
      [r"M1 (AO 3.1a): Attempts to set $b^2-4ac=0$. Notes: Deduces that $b^2-4ac=0$ or equivalent for the given "
       r"equation. If $a$, $b$ and $c$ are stated only accept $a=2, b=\pm4, c=k^2$ so $4^2-4\times2\times k^2=0$",
       r"A1 (AO 1.1b): $8k^2=16$. Notes: $8k^2=16$ or exact simplified equivalent. Eg $8k^2-16=0$. If $a$, $b$ and $c$ "
       r"are stated they must be correct. Note that $b^2$ appearing as $4^2$ is correct",
       r"A1 (AO 1.1b): $k=\pm\sqrt{2}$. Notes: $k=\pm\sqrt{2}$ and following correct $a$, $b$ and $c$ if stated",
       r"ALT: Alternatively (c), completing the square — M1: Alternatively completes the square "
       r"$x^2-2x+\frac{1}{2}k^2=0\Rightarrow(x-1)^2=1-\frac{1}{2}k^2\Rightarrow$ “$1-\frac{1}{2}k^2$” $=0$",
       r"ALT: A solution via differentiation (c) — M1: Sets the gradient of the curve "
       r"$=-2\Rightarrow-\frac{k^2}{x^2}=-2\Rightarrow x=(\pm)\frac{k}{\sqrt{2}}$ oe and attempts to substitute into "
       r"$2x^2-4x+k^2=0$",
       r"ALT: A solution via differentiation (c) — A1: $2k^2=(\pm)2\sqrt{2}k$ oe",
       r"ALT: A solution via differentiation (c) — A1: $k=\pm\sqrt{2}$"],
      False, 14),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", "Sequences and series", "4.1", 4, LATEX["08a"],
      [r"B1 (AO 1.1b): $2^6$ or 64 as the constant term. Notes: Sight of either $2^6$ or 64 as the constant term",
       r"M1 (AO 1.1b): $\left(2+\frac{3x}{4}\right)^6=\ldots+{}^6C_1\,2^5\left(\frac{3x}{4}\right)^1"
       r"+{}^6C_2\,2^4\left(\frac{3x}{4}\right)^2+\ldots$ Notes: An attempt at the binomial expansion. This may be "
       r"awarded for a correct attempt at either the second OR third term. Score for the correct binomial coefficient "
       r"with the correct power of 2 and the correct power of $\frac{3x}{4}$ condoning slips. Correct bracketing is not "
       r"essential for this M mark. Condone ${}^6C_2\,2^4\frac{3x^2}{4}$ for this mark",
       r"A1 (AO 1.1b): $=\ldots+6\times2^5\left(\frac{3x}{4}\right)^1+\frac{6\times5}{2}\times2^4\left(\frac{3x}{4}\right)^2"
       r"+\ldots$ Notes: Correct (unsimplified) second AND third terms. The binomial coefficients must be processed to "
       r"numbers /numerical expression e.g $\frac{6!}{4!2!}$ or $\frac{6\times5}{2}$. They cannot be left in the form "
       r"${}^6C_1$ and/or $\binom{6}{2}$",
       r"A1 (AO 1.1b): $=64+144x+135x^2+\ldots$ Notes: $64+144x+135x^2+\ldots$ Ignore any terms after this. Allow to "
       r"be written $64, 144x, 135x^2$",
       r"ALT: Alternative to part (a), $\left(2+\frac{3x}{4}\right)^6=2^6\left(1+\frac{3x}{8}\right)^6="
       r"2^6\left(1+{}^6C_1\left(\frac{3x}{8}\right)^1+{}^6C_2\left(\frac{3x}{8}\right)^2+\ldots\right)$ — B1: Sight "
       r"of either $2^6$ or 64",
       r"ALT: Alternative to part (a) — M1: An attempt at the binomial expansion. This may be awarded for either the "
       r"second or third term. Score for the correct binomial coefficient with the correct power of $\frac{3x}{8}$ "
       r"Correct bracketing is not essential for this mark.",
       r"ALT: Alternative to part (a) — A1: A correct attempt at the binomial expansion on the second and third terms.",
       r"ALT: Alternative to part (a) — A1: $64+144x+135x^2+\ldots$ Ignore any terms after this."],
      False, 16),
    e("08b", "8(b)", "Sequences and series", "4.1", 1,
      LATEX["08b"],
      [r"B1ft (AO 2.4): $\frac{3x}{4}=-0.075\Rightarrow x=-0.1$ So find the value of $64+144x+135x^2$ with $x=-0.1$. "
       r"Notes: $x=-0.1$ or $-\frac{1}{10}$ with a comment about substituting this into their $64+144x+135x^2$. If "
       r"they have written (a) as $64, 144x, 135x^2$ candidate would need to say substitute $x=-0.1$ into the sum of "
       r"the first three terms. As they do not have to perform the calculation allow: Set $2+\frac{3x}{4}=1.925$, solve "
       r"for $x$ and then substitute this value into the expression from (a). If a value of $x$ is found then it must "
       r"be correct"],
      False, 16),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", ALG, "2.3", 1, LATEX["09a"],
      [r"B1 (AO 3.4): 117 tonnes. Notes: " + TONNES + r"117 tonnes or 117 t."],
      False, 18),
    e("09b", "9(b)", ALG, "2.3", 1, LATEX["09b"],
      [r"B1 (AO 2.2a): 1200 tonnes. Notes: " + TONNES + r"1200 tonnes or 1200 t."],
      False, 18),
    e("09c", "9(c)", ALG, "2.3", 2, LATEX["09c"],
      [r"M1 (AO 3.1a): Attempts $\left\{1200-3\times(5-20)^2\right\}-\left\{1200-3\times(4-20)^2\right\}$. Notes: "
       r"Attempts $T_5-T_4=\left\{1200-3\times(5-20)^2\right\}-\left\{1200-3\times(4-20)^2\right\}$ May be implied by "
       r"$525-432$. Condone for this mark an attempt at "
       r"$T_4-T_3=\left\{1200-3\times(4-20)^2\right\}-\left\{1200-3\times(3-20)^2\right\}$",
       r"A1 (AO 1.1b): 93 tonnes. Notes: " + TONNES + r"93 tonnes or 93 t"],
      False, 18),
    e("09d", "9(d)", ALG, "2.3", 2, LATEX["09d"],
      [r"B1 (AO 3.5b): States the model is only valid for values of $n$ such that $n\leqslant20$. Notes: For one mark: "
       r"shows an appreciation of the model: states $n\leqslant20$ or $n<20$; condone for one mark $n\leqslant40$ or "
       r"$n<40$ with “the mass of tin mined cannot be negative” oe; condone for one mark $n=40$ with a statement that "
       r"“the mass of tin mined becomes 0” oe; after 20 years the (total) amount of tin mined starts to go down ($n$ "
       r"may not be mentioned and total may be missing); after 20 years the (total) mass reaches a maximum value. "
       r"(Similar to above); states $T_{max}$ is reached when $n=20$",
       r"B1 (AO 2.3): States that the total amount mined cannot decrease. Notes: For two marks: states the limitation "
       r"on $n$ and explains fully. (Total mass, not mass must be used): states that $n\leqslant20$ and explains that "
       r"the total mass of tin cannot decrease; $0<n\leqslant20$ as the maximum total amount of tin mined is reached at "
       r"20 years",
       r"ALT: Alternatively (d), for two marks — B1 B1: Alternatively states that $n$ cannot be more than 20 and the "
       r"total mass of tin would be decreasing"],
      False, 18),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", COORD, "3.2, 2.3", 3,
      LATEX["10a"],
      [r"M1 (AO 1.1b): Attempts $(x-2)^2+(y+4)^2-4-16-8=0$. Notes: Attempts to complete the square. Look for "
       r"$(x\pm2)^2+(y\pm4)^2\ldots$ If a candidate attempts to use $x^2+y^2+2gx+2fy+c=0$ then it may be awarded for "
       r"a centre of $(\pm2,\pm4)$ Condone $a=\pm2, b=\pm4$",
       r"A1 (AO 1.1b): (i) Centre $(2,-4)$. Notes: Centre $(2,-4)$ This may be written separately as $x=2, y=-4$ BUT "
       r"$a=2, b=-4$ is A0",
       r"A1 (AO 1.1b): (ii) Radius $\sqrt{28}$ oe Eg $2\sqrt{7}$. Notes: Radius $\sqrt{28}$ or $2\sqrt{7}$ isw after a "
       r"correct answer"],
      False, 22),
    e("10b", "10(b)", COORD, "3.2", 2,
      LATEX["10b"],
      [r"M1 (AO 3.1a): Attempts to add/subtract '$r$' from '2' (beside a sketch of the circle, centre $(2,-4)$, with "
       r"vertical tangents). Notes: Attempts to add or subtract their radius from their 2.",
       r"A1ft (AO 1.1b): $k=2\pm\sqrt{28}$. Notes: $k=2+\sqrt{28}$ and $k=2-\sqrt{28}$ Follow through on their 2 and "
       r"their $\sqrt{28}$. If decimals are used the values must be calculated. Eg $k=2\pm5.29\to k=7.29, k=-3.29$. "
       r"Accept just $2\pm\sqrt{28}$ or equivalent such as $2\pm2\sqrt{7}$. Condone $x=2+\sqrt{28}$ and "
       r"$x=2-\sqrt{28}$ but not $y=2+\sqrt{28}$ and $y=2-\sqrt{28}$",
       r"ALT: Alternatively (b) — M1: Alternatively substitutes $y=-4$ into circle equation and finds $x/k$ by solving "
       r"the quadratic equation by a suitable method.",
       r"ALT: A third (and more difficult) method (b) — M1: Substitute $x=k$ into the equation to form a quadratic eqn "
       r"in $y\Rightarrow y^2+8y+k^2-4k-8=0$ and use the fact that this would have one root. E.g. "
       r"$b^2-4ac=0\Rightarrow64-4(k^2-4k-8)=0\Rightarrow k=\ldots$ Condone slips but the method must be sound."],
      False, 22),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", ALG, "2.6", 2, LATEX["11a"],
      [r"M1 (AO 1.1b): Attempts $\mathrm{f}(4)=2\times4^3-13\times4^2+8\times4+48$. Notes: Attempts to calculate "
       r"$\mathrm{f}(4)$. Do not accept $\mathrm{f}(4)=0$ without sight of embedded values or calculations. If values "
       r"are not embedded look for two correct terms from $\mathrm{f}(4)=128-208+32+48$",
       r"A1 (AO 1.1b): $\mathrm{f}(4)=0\Rightarrow(x-4)$ is a factor. Notes: Correct reason with conclusion. Accept "
       r"$\mathrm{f}(4)=0$, hence factor as long as M1 has been scored. This should really be stated on one line after "
       r"having performed a correct calculation. It could appear as a preamble if the candidate states “If "
       r"$\mathrm{f}(4)=0$, then $(x-4)$ is a factor before doing the calculation and then writing hence proven or ✓ "
       r"oe. If division/inspection is attempted it must be correct and there must be some attempt to explain why they "
       r"have shown that $(x-4)$ is a factor. Eg Via division they must state that there is no remainder, hence factor",
       r"ALT: Alternatively (a), division — M1: Alternatively attempts to divide by $(x-4)$. Accept via long division "
       r"or inspection. See below for awarding these marks."],
      False, 24),
    e("11b", "11(b)", ALG, "2.6", 4,
      LATEX["11b"],
      [r"M1 (AO 2.1): $2x^3-13x^2+8x+48=(x-4)(2x^2\ldots x-12)$. Notes: Attempts to find the quadratic factor by "
       r"inspection (correct first and last terms) or by division (correct first two terms). So for inspection award "
       r"for $2x^3-13x^2+8x+48=(x-4)(2x^2\ldots x\pm12)$. For division look for $2x^2-5x$ in the quotient, with "
       r"$2x^3-8x^2$ and $-5x^2$ in the working",
       r"A1 (AO 1.1b): $=(x-4)(2x^2-5x-12)$. Notes: Correct quadratic factor $(2x^2-5x-12)$ For division award for "
       r"sight of this “in the correct place” You don't have to see it paired with the $(x-4)$ for this mark. If a "
       r"student has used division in part (a) they can score the M1 A1 in (b) as soon as they start attempting to "
       r"factorise their $(2x^2-5x-12)$.",
       r"dM1 (AO 1.1b): Attempts to factorise quadratic factor or solve quadratic eqn. Notes: Correct attempt to solve "
       r"or factorise their $(2x^2-5x-12)$ including use of formula. Apply the usual rules $(2x^2-5x-12)=(ax+b)(cx+d)$ "
       r"where $ac=\pm2$ and $bd=\pm12$. Allow the candidate to move from $(x-4)(2x^2-5x-12)$ to $(x-4)^2(2x+3)$ for "
       r"this mark.",
       r"A1 (AO 2.4): $\mathrm{f}(x)=(x-4)^2(2x+3)\Rightarrow\mathrm{f}(x)=0$ has only two roots, 4 and $-1.5$. Notes: "
       r"Via factorisation: factorises twice to $\mathrm{f}(x)=(x-4)(2x+3)(x-4)$ or $\mathrm{f}(x)=(x-4)^2(2x+3)$ or "
       r"$\mathrm{f}(x)=2(x-4)^2\left(x+\frac{3}{2}\right)$ followed by a valid explanation why there are only two "
       r"roots. The explanation can be as simple as: hence $x=4$ and $-\frac{3}{2}$ (only). The roots must be correct; "
       r"only two distinct roots as 4 is a repeated root. There must be some understanding between roots and factors. "
       r"E.g. $\mathrm{f}(x)=(x-4)^2(2x+3)$ [arrows pointing to the two factors] only two distinct roots is "
       r"insufficient. This would require two distinct factors, so there are two distinct roots. Via solving: "
       r"factorises to $(x-4)(2x^2-5x-12)$ and solves $2x^2-5x-12=0\Rightarrow x=4,-\frac{3}{2}$ followed by an "
       r"explanation that the roots are $4,4,-\frac{3}{2}$ so only two distinct roots. Note that this question asks "
       r"the candidate to use algebra so you cannot accept any attempt to use their calculators to produce the answers."],
      False, 24),
    e("11c", "11(c)", ALG, "2.8, 2.7", 2,
      LATEX["11c"],
      [r"M1 (AO 2.2a): Deduces either three roots or deduces that $\mathrm{f}(x)$ is moved down two units. Notes: For a "
       r"valid deduction. Accept either there are 3 roots or states that it is a solution of $\mathrm{f}(x)=2$ or "
       r"$\mathrm{f}(x)-2=0$",
       r"A1 (AO 2.4): States three roots, as when $\mathrm{f}(x)$ is moved down two units there will be three points of "
       r"intersection (with the $x$-axis). Notes: Fully explains: Eg. States three roots, as $\mathrm{f}(x)$ is moved "
       r"down by two units (giving three points of intersection with the $x$-axis). Eg. States three roots, as it is "
       r"where $\mathrm{f}(x)=2$ (You may see $y=2$ drawn on the diagram)"],
      True, 24),
    e("11d", "11(d)", ALG, "2.8", 2,
      LATEX["11d"],
      [r"M1 (AO 1.1b): For sight of $k=\pm4,\pm\frac{3}{2}$. Notes: For sight of $\pm4$ and $\pm\frac{3}{2}$ Follow "
       r"through on $\pm$ their roots.",
       r"A1ft (AO 1.1b): $k=4,-\frac{3}{2}$. Notes: $k=4,-\frac{3}{2}$ Follow through on their roots. Accept "
       r"$4,-\frac{3}{2}$ but not $x=4,-\frac{3}{2}$"],
      True, 24),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", TRIG, "5.3", 4, LATEX["12a"],
      [r"M1 (AO 1.1b): $\frac{10\sin^2\theta-7\cos\theta+2}{3+2\cos\theta}\equiv"
       r"\frac{10(1-\cos^2\theta)-7\cos\theta+2}{3+2\cos\theta}$. Notes: Uses the identity $\sin^2\theta=1-\cos^2\theta$ "
       r"within the fraction",
       r"A1 (AO 1.1b): $\equiv\frac{12-7\cos\theta-10\cos^2\theta}{3+2\cos\theta}$. Notes: Correct (simplified) "
       r"expression in just $\cos\theta$: $\frac{12-7\cos\theta-10\cos^2\theta}{3+2\cos\theta}$ or exact equivalent "
       r"such as $\frac{(3+2\cos\theta)(4-5\cos\theta)}{3+2\cos\theta}$. Allow for $\frac{12-7u-10u^2}{3+2u}$ where "
       r"they introduce $u=\cos\theta$. We would condone mixed variables here.",
       r"M1 (AO 1.1b): $\equiv\frac{(3+2\cos\theta)(4-5\cos\theta)}{3+2\cos\theta}$. Notes: A correct attempt to "
       r"factorise the numerator, usual rules. Allow candidates to use $u=\cos\theta$ oe",
       r"A1* (AO 2.1): $\equiv4-5\cos\theta$ *. Notes: A fully correct proof with correct notation and no errors. Only "
       r"withhold the last mark for (1) Mixed variable e.g. $\theta$ and $x$'s (2) Poor notation "
       r"$\cos\theta^2\leftrightarrow\cos^2\theta$ or $\sin^2=1-\cos^2$ within the solution. Don't penalise incomplete "
       r"lines if it is obvious that it is just part of their working E.g. "
       r"$\frac{10\sin^2\theta-7\cos\theta+2}{3+2\cos\theta}\equiv10(1-\cos^2\theta)-7\cos\theta+2"
       r"=\frac{12-7\cos\theta-10\cos^2\theta}{3+2\cos\theta}$",
       r"ALT: Alternative proof in part (a) — M1: Multiplies across and form 3TQ in $\cos\theta$ on rhs "
       r"$10\sin^2\theta-7\cos\theta+2=(4-5\cos\theta)(3+2\cos\theta)\Rightarrow10\sin^2\theta-7\cos\theta+2"
       r"=A\cos^2\theta+B\cos\theta+C$",
       r"ALT: Alternative proof in part (a) — A1: Correct identity formed "
       r"$10\sin^2\theta-7\cos\theta+2=-10\cos^2\theta-7\cos\theta+12$",
       r"ALT: Alternative proof in part (a) — dM1: Uses $\cos^2\theta=1-\sin^2\theta$ on the rhs or "
       r"$\sin^2\theta=1-\cos^2\theta$ on the lhs. Alternatively proceeds to $10\sin^2\theta+10\cos^2\theta=10$ and "
       r"makes a statement about $\sin^2\theta+\cos^2\theta=1$ oe",
       r"ALT: Alternative proof in part (a) — A1*: Shows that "
       r"$(4-5\cos\theta)(3+2\cos\theta)\equiv10\sin^2\theta-7\cos\theta+2$ oe AND makes a minimal statement "
       r"“hence true”"],
      False, 28),
    e("12b", "12(b)", TRIG, "5.4, 5.3", 3,
      LATEX["12b"],
      [r"M1 (AO 2.1): $4+3\sin x=4-5\cos x\Rightarrow\tan x=-\frac{5}{3}$. Notes: Attempts to use part (a) and "
       r"proceeds to an equation of the form $\tan x=k$, $k\neq0$. Condone $\theta\leftrightarrow x$. Do not condone "
       r"$a\tan x=0\Rightarrow\tan x=b\Rightarrow x=\ldots$",
       r"A1 (AO 1.1b): $x=$ awrt $121^\circ, 301^\circ$. Notes: Either $x=$ awrt $121^\circ$ or $301^\circ$. Condone "
       r"awrt 2.11 or 5.25 which are the radian solutions",
       r"A1 (AO 1.1b): $x=$ awrt $121^\circ, 301^\circ$. Notes: Both $x=$ awrt $121^\circ$ and $301^\circ$ and no other "
       r"solutions. Answers without working, or with no incorrect working in (b): Question states hence or otherwise so "
       r"allow for 3 marks both $x=$ awrt $121^\circ$ and $301^\circ$ and no other solutions. For 1 marks scored SC 100 "
       r"for either $x=$ awrt $121^\circ$ or $301^\circ$",
       r"ALT: Alternatively (b) — M1: Alternatively squares $3\sin x=-5\cos x$ and uses $\sin^2x=1-\cos^2x$ oe to reach "
       r"$\sin x=A, -1<A<1$ or $\cos x=B, -1<B<1$"],
      False, 28),

    # ---------------- Q13 ----------------
    e("13", "13", INT, "8.3, 7.3, 8.2", 7,
      LATEX["13"],
      [r"M1 (AO 3.1a): The overall method of finding the $x$ coordinate of $A$. Notes: An overall problem-solving "
       r"method mark to find the minimum point. To score this you need to see: an attempt to differentiate with at least "
       r"two correct terms; an attempt to set their $\frac{\mathrm{d}y}{\mathrm{d}x}=0$ and then solve to find $x$. "
       r"Don't be overly concerned by the mechanics of this solution",
       r"B1 (AO 1.1b): $y=2x^3-17x^2+40x\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}x}=6x^2-34x+40$. Notes: "
       r"$\left(\frac{\mathrm{d}y}{\mathrm{d}x}=\right)6x^2-34x+40$ which may be unsimplified",
       r"M1 (AO 1.1b): $\frac{\mathrm{d}y}{\mathrm{d}x}=0\Rightarrow6x^2-34x+40=0\Rightarrow2(3x-5)(x-4)=0\Rightarrow "
       r"x=\ldots$ Notes: Sets their $\frac{\mathrm{d}y}{\mathrm{d}x}=0$, which must be a 3TQ in $x$, and attempts to "
       r"solve via factorisation, formula or calculator. If a calculator is used to find the roots, they must be correct "
       r"for their quadratic. If $\frac{\mathrm{d}y}{\mathrm{d}x}$ is correct allow them to just choose the root 4 for "
       r"M1 A1. Condone $(x-4)\left(x-\frac{5}{3}\right)$",
       r"A1 (AO 3.2a): Chooses $x=4$ (with $x=\frac{5}{3}$ crossed out). Notes: Chooses $x=4$ This may be awarded from "
       r"the upper limit in their integral",
       r"B1 (AO 1.1b): $\int2x^3-17x^2+40x\,\mathrm{d}x=\left[\frac{1}{2}x^4-\frac{17}{3}x^3+20x^2\right]$. Notes: "
       r"$\int2x^3-17x^2+40x\,\mathrm{d}x=\left[\frac{1}{2}x^4-\frac{17}{3}x^3+20x^2\right]$ which may be unsimplified",
       r"M1 (AO 1.1b): Area $=\frac{1}{2}(4)^4-\frac{17}{3}(4)^3+20(4)^2$. Notes: Correct attempt at area. There may be "
       r"slips on the integration but expect two correct terms. The upper limit used must be their larger solution of "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}=0$ and the lower limit used must be 0. So if their roots are 6 and 10, then "
       r"they must use 10 and 0. If only one value is found then the limits must be 0 to that value. Expect to see "
       r"embedded or calculated values. Don't accept $\int_0^4 2x^3-17x^2+40x\,\mathrm{d}x=\frac{256}{3}$ without "
       r"seeing the integration and the embedded or calculated values",
       r"A1* (AO 2.1): $=\frac{256}{3}$ *. Notes: Area $=\frac{256}{3}$ with correct notation and no errors. Note that "
       r"this is a given answer. For correct notation expect to see: $\frac{\mathrm{d}y}{\mathrm{d}x}$ or "
       r"$\frac{\mathrm{d}}{\mathrm{d}x}$ used correctly at least once. If $\mathrm{f}(x)$ is used accept "
       r"$\mathrm{f}'(x)$. Condone $y'$; $\int2x^3-17x^2+40x\,\mathrm{d}x$ used correctly at least once with or "
       r"without the limits."],
      True, 32),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", EXP, "6.7", 1, LATEX["14a"],
      [r"B1 (AO 3.4): (£)18 000. Notes: £18 000 There is no requirement to have the units"],
      False, 36),
    e("14b", "14(b)", EXP, "6.2, 6.3, 6.7", 6,
      LATEX["14b"],
      [r"M1 (AO 3.1b): (i) $\frac{\mathrm{d}V}{\mathrm{d}t}=-3925\mathrm{e}^{-0.25t}$. Notes: Award for making the "
       r"link between gradient and rate of change. Score for attempting to differentiate $V$ to "
       r"$\frac{\mathrm{d}V}{\mathrm{d}t}=k\mathrm{e}^{-0.25t}$ An attempt at both sides are required. For the left "
       r"hand side you may condone attempts such as $\frac{\mathrm{d}y}{\mathrm{d}x}$",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}V}{\mathrm{d}t}=-3925\mathrm{e}^{-0.25t}$. Notes: Achieves "
       r"$\frac{\mathrm{d}V}{\mathrm{d}t}=-3925\mathrm{e}^{-0.25t}$ or "
       r"$\frac{\mathrm{d}V}{\mathrm{d}t}=15700\times-0.25\mathrm{e}^{-0.25t}$ with both sides correct",
       r"A1* (AO 3.4): Sets $-3925\mathrm{e}^{-0.25T}=-500\Rightarrow3925\mathrm{e}^{-0.25T}=500$ * cso. Notes: Sets "
       r"$-3925\mathrm{e}^{-0.25T}=-500$ oe and proceeds to $3925\mathrm{e}^{-0.25T}=500$ This is a given answer and to "
       r"achieve this mark, all aspects must be seen and be correct. $t$ must be changed to $T$ at some point even if "
       r"just at the end of their solution/proof. SC: Award SC 110 candidates who simply write "
       r"$-3925\mathrm{e}^{-0.25T}=-500\Rightarrow3925\mathrm{e}^{-0.25T}=500$ without any mention or reference to "
       r"$\frac{\mathrm{d}V}{\mathrm{d}t}$ Or $15700\times-0.25\mathrm{e}^{-0.25t}=-500\Rightarrow"
       r"3925\mathrm{e}^{-0.25T}=500$ without any mention or reference to $\frac{\mathrm{d}V}{\mathrm{d}t}$",
       r"M1 (AO 1.1b): (ii) $\mathrm{e}^{-0.25T}=0.127\ldots\Rightarrow-0.25T=\ln0.127\ldots$ Notes: Proceeds from "
       r"$\mathrm{e}^{-0.25T}=A, A>0$ using ln's to $\pm0.25T=\ldots$ but "
       r"$3925\mathrm{e}^{-0.25T}=500\Rightarrow\ln3925\times-0.25T=\ln500\Rightarrow\pm0.25T=\ldots$ is M0",
       r"A1 (AO 1.1b): $T=8.24$ (awrt). Notes: $T=$ awrt 8.24 or $-\frac{1}{0.25}\ln\left(\frac{20}{157}\right)$ Allow "
       r"$t=$ awrt 8.24",
       r"A1 (AO 3.2a): 8 years 3 months. Notes: 8 years 3 months. Correct answer and solution only. Answers obtained "
       r"numerically score 0 marks. The M mark must be scored.",
       r"ALT: Alternatively (b)(ii) — M1: Alternatively takes lns first "
       r"$3925\mathrm{e}^{-0.25T}=500\Rightarrow\ln3925-0.25T=\ln500\Rightarrow\pm0.25T=\ldots$"],
      False, 36),
    e("14c", "14(c)", EXP, "6.7, 6.1", 1, LATEX["14c"],
      [r"B1 (AO 1.1b): 2 300. Notes: 2 300 but condone £2 300"],
      False, 36),
    e("14d", "14(d)", EXP, "6.7", 1, LATEX["14d"],
      [r"B1 (AO 3.5b): Any suitable reason such as: other factors affect price such as condition/mileage; if the car "
       r"has had an accident it will be worth less than the model predicts; the price may go up in the long term as it "
       r"becomes rare; £2300 is too large a value for a car's scrap price. Most cars scrap for around £400. Notes: Any "
       r"suitable reason. See scheme. Accept “Scrappage” schemes may pay more (or less) than £2 300. Do not accept "
       r"“does not take into account inflation”. It asks for a limitation of the model so candidates cannot score "
       r"marks by suggesting other suitable models “the value may fall by the same amount each year”"],
      False, 36),

    # ---------------- Q15 ----------------
    e("15", "15", "Proof", "1.1", 4, LATEX["15"],
      [r"M1 (AO 2.1): (If $n$ is even,) $n=2k$ and $n^3+2=(2k)^3+2=8k^3+2$. Notes: Score as below so M0 A0 M1 A1 or "
       r"M1 A0 M1 A1 are not possible. M1: Suitable approach to answer the question for $n$ being even OR odd. There is "
       r"no merit in a student taking values, or multiple values, of $n$ and then drawing conclusions. So "
       r"$n=5\Rightarrow n^3+2=127$ which is not a multiple of 8 scores no marks; student using divided when they mean "
       r"divisible. Eg. “Odd numbers cannot be divided by 8” is incorrect. We need to see either “odd numbers are "
       r"not divisible by 8” or “odd numbers cannot be divided by 8 exactly”; stating "
       r"$\frac{n^3+2}{8}=\frac{1}{8}n^3+\frac{1}{4}$ which is not a whole number; stating "
       r"$\frac{(n+1)^3+2}{8}=\frac{1}{8}n^3+\frac{3}{8}n^2+\frac{3}{8}n+\frac{3}{8}$ which is not a whole number. There "
       r"must be an attempt to generalise either logic or algebra. Correct expressions are required for the M's. There "
       r"is no need to state “If $n$ is even,” $n=2k$ and “If $n$ is odd,” $n=2k+1$ for the two M's as the "
       r"expressions encompass all numbers. However the concluding statement must attempt to show that it has been "
       r"proven for all $n\in\mathbb{N}$. Some students will use $2k-1$ for odd numbers. There is no requirement to "
       r"change the variable. They may use $2n$ and $2n\pm1$",
       r"A1 (AO 2.2a): Eg. 'This is 2 more than a multiple of 8, hence not divisible by 8' Or 'as $8k^3$ is divisible "
       r"by 8, $8k^3+2$ isn't'. Notes: A1: Acceptable proof for $n$ being even OR odd. Reasons must be correct. Don't "
       r"accept $8k^3+2$ cannot be divided by 8 for example. (It can!)",
       r"M1 (AO 2.1): (If $n$ is odd,) $n=2k+1$ and $n^3+2=(2k+1)^3+2$. Notes: M1: Suitable approach to answer the "
       r"question for $n$ being even AND odd",
       r"A1 (AO 2.2a): $=8k^3+12k^2+6k+3$ which is an even number add 3, therefore odd. Hence it is not divisible by 8. "
       r"So (given $n\in\mathbb{N}$,) $n^3+2$ is not divisible by 8. Notes: A1: Acceptable proof for $n$ being even "
       r"AND odd WITH concluding statement.",
       r"ALT: Alt algebraic approach — M1 (AO 2.1): (If $n$ is even,) $n=2k$ and "
       r"$\frac{n^3+2}{8}=\frac{(2k)^3+2}{8}=\frac{8k^3+2}{8}$",
       r"ALT: Alt algebraic approach — A1 (AO 2.2a): $=k^3+\frac{1}{4}$ oe which is not a whole number and hence not "
       r"divisible by 8",
       r"ALT: Alt algebraic approach — M1 (AO 2.1): (If $n$ is odd,) $n=2k+1$ and $\frac{n^3+2}{8}=\frac{(2k+1)^3+2}{8}$",
       r"ALT: Alt algebraic approach — A1 (AO 2.2a): $=\frac{8k^3+12k^2+6k+3}{8}$ ** The numerator is odd as "
       r"$8k^3+12k^2+6k+3$ is an even number +3 hence not divisible by 8. So (Given $n\in\mathbb{N}$,) $n^3+2$ is not "
       r"divisible by 8. Notes: Also ** “$=k^3+\frac{3}{2}k^2+\frac{3}{4}k+\frac{3}{8}$ which is not whole number” "
       r"is too vague so A0",
       r"ALT: Logical approach (example in the mark scheme) — M1 (AO 2.1): States that if $n$ is odd, $n^3$ is odd. "
       r"Notes: First M1: States the result of cubing an odd or an even number",
       r"ALT: Logical approach — A1 (AO 2.2a): so $n^3+2$ is odd and therefore cannot be divisible by 8. Notes: First "
       r"A1: Followed by the result of adding two and gives a valid reason why it is not divisible by 8. So for odd "
       r"numbers accept for example “odd number + 2 is still odd and odd numbers are not divisible by 8”, “$n^3+2$ "
       r"is odd and cannot be divided by 8 exactly” and for even numbers accept “a multiple of 8 add 2 is not a "
       r"multiple of 8, so $n^3+2$ is not divisible by 8”, “if $n^3$ is a multiple of 8 then $n^3+2$ cannot be "
       r"divisible by 8”",
       r"ALT: Logical approach — M1 (AO 2.1): States that if $n$ is even, $n^3$ is a multiple of 8. Notes: Second M1: "
       r"States the result of cubing an odd and an even number",
       r"ALT: Logical approach — A1 (AO 2.2a): so $n^3+2$ cannot be a multiple of 8. So (Given $n\in\mathbb{N}$), "
       r"$n^3+2$ is not divisible by 8. Notes: Second A1: Both valid reasons must be given followed by a concluding "
       r"statement."],
      False, 40),

    # ---------------- Q16 ----------------
    e("16i", "16(i)", "Vectors", "9.3", 1,
      LATEX["16i"],
      [r"B1 (AO 2.4): Explains that $\mathbf{a}$ and $\mathbf{b}$ lie in the same direction oe. Notes: Accept any valid "
       r"response E.g The lines are collinear. Condone “They are parallel” Mark positively. ISW after a correct "
       r"answer. Do not accept “the length of line a +b is the same as the length of line a + the length of line b”. "
       r"Do not accept $|\mathbf{a}|$ and $|\mathbf{b}|$ are parallel."],
      False, 42),
    e("16ii", "16(ii)", "Vectors", "9.5, 9.2, 5.1", 4,
      LATEX["16ii"],
      [r"M1 (AO 1.1b): [Mark scheme diagrams: $\mathbf{m}$ and $\mathbf{n}$ drawn from one point with $30^\circ$ "
       r"between them; a triangle with sides $|\mathbf{m}|=3$, $-\mathbf{n}$ and $|\mathbf{m}-\mathbf{n}|=6$, with "
       r"$30^\circ$ marked between $\mathbf{m}$ and $-\mathbf{n}$.] Notes: A triangle showing 3, 6 and $30^\circ$ in the "
       r"correct positions. Look for 6 opposite $30^\circ$ with another side of 3. Condone the triangle not being obtuse "
       r"angled and not being to scale. Do not condone negative lengths in the tringle. This would automatically be M0",
       r"M1 (AO 3.1a): Attempts $\frac{\sin30^\circ}{6}=\frac{\sin\theta}{3}$. Notes: Correct sine rule statement with "
       r"the sides and angles in the correct positions. If a triangle is drawn then the angles and sides must be in the "
       r"correct positions. This is not dependent so allow recovery from negative lengths in the triangle. If the "
       r"candidate has not drawn a diagram then correct sine rule would be M1 M1. Do not accept calculations where the "
       r"sides have a negative length. Eg $\frac{\sin30^\circ}{6}=\frac{\sin\theta}{-3}$ is M0",
       r"A1 (AO 1.1b): $\theta=$ awrt $14.5^\circ$. Notes: $\theta=$ awrt $14.5^\circ$",
       r"A1 (AO 3.2a): Angle between vector $\mathbf{m}$ and vector $\mathbf{m}-\mathbf{n}$ is awrt $135.5^\circ$. "
       r"Notes: CSO awrt $135.5^\circ$"],
      False, 42),
]

# Examiner report, sentence by sentence, in report order.
#   (None, text)              about the whole question -> every part
#   ({"a"}, text)             about part (a) only; {"b", "c"} for both
#   (parts, text, {"ref": True})        refers back to the sentence before
#   (parts, text, {"ref": "Opening words"})  refers back to that earlier sentence
#   (parts, text, {"ref": False})       contains this/it/these/... but doesn't refer back
# Bulleted lists are joined into the sentence that introduces them, with "; ".
# A sentence that mentions another part only in passing (e.g. "their result
# from part (a)") is tagged with the part it is about.
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "This question was generally well answered."),
        ({"a"}, r"(a) Most candidates attempted to rearrange the equation of $l_1$ into the form $y=mx+c$, with only a "
                r"small minority stating that the gradient was 2."),
        ({"a"}, "In a few cases a sign error crept in when the terms in the original equation were rearranged."),
        ({"a"}, "Most candidates attempted the negative reciprocal, although a significant minority failed to change "
                "the sign."),
        ({"a"}, r"Relatively few candidates lost a mark by leaving the gradient unsimplified (as $\frac{4}{2}$)."),
        ({"b"}, r"(b) Marks were lost owing to slips in the rearrangement of the equation of $l_1$ by either a sign "
                r"error or, more frequently, a failure to divide the constant by 4."),
        ({"b"}, r"Most candidates attempted to equate two equations rather than substituting their $y=2x+7$ into the "
                r"original equation."),
        ({"b"}, r"Sign errors, particularly with the constant, were a frequent cause of lost marks as the candidates "
                r"attempted to solve their equation for $x$."),
        ({"b"}, r"Many candidates continued, unnecessarily, to find the $y$-coordinate."),
        ({"b"}, "A few candidates, who erroneously had parallel lines, still tried to find a point of intersection."),
    ],
    "02": [
        ({"i"}, r"(i) Many candidates approached this question well and were able to manipulate the indices correctly "
                r"to achieve $a=0.25$."),
        ({"i"}, r"Several candidates who derived a fractional index of $x$ on one side of the equation were unable to "
                r"successfully ‘undo’ the index e.g. $x^{3/2}=k$ often became $x=\sqrt{k^3}$."),
        ({"i"}, r"Few managed to deduce $a=0$ due to cancelling a factor of $a$ instead of factorising it out.", NO),
        ({"i"}, "Many candidates squared both sides of the given equation to have integer indices, though they "
                "frequently did not square the coefficients as well."),
        ({"i"}, "Depending on how they processed their equation was key to whether they got both solutions."),
        ({"i"}, "Those who factorised or used calculator methods to solve the quartic equation were more likely to "
                "get both solutions.", NO),
        ({"i", "ii"}, r"A significant number of candidates displayed very poor algebra skills when attempting to "
                      r"isolate $a$ in this part and for the most part the same candidates also tackled (ii) poorly."),
        ({"ii"}, r"(ii) Many candidates were able to spot the quadratic equation in $b^2$ which then led to correct "
                 r"factorising and the elimination of the imaginary solutions."),
        ({"ii"}, r"Reasons for losing marks were: giving only $+\sqrt{2}$, instead of the full solution $\pm\sqrt{2}$; "
                 r"including the imaginary solutions $\pm3i$ so losing the final mark; solving the equation using "
                 r"their calculator, a method forbidden by the question."),
    ],
    "03": [
        ({"a"}, r"In part (a) the majority of candidates found this part straightforward, although the omission of "
                r"$+c$ remains a common flaw."),
        ({"a"}, "Errors tended to lie with the first term; the minus sign was almost always present but the "
                "coefficient was sometimes left unsimplified or the index ‘increased’ to 4."),
        ({"b"}, r"In part (b) most candidates were able to substitute the correct limits into their result from part "
                r"(a) in an attempt to find $k$ from the resulting linear equation."),
        ({"b"}, r"Common errors in part (b) consisted of a lack of bracketing when substituting in 0.5; equating their "
                r"integrated expression equal to 0; algebraic slips in solving their linear equation in $k$."),
    ],
    "04": [
        (W, "This was a relatively straightforward question, but the success of candidates tended to be centre "
            "dependent, due to it being one of the newer aspects of the specification.", NO),
        ({"a"}, r"In (a), candidates used a variety of successful methods to gain all three marks: the most commonly "
                r"seen method involved using the given values to, first find the gradient, and then one of the "
                r"straight-line graph forms to arrive at $H=mt+c$."),
        ({"a"}, r"Other methods included formation of simultaneous equations in $m$ and $c$ which could be solved in a "
                r"variety of ways."),
        ({"a"}, r"The words ‘Using a linear model’, however, led some candidates to make the erroneous assumption of "
                r"$H=at^b$ or $H=a(b^t)$."),
        ({"b"}, "In part (b), most candidates achieving a linear model in (a) were able to recognise that the tree’s "
                "initial height, (consistent with their equation), was the value of ‘c’ in their linear model."),
        ({"b"}, "The second mark was for a convincing statement suggesting that the values of 1.42m and 1.4m were "
                "similar and therefore supported the model."),
        ({"b"}, "This mark was often lost due to lack of the correct deduction, or by thinking that these two values "
                "needed to be exactly the same and so rejecting the model.", BACK),
    ],
    "05": [
        ({"a"}, "Almost all candidates were able to access some of the marks available in this question with many "
                "gaining full marks in (a)."),
        ({"b"}, "However, (b) was done with much less confidence with many candidates making little or no attempt.",
         BACK),
        ({"a"}, r"(a) The majority of candidates achieved the first two marks (for the $6x$), with very few integrating "
                r"instead of differentiating."),
        ({"a"}, r"Common errors with the $\frac{24}{x}$ term included rewriting the term as $+24x$ or $24x^{1/2}$ "
                r"before differentiating."),
        ({"a"}, r"A few wrote the term correctly as $24x^{-1}$ but differentiated to $-24$."),
        ({"b"}, r"(b) Some candidates seemed unfamiliar with what was meant by an increasing function and did not "
                r"attempt to use $\frac{\mathrm{d}y}{\mathrm{d}x}>0$."),
        ({"b"}, r"Common incorrect attempts included finding $\frac{\mathrm{d}^2y}{\mathrm{d}x^2}$ or treating the "
                r"original function as a quadratic with attempts to complete the square or find the discriminant."),
        ({"b"}, r"Of those who constructed the correct inequality, a number lacked the algebraic manipulation skills to "
                r"deal with inequalities with both positive and negative powers of $x$.", NO),
        ({"b"}, "Candidates should ensure they provide answers in the form requested by the question."),
        ({"b"}, "It was very common to see final answers given as rounded decimals only, when an exact answer was "
                "required.", NO),
    ],
    "06": [
        ({"a", "b"}, "This question was accessible to the vast majority of candidates, most of whom were able to, at "
                     "the least, make a start in both part a) and part b)."),
        ({"a"}, "In part a), most candidates could recall the correct formula for the area of a triangle."),
        ({"a"}, r"After a correct initial statement for the area of the triangle, a number of candidates lost a factor "
                r"of $x$, simplifying $\frac{1}{2}.2x.3x$ to $3x$ thus obtaining a linear equation in $x$ rather than "
                r"a quadratic."),
        ({"a"}, "The rigour demanded in a ‘show that’ question tended to cost some candidates marks when they failed "
                "to demonstrate the individual steps in their calculations."),
        ({"a"}, r"In particular, it was quite common for candidates to fail to demonstrate that they had used "
                r"$\sin60^\circ=\frac{\sqrt{3}}{2}$ within their calculation.", NO),
        ({"a"}, "Candidates should be made aware that for questions such as these where they are asked to ‘show "
                "that’, it is imperative that they demonstrate each step of their method on paper.", NO),
        ({"a", "b"}, "Part b) tended to be less problematic and candidates were often more successful here than in "
                     "part a)."),
        ({"b"}, "The vast majority of candidates were able to correctly quote and use the cosine rule."),
        ({"b"}, r"Occasionally, candidates became confused with the side lengths and errors arose in the substitution "
                r"of $x$ into the cosine formula."),
        ({"b"}, r"Other errors arose in the squaring, sometimes $(3\times2\sqrt{3})^2$ became $3(2\sqrt{3})^2$ for "
                r"example."),
        ({"b"}, r"Finally, and worryingly, a very common mistake was not knowing about ‘order of operations’ with "
                r"$156-144\cos60^\circ=12\cos60^\circ$ frequently seen"),
    ],
    "07": [
        ({"a", "b", "c"}, "In general, parts (a) and (b) were well done with part (c) causing some issues."),
        ({"a"}, "(a) There were many well drawn sketches with the correct equation of the asymptote either stated on "
                "the graph or below it.", NO),
        ({"a"}, r"A common mistake was for the lower branch not to cross the $x$-axis, thus demonstrating a lack of "
                r"understanding of the relevance of the asymptote (in effect $y=0$ became another asymptote)."),
        ({"a"}, "One observation from part (a) is that many candidates ignored the blank section of the paper and "
                "attempted to draw their graph on the line page."),
        ({"a"}, r"Whilst this is not an issue, too many candidates failed to use a ruler and had dubiously shaped "
                r"curves, often curving away from the asymptotes for larger values of $x$ and $y$.", BACK),
        ({"b"}, "(b) This part was answered well, and most candidates, realising that a proof was required, took care "
                "over their presentation and showed all their steps."),
        ({"b"}, r"A few lost the final mark for failing to show how they had multiplied by $x$, or for small algebraic "
                r"errors."),
        ({"c"}, r"(c) Candidates who identified the link between the discriminant and the fact that $l$ was a tangent, "
                r"generally secured full marks."),
        ({"c"}, "Those who attempted the alternative method of completing the square were often defeated by the "
                "algebra.", NO),
        ({"c"}, "Attempts using differentiation tended not to gain any credit."),
    ],
    "08": [
        ({"a"}, "This question was generally well answered with many candidates scoring full marks in part (a)."),
        ({"a"}, "Candidates had been clearly well rehearsed with binomial expansion and were able to make an attempt "
                "at applying the correct technique."),
        ({"a"}, r"For those that had some success with the question, the ‘64’ to score B1 was almost always seen, as "
                r"was the ‘$144x$’.", NO),
        ({"a"}, r"The most common mistake was with ‘$135x^2$’, with many candidates not including the coefficient of "
                r"$x$ when squaring and using $\frac{3x^2}{4}$ instead of $\frac{9x^2}{16}$."),
        ({"a"}, "Seeing more than three terms calculated was rare."),
        ({"a"}, "Occasionally candidates did not sum the terms, but this was condoned for the question.", NO),
        ({"a"}, "Finally, there were some candidates who failed to simplify their expressions fully, which was "
                "penalised in the final accuracy mark."),
        ({"b"}, "In part (b) candidates had less success."),
        ({"b"}, r"While the vast majority had some idea what to do, frequently the language used was unclear and "
                r"candidates did not always fully explain what to do, often omitting the detail of substituting the "
                r"value of $x$ into their binomial expansion."),
        ({"b"}, "Ambiguous phrasing, such as, “substituted into the previous equation” was penalised here.", NO),
        ({"b"}, r"Many candidates went beyond the requirements of the question and calculated $x$, with some going "
                r"further and substituted their value in to the binomial expansion."),
        ({"b"}, r"As usual, a common misconception was to let $x=1.925$ and substitute it into the expansion.", NO),
    ],
    "09": [
        (W, "Most were able to attempt this question, but lack of units cost a significant minority a mark."),
        ({"a"}, "(a) All but the weakest candidates produced a correct value."),
        ({"b"}, "(b) Again, the majority of candidates found this value."),
        ({"b"}, "However, many did not appreciate the form of the given equation and embarked on differentiation, "
                "thus expending much effort for a single mark."),
        ({"c"}, r"(c) Most candidates could not distinguish between ‘in 2023’ and ‘up to the end of 2023’ and offered "
                r"432 as their final answer (from $n=4$)."),
        ({"c"}, r"Those who had some understanding of the requirement of the question were about equally split "
                r"between the correct $T_5-T_4$ (= 93) and $T_4-T_3$ (= 99).", NO),
        ({"d"}, "(d) Whilst some candidates realised the model could not work after 20 years (or 40), most could not "
                "explain why."),
        ({"d"}, r"The second mark was rarely awarded as candidates failed to appreciate that it was the total mass "
                r"mined ($T$) that could not decrease.", NO),
        ({"d"}, "Many responses commented on the context of the question rather than the model and went on to discuss "
                "the logistics of mining and how the tin might or might not run out over time."),
    ],
    "10": [
        ({"a"}, "(a) This was generally answered successfully with candidates able to complete the square and set "
                "the equation in the correct format.", NO),
        ({"a"}, r"Usual numerical errors when manipulating equation led to sign errors and a wrong value for $r^2$."),
        ({"b"}, "(b) Candidates need to use the marks available as a guide to how much work they need to be doing."),
        ({"b"}, r"The most common error was to fail to recognise that $x=k$ is a vertical straight line."),
        ({"b"}, r"Those who sketched a diagram were able to deduce the values of $k$ by adding and subtracting their "
                r"radius from the centre’s $x$-coordinate.", NO),
        ({"b"}, r"However many, many candidates opted to equate the line $x=k$ with the circle equation using "
                r"substitution which led to a complicated manipulation and use of the discriminant to achieve their "
                r"final answer."),
        ({"b"}, "Of those who attempted this method, few were successful with most abandoning their method before "
                "reaching a conclusion.", BACK),
    ],
    "11": [
        (W, "As a general point, it is worth noting that a good examination technique is to look at the mark "
            "allocation in a question.", NO),
        ({"b", "c", "d"}, "Some candidates submitted virtually no work in part (b) where there were 4 marks, yet "
                          "produced half a page of work in (c) or (d) which had an allocation of just 2 marks."),
        (W, "The number of marks allocated to any part of a question is a good hint to the depth and detail of work "
            "required."),
        ({"a"}, r"(a) Almost every candidate gained the first mark by either substituting $x=4$ into $\mathrm{f}(x)$ "
                r"and finding that $\mathrm{f}(4)=0$, or by dividing $\mathrm{f}(x)$ by $(x-4)$ and achieving a "
                r"remainder of 0."),
        ({"a"}, "However, in a proof, a conclusion is always required."),
        ({"a"}, r"Therefore, candidates were required to state that $(x-4)$ is a factor because $\mathrm{f}(4)=0$."),
        ({"a"}, "However, it was pleasing to note that many more did follow this protocol than in the preceding "
                "year.", BACK),
        ({"b"}, "(b) As in part (a), a ‘show that’ question always needs a concluding statement."),
        ({"b"}, "Most candidates were very adept in algebraic division and did so clearly and accurately gaining the "
                "first two marks."),
        ({"b"}, "The majority went on to factorise the 3TQ successfully."),
        ({"b"}, r"What too many candidates failed to do at this stage was to refer back to $\mathrm{f}(x)$, write it "
                r"out in its complete factorised form of $\mathrm{f}(x)=(x-4)(x-4)(2x+3)$, and then state that "
                r"because there was a repeated factor, the equation $\mathrm{f}(x)=0$ had only two roots.", BACK),
        ({"b"}, r"Confusion between roots and factors cost some candidates the final mark as they incorrectly referred "
                r"to $(x-4)$ as a root."),
        ({"b"}, r"Quite a few candidates found $b^2-4ac$ for the quadratic expression, stated that as it was $>0$ and "
                r"therefore two roots, clearly thinking that they had answered the question.", NO),
        ({"b"}, "There was also clear evidence of use of calculators to find the roots followed by an attempt to work "
                "backwards to obtain the factors; this was unacceptable.", NO),
        ({"c"}, "(c) Those who noticed that the value of the constant had changed from 48 to 46 recognised that the "
                "new equation had three roots.", NO),
        ({"c"}, r"Only a few went on to explain that $\mathrm{f}(x)$ had been transformed by the vector "
                r"$\begin{pmatrix}0\\-2\end{pmatrix}$, or even just 2 places downwards cutting the $x$-axis in three "
                r"places."),
        ({"c"}, r"A large number of candidates did not spot the difference between the equation in (c) and "
                r"$\mathrm{f}(x)=0$ and many of those merely explained what they had done in (b).", NO),
        ({"d"}, "(d) This part of the question was generally either missed out entirely, or else the correct answer "
                "was given."),
        ({"d"}, "Infact quite a few candidates, who had scored only a few marks in parts (a) (b) and (c) combined, "
                "achieved both marks here."),
    ],
    "12": [
        ({"a"}, "(a) This was a straightforward proof.", NO),
        ({"a"}, r"Most candidates recognised the need to use $\sin^2\theta+\cos^2\theta=1$ but there were many "
                r"instances where $10\sin^2\theta$ became $10-\cos^2\theta$ or the $7\cos\theta$ was adapted."),
        ({"a"}, r"There were many well written out proof however with few candidates being penalised marks for "
                r"incorrect notation eg cos for $\cos\theta$ or $\sin\theta^2$ for $\sin^2\theta$."),
        ({"b"}, "Part (b) was, on the other hand, very badly done."),
        ({"b"}, "Many candidates failed to heed the use of the word “Hence” and started again wasting valuable "
                "time."),
        ({"b"}, r"Of those who did use part (a) failed to have a reliable method of solving $4-5\cos x=4+3\sin x$ with "
                r"may failing to eliminate the 4's.", NO),
        ({"b"}, r"Of those who did reach $-5\cos x=3\sin x$ many had solutions that involved variations of "
                r"$-\frac{3}{5}\tan x=0$.", NO),
        ({"b"}, "Better candidates found the manipulation straightforward and proceeded to find both solutions "
                "without any difficulty."),
        (W, "As a result this question was an effective discriminator."),
    ],
    "13": [
        (W, "This was an open ended question, types of which are expected in the new specification.", NO),
        (W, "Almost all candidates were able to achieve some credit in this question."),
        (W, r"Poor notation (usually the omission of $\mathrm{d}x$ from the integral) caused many to forfeit the "
            r"final mark."),
        (W, "Some candidates seemed unaware that it was unacceptable to rely entirely on a calculator and that they "
            "needed to show detailed working in this “show that” question.", NO),
        (W, r"Many candidates attempted to integrate (usually correctly) but with no other work of any value, some "
            r"using 0 and $k$ as limits and some even showing the substitution of $k$ and 0 and subtracting."),
        (W, r"But without a value of $k$ found via differentiation, only the second B mark was available to them."),
        (W, r"Other candidates thought they could find $k$ by finding the roots of the original cubic despite it "
            r"being clear from the diagram that the origin was the only root.", NO),
        (W, r"Of those who realised differentiation was required, most arrived at $x=\frac{5}{3}, 4$.", NO),
        (W, r"Some of these candidates spotted from the graph that $k=4$, but many wasted time, either by finding the "
            r"corresponding $y$-coordinates (and using the $x$ value corresponding to the lower of these) or using "
            r"the second differential (where $\frac{\mathrm{d}^2y}{\mathrm{d}x^2}>0$) to determine which was $k$.",
         BACK),
        (W, r"A few candidates having found the second differential, equated this to zero and erroneously used the "
            r"resulting value as $k$.", NO),
        (W, r"Occasional mistakes with limits included using $\frac{5}{3}$ instead of 0 as the bottom limit and "
            r"subtracting the wrong way round (or even adding) after substituting."),
        (W, "Some candidates forfeited the final two marks for failing to show intermediate working."),
    ],
    "14": [
        ({"a", "c", "d"}, "In general parts (a), (c) and (d) were well attempted, with many scoring the three "
                          "available marks here and nothing else."),
        ({"a"}, "Part (a) was well answered by most."),
        ({"a"}, "It was rare to see any working out – just the correct answer stated.", NO),
        ({"a"}, "Very occasionally £2300 was seen here."),
        ({"b"}, "Part (b) was the part candidates found most challenging, and many left it completely blank.", NO),
        ({"b"}, "Of those that attempted part (i), most knew to multiply by 0.25, but many struggled to construct a "
                "sufficiently thorough explanation to support their work to arrive at the given equation.", NO),
        ({"b"}, "The most common mistake was getting confused by the negative sign."),
        ({"b"}, "Some candidates didn’t seem to have recognised that a decreasing rate of change would be negative, "
                "and quite often the negative sign was just ignored."),
        ({"b"}, r"Often the given equation was relied upon too heavily, with some appearing to work backwards – the "
                r"mark scheme required some evidence that they had differentiated, and as a result, many scored no "
                r"marks due to no reference to $\frac{\mathrm{d}V}{\mathrm{d}t}$ (or at least "
                r"$\frac{\mathrm{d}y}{\mathrm{d}x}$ for the first M1)."),
        ({"b"}, r"Occasionally candidates who had otherwise been successful here were not awarded the final accuracy "
                r"mark due to a failure to replace $t$ with $T$."),
        ({"b"}, "It was encouraging to see that even when candidates were unable to make progress with (b)(i), they "
                "frequently had a go at part (ii), often with some success.", NO),
        ({"b"}, "Candidates’ use of logarithms was broadly good, with only a few forgetting to divide by 3925 before "
                "introducing logs."),
        ({"b"}, r"If attempted, most were able to get to $T=8.24$."),
        ({"b"}, "There were several instances of this then being written as 8 years 2 months, instead of the correct "
                "8 years 3 months, but the majority of those got to the decimal answer were able to convert it "
                "successfully.", BACK),
        ({"c"}, "A good understanding of the exponential graph was clear in part (c) as the vast majority scored the "
                "mark here for (£)2300."),
        ({"c"}, "Occasionally 500 was seen here, perhaps misinterpreting the question."),
        ({"d"}, "Responses to (d) were many and varied."),
        ({"d"}, "Frequent correct answers included mentioning damage to the vehicle, variability in mileage, and the "
                "potential for the car to become an antique."),
        ({"d"}, "For those who weren’t awarded the mark the most popular responses were that it only made "
                "predictions based on year, not months or days, claiming the car’s value may not follow a linear "
                "pattern of decrease and predicting that the car’s value will eventually become zero.", NO),
    ],
    "15": [
        (W, "It was very rare to see a response worthy of full marks and many candidates made no attempt to answer "
            "this question.", NO),
        (W, "It was clear that this new aspect of the specification was not well known by candidates.", NO),
        (W, "It was expected that candidates would consider odd and even numbers separately using a logical or an "
            "algebraic approach as detailed in the mark scheme.", NO),
        (W, "Almost all the candidates who gained any marks used either approach, or even a mixture of both."),
        (W, r"Marks were commonly lost by: using $n$ (even) and $n+1$ (odd) which brought no success at all; failing "
            r"to appreciate the difference between “cannot be divided by 8” and “is not divisible by 8”; errors in the "
            r"expansion and simplification of $(2k+1)^3+2$; a lack of rigour in the explanation that "
            r"$8k^3+12k^2+6k+3$ is not divisible by 8; failing to write a concluding statement (for the final mark)"),
        (W, "There were also a few attempts at proof by contradiction, some of which were quite impressive, "
            "considering the more difficult nature of this approach."),
        (W, "Many embarked on a completely numerical approach (in some cases claiming to have demonstrated proof by "
            "exhaustion) and did not, of course, score any marks."),
    ],
    # The report calls the parts (a) and (b); the paper numbers them (i) and (ii).
    "16": [
        (W, "This was a poorly answered question at all levels.", NO),
        ({"i"}, "In part (a) it was expected that candidates would recognise the fact that the vectors would need to "
                "lie in the same direction but many attempted to write out the given expression in words.",
         {"ref": False, "note": "the paper numbers this part (i)"}),
        ({"ii"}, "There was slightly more success in part (b) with most attempting a diagram of sorts to get a feel "
                 "for the problem.", {"note": "the paper numbers this part (ii)"}),
        ({"ii"}, r"Unfortunately a lack of understanding of vectors meant that $|\mathbf{m}|=3$ and "
                 r"$|\mathbf{m}-\mathbf{n}|=6$ was usually followed by $|\mathbf{n}|=-3$."),
        (W, "There were however, some excellent and well thought out solutions showing a full understanding of the "
            "question,"),
    ],
}


def at(q, opening):
    """(question, index) of the one REPORT sentence for q starting with these words."""
    hits = [i for i, s in enumerate(REPORT[q]) if s[1].startswith(opening)]
    if len(hits) != 1:
        raise SystemExit(f"Q{q}: {opening!r} matches {len(hits)} sentences")
    return q, hits[0]


# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
RATINGS = {
    "01a": ("easy", at("01", "This question was generally well answered")),
    "01b": ("easy", at("01", "This question was generally well answered")),
    "02i": ("hard", at("02", "Few managed to deduce")),
    "02ii": ("medium", at("02", "(ii) Many candidates were able to spot")),
    "03a": ("easy", at("03", "In part (a) the majority")),
    "03b": ("medium", at("03", "In part (b) most candidates")),
    "04a": ("medium", at("04", "This was a relatively straightforward question")),
    "04b": ("medium", at("04", "This mark was often lost")),
    "05a": ("easy", at("05", "(a) The majority of candidates")),
    "05b": ("hard", at("05", "However, (b) was done")),
    "06a": ("medium", at("06", "The rigour demanded")),
    "06b": ("medium", at("06", "Finally, and worryingly")),
    "07a": ("easy", at("07", "In general, parts (a) and (b)")),
    "07b": ("easy", at("07", "(b) This part was answered well")),
    "07c": ("medium", at("07", "In general, parts (a) and (b)")),
    "08a": ("easy", at("08", "This question was generally well answered")),
    "08b": ("medium", at("08", "In part (b) candidates had less success")),
    "09a": ("easy", at("09", "(a) All but the weakest")),
    "09b": ("easy", at("09", "(b) Again, the majority")),
    "09c": ("hard", at("09", "(c) Most candidates could not distinguish")),
    "09d": ("hard", at("09", "(d) Whilst some candidates")),
    "10a": ("easy", at("10", "(a) This was generally answered successfully")),
    "10b": ("hard", at("10", "Of those who attempted this method")),
    "11a": ("easy", at("11", "(a) Almost every candidate")),
    "11b": ("medium", at("11", "What too many candidates")),
    "11c": ("hard", at("11", "A large number of candidates")),
    "11d": ("medium", at("11", "(d) This part of the question")),
    "12a": ("easy", at("12", "There were many well written out proof")),
    "12b": ("hard", at("12", "Part (b) was, on the other hand")),
    "13": ("medium", at("13", "Poor notation")),
    "14a": ("easy", at("14", "Part (a) was well answered by most")),
    "14b": ("hard", at("14", "Part (b) was the part candidates found most challenging")),
    "14c": ("easy", at("14", "A good understanding of the exponential graph")),
    "14d": ("easy", at("14", "In general parts (a), (c) and (d)")),
    "15": ("hard", at("15", "It was very rare to see a response")),
    "16i": ("hard", at("16", "This was a poorly answered question")),
    "16ii": ("hard", at("16", "Unfortunately a lack of understanding")),
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
