"""Draft builder for 9MA0-01 2022-06 (A level Pure Paper 1, June 2022).

Run (from the project root, with the venv active):
    python extraction/9MA0-01_2022-06.py        # writes out/drafts/9MA0-01_2022-06.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-01_2022-06.json

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

P, S = "9MA0-01", "2022-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "13iia"); label as printed (e.g. "13(ii)(a)")."""
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


I, J, K = r"\mathbf{i}", r"\mathbf{j}", r"\mathbf{k}"
SHOW = ["In this question you must show all stages of your working.",
        "Solutions relying entirely on calculator technology are not acceptable."]

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q1 = [r"The point $P(-2,-5)$ lies on the curve with equation $y=\mathrm{f}(x)$, $x\in\mathbb{R}$",
      r"Find the point to which $P$ is mapped, when the curve with equation $y=\mathrm{f}(x)$ is transformed to the "
      r"curve with equation"]
Q3 = ["A circle has equation", "$$x^2+y^2-10x+16y=80$$"]
Q4A = r"Express $\displaystyle\lim_{\delta x\to0}\sum_{x=2.1}^{6.3}\frac{2}{x}\delta x$ as an integral."
Q5 = ["The height, $h$ metres, of a tree, $t$ years after being planted, is modelled by the equation",
      r"$$h^2=at+b\qquad0\leqslant t<25$$", "where $a$ and $b$ are constants.", "Given that",
      "• the height of the tree was 2.60 m, exactly 2 years after being planted",
      "• the height of the tree was 5.10 m, exactly 10 years after being planted"]
Q5A = "find a complete equation for the model, giving the values of $a$ and $b$ to 3 significant figures."
Q6 = [r"[Figure 1: the curve $C$, a cubic rising from the bottom left through $O$ to a maximum at $(2, 8)$, falling to "
      r"touch the $x$-axis at a minimum at 6, then rising steeply.]",
      r"Figure 1 shows a sketch of a curve $C$ with equation $y=\mathrm{f}(x)$ where $\mathrm{f}(x)$ is a cubic "
      r"expression in $x$.", "The curve", "• passes through the origin", "• has a maximum turning point at $(2, 8)$",
      "• has a minimum turning point at $(6, 0)$"]
Q8 = [r"[Figure 2: the speed $v$ against $t$: a curve rising steeply from $O$ to a maximum, then falling more gently to "
      r"meet the $t$-axis at $T$.]",
      "A car stops at two sets of traffic lights.",
      r"Figure 2 shows a graph of the speed of the car, $v$ m s$^{-1}$, as it travels between the two sets of traffic "
      r"lights.",
      "The car takes $T$ seconds to travel between the two sets of traffic lights.",
      "The speed of the car is modelled by the equation", r"$$v=(10-0.4t)\ln(t+1)\qquad0\leqslant t\leqslant T$$",
      "where $t$ seconds is the time after the car leaves the first set of traffic lights."]
Q8B = ["show that the maximum speed of the car occurs when", r"$$t=\frac{26}{1+\ln(t+1)}-1$$"]
Q9 = [r"[Figure 3: a parallelogram $PQRS$ with $P$ at the left, $Q$ at the top, $R$ to the right and $S$ at the "
      r"bottom.]",
      "Figure 3 shows a sketch of a parallelogram $PQRS$.", "Given that",
      rf"• $\overrightarrow{{PQ}}=2{I}+3{J}-4{K}$", rf"• $\overrightarrow{{QR}}=5{I}-2{K}$"]
Q10 = ["A scientist is studying the number of bees and the number of wasps on an island.",
       "The number of bees, measured in thousands, $N_b$, is modelled by the equation",
       r"$$N_b=45+220\mathrm{e}^{0.05t}$$", "where $t$ is the number of years from the start of the study."]
Q11 = [r"[Figure 4: the curve $C_1$ starting on the positive $y$-axis, flat at first and then rising steeply; the curve "
       r"$C_2$, an $\cap$-shaped curve rising from below the $x$-axis just right of $O$ to a maximum and falling again "
       r"through the $x$-axis; the curves cross twice.]",
       "Figure 4 shows a sketch of part of the curve $C_1$ with equation", r"$$y=2x^3+10\qquad x>0$$",
       "and part of the curve $C_2$ with equation", r"$$y=42x-15x^2-7\qquad x>0$$"]
Q11A = r"Verify that the curves intersect at $x=\frac{1}{2}$"
Q13II = ["(ii) James saves money over a number of weeks to buy a printer that costs £64",
         "He saves £10 in week 1, £9.20 in week 2, £8.40 in week 3 and so on, so that the weekly amounts he saves form "
         "an arithmetic sequence.", "Given that James takes $n$ weeks to save exactly £64"]
Q13A = ["(a) show that", "$$n^2-26n+160=0$$"]
Q13B = ["(b) Solve the equation", "$$n^2-26n+160=0$$"]
Q14A = ["Given that", r"$$2\sin(x-60^\circ)=\cos(x-30^\circ)$$", "show that", r"$$\tan x=3\sqrt{3}$$"]
Q15 = [r"[Figure 5: a solid shaped like a wedge of cheese: the top face $ABC$ is a sector with centre $A$, radii $AB$ and "
       r"$AC$ labelled $r$ and angle $0.8$ rad at $A$; the vertical edges $AD$ (labelled $h$), $CF$ and $BE$ join it to "
       r"the congruent bottom face $DEF$; the hidden edge $DE$ is dashed.]",
       "A company makes toys for children.",
       "Figure 5 shows the design for a solid toy that looks like a piece of cheese.", "The toy is modelled so that",
       "• face $ABC$ is a sector of a circle with radius $r$ cm and centre $A$", "• angle $BAC=0.8$ radians",
       "• faces $ABC$ and $DEF$ are congruent",
       "• edges $AD$, $CF$ and $BE$ are perpendicular to faces $ABC$ and $DEF$",
       "• edges $AD$, $CF$ and $BE$ have length $h$ cm", "Given that the volume of the toy is 240 cm$^3$"]
Q15A = ["show that the surface area of the toy, $S$ cm$^2$, is given by", r"$$S=0.8r^2+\frac{1680}{r}$$",
        "making your method clear."]
Q15B = "Find the value of $r$ for which $S$ has a stationary point."
Q16 = [r"[Figure 6: the curve $C$ rising from $O$, curving over to a maximum and then turning back down and to the "
       r"left a little at its end; the region $R$ under $C$ from $O$ to the vertical line $x=4$ is shaded.]",
       "Figure 6 shows a sketch of the curve $C$ with parametric equations",
       r"$$x=8\sin^2t\qquad y=2\sin2t+3\sin t\qquad0\leqslant t\leqslant\frac{\pi}{2}$$",
       "The region $R$, shown shaded in Figure 6, is bounded by $C$, the $x$-axis and the line with equation $x=4$"]
Q16A = ["Show that the area of $R$ is given by",
        r"$$\int_0^a\left(8-8\cos4t+48\sin^2t\cos t\right)\mathrm{d}t$$", "where $a$ is a constant to be found."]

LATEX = {
    "01a": L(*Q1, r"$y=\mathrm{f}(x)+2$"),
    "01b": L(*Q1, r"$y=\left|\mathrm{f}(x)\right|$"),
    "01c": L(*Q1, r"$y=3\mathrm{f}(x-2)+2$"),
    "02": L(r"$$\mathrm{f}(x)=(x-4)(x^2-3x+k)-42\quad\text{where }k\text{ is a constant}$$",
            r"Given that $(x+2)$ is a factor of $\mathrm{f}(x)$, find the value of $k$."),
    "03a": L(*Q3, "Find", "(i) the coordinates of the centre of the circle,", "(ii) the radius of the circle."),
    "03b": L(*Q3, "Given that $P$ is the point on the circle that is furthest away from the origin $O$,",
             "find the exact length $OP$"),
    "04a": L(Q4A),
    "04b": L("(a) " + Q4A, "(b) Hence show that", r"$$\lim_{\delta x\to0}\sum_{x=2.1}^{6.3}\frac{2}{x}\delta x=\ln k$$",
             "where $k$ is a constant to be found."),
    "05a": L(*Q5, Q5A),
    "05b": L(*Q5, "(a) " + Q5A, "Given that the height of the tree was 7 m, exactly 20 years after being planted",
             "(b) evaluate the model, giving reasons for your answer."),
    "06a": L(*Q6, r"Write down the set of values of $x$ for which", r"$$\mathrm{f}'(x)<0$$"),
    "06b": L(*Q6, "The line with equation $y=k$, where $k$ is a constant, intersects $C$ at only one point.",
             "Find the set of values of $k$, giving your answer in set notation."),
    "06c": L(*Q6, "Find the equation of $C$. You may leave your answer in factorised form."),
    "07i": L("Given that $p$ and $q$ are integers such that", "$$pq\\text{ is even}$$",
             "use algebra to prove by contradiction that at least one of $p$ or $q$ is even."),
    "07ii": L("Given that $x$ and $y$ are integers such that", "• $x<0$", "• $(x+y)^2<9x^2+y^2$",
              "show that $y>4x$"),
    "08a": L(*Q8, "According to the model,", "find the value of $T$"),
    "08b": L(*Q8, "According to the model,", *Q8B),
    "08c": L(*Q8, "(b) " + Q8B[0], Q8B[1], "Using the iteration formula",
             r"$$t_{n+1}=\frac{26}{1+\ln(t_n+1)}-1$$", "with $t_1=7$", "(c) (i) find the value of $t_3$ to 3 decimal "
             "places,", "(ii) find, by repeated iteration, the time taken for the car to reach maximum speed."),
    "09a": L(*Q9, "show that parallelogram $PQRS$ is a rhombus."),
    "09b": L(*Q9, "Find the exact area of the rhombus $PQRS$."),
    "10a": L(*Q10, "According to the model,", "find the number of bees at the start of the study,"),
    "10b": L(*Q10, "According to the model,",
             r"show that, exactly 10 years after the start of the study, the number of bees was increasing at a "
             r"$\textbf{rate}$ of approximately 18 thousand per year."),
    "10c": L(*Q10, "The number of wasps, measured in thousands, $N_w$, is modelled by the equation",
             r"$$N_w=10+800\mathrm{e}^{-0.05t}$$", "where $t$ is the number of years from the start of the study.",
             "When $t=T$, according to the models, there are an equal number of bees and wasps.",
             "Find the value of $T$ to 2 decimal places."),
    "11a": L(*Q11, Q11A),
    "11b": L(*Q11, "(a) " + Q11A, "The curves intersect again at the point $P$",
             "(b) Using algebra and showing all stages of working, find the exact $x$ coordinate of $P$"),
    "12": L("In this question you must show all stages of your working.",
            "Solutions relying on calculator technology are not acceptable.", "Show that",
            r"$$\int_1^{\mathrm{e}^2}x^3\ln x\,\mathrm{d}x=a\mathrm{e}^8+b$$",
            "where $a$ and $b$ are rational constants to be found."),
    "13i": L("In an arithmetic series, the first term is $a$ and the common difference is $d$.", "Show that",
             r"$$S_n=\frac{n}{2}[2a+(n-1)d]$$"),
    "13iia": L(*Q13II, *Q13A),
    "13iib": L(*Q13II, *Q13A, *Q13B),
    "13iic": L(*Q13II, *Q13A, *Q13B,
               "(c) Hence state the number of weeks James takes to save enough money to buy the printer, giving a brief "
               "reason for your answer."),
    "14a": L(*SHOW, *Q14A),
    "14b": L(*SHOW, "(a) " + Q14A[0], *Q14A[1:], r"(b) Hence or otherwise solve, for $0\leqslant\theta<180^\circ$",
             r"$$2\sin2\theta=\cos(2\theta+30^\circ)$$", "giving your answers to one decimal place."),
    "15a": L(*Q15, *Q15A),
    "15b": L(*Q15, "(a) " + Q15A[0], *Q15A[1:], "Using algebraic differentiation,", "(b) " + Q15B),
    "15c": L(*Q15, "(a) " + Q15A[0], *Q15A[1:], "(b) " + Q15B,
             "(c) Prove, by further differentiation, that this value of $r$ gives the minimum surface area of the toy."),
    "16a": L(*Q16, *Q16A),
    "16b": L(*Q16, "(a) " + Q16A[0], *Q16A[1:], "(b) Hence, using algebraic integration, find the exact area of $R$."),
}

DVT = r"\frac{\mathrm{d}v}{\mathrm{d}t}"
DSR = r"\frac{\mathrm{d}S}{\mathrm{d}r}"
D2S = r"\frac{\mathrm{d}^2S}{\mathrm{d}r^2}"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", ALG, "2.9", 1, LATEX["01a"],
      [r"B1 (AO 1.1b): $(-2,-3)$. Notes: Watch for answers in the body of the question and on sketch graphs. This is "
       r"acceptable. If coordinates are written by the question and in the main answer section the answer section takes "
       r"precedence. Accept without brackets. May be written $x=-2,y=-3$"],
      False, 2),
    e("01b", "1(b)", ALG, "2.9, 2.7", 1, LATEX["01b"],
      [r"B1 (AO 1.1b): $(-2,5)$. Notes: Accept without brackets. May be written $x=-2,y=5$"],
      False, 2),
    e("01c", "1(c)", ALG, "2.9", 2, LATEX["01c"],
      [r"M1 (AO 1.1b): Either $x=0$ or $y=-13$. Notes: For either coordinate. E.g. $(0,\ldots)$ or $(\ldots,-13)$ If they "
       r"are building up their solution in stages e.g. $(-2,-5)\to(0,-5)\to(0,-15)\to(0,-13)$ only mark their final "
       r"coordinate pair",
       r"A1 (AO 1.1b): $(0,-13)$. Notes: Correct coordinates. See above for building up solution in stages Accept without "
       r"brackets. May be written $x=0,y=-13$ SC 10 for candidates who write $(-13,0)$"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02", "2", ALG, "2.6", 3, LATEX["02"],
      [r"M1 (AO 3.1a): Sets $\mathrm{f}(-2)=0\Rightarrow(-2-4)\left((-2)^2-3\times-2+k\right)-42=0$. Notes: Attempts "
       r"$\mathrm{f}(-2)=0$ leading to an equation in $k$. So $(-2-4)\left((-2)^2-3\times-2+k\right)-42=0$ is fine Condone "
       r"slips but expect to see a first bracket of $(-2-4)$ . “$-42$” must not be omitted but could appear as +42 with a "
       r"sign slip. There may have been attempts to expand $\mathrm{f}(x)=(x-4)(x^2-3x+k)-42$ before attempting to set "
       r"$\mathrm{f}(-2)=0$. This is acceptable and condone slips/errors in the expansion, but the 42 must be present. FYI "
       r"the expanded (and simplified ) $\mathrm{f}(x)=x^3-7x^2+(12+k)x-4k-42$",
       r"M1 (AO 1.1b): $-6(k+10)=42\Rightarrow k=\ldots$ Notes: Solves a linear equation in $k$ as a result of setting "
       r"$\mathrm{f}(\pm2)=0$. The $\pm42$ must be there at some point when the substitution is made. Allow minimal "
       r"evidence here. A linear equation leading to a solution is fine. If $\mathrm{f}(x)$ is expanded then it is "
       r"dependent upon being a cubic which contains a $kx$ term and a ‘42’",
       r"A1 (AO 1.1b): $k=-17$. Notes: $k=-17$ correct answer following correct work but allow recovery from invisible "
       r"brackets Answers of $k=-17$ may appear with very little or no working, perhaps via trial and improvement. If so, "
       r"then marks can only be allocated if evidence is shown. E.g. $k=-17\Rightarrow\mathrm{f}(x)=(x-4)(x^2-3x-17)-42$ "
       r"$\mathrm{f}(-2)=(-6)\times(-7)-42=0$. Hence $(x+2)$ is a factor.",
       r"ALT: Alt I : You may see attempts via division / inspection (the mark scheme shows $x^3-7x^2+(12+k)x-4k-42$ "
       r"divided by $x+2$ with quotient $x^2-9x+(k+30)$, then sets remainder $-6k-102=0\Rightarrow k=-17$) — M1: For "
       r"dividing their cubic by $(x+2)$ which has both an $x$ and a constant coefficient in $k$, leading to a quadratic "
       r"quotient and a linear remainder in $k$ which is then set = 0",
       r"ALT: Alt I — M1: Solves a equation resulting from setting a linear remainder in $k$ equal to 0 . It is dependent "
       r"on the first M via this route",
       r"ALT: Alt I — A1: Completely correct with $k=-17$",
       r"ALT: Alt II: You may also see a grid or an attempt at factorisation via inspection, e.g. "
       r"$x^3-7x^2+(12+k)x-4k-42\equiv(x+2)(x^2-9x-2k-21)$ followed by equating the $x$ terms "
       r"$12+k=-18-2k-21\Rightarrow3k=-51\Rightarrow k=-17$, or $\equiv(x+2)(x^2-9x+k+30)$ followed by equating the "
       r"constant terms $-4k-42=2(k+30)\Rightarrow6k=-102\Rightarrow k=-17$ — M1: For an attempt at factorising E.g. "
       r"$x^3-7x^2+(12+k)x-4k-42\equiv(x+2)(x^2+bx+c)$ and attempting to set up three equations in $b$, $c$ and $k$. E.g "
       r"$2+b=-7,2b+c=12+k,2c=-4k-42$ The expanded $\mathrm{f}(x)$ must be a cubic which contains both a $kx$ term and a "
       r"‘42’",
       r"ALT: Alt II — M1: Solves the equations set up from an allowable equation to find $k$. It is dependent via this "
       r"route.",
       r"ALT: Alt II — A1: Completely correct with $k=-17$"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", COORD, "3.2", 3, LATEX["03a"],
      [r"M1 (AO 1.1b): (i) $x^2+y^2-10x+16y=80\Rightarrow(x-5)^2+(y+8)^2=\ldots$ Notes: Attempts to complete the square on "
       r"both $x$ and $y$ terms. Accept $(x\pm5)^2+(y\pm8)^2=\ldots$ or imply this mark for a centre of $(\pm5,\pm8)$ "
       r"Condone $(x\pm5)^2\ldots(y\pm8)^2=\ldots$ where the first ... could be , or even $-$",
       r"A1 (AO 1.1b): Centre $(5,-8)$. Notes: Correct centre $(5,-8)$. Accept without brackets. May be written "
       r"$x=5,y=-8$",
       r"A1 (AO 1.1b): (ii) Radius 13. Notes: 13. The M mark must have been awarded, so it can be scored following a "
       r"centre of $(\pm5,\pm8)$. Do not allow for $\sqrt{169}$ or $\pm13$"],
      False, 6),
    e("03b", "3(b)", COORD, "3.2", 2, LATEX["03b"],
      [r"M1 (AO 3.1a): Attempts $\sqrt{\text{“}5\text{”}^2+\text{“}8\text{”}^2}+\text{“}13\text{”}$. Notes: Attempts "
       r"$\sqrt{\text{“}5\text{”}^2+\text{“}8\text{”}^2}+\text{“}13\text{”}$ for their centre $(5,-8)$ and their radius 13. "
       r"Award when this is given as a decimal, e.g. 22.4 for correct centre and radius. Look for $\sqrt{a^2+b^2}+r$ where "
       r"centre is $(\pm a,\pm b)$ and radius is $r$ [The mark scheme shows a sketch of the circle with centre $(5,-8)$ and "
       r"the line through $O$ and the centre meeting the circle at $P$.]",
       r"A1ft (AO 1.1b): $13+\sqrt{89}$ but ft on their centre and radius. Notes: $13+\sqrt{89}$ Follow through on their "
       r"$(5,-8)$ and their 13 leading to an exact answer. ISW for example if they write $13+\sqrt{89}=22.4$",
       r"ALT: There are more complicated attempts which could involve finding $P$ by solving $y=\text{“}-\frac{8}{5}x"
       r"\text{”}$ and $x^2+y^2-10x+16y=80$ simultaneously and choosing the coordinate with the greatest modulus — M1: "
       r"The method is only scored when the distance of the largest coordinate from $O$ is attempted. Such methods are "
       r"unlikely to result in an exact value but can score 1 mark for the method. Condone slips FYI. Solving "
       r"$y=-\frac{8}{5}x$ and $x^2+y^2-10x+16y=80\Rightarrow89x^2-890x-2000=0\Rightarrow P=(11.89,-19.02)$ Hence "
       r"$OP=\sqrt{\text{“}11.89\text{”}^2+\text{“}19.02\text{”}^2}\ (=22.43)$ scores M1 A0 but "
       r"$OP=\sqrt{258+26\sqrt{89}}$ is M1 A1"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", INT, "8.4", 1, LATEX["04a"],
      [r"B1 (AO 1.2): $\lim_{\delta x\to0}\sum_{x=2.1}^{6.3}\frac{2}{x}\delta x=\int_{2.1}^{6.3}\frac{2}{x}\,\mathrm{d}x$. "
       r"Notes: Mark (a) and (b) as one States that $\int_{2.1}^{6.3}\frac{2}{x}\,\mathrm{d}x$ or equivalent such as "
       r"$2\int_{2.1}^{6.3}x^{-1}\,\mathrm{d}x$ but must include the limits and the $\mathrm{d}x$. Condone "
       r"$\mathrm{d}x\leftrightarrow\delta x$ as it is very difficult to tell one from another sometimes"],
      False, 8),
    e("04b", "4(b)", INT, "8.3, 8.2, 6.4", 2, LATEX["04b"],
      [r"M1 (AO 1.1b): $=[2\ln x]_{2.1}^{6.3}=2\ln6.3-2\ln2.1$. Notes: Know that $\int\frac{1}{x}\,\mathrm{d}x=\ln x$ and "
       r"attempts to apply the limits (either way around) Condone $\int\frac{2}{x}\,\mathrm{d}x=p\ln x$ (including $p=1$) "
       r"or $\int\frac{2}{x}\,\mathrm{d}x=p\ln qx$ as long as the limits are applied. Also be aware that "
       r"$\int\frac{2}{x}\,\mathrm{d}x=\ln x^2$, $\int\frac{2}{x}\,\mathrm{d}x=2\ln|x|+c$ and $\int\frac{2}{x}\,"
       r"\mathrm{d}x=2\ln cx$ o.e. are also correct $[p\ln x]_{2.1}^{6.3}=p\ln6.3-p\ln2.1$ is sufficient evidence to "
       r"award this mark",
       r"A1 (AO 1.1b): $=\ln9$ CSO. Notes: CSO $\ln9$ . Also answer = $\ln3^2$ so $k=9$ is fine. Condone $\ln|9|$ The "
       r"method mark must have been awarded. Do not accept answers such as $\ln\frac{39.69}{4.41}$ Note that solutions "
       r"appearing from “rounded” decimal work when taking lns should not score the final mark. It is a “show that” "
       r"question E.g. $[2\ln x]_{2.1}^{6.3}=2\ln6.3-2\ln2.1=2.197=\ln k\Rightarrow k=\mathrm{e}^{2.197}=8.998=9$"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", ALG, "2.11, 2.4", 4, LATEX["05a"],
      [r"M1 (AO 3.1b): Attempts to use $h^2=at+b$ with either $t=2,h=2.6$ or $t=10,h=5.1$. Notes: For translating the "
       r"problem into mathematics. Attempts to use the given equation o.e. with either of the pieces of information to "
       r"form one correct equation. Award for unsimplified equations as well, such as $2.6^2=2a+b$ or "
       r"$2.6=\sqrt{2a+b}$",
       r"A1 (AO 1.1b): Correct equations $2a+b=6.76$, $10a+b=26.01$. Notes: Two correct (and different) equations which "
       r"may be unsimplified",
       r"dM1 (AO 1.1b): Solves simultaneously to find values for $a$ and $b$. Notes: Solves simultaneously to find values "
       r"for $a$ and $b$. It is dependent upon the previous M Don't be too concerned with the process here as calculators "
       r"may be used. Score if values of $a$ and $b$ are reached from a pair of simultaneous equations",
       r"A1 (AO 3.3): $h^2=2.41t+1.95$ cao. Notes: Establishes the full equation of the model with values of $a$ and $b$ "
       r"given to exactly 3sf. Award if seen in either (a) or (b). It is not scored for the values of $a$ and $b$. Allow "
       r"either $h^2=2.41t+1.95$ or $h=\sqrt{2.41t+1.95}$ If they go on to square root each term from $h^2=2.41t+1.95$ "
       r"then it is A0. E.g. $h=1.55t+1.40$ Special case for candidates who mistakenly use $h=at+b$ For $2.6=2a+b$, "
       r"$5.1=10a+b\Rightarrow h=0.3125t+1.975$ or $h=0.313t+1.98$ can score M1 correct equations with attempt to solve "
       r"and A1 for either correct answer shown above. These are the only marks available to them for a maximum mark of "
       r"1100 00"],
      False, 10),
    e("05b", "5(b)", ALG, "2.11", 2, LATEX["05b"],
      [r"M1 (AO 3.4): Substitutes $t=20$ into their $h^2=2.41t+1.95$ and finds $h$ or $h^2$ Or substitutes $h=7$ into their "
       r"$h^2=2.41t+1.95$ and finds $t$. Notes: A full and valid attempt to either substitute $t=20$ into their "
       r"$h^2=2.41t+1.95$ o.e. and find a value for $h$ or $h^2$ or substitute $h=7$ into their $h^2=2.41t+1.95$ o.e. and "
       r"find a value for $t$ (to enable the candidate to compare real life data with that of the model.) The equation of "
       r"the model must be of the correct form, either $h^2=at+b$ or $h=\sqrt{at+b}$ Do not be too concerned with the "
       r"mechanics of the solution but the square or $\sqrt{}$ must have been used appropriately to enable the comparison "
       r"to be made. In cases with no working you will need to check the calculation",
       r"A1 (AO 3.5a): Compares the model with the true values and concludes “good model” with a minimal reason E.g. I "
       r"Finds $h=7.08$ (m) and states that it is a good model as 7.08 (m) is close to 7 (m) E.g II Finds $t$ =19.5 years "
       r"and states that the model is accurate as 19.5 ( years) ≈ 20 (years). Notes: Compares their $h$=7.08m to 7m o.e "
       r"using $h^2$ or their $t$ =19.5 years to 20 years and makes valid conclusion with reason. For this mark you "
       r"require • a statement that it is a “good” or “accurate” model or similar wording • a reason such as “the values "
       r"are close”, “the values are similar” or “the predicted values are within 5% of the true values.” • a model with "
       r"equation $h^2=at+b$ o.e. where $a=$ awrt 2.4 and $b\in[1.9,2.0]$ • correct calculations Condone a statement like "
       r"‘ the model is pretty accurate as it predicted 7.08m and the actual value is 7m’ Do not allow incorrect "
       r"statements such as the model is incorrect as it does not give 7 metres. Do not allow just “the model gives an "
       r"underestimate of the true value.” Do not allow ‘bad’ or ‘poor’ model"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", DIFF, "7.3", 1, LATEX["06a"],
      [r"B1 (AO 1.1b): $2<x<6$. Notes: Watch for answers written by the question. If they are beside the question and in "
       r"the answer space, the one in the answer space takes precedence Deduces $2<x<6$ o.e. such as $x>2,x<6$ $x>2$ and "
       r"$x<6$ $\{x:x>2\}\cap\{x:x<6\}$ $x\in(2,6)$ Condone attempts in which set notation is incorrectly attempted but "
       r"correct values can be seen or implied E.g. $\{x>2\}\cap\{x<6\}$ $\{x>2,x<6\}$. Allow just the open interval "
       r"$(2,6)$ Do not allow for incorrect inequalities such as e.g. $x>2$ or $x<6$, $\{x:x>2\}\cup\{x:x<6\}$ "
       r"$x\in[2,6]$"],
      True, 12),
    e("06b", "6(b)", ALG, "2.7, 2.5", 2, LATEX["06b"],
      [r"M1 (AO 3.1a): States either $k>8$ or $k<0$. Notes: Establishes a correct method by finding one of the (correct) "
       r"inequalities States either $k>8$ (condone $k\geqslant8$ ) or $k<0$ (condone $k\leqslant0$) Condone for this mark "
       r"$y\leftrightarrow k$ or $\mathrm{f}(x)\leftrightarrow k$ and $8<k<0$",
       r"A1 (AO 2.5): States e.g. $\{k:k>8\}\cup\{k:k<0\}$. Notes: Fully correct solution in the form "
       r"$\{k:k>8\}\cup\{k:k<0\}$ or $\{k|k>8\}\cup\{k|k<0\}$ either way around but condone $\{k<0\}\cup\{k>8\}$, "
       r"$\{k:k<0\cup k>8\}$, $\{k<0\cup k>8\}$. It is not necessary to mention $\mathbb{R}$, e.g. "
       r"$\{k:k\in\mathbb{R},k>8\}\cup\{k:k\in\mathbb{R},k<0\}$ Look for $\{\ \}$ and $\cup$ Do not allow solutions not in "
       r"set notation such as $k<0$ or $k>8$."],
      True, 12),
    e("06c", "6(c)", ALG, "2.7, 2.6", 3, LATEX["06c"],
      [r"M1 (AO 1.1b): Please see notes for alternatives States $y=ax(x-6)^2$ or $\mathrm{f}(x)=ax(x-6)^2$. Notes: Realises "
       r"that the equation of $C$ is of the form $y=ax(x-6)^2$. Condone with $a=1$ for this mark. So award for sight of "
       r"$ax(x-6)^2$ even with $a=1$",
       r"dM1 (AO 3.1a): Substitutes $(2,8)$ into $y=ax(x-6)^2$ and attempts to find $a$. Notes: Substitutes $(2,8)$ into "
       r"the form $y=ax(x-6)^2$ and attempts to find the value for $a$. It is dependent upon having an equation, which the "
       r"( $y$=..) may be implied, of the correct form.",
       r"A1 (AO 2.1): $y=\frac{1}{4}x(x-6)^2$ or $\mathrm{f}(x)=\frac{1}{4}x(x-6)^2$ o.e. Notes: Uses all of the information "
       r"to form a correct equation for $C$ $y=\frac{1}{4}x(x-6)^2$ o.e. ISW after a correct answer. Condone "
       r"$\mathrm{f}(x)=\frac{1}{4}x(x-6)^2$ but not $C=\frac{1}{4}x(x-6)^2$. Allow this to be written down for all 3 "
       r"marks",
       r"ALT: Alternative I part (c): Using the form $y=ax^3+bx^2+cx$ and setting up then solving simultaneous equations. "
       r"There are various versions of this but can be marked similarly — M1: Realises that the equation of $C$ is of the "
       r"form $y=ax^3+bx^2+cx$ and forms two equations in $a$, $b$ and $c$. Condone with $a$ =1 for this mark. Note that "
       r"the form $y=ax^3+bx^2+cx+d$ is M0 until $d$ is set equal to 0. There are four equations that could be formed, only "
       r"two are necessary for this mark. Condone slips Using $(6,0)\Rightarrow216a+36b+6c=0$ Using "
       r"$(2,8)\Rightarrow8a+4b+2c=8$ Using $\frac{\mathrm{d}y}{\mathrm{d}x}=0$ at $x=2\Rightarrow12a+4b+c=0$ Using "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}=0$ at $x=6\Rightarrow108a+12b+c=0$",
       r"ALT: Alternative I part (c) — dM1: Forms and solves three different equations, one of which must be using "
       r"$(2,8)$ to find values for $a$, $b$ and $c$. A calculator can be used to solve the equations",
       r"ALT: Alternative I part (c) — A1: Uses all of the information to form a correct equation for $C$ "
       r"$y=\frac{1}{4}x^3-3x^2+9x$ o.e. ISW after a correct answer. Condone $\mathrm{f}(x)=\frac{1}{4}x^3-3x^2+9x$",
       r"ALT: Alternative II part (c) Using the gradient and integrating — M1: Realises that the gradient of $C$ is zero "
       r"at 2 and 6 so sets $\mathrm{f}'(x)=k(x-2)(x-6)$ oe and attempts to integrate. Condone with $k=1$",
       r"ALT: Alternative II part (c) — dM1: Substitutes $x=2,y=8$ into $\mathrm{f}(x)=k\left(\ldots x^3+\ldots x+"
       r"\ldots\right)$ and finds a value for $k$",
       r"ALT: Alternative II part (c) — A1: Uses all of the information to form a correct equation for $C$ "
       r"$y=\frac{3}{4}\left(\frac{1}{3}x^3-4x^2+12x\right)$ o.e. ISW after a correct answer. Condone "
       r"$\mathrm{f}(x)=\frac{3}{4}\left(\frac{1}{3}x^3-4x^2+12x\right)$"],
      True, 12),

    # ---------------- Q7 ----------------
    e("07i", "7(i)", PROOF, "1.1", 3, LATEX["07i"],
      [r"B1 (AO 2.5): For setting up the contradiction: There exists integers $p$ and $q$ such that $pq$ is even and both "
       r"$p$ and $q$ are odd. Notes: For using the “correct”/ allowable language in setting up the contradiction. Expect to "
       r"see a minimum of • “assume” or “let” or “there is ” or other similar words • “$pq$ is even” and “$p$ and $q$ are "
       r"(both) odd”",
       r"M1 (AO 1.1b): For example, sets $p=2m+1$ and $q=2n+1$ and then attempts $pq=(2m+1)(2n+1)=\ldots$ Notes: Uses a "
       r"correct algebraic form for $p$ and $q$ and attempting to multiply. Allow any correct form so $p=2n+1$ and "
       r"$q=2m+3$ would be fine to use Different variables must be used for $p$ and $q$, so $p=2n+1$ and $q=2n-1$ would "
       r"be M0",
       r"A1* (AO 2.1): Obtains $pq=(2m+1)(2n+1)=4mn+2m+2n+1=2(2mn+m+n)+1$ States that this is odd, giving a contradiction "
       r"so “ if $pq$ is even, then at least one of $p$ and $q$ is even” *. Notes: Full argument . This requires (1) a "
       r"correct calculation for their $pq$ (2) a correct reason and conclusion that it is odd E.g. "
       r"$(2m+1)(2n+1)=4mn+2m+2n+1=2(2mn+m+n)+1=$ odd E.g. $(2m-1)(2n+1)=4mn+2m-2n-1=$ even + even – even – 1 = odd and (3) "
       r"a minimal statement implying that they have proven what was required which could be QED, proven etc Note that "
       r"B0 M1 A1 is possible"],
      False, 14),
    e("07ii", "7(ii)", PROOF, "1.1, 2.5", 2, LATEX["07ii"],
      [r"M1 (AO 2.2a): $(x+y)^2<9x^2+y^2\Rightarrow2xy<8x^2$. Notes: For multiplying out and cancelling terms before "
       r"proceeding to a correct intermediate line such as $2xy<8x^2$ o.e. such as $2x(4x-y)>0$",
       r"A1* (AO 2.1): States that as $x<0\Rightarrow2y>8x\Rightarrow y>4x$ *. Notes: Full and rigorous proof with reason "
       r"shown as to why inequality reverses. The point at which it reverses must be correct and a correct reason given "
       r"See scheme So, the following should be scored M1 A0 as line 3 is incorrect $2xy-8x^2<0\Rightarrow2xy<8x^2"
       r"\Rightarrow y<4x\Rightarrow y>4x$ as $x<0$ There should be no incorrect lines in their proof",
       r"ALT: Alt: $2xy<8x^2\Rightarrow xy-4x^2<0\Rightarrow x(y-4x)<0$ as $x<0$, $(y-4x)>0\Rightarrow y>4x$ scores M1 "
       r"A1 — M1: $2xy<8x^2\Rightarrow xy-4x^2<0\Rightarrow x(y-4x)<0$",
       r"ALT: Alt — A1*: as $x<0$, $(y-4x)>0\Rightarrow y>4x$"],
      False, 14),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", ALG, "2.11", 1, LATEX["08a"],
      [r"B1 (AO 3.4): 25. Notes: 25 but condone 25 seconds. If another value is given (apart from 0) it is B0"],
      True, 16),
    e("08b", "8(b)", DIFF, "7.4, 7.3", 4, LATEX["08b"],
      [rf"M1 (AO 3.1b): Attempts to differentiate using the product rule ${DVT}=\ln(t+1)\times-0.4+\frac{{(10-0.4t)}}{{t+1}}$. "
       rf"Notes: Attempts to use the product rule in an attempt to differentiate $v=(10-0.4t)\ln(t+1)$ Look for "
       rf"$(10-0.4t)\times\frac{{1}}{{(t+1)}}\pm k\ln(t+1)$, where $k$ is a constant, condoning slips. If you see direct "
       rf"evidence of an incorrect rule used e.g. $vu'-uv'$ it is M0 You will see attempts from $v=10\ln(t+1)-0.4t\ln(t+1)$ "
       rf"which can be similarly marked. In this case look for $\frac{{a}}{{t+1}}\pm\frac{{bt}}{{t+1}}\pm c\ln(t+1)$",
       rf"A1 (AO 1.1b): ${DVT}=\ln(t+1)\times-0.4+\frac{{(10-0.4t)}}{{t+1}}$. Notes: Correct differentiation. Condone a "
       rf"missing left hand or it seen as $v'$, $\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}x}}$ or even = 0 "
       rf"$\left({DVT}\right)=\ln(t+1)\times-0.4+\frac{{(10-0.4t)}}{{t+1}}$ or equivalent such as "
       rf"$\left({DVT}\right)=\frac{{10}}{{t+1}}-\frac{{0.4t}}{{(t+1)}}-0.4\ln(t+1)$",
       rf"dM1 (AO 1.1b): Sets their ${DVT}=0\Rightarrow\frac{{(10-0.4t)}}{{(t+1)}}=0.4\ln(t+1)$ and then makes progress towards "
       rf"making “$t$” the subject (See notes for this). Notes: Score for setting their $\mathrm{{d}}V/\mathrm{{d}}t$ = 0 "
       rf"(which must be in an appropriate form) and proceeding to an equation where the variable $t$ occurs only once – "
       rf"ignoring $\ln(t+1)$. See two examples of how this can be achieved below. It is dependent upon the previous M. "
       rf"Look for the following steps • An allowable derivative set (or implied) = 0 E.g. "
       rf"$\ln(t+1)\times0.4=\frac{{(10-0.4t)}}{{t+1}}$ • Cross multiplication (or division) and rearrangement to form an "
       rf"equation where the variable $t$ only occurs once. E.g.1. $\ln(t+1)\times0.4=\frac{{(10-0.4t)}}{{t+1}}\Rightarrow"
       rf"\ln(t+1)=\frac{{25-t}}{{t+1}}\Rightarrow\ln(t+1)=-1+\frac{{26}}{{t+1}}$ E.g 2 $\ln(t+1)\times0.4="
       rf"\frac{{(10-0.4t)}}{{t+1}}\Rightarrow0.4t\ln(t+1)+0.4\ln(t+1)=10-0.4t\Rightarrow0.4t(1+\ln(t+1))=10-0.4\ln(t+1)$",
       rf"A1* (AO 2.1): $t=\frac{{25-\ln(t+1)}}{{1+\ln(t+1)}}$ $t=\frac{{26}}{{1+\ln(t+1)}}-1$ *. Notes: Correctly proceeds "
       rf"to the given answer of $t=\frac{{26}}{{1+\ln(t+1)}}-1$ showing all key steps. The key steps must include • use of "
       rf"${DVT}$ or $v'$ which must be correct • a correct line preceding the given answer, usually "
       rf"$t=\frac{{25-\ln(t+1)}}{{1+\ln(t+1)}}$ or $\frac{{26}}{{t+1}}-1=\ln(t+1)$"],
      True, 16),
    e("08c", "8(c)", NUM, "9.3", 3, LATEX["08c"],
      [r"M1 (AO 1.1b): (i) Attempts $t_2=\frac{26}{1+\ln8}-1$. Notes: Attempts to use the iteration formula at least once. "
       r"Usually to find $t_2=\frac{26}{1+\ln8}-1$ which may be implied by awrt 7.44",
       r"A1 (AO 1.1b): awrt 7.298. Notes: awrt 7.298. This alone will score both marks as iteration is implied. ISW after "
       r"sight of this value. As $t_3$ is the only value that rounds to 7.298 just score the rhs, it does not need to be "
       r"labelled $t_3$",
       r"A1 (AO 3.2a): (ii) awrt 7.33 seconds. Notes: Uses repeated iteration until value established as awrt 7.33 "
       r"seconds. Allow awrt 7.33 s Requires units. It also requires some evidence of iteration which will be usually be "
       r"awarded from the award of the M"],
      True, 16),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", VEC, "10.2, 10.5", 2, LATEX["09a"],
      [r"M1 (AO 3.1a): Attempts both $\left|\overrightarrow{PQ}\right|=\sqrt{2^2+3^2+(-4)^2}$ and "
       r"$\left|\overrightarrow{QR}\right|=\sqrt{5^2+(-2)^2}$. Notes: (a) Do not award marks in part (a) from work in part "
       r"(b). Attempts both $\left|\overrightarrow{PQ}\right|=\sqrt{2^2+3^2+(\pm4)^2}$ and "
       r"$\left|\overrightarrow{QR}\right|=\sqrt{5^2+(\pm2)^2}$ or $PQ^2$ and $QR^2$ . For this mark only, condone just the "
       r"correct answers $\left|\overrightarrow{PQ}\right|=\sqrt{29}$ and $\left|\overrightarrow{QR}\right|=\sqrt{29}$ . "
       r"Alternatively attempts $\overrightarrow{PR}\bullet\overrightarrow{QS}$ or $PM^2,MQ^2$ and $PQ^2$ where $M$ is the "
       r"mid point of $PR$",
       r"A1 (AO 2.4): States that $\left|\overrightarrow{PQ}\right|=\left|\overrightarrow{QR}\right|=\sqrt{29}$ so $PQRS$ is "
       r"a rhombus. Notes: Shows that $\left|\overrightarrow{PQ}\right|=\left|\overrightarrow{QR}\right|=\sqrt{29}$ (with "
       r"calculations) and states $PQRS$ is a rhombus. Condone poor notation such as $\overrightarrow{PQ}=\sqrt{29}$ here, "
       r"So $\overrightarrow{PQ}=\overrightarrow{QR}=\sqrt{29}$ hence rhombus. Requires both a reason and a conclusion. The "
       r"reason may be given at the start of their solution. In the alternatives $\overrightarrow{PR}\bullet"
       rf"\overrightarrow{{QS}}=(7{I}+3{J}-6{K})\bullet(3{I}-3{J}+2{K})=21-9-12=0$ so diagonals cross at $90^\circ$ so "
       r"$PQRS$ is a rhombus or $PM^2+MQ^2=PQ^2\Rightarrow23.5+5.5=29\Rightarrow\angle PMQ=90^\circ\Rightarrow$ Rhombus"],
      True, 20),
    e("09b", "9(b)", VEC, "10.5, 10.3, 10.2", 4, LATEX["09b"],
      [rf"M1 (AO 3.1a): Attempts BOTH $\overrightarrow{{PR}}=\overrightarrow{{PQ}}+\overrightarrow{{QR}}=7{I}+3{J}-6{K}$ AND "
       rf"$\overrightarrow{{QS}}=-\overrightarrow{{PQ}}+\overrightarrow{{PS}}=3{I}-3{J}+2{K}$. Notes: (b) Candidates can "
       rf"transfer answers from (a) to use in part (b) to find the area Look through their complete solution first. The "
       rf"first two marks are for finding the elements that are required to calculate the area. The second set of two "
       rf"marks is for combining these elements correctly. If the method is NOT shown on how to find vector it can be "
       rf"implied by two correct components. Allow as column vectors. M1: For a key step in solving the problem. It is "
       rf"scored for attempting to find both key vectors. Attempts both $\overrightarrow{{PR}}=\overrightarrow{{PQ}}+"
       rf"\overrightarrow{{QR}}=(7{I}+3{J}-6{K})$ AND $\overrightarrow{{QS}}=-\overrightarrow{{PQ}}+\overrightarrow{{PS}}="
       rf"(3{I}-3{J}+2{K})$ You may see $\overrightarrow{{PM}}=\frac{{1}}{{2}}\overrightarrow{{PQ}}+\frac{{1}}{{2}}"
       rf"\overrightarrow{{QR}}=\left(\frac{{7}}{{2}}{I}+\frac{{3}}{{2}}{J}-3{K}\right)$ AND $\overrightarrow{{QM}}="
       rf"-\frac{{1}}{{2}}\overrightarrow{{PQ}}+\frac{{1}}{{2}}\overrightarrow{{PS}}=\left(\frac{{3}}{{2}}{I}-\frac{{3}}{{2}}{J}"
       rf"+1{K}\right)$",
       rf"A1 (AO 1.1b): Correct $\overrightarrow{{PR}}=7{I}+3{J}-6{K}$ and $\overrightarrow{{QS}}=3{I}-3{J}+2{K}$. Notes: "
       rf"Accurately finds both key vectors whose lengths are required to solve the problem. Score for both "
       rf"$\overrightarrow{{PR}}=7{I}+3{J}-6{K}$ and $\overrightarrow{{QS}}=3{I}-3{J}+2{K}$ (Allow either way around.) or "
       rf"both $\overrightarrow{{PM}}=\frac{{7}}{{2}}{I}+\frac{{3}}{{2}}{J}-3{K}$ and $\overrightarrow{{QM}}=\frac{{3}}{{2}}{I}"
       rf"-\frac{{3}}{{2}}{J}+1{K}$ (Allow either way around.)",
       r"dM1 (AO 2.1): Correct method for area $PQRS$. E.g. $\frac{1}{2}\times\left|\overrightarrow{PR}\right|\times"
       r"\left|\overrightarrow{QS}\right|$. Notes: Constructs a rigorous method leading to the area $PQRS$. Dependent upon "
       r"previous M. E.g. See scheme. Alt: the sum of the area of four right angled triangles e.g. "
       r"$4\times\frac{1}{2}\times\left|\overrightarrow{PM}\right|\times\left|\overrightarrow{QM}\right|$,",
       r"A1 (AO 1.1b): $=\sqrt{517}$. Notes: $\sqrt{517}$ [The mark scheme's FYI diagram gives "
       rf"$\overrightarrow{{QR}}=5{I}+0{J}-2{K}$, $\overrightarrow{{PQ}}=2{I}+3{J}-4{K}$, $\overrightarrow{{SQ}}=-3{I}+3{J}-2{K}$, "
       rf"$\overrightarrow{{MQ}}=-1.5{I}+1.5{J}-1{K}$, $\overrightarrow{{PR}}=7{I}+3{J}-6{K}$ and "
       rf"$\overrightarrow{{PM}}=3.5{I}+1.5{J}-3{K}$.]",
       r"ALT: Alt (b) Example using the cosine rule — M1 (AO 3.1a): Attempts $\left|\overrightarrow{QS}\right|="
       r"\sqrt{3^2+(-3)^2+2^2}=\sqrt{22}$ and so $22=29+29-2\sqrt{29}\sqrt{29}\cos SPQ$. Notes: Alt 1-Examples via cosine "
       r"rule but you may see use of scalar product via a Further Maths method. M1: For a key step in solving the problem. "
       r"In this case it for an attempt at $\cos PQR$ or $\cos SPQ$. Don't be too concerned with the labelling of the "
       r"angle which may appear as $\theta$. Attempts $\pm\begin{pmatrix}2\\3\\-4\end{pmatrix}\bullet\pm\begin{pmatrix}5\\0"
       r"\\-2\end{pmatrix}=\sqrt{2^2+3^2+(-4)^2}\times\sqrt{5^2+(-2)^2}\cos PQR$",
       r"ALT: Alt (b) cosine rule — A1 (AO 1.1b): $\cos PQR=-\frac{18}{29}$ or $\cos SPQ=\frac{18}{29}$ Condone angles in "
       r"degrees 51.6, 128.4 (1dp) or radians 2.24, 0.901 (3sf) here. Notes: Finds the cosine of one of the angles in the "
       r"Figure. Look for $\cos\ldots=-\frac{18}{29}$ or $\cos\ldots=\frac{18}{29}$ which may have been achieved via the "
       r"cosine rule. Accept rounded answers and the angles in degrees 51.6, 128.4 (1dp) or radians 2.24, 0.901 (3sf) here.",
       r"ALT: Alt (b) cosine rule — dM1 (AO 2.1): Correct method for area $PQRS$. E.g. $PQ\times QR\sin PQR="
       r"\sqrt{2^2+3^2+(-4)^2}\times\sqrt{5^2+(-2)^2}\times\frac{\sqrt{517}}{29}$. Notes: Constructs a rigorous method "
       r"leading to the area $PQRS$. Implied by awrt 22.7",
       r"ALT: Alt (b) cosine rule — A1 (AO 1.1b): $=\sqrt{517}$",
       r"ALT: Alt 2-Example via vector product via a Further Maths method. — M1: For a key step in solving the problem. "
       r"In this case it for an attempt at $\pm\overrightarrow{PQ}\times\overrightarrow{QR}$ E.g. "
       rf"$\overrightarrow{{PQ}}\times\overrightarrow{{QR}}=\begin{{pmatrix}}{I}&{J}&{K}\\2&3&-4\\5&0&-2\end{{pmatrix}}="
       rf"(3\times-2-0\times-4){I}-(2\times-2-5\times-4){J}+(2\times0-3\times5){K}$",
       rf"ALT: Alt 2 vector product — A1: E.g. $\overrightarrow{{PQ}}\times\overrightarrow{{QR}}=-6{I}-16{J}-15{K}$",
       r"ALT: Alt 2 vector product — dM1: Constructs a rigorous method leading to the area $PQRS$. In this case "
       r"$\left|\overrightarrow{PQ}\times\overrightarrow{QR}\right|$",
       r"ALT: Alt 2 vector product — A1: $=\sqrt{(-6)^2+(-16)^2+(-15)^2}=\sqrt{517}$"],
      True, 20),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", EXP, "6.7", 1, LATEX["10a"],
      [r"B1 (AO 3.4): 265 thousand. Notes: May be seen in the question so watch out. Accept 265 thousand or 265 000 or "
       r"equivalent such as 265 k but not just 265."],
      False, 24),
    e("10b", "10(b)", EXP, "6.2, 6.7", 3, LATEX["10b"],
      [r"M1 (AO 1.1b): Attempts $\frac{\mathrm{d}N_b}{\mathrm{d}t}=11\mathrm{e}^{0.05t}$. Notes: Differentiates to a form "
       r"$k\mathrm{e}^{0.05t},k>0,k\neq220$ . Do not be too concerned about the lhs.",
       r"M1 (AO 3.4): Substitutes $t=10$ into their $\frac{\mathrm{d}N_b}{\mathrm{d}t}$. Notes: Substitutes $t=10$ into a "
       r"changed function that was formed from an attempt at differentiation. The left hand side must have implied "
       r"differentiation. E.g. Rate = , $N'$, $\frac{\mathrm{d}N_b}{\mathrm{d}t}$, $\frac{\mathrm{d}N}{\mathrm{d}t}$ or even "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}$",
       r"A1* (AO 2.1): $\frac{\mathrm{d}N_b}{\mathrm{d}t}=$ awrt 18.1 which is approximately 18 thousand per year *. Notes: "
       r"Full and complete proof that requires • some correct lhs seen at some point. E.g. “Rate = , ” "
       r"$\frac{\mathrm{d}N_b}{\mathrm{d}t}$, $\frac{\mathrm{d}N}{\mathrm{d}t}$ but condone $N'$. • an intermediate "
       r"line/answer of either $11\mathrm{e}^{0.05\times10}$ or awrt 18.1 before a minimal conclusion which must be "
       r"referencing the 18 000 or 18 thousand Answers with limited or no working in (b) and (c) (b) A derivative in the "
       r"correct form must be seen"],
      False, 24),
    e("10c", "10(c)", EXP, "6.7, 6.4, 2.3", 4, LATEX["10c"],
      [r"M1 (AO 3.1b): Sets $45+220\mathrm{e}^{0.05t}=10+800\mathrm{e}^{-0.05t}\Rightarrow220\mathrm{e}^{0.05t}+35-"
       r"800\mathrm{e}^{-0.05t}=0$. Notes: Attempts to set both equations equal to each other and simplify the constant "
       r"terms. Look for $220\mathrm{e}^{0.05t}+35=800\mathrm{e}^{-0.05t}$ o.e but condone slips It is also possible to set "
       r"$\frac{N-45}{220}=\left(\mathrm{e}^{0.05t}=\right)\frac{800}{N-10}$ and form an equation in $N$",
       r"A1 (AO 1.1b): Correct quadratic equation $\Rightarrow220\left(\mathrm{e}^{0.05t}\right)^2+35\mathrm{e}^{0.05t}-800=0$. "
       r"Notes: Correct quadratic form. Look for $220\left(\mathrm{e}^{0.05t}\right)^2+35\mathrm{e}^{0.05t}-800=0$ or "
       r"$220\mathrm{e}^{0.1t}+35\mathrm{e}^{0.05t}-800=0$ but allow with terms in different order such as "
       r"$220\mathrm{e}^{0.1t}+35\mathrm{e}^{0.05t}=800$ FYI the equation in $N$ is $N^2-55N-175550=0$",
       r"M1 (AO 2.1): $\mathrm{e}^{0.05t}=1.829,(-1.988)\Rightarrow0.05t=\ln(1.829)$. Notes: Full attempt to find the value "
       r"of $t$ (or a constant multiple of $t$) This involves the key step of recognising and solving a 3TQ in "
       r"$\mathrm{e}^{0.05t}$ followed by the use of lns. If the answers to the quadratic just appear (from a calculator) "
       r"you will need to check. Accuracy should be to 3sf. You may see different variables used such as $x$ "
       r"$x=\mathrm{e}^{0.05t}$, $220\mathrm{e}^{0.1t}+35\mathrm{e}^{0.05t}=800\Rightarrow220x^2+35x=800\Rightarrow "
       r"x=1.82\ldots\Rightarrow t=20\ln1.82\ldots$ Allow use of calculator for solving the quadratic and for "
       r"$\mathrm{e}^{0.05t}=1.82..\Rightarrow t=12.08$ Via the $N$ route it will involve substituting the positive "
       r"solution to their quadratic into either equation to find a value for $t/T$ using same rules as above.",
       r"A1 (AO 1.1b): $T=12.08$. Notes: AWRT 12.08 (c) Candidates who state $45+220\mathrm{e}^{0.05t}=10+800"
       r"\mathrm{e}^{-0.05t}$ followed by awrt 12.08 (presumably from using num-solv on their calculators) can score SC "
       r"1100. Rubric on the front of the paper states that “Answers without working may not gain full credit” so we "
       r"demand a method in this part."],
      False, 24),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", ALG, "2.4, 2.6", 2, LATEX["11a"],
      [r"M1 (AO 1.1b): Substitutes $x=\frac{1}{2}$ into $y=2x^3+10$ and $y=42x-15x^2-7$ and finds the $y$ values for both. "
       r"Notes: Substitutes $x=\frac{1}{2}$ into both $y=2x^3+10$ and $y=42x-15x^2-7$ and finds $y$ values Sight of just "
       r"the $y$ values at each is sufficient for this mark only. Alternative: Sets $42x-15x^2-7=2x^3+10\Rightarrow$ cubic "
       r"and substitutes $x=\frac{1}{2}$ into the expression, attempts $\mathrm{f}\left(\frac{1}{2}\right)$ or else attempts "
       r"to divide the cubic = 0 by $(2x-1)$ or $\left(x-\frac{1}{2}\right)$. Condone $\mathrm{f}\left(\frac{1}{2}\right)=0$ "
       r"without calculations for this mark only.",
       r"A1* (AO 2.4): Achieves $\frac{41}{4}$ o.e. for both and makes a valid conclusion. *. Notes: Correct calculations "
       r"must be seen with a minimal conclusion that curves intersect (at $x=\frac{1}{2}$). E.g. "
       r"$2\left(\frac{1}{2}\right)^3+10=10.25$ and $42\left(\frac{1}{2}\right)-15\left(\frac{1}{2}\right)^2-7=10.25$ so "
       r"curves intersect. Acceptable alternatives are: $\mathrm{f}(x)=42x-15x^2-7-2x^3-10$, "
       r"$\mathrm{f}\left(\frac{1}{2}\right)=42\left(\frac{1}{2}\right)-15\left(\frac{1}{2}\right)^2-7-2\left(\frac{1}{2}"
       r"\right)^3-10=0\Rightarrow$ so curves intersect $\mathrm{f}(x)=2x^3+15x^2-42x+17\Rightarrow\left(x-\frac{1}{2}"
       r"\right)(2x^2+16x-34)$ so $x=\frac{1}{2}$ is a root so curves intersect $\mathrm{f}(x)=2x^3+15x^2-42x+17\Rightarrow"
       r"(2x-1)(x^2+8x-17)$ so $(2x-1)$ is a factor hence curves intersect Only accept verified, QED etc if there is a "
       r"preamble mentioning intersection about how it will be shown. Special case: Scores M1 A0 with or without a "
       r"conclusion This is presumably done using a calculator and requires all three roots exact or correct to 3sf "
       r"$\mathrm{f}(x)=2x^3+15x^2-42x+17=0\Rightarrow x=0.5,1.74,-9.74$"],
      True, 28),
    e("11b", "11(b)", ALG, "2.6, 2.3", 5, LATEX["11b"],
      [r"M1 (AO 1.1b): Sets $42x-15x^2-7=2x^3+10\Rightarrow2x^3+15x^2-42x+17=0$. Notes: (b) This part requires candidates "
       r"to show all stages of their working. Answers without working will not score any marks A method must be seen "
       r"which could be from part (a) which must then be continued in (b) M1: Sets $42x-15x^2-7=2x^3+10$ and proceeds to 4 "
       r"term cubic equation. Condone slips, e.g. signs. Terms do not have to be on one side of the equation.",
       r"dM1 (AO 2.1): Deduces that $(2x-1)$ is a factor and attempts to divide. Notes: For the key step in attempting to "
       r"“divide” the cubic by $(2x-1)$ If attempted via inspection look for correct first and last terms E.g. "
       r"$2x^3+15x^2-42x+17=(2x-1)(x^2+\ldots\pm17)$ if cubic expression is correct If attempted via division look for "
       r"correct first and second terms [quotient $x^2+8x$ when dividing $2x^3+15x^2-42x+17$ by $2x-1$] if cubic "
       r"expression is correct It is acceptable for an attempt to divide by $\left(x-\frac{1}{2}\right)$. It is easily "
       r"marked using the same guidelines, e.g. $2x^3+15x^2-42x+17=\left(x-\frac{1}{2}\right)(2x^2+16x\ldots)$",
       r"A1 (AO 1.1b): $2x^3+15x^2-42x+17=(2x-1)(x^2+8x-17)$. Notes: $2x^3+15x^2-42x+17=(2x-1)(x^2+8x-17)$ o.e. "
       r"$\left(x-\frac{1}{2}\right)(2x^2+16x-34)$ This may be implied by sight of $(x^2+8x-17)$ or $(2x^2+16x-34)$ in a "
       r"“division” sum.",
       r"M1 (AO 1.1b): Solves their $x^2+8x-17=0$ using suitable method. Notes: Solves their quadratic $x^2+8x-17=0$ using a "
       r"suitable method including calculator. You may need to check this. It is not completely dependent upon the "
       r"previous M's but an attempt at a full method must have been seen. So look for • the two equations being set "
       r"equal to each other and some attempt made to combine • some attempt to “divide” the result by $(2x-1)$ o.e. "
       r"allowing for flaws in the method",
       r"A1 (AO 2.2a): Deduces $x=-4+\sqrt{33}$ (see note). Notes: Gives $x=-4+\sqrt{33}$ o.e. only. The $x=-4-\sqrt{33}$ "
       r"must not be included in the final answer. Allow exact unsimplified equivalents such as "
       r"$x=\frac{-8+\sqrt{132}}{2}$. ISW for instance if they then put this in decimal form."],
      True, 28),

    # ---------------- Q12 ----------------
    e("12", "12", INT, "8.5, 8.3, 6.4", 5, LATEX["12"],
      [r"M1 (AO 1.1b): $\int x^3\ln x\,\mathrm{d}x=\frac{x^4}{4}\ln x-\int\frac{x^4}{4}\times\frac{1}{x}\,\mathrm{d}x$. "
       r"Notes: Integrates by parts the right way round. Look for $kx^4\ln x-\int kx^4\times\frac{1}{x}\,\mathrm{d}x$ o.e. "
       r"with $k>0$ . Condone a missing $\mathrm{d}x$",
       r"M1 (AO 1.1b): $=\frac{x^4}{4}\ln x-\frac{x^4}{16}(+c)$. Notes: Uses a correct method to integrate an expression of "
       r"the form $\int kx^4\times\frac{1}{x}\,\mathrm{d}x\to cx^4$",
       r"A1 (AO 1.1b): $=\frac{x^4}{4}\ln x-\frac{x^4}{16}(+c)$. Notes: $\int x^3\ln x\,\mathrm{d}x=\frac{x^4}{4}\ln x-"
       r"\frac{x^4}{16}$ (+ $c$) which may be left unsimplified",
       r"M1 (AO 2.1): $\int_1^{\mathrm{e}^2}x^3\ln x\,\mathrm{d}x=\left[\frac{x^4}{4}\ln x-\frac{x^4}{16}\right]_1^{\mathrm{e}^2}"
       r"=\left(\frac{\mathrm{e}^8}{4}\ln\mathrm{e}^2-\frac{\mathrm{e}^8}{16}\right)-\left(-\frac{1^4}{16}\right)$. Notes: "
       r"Attempts to substitute 1 and $\mathrm{e}^2$ into an expression of the form $\pm px^4\ln x\pm qx^4$, subtracts and "
       r"uses $\ln\mathrm{e}^2=2$ (which may be implied).",
       r"A1 (AO 1.1b): $=\frac{7}{16}\mathrm{e}^8+\frac{1}{16}$. Notes: $\frac{7}{16}\mathrm{e}^8+\frac{1}{16}$ o.e. Allow "
       r"$0.4375\mathrm{e}^8+0.0625$ or uncancelled fractions. NOT ISW: $7\mathrm{e}^8+1$ is A0",
       r"ALT: You may see attempts where substitution has been attempted. E.g. $u=\ln x\Rightarrow x=\mathrm{e}^u$ and "
       r"$\frac{\mathrm{d}x}{\mathrm{d}u}=\mathrm{e}^u$ — M1: Attempts to integrate the correct way around condoning slips "
       r"on the coefficients $\int x^3\ln x\,\mathrm{d}x=\int\mathrm{e}^{4u}u\,\mathrm{d}u=\frac{\mathrm{e}^{4u}}{4}u-"
       r"\int\frac{\mathrm{e}^{4u}}{4}\,\mathrm{d}u$",
       r"ALT: Via substitution $u=\ln x$ — M1 A1: $\int x^3\ln x\,\mathrm{d}x=\frac{\mathrm{e}^{4u}}{4}u-"
       r"\frac{\mathrm{e}^{4u}}{16}(+c)$",
       r"ALT: Via substitution $u=\ln x$ — M1 A1: Substitutes 0 and 2 into an expression of the form "
       r"$\pm pu\mathrm{e}^{4u}\pm q\mathrm{e}^{4u}$ and subtracts",
       r"ALT: It is possible to use integration by parts “the other way around” To do this, candidates need to know or "
       r"use $\int\ln x\,\mathrm{d}x=x\ln x-x$ FYI $I=\int x^3\ln x\,\mathrm{d}x=x^3(x\ln x-x)-\int(x\ln x-x)\times3x^2\,"
       r"\mathrm{d}x=x^3(x\ln x-x)-3I+\frac{3}{4}x^4$ Hence $4I=x^4\ln x-\frac{1}{4}x^4\Rightarrow I=\frac{1}{4}x^4\ln x-"
       r"\frac{1}{16}x^4$ — M1: Score M1 for a full attempt at line 1 (condoning bracketing and coefficient slips)",
       r"ALT: Parts “the other way around” — M1: followed by M 1 for line 2 where terms in $I$ o.e. to form the answer."],
      False, 32),

    # ---------------- Q13 ----------------
    e("13i", "13(i)", SEQ, "4.4, 1.1", 3, LATEX["13i"],
      [r"B1 (AO 1.1a): States that $S=a+(a+d)+\ldots\ldots\ldots\ldots+(a+(n-1)d)$. Notes: Correctly writes down an "
       r"expression for the key terms $S$ or $S_n$ including $S$ = or $S_n$ = Allow a minimum of 3 correct terms "
       r"including the first and last terms, and no incorrect terms. Score for $S$ or $S_n=a+(a+d)+\ldots\ldots+(a+(n-1)d)$ "
       r"with + signs, not commas If the series contains extra terms that should not be there E.g "
       r"$S=a+(a+d)+\ldots\ldots(a+nd)+(a+(n-1)d)$ score B0",
       r"M1 (AO 3.1a): $S=a+(a+d)+\ldots+(a+(n-1)d)$ $S=(a+(n-1)d)+(a+(n-2)d)+\ldots\ldots+a$. Notes: For the key step in "
       r"reversing the terms and adding the two series. Look for a minimum of two terms, including $a$ and $a+(n-1)d$ , "
       r"the series reversed with evidence of adding, for example $2S$ = Condone the extra incorrect terms (see above) "
       r"appearing. Can be scored when terms are separated by commas",
       r"A1* (AO 2.1): Reaches $2S=n\times(2a+(n-1)d)$ And so proves that $S=\frac{n}{2}[2a+(n-1)d]$ *. Notes: Shows "
       r"correct work (no errors) with all steps shown leading to given answer. There should be no incorrect terms. A "
       r"minimum of 3 terms should be shown in each sum The solution below is a variation of this. "
       r"$S=a+(a+d)+\ldots+l$ $S=l+(l-d)+\ldots+a$ $2S=n(a+l)$ $S=\frac{n}{2}(a+l)=\frac{n}{2}(a+a+(n-1)d)="
       r"\frac{n}{2}(2a+(n-1)d)$ B1 and A1 are not scored until the last line, M scored on line 3 [The mark scheme shows a "
       r"candidate response scoring B1 M0 A0 as the terms in the second sum are not reversed, and an SC response scoring "
       r"B1 M0 A0 which uses $0+1+2+\ldots+(n-1)=\frac{n(n-1)}{2}$, relying on the quoted proof.]"],
      False, 34),
    e("13iia", "13(ii)(a)", SEQ, "4.4, 4.6", 2, LATEX["13iia"],
      [r"M1 (AO 3.1b): $S=10+9.20+8.40+\ldots$ $64=\frac{n}{2}(20-0.8(n-1))$ o.e. Notes: Uses the information given to set "
       r"up a correct equation in $n$. The values of $S$, $a$ and $d$ need to be correct and used within a correct formula "
       r"Possible ways to score this include unsimplified versions $64=\frac{n}{2}(2\times10+(n-1)\times-0.8)$, "
       r"$64=\frac{n}{2}(10+10+(n-1)\times-0.8)$ or versions using pence rather than £'s "
       r"$6400=\frac{n}{2}(2000+(n-1)\times-80)$ Allow recovery for both marks following "
       r"$64=\frac{n}{2}(2\times10+(n-1)-0.8)$ with an invisible ×",
       r"A1* (AO 2.1): $128=20n-0.8n^2+0.8n$ $0.8n^2-20.8n+128=0$ $n^2-26n+160=0$ *. Notes: Proceeds without error to the "
       r"given answer. (Do not penalise a missing final trailing bracket ) Look for at least a line with the brackets "
       r"correctly removed as well as a line with the terms in $n$ correctly combined E.g. "
       r"$64=\frac{n}{2}(20+(n-1)\times-0.8)\Rightarrow64=10n-0.4n^2+0.4n\Rightarrow0.4n^2-10.4n+64=0\Rightarrow "
       r"n^2-26n+160=0$"],
      False, 34),
    e("13iib", "13(ii)(b)", SEQ, "4.4, 2.3", 1, LATEX["13iib"],
      [r"B1 (AO 1.1b): $n=10,16$. Notes: $n=10,16$"],
      False, 34),
    e("13iic", "13(ii)(c)", SEQ, "4.6", 1, LATEX["13iic"],
      [r"B1 (AO 2.3): 10 weeks with a minimal correct reason. E.g. • He has saved up the amount by 10 weeks so he would "
       r"not save for another 6 weeks • You would choose the smaller number • He starts saving negative amounts (in week "
       r"14) so 16 does not make sense. Notes: Chooses 10 (weeks) and gives a minimal acceptable reason. The reason must "
       r"focus on why the answer is 10 (weeks) rather than 16(weeks) or alternatively why it would not be 16 weeks."],
      False, 34),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", TRIG, "5.6, 5.5, 5.8", 4, LATEX["14a"],
      [r"M1 (AO 2.1): Attempts to use both $\sin(x-60^\circ)=\pm\sin x\cos60^\circ\pm\cos x\sin60^\circ$ "
       r"$\cos(x-30^\circ)=\pm\cos x\cos30^\circ\pm\sin x\sin30^\circ$. Notes: Attempts to use both compound angle "
       r"expansions to set up an equation in $\sin x$ and $\cos x$ The terms must be correct but condone sign errors and a "
       r"slip on the multiplication of 2",
       r"A1 (AO 1.1b): Correct equation $2\sin x\cos60^\circ-2\cos x\sin60^\circ=\cos x\cos30^\circ+\sin x\sin30^\circ$. "
       r"Notes: Correct equation $2\sin x\cos60^\circ-2\cos x\sin60^\circ=\cos x\cos30^\circ+\sin x\sin30^\circ$ o.e. Note "
       r"that $\cos60^\circ=\sin30^\circ$ and $\cos30^\circ=\sin60^\circ$ Also allow this mark for candidates who "
       r"substitute in their trigonometric values “early” $2\sin x\times\frac{1}{2}-2\cos x\times\frac{\sqrt{3}}{2}="
       r"\cos x\times\frac{\sqrt{3}}{2}+\sin x\times\frac{1}{2}$ o.e.",
       r"M1 (AO 2.1): Either uses $\frac{\sin x}{\cos x}=\tan x$ and attempts to make $\tan x$ the subject E.g. "
       r"$(2\cos60^\circ-\sin30^\circ)\tan x=\cos30^\circ+2\sin60^\circ$ Or attempts $\sin30^\circ$ etc with at least two "
       r"correct and collects terms in $\sin x$ and $\cos x$ E.g. $\left(2\times\frac{1}{2}-\frac{1}{2}\right)\sin x="
       r"\left(2\times\frac{\sqrt{3}}{2}+\frac{\sqrt{3}}{2}\right)\cos x$. Notes: Shows the necessary progress towards "
       r"showing the given result. There are three key moves, two of which must be shown for this mark. • uses "
       r"$\frac{\sin x}{\cos x}=\tan x$ to form an equation in just $\tan x$. • uses exact numerical values for "
       r"$\sin30^\circ,\sin60^\circ,\cos30^\circ,\cos60^\circ$ with at least two correct • collects terms in $\sin x$ and "
       r"$\cos x$ or alternatively in $\tan x$",
       r"A1* (AO 1.1b): Proceeds to given answer showing all key steps E.g. $\frac{1}{2}\tan x=\frac{3\sqrt{3}}{2}"
       r"\Rightarrow\tan x=3\sqrt{3}$ *. Notes: Proceeds to the given answer with accurate work showing all necessary "
       r"lines. Examples of two proofs showing all necessary lines E.g. I $2\sin x\cos60^\circ-2\cos x\sin60^\circ="
       r"\cos x\cos30^\circ+\sin x\sin30^\circ$ $\sin x(2\cos60^\circ-\sin30^\circ)=\cos x(\cos30^\circ+2\sin60^\circ)$ 1. "
       r"collect terms $(2\cos60^\circ-\sin30^\circ)\tan x=\cos30^\circ+2\sin60^\circ$ 2. $\frac{\sin x}{\cos x}=\tan x$ so "
       r"M1 $\tan x=\frac{\cos30^\circ+2\sin60^\circ}{2\cos60^\circ-\sin30^\circ}=\frac{\frac{\sqrt{3}}{2}+\sqrt{3}}"
       r"{1-\frac{1}{2}}=3\sqrt{3}$ 3..uses values and completes proof A1* E.g II $2\sin x\times\frac{1}{2}-2\cos x\times"
       r"\frac{\sqrt{3}}{2}=\cos x\times\frac{\sqrt{3}}{2}+\sin x\times\frac{1}{2}$ 1.uses values "
       r"$\Rightarrow\frac{1}{2}\sin x=\frac{3\sqrt{3}}{2}\cos x$ 2.collects terms so M1 $\Rightarrow\tan x=3\sqrt{3}$ 3. "
       r"$\frac{\sin x}{\cos x}=\tan x$ completes proof A1*"],
      False, 38),
    e("14b", "14(b)", TRIG, "5.7, 5.6", 4, LATEX["14b"],
      [r"B1 (AO 2.2a): Deduces that $x=2\theta+60^\circ$. Notes: (b) Hence B1: Deduces that $x=2\theta+60^\circ$ o.e such "
       r"as $\theta=\frac{x-60^\circ}{2}$ This is implied for sight of the equation $\tan(2\theta+60^\circ)=3\sqrt{3}$",
       r"M1 (AO 1.1b): $\tan(2\theta+60^\circ)=3\sqrt{3}\Rightarrow2\theta+60^\circ=79.1^\circ,259.1^\circ,\ldots$ Notes: "
       r"Proceeds from $\tan(2\theta\pm\alpha^\circ)=3\sqrt{3}\Rightarrow2\theta\pm\alpha^\circ=$ one of "
       r"$79.1^\circ,259.1^\circ,\ldots$ where $\alpha\neq0$ One angle for $\arctan(3\sqrt{3})$ must be correct in degrees "
       r"or radians(3sf). FYI radian answers 1.38, 4.52",
       r"dM1 (AO 1.1b): Correct method to find one value of $\theta$ E.g $\theta=\frac{79.1^\circ-60^\circ}{2}$. Notes: "
       r"Correct method to find one value of $\theta$ from their $2\theta\pm\alpha^\circ=79.1^\circ$ to "
       r"$\theta=\frac{79.1^\circ\mp\alpha^\circ}{2}$ This is dependent upon one angle being correct, which must be in "
       r"degrees, for $\arctan(3\sqrt{3})$ $\tan(2\theta+60^\circ)=3\sqrt{3}\Rightarrow\theta=9.6^\circ$ would imply B1 M1 "
       r"dM1",
       r"A1 (AO 2.1): $\theta=$ awrt $9.6^\circ$, $99.6^\circ$ (See note). Notes: $\theta=$ awrt $9.6^\circ$, $99.6^\circ$ "
       r"with no other values given in the range",
       r"ALT: Otherwise: Via the use of $\cos(2\theta+30^\circ)=\cos2\theta\cos30^\circ-\sin2\theta\sin30^\circ$. "
       r"$2\sin2\theta=\cos(2\theta+30^\circ)\Rightarrow\tan2\theta=\frac{\sqrt{3}}{5}\Rightarrow\theta=9.6^\circ,99.6^\circ$ "
       r"The order of the marks needs to match up to the main scheme so 0110 is possible. — B1: For achieving "
       r"$\tan2\theta=\frac{\sqrt{3}}{5}$ o.e so allow $\tan2\theta=$ awrt 0.346 or $\tan2\theta=\frac{\cos30^\circ}"
       r"{2+\sin30^\circ}$ Or via double angle identities $\sqrt{3}\tan^2\theta+10\tan\theta-\sqrt{3}=0$ o.e.",
       r"ALT: Otherwise — M1: Attempts to use the compound angle identities to reach a form $\tan2\theta=k$ where $k$ is a "
       r"constant not $3\sqrt{3}$ (or expression in trig terms such as cos 30 etc as seen above) Or via double angle "
       r"identities reaches a 3TQ in $\tan\theta$",
       r"ALT: Otherwise — dM1: Correct order of operations from $\tan2\theta=k$ leading to $\theta=\ldots$ Correctly solves "
       r"their $\sqrt{3}\tan^2\theta+10\tan\theta-\sqrt{3}=0$ leading to $\theta=\ldots$",
       r"ALT: Otherwise — A1: $\theta=$ awrt $9.6^\circ$, $99.6^\circ$ with no other values given in the range. Note that "
       r"$\tan(2\theta+60^\circ)=3\sqrt{3}\Rightarrow\theta=9.6^\circ,99.6^\circ$ is acceptable for full marks"],
      False, 38),

    # ---------------- Q15 ----------------
    e("15a", "15(a)", TRIG, "5.1, 2.11", 4, LATEX["15a"],
      [r"M1 (AO 3.4): Sets up an allowable equation using volume = 240 E.g. $\frac{1}{2}r^2\times0.8h=240\Rightarrow "
       r"h=\frac{600}{r^2}$ o.e. Notes: Attempts to use the fact that the volume of the toy is 240 cm$^3$ Sight of "
       r"$\frac{1}{2}r^2\times0.8\times h=240$ leading to $h=\ldots$ or $rh=\ldots$ scores this mark But condone an "
       r"equation of the correct form so allow for $kr^2h=240\Rightarrow h=\ldots$ or $rh=\ldots$ [The mark scheme's "
       r"diagram gives Volume $=0.4r^2h$, the sector faces each of area $0.4r^2$, the flat faces each of area $rh$, the "
       r"curved face of area $0.8rh$, and Total surface area $=2rh+0.8r^2+0.8rh$.]",
       r"A1 (AO 1.1b): E.g. $\frac{1}{2}r^2\times0.8h=240\Rightarrow h=\frac{600}{r^2}$ o.e. Notes: A correct expression "
       r"for $h=\frac{600}{r^2}$ or $rh=\frac{600}{r}$ which may be left unsimplified. This may be implied when you see an "
       r"expression for S or part of S E.g $2rh=2r\times\frac{600}{r^2}$",
       r"dM1 (AO 3.4): Attempts to substitute their $h=\frac{600}{r^2}$ into $(S=)\frac{1}{2}r^2\times0.8+\frac{1}{2}r^2"
       r"\times0.8+2rh+0.8rh$. Notes: Attempts to substitute their $h=\frac{a}{r^2}$ o.e. such as $hr=\frac{a}{r}$ into a "
       r"correct expression for $S$ Sight of $\frac{1}{2}r^2\times0.8+\frac{1}{2}r^2\times0.8+rh+rh+0.8rh$ with an "
       r"appropriate substitution Simplified versions such as $0.8r^2+2rh+0.8rh$ used with an appropriate substitution is "
       r"fine.",
       r"A1* (AO 2.1): $S=0.8r^2+2.8rh=0.8r^2+2.8\times\frac{600}{r}=0.8r^2+\frac{1680}{r}$ *. Notes: Correct work leading "
       r"to the given result. S =, SA = or surface area = must be seen at least once in the correct place The method must "
       r"be made clear so expect to see evidence. For example $S=0.8r^2+2rh+0.8rh\Rightarrow S=0.8r^2+2r\times"
       r"\frac{600}{r^2}+0.8r\times\frac{600}{r^2}\Rightarrow S=0.8r^2+\frac{1680}{r}$ would be fine."],
      True, 42),
    e("15b", "15(b)", DIFF, "7.3, 7.2", 4, LATEX["15b"],
      [rf"M1 (AO 3.1a): $\left({DSR}\right)=1.6r-\frac{{1680}}{{r^2}}$. Notes: There is no requirement to see ${DSR}$ in "
       rf"part (b). It may even be called $\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}x}}$. M1: Achieves a derivative of the form "
       rf"$pr\pm\frac{{q}}{{r^2}}$ where $p$ and $q$ are non- zero constants",
       rf"A1 (AO 1.1b): $\left({DSR}\right)=1.6r-\frac{{1680}}{{r^2}}$. Notes: Achieves $\left({DSR}\right)=1.6r-"
       rf"\frac{{1680}}{{r^2}}$",
       rf"dM1 (AO 2.1): Sets ${DSR}=0\Rightarrow r^3=1050$. Notes: Sets or implies that their ${DSR}=0$ and proceeds to "
       rf"$mr^3=n$, $m\times n>0$. It is dependent upon a correct attempt at differentiation. This mark may be implied by "
       rf"a correct answer to their $pr-\frac{{q}}{{r^2}}=0$",
       r"A1 (AO 1.1b): $r=$ awrt 10.2. Notes: $r=$ awrt 10.2 or $\sqrt[3]{1050}$"],
      True, 42),
    e("15c", "15(c)", DIFF, "7.3", 2, LATEX["15c"],
      [rf"M1 (AO 1.1b): Attempts to substitute their positive $r$ into $\left({D2S}\right)=1.6+\frac{{3360}}{{r^3}}$ and "
       rf"considers its value or sign. Notes: Attempts to substitute their positive $r$ (found in (b)) into "
       rf"$\left({D2S}\right)=e\pm\frac{{f}}{{r^3}}$ where $e$ and $f$ are non zero and finds its value or sign. "
       rf"Alternatively considers the sign of $\left({D2S}\right)=e\pm\frac{{f}}{{r^3}}$ (at their positive $r$ found in "
       rf"(b)) Condone the ${D2S}$ to be $\frac{{\mathrm{{d}}^2y}}{{\mathrm{{d}}x^2}}$ or being absent, but only for this "
       rf"mark.",
       rf"A1 (AO 1.1b): E.g. Correct ${D2S}=1.6+\frac{{3360}}{{r^3}}$ with $\left.{D2S}\right|_{{r=10.2}}=5>0$ proving a "
       rf"minimum value of $S$. Notes: States that ${D2S}$ or $S''=1.6+\frac{{3360}}{{r^3}}=$ awrt $5>0$ proving a minimum "
       rf"value of $S$ This is dependent upon having achieved $r=$ awrt 10 and a correct ${D2S}=1.6+\frac{{3360}}{{r^3}}$ "
       rf"It can be argued without finding the value of ${D2S}$. E.g. ${D2S}=1.6+\frac{{3360}}{{r^3}}>0$ as $r>0$ , so "
       rf"minimum value of S. For consistency it is also dependent upon having achieved $r=$ awrt 10 Do NOT allow "
       rf"$\frac{{\mathrm{{d}}^2y}}{{\mathrm{{d}}x^2}}$ for this mark"],
      True, 42),

    # ---------------- Q16 ----------------
    e("16a", "16(a)", INT, "8.3, 3.3, 5.6", 5, LATEX["16a"],
      [r"M1 (AO 2.1): Attempts $y.\frac{\mathrm{d}x}{\mathrm{d}t}=(2\sin2t+3\sin t)\times16\sin t\cos t$ and uses "
       r"$\sin2t=2\sin t\cos t$. Notes: (a) Condone work in another variable, say $\theta\leftrightarrow t$ if used "
       r"consistently for the first 3 marks M1: For the key step in attempting $y.\frac{\mathrm{d}x}{\mathrm{d}t}="
       r"(2\sin2t+3\sin t)\times16\sin t\cos t$ with an attempt to use $\sin2t=2\sin t\cos t$ Condone slips in finding "
       r"$\frac{\mathrm{d}x}{\mathrm{d}t}$ but it must be of the form $k\sin t\cos t$ E.g. I $y.\frac{\mathrm{d}x}"
       r"{\mathrm{d}t}=(2\sin2t+3\sin t)\times k\sin t\cos t=(4\sin t\cos t+3\sin t)\times k\sin t\cos t$ E.g. II "
       r"$y.\frac{\mathrm{d}x}{\mathrm{d}t}=(2\sin2t+3\sin t)\times k\sin t\cos t=(2\sin2t+3\sin t)\times\frac{k}{2}\sin2t$",
       r"A1 (AO 1.1b): Correct expanded integrand. Usually for one of $(R)=\int48\sin^2t\cos t+16\sin^22t\,\mathrm{d}t$ "
       r"$(R)=\int48\sin^2t\cos t+64\sin^2t\cos^2t\,\mathrm{d}t$ $(R)=\int24\sin2t\sin t+16\sin^22t\,\mathrm{d}t$. Notes: A "
       r"correct (expanded) integrand in $t$ . Don't be concerned by the absence of $\int$ or $\mathrm{d}t$ or limits "
       r"$(R)=\int48\sin^2t\cos t+16\sin^22t\,\mathrm{d}t$ or $(R)=\int48\sin^2t\cos t+64\sin^2t\cos^2t\,\mathrm{d}t$ but "
       r"watch for other correct versions such as $(R)=\int24\sin2t\sin t+16\sin^22t\,\mathrm{d}t$",
       r"M1 (AO 1.1b): Attempts to use $\cos4t=1-2\sin^22t=(1-8\sin^2t\cos^2t)$. Notes: Attempts to use "
       r"$\cos4t=\pm1\pm2\times\sin^22t$ to get the integrand in the correct form. If they have the form $P\sin^22t$ it is "
       r"acceptable to write $P\sin^22t=\frac{P}{2}(\pm1\pm\cos4t)$ If they have the form $Q\sin^2t\cos^2t$ sight and use "
       r"of $\sin2t$ and/or $\cos2t$ will usually be seen first. There are many ways to do this, below is such an example "
       r"$Q\sin^2t\cos^2t=Q\left(\frac{1-\cos2t}{2}\right)\left(\frac{1+\cos2t}{2}\right)=Q\left(\frac{1-\cos^22t}{4}\right)"
       r"=Q\left(\frac{1}{4}-\frac{\cos^22t}{4}\right)=Q\left(\frac{1}{4}-\frac{1+\cos4t}{8}\right)$ Allow candidates to "
       r"start with the given answer and work backwards using the same rules. So expect to see "
       r"$\cos4t=\pm1\pm2\times\sin^22t$ or $\cos4t=\pm2\times\cos^22t\pm1$ before double angle identities for $\sin2t$ or "
       r"$\cos2t$ are used.",
       r"A1* (AO 2.1): $R=\int_0^a8-8\cos4t+48\sin^2t\cos t\,\mathrm{d}t$ *. Notes: Proceeds to the given answer with "
       r"correct working. The order of the terms is not important. Ignore limits for this mark. The integration sign and "
       r"the $\mathrm{d}t$ must be seen on their final answer. If they have worked backwards there must be a concluding "
       r"statement to the effect that they know that they have shown it. The integration sign and the $\mathrm{d}t$ must "
       r"also be seen E.g. Reaches $\int48\sin^2t\cos t+64\sin^2t\cos^2t\,\mathrm{d}t$ Answer is "
       r"$\int8-8\cos4t+48\sin^2t\cos t\,\mathrm{d}t=\int8-8(1-2\sin^22t)+48\sin^2t\cos t\,\mathrm{d}t=\int16\sin^22t+"
       r"48\sin^2t\cos t\,\mathrm{d}t=\int64\sin^2t\cos^2t+48\sin^2t\cos t\,\mathrm{d}t$ which is the same, ✓",
       r"B1 (AO 2.2a): Deduces $a=\frac{\pi}{4}$. Notes: Deduces $a=\frac{\pi}{4}$. It may be awarded from the upper limit "
       r"and can be awarded from (b)"],
      True, 46),
    e("16b", "16(b)", INT, "8.2, 8.3", 4, LATEX["16b"],
      [r"M1 (AO 2.1): $\int8-8\cos4t+48\sin^2t\cos t\,\mathrm{d}t=8t-2\sin4t+16\sin^3t$. Notes: For the key process in "
       r"using a correct approach to integrating the trigonometric terms. May be done separately. There may be lots of "
       r"intermediate steps (e.g. let $u=\sin t$). There are other more complicated methods so look carefully at what they "
       r"are doing. $\int8-8\cos4t+48\sin^2t\cos t\,\mathrm{d}t=\ldots\pm P\sin4t\pm Q\sin^3t$ where $P$ and $Q$ are "
       r"constants",
       r"A1 (AO 1.1b): $\int8-8\cos4t+48\sin^2t\cos t\,\mathrm{d}t=8t-2\sin4t+16\sin^3t$. Notes: $\int8-8\cos4t+48\sin^2t"
       r"\cos t\,\mathrm{d}t=8t-2\sin4t+16\sin^3t(+c)$ If they have written $16\sin^3t$ as $16\sin t^3$ only award if "
       r"further work implies a correct answer. Similarly, $8t$ may be written as $8x$. Award if further work implies "
       r"$8t$, e.g. substituting in their limits. Do not penalise this sort of slip at all, these are intermediate "
       r"answers.",
       r"M1 (AO 2.1): $\left[8t-2\sin4t+16\sin^3t\right]_0^{\frac{\pi}{4}}=2\pi+4\sqrt{2}$. Notes: Uses the limits their $a$ "
       r"and 0 where $a=\frac{\pi}{6},\frac{\pi}{4}$ or $\frac{\pi}{3}$ in an expression of the form "
       r"$kt\pm P\sin4t\pm Q\sin^3t$ leading to an exact answer. Ignore evidence at lower limit as terms are 0",
       r"A1 (AO 1.1b): $\left[8t-2\sin4t+16\sin^3t\right]_0^{\frac{\pi}{4}}=2\pi+4\sqrt{2}$. Notes: CSO $2\pi+4\sqrt{2}$ or "
       r"exact simplified equivalent such as $2\pi+\frac{8}{\sqrt{2}}$ or $2\pi+\sqrt{32}$ . Be aware that "
       r"$\int_0^{\frac{\pi}{4}}8-8\cos4t+48\sin^2t\cos t\,\mathrm{d}t=8t+\lambda\sin4t+16\sin^3t(+c)$ would lead to the "
       r"correct answer but would only score M1 A0 M1 A0"],
      True, 46),
]

# Examiner report, sentence by sentence, in report order (the General Comments
# are not attached to any question). Bulleted lists are joined into the sentence
# that introduces them, with "; ".
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "This was an accessible question for virtually all candidates.", NO),
        (W, "It asked for the point to which $P$ was mapped, and most candidates gave this as a coordinate pair.", NO),
        ({"a"}, "Part (a) was frequently correct; candidates identified the translation and applied it successfully.", NO),
        ({"b"}, "The attempts at part (b) were less successful."),
        ({"b"}, "Most solutions used the modulus concept but applied it to both coordinates.", NO),
        ({"c"}, "Part (c) was a 3-stage transformation and required the candidates to identify both the transformations "
                "and the order in which they were to be applied."),
        ({"c"}, "This was more of a challenge.", BACK),
        ({"c"}, "In particular, the stretch parallel to the $y$-axis and final translation were mixed up; those who did, "
                "generally received some credit as they obtained $x=0$.", NO),
    ],
    "02": [
        (W, "This was a familiar and accessible question with most candidates scoring 2 or 3 marks.", NO),
        (W, "The most common and successful approach was via the use of the factor theorem."),
        (W, r"Following on from setting $\mathrm{f}(-2)=0$, most candidates were able to set up and solve the linear "
            r"equation in $k$."),
        (W, r"Errors seen resulting in the loss of marks were: having $(10k)$ not $(10+k)$ in the linear equation; "
            r"expanding $-6(10+k)$ to $\pm60\pm k$, or making a sign error on the final stage to get $k$=17; setting "
            r"$\mathrm{f}(2)=0$; expanding the expression before substituting, often leading to sign errors or the loss "
            r"of the 42"),
        (W, "There was a small proportion of candidates who tried to use algebraic division to solve the problem, but "
            "most did not score many marks since the working needed here was much more complicated."),
        (W, "Often the division was left incomplete, or there was not a linear remainder in $k$ to set equal to zero."),
        (W, "Even fewer candidates attempted factorisation by inspection; only a handful of candidates gained marks "
            "using this method.", NO),
    ],
    "03": [
        (W, "This question on the geometry of a circle had standard bookwork in part (a) followed by problem solving in "
            "part (b).", NO),
        ({"b"}, "Success in part (b) was usually achieved by candidates who drew a diagram."),
        ({"a"}, "In part (a) most candidates scored all three marks."),
        ({"a"}, r"Some candidates made sign errors when completing the square but still obtained some version of "
                r"$(\pm5,\pm8)$."),
        ({"a"}, "Many candidates were still able to get the correct radius following this slip.", NO),
        ({"a"}, "A significant minority of candidates obtained a centre of $(5,-4)$ seemingly from square rooting the 16 "
                "rather than halving."),
        ({"b"}, "In part (b), there was full follow through on the centre and radius, which allowed many candidates to "
                "score full marks despite errors in part (a)."),
        ({"b"}, "Candidates who drew a diagram worked out that they need to find the distance of the centre from the "
                "origin and add on the radius."),
        ({"b"}, "One lengthy method involved finding the intersection of the circle with the line through $O$ and $C$, "
                "but this was unlikely to give the requested exact answer, and some candidates gave up at the point "
                "where the quadratic had to be solved as it had unpleasant coefficients.", BACK),
        ({"b"}, r"A common error was based on simply doubling the radius, either as 26 or finding the length of the "
                r"vector $(10,-16)$ as $2\sqrt{89}$."),
    ],
    "04": [
        (W, "This was a generously worded question with plenty of guidance to help candidates throughout.", NO),
        (W, "As a result, it was generally well attempted, with many candidates scoring full marks.", BACK),
        ({"a"}, "There were a number of candidates who made no attempt at part (a) despite the guidance to express the "
                "given sum as an integral."),
        ({"a"}, "Where candidates had used the information given in the question the correct answer was relatively easy "
                "to deduce."),
        ({"a"}, r"Common errors seen in part (a) were omitting the limits or the $\mathrm{d}x$, and writing "
                r"$\mathrm{d}x$ as $\delta x$ (although this was condoned).", NO),
        ({"b"}, "Candidates who had attempted part (a) generally went on to attempt part (b)."),
        ({"b"}, "Most candidates provided a fully correct solution and gained both marks."),
        ({"b"}, "Where errors were made, this was usually at the last mark.", NO),
        ({"b"}, r"Common errors seen were; incorrectly integrating the expression to $\ln x$ or $\ln2x$; differentiating "
                r"$\frac{2}{x}$ rather than integrating it; leaving the answer as 2ln3 rather than ln9", NO),
    ],
    "05": [
        (W, "This question involved solving simultaneous equations set within the context of the height of a tree "
            "modelled over a number of years."),
        (W, "The question was very accessible for many candidates."),
        ({"a"}, "In part (a) the majority of candidates gained the first three marks for forming and solving two correct "
                "simultaneous equations."),
        ({"a"}, "Many went to a great deal of effort to solve the simultaneous equations using algebraic methods, "
                "whereas some just put the equations into a calculator and wrote down the values of the constants $a$ "
                "and $b$."),
        ({"a"}, "Some candidates used the 3 significant figure value of $a$ to subsequently find the value of $b$, "
                "resulting in finding $b$ as 1.94 rather than 1.95 and thus losing the final A mark."),
        ({"a"}, "A significant number of candidates correctly found the values of the constants $a$ and $b$, but then "
                "failed to state the equation of the model explicitly anywhere in their answer, losing the final A "
                "mark."),
        ({"b"}, "In part (b) most candidates realised they had to substitute either $t$ =20 or $h$ =7 into their model "
                "and compare the value obtained with the given values."),
        ({"b"}, "However, some candidates did not know how to evaluate the model with several coming to the wrong "
                "conclusion that the model was poor, because it didn’t give the exact values for $h$ or $t$.", NO),
        ({"b"}, "There were quite a few candidates who correctly calculated the percentage error as an impressive "
                "comparison."),
        ({"b"}, "It is very important for candidates to give a reason for their answer when the question explicitly "
                "demands it.", NO),
    ],
    "06": [
        (W, "There was a very mixed response to this question on a cubic function with only one in eight candidates "
            "scoring all 6 marks.", NO),
        ({"a"}, r"Part (a) was for finding the set of values of $x$ for which $\mathrm{f}'(x)<0$."),
        ({"a"}, "Candidates generally knew what to do and most scored this B mark.", NO),
        ({"a"}, r"Marks were lost when candidates gave the inequality as $2\leqslant x\leqslant6$ or else "
                r"$2<\mathrm{f}'(x)<6$ ."),
        ({"b"}, "In part (b) the request to give the answer in set notation proved a challenge for many candidates, with "
                "many only gaining the M mark for correctly identifying at least one of the correct inequalities."),
        ({"b"}, r"A minority of candidates gained both marks by giving their answer in acceptable set notation but there "
                r"was widespread misapplication of $\cap$ rather than $\cup$."),
        ({"c"}, "Part (c) required the candidates to find the equation of the curve."),
        ({"c"}, "A very common response, which gained only the first mark, was to give their answer as $y=x(x-6)^2$ "
                "without any appreciation of the stretch factor."),
        ({"c"}, "Candidates who did appreciate that it could be $y=ax(x-6)^2$ could easily use the coordinate (2, 8) to "
                "find the value of $a$ and hence the equation of the curve.", NO),
        ({"c"}, r"A sizeable minority of otherwise good candidates lost the final mark by incorrectly writing down the "
                r"equation of the curve as $C=\frac{1}{4}x(x-6)^2$ ."),
        ({"c"}, "There were many more time consuming and long winded methods seen here."),
        ({"c"}, r"A significant number of candidates formed the equation of a cubic, i.e. $y=ax^3+bx^2+cx+d$ and then "
                r"attempted to use the points on the curve to find the values of $a$, $b$, $c$ and $d$."),
        ({"c"}, "This approach was rarely fully correct with many failing to identify that $d$ = 0 or being able to form "
                "only 2 equations.", BACK),
        ({"c"}, r"A small minority of candidates did attempt to use the turning points at $x=2$ and $x=6$ to form the "
                r"equation $\frac{\mathrm{d}y}{\mathrm{d}x}=(x-2)(x-6)$ without again, an appreciation of the need for a "
                r"stretch factor."),
        ({"c"}, "It was disappointing to see how many candidates got bogged down in pages of algebraic working without "
                "noticing that this part of the question was only worth 3 marks.", NO),
    ],
    "07": [
        (W, "This question, on two different kinds of proof, proved more demanding than expected.", NO),
        (W, "As a result, there were very few completely correct solutions to both parts of this question.", NO),
        ({"i"}, "In part (i) candidates were often unable to set up a proof by contradiction using appropriate language, "
                "failing to use words such as 'assume', 'there exists' or 'let' .", NO),
        ({"i"}, "Others simply set up a contradiction such as 'assume $p$ and $q$ are odd' without any reference to $pq$ "
                "being even.", NO),
        ({"i"}, "Many candidates also failed to use different variables for their odd numbers $p$ and $q$, implying that "
                "$p$ and $q$ were either the same odd number, or two consecutive odd numbers such as $2n$+1 and "
                "$2n$+3.", NO),
        ({"i"}, "Candidates who managed to write $p$ and $q$ using different variables were generally able to multiply "
                "out $pq$ correctly and write it in the form 2(.....)+1.", NO),
        ({"i"}, "If this stage was reached, the conclusion was generally correct and an acceptable sentence was written "
                "down.", BACK),
        ({"i"}, "A mark of 011 was possible from the mark scheme."),
        ({"ii"}, "In part (ii) most candidates expanded the left hand side and cancelled terms getting to $2xy<8x^2$ or "
                 "equivalent for the method mark."),
        ({"ii"}, "Many then lost the second mark by failing to identify the point at which the inequality reverses, "
                 "simply writing down $y<4x$ followed by 'so $y>4x$'."),
        ({"ii"}, "Other candidates did reverse the inequality at the right point but didn't give an explanation as to "
                 "why, and so lost the final mark."),
    ],
    "08": [
        (W, "This was the second modelling question on the paper.", NO),
        (W, "The given equation modelled the speed of a car as it travelled between a pair of traffic lights.", NO),
        ({"a", "c"}, "Many weaker candidates missed out part (b) and scored marks in the more accessible parts (a) and "
                     "(c)."),
        ({"a"}, "Most candidates managed to reach the correct answer of 25 in part (a)."),
        ({"a"}, "A common incorrect answer was 10, possibly from sight of the 10 in the given equation "
                "$v=(10-0.4t)\\ln(t+1)$"),
        ({"b"}, "The first two marks in part (b) were often achieved by those who attempted it.", NO),
        ({"b"}, r"Using the product rule to find $\frac{\mathrm{d}v}{\mathrm{d}t}$ and then setting this = 0 gave them "
                r"one form of the given equation.", NO),
        ({"b"}, "The final two marks were only achieved by the best of students."),
        ({"b"}, "In reality, all that was required was to make $t$ the subject of the formula, but it was beyond most.",
         NO),
        ({"c"}, "Part (c) was the most successful part of the question and familiar to most candidates."),
        ({"c"}, "Many were able to carry out the iteration process correctly, and write down 7.298 without any "
                "problems."),
        ({"c"}, "In part (c) (ii), the omission of the units, “seconds”, was the most common slip."),
    ],
    "09": [
        (W, "This vector question was set within the context of a rhombus.", NO),
        (W, "Surprisingly, many candidates were unable to use (or remember) the basic geometric of a rhombus and over "
            "30% did not manage to make any progress."),
        ({"a"}, "Part (a) required candidates to show that parallelogram $PQRS$ was a rhombus."),
        ({"a"}, "Although the requirement to 'show' is becoming more familiar to candidates, a significant number in "
                "this case didn't recognise the level of detail expected.", NO),
        ({"a"}, r"So a lack of conclusion, or stating the sides were of length $\sqrt{29}$ without evidence of "
                r"calculation, led to loss of credit."),
        ({"a"}, "It was also necessary to conclude that the sides were equal, and not simply find the lengths and leave "
                "it to the reader to decide.", NO),
        ({"b"}, "A vast array of approaches were in evidence in part (b) to find the area of the rhombus."),
        ({"b"}, r"The easiest and most direct approach was to find $\frac{1}{2}\left|PR\right|\times\left|QS\right|$ ."),
        ({"b"}, "A more common method used involved finding the length of one diagonal, followed by the cosine rule to "
                "find an internal angle and then use of the formula '$ab\\sin C$ '."),
        ({"b"}, r"Unfortunately most attempts using this method only scored 3 marks as it was usual for answers to be "
                r"given as 22.7 rather than the one required, $\sqrt{517}$.", NO),
        ({"b"}, "Other methods seen involved use of Heron’s formula, the “shoelace” determinant method, scalar product "
                "and vector product….. with many successfully used."),
        ({"b"}, "Students who added a “narrative” – so explaining what they attempted to do – were in a better position "
                "to gain credit if they suffered a processing error early in their solution."),
        ({"b"}, "This has to be considered good practice.", BACK),
        ({"b"}, r"The most common incorrect solution, seen many times over was in stating area = "
                r"$\left|PQ\right|\times\left|PS\right|=\sqrt{29}\times\sqrt{29}=29$"),
    ],
    "10": [
        (W, "This was the third modelling question on the paper, this time based around an exponential model.", NO),
        ({"a", "b"}, "This should have been expected given the Advance Information and candidates performed well on "
                     "parts (a) and (b).", NO),
        ({"c"}, "Part (c) was more of a challenge with only higher achieving students scoring all 4 marks."),
        ({"a"}, "Part (a) was either answered correctly, or the mark was not awarded because the answer stated was 265 "
                "bees not 265,000 bees."),
        ({"b"}, "Most candidates recognised the need to differentiate in part (b), and used appropriate notation."),
        ({"b"}, "Most did this accurately before substituting in $t$ =10 to obtain 18.1.", NO),
        ({"b"}, "A number of candidates failed to secure the final mark however, for not providing a minimal conclusion "
                "relating their answer to 18,000."),
        ({"b"}, r"Common reasons for not achieving full marks were failing to use appropriate notation often using "
                r"$\frac{\mathrm{d}y}{\mathrm{d}x}$ instead of $\frac{\mathrm{d}N}{\mathrm{d}t}$; failing to recognise "
                r"the need to use differentiation often subtracting the values of $N_b$ at $t$ =9 and 10 or else $t$ =10 "
                r"and 11"),
        ({"c"}, "Part (c) was the most demanding part of the question with many candidates just picking up the first "
                "mark for equating the two expressions."),
        ({"c"}, "Having equated the two expressions, the significance of the negative exponential term seemed to be "
                "poorly understood."),
        ({"c"}, r"Very common errors included changing the $\mathrm{e}^{-0.05t}$ term to $\mathrm{e}^{0.05t}$ and then "
                r"solving; applying 'ln' to each term in the equation to form a linear equation in $t$; slips in "
                r"coefficients with 220 becoming 200"),
        ({"c"}, "A number of candidates reverted to numerical methods or the use of their calculator to solve the "
                "equation rather than solve by algebraic methods."),
        ({"c"}, r"The strongest candidates recognised the quadratic equation in $\mathrm{e}^{0.05t}$ and were able then "
                r"to solve it correctly, many after making a substitution $x=\mathrm{e}^{0.05t}$ .", NO),
    ],
    "11": [
        (W, "This question was based around the intersection of a cubic and a quadratic equation."),
        (W, "It proved to be very accessible with many candidates able to make progress in both parts.", BACK),
        (W, "In fact 30% of all candidates scored full marks on this question.", NO),
        ({"a"}, r"Part (a) asked candidates to verify that the curves intersect at $x=\frac{1}{2}$."),
        ({"a"}, r"The easiest and most common approach was to substitute $x=\frac{1}{2}$ into both equations, obtain $y$ "
                r"values of $\frac{41}{4}$ in each and then conclude that the curves did intersect."),
        ({"a"}, "Candidates using this approach generally scored the method mark, but some lost the accuracy mark "
                "either from failing to show full details of the calculations, or from failing to state the conclusion "
                "that the curves intersect.", NO),
        ({"a"}, r"Other methods seen included setting the equations of the curves equal, rearranging to form a cubic, "
                r"and then showing that $x=\frac{1}{2}$ satisfied the resulting equation. Again, most gained the method "
                r"mark, but again some lost the accuracy mark due to a lack of a conclusion; setting the equations of the "
                r"curves equal, rearranging to form a cubic, using the calculator to solve the cubic equation and then "
                r"writing down the three solutions, indicating that one of the solutions was $x=\frac{1}{2}$. This "
                r"approach could only achieve the method mark here."),
        ({"b"}, "In part (b) most candidates made some progress with weaker students scoring only the first mark for "
                "setting up the cubic equation."),
        ({"b"}, r"The majority were then able to divide by either $\left(x-\frac{1}{2}\right)$ or $(2x-1)$ to form a "
                r"quadratic factor and then equation which could then be solved to find the positive root."),
        ({"b"}, r"Marks lost were usually as a result of slips in establishing the cubic equation or else errors in the "
                r"division; not giving the exact answer of $-4+\sqrt{33}$ but instead its decimal equivalent; using a "
                r"calculator to solve the cubic equation $2x^3+15x^2-42x+17=0$"),
    ],
    "12": [
        (W, "This was a very straight forward question on integration by parts with 40% of the candidates scoring full "
            "marks.", NO),
        (W, "On the reverse side there were also a sizeable number, some 30%, who did not know how to begin and failed "
            "to score any marks."),
        (W, "Those candidates who knew the method nearly always scored 3, 4 or 5 marks.", NO),
        (W, r"Reasons for these candidates dropping 1 or 2 marks nearly always centred around a failure to integrate the "
            r"term $\frac{x^4}{4}\times\frac{1}{x}$ correctly, many times to $\frac{x^4}{12}$; failing to correctly "
            r"apply the limits, usually achieving $\frac{7}{16}\mathrm{e}^8-\frac{1}{16}$; achieving a correct answer of "
            r"$\frac{7}{16}\mathrm{e}^8+\frac{1}{16}$ then inexplicably “simplifying” this to $7\mathrm{e}^8+1$", BACK),
        (W, r"Low scoring candidates who attempted the question, usually resorted to integrating each term of the "
            r"integrand or else having made a good start, disappointingly integrating the $\frac{x^4}{4}\times\frac{1}{x}$ "
            r"term to $\frac{x^5}{20}\times\ln x$"),
    ],
    "13": [
        (W, "This question on arithmetic sequences and series proved to be very discriminating.", NO),
        ({"i"}, "The proof of the sum of an arithmetic sequence is standard, but was not answered well by many "
                "candidates."),
        ({"iia", "iib", "iic"}, "Most candidates however were able to then made progress with the rest of the "
                                "question, having been given the required formula."),
        (W, "Good candidates often did well in this question however, with 17% of the cohort achieving full marks.",
         NO),
        ({"i"}, "In part(i) those who had learned the standard proof for the sum of the first $n$ terms of an arithmetic "
                "series often gained full marks.", NO),
        ({"i"}, "It was however, unusual to see a well set out, fully correct proof.", NO),
        ({"i"}, "Candidates often failed to write a correct expression for $S_n$ at the start of their proof, or "
                "sometimes having an incorrect first or last term or extra terms (most often $a+nd$) within their sum."),
        ({"i"}, "Other errors included not displaying a sufficient number of terms, not writing $S$= or $S_n$ =, and "
                "using commas instead of + sign between the terms."),
        ({"iia", "iib", "iic"}, "In part(ii) most realised that they could make headway even if they hadn’t attempted "
                                "part (i)."),
        ({"iia"}, "In (ii) (a) many of the candidates used $a$=20, $d$ = –0.8 and $S_n$ = 64 in the sum formula to score "
                  "the M mark.", {"note": "the question gives a first term of £10 and the mark scheme writes $2\times10$ in the sum formula"}),
        ({"iia"}, r"Poor notation such as $(n-1)-0.8$ was frequently seen, but candidates usually recovered from this.", NO),
        ({"iia"}, "Following a correct equation most were able to proceed correctly to the given quadratic for the "
                  "accuracy mark."),
        ({"iia"}, "A common error was where candidates used +0.8 as the common difference rather than –0.8"),
        ({"iib"}, "Part (ii) (b) was generally answered without issues."),
        ({"iib"}, "Almost all candidates managed to get B1 for getting the two values of $n$, either by factorising or "
                  "by using a calculator."),
        ({"iic"}, "Part (ii)(c) was not answered very well with most candidates identifying 10 as the valid solution but "
                  "not adequately justifying this choice.", NO),
        ({"iic"}, "The reasons provided were often too vague or not related to why 10 was better than 16."),
        ({"iic"}, "More tended to score the mark by explaining that at 16 weeks he would be saving a negative amount "
                  "rather than using the fact that 10 was the smaller number or that he would have had enough by 10 "
                  "weeks so would not continue saving until 16 weeks."),
    ],
    "14": [
        (W, "This question was another big discriminator.", NO),
        (W, "Good candidates found it familiar and accessible with some 25% scoring full marks.", NO),
        (W, "Strangely, for candidates who dropped marks, they seemed to be able to do either part (a) or part (b), but "
            "not both."),
        ({"a"}, "For those candidates who attempted part (a) most recognised the need to use the compound angle "
                "expansions.", NO),
        ({"a"}, "Carelessness with the multiplication by 2, signs and use of the formulas was seen in a small minority "
                "of the scripts."),
        ({"a"}, "Students who attempted to use sin ($A$+$B$) and cos ($A$+$B$) with a negative angle $B$, often "
                "introduced sign errors; it is clear that such a method is not to be recommended.", NO),
        ({"a"}, "Substituting exact numerical values was usually correct, however candidates occasionally fudged their "
                "working to get the given answer."),
        ({"b"}, "Part (b) could be attempted without having done part (a) and many took up this opportunity.", NO),
        ({"b"}, r"Those who paid attention to the 'hence', deducing that $x=2\theta+60$, were very successful in achieving "
                r"the correct answers, though quite a few only found one solution.", NO),
        ({"b"}, "For the many students who did not see the link between parts (a) and (b), generally encountered much "
                "more complex, longer algebraic manipulation."),
        ({"b"}, "Such students re-started the question using the compound angle formulae with a combination of other "
                "trigonometric identities, but were often not able to reach an equation in one function, or else made "
                "numerous slips.", BACK),
        ({"b"}, r"If quadratics in tan $\theta$ were reached, they were dealt with competently."),
        ({"b"}, r"If the candidate’s efforts led to $\tan2\theta=k$, $k\neq3\sqrt{3}$ or $\tan(2\theta\pm60)=3\sqrt{3}$ "
                r"they were generally able to use the correct order of operations to solve their equation to find at "
                r"least one solution."),
        ({"b"}, "A fair number of correct answers were seen written down without any correct working."),
        ({"b"}, "As the question had a warning about the use of calculator technology, these responses gained no marks",
         BACK),
    ],
    "15": [
        (W, "This question, based on the minimum surface area of a children's toy proved to be a useful source of marks "
            "so late in the paper.", NO),
        (W, "In fact 25% of the cohort achieved full marks."),
        ({"b", "c"}, "Many candidates who could not access part (a) were able to use their skills in differentiation to "
                     "find an appropriate value for the radius and prove that their value gave a minimum surface "
                     "area."),
        ({"a"}, "Unsurprisingly, part (a) was the most demanding part of this question.", NO),
        ({"a"}, "The key was to find an expression (using the volume of 240 cm$^3$) for $h$ in terms of $r$."),
        ({"a"}, "Unfortunately some solutions featured the volume of a sphere, which proved a costly error, from which "
                "there was no return."),
        ({"a"}, "Candidates produced their formula for surface area in a variety of ways – sometimes leaving it to the "
                "last line to substitute in the value for the angle, occasionally replacing 0.8 by 4/5.", NO),
        ({"a"}, "As with other “show” questions, sufficient detail has to be written to convince the reader that "
                "progress is genuine."),
        ({"b"}, "Part (b) well generally well done."),
        ({"b"}, r"Many candidates scored full marks for reaching either $\sqrt[3]{1050}$ or 10.2."),
        ({"b"}, r"Occasionally some candidates mistakenly wrote down $\sqrt{1050}$ and subsequently simplified their "
                r"answer to $5\sqrt{42}$ ."),
        ({"b"}, "Very few candidates who attempted this part failed to score marks.", NO),
        ({"b"}, r"The main reason for this was usually an inability to differentiate $\frac{1680}{r}$ which usually became "
                r"$\frac{1680}{1}$ or $1680\ln r$", BACK),
        ({"c"}, "Most candidates were able to find the second derivative correctly in part (c)."),
        ({"c"}, "How it should be used was confused in much of the work seen.", BACK),
        ({"c"}, r"Common reasons for a loss of marks here were; candidates solving the equation "
                r"$\frac{\mathrm{d}^2S}{\mathrm{d}r^2}$ = 0; use of incorrect notation including "
                r"$\frac{\mathrm{d}^2S}{\mathrm{d}r^2}$ and $\frac{\mathrm{d}^2y}{\mathrm{d}x^2}$; incomplete solutions "
                r"with calculations or conclusions missing"),
    ],
    "16": [
        (W, "The final question on the paper proved to be a challenge for many candidates and there were several blank "
            "responses seen.", NO),
        (W, "It is possible that this was due to time management.", BACK),
        (W, "Some candidates attempted unsuccessfully to change to a Cartesian equation, suggesting that possibly "
            "parametric integration had not been covered."),
        ({"a"}, r"In part (a), candidates who recognised the need to use parametric integration were usually able to "
                r"differentiate correctly to find $\frac{\mathrm{d}x}{\mathrm{d}t}$, multiply this by $y$ and then use "
                r"the double angle formulae to find an acceptable expression for $y\frac{\mathrm{d}x}{\mathrm{d}t}$.",
         NO),
        ({"a"}, "It was common for candidates to score the first two marks.", NO),
        ({"a"}, "The next two marks were more elusive, and it was common to see candidates perform a lot of onerous "
                "manipulation without making any significant progress.", NO),
        ({"a"}, r"Those who were most likely to be successful were the ones who had an expression in terms of "
                r"$\sin^22t$ and then spotting the need to use the double angle formula to form a term in cos 4t.", NO),
        ({"a"}, "For many candidates the mark for the upper limit was all that was achieved in part (a)."),
        ({"a"}, "However, some failed to achieve it as they left it as 4 (value for $x$ not $t$) or 45 (degrees).", BACK),
        ({"b"}, "It was good to see students who were unsuccessful at part (a) still attempting part (b), and in some "
                "cases scoring full marks.", NO),
        ({"b"}, "Most candidates were able to integrate the first two terms correctly, but a significant proportion were "
                "unable to integrate the third term to get an expression in $\\sin^3t$."),
        ({"b"}, "The majority of correct solutions came from the use of the reverse chain rule for the final term."),
        ({"b"}, "Those who attempted to use integration by substitution or by parts were usually unsuccessful.", NO),
        ({"b"}, "Candidates who had successfully completed the integration often went on to score full marks."),
    ],
}

# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
RATINGS = {
    "01a": ("easy", ("01", 2)),
    "01b": ("medium", ("01", 3)),
    "01c": ("medium", ("01", 6)),
    "02": ("easy", ("02", 0)),
    "03a": ("easy", ("03", 2)),
    "03b": ("medium", ("03", 6)),
    "04a": ("medium", ("04", 2)),
    "04b": ("easy", ("04", 6)),
    "05a": ("medium", ("05", 5)),
    "05b": ("medium", ("05", 7)),
    "06a": ("easy", ("06", 2)),
    "06b": ("medium", ("06", 4)),
    "06c": ("hard", ("06", 7)),
    "07i": ("hard", ("07", 2)),
    "07ii": ("medium", ("07", 9)),
    "08a": ("easy", ("08", 3)),
    "08b": ("hard", ("08", 7)),
    "08c": ("easy", ("08", 9)),
    "09a": ("medium", ("09", 3)),
    "09b": ("hard", ("09", 9)),
    "10a": ("easy", ("10", 1)),
    "10b": ("easy", ("10", 5)),
    "10c": ("hard", ("10", 8)),
    "11a": ("easy", ("11", 1)),
    "11b": ("easy", ("11", 8)),
    "12": ("medium", ("12", 1)),
    "13i": ("hard", ("13", 5)),
    "13iia": ("easy", ("13", 11)),
    "13iib": ("easy", ("13", 14)),
    "13iic": ("hard", ("13", 15)),
    "14a": ("easy", ("14", 3)),
    "14b": ("medium", ("14", 8)),
    "15a": ("hard", ("15", 3)),
    "15b": ("easy", ("15", 8)),
    "15c": ("medium", ("15", 14)),
    "16a": ("hard", ("16", 5)),
    "16b": ("medium", ("16", 10)),
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
