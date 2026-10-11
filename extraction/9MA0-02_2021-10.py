"""Draft builder for 9MA0-02 2021-10 (A level Pure Paper 2, October 2021).

Run (from the project root, with the venv active):
    python extraction/9MA0-02_2021-10.py        # writes out/drafts/9MA0-02_2021-10.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-02_2021-10.json

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

P, S = "9MA0-02", "2021-10"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "12aii"); label as printed (e.g. "12(a)(ii)")."""
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


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


DYDX = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
D2YDX2 = r"\frac{\mathrm{d}^2y}{\mathrm{d}x^2}"
CALC = ["In this question you should show all stages of your working.",
        "Solutions relying entirely on calculator technology are not acceptable."]

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q1 = ["In an arithmetic series", "• the first term is 16", "• the 21st term is 24"]
Q1A = "Find the common difference of the series."
Q2 = ["The functions f and g are defined by",
      r"$$\mathrm{f}(x)=7-2x^2\qquad x\in\mathbb{R}$$",
      r"$$\mathrm{g}(x)=\frac{3x}{5x-1}\qquad x\in\mathbb{R}\qquad x\neq\frac{1}{5}$$"]
Q5 = [r"The curve $C$ has equation", r"$$y=5x^4-24x^3+42x^2-32x+11\qquad x\in\mathbb{R}$$"]
Q5A = ["Find", r"(i) $" + DYDX + "$", r"(ii) $" + D2YDX2 + "$"]
Q6 = [r"[Figure 1: a logo made of three sectors, symmetrical about a vertical line through $O$. $A$, $O$ and $F$ lie "
      r"on a horizontal straight line, with $AO$ and $OF$ each labelled $r$. Arc $AB$ and arc $FE$ are short "
      r"arcs centred on $O$ rising from $A$ and $F$ to $B$ and $E$. The radii from $O$ through $B$ to $C$ and from $O$ "
      r"through $E$ to $D$ are dashed from $O$ to $B$ and to $E$ and solid beyond; $OC$ and $OD$ are each labelled "
      r"$2r$. Arc $CD$, centred on $O$, joins $C$ and $D$ across the top. The angle $\theta$ is marked at $O$ between "
      r"$OB$ and $OE$.]",
      r"The shape $OABCDEFO$ shown in Figure 1 is a design for a logo.",
      "In the design",
      r"• $OAB$ is a sector of a circle centre $O$ and radius $r$",
      r"• sector $OFE$ is congruent to sector $OAB$",
      r"• $ODC$ is a sector of a circle centre $O$ and radius $2r$",
      r"• $AOF$ is a straight line",
      r"Given that the size of angle $COD$ is $\theta$ radians,"]
Q6A = r"write down, in terms of $\theta$, the size of angle $AOB$"
Q7 = [*CALC,
      r"[Figure 2: the curve $C$ comes up steeply from below, crossing the negative $y$-axis, rises to a maximum just "
      r"below the $x$-axis, falls to the point $P(5,-13)$ and then rises steeply, crossing the positive $x$-axis. The "
      r"straight line $l$ touches $C$ at $P$, meets $C$ again where they both cross the negative $y$-axis, and crosses "
      r"the positive $x$-axis further to the right. The finite region $R$ between $C$ and $l$, from the $y$-axis to "
      r"$P$, is shaded.]",
      r"Figure 2 shows a sketch of part of the curve $C$ with equation",
      r"$$y=x^3-10x^2+27x-23$$",
      r"The point $P(5,-13)$ lies on $C$",
      r"The line $l$ is the tangent to $C$ at $P$"]
Q7A = (r"Use differentiation to find the equation of $l$, giving your answer in the form $y=mx+c$ where $m$ and $c$ "
       r"are integers to be found.")
Q7B = r"(b) Hence verify that $l$ meets $C$ again on the $y$-axis."
Q8 = [r"The curve $C$ has equation", r"$$px^3+qxy+3y^2=26$$", r"where $p$ and $q$ are constants."]
Q8A = ["Show that", r"$$" + DYDX + r"=\frac{apx^2+bqy}{qx+cy}$$", r"where $a$, $b$ and $c$ are integers to be found."]
Q10 = [r"The time, $T$ seconds, that a pendulum takes to complete one swing is modelled by the formula",
       r"$$T=al^b$$",
       r"where $l$ metres is the length of the pendulum and $a$ and $b$ are constants."]
Q10A = ["Show that this relationship can be written in the form", r"$$\log_{10}T=b\log_{10}l+\log_{10}a$$"]
Q10F = [r"[Figure 3: axes $\log_{10}l$ (horizontal) and $\log_{10}T$ (vertical) with origin $O$; a straight line "
        r"segment rises from the point $(-0.7,0)$ on the negative horizontal axis, crosses the positive vertical axis, "
        r"and ends at the point $(0.21,0.45)$ in the first quadrant.]",
        r"A student carried out an experiment to find the values of the constants $a$ and $b$.",
        r"The student recorded the value of $T$ for different values of $l$.",
        r"Figure 3 shows the linear relationship between $\log_{10}l$ and $\log_{10}T$ for the student’s data.",
        r"The straight line passes through the points $(-0.7,0)$ and $(0.21,0.45)$"]
Q11 = [r"[Figure 4: a V-shaped graph with its vertex on the positive $x$-axis; the left branch crosses the positive "
       r"$y$-axis and both branches rise to the top of the diagram. No values are marked.]",
       "Figure 4 shows a sketch of the graph with equation",
       r"$$y=\left|2x-3k\right|$$",
       r"where $k$ is a positive constant."]
Q11A = [r"Sketch the graph with equation $y=\mathrm{f}(x)$ where", r"$$\mathrm{f}(x)=k-\left|2x-3k\right|$$", "stating",
        "• the coordinates of the maximum point",
        "• the coordinates of any points where the graph cuts the coordinate axes"]
I12 = r"\int_0^{16}\frac{x}{1+\sqrt{x}}\,\mathrm{d}x"
Q12A = [r"Use the substitution $u=1+\sqrt{x}$ to show that",
        r"$$" + I12 + r"=\int_p^q\frac{2(u-1)^3}{u}\,\mathrm{d}u$$",
        r"where $p$ and $q$ are constants to be found."]
Q13 = [r"The curve $C$ has parametric equations",
       r"$$x=\sin2\theta\qquad y=\mathrm{cosec}^3\theta\qquad0<\theta<\frac{\pi}{2}$$"]
Q13A = r"Find an expression for $" + DYDX + r"$ in terms of $\theta$"
Q14 = [r"[Figure 5: a cuboid tank drawn in three dimensions, with base 8 m by 3 m and height 5 m; the lower part is "
       r"shaded to show water of depth $h$ m; the tap $T$ is a dot at the bottom front left corner of the tank.]",
       "Water flows at a constant rate into a large tank.",
       "The tank is a cuboid, with all sides of negligible thickness.",
       "The base of the tank measures 8 m by 3 m and the height of the tank is 5 m.",
       r"There is a tap at a point $T$ at the bottom of the tank, as shown in Figure 5.",
       r"At time $t$ minutes after the tap has been opened",
       r"• the depth of water in the tank is $h$ metres",
       r"• water is flowing into the tank at a constant rate of 0.48 m$^3$ per minute",
       r"• water is modelled as leaving the tank through the tap at a rate of $0.1h$ m$^3$ per minute"]
Q14A = ["Show that, according to the model,", r"$$1200\frac{\mathrm{d}h}{\mathrm{d}t}=24-5h$$"]
Q14G = "Given that when the tap was opened, the depth of water in the tank was 2 m,"
Q15A = [r"Express $2\cos\theta-\sin\theta$ in the form $R\cos(\theta+\alpha)$, where $R>0$ and "
        r"$0<\alpha<\frac{\pi}{2}$",
        r"Give the exact value of $R$ and the value of $\alpha$ in radians to 3 decimal places."]
Q15 = [r"[Figure 6: a water wheel with centre $C$ and paddles all round its rim; $P$ is the end of the paddle at the "
       r"upper right. A horizontal dashed line labelled “Water level” passes below $C$, through the lower paddles. The "
       r"vertical height of $P$ above the water level is marked $H$ metres.]",
       "Figure 6 shows the cross-section of a water wheel.",
       r"The wheel is free to rotate about a fixed axis through the point $C$.",
       r"The point $P$ is at the end of one of the paddles of the wheel, as shown in Figure 6.",
       "The water level is assumed to be horizontal and of constant height.",
       r"The vertical height, $H$ metres, of $P$ above the water level is modelled by the equation",
       r"$$H=3+4\cos(0.5t)-2\sin(0.5t)$$",
       r"where $t$ is the time in seconds after the wheel starts rotating."]
Q15T = r"In a single revolution of the wheel, $P$ is below the water level for a total of $T$ seconds."

LATEX = {
    "01a": L(*Q1, Q1A),
    "01b": L(*Q1, "(a) " + Q1A, "(b) Hence find the sum of the first 500 terms of the series."),
    "02a": L(*Q2, "State the range of f"),
    "02b": L(*Q2, r"Find $\mathrm{gf}(1.8)$"),
    "02c": L(*Q2, r"Find $\mathrm{g}^{-1}(x)$"),
    "03": L("Using the laws of logarithms, solve the equation", r"$$\log_3(12y+5)-\log_3(1-3y)=2$$"),
    "04": L(r"Given that $\theta$ is small and measured in radians, use the small angle approximations to show that",
            r"$$4\sin\frac{\theta}{2}+3\cos^2\theta\approx a+b\theta+c\theta^2$$",
            r"where $a$, $b$ and $c$ are integers to be found."),
    "05a": L(*Q5, *Q5A),
    "05b": L(*Q5, "(a) " + Q5A[0], *Q5A[1:],
             r"(b) (i) Verify that $C$ has a stationary point at $x=1$",
             "(ii) Show that this stationary point is a point of inflection, giving reasons for your answer."),
    "06a": L(*Q6, Q6A),
    "06b": L(*Q6, "(a) " + Q6A, "(b) Show that the area of the logo is", r"$$\frac{1}{2}r^2(3\theta+\pi)$$"),
    "06c": L(*Q6, "(a) " + Q6A,
             r"(c) Find the perimeter of the logo, giving your answer in simplest form in terms of $r$, $\theta$ and "
             r"$\pi$."),
    "07a": L(*Q7, Q7A),
    "07b": L(*Q7, "(a) " + Q7A, Q7B),
    "07c": L(*Q7, "(a) " + Q7A, Q7B,
             r"The finite region $R$, shown shaded in Figure 2, is bounded by the curve $C$ and the line $l$.",
             r"(c) Use algebraic integration to find the exact area of $R$."),
    "08a": L(*Q8, *Q8A),
    "08b": L(*Q8, "(a) " + Q8A[0], *Q8A[1:], "Given that",
             r"• the point $P(-1,-4)$ lies on $C$",
             r"• the normal to $C$ at $P$ has equation $19x+26y+123=0$",
             r"(b) find the value of $p$ and the value of $q$."),
    "09": L("Show that", r"$$\sum_{n=2}^{\infty}\left(\frac{3}{4}\right)^n\cos(180n)^\circ=\frac{9}{28}$$"),
    "10a": L(*Q10, *Q10A),
    "10b": L(*Q10, "(a) " + Q10A[0], Q10A[1], *Q10F, "Using this information,",
             "(b) find a complete equation for the model in the form", r"$$T=al^b$$",
             r"giving the value of $a$ and the value of $b$, each to 3 significant figures."),
    "10c": L(*Q10, *Q10F, r"With reference to the model, interpret the value of the constant $a$."),
    "11a": L(*Q11, *Q11A),
    "11b": L(*Q11, r"Find, in terms of $k$, the set of values of $x$ for which",
             r"$$k-\left|2x-3k\right|>x-k$$", "giving your answer in set notation."),
    "11c": L(*Q11, "(a) " + Q11A[0], *Q11A[1:],
             r"(c) Find, in terms of $k$, the coordinates of the minimum point of the graph with equation",
             r"$$y=3-5\mathrm{f}\left(\frac{1}{2}x\right)$$"),
    "12a": L(*Q12A),
    "12b": L("(a) " + Q12A[0], *Q12A[1:], "(b) Hence show that", r"$$" + I12 + r"=A-B\ln5$$",
             r"where $A$ and $B$ are constants to be found."),
    "13a": L(*Q13, Q13A),
    "13b": L(*Q13, "(a) " + Q13A,
             r"(b) Hence find the exact value of the gradient of the tangent to $C$ at the point where $y=8$"),
    "14a": L(*Q14, *Q14A),
    "14b": L(*Q14, "(a) " + Q14A[0], Q14A[1], Q14G, "(b) show that, according to the model,",
             r"$$h=A+B\mathrm{e}^{-kt}$$", r"where $A$, $B$ and $k$ are constants to be found."),
    "14c": L(*Q14, Q14G, "Given that the tap remains open,",
             "determine, according to the model, whether the tank will ever become full, giving a reason for your "
             "answer."),
    "15a": L(*Q15A),
    "15b": L("(a) " + Q15A[0], Q15A[1], *Q15, "Using the model, find",
             r"(b) (i) the maximum height of $P$ above the water level,",
             r"(ii) the value of $t$ when this maximum height first occurs, giving your answer to one decimal place."),
    "15c": L("(a) " + Q15A[0], Q15A[1], *Q15, Q15T, "According to the model,",
             r"(c) find the value of $T$ giving your answer to 3 significant figures.",
             "(Solutions based entirely on calculator technology are not acceptable.)"),
    "15d": L(*Q15, Q15T, "In reality, the water level may not be of constant height.",
             "Explain how the equation of the model should be refined to take this into account."),
}

# Repeated mark-scheme pieces.
Q9A1 = r"A1* (AO 1.1b): $=\frac{9}{28}$ *"
Q12ALIM = r"\int_0^{16}\frac{x}{1+\sqrt{x}}\,\mathrm{d}x"
Q15B1 = r"3+2\sqrt{5}"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", SEQ, "4.4", 2, LATEX["01a"],
      [r"M1 (AO 1.1b): $16+(21-1)\times d=24\Rightarrow d=\ldots$. Notes: Correct strategy to find the common "
       r"difference – must be a correct method using $a=16$, and $n=21$ and the 24. The method may be implied by their "
       r"working. If the AP term formula is quoted it must be correct, so use of e.g. $u_n=a+nd$ scores M0",
       r"A1 (AO 1.1b): $d=0.4$ Answer only scores both marks. Notes: Correct value. Accept equivalents e.g. "
       r"$\frac{8}{20},\frac{4}{10},\frac{2}{5}$ etc. Note that some candidates are showing implied use of "
       r"$u_n=a+nd$ by showing the following: (a) $d=\frac{24-16}{21}=\frac{8}{21}$ (b) $S_{500}=\frac{1}{2}\times500"
       r"\left\{2\times16+499\times\frac{8}{21}\right\}=55523.80952\ldots$ This scores (a) M0A0 (b) M1A0"],
      False, 2),
    e("01b", "1(b)", SEQ, "4.4", 2, LATEX["01b"],
      [r"M1 (AO 1.1b): $S_n=\frac{1}{2}n\{2a+(n-1)d\}\Rightarrow S_{500}=\frac{1}{2}\times500\{2\times16+499\times"
       r"\text{“}0.4\text{”}\}$. Notes: Attempts to use a correct sum formula with $a=16$, $n=500$ and their numerical "
       r"$d$ from part (a) If a formula is quoted it must be correct (it is in the formula book)",
       r"A1 (AO 1.1b): $=57900$ Answer only scores both marks. Notes: Correct value",
       r"ALT: (b) Alternative using $S_n=\frac{1}{2}n\{a+l\}$ — M1 (AO 1.1b): $l=16+(500-1)\times\text{“}0.4\text{”}="
       r"215.6\Rightarrow S_{500}=\frac{1}{2}\times500\{16+\text{“}215.6\text{”}\}$. Notes: Correct method for the "
       r"500th term and then uses $S_n=\frac{1}{2}n\{a+l\}$ with their $l$",
       r"ALT: (b) Alternative using $S_n=\frac{1}{2}n\{a+l\}$ — A1 (AO 1.1b): $=57900$. Notes: Correct value"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", ALG, "2.8", 1, LATEX["02a"],
      [r"B1 (AO 2.5): $y\leqslant7$. Notes: Correct range. Allow $\mathrm{f}(x)$ or f for $y$. Allow e.g. "
       r"$\{y\in\mathbb{R}:\ y\leqslant7\}$, $-\infty<y\leqslant7$, $(-\infty,7]$"],
      False, 4),
    e("02b", "2(b)", ALG, "2.8", 2, LATEX["02b"],
      [r"M1 (AO 1.1b): $\mathrm{f}(1.8)=7-2\times1.8^2=0.52\Rightarrow\mathrm{gf}(1.8)=\mathrm{g}(0.52)="
       r"\frac{3\times0.52}{5\times0.52-1}=\ldots$. Notes: Full method to find $\mathrm{f}(1.8)$ and substitutes the "
       r"result into g to obtain a value. Also allow for an attempt to substitute $x=1.8$ into an attempt at "
       r"$\mathrm{gf}(x)$. E.g. $\mathrm{gf}(x)=\frac{3(7-2x^2)}{5(7-2x^2)-1}=\frac{3(7-2(1.8)^2)}{5(7-2\times(1.8)^2)"
       r"-1}=\ldots$",
       r"A1 (AO 1.1b): $\mathrm{gf}(1.8)=0.975$ oe e.g. $\frac{39}{40}$. Notes: Correct value"],
      False, 4),
    e("02c", "2(c)", ALG, "2.8", 2, LATEX["02c"],
      [r"M1 (AO 1.1b): $y=\frac{3x}{5x-1}\Rightarrow5xy-y=3x\Rightarrow x(5y-3)=y$. Notes: Correct attempt to cross "
       r"multiply, followed by an attempt to factorise out $x$ from an $xy$ term and an $x$ term. If they swap $x$ and "
       r"$y$ at the start then it will be for an attempt to cross multiply followed by an attempt to factorise out $y$ "
       r"from an $xy$ term and a $y$ term.",
       r"A1 (AO 2.2a): $(\mathrm{g}^{-1}(x)=)\frac{x}{5x-3}$. Notes: Correct expression. Allow equivalent correct "
       r"expressions e.g. $\frac{-x}{3-5x},\ \frac{1}{5}+\frac{3}{25x-15}$ Ignore any domain if given."],
      False, 4),

    # ---------------- Q3 ----------------
    e("03", "3", EXP, "6.4, 6.3", 3, LATEX["03"],
      [r"B1 (M1 on EPEN) (AO 1.1b): $\log_3(12y+5)-\log_3(1-3y)=2\Rightarrow\log_3\frac{12y+5}{1-3y}=2$ or e.g. "
       r"$2=\log_39$. Notes: Applies at least one addition or subtraction law of logs correctly. Can also be awarded "
       r"for using $2=\log_39$. This may be implied by e.g. $\log_3\ldots=2\Rightarrow\ldots=9$",
       r"M1 (AO 2.1): $\log_3\frac{12y+5}{1-3y}=2\Rightarrow\frac{12y+5}{1-3y}=3^2\Rightarrow9-27y=12y+5\Rightarrow "
       r"y=\ldots$ or e.g. $\log_3(12y+5)=\log_3(3^2(1-3y))\Rightarrow(12y+5)=3^2(1-3y)\Rightarrow y=\ldots$. Notes: A "
       r"rigorous argument with no incorrect working to remove the log or logs correctly and obtain a "
       r"$\underline{\text{correct}}$ equation in any form $\textbf{and}$ solve for $y$.",
       r"A1 (AO 1.1b): $y=\frac{4}{39}$. Notes: Correct $\textbf{exact}$ value. Allow equivalent fractions. "
       r"$\underline{\textbf{Guidance on how to mark particular cases:}}$ "
       r"$\log_3(12y+5)-\log_3(1-3y)=2\Rightarrow\frac{\log_3(12y+5)}{\log_3(1-3y)}=2\Rightarrow\frac{12y+5}{1-3y}="
       r"3^2\Rightarrow9-27y=12y+5\Rightarrow y=\frac{4}{39}$ B1M0A0 "
       r"$\log_3(12y+5)-\log_3(1-3y)=2\Rightarrow\frac{\log_3(12y+5)}{\log_3(1-3y)}=2\Rightarrow\log_3\frac{12y+5}"
       r"{1-3y}=2\Rightarrow\frac{12y+5}{1-3y}=3^2\Rightarrow9-27y=12y+5\Rightarrow y=\frac{4}{39}$ B1M0A0 "
       r"$\log_3(12y+5)-\log_3(1-3y)=2\Rightarrow\frac{12y+5}{1-3y}=3^2\Rightarrow9-27y=12y+5\Rightarrow "
       r"y=\frac{4}{39}$ B1M1A1"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04", "4", TRIG, "5.2", 3, LATEX["04"],
      [r"M1 (AO 1.1a): Examples: $4\sin\frac{\theta}{2}\approx4\left(\frac{\theta}{2}\right)$, $3\cos^2\theta\approx"
       r"3\left(1-\frac{\theta^2}{2}\right)^2$ $3\cos^2\theta=3(1-\sin^2\theta)\approx3(1-\theta^2)$ "
       r"$3\cos^2\theta=3\frac{(\cos2\theta+1)}{2}\approx\frac{3}{2}\left(1-\frac{4\theta^2}{2}+1\right)$. Notes: "
       r"Attempts to use at least one correct approximation $\textbf{within the given expression}$. Either "
       r"$\sin\frac{\theta}{2}\approx\frac{\theta}{2}$ or $\cos\theta\approx1-\frac{\theta^2}{2}$ or e.g. "
       r"$\sin\theta\approx\theta$ if they write $\cos^2\theta$ as $1-\sin^2\theta$ or e.g. $\cos2\theta\approx1-"
       r"\frac{(2\theta)^2}{2}$ (condone missing brackets) if they write $\cos^2\theta$ as $\frac{1+\cos2\theta}{2}$. "
       r"Allow sign slips only with any identities used but the appropriate approximations must be applied.",
       r"dM1 (AO 1.1b): Examples: $4\sin\frac{\theta}{2}+3\cos^2\theta\approx4\left(\frac{\theta}{2}\right)+3\left(1-"
       r"\frac{\theta^2}{2}\right)^2$ $4\sin\frac{\theta}{2}+3\cos^2\theta=4\left(\frac{\theta}{2}\right)+3(1-\sin^2"
       r"\theta)\approx2\theta+3(1-\theta^2)$ $4\sin\frac{\theta}{2}+3\cos^2\theta=4\sin\frac{\theta}{2}+3\frac{(\cos2"
       r"\theta+1)}{2}\approx4\left(\frac{\theta}{2}\right)+\frac{3}{2}\left(1-\frac{4\theta^2}{2}+1\right)$. Notes: "
       r"Attempts to use correct approximations $\textbf{with the given expression}$ to obtain an expression in terms "
       r"of $\theta$ only. $\textbf{Depends on the first method mark.}$",
       r"A1 (AO 2.1): $=2\theta+3(1-\theta^2+\ldots)=3+2\theta-3\theta^2$. Notes: Correct terms following correct "
       r"work. Allow the terms in any order and ignore any extra terms if given correct or incorrect."],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", DIFF, "7.2, 7.1", 3, LATEX["05a"],
      [r"M1 (AO 1.1b): (i) $" + DYDX + r"=20x^3-72x^2+84x-32$. Notes: $x^n\to x^{n-1}$ for at least one power of $x$",
       r"A1 (AO 1.1b): (i) $" + DYDX + r"=20x^3-72x^2+84x-32$. Notes: $" + DYDX + r"=20x^3-72x^2+84x-32$",
       r"A1ft (AO 1.1b): (ii) $" + D2YDX2 + r"=60x^2-144x+84$. Notes: Achieves a correct $" + D2YDX2
       + r"$ for their $" + DYDX + r"=20x^3-72x^2+84x-32$"],
      False, 10),
    e("05b", "5(b)", DIFF, "7.3, 7.1", 4, LATEX["05b"],
      [r"M1 (AO 1.1b): (b)(i) $x=1\Rightarrow" + DYDX + r"=20-72+84-32$. Notes: Substitutes $x=1$ into their $"
       + DYDX + "$",
       r"A1 (AO 2.1): $" + DYDX + r"=0$ so there is a stationary point at $x=1$. Notes: Obtains $" + DYDX
       + r"=0$ following a correct derivative and makes a conclusion which can be minimal e.g. tick, QED etc. which "
       r"may be in a preamble e.g. stationary point when $" + DYDX + r"=0$ and then shows $" + DYDX + "=0$",
       r"M1 (AO 2.1): (b)(ii) Note that in (b)(ii) there are no marks for $\underline{\text{just}}$ evaluating "
       r"$\left(" + D2YDX2 + r"\right)_{x=1}$ E.g. $\left(" + D2YDX2 + r"\right)_{x=0.8}=\ldots$ $\left(" + D2YDX2
       + r"\right)_{x=1.2}=\ldots$. Notes: Considers the value of the second derivative either side of $x=1$. Do not "
       r"be too concerned with the interval for the method mark. (NB $" + D2YDX2 + r"=(x-1)(60x-84)$ so may use this "
       r"factorised form when considering $x<1$, $x>1$ for sign change of second derivative)",
       r"A1 (AO 2.2a): $\left(" + D2YDX2 + r"\right)_{x=0.8}>0$, $\left(" + D2YDX2 + r"\right)_{x=1.2}<0$ Hence point "
       r"of inflection. Notes: Fully correct work including a correct $" + D2YDX2 + r"$ with a reasoned conclusion "
       r"indicating that the stationary point is a point of inflection. Sufficient reason is e.g. “sign change”/ "
       r"“$>0$, $<0$”. If values are given they should be correct (but be generous with accuracy) but also just allow "
       r"“$>0$” and “$<0$” provided they are correctly paired. The interval must be where $x<1.4$ "
       r"[Table of values: $x$ = 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1; $\mathrm{f}'(x)$ = $-32$, $-24.3$, "
       r"$-17.92$, $-12.74$, $-8.64$, $-5.5$, $-3.2$, $-1.62$, $-0.64$, $-0.14$, 0; $\mathrm{f}''(x)$ = 84, 70.2, "
       r"57.6, 46.2, 36, 27, 19.2, 12.6, 7.2, 3, 0. $x$ = 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7; $\mathrm{f}'(x)$ = "
       r"$-0.1$, $-0.32$, $-0.54$, $-0.64$, $-0.5$, 0, 0.98; $\mathrm{f}''(x)$ = $-1.8$, $-2.4$, $-1.8$, 0, 3, 7.2, "
       r"12.6]",
       r"ALT: Alternative for (b)(i) — M1 (AO 1.1b): $20x^3-72x^2+84x-32=4(x-1)^2(5x-8)=0\Rightarrow x=\ldots$. Notes: "
       r"Attempts to solve $" + DYDX + r"=0$ by factorisation. This may be by using the factor of $(x-1)$ or possibly "
       r"using a calculator to find the roots and showing the factorisation. Note that they may divide by 4 before "
       r"factorising which is acceptable. Need to either see either $4(x-1)^2(5x-8)$ or $(x-1)^2(5x-8)$ for the "
       r"factorisation or $x=\frac{8}{5}$ and $x=1$ seen as the roots.",
       r"ALT: Alternative for (b)(i) — A1 (AO 2.1): When $x=1$, $" + DYDX + r"=0$ so there is a stationary point. "
       r"Notes: Obtains $x=1$ and makes a conclusion as above",
       r"ALT: Alternative 1 for (b)(ii) — M1 (AO 2.1): $\left(" + D2YDX2 + r"\right)_{x=1}=60x^2-144x+84=0$ (is "
       r"inconclusive) $\left(\frac{\mathrm{d}^3y}{\mathrm{d}x^3}\right)=120x-144\Rightarrow\left(\frac{\mathrm{d}^3y}"
       r"{\mathrm{d}x^3}\right)_{x=1}=\ldots$. Notes: Shows that second derivative at $x=1$ is zero and $\textbf{then "
       r"finds the third derivative at}$ $x=1$",
       r"ALT: Alternative 1 for (b)(ii) — A1 (AO 2.2a): $\left(" + D2YDX2 + r"\right)_{x=1}=0$ and $\left(\frac{"
       r"\mathrm{d}^3y}{\mathrm{d}x^3}\right)_{x=1}\neq0$ Hence point of inflection. Notes: Fully correct work "
       r"including a correct $" + D2YDX2 + r"$ with a reasoned conclusion indicating that stationary point is a point "
       r"of inflection. Sufficient reason is “$\neq0$” but must follow a correct third derivative and a correct value "
       r"if evaluated. For reference $\left(\frac{\mathrm{d}^3y}{\mathrm{d}x^3}\right)_{x=1}=-24$",
       r"ALT: Alternative 2 for (b)(ii) — M1 (AO 2.1): E.g. $\left(" + DYDX + r"\right)_{x=0.8}=\ldots$ $\left(" + DYDX
       + r"\right)_{x=1.2}=\ldots$. Notes: Considers the value of the first derivative either side of $x=1$. Do not "
       r"be too concerned with the interval for the method mark.",
       r"ALT: Alternative 2 for (b)(ii) — A1 (AO 2.2a): $\left(" + DYDX + r"\right)_{x=0.8}<0$, $\left(" + DYDX
       + r"\right)_{x=1.2}<0$ Hence point of inflection. Notes: Fully correct work with a reasoned conclusion "
       r"indicating that stationary point is a point of inflection. Sufficient reason is e.g. “same sign”/“both "
       r"negative”/“$<0$, $<0$”. If values are given they should be correct (but be generous with accuracy). The "
       r"interval must be where $x<1.4$"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", TRIG, "5.1", 1, LATEX["06a"],
      [r"B1 (AO 2.2a): Angle $AOB=\frac{\pi-\theta}{2}$. Notes: Deduces the correct expression for angle $AOB$ Note "
       r"that $\frac{180-\theta}{2}$ scores B0. Note that some candidates may change the angle to degrees at the start "
       r"and all marks are available e.g. (a) $\frac{180-\frac{180\theta}{\pi}}{2}$"],
      True, 12),
    e("06b", "6(b)", TRIG, "5.1", 2, LATEX["06b"],
      [r"M1 (AO 2.1): Area $=2\times\frac{1}{2}r^2\left(\frac{\pi-\theta}{2}\right)+\frac{1}{2}(2r)^2\theta$. Notes: "
       r"Fully correct strategy for the area using their angle from (a) appropriately. Need to see $2\times\frac{1}{2}"
       r"r^2\alpha$ or just $r^2\alpha$ where $\alpha$ is their angle in terms of $\theta$ from part (a) + "
       r"$\frac{1}{2}(2r)^2\theta$ with or without the brackets.",
       r"A1* (AO 1.1b): $=\frac{1}{2}r^2\pi-\frac{1}{2}r^2\theta+2r^2\theta=\frac{3}{2}r^2\theta+\frac{1}{2}r^2\pi="
       r"\frac{1}{2}r^2(3\theta+\pi)$*. Notes: Correct proof. For this mark you can condone the omission of the "
       r"brackets in $\frac{1}{2}(2r)^2\theta$ as long as they are recovered in subsequent work e.g. when this term "
       r"becomes $2r^2\theta$ The first term must be seen expanded as e.g. $\frac{1}{2}r^2\pi-\frac{1}{2}r^2\theta$ or "
       r"equivalent. Note that some candidates may change the angle to degrees at the start and all marks are "
       r"available e.g. (b) $2\left(\frac{180-\frac{180\theta}{\pi}}{2}\right)\times\frac{1}{360}\times\pi r^2+"
       r"\frac{\theta}{360}\times\frac{180}{\pi}\times\pi(2r)^2=\frac{1}{2}\pi r^2-\frac{1}{2}r^2\theta+2r^2\theta="
       r"\frac{1}{2}r^2(3\theta+\pi)$"],
      True, 12),
    e("06c", "6(c)", TRIG, "5.1", 2, LATEX["06c"],
      [r"M1 (AO 3.1a): Perimeter $=4r+2r\left(\frac{\pi-\theta}{2}\right)+2r\theta$. Notes: Fully correct strategy for "
       r"the perimeter using their angle from (a) appropriately Need to see $4r+2r\alpha+2r\theta$ where $\alpha$ is "
       r"their angle from part (a) in terms of $\theta$",
       r"A1 (AO 1.1b): $=4r+r\pi+r\theta$ or e.g. $r(4+\pi+\theta)$. Notes: Correct simplified expression. Note that "
       r"some candidates may change the angle to degrees at the start and all marks are available e.g. (c) $4r+2\left("
       r"\frac{180-\frac{180\theta}{\pi}}{2}\right)\times\frac{1}{360}\times2\pi r+\frac{180\theta}{\pi}\times\frac{1}"
       r"{360}\times2\pi(2r)=4r+\pi r+r\theta$"],
      True, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", DIFF, "7.3, 7.2, 3.1", 4, LATEX["07a"],
      [r"B1 (AO 1.1b): $y=x^3-10x^2+27x-23\Rightarrow" + DYDX + r"=3x^2-20x+27$. Notes: Correct derivative",
       r"M1 (AO 1.1b): $\left(" + DYDX + r"\right)_{x=5}=3\times5^2-20\times5+27(=2)$. Notes: Substitutes $x=5$ into "
       r"their derivative. This may be implied by their value for $" + DYDX + "$",
       r"M1 (AO 2.1): $y+13=2(x-5)$. Notes: Fully correct straight line method using $(5,-13)$ and their $" + DYDX
       + r"$ at $x=5$",
       r"A1 (AO 1.1b): $y=2x-23$. Notes: cao. Must see the full equation in the required form."],
      True, 16),
    e("07b", "7(b)", COORD, "3.1, 2.7", 1, LATEX["07b"],
      [r"B1 (AO 2.2a): Both $C$ and $l$ pass through $(0,-23)$ and so $C$ meets $l$ again on the $y$-axis. Notes: "
       r"Makes a suitable deduction.",
       r"ALT: Alternative via equating $l$ and $C$ and factorising — B1: e.g. $x^3-10x^2+27x-23=2x-23$ $x^3-10x^2+25x="
       r"0$ $x(x^2-10x+25)=0\Rightarrow x=0$ So they meet on the $y$-axis"],
      True, 16),
    e("07c", "7(c)", INT, "8.3, 8.2", 4, LATEX["07c"],
      [r"M1 (AO 1.1b): $\pm\int(x^3-10x^2+27x-23-(2x-23))\,\mathrm{d}x=\pm\left(\frac{x^4}{4}-\frac{10}{3}x^3+"
       r"\frac{25}{2}x^2\right)$. Notes: For an attempt to integrate $x^n\to x^{n+1}$ for $\pm$“$C-l$”",
       r"A1ft (AO 1.1b): $\pm\left(\frac{x^4}{4}-\frac{10}{3}x^3+\frac{25}{2}x^2\right)$. Notes: Correct integration "
       r"in any form which may be simplified or unsimplified. (follow through their equation from (a)) If they "
       r"attempt as 2 separate integrals e.g. $\int(x^3-10x^2+27x-23)\,\mathrm{d}x-\int(2x-23)\,\mathrm{d}x$ then "
       r"award this mark for the correct integration of the curve as in the alternative. If they combine the curve "
       r"with the line first then the subsequent integration must be correct or a correct ft for their line and allow "
       r"for $\pm$“$C-l$”",
       r"dM1 (AO 2.1): $\left[\frac{x^4}{4}-\frac{10}{3}x^3+\frac{25}{2}x^2\right]_0^5=\left(\frac{625}{4}-"
       r"\frac{1250}{3}+\frac{625}{2}\right)(-0)$. Notes: Fully correct strategy for the area. Award for use of 5 as "
       r"the limit and condone the omission of the “$-0$”. $\textbf{Depends on the first method mark.}$",
       r"A1 (AO 1.1b): $=\frac{625}{12}$. Notes: Correct exact value. Note if they do $l-C$ rather than $C-l$ and the "
       r"working is otherwise correct allow full marks if their final answer is given as a positive value. E.g. "
       r"correct work with $l-C$ leading to $-\frac{625}{12}$ and then e.g. hence area is $\frac{625}{12}$ is "
       r"acceptable for full marks. If the answer is left as $-\frac{625}{12}$ then score A0",
       r"ALT: (c) Alternative — M1 (AO 1.1b): $\pm\int(x^3-10x^2+27x-23)\,\mathrm{d}x=\pm\left(\frac{x^4}{4}-\frac{10}"
       r"{3}x^3+\frac{27}{2}x^2-23x\right)$. Notes: For an attempt to integrate $x^n\to x^{n+1}$ for $\pm C$",
       r"ALT: (c) Alternative — A1 (AO 1.1b): $\pm\left(\frac{x^4}{4}-\frac{10}{3}x^3+\frac{27}{2}x^2-23x\right)$. "
       r"Notes: Correct integration for $\pm C$",
       r"ALT: (c) Alternative — dM1 (AO 2.1): $\left[\frac{x^4}{4}-\frac{10}{3}x^3+\frac{27}{2}x^2-23x\right]_0^5+"
       r"\frac{1}{2}\times5(23+13)=-\frac{455}{12}+90$. Notes: Fully correct strategy for the area e.g. correctly "
       r"attempts the area of the trapezium and subtracts the area enclosed between the curve and the $x$-axis. Need "
       r"to see the use of 5 as the limit condoning the omission of the “$-0$” $\textbf{and}$ a correct attempt at the "
       r"trapezium $\textbf{and}$ the subtraction. May see the trapezium area attempted as $\int(2x-23)\,\mathrm{d}x$ "
       r"in which case the integration and use of the limits needs to be correct or correct follow through for their "
       r"straight line equation. $\textbf{Depends on the first method mark.}$",
       r"ALT: (c) Alternative — A1 (AO 1.1b): $=\frac{625}{12}$. Notes: Correct exact value"],
      True, 16),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", DIFF, "7.5", 4, LATEX["08a"],
      [r"M1 (AO 2.1): $\frac{\mathrm{d}}{\mathrm{d}x}(3y^2)=6y" + DYDX + r"$ or $\frac{\mathrm{d}}{\mathrm{d}x}(qxy)="
       r"qx" + DYDX + r"+qy$. Notes: For selecting the appropriate method of differentiating: Allow this mark for "
       r"either $3y^2\to\alpha y" + DYDX + r"$ or $qxy\to\alpha x" + DYDX + r"+\beta y$",
       r"A1 (AO 1.1b): $3px^2+qx" + DYDX + r"+qy+6y" + DYDX + r"=0$. Notes: Fully correct differentiation. Ignore any "
       r"spurious $" + DYDX + r"=\ldots$",
       r"dM1 (AO 2.1): $(qx+6y)" + DYDX + r"=-3px^2-qy\Rightarrow" + DYDX + r"=\ldots$. Notes: A valid attempt to make "
       r"$" + DYDX + r"$ the subject with 2 terms only in $" + DYDX + r"$ coming from $qxy$ and $3y^2$ "
       r"$\textbf{Depends on the first method mark.}$",
       r"A1 (AO 1.1b): $" + DYDX + r"=\frac{-3px^2-qy}{qx+6y}$. Notes: Fully correct expression"],
      False, 20),
    e("08b", "8(b)", DIFF, "7.5, 7.3, 3.1, 2.4", 5, LATEX["08b"],
      [r"M1 (AO 1.1b): $p(-1)^3+q(-1)(-4)+3(-4)^2=26$. Notes: Uses $x=-1$ and $y=-4$ in the equation of $C$ to obtain "
       r"an equation in $p$ and $q$",
       r"B1 (AO 2.2a): $19x+26y+123=0\Rightarrow m=-\frac{19}{26}$. Notes: Deduces the correct gradient of the given "
       r"normal. This may be implied by e.g. $19x+26y+123=0\Rightarrow y=-\frac{19}{26}x+\ldots\Rightarrow$ Tangent "
       r"equation is $y=\frac{26}{19}x+\ldots$",
       r"M1 (AO 3.1a): $\frac{-3p(-1)^2-q(-4)}{q(-1)+6(-4)}=\frac{26}{19}$ or $\frac{q(-1)+6(-4)}{3p(-1)^2+q(-4)}="
       r"-\frac{19}{26}$. Notes: Fully correct strategy to establish an equation connecting $p$ and $q$ using $x=-1$ "
       r"and $y=-4$ in their $" + DYDX + r"$ and the gradient of the normal. E.g. $(a)=-1\div\text{their}-\frac{19}"
       r"{26}$ or $-1\div(a)=\text{their}-\frac{19}{26}$",
       r"dM1 (AO 1.1b): $p-4q=22,\ 57p-102q=624\Rightarrow p=\ldots,q=\ldots$. Notes: Solves simultaneously to obtain "
       r"values for $p$ and $q$. $\textbf{Depends on both previous method marks.}$",
       r"A1 (AO 1.1b): $p=2,\ q=-5$. Notes: Correct values",
       r"ALT: Alternative for (b) — M1: $" + DYDX + r"=\frac{-3p+4q}{-q-24}\Rightarrow y+4=\frac{q+24}{4q-3p}(x+1)$. "
       r"Notes: Uses $(-1,-4)$ in the tangent gradient and attempts to form normal equation",
       r"ALT: Alternative for (b) — A1: $y+4=\frac{q+24}{4q-3p}(x+1)$. Notes: Correct equation for normal",
       r"ALT: Alternative for (b) — M1: $\Rightarrow y(4q-3p)+4(4q-3p)=(q+24)x+q+24$. Notes: Multiplies up so that "
       r"coefficients can be compared",
       r"ALT: Alternative for (b) — dM1: $19x+26y+123=0\Rightarrow q+24=19\Rightarrow q=-5$ $3p-4q=26\Rightarrow3p+20="
       r"26\Rightarrow p=2$. Notes: Full method comparing coefficients to find values for $p$ and $q$",
       r"ALT: Alternative for (b) — A1: $q=-5$, $p=2$. Notes: Correct values"],
      False, 20),

    # ---------------- Q9 ----------------
    e("09", "9", SEQ, "4.5, 4.3, 5.3", 3, LATEX["09"],
      [r"B1 (AO 2.2a): $a=\left(\frac{3}{4}\right)^2$ or $a=\frac{9}{16}$ or $r=-\frac{3}{4}$. Notes: Deduces the "
       r"correct value of the $\textbf{first}$ term or the common ratio. The correct first term can be seen as part of "
       r"them writing down the sequence but must be the $\textbf{first}$ term.",
       r"M1 (AO 3.1a): $\sum_{n=2}^{\infty}\left(\frac{3}{4}\right)^n\cos(180n)^\circ=\frac{\frac{9}{16}}{1-\left(-"
       r"\frac{3}{4}\right)}=\ldots$. Notes: Recognises that the series is infinite geometric and applies the sum to "
       r"infinity GP formula with $a=\frac{9}{16}$ and $r=\pm\frac{3}{4}$",
       Q9A1 + ". Notes: Correct proof",
       r"ALT: Alternative 1 — B1 (AO 2.2a): $\sum_{n=1}^{\infty}\left(\frac{3}{4}\right)^n\cos(180n)^\circ=\frac{-"
       r"\frac{3}{4}}{1-\left(-\frac{3}{4}\right)}=\ldots$ or $r=-\frac{3}{4}$. Notes: Deduces the correct value for "
       r"the sum to infinity (starting at $n=1$) or the common ratio",
       r"ALT: Alternative 1 — M1 (AO 3.1a): $\sum_{n=2}^{\infty}\left(\frac{3}{4}\right)^n\cos(180n)^\circ=-\frac{3}{7}"
       r"-\left(-\frac{3}{4}\right)$. Notes: Calculates the required value by subtracting the first term from their "
       r"sum to infinity",
       r"ALT: Alternative 1 — " + Q9A1 + ". Notes: Correct proof",
       r"ALT: Alternative 2 — B1 (AO 2.2a): $\sum_{n=2}^{\infty}\left(\frac{3}{4}\right)^n\cos(180n)^\circ=\left("
       r"\frac{3}{4}\right)^2-\left(\frac{3}{4}\right)^3+\left(\frac{3}{4}\right)^4-\ldots$. Notes: Deduces the "
       r"correct value of the $\textbf{first}$ term or the common ratio.",
       r"ALT: Alternative 2 — M1 (AO 3.1a): $=\left(\frac{3}{4}\right)^2+\left(\frac{3}{4}\right)^4+\ldots-\left("
       r"\frac{3}{4}\right)^3-\left(\frac{3}{4}\right)^5-\ldots$ $\left(\frac{3}{4}\right)^2+\left(\frac{3}{4}"
       r"\right)^4+\ldots=\left(\frac{3}{4}\right)^2\left(\frac{1}{1-\left(\frac{3}{4}\right)^2}\right)$ or $-\left("
       r"\frac{3}{4}\right)^3-\left(\frac{3}{4}\right)^5-\ldots=-\left(\frac{3}{4}\right)^3\left(\frac{1}{1-\left("
       r"\frac{3}{4}\right)^2}\right)$ $\sum_{n=2}^{\infty}\left(\frac{3}{4}\right)^n\cos(180n)^\circ=\left(\frac{3}{4}"
       r"\right)^2\left(\frac{1}{1-\left(\frac{3}{4}\right)^2}\right)-\left(\frac{3}{4}\right)^3\left(\frac{1}{1-\left("
       r"\frac{3}{4}\right)^2}\right)$. Notes: Splits the series into “odds” and “evens”, attempts the sum of both "
       r"parts and calculates the required value by adding both sums",
       r"ALT: Alternative 2 — " + Q9A1 + ". Notes: Correct proof",
       r"ALT: Alternative 3 — B1 (AO 2.2a): $\sum_{n=2}^{\infty}\left(\frac{3}{4}\right)^n\cos(180n)^\circ=S=\left("
       r"\frac{3}{4}\right)^2-\left(\frac{3}{4}\right)^3+\left(\frac{3}{4}\right)^4-\ldots$. Notes: Deduces the correct "
       r"value of the $\textbf{first}$ term",
       r"ALT: Alternative 3 — M1 (AO 3.1a): $=\left(\frac{3}{4}\right)^2\left(1-\left(\frac{3}{4}\right)+\left(\frac{3}"
       r"{4}\right)^2-\ldots\right)=\left(\frac{3}{4}\right)^2\left(\frac{1}{4}+S\right)\Rightarrow\frac{7}{16}S="
       r"\frac{9}{64}\Rightarrow S=\ldots$. Notes: A complete method by taking out the first term, expresses the rhs "
       r"in terms of the original sum and rearranges for “S”",
       r"ALT: Alternative 3 — " + Q9A1 + ". Notes: Correct proof"],
      False, 24),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", EXP, "6.6, 6.4", 2, LATEX["10a"],
      [r"M1 (AO 2.1): $T=al^b\Rightarrow\log_{10}T=\log_{10}a+\log_{10}l^b$. Notes: Takes logs of both sides and "
       r"shows the addition law. Implied by $T=al^b\Rightarrow\log_{10}a+\log_{10}l^b$",
       r"A1* (AO 1.1b): $\Rightarrow\log_{10}T=\log_{10}a+b\log_{10}l$* or $\Rightarrow\log_{10}T=b\log_{10}l+"
       r"\log_{10}a$*. Notes: Uses the power law to obtain the given equation with no errors. Allow the bases to be "
       r"missing in the working but they must be present in the final answer. Also allow $t$ rather than $T$ and $A$ "
       r"rather than $a$. $\textbf{Allow working backwards e.g.}$ $\log_{10}T=b\log_{10}l+\log_{10}a\Rightarrow"
       r"\log_{10}T=\log_{10}l^b+\log_{10}a\Rightarrow\log_{10}T=\log_{10}al^b\Rightarrow T=al^b$* M1: Uses the given "
       r"answer and uses the power law and addition law correctly A1: Reaches the given equation with no errors as "
       r"above"],
      False, 26),
    e("10b", "10(b)", EXP, "6.6, 3.1", 3, LATEX["10b"],
      [r"B1 (AO 2.2a): $b=0.495$ or $b=\frac{45}{91}$. Notes: Deduces the correct value for $b$ (Allow awrt 0.495 or "
       r"$\frac{45}{91}$)",
       r"M1 (AO 3.1a): $0=\text{“}0.495\text{”}\times-0.7+\log_{10}a\Rightarrow a=10^{0.346\ldots}$ or $0.45="
       r"\text{“}0.495\text{”}\times0.21+\log_{10}a\Rightarrow a=10^{0.346\ldots}$. Notes: Correct strategy to find the "
       r"value of $a$. E.g. substitutes one of the given points and their value for $b$ into $\log_{10}T=\log_{10}a+"
       r"b\log_{10}l$ and uses correct log work to identify the value of $a$. Allow slips in rearranging their equation "
       r"but must be correct log work to find $a$. Alternatively finds the equation of the straight line and equates "
       r"the constant to $\log_{10}a$ and uses correct log work to identify the value of $a$. E.g. $y-0.45=\text{“}"
       r"0.495\text{”}(x-0.21)\Rightarrow y=\text{“}0.495\text{”}x+0.346\Rightarrow a=10^{0.346}=\ldots$",
       r"A1 (AO 3.3): $T=2.22l^{0.495}$. Notes: Complete equation $T=2.22l^{0.495}$ or $T=2.22l^{\frac{45}{91}}$ "
       r"(Allow awrt 2.22 and awrt 0.495 or $\frac{45}{91}$) $\textbf{Must see the}$ $\underline{\textbf{equation}}$ "
       r"$\textbf{not just correct values as it is a requirement of the question.}$"],
      True, 26),
    e("10c", "10(c)", EXP, "6.6, 2.11", 1, LATEX["10c"],
      [r"B1 (AO 3.2a): The time taken for one swing of a pendulum of length 1 m. Notes: Correct interpretation"],
      True, 26),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", ALG, "2.7, 2.9", 4, LATEX["11a"],
      [r"B1 (AO 1.1b): [Sketch: a $\wedge$ shape with its vertex at $(1.5k,k)$, crossing the $x$-axis at $k$ and $2k$ "
       r"and the $y$-axis at $-2k$] $\wedge$ shape in any position. Notes: Note that the sketch may be seen on Figure 4 "
       r"See scheme",
       r"B1 (AO 1.1b): Correct $x$-intercepts or coordinates. Notes: Correct $x$-intercepts. Allow as shown or "
       r"written as $(k,0)$ and $(2k,0)$ and condone coordinates written as $(0,k)$ and $(0,2k)$ as long as they are "
       r"in the correct places.",
       r"B1 (AO 1.1b): Correct $y$-intercept or coordinates. Notes: Correct $y$-intercept. Allow as shown or written as "
       r"$(0,-2k)$ or $(-2k,0)$ as long as it is in the correct place. Condone $k-3k$ for $-2k$.",
       r"B1 (AO 1.1b): Correct coordinates for the vertex of a $\wedge$ shape. Notes: Correct coordinates as shown "
       r"$\textbf{Note that the marks for the intercepts and the maximum can be seen away from the sketch but the "
       r"coordinates must be the right way round or e.g. as}$ $y=0$, $x=k$ $\textbf{etc. These marks can be awarded "
       r"without a sketch but if there is a sketch, such points must not contradict the sketch.}$"],
      True, 30),
    e("11b", "11(b)", ALG, "2.5, 2.7", 4, LATEX["11b"],
      [r"B1 (AO 2.2a): $x=k$. Notes: Deduces the correct critical value of $x=k$. May be implied by e.g. $x>k$ or "
       r"$x<k$",
       r"M1 (AO 3.1a): $k-(2x-3k)=x-k\Rightarrow x=\ldots$. Notes: Attempts to solve $k-(2x-3k)=x-k$ or an equivalent "
       r"equation/inequality to find the other critical value. Allow this mark for reaching $k=\ldots$ or $x=\ldots$ as "
       r"long as they are solving the required equation.",
       r"A1 (AO 1.1b): $x=\frac{5k}{3}$. Notes: Correct value",
       r"A1 (AO 2.5): Set notation is required here for this mark $\left\{x:x<\frac{5k}{3}\right\}\cap\{x:x>k\}$. "
       r"Notes: Correct answer using the correct set notation. Allow e.g. $\left\{x:x\in\mathbb{R},k<x<\frac{5k}{3}"
       r"\right\}$, $\left\{x:\ k<x<\frac{5k}{3}\right\}$, $x\in\left(k,\frac{5k}{3}\right)$ and allow “|” for “:” But "
       r"$\left\{x:x<\frac{5k}{3}\right\}\cup\{x:x>k\}$ scores A0 $\left\{x:\ k<x,\ x<\frac{5k}{3}\right\}$ scores A0"],
      True, 30),
    e("11c", "11(c)", ALG, "2.9, 2.7", 2, LATEX["11c"],
      [r"B1ft (AO 2.2a): $x=3k$ $\textbf{or}$ $y=3-5k$. Notes: Deduces one correct coordinate. Follow through their "
       r"maximum coordinates from (a) so allow $x=2\times$“$1.5k$” or $y=3-5\times$“$k$” but must be in terms of $k$. "
       r"Allow as coordinates or $x=\ldots$, $y=\ldots$",
       r"B1ft (AO 2.2a): $x=3k$ $\textbf{and}$ $y=3-5k$. Notes: Deduces both correct coordinates. Follow through their "
       r"maximum coordinates from (a) so allow $x=2\times$“$1.5k$” and $y=3-5\times$“$k$” but must be in terms of $k$. "
       r"Allow as coordinates or $x=\ldots$, $y=\ldots$ If coordinates are given the wrong way round and not seen "
       r"correctly as $x=\ldots$, $y=\ldots$ e.g. $(3-5k,3k)$ this is B0B0"],
      True, 30),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", INT, "8.5", 3, LATEX["12a"],
      [r"B1 (AO 1.1b): $u=1+\sqrt{x}\Rightarrow x=(u-1)^2\Rightarrow\frac{\mathrm{d}x}{\mathrm{d}u}=2(u-1)$ or "
       r"$u=1+\sqrt{x}\Rightarrow\frac{\mathrm{d}u}{\mathrm{d}x}=\frac{1}{2}x^{-\frac{1}{2}}$. Notes: Correct "
       r"expression for $\frac{\mathrm{d}x}{\mathrm{d}u}$ or $\frac{\mathrm{d}u}{\mathrm{d}x}$ (or $u'$) or "
       r"$\mathrm{d}x$ in terms of $\mathrm{d}u$ or $\mathrm{d}u$ in terms of $\mathrm{d}x$",
       r"M1 (AO 2.1): $\int\frac{x}{1+\sqrt{x}}\,\mathrm{d}x=\int\frac{(u-1)^2}{u}2(u-1)\,\mathrm{d}u$ or $\int"
       r"\frac{x}{1+\sqrt{x}}\,\mathrm{d}x=\int\frac{x}{u}\times2x^{\frac{1}{2}}\,\mathrm{d}u=\int\frac{2x^{\frac{3}"
       r"{2}}}{u}\,\mathrm{d}u=\int\frac{2(u-1)^3}{u}\,\mathrm{d}u$. Notes: Complete method using the given "
       r"substitution. This needs to be a correct method for their $\frac{\mathrm{d}x}{\mathrm{d}u}$ or "
       r"$\frac{\mathrm{d}u}{\mathrm{d}x}$ leading to an integral in terms of $u$ only (ignore any limits if present) "
       r"so for each case you need to see: $\frac{\mathrm{d}x}{\mathrm{d}u}=\mathrm{f}(u)\to\int\frac{x}{1+\sqrt{x}}"
       r"\,\mathrm{d}x=\int\frac{(u-1)^2}{u}\mathrm{f}(u)\,\mathrm{d}u$ $\frac{\mathrm{d}u}{\mathrm{d}x}=\mathrm{g}(x)"
       r"\to\int\frac{x}{1+\sqrt{x}}\,\mathrm{d}x=\int\frac{x}{u}\times\frac{\mathrm{d}u}{\mathrm{g}(x)}=\int\mathrm{h}"
       r"(u)\,\mathrm{d}u$. In this case you can condone slips with coefficients e.g. allow $\frac{\mathrm{d}u}"
       r"{\mathrm{d}x}=\frac{1}{2}x^{-\frac{1}{2}}\to\int\frac{x}{1+\sqrt{x}}\,\mathrm{d}x=\int\frac{x}{u}\times"
       r"\frac{x^{\frac{1}{2}}}{2}\,\mathrm{d}u=\int\mathrm{h}(u)\,\mathrm{d}u$ but not $\frac{\mathrm{d}u}{\mathrm{d}x}="
       r"\frac{1}{2}x^{-\frac{1}{2}}\to\int\frac{x}{1+\sqrt{x}}\,\mathrm{d}x=\int\frac{x}{u}\times\frac{x^{-\frac{1}"
       r"{2}}}{2}\,\mathrm{d}u=\int\mathrm{h}(u)\,\mathrm{d}u$",
       r"A1 (AO 1.1b): $" + Q12ALIM + r"=\int_1^5\frac{2(u-1)^3}{u}\,\mathrm{d}u$. Notes: All correct with correct "
       r"limits and no errors. The “$\mathrm{d}u$” must be present but may have been omitted along the way but it must "
       r"have been seen at least once before the final answer. The limits can be seen as part of the integral or "
       r"stated separately."],
      False, 34),
    e("12b", "12(b)", INT, "8.5, 8.3, 8.2", 4, LATEX["12b"],
      [r"M1 (AO 3.1a): $2\int\frac{u^3-3u^2+3u-1}{u}\,\mathrm{d}u=2\int\left(u^2-3u+3-\frac{1}{u}\right)\mathrm{d}u="
       r"\ldots$. Notes: Realises the requirement to cube the bracket and divide through by $u$ and makes progress "
       r"with the integration to obtain at least 3 terms of the required form e.g. 3 from $ku^3$, $ku^2$, $ku$, "
       r"$k\ln u$",
       r"A1 (AO 1.1b): $=(2)\left[\frac{u^3}{3}-\frac{3u^2}{2}+3u-\ln u\right]$. Notes: Correct integration. This mark "
       r"can be scored with the “2” still outside the integral or even if it has been omitted. But if the “2” has been "
       r"combined with the integrand, the integration must be correct.",
       r"dM1 (AO 2.1): $=2\left[\frac{5^3}{3}-\frac{3(5)^2}{2}+3(5)-\ln5-\left(\frac{1}{3}-\frac{3}{2}+3-\ln1\right)"
       r"\right]$. Notes: Completes the process by applying their “changed” limits and subtracts the right way round "
       r"$\textbf{Depends on the first method mark.}$",
       r"A1 (AO 1.1b): $=\frac{104}{3}-2\ln5$. Notes: Cao (Allow equivalents for $\frac{104}{3}$ e.g. $\frac{208}{6}$)"],
      False, 34),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", DIFF, "7.5, 7.4, 5.4", 3, LATEX["13a"],
      [r"B1 (AO 1.1b): $y=\mathrm{cosec}^3\theta\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}\theta}=-3\mathrm{cosec}^2"
       r"\theta\,\mathrm{cosec}\theta\cot\theta$. Notes: Correct expression for $\frac{\mathrm{d}y}{\mathrm{d}\theta}$ "
       r"seen or implied in any form e.g. $\frac{-3\cos\theta}{\sin^4\theta}$",
       r"M1 (AO 1.1b): $" + DYDX + r"=\frac{\mathrm{d}y}{\mathrm{d}\theta}\div\frac{\mathrm{d}x}{\mathrm{d}\theta}$. "
       r"Notes: Obtains $\frac{\mathrm{d}x}{\mathrm{d}\theta}=k\cos2\theta$ or $\alpha\cos^2\theta+\beta\sin^2\theta$ "
       r"(from product rule on $\sin\theta\cos\theta$) and attempts $" + DYDX + r"=\frac{\mathrm{d}y}{\mathrm{d}\theta}"
       r"\div\frac{\mathrm{d}x}{\mathrm{d}\theta}$",
       r"A1 (AO 1.1b): $" + DYDX + r"=\frac{-3\mathrm{cosec}^3\theta\cot\theta}{2\cos2\theta}$. Notes: Correct "
       r"expression in any form. May see e.g. $\frac{-3\cos\theta}{2\sin^4\theta\cos2\theta}$, $-\frac{3}{4\sin^4"
       r"\theta\cos\theta-2\sin^3\theta\tan\theta}$"],
      False, 38),
    e("13b", "13(b)", DIFF, "7.5, 5.4, 5.3", 3, LATEX["13b"],
      [r"M1 (AO 3.1a): $y=8\Rightarrow\mathrm{cosec}^3\theta=8\Rightarrow\sin^3\theta=\frac{1}{8}\Rightarrow\sin\theta="
       r"\frac{1}{2}$. Notes: Recognises the need to find the value of $\sin\theta$ or $\theta$ when $y=8$ and uses the "
       r"$y$ parameter to establish its value. This should be correct work leading to $\sin\theta=\frac{1}{2}$ or e.g. "
       r"$\theta=\frac{\pi}{6}$ or $30^\circ$.",
       r"M1 (AO 2.1): $\theta=\frac{\pi}{6}\Rightarrow" + DYDX + r"=\frac{-3\mathrm{cosec}^3\left(\frac{\pi}{6}\right)"
       r"\cot\left(\frac{\pi}{6}\right)}{2\cos\left(\frac{2\pi}{6}\right)}=\ldots$ or $\sin\theta=\frac{1}{2}\Rightarrow"
       + DYDX + r"=\frac{\frac{-3}{\sin^3\theta}\times\frac{\cos\theta}{\sin\theta}}{2(1-2\sin^2\theta)}=\frac{-3\times8"
       r"\times\frac{\sqrt{3}/2}{1/2}}{2\left(1-2\times\frac{1}{4}\right)}$. Notes: Uses their value of $\sin\theta$ or "
       r"$\theta$ in their $" + DYDX + r"$ from part (a) (working in exact form) in an attempt to obtain an exact value "
       r"for $" + DYDX + r"$. May be implied by a correct exact answer. If no working is shown but an exact answer is "
       r"given you may need to check that this follows their $" + DYDX + "$.",
       r"A1 (AO 2.2a): $=-24\sqrt{3}$. Notes: Deduces the correct gradient"],
      False, 38),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", DIFF, "7.6, 7.4", 4, LATEX["14a"],
      [r"B1 (AO 3.1b): $\frac{\mathrm{d}V}{\mathrm{d}t}=0.48-0.1h$. Notes: Identifies the correct expression for "
       r"$\frac{\mathrm{d}V}{\mathrm{d}t}$ according to the model",
       r"B1 (AO 3.1b): $V=24h\Rightarrow\frac{\mathrm{d}V}{\mathrm{d}h}=24$ or $\frac{\mathrm{d}h}{\mathrm{d}V}="
       r"\frac{1}{24}$. Notes: Identifies the correct expression for $\frac{\mathrm{d}V}{\mathrm{d}h}$ according to the "
       r"model",
       r"M1 (AO 2.1): $\frac{\mathrm{d}h}{\mathrm{d}t}=\frac{\mathrm{d}V}{\mathrm{d}t}\times\frac{\mathrm{d}h}"
       r"{\mathrm{d}V}=\frac{0.48-0.1h}{24}$ or e.g. $\frac{\mathrm{d}V}{\mathrm{d}t}=\frac{\mathrm{d}V}{\mathrm{d}h}"
       r"\frac{\mathrm{d}h}{\mathrm{d}t}\Rightarrow0.48-0.1h=24\frac{\mathrm{d}h}{\mathrm{d}t}$. Notes: Applies "
       r"$\frac{\mathrm{d}h}{\mathrm{d}t}=\frac{\mathrm{d}V}{\mathrm{d}t}\times\frac{\mathrm{d}h}{\mathrm{d}V}$ or "
       r"equivalent correct formula with their $\frac{\mathrm{d}V}{\mathrm{d}t}$ and $\frac{\mathrm{d}V}{\mathrm{d}h}$ "
       r"which may be implied by their working",
       r"A1* (AO 1.1b): $1200\frac{\mathrm{d}h}{\mathrm{d}t}=24-5h$*. Notes: Correct equation obtained with no errors "
       r"Note that: $\frac{\mathrm{d}V}{\mathrm{d}t}=0.48-0.1h\Rightarrow\frac{\mathrm{d}h}{\mathrm{d}t}=\frac{0.48-0.1h}"
       r"{24}\Rightarrow1200\frac{\mathrm{d}h}{\mathrm{d}t}=24-5h$* scores B1B0M0A0. There must be clear evidence "
       r"where the “24” comes from and evidence of the correct chain rule being applied."],
      True, 40),
    e("14b", "14(b)", INT, "8.7, 6.7", 6, LATEX["14b"],
      [r"M1 (AO 3.1a): $1200\frac{\mathrm{d}h}{\mathrm{d}t}=24-5h\Rightarrow\int\frac{1200}{24-5h}\,\mathrm{d}h=\int"
       r"\mathrm{d}t\Rightarrow$ e.g. $\alpha\ln(24-5h)=t(+c)$ oe or $1200\frac{\mathrm{d}h}{\mathrm{d}t}=24-5h"
       r"\Rightarrow\frac{\mathrm{d}t}{\mathrm{d}h}=\frac{1200}{24-5h}\Rightarrow$ e.g. $t(+c)=\alpha\ln(24-5h)$ oe. "
       r"Notes: Adopts a correct strategy by separating the variables correctly or rearranges to obtain $\frac{"
       r"\mathrm{d}t}{\mathrm{d}h}$ correctly in terms of $h$ $\textbf{and}$ integrates to obtain $t=\alpha\ln(24-5h)"
       r"(+c)$ or equivalent (condone missing brackets around the “$24-5h$”) and $+c$ not required for this mark.",
       r"A1 (AO 1.1b): $t=-240\ln(24-5h)(+c)$ oe. Notes: Correct equation in any form and $+c$ not required. Do not "
       r"condone missing brackets unless they are implied by subsequent work.",
       r"M1 (AO 3.4): $t=0,h=2\Rightarrow0=-240\ln(24-10)+c\Rightarrow c=\ldots(240\ln14)$. Notes: Substitutes $t=0$ "
       r"and $h=2$ to find their constant of integration (there must have been some attempt to integrate)",
       r"A1 (AO 1.1b): $t=240\ln(14)-240\ln(24-5h)$. Notes: Correct equation in any form",
       r"ddM1 (AO 2.1): $t=240\ln\frac{14}{24-5h}\Rightarrow\frac{t}{240}=\ln\frac{14}{24-5h}\Rightarrow\mathrm{e}^{"
       r"\frac{t}{240}}=\frac{14}{24-5h}$ $\Rightarrow14\mathrm{e}^{-\frac{t}{240}}=24-5h\Rightarrow h=\ldots$. Notes: "
       r"Uses fully correct log work to obtain $h$ in terms of $t$. $\textbf{This depends on}$ "
       r"$\underline{\textbf{both}}$ $\textbf{previous method marks.}$",
       r"A1 (AO 3.3): $h=4.8-2.8\mathrm{e}^{-\frac{t}{240}}$ oe e.g. $h=\frac{24}{5}-\frac{14}{5}\mathrm{e}^{-"
       r"\frac{t}{240}}$. Notes: Correct equation Note that the marks may be earned in a different order e.g.: "
       r"$t+c=-240\ln(24-5h)\Rightarrow-\frac{t}{240}+d=\ln(24-5h)\Rightarrow A\mathrm{e}^{-\frac{t}{240}}=24-5h$ "
       r"$t=0,h=2\Rightarrow A=14\Rightarrow14\mathrm{e}^{-\frac{t}{240}}=24-5h\Rightarrow h=4.8-2.8\mathrm{e}^{-"
       r"\frac{t}{240}}$ Score as M1 A1 as in main scheme then M1: Correct work leading to $A\mathrm{e}^{\alpha t}="
       r"24-5h$ (must have a constant “A”) A1: $A\mathrm{e}^{-\frac{t}{240}}=24-5h$ ddM1: Uses $t=0$, $h=2$ in an "
       r"expression of the form above to find $A$ A1: $h=4.8-2.8\mathrm{e}^{-\frac{t}{240}}$"],
      True, 40),
    e("14c", "14(c)", INT, "8.8, 6.7", 2, LATEX["14c"],
      [r"M1 (AO 3.1b): Examples: • As $t\to\infty$, $\mathrm{e}^{-\frac{t}{240}}\to0$ • When $h>4.8$, "
       r"$\frac{\mathrm{d}V}{\mathrm{d}t}<0$ • Flow in = flow out at max $h$ so $0.1h=4.8\to h=4.8$ • As $\mathrm{e}^{-"
       r"\frac{t}{240}}>0$, $h<4.8$ • $h=5\Rightarrow\frac{\mathrm{d}V}{\mathrm{d}t}=-0.02$ or $\frac{\mathrm{d}h}"
       r"{\mathrm{d}t}=-\frac{1}{1200}$ • $\frac{\mathrm{d}h}{\mathrm{d}t}=0\Rightarrow h=4.8$ • $h=5\Rightarrow4.8-2.8"
       r"\mathrm{e}^{-\frac{t}{240}}=5\Rightarrow\mathrm{e}^{-\frac{t}{240}}<0$. Notes: See scheme for some examples",
       r"A1 (AO 3.2a): • The limit for $h$ (according to the model) is 4.8m and the tank is 5m high so the tank will "
       r"never become full • If $h=5$ the tank would be emptying so can never be full • The equation can’t be solved "
       r"when $h=5$. Notes: Makes a correct interpretation for their method. There must be no incorrect working or "
       r"contradictory statements. This is not a follow through mark and if their equation in (b) is used it must be "
       r"correct."],
      True, 40),

    # ---------------- Q15 ----------------
    e("15a", "15(a)", TRIG, "5.6", 3, LATEX["15a"],
      [r"B1 (AO 1.1b): $R=\sqrt{5}$. Notes: $R=\sqrt{5}$ only.",
       r"M1 (AO 1.1b): $\tan\alpha=\frac{1}{2}$ or $\sin\alpha=\frac{1}{\sqrt{5}}$ or $\cos\alpha=\frac{2}{\sqrt{5}}"
       r"\Rightarrow\alpha=\ldots$. Notes: Proceeds to a value for $\alpha$ from $\tan\alpha=\pm\frac{1}{2}$ or "
       r"$\sin\alpha=\pm\frac{1}{\text{“}R\text{”}}$ or $\cos\alpha=\pm\frac{2}{\text{“}R\text{”}}$ It is implied by "
       r"either awrt 0.464 (radians) or awrt 26.6 (degrees)",
       r"A1 (AO 1.1b): $\alpha=0.464$. Notes: $\alpha=$ awrt 0.464"],
      False, 44),
    e("15b", "15(b)", TRIG, "5.9, 5.6", 3, LATEX["15b"],
      [r"B1ft (AO 3.4): (b)(i) $" + Q15B1 + r"$. Notes: For $(" + Q15B1 + r")$ m or awrt 7.47 m and remember to isw. "
       r"Condone lack of units. Follow through on their $R$ value so allow $3+2\times$Their $R$. (Allow in decimals "
       r"with at least 3sf accuracy)",
       r"M1 (AO 3.4): (ii) $\cos(0.5t+0.464)=1\Rightarrow0.5t+0.464=2\pi\Rightarrow t=\ldots$. Notes: Uses $0.5t\pm"
       r"\text{“}0.464\text{”}=2\pi$ to obtain a value for $t$ Follow through on their 0.464 but this angle must be in "
       r"radians. It is possible in degrees but only using $0.5t\pm\text{“}26.6\text{”}=360$",
       r"A1 (AO 1.1b): $t=11.6$. Notes: Awrt 11.6",
       r"ALT: Alternative for (b) — M1: $H=3+4\cos(0.5t)-2\sin(0.5t)\Rightarrow\frac{\mathrm{d}H}{\mathrm{d}t}=-2\sin"
       r"(0.5t)-\cos(0.5t)=0$ $\Rightarrow\tan(0.5t)=-\frac{1}{2}\Rightarrow0.5t=2.677\ldots,5.819\ldots\Rightarrow t="
       r"5.36,11.6$. Notes: For a complete method: Attempts $\frac{\mathrm{d}H}{\mathrm{d}t}$ and attempts to solve "
       r"$\frac{\mathrm{d}H}{\mathrm{d}t}=0$ for $t$",
       r"ALT: Alternative for (b) — A1: $t=11.6$. Notes: For $t=$ awrt 11.6",
       r"ALT: Alternative for (b) — B1ft: $t=11.6\Rightarrow H=7.47$. Notes: For awrt 7.47 or $3+2\times$Their $R$"],
      True, 44),
    e("15c", "15(c)", TRIG, "5.9, 5.7, 5.6", 4, LATEX["15c"],
      [r"M1 (AO 3.4): $" + Q15B1 + r"\cos(0.5t+0.464)=0$ $\cos(0.5t+0.464)=-\frac{3}{2\sqrt{5}}$. Notes: Uses the "
       r"model and sets $3+2\text{“}\sqrt{5}\text{”}\cos(\ldots)=0$ and proceeds to $\cos(\ldots)=k$ where $|k|<1$. "
       r"Allow e.g. $3+2\text{“}\sqrt{5}\text{”}\cos(\ldots)<0$",
       r"dM1 (AO 1.1b): $\cos(0.5t+0.464)=-\frac{3}{2\sqrt{5}}\Rightarrow0.5t+0.464=\cos^{-1}\left(-\frac{3}{2\sqrt{5}}"
       r"\right)$ $\Rightarrow t=2\left(\cos^{-1}\left(-\frac{3}{2\sqrt{5}}\right)-0.464\right)$. Notes: Solves "
       r"$\cos(0.5t\pm\text{“}0.464\text{”})=k$ where $|k|<1$ to obtain at least one value for $t$ This requires e.g. "
       r"$2\left(\pi+\cos^{-1}(k)\pm\tan^{-1}\left(\frac{1}{2}\right)\right)$ or e.g. $2\left(\pi-\cos^{-1}(k)\pm"
       r"\tan^{-1}\left(\frac{1}{2}\right)\right)$ $\textbf{Depends on the previous method mark.}$",
       r"dM1 (AO 3.1b): So the time required is e.g.: $2(3.977\ldots-0.464)-2(2.306\ldots-0.464)$. Notes: A fully "
       r"correct strategy to find the required duration. E.g. finds 2 consecutive values of $t$ when $H=0$ and "
       r"subtracts. Alternatively finds $t$ when $H$ is minimum and uses the times found correctly to find the required "
       r"duration. $\textbf{Depends on the previous method mark.}$ $\underline{\textbf{Examples:}}$ Second time at "
       r"water level – first time at water level: $2\left(\pi+\cos^{-1}\left(\frac{3}{2\sqrt{5}}\right)-\tan^{-1}\left("
       r"\frac{1}{2}\right)\right)-2\left(\pi-\cos^{-1}\left(\frac{3}{2\sqrt{5}}\right)-\tan^{-1}\left(\frac{1}{2}"
       r"\right)\right)=7.02685\ldots-3.68492\ldots$ $2\times$(first time at minimum point – first time at water "
       r"level): $2\left(2\left(\pi-\tan^{-1}\left(\frac{1}{2}\right)\right)-2\left(\pi-\cos^{-1}\left(\frac{3}"
       r"{2\sqrt{5}}\right)-\tan^{-1}\left(\frac{1}{2}\right)\right)\right)=2(5.35589\ldots-3.68492\ldots)$ "
       r"$\textbf{Note that both of these examples equate to}$ $4\cos^{-1}\left(\frac{3}{2\sqrt{5}}\right)$ "
       r"$\textbf{which is not immediately obvious but may be seen as an overall method.}$ $\textbf{There may be other "
       r"methods – if you are not sure if they deserve credit send to review.}$",
       r"A1 (AO 1.1b): $=3.34$. Notes: Correct value. Must be 3.34 ($\textbf{not}$ awrt). "
       r"$\underline{\textbf{Special Cases in (c):}}$ Note that if candidates have an incorrect $\alpha$ and have e.g. "
       r"$" + Q15B1 + r"\cos(0.5t-0.464)$, this has no impact on the final answer. So for candidates using $" + Q15B1
       + r"\cos(0.5t\pm\alpha)$ in (c) allow all the marks including the A mark as a correct method should always "
       r"lead to 3.34 $\underline{\textbf{Some values to look for:}}$ $0.5t\pm\text{“}0.464\text{”}=\pm2.306,\pm3.977,"
       r"\ \pm8.598,\pm10.26$"],
      True, 44),
    e("15d", "15(d)", TRIG, "5.9, 2.11", 1, LATEX["15d"],
      [r"B1 (AO 3.5c): e.g. the “3” would need to vary. Notes: Correct refinement e.g. As in scheme. If they suggest a "
       r"specific function to replace the “3” then it must be sensible e.g. a trigonometric function rather than e.g. "
       r"a quadratic/linear one."],
      True, 44),
]

W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "As the first question of the paper this did its job in settling nervous students: a straightforward "
            "question on arithmetic series which was answered correctly by the vast majority of students.", NO),
        ({"a"}, r"Where mistakes were made the most common error in part (a) was to use the 21st term as 21, rather "
                r"than 24, or students used an incorrect formula for the $n$th term, using $u_n=a+nd$ and not "
                r"$u_n=a+(n-1)d$."),
        ({"a"}, r"A few students incorrectly treated 24 as the sum of the first 21 terms in their attempt to find $d$."),
        ({"b"}, r"For part (b) most students used the correct formula and therefore gained the method mark, however "
                r"some lost the accuracy mark from the incorrect common difference, and a very small minority of "
                r"students used $S_{500}=\frac{n}{2}(a+(n-1)d)$ rather than $S_{500}=\frac{n}{2}(2a+(n-1)d)$."),
    ],
    "02": [
        (W, "This question was well answered with the modal mark being full marks.", NO),
        ({"a"}, "Part (a) was the least well answered part where and it is clear that students have difficulty with "
                "the concept of range.", NO),
        ({"a"}, r"Incorrect answers included $y<7$and $y\geqslant7$."),
        ({"a"}, r"Some candidates attempted to use the graph’s $x$-intercepts in their work, so incorrect answers such "
                r"as $-\frac{\sqrt{14}}{4}<x<\frac{\sqrt{14}}{4}$ appeared occasionally.", NO),
        ({"b"}, "In contrast, part (b) was well answered, with most candidates gaining all of the marks."),
        ({"b"}, r"The most common approach was to find $\mathrm{f}(1.8)=0.52$ and then $\mathrm{g}(x)=0.975$.",
         {"note": "the mark scheme has g(0.52) = 0.975"}),
        ({"b"}, r"Some candidates correctly established the composite function $\mathrm{gf}(x)$ and then calculated "
                r"$\mathrm{gf}(1.8)$."),
        ({"b"}, r"There were occasional instances of finding $\mathrm{fg}(1.8)$ by mistake."),
        ({"c"}, "Similarly (c) was well answered."),
        ({"c"}, r"Most candidates knew the process of finding the inverse function by rearranging $y=\frac{3x}{5x-1}$ "
                r"to make $x$ the subject and switching the $x$’s and $y$’s (or by switching first and then "
                r"rearranging) and many successfully reached the correct answer of $\mathrm{g}^{-1}(x)=\frac{x}{5x-3}$."),
    ],
    "03": [
        (W, "This 3 mark question was attempted by almost all students and differentiated between those who could "
            "apply laws of logarithms and those who could not.", NO),
        (W, "It was generally a well answered question and most students were able to get some marks and a large "
            "majority scored full marks.", NO),
        (W, r"A few students showed an invalid line of $\log_3(12y+5)-\log_3(1-3y)=2\Rightarrow\frac{\log_3(12y+5)}"
            r"{\log_3(1-3y)}=2$ before recovering the error and continuing to the correct value of $\frac{4}{39}$ for "
            r"$y$, so only scored 1 of the 3 available marks."),
        (W, "A few students were unable to apply the subtraction law but they were often able to score the B mark for "
            "9 seen."),
        (W, "This was a straight forward question on logarithms so it was nice to see the candidates were generally "
            "prepared and those that correctly removed the logs were, on the whole, able to go on get full marks.",
         NO),
        (W, r"A few students make slips when solving their linear equation, obtaining $\frac{39}{4}$ instead of "
            r"$\frac{4}{39}$."),
        (W, "A few also tried to use base e incorrectly, and a minority tried expanding the logs, hence getting no "
            "marks."),
    ],
    "04": [
        (W, r"The first method mark in this question was often gained for sight of $4\left(\frac{\theta}{2}\right)$ but "
            r"the second mark proved more challenging, with errors seen in the correct application of the "
            r"$\cos\theta$ small-angle approximation."),
        (W, r"Some candidates missed out the square completely and just wrote $3\left(1-\frac{\theta^2}{2}\right)$."),
        (W, r"Many of those who did attempt to expand $3\left(1-\frac{\theta^2}{2}\right)^2$ made mistakes with "
            r"fractions and powers, with $3\left(1-\theta^2+\frac{\theta^2}{4}\right)$ occasionally seen.", NO),
        (W, r"Candidates who realised they could use $3\cos^2\theta=3(1-\sin^2\theta)$ and then use the $\sin\theta$ "
            r"approximation fared better."),
        (W, "In contrast, those using the double angle formula performed less well, with many fraction and sign "
            "errors seen with this approach.", NO),
        (W, r"It was not uncommon to see candidates who followed the main $\cos\theta$ method ‘multiply everything by "
            r"4’ at the end leading to an incorrect final expression of $12+8\theta-12\theta^2\{+3\theta^4\}$, "
            r"forfeiting the final A mark.", NO),
    ],
    "05": [
        (W, "This question was accessible to the majority of students however part (b) proved to be a good "
            "discriminator with only the most able gaining all 7 marks."),
        ({"a"}, "The majority of students gained the first three marks of this questions by correctly differentiating "
                "the expression twice."),
        ({"a"}, "A few arithmetic errors were seen occasionally, although if this was the case then students would "
                "only lose 1 out of the three marks.", BACK),
        ({"b"}, "Part (b) differentiated out the students to a greater extend."),
        ({"b"}, "Most students could identify the correct method to find the stationary point, although there were a "
                "disappointing number of students who failed to follow this up with a concluding statement or "
                "preamble.", NO),
        ({"b"}, "A number of students got confused between parts (i) and (ii) and tried to use the second derivative "
                "to identify stationary points."),
        ({"b"}, r"The most common method to identify the stationary point was using the first derivative and "
                r"substituting the value $x=1$, although there were a significant number who chose to deduce the "
                r"value $x=1$ by factorising their cubic expression."),
        ({"b"}, "Both approaches tended to lead to a positive outcome, and full marks."),
        ({"b"}, "Part (ii) was much more mixed in response."),
        ({"b"}, "A significant number of students gained no marks on this part as they assumed that when both first "
                "and second derivative equal zero then the point is a point of inflection."),
        ({"b"}, "Of those students who successfully answered this question there were an equal number of students "
                "who considered the first derivative as those that considered the second derivative.", NO),
        ({"b"}, "Most of these students considered an appropriate intervals to gain full marks here, however a "
                "significant number of students considered inappropriate intervals such as 0 and 2 or 1.5 and so "
                "were unable to gain the accuracy mark.", {"ref": True}),
    ],
    "06": [
        (W, "Performance on this question was variable and approximately 25% of candidates failed to score any "
            "marks."),
        ({"a"}, "(a) The majority of candidates were successful with this part."),
        ({"a"}, r"Common errors were stating that angle $AOB$ was $\frac{1}{2}\theta$ or $\frac{180-\theta}{2}$, "
                r"sometimes following through to gain marks in (b) and (c)."),
        ({"b"}, r"(b) Most candidates followed the correct strategy for finding the area of the logo by finding the "
                r"sum of the areas of sectors $OCD$, $OAB$ and $OEF$."),
        ({"b"}, r"Common errors were omitting the brackets round the $2r$ when finding the area of the sector $OCD$ "
                r"and algebraic errors when simplifying their expression for the sum of the two smaller sectors $OAB$ "
                r"and $OEF$."),
        ({"b"}, "A small number of candidates showed insufficient working when simplifying their area of the sum of "
                "the two smaller sectors to arrive at the given result."),
        ({"c"}, "(c) Again, most candidates attempted this part well."),
        ({"c"}, r"A common errors was not to include $4r$ in the expression for the perimeter of the logo and there "
                r"were some algebraic errors when simplifying the expression for the sum of the perimeters of sectors "
                r"$OAB$ and $OEF$."),
    ],
    "07": [
        ({"a"}, "Part (a) was generally well answered, with most students able to differentiate correctly and "
                "understand the need to use the first derivate to find the gradient of the tangent line."),
        ({"a"}, "A few tried to use the diagram to obtain the gradient, even after differentiating correctly so were "
                "only able to gain the first B mark, but they were in a minority."),
        ({"a"}, r"The vast majority of candidates who correctly differentiated (a few integrated, hence lost the "
                r"marks), were able to go on to find the correct equation of the line, often using $y=mx+c$ rather "
                r"than $y-y_1=m(x-x_1)$."),
        ({"a"}, r"A small minority displayed poor algebraic skills when rearranging their linear equation to find $c$, "
                r"and a few used a gradient of $\frac{1}{2}$ instead of 2."),
        ({"b"}, r"In part (b), most students understood the need to show that the $y$-intercepts were the same for "
                r"both the line and the curve, but often candidates struggled to write an adequate conclusion to "
                r"verify they meet again, and hence lost this mark.", NO),
        ({"c"}, "Most students were able to gain some marks in part (c) but a score of two out of four was common."),
        ({"c"}, r"Those who got this, generally integrated the curve, obtaining a correct area of $\frac{455}{12}$, "
                r"but then failed to go any further.", BACK),
        ({"c"}, r"Very few students used the area of a trapezium formula, instead preferring to integrate the "
                r"$(2x-23)$ or to split the area into a rectangle and triangle."),
        ({"c"}, "Of those who attempted the area of the trapezium a number struggled to get the correct dimensions.",
         NO),
        ({"c"}, "Fully correct solutions using a trapezium were rare."),
        ({"c"}, "A few students translated the curve and line upwards correctly by 23 units and often scored full "
                "marks using this method."),
        ({"c"}, r"Those students who attempted the curve minus the line, often struggled with the constant 23, or "
                r"incorrectly collected like terms (e.g. an $x$ term with an $x^2$ term).", NO),
    ],
    "08": [
        (W, "Many candidates gained some credit in this question but few gained full marks."),
        ({"a"}, "Part (a) was relatively well answered."),
        ({"a"}, "Most candidates identified that implicit differentiation was required and made good progress by "
                "correctly differentiating the given equation."),
        ({"a"}, r"When mistakes happened at this stage, they usually appeared in the differentiation of $qxy$ rather "
                r"than in the differentiation of $px^3$or $3y^2$.", NO),
        ({"a"}, "There were a few candidates, however, who clearly were not able to employ implicit differentiation "
                "and who gained no marks."),
        ({"a"}, r"Once a differentiated expression had been obtained, many were able to rearrange correctly to make "
                r"$" + DYDX + r"$ the subject, obtaining the required answer of $" + DYDX + r"=\frac{-3px^2-qy}"
                r"{qx+6y}$."),
        ({"a"}, r"A common mistake, however, was to make sign errors in the rearranging process and incorrect answers "
                r"like $" + DYDX + r"=\frac{3px^2+qy}{qx+6y}$ and $" + DYDX + r"=\frac{-3px^2+qy}{qx+6y}$were "
                r"surprisingly common following correct differentiation."),
        ({"b"}, r"In (b) most candidates gained some marks but few used a fully correct method to achieve the correct "
                r"answer of $p=2$and $q=-5$."),
        ({"b"}, r"Most were able to rearrange the equation of the normal, and identified that its gradient was "
                r"$-\frac{19}{26}$.", NO),
        ({"b"}, r"They then identified the gradient of the tangent as $\frac{26}{19}$and used their result from (a) at "
                r"$x=-1$and $y=-4$ to attempt to form a correct equation in $p$ and $q$ such as $\frac{3p-4q}{q+24}="
                r"\frac{26}{19}$.", BACK),
        ({"b"}, r"A number of candidates incorrectly equated the numerators and denominators to form the equations "
                r"$3p-4q=26$and $q+24=19$and solved these to fortuitously arrive at the correct solution, losing most "
                r"marks in (b).", NO),
        ({"b"}, r"Another incorrect approach was to form the equation of the normal of the form $y+4=\frac{q+24}"
                r"{4q-3p}(x+1)$and to rearrange to the form $\alpha x+\beta y+\gamma=0$followed by ‘comparing "
                r"coefficients’ with $19x+26y+123=0$(an incorrect method)."),
        ({"b"}, r"Many candidates successfully substituted $x=-1$and $y=-4$ into the equation of C to get $p-4q=22$."),
        ({"b"}, "This step was missed, however, by quite a few candidates, who could not then gain full marks for the "
                "question.", BACK),
    ],
    "09": [
        (W, r"This question was fairly well answered by a number of candidates, who understood the need to use the "
            r"sum to infinity formula, but a sizeable majority made little or no progress, not realising for example, "
            r"that the sum started from $n=2$ and not $n=1$ – hence they often did not get the first mark for a "
            r"correct first term and/or common ratio."),
        (W, r"$\frac{9}{16}$ was seen fairly often, but not always attributed to the first term, with some candidates "
            r"thinking this was the value of the sum.", NO),
        (W, "One candidate misread the infinity symbol as an 8 and applied the sum to 8 terms correctly, but was "
            "obviously not able to score any marks."),
        (W, r"A number of students found the sum to infinity, using $n=1$ to infinity and then subtracting the first "
            r"term."),
        (W, "This was done well by candidates who went down this route.", BACK),
        (W, "Unfortunately, many students achieved no marks on this part due to a wide variety of errors at the "
            "beginning."),
        (W, "Calculating cos (360) on the calculator in radians instead of degrees was seen."),
        (W, r"Some tried to split the summation incorrectly into $\sum_2^\infty\left(\frac{3}{4}\right)^n\times\sum_1^"
            r"\infty\cos180n$ and find the sum to infinity of the trigonometric terms separately."),
        (W, r"A few wrote $\left(\frac{3}{4}\right)^2\cos(360)$ but did not evaluate the cos(360)."),
        (W, "There were some very good solutions but in many responses there was often a lack of clear structure to "
            "their proof."),
    ],
    "10": [
        ({"a"}, "The majority of candidates scored both marks for part (a)."),
        ({"a"}, "A common error was omitting base 10 when writing their final equation."),
        ({"a"}, "In “show that” questions, we need to see the equation as stated in the question."),
        ({"b"}, "Part (b) was demanding for many candidates, with confusion as to how to correctly deal with the log "
                "terms."),
        ({"b"}, r"Most candidates who were successful found the value of $b$ by finding the gradient of the line."),
        ({"b"}, r"A less popular but usually successful approach was using simultaneous equations to eliminate $b$."),
        ({"b"}, r"Solving the equation $\log_{10}a=\frac{9}{26}$to find the value of $a$ caused some problems."),
        ({"b"}, r"The question required a complete equation for the model, so just stating the correct values of $a$ "
                r"and $b$without the equation written explicitly meant candidates scored 3 out of 4 marks, which was "
                r"a very common error.",
         {"note": "part (b) is worth 3 marks; the mark scheme withholds only its final A1 when the equation is not "
                  "written"}),
        ({"c"}, r"Part (c) was very rarely completed successfully."),
        ({"c"}, r"Common errors were thinking $a$ was the intercept on the T axis or the time for the initial swing of "
                r"the pendulum."),
    ],
    "11": [
        ({"a"}, "In general part (a) was poorly answered, with many candidates seemingly unfamiliar with sketching "
                "modulus functions."),
        ({"a"}, "The majority of candidates scored at least one B mark for their upturned V but a V shape was "
                "occasionally seen, typically scoring no marks."),
        ({"a"}, "Of those with the correct, many could not find the correct intersections and maximum point.", BACK),
        ({"a"}, r"Finding the correct $y$ intercept seemed to be less challenging than finding the $x$ intercept or "
                r"the maximum point."),
        ({"b"}, "Part (b) was better answered than part (a)."),
        ({"b"}, r"Many candidates made correct attempts to find the second critical value of $x=\frac{5k}{3}$, "
                r"gaining the M mark, but $x=k$ was often not found."),
        ({"b"}, r"The ‘squaring’ method was occasionally seen, but as this led to a 3TQ in $x$ and $k$ and which was "
                r"hard to factorise this was rarely successful.", NO),
        ({"b"}, "The final A mark was often lost due to lack of correct set notation."),
        ({"c"}, "There were few fully successful answers to part (c) but some candidates could write down one correct "
                "co-ordinate."),
        ({"c"}, r"There was occasional success seen by candidates who used algebra by writing the transformed "
                r"function as $y=(3-5k)+5\left|x-3k\right|$."),
    ],
    "12": [
        (W, "This question discriminated well with weaker students generally able to pick up 2 marks and many able "
            "students were able to gain full marks."),
        ({"a"}, "Part (a) was a relatively straightforward substitution question and as such many students made a "
                "very positive attempt at this part.", NO),
        ({"a"}, r"There were a mixture of methods used to answer part (a) with most students correctly identifying "
                r"$\mathrm{d}u/\mathrm{d}x$ or $\mathrm{d}x/\mathrm{d}u$."),
        ({"a"}, "Those that found the second of these found the substitution very straightforward and generally went "
                "on to achieve full marks.", BACK),
        ({"a"}, r"Students who found $\mathrm{d}u/\mathrm{d}x$ instead sometimes struggled with the indices and how to "
                r"deal with the negative power when dividing and hence made mistakes here."),
        ({"a"}, "There were a small number of students who simply failed to make any attempt at this question, and "
                "generally these students gave up on the question entirely.", NO),
        ({"a"}, r"A few students lost the accuracy mark for not stating the limits or omitting $\mathrm{d}u$."),
        ({"b"}, r"In part (b) it was good to see many students recognised that “hence” meant that the answer in part "
                r"(a) must be used and proceeded with the correct method of expanding the cubic and dividing by $u$, "
                r"proceeding correctly to the correct answer.", NO),
        ({"b"}, "If this was done correctly these students would usually go on to successfully apply the limits "
                "correctly and gain full marks.", BACK),
        ({"b"}, "Unfortunately, a number of students attempted a method of integration by parts or some kind of "
                "product rule and therefore gained no marks here."),
        ({"b"}, "Unfortunately a few did not take heed of the “hence” and proceeded to integrate the original "
                "expression scoring no marks in this part."),
        ({"b"}, r"Some weaker students split the integral into an incorrect sum of 2 fractions eg $\frac{2}{u}+"
                r"\frac{(u-1)^3}{u}$ and then used integration by parts which they tended to give up on half way "
                r"through."),
        ({"b"}, "The method most successful was to take the 2 outside the integral, then integrate."),
        ({"b"}, r"Those that multiplied by 2 were more likely to make slips on the value of the coefficients for the "
                r"3rd and 4th term.", NO),
        ({"b"}, "Several students lost the final 2 marks as they used incorrect limits either 16 and 0 or 5 and 0."),
    ],
    "13": [
        (W, r"This question involving differentiation of parametric equations was found to be challenging by the "
            r"majority of students, particularly the differentiation of $y=\mathrm{cosec}^3\theta$ and part (b)."),
        ({"a"}, r"The majority of candidates knew what was expected in part (a) and proceeded to attempt to use the "
                r"chain rule to find $" + DYDX + r"$, however they found differentiating $y=\mathrm{cosec}^3\theta$ "
                r"challenging."),
        ({"a"}, r"Some did not check in the formula book that the derivative of cosec $\theta$ was negative, or omitted "
                r"the constant 3, and this cost 3 of the 6 marks available in the whole question.", NO),
        ({"a"}, r"For those that attempted to write $y=\sin^{-3}\theta$ and use either the chain rule or the quotient "
                r"rule success was mixed.", NO),
        ({"a"}, r"Other common incorrect derivatives included $\frac{\mathrm{d}y}{\mathrm{d}\theta}=(\mathrm{cosec}^3"
                r"\theta\cot^3\theta)$ and variants of this.", NO),
        ({"a"}, r"Differentiating $x=\sin2\theta$ proved less troublesome, with most doing so correctly."),
        ({"a"}, r"There was a proportion of candidates that rewrote $\sin2\theta$ as $2\sin\theta\cos\theta$ and used "
                r"the product rule, creating more work but ultimately doing so successfully in most cases."),
        ({"a"}, r"The method mark was scored by the majority of candidates as a result, although there were a few "
                r"candidates who tried to write $y$ in terms of $x$ and differentiate, with no marks being scored for "
                r"this approach."),
        ({"a"}, "A number of candidates, having found a correct derivative, proceeded to attempt to tidy this up, "
                "unfortunately using time that could have been spent elsewhere in the paper.", NO),
        ({"b"}, r"Part (b) proved more challenging for many candidates, with some unable to make a start as they were "
                r"unable to process $8=\mathrm{cosec}^3\theta$ to arrive at either a value for $\sin\theta$ or "
                r"$\theta$."),
        ({"b"}, r"Of those that did arrive at a value for $\sin\theta$ or $\theta$, many were able to work in exact "
                r"form using their value to find an exact value for their $" + DYDX + r"$, others were unable to "
                r"proceed or attempted to give a decimal answer.", BACK),
        ({"b"}, r"$24\sqrt{3}$ and $8\sqrt{3}$ were common incorrect final answers."),
        ({"b"}, "There were, however, some excellent and concise responses to this question."),
    ],
    "14": [
        (W, "This question proved challenging for the majority of candidates, with many not answering it at all.", NO),
        ({"a"}, "For those that did attempt a response, part (a) was reasonably well answered, with many candidates "
                "gaining at least one of the B marks but quite a few then failing to correctly apply the chain rule "
                "and complete the proof.", NO),
        ({"a"}, r"Some weaker candidates recognised they had to consider “flow in - flow out” but didn’t identify this "
                r"as $\frac{\mathrm{d}V}{\mathrm{d}t}$, with $\frac{\mathrm{d}h}{\mathrm{d}t}=0.48-0.1h$ sometimes "
                r"seen.", NO),
        ({"a"}, r"It was also not uncommon to see $\frac{\mathrm{d}V}{\mathrm{d}t}=0.48$ or $\frac{\mathrm{d}V}"
                r"{\mathrm{d}t}=0.1h$ ‘uncombined’ in some responses.", NO),
        ({"a"}, r"Some candidates even started with $24h=0.48t-0.1ht$and “differentiated” to get the printed result."),
        ({"b"}, "Responses to part (b) were mixed."),
        ({"b"}, "Some candidates failed to separate the variables correctly or did not recognise the logarithmic form "
                "for the integration."),
        ({"b"}, "It was not unusual for the “+c” to be missed completely, but if it was included candidates were able "
                "to gain the 2nd method mark despite poor integration.", NO),
        ({"b"}, r"Some candidates changed $a\ln(24-5h)$to $\ln\left[(24-5h)^a\right]$, making their following working "
                r"much harder."),
        ({"b"}, "There was some occasional use of Further Maths methods (e.g. integrating factors), potentially gaining "
                "full marks."),
        ({"b"}, "Candidates who did not answer (a) rarely attempted (b), perhaps not realising (b) could be answered "
                "independently using the printed differential equation."),
        ({"c"}, "Part (c) was attempted by many candidates, even if they hadn’t attempted (a) and (b)."),
        ({"c"}, "Students who progressed well in (b) often interpreted their formula correctly to obtain marks in (c)."),
        ({"c"}, r"A minority of students who didn’t complete (b) still attempted (c) with some success, e.g. "
                r"recognising that $\frac{\mathrm{d}h}{\mathrm{d}t}$ was zero at the maximum height or using a ‘flow "
                r"in = flow out’ argument."),
    ],
    "15": [
        (W, "This question discriminated well between candidates that got this far, but it did appear that many "
            "candidates had simply run out of time, perhaps indicative of a generally lower understanding than in a "
            "June series because of it being a resit paper following the pandemic.", NO),
        ({"a"}, r"Part (a) was answered very accurately by the vast majority of candidates, recognising the need to "
                r"use the compound angle formulae for $\cos(\theta+\alpha)$."),
        ({"a"}, r"Two common errors occurred, namely $\tan\alpha=-\frac{1}{2}$, following inaccurate equating of the "
                r"coefficients of $\cos\theta$ and $\sin\theta$, and an approximate value for $R$, which usually arose "
                r"from candidates using their value of $\alpha$ to find $R$ from either $\sin\alpha=\frac{1}{R}$ or "
                r"$\cos\alpha=\frac{2}{R}$."),
        ({"a"}, r"These candidates should be encouraged to find $R$ using Pythagoras.", BACK),
        ({"b"}, r"Part (b)(i) was usually well attempted by those who had answered part (a), however, some candidates "
                r"did not recognise the need to double $R$ and arrived at $3+R$ rather than $3+2R$ instead.", NO),
        ({"b"}, "Others simply assumed that the maximum was 3, 5 or 7, from a poor understanding of combining two "
                "trigonometric functions and the purpose of using the compound angle formulae to combine these two "
                "functions.", NO),
        ({"b"}, r"Part (b)(ii) proved to cause problems for many candidates, with the majority incorrectly assuming "
                r"that $0.5t+\alpha=0$, and proceeded to ignore that this equation results in a negative value of $t$ "
                r"(usually $-0.9$) by simply making this value of $t$ positive.", NO),
        ({"b"}, r"They had failed to recognise that the first maximum would occur when $0.5t+\alpha=2\pi$.", BACK),
        ({"b"}, "Perhaps the use of a sketch or graphical calculators would have helped these candidates.", BACK),
        ({"b"}, r"An alternative approach to part (b) required candidates to differentiate $H$, either in its original "
                r"form or having used part (a) and solve the equation $\frac{\mathrm{d}H}{\mathrm{d}t}=0$."),
        ({"b"}, r"This approach was more complicated and resulted in needing to solve $\tan(0.5t)=-\frac{1}{2}$ and "
                r"find the third solution, in order to avoid finding the maximum when $t<0$ or the first minimum.",
         BACK),
        ({"b"}, "Generally, candidates taking this approach were unsuccessful in scoring the accuracy mark, although "
                "the method mark was scored reasonably frequently.", BACK),
        ({"c"}, "Part (c) was another challenging part to this question and many candidates made no attempt."),
        ({"c"}, r"A surprising proportion of candidates attempted to solve the equation $\cos(0.5t+\alpha)=-1$, "
                r"apparently in an attempt to find the minimum, but did not appear to understand how to use this to "
                r"solve the problem.", NO),
        ({"c"}, r"It was uncommon to see this method result in a correct value for $T$.", BACK),
        ({"c"}, r"More commonly, candidates were successful in finding a value for $t$ that satisfied $H=0$, but "
                r"incorrectly interpreted this as the solution to the problem.", BACK),
        ({"c"}, r"Instead, they were required to find a second value of $t$ and find the difference between these "
                r"times.", BACK),
        ({"c"}, "Again, there were a number of efficient and concise solutions to the problem that demonstrated an "
                "excellent understanding of what was required."),
        ({"d"}, "The final mark in this question, in part (d), was rarely scored, and demonstrated that candidates are "
                "generally not well prepared to answer questions about refining models, as required in AO3.5c."),
        ({"d"}, "Many candidates did attempt this part, often despite making little or no progress with the earlier "
                "parts of the question."),
        ({"d"}, "Most concentrated on having an extra constant, wanted the average water level to be used, or simply "
                "restated the question by saying that the varying water level needed to be accounted for, without "
                "suggesting how this might be done.", NO),
        ({"d"}, "Others knew that they needed to adjust the model, but suggested exponential, linear or quadratic "
                "terms to do this, which would not have been appropriate.", NO),
        ({"d"}, "Again, there were some excellent and detailed explanations of how a trigonometric function could be "
                "included to taken into account the varying water level."),
    ],
}

RATINGS = {
    "01a": ("easy", ("01", 0)),
    "01b": ("easy", ("01", 3)),
    "02a": ("medium", ("02", 1)),
    "02b": ("easy", ("02", 4)),
    "02c": ("easy", ("02", 8)),
    "03": ("easy", ("03", 1)),
    "04": ("medium", ("04", 0)),
    "05a": ("easy", ("05", 1)),
    "05b": ("hard", ("05", 0)),
    "06a": ("easy", ("06", 1)),
    "06b": ("easy", ("06", 3)),
    "06c": ("easy", ("06", 6)),
    "07a": ("easy", ("07", 0)),
    "07b": ("medium", ("07", 4)),
    "07c": ("hard", ("07", 5)),
    "08a": ("medium", ("08", 5)),
    "08b": ("hard", ("08", 7)),
    "09": ("hard", ("09", 0)),
    "10a": ("easy", ("10", 0)),
    "10b": ("hard", ("10", 3)),
    "10c": ("hard", ("10", 8)),
    "11a": ("hard", ("11", 0)),
    "11b": ("medium", ("11", 7)),
    "11c": ("hard", ("11", 8)),
    "12a": ("medium", ("12", 1)),
    "12b": ("medium", ("12", 7)),
    "13a": ("hard", ("13", 1)),
    "13b": ("hard", ("13", 9)),
    "14a": ("hard", ("14", 0)),
    "14b": ("hard", ("14", 10)),
    "14c": ("hard", ("14", 0)),
    "15a": ("easy", ("15", 1)),
    "15b": ("hard", ("15", 6)),
    "15c": ("hard", ("15", 12)),
    "15d": ("hard", ("15", 18)),
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
