"""Draft builder for 9MA0-02 SAM (A level Pure Paper 2, sample assessment materials).

Run (from the project root, with the venv active):
    python extraction/9MA0-02_SAM.py        # writes out/drafts/9MA0-02_SAM.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-02_SAM.json

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

P, S = "9MA0-02", "SAM"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "13c"); label as printed (e.g. "13(c)")."""
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


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


DY = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
DS = r"\frac{\mathrm{d}S}{\mathrm{d}r}"

# ---------------- shared stems and parts ----------------
Q2 = ["Some A level students were given the following question.",
      r"Solve, for $-90^\circ<\theta<90^\circ$, the equation",
      r"$$\cos\theta=2\sin\theta$$",
      "The attempts of two of the students are shown below.",
      r"$$\begin{array}{|c|}\hline\underline{\text{Student }A}\\\cos\theta=2\sin\theta\\\tan\theta=2\\"
      r"\theta=63.4^\circ\\\hline\end{array}\qquad\begin{array}{|c|}\hline\underline{\text{Student }B}\\"
      r"\cos\theta=2\sin\theta\\\cos^2\theta=4\sin^2\theta\\1-\sin^2\theta=4\sin^2\theta\\"
      r"\sin^2\theta=\frac{1}{5}\\\sin\theta=\pm\frac{1}{\sqrt{5}}\\\theta=\pm26.6^\circ\\\hline\end{array}$$"]

Q4 = ["Given", r"$$\mathrm{f}(x)=\mathrm{e}^x,\quad x\in\mathbb{R}$$",
      r"$$\mathrm{g}(x)=3\ln x,\quad x>0,\ x\in\mathbb{R}$$"]
Q4A = r"find an expression for $\mathrm{gf}(x)$, simplifying your answer."

Q5 = [r"The mass, $m$ grams, of a radioactive substance, $t$ years after first being observed, is modelled by the "
      r"equation", r"$$m=25\mathrm{e}^{-0.05t}$$"]

# Q6 is a table: the header and the worked first row are shared; each part adds its own row.
Q6 = ["Complete the table below. The first one has been done for you.",
      "For each statement you must state if it is always true, sometimes true or never true, giving a reason in each "
      "case."]
Q6HEAD = (r"$$\begin{array}{|l|c|c|c|l|}\hline\text{Statement}&\text{Always True}&\text{Sometimes True}&"
          r"\text{Never True}&\text{Reason}\\\hline\begin{array}{l}\text{The quadratic equation }ax^2+bx+c=0,\quad"
          r"(a\neq0)\\\text{has 2 real roots.}\end{array}&&\checkmark&&\begin{array}{l}\text{It only has 2 real roots "
          r"when }b^2-4ac>0.\\\text{When }b^2-4ac=0\text{ it has 1 real root and when }b^2-4ac<0\text{ it has 0 real "
          r"roots.}\end{array}\\\hline")


def q6(row):
    """The Q6 table with the worked row and this part's own row."""
    return L(*Q6, Q6HEAD + row + r"&&&&\\\hline\end{array}$$")


Q7A = ["Use the binomial expansion, in ascending powers of $x$, to show that",
       r"$$\sqrt{(4-x)}=2-\frac{1}{4}x+kx^2+\ldots$$", "where $k$ is a rational constant to be found."]

FIG1 = (r"[Figure 1: axes with origin $O$ and the shaded rectangle $ABCD$, its sides sloping: $A$ on the positive "
        r"$y$-axis, $D$ on the negative $x$-axis close to $O$, $B$ on the positive $x$-axis well to the right, and $C$ "
        r"below the $x$-axis, down and slightly to the left of $B$.]")
Q8 = [FIG1, "Figure 1 shows a rectangle $ABCD$.",
      "The point $A$ lies on the $y$-axis and the points $B$ and $D$ lie on the $x$-axis as shown in Figure 1.",
      "Given that the straight line through the points $A$ and $B$ has equation $5y+2x=10$"]
Q8A = "show that the straight line through the points $A$ and $D$ has equation $2y-5x=4$"

FIG2 = (r"[Figure 2: the graph of $y=\mathrm{f}(x)$ for $x\geqslant0$: a straight line falling from a point on the "
        r"positive $y$-axis to a vertex above the $x$-axis, then a steeper straight line rising from the vertex.]")
Q11 = [FIG2, r"Figure 2 shows a sketch of part of the graph $y=\mathrm{f}(x)$, where",
       r"$$\mathrm{f}(x)=2|3-x|+5,\quad x\geqslant0$$"]

Q12A = [r"Solve, for $-180^\circ\leqslant x<180^\circ$, the equation", r"$$3\sin^2x+\sin x+8=9\cos^2x$$",
        "giving your answers to 2 decimal places."]

Q13A = [r"Express $10\cos\theta-3\sin\theta$ in the form $R\cos(\theta+\alpha)$, where $R>0$ and "
        r"$0<\alpha<90^\circ$",
        r"Give the exact value of $R$ and give the value of $\alpha$, in degrees, to 2 decimal places."]
FIG3 = (r"[Figure 3: on the left, a drawing of a Ferris wheel standing on the ground; on the right, a graph of $H$ "
        r"against $t$ on a grid: a smooth wave starting at a small height on the $H$-axis, rising to a maximum, "
        r"falling to a minimum just above the $t$-axis, rising to a second equal maximum and falling to a second "
        r"minimum, two complete cycles.]")
Q13 = [FIG3,
       "The height above the ground, $H$ metres, of a passenger on a Ferris wheel $t$ minutes after the wheel starts "
       "turning, is modelled by the equation",
       r"$$H=a-10\cos(80t)^\circ+3\sin(80t)^\circ$$", "where $a$ is a constant.",
       "Figure 3 shows the graph of $H$ against $t$ for two complete cycles of the wheel.",
       "Given that the initial height of the passenger above the ground is 1 metre,"]

Q14 = ["A company decides to manufacture a soft drinks can with a capacity of 500 ml.",
       "The company models the can in the shape of a right circular cylinder with radius $r$ cm and height $h$ cm.",
       "In the model they assume that the can is made from a metal of negligible thickness."]
Q14A = ["Prove that the total surface area, $S$ cm$^2$, of the can is given by", r"$$S=2\pi r^2+\frac{1000}{r}$$"]
Q14B = "find the dimensions of a can that has minimum surface area."

FIG4 = (r"[Figure 4: the curve $C$ starting on the positive $y$-axis, dipping to a shallow minimum and then rising "
        r"steeply; the straight line $l$ touches $C$ at the point $P$ and crosses the $x$-axis just to the right of $O$ "
        r"and the $y$-axis below $O$; the region $R$, between $C$, $l$ and the $y$-axis, is shaded, including the "
        r"small triangle below the $x$-axis.]")

Q16A = r"Express $\frac{1}{P(11-2P)}$ in partial fractions."
Q16 = ["A population of meerkats is being studied.", "The population is modelled by the differential equation",
       r"$$\frac{\mathrm{d}P}{\mathrm{d}t}=\frac{1}{22}P(11-2P),\quad t\geqslant0,\qquad0<P<5.5$$",
       "where $P$, in thousands, is the population of meerkats and $t$ is the time measured in years since the study "
       "began.",
       "Given that there were 1000 meerkats in the population when the study began,"]
Q16B = "determine the time taken, in years, for this population of meerkats to double,"

LATEX = {
    "01": L(r"$$\mathrm{f}(x)=2x^3-5x^2+ax+a$$",
            r"Given that $(x+2)$ is a factor of $\mathrm{f}(x)$, find the value of the constant $a$."),
    "02a": L(*Q2, "Identify an error made by student $A$."),
    "02b": L(*Q2, r"Student $B$ gives $\theta=-26.6^\circ$ as one of the answers to $\cos\theta=2\sin\theta$.",
             "(i) Explain why this answer is incorrect.", "(ii) Explain how this incorrect answer arose."),
    "03": L("Given $y=x(2x+1)^4$, show that", rf"$${DY}=(2x+1)^n(Ax+B)$$",
            "where $n$, $A$ and $B$ are constants to be found."),
    "04a": L(*Q4, Q4A),
    "04b": L(*Q4, "(a) " + Q4A,
             r"(b) Show that there is only one real value of $x$ for which $\mathrm{gf}(x)=\mathrm{fg}(x)$"),
    "05a": L(*Q5, "According to the model,",
             "find the mass of the radioactive substance six months after it was first observed,"),
    "05b": L(*Q5, r"Show that $\frac{\mathrm{d}m}{\mathrm{d}t}=km$, where $k$ is a constant to be found."),
    "06i": q6(r"\begin{array}{l}\text{(i)}\\\text{When a real value of }x\text{ is substituted into}\\x^2-6x+10"
              r"\text{ the result is positive.}\end{array}"),
    "06ii": q6(r"\begin{array}{l}\text{(ii)}\\\text{If }ax>b\text{ then }x>\frac{b}{a}\end{array}"),
    "06iii": q6(r"\begin{array}{l}\text{(iii)}\\\text{The difference between consecutive square numbers is odd.}"
                r"\end{array}"),
    "07a": L(*Q7A),
    "07b": L("(a) " + Q7A[0], *Q7A[1:],
             r"A student attempts to substitute $x=1$ into both sides of this equation to find an approximate value "
             r"for $\sqrt{3}$.",
             "(b) State, giving a reason, if the expansion is valid for this value of $x$."),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, "(a) " + Q8A, "(b) find the area of the rectangle $ABCD$."),
    "09": L("Given that $A$ is constant and", r"$$\int_1^4\left(3\sqrt{x}+A\right)\mathrm{d}x=2A^2$$",
            "show that there are exactly two possible values for $A$."),
    "10": L("In a geometric series the common ratio is $r$ and sum to $n$ terms is $S_n$", "Given",
            r"$$S_\infty=\frac{8}{7}\times S_6$$",
            r"show that $r=\pm\frac{1}{\sqrt{k}}$, where $k$ is an integer to be found."),
    "11a": L(*Q11, "State the range of f"),
    "11b": L(*Q11, "Solve the equation", r"$$\mathrm{f}(x)=\frac{1}{2}x+30$$"),
    "11c": L(*Q11, r"Given that the equation $\mathrm{f}(x)=k$, where $k$ is a constant, has two distinct roots,",
             "state the set of possible values for $k$."),
    "12a": L(*Q12A),
    "12b": L("(a) " + Q12A[0], *Q12A[1:], "(b) Hence find the smallest positive solution of the equation",
             r"$$3\sin^2(2\theta-30^\circ)+\sin(2\theta-30^\circ)+8=9\cos^2(2\theta-30^\circ)$$",
             "giving your answer to 2 decimal places."),
    "13a": L(*Q13A),
    "13b": L("(a) " + Q13A[0], Q13A[1], *Q13, "(b) (i) find a complete equation for the model,",
             "(ii) hence find the maximum height of the passenger above the ground."),
    "13c": L("(a) " + Q13A[0], Q13A[1], *Q13,
             "(c) Find the time taken, to the nearest second, for the passenger to reach the maximum height on the "
             "second cycle.",
             "(Solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "13d": L(*Q13, "It is decided that, to increase profits, the speed of the wheel is to be increased.",
             "How would you adapt the equation of the model to reflect this increase in speed?"),
    "14a": L(*Q14, *Q14A),
    "14b": L(*Q14, "(a) " + Q14A[0], Q14A[1], "Given that $r$ can vary,", "(b) " + Q14B),
    "14c": L(*Q14, "(a) " + Q14A[0], Q14A[1], "Given that $r$ can vary,", "(b) " + Q14B,
             "(c) With reference to the shape of the can, suggest a reason why the company may choose not to "
             "manufacture a can with minimum surface area."),
    "15": L(FIG4, "Figure 4 shows a sketch of the curve $C$ with equation",
            r"$$y=5x^{\frac{3}{2}}-9x+11,\ x\geqslant0$$", "The point $P$ with coordinates $(4, 15)$ lies on $C$.",
            "The line $l$ is the tangent to $C$ at the point $P$.",
            "The region $R$, shown shaded in Figure 4, is bounded by the curve $C$, the line $l$ and the $y$-axis.",
            "Show that the area of $R$ is 24, making your method clear.",
            "(Solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "16a": L(Q16A),
    "16b": L("(a) " + Q16A, *Q16, "(b) " + Q16B),
    "16c": L("(a) " + Q16A, *Q16, "(b) " + Q16B, "(c) show that",
             r"$$P=\frac{A}{B+C\mathrm{e}^{-\frac{1}{2}t}}$$", "where $A$, $B$ and $C$ are integers to be found."),
}

Q9ALT = "ALT: Second scheme column (discriminant)"
Q15ALT = "ALT: Alternative method for the area using area under curve and triangles (Way 2)"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", ALG, "2.6", 3, LATEX["01"],
      [r"M1 (AO 3.1a): Sets $\mathrm{f}(-2)=0\Rightarrow2\times(-2)^3-5\times(-2)^2+a\times-2+a=0$. Notes: Selects a "
       r"suitable method given that $(x+2)$ is a factor of $\mathrm{f}(x)$ Accept either setting $\mathrm{f}(-2)=0$ or "
       r"attempted division of $\mathrm{f}(x)$ by $(x+2)$",
       r"dM1 (AO 1.1b): Solves linear equation $2a-a=-36\Rightarrow a=$. Notes: Solves linear equation in $a$. Minimum "
       r"requirement is that there are two terms in ‘$a$’ which must be collected to get $..a=..\Rightarrow a=$",
       r"A1 (AO 1.1b): $\Rightarrow a=-36$. Notes: $a=-36$"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", TRIG, "5.5", 1, LATEX["02a"],
      [r"B1 (AO 2.3): Identifies an error for student A: They use $\frac{\cos\theta}{\sin\theta}=\tan\theta$ It should "
       r"be $\frac{\sin\theta}{\cos\theta}=\tan\theta$. Notes: Accept a response of the type ‘They use "
       r"$\frac{\cos\theta}{\sin\theta}=\tan\theta$. This is incorrect as $\frac{\sin\theta}{\cos\theta}=\tan\theta$’ "
       r"It can be implied by a response such as ‘They should get $\tan\theta=\frac{1}{2}$ not $\tan\theta=2$’ Accept "
       r"also statements such as ‘it should be $\cot\theta=2$’"],
      False, 3),
    e("02b", "2(b)", TRIG, "5.7, 5.5", 2, LATEX["02b"],
      [r"B1 (AO 2.4): (i) Shows $\cos(-26.6^\circ)\neq2\sin(-26.6^\circ)$, so cannot be a solution. Notes: Accept a "
       r"response where the candidate shows that $-26.6^\circ$ is not a solution of $\cos\theta=2\sin\theta$. This can "
       r"be shown by, for example, finding both $\cos(-26.6^\circ)$ and $2\sin(-26.6^\circ)$ and stating that they are "
       r"not equal. An acceptable alternative is to state that $\cos(-26.6^\circ)=+ve$ and $2\sin(-26.6^\circ)=-ve$ "
       r"and stating that they therefore cannot be equal.",
       r"B1 (AO 2.4): (ii) Explains that the incorrect answer was introduced by squaring. Notes: Explains that the "
       r"incorrect answer was introduced by squaring Accept an example showing this. For example $x=5$ squared gives "
       r"$x^2=25$ which has answers $\pm5$"],
      False, 3),

    # ---------------- Q3 ----------------
    e("03", "3", DIFF, "7.4", 4, LATEX["03"],
      [r"M1 (AO 2.1): Attempts the product and chain rule on $y=x(2x+1)^4$. Notes: Applies the product rule to reach "
       rf"${DY}=(2x+1)^4+Bx(2x+1)^3$",
       rf"A1 (AO 1.1b): ${DY}=(2x+1)^4+8x(2x+1)^3$. Notes: ${DY}=(2x+1)^4+8x(2x+1)^3$",
       rf"M1 (AO 1.1b): Takes out a common factor ${DY}=(2x+1)^3\left\{{(2x+1)+8x\right\}}$. Notes: Takes out a "
       r"common factor of $(2x+1)^3$",
       rf"A1 (AO 1.1b): ${DY}=(2x+1)^3(10x+1)\Rightarrow n=3,A=10,B=1$. Notes: The form of this answer is given. Look "
       rf"for ${DY}=(2x+1)^3(10x+1)\Rightarrow n=3,A=10,B=1$"],
      False, 4),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", ALG, "2.8, 6.3", 2, LATEX["04a"],
      [r"M1 (AO 1.1b): $\mathrm{gf}(x)=3\ln\mathrm{e}^x$. Notes: For applying the functions in the correct order",
       r"A1 (AO 1.1b): $=3x,\ (x\in\mathbb{R})$. Notes: The simplest form is required so it must be $3x$ and not left "
       r"in the form $3\ln\mathrm{e}^x$ An answer of $3x$ with no working would score both marks"],
      False, 5),
    e("04b", "4(b)", ALG, "2.8, 6.3", 3, LATEX["04b"],
      [r"M1 (AO 1.1b): $\mathrm{gf}(x)=\mathrm{fg}(x)\Rightarrow3x=x^3$. Notes: Allow the candidates to score this mark "
       r"if they have $\mathrm{e}^{3\ln x}=$ their $3x$",
       r"M1 (AO 1.1b): $\Rightarrow x^3-3x=0\Rightarrow x=$. Notes: For solving their cubic in $x$ and obtaining at "
       r"least one solution.",
       r"M1 (AO 2.2a): $\Rightarrow x=(+)\sqrt{3}$ only as $\ln x$ is not defined at $x=0$ and $-\sqrt{3}$. Notes: [the "
       r"notes label this mark A1] For either stating that $x=\sqrt{3}$ $\textbf{only}$ as $\ln x$ (or $3\ln x$) is "
       r"not defined at $x=0$ and $-\sqrt{3}$ or stating that $3x=x^3$ would have three answers, one positive one "
       r"negative and one zero but $\ln x$ (or $3\ln x$) is not defined for $x\leqslant0$ so therefore there is only "
       r"one (real) answer. Note: Student who mix up fg and gf can score full marks in part (b) as they have already "
       r"been penalised in part (a)"],
      False, 5),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", EXP, "6.7", 2, LATEX["05a"],
      [r"M1 (AO 3.4): Substitutes $t=0.5$ into $m=25\mathrm{e}^{-0.05t}\Rightarrow m=25\mathrm{e}^{-0.05\times0.5}$. "
       r"Notes: Substitutes $t=0.5$ into $m=25\mathrm{e}^{-0.05t}\Rightarrow m=25\mathrm{e}^{-0.05\times0.5}$",
       r"A1 (AO 1.1b): $\Rightarrow m=24.4$g. Notes: $m=24.4$g An answer of $m=24.4$g with no working would score both "
       r"marks"],
      False, 6),
    e("05b", "5(b)", EXP, "6.2, 6.7", 2, LATEX["05b"],
      [r"M1 (AO 2.1): States or uses $\frac{\mathrm{d}}{\mathrm{d}t}\left(\mathrm{e}^{-0.05t}\right)=\pm C"
       r"\mathrm{e}^{-0.05t}$. Notes: Applies the rule $\frac{\mathrm{d}}{\mathrm{d}t}\left(\mathrm{e}^{kx}\right)="
       r"k\mathrm{e}^{kx}$ in this context by stating or using $\frac{\mathrm{d}}{\mathrm{d}t}\left(\mathrm{e}^{-0.05t}"
       r"\right)=\pm C\mathrm{e}^{-0.05t}$",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}m}{\mathrm{d}t}=-0.05\times25\mathrm{e}^{-0.05t}=-0.05m\Rightarrow k=-0.05$. "
       r"Notes: $\frac{\mathrm{d}m}{\mathrm{d}t}=-0.05\times25\mathrm{e}^{-0.05t}=-0.05m\Rightarrow k=-0.05$"],
      False, 6),

    # ---------------- Q6 ----------------
    e("06i", "6(i)", ALG, "2.3, 1.1", 2, LATEX["06i"],
      [r"M1 (AO 2.1): $x^2-6x+10=(x-3)^2+1$. Notes: Attempts to complete the square or any other valid reason. Allow "
       r"for a graph of $y=x^2-6x+10$ or an attempt to find the minimum by differentiation",
       r"A1 (AO 2.2a): Deduces “always true” as $(x-3)^2\geqslant0\Rightarrow(x-3)^2+1\geqslant1$ and so is always "
       r"positive. Notes: States always true with a valid reason for their method"],
      False, 7),
    e("06ii", "6(ii)", PROOF, "1.1, 2.5", 2, LATEX["06ii"],
      [r"M1 (AO 2.3): For an explanation that it need not (always) be true This could be if $a<0$ then "
       r"$ax>b\Rightarrow x<\frac{b}{a}$. Notes: For an explanation that it need not be true (sometimes). This could be "
       r"if $a<0$ then $ax>b\Rightarrow x<\frac{b}{a}$ or simply $-3x>6\Rightarrow x<-2$",
       r"A1 (AO 2.4): States ‘sometimes’ and explains if $a>0$ then $ax>b\Rightarrow x>\frac{b}{a}$ if $a<0$ then "
       r"$ax>b\Rightarrow x<\frac{b}{a}$. Notes: Correct statement (sometimes true) and explanation"],
      False, 7),
    e("06iii", "6(iii)", PROOF, "1.1", 2, LATEX["06iii"],
      [r"M1 (AO 3.1a): Difference $=(n+1)^2-n^2=2n+1$. Notes: Sets up the proof algebraically. For example by "
       r"attempting $(n+1)^2-n^2=2n+1$ or $m^2-n^2=(m-n)(m+n)$ with $m=n+1$",
       r"A1 (AO 2.2a): Deduces “Always true” as $2n+1=$ (even $+1$) $=$ odd. Notes: States always true with reason and "
       r"proof Accept a proof written in words. For example If integers are consecutive, one is odd and one is even "
       r"When squared $\text{odd}\times\text{odd}=\text{odd}$ and $\text{even}\times\text{even}=\text{even}$ The "
       r"difference between odd and even is always odd, hence always true Score M1 for two of these lines and A1 for a "
       r"good proof with all three lines or equivalent."],
      False, 7),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", SEQ, "4.1", 4, LATEX["07a"],
      [r"M1 (AO 2.1): $\sqrt{(4-x)}=2\left(1-\frac{1}{4}x\right)^{\frac{1}{2}}$. Notes: Takes out a factor of 4 and "
       r"writes $\sqrt{(4-x)}=2(1\pm\ldots)^{\frac{1}{2}}$",
       r"M1 (AO 1.1b): $\left(1-\frac{1}{4}x\right)^{\frac{1}{2}}=1+\frac{1}{2}\left(-\frac{1}{4}x\right)+"
       r"\frac{\left(\frac{1}{2}\right)\left(-\frac{1}{2}\right)}{2!}\left(-\frac{1}{4}x\right)^2+\ldots$. Notes: For an "
       r"attempt at the binomial expansion with $n=\frac{1}{2}$ Eg. $(1+ax)^{\frac{1}{2}}=1+\frac{1}{2}(ax)+"
       r"\frac{\left(\frac{1}{2}\right)\left(-\frac{1}{2}\right)}{2!}(ax)^2+\ldots$",
       r"A1 (AO 1.1b): $\sqrt{(4-x)}=2\left(1-\frac{1}{8}x-\frac{1}{128}x^2+..\right)$. Notes: Correct expression "
       r"inside the bracket $1-\frac{1}{8}x-\frac{1}{128}x^2+$ which may be left unsimplified",
       r"A1 (AO 1.1b): $\sqrt{(4-x)}=2-\frac{1}{4}x-\frac{1}{64}x^2+\ldots$ and $k=-\frac{1}{64}$. Notes: "
       r"$\sqrt{(4-x)}=2-\frac{1}{4}x-\frac{1}{64}x^2+\ldots$ and $k=-\frac{1}{64}$"],
      False, 8),
    e("07b", "7(b)", SEQ, "4.1", 1, LATEX["07b"],
      [r"B1 (AO 2.4): The expansion is valid for $|x|<4$, so $x=1$ can be used. Notes: The expansion is valid for "
       r"$|x|<4$, so $x=1$ can be used"],
      False, 8),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", COORD, "3.1", 4, LATEX["08a"],
      [r"B1 (AO 2.1): Gradient $AB=-\frac{2}{5}$. Notes: (a) It is important that the student communicates each of "
       r"these steps clearly States the gradient of $AB$ is $-\frac{2}{5}$",
       r"B1 (AO 2.1): $y$ coordinate of $A$ is 2. Notes: States that $y$ coordinate of $A=2$",
       r"M1 (AO 2.2a): Uses perpendicular gradients $y=+\frac{5}{2}x+c$. Notes: Uses the form $y=mx+c$ with $m=$ their "
       r"adapted $-\frac{2}{5}$ and $c=$ their 2 Alternatively uses the form $y-y_1=m(x-x_1)$ with $m=$ their adapted "
       r"$-\frac{2}{5}$ and $(x_1,y_1)=(0,2)$",
       r"A1* (AO 1.1b): $\Rightarrow2y-5x=4$ *. Notes: Proceeds to given answer"],
      True, 10),
    e("08b", "8(b)", COORD, "3.1", 3, LATEX["08b"],
      [r"M1 (AO 3.1a): Uses Pythagoras' theorem to find $AB$ or $AD$ Either $\sqrt{5^2+2^2}$ or "
       r"$\sqrt{\left(\frac{4}{5}\right)^2+2^2}$. Notes: Finds the lengths of $AB$ or $AD$ using Pythagoras' Theorem. "
       r"Look for $\sqrt{5^2+2^2}$ or $\sqrt{\left(\frac{4}{5}\right)^2+2^2}$ Alternatively finds the lengths $BD$ and "
       r"$AO$ using coordinates. Look for $\left(5+\frac{4}{5}\right)$ and 2",
       r"M1 (AO 1.1b): Uses area $ABCD=AD\times AB=\sqrt{29}\times\sqrt{\frac{116}{25}}$. Notes: For a full method of "
       r"finding the area of the rectangle $ABCD$. Allow for $AD\times AB$ Alternatively attempts area $ABCD="
       r"2\times\frac{1}{2}BD\times AO=2\times\frac{1}{2}\text{‘}5.8\text{’}\times\text{‘}2\text{’}$",
       r"A1 (AO 1.1b): area $ABCD=11.6$. Notes: Area $ABCD=11.6$ or other exact equivalent such as $\frac{58}{5}$"],
      True, 10),

    # ---------------- Q9 ----------------
    e("09", "9", INT, "8.3, 8.2, 2.3", 5, LATEX["09"],
      [r"M1 (AO 3.1a): $\int\left(3x^{0.5}+A\right)\mathrm{d}x=2x^{1.5}+Ax(+c)$. Notes: Integrates the given function "
       r"and achieves an answer of the form $kx^{1.5}+Ax(+c)$ where $k$ is a non- zero constant",
       r"A1 (AO 1.1b): $\int\left(3x^{0.5}+A\right)\mathrm{d}x=2x^{1.5}+Ax(+c)$. Notes: Correct answer but may not be "
       r"simplified",
       r"M1 (AO 1.1b): Uses limits and sets $=2A^2\Rightarrow(2\times8+4A)-(2\times1+A)=2A^2$. Notes: Substitutes in "
       r"limits and subtracts. This can only be scored if $\int A\,\mathrm{d}x=Ax$ and not $\frac{A^2}{2}$",
       r"M1 (AO 1.1b): Sets up quadratic and attempts to solve. Notes: Sets up quadratic equation in $A$ and either "
       r"attempts to solve or attempts $b^2-4ac$",
       r"A1 (AO 2.4): $\Rightarrow A=-2,\frac{7}{2}$ $\textbf{and}$ states that there are two roots. Notes: Either "
       r"$A=-2,\frac{7}{2}$ $\textbf{and}$ states that there are two roots Or states $b^2-4ac=121>0$ and hence there "
       r"are two roots",
       rf"{Q9ALT} — M1 (AO 1.1b): Sets up quadratic and attempts $b^2-4ac$",
       rf"{Q9ALT} — A1 (AO 2.4): States $b^2-4ac=121>0$ and hence there are two roots"],
      False, 12),

    # ---------------- Q10 ----------------
    e("10", "10", SEQ, "4.5", 4, LATEX["10"],
      [r"M1 (AO 2.1): Attempts $S_\infty=\frac{8}{7}\times S_6\Rightarrow\frac{a}{1-r}=\frac{8}{7}\times"
       r"\frac{a(1-r^6)}{1-r}$. Notes: Substitutes the correct formulae for $S_\infty$ and $S_6$ into the given "
       r"equation $S_\infty=\frac{8}{7}\times S_6$",
       r"M1 (AO 2.1): $\Rightarrow1=\frac{8}{7}\times(1-r^6)$. Notes: Proceeds to an equation just in $r$",
       r"M1 (AO 1.1b): $\Rightarrow r^6=\frac{1}{8}\Rightarrow r=..$. Notes: Solves using a correct method",
       r"A1 (AO 1.1b): $\Rightarrow r=\pm\frac{1}{\sqrt{2}}$ (so $k=2$). Notes: Proceeds to "
       r"$r=\pm\frac{1}{\sqrt{2}}$ giving $k=2$"],
      False, 13),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", ALG, "2.7, 2.8", 1, LATEX["11a"],
      [r"B1 (AO 1.1b): $\mathrm{f}(x)\geqslant5$. Notes: $\mathrm{f}(x)\geqslant5$ Also allow "
       r"$\mathrm{f}(x)\in[5,\infty)$"],
      True, 14),
    e("11b", "11(b)", ALG, "2.7", 3, LATEX["11b"],
      [r"M1 (AO 3.1a): Uses $-2(3-x)+5=\frac{1}{2}x+30$. Notes: Deduces that the solution to "
       r"$\mathrm{f}(x)=\frac{1}{2}x+30$ can be found by solving $-2(3-x)+5=\frac{1}{2}x+30$",
       r"M1 (AO 1.1b): Attempts to solve by multiplying out bracket, collect terms etc $\frac{3}{2}x=31$. Notes: "
       r"Correct method used to solve their equation. Multiplies out bracket/ collects like terms",
       r"A1 (AO 1.1b): $x=\frac{62}{3}$ only. Notes: $x=\frac{62}{3}$ only. Do not allow 20.6"],
      True, 14),
    e("11c", "11(c)", ALG, "2.7, 2.5", 2, LATEX["11c"],
      [r"M1 (AO 2.2a): Makes the connection that there must be two intersections. Implied by either end point $k>5$ "
       r"or $k\leqslant11$. Notes: Deduces that two distinct roots occurs when $y=k$ intersects $y=\mathrm{f}(x)$ in "
       r"two places. This may be implied by the sight of either end point. Score for sight of either $k>5$ or "
       r"$k\leqslant11$",
       r"A1 (AO 2.5): $\{k:k\in\mathbb{R},5<k\leqslant11\}$. Notes: Correct solution only "
       r"$\{k:k\in\mathbb{R},5<k\leqslant11\}$"],
      True, 14),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", TRIG, "5.7, 5.5", 6, LATEX["12a"],
      [r"M1 (AO 3.1a): Uses $\cos^2x=1-\sin^2x\Rightarrow3\sin^2x+\sin x+8=9\left(1-\sin^2x\right)$. Notes: "
       r"Substitutes $\cos^2x=1-\sin^2x$ into $3\sin^2x+\sin x+8=9\cos^2x$ to create a quadratic equation in just "
       r"$\sin x$",
       r"A1 (AO 1.1b): $\Rightarrow12\sin^2x+\sin x-1=0$. Notes: $12\sin^2x+\sin x-1=0$ or exact equivalent",
       r"M1 (AO 1.1b): $\Rightarrow(4\sin x-1)(3\sin x+1)=0$. Notes: Attempts to solve their quadratic equation in "
       r"$\sin x$ by a suitable method. These could include factorisation, formula or completing the square.",
       r"A1 (AO 1.1b): $\Rightarrow\sin x=\frac{1}{4},-\frac{1}{3}$. Notes: $\sin x=\frac{1}{4},-\frac{1}{3}$",
       r"M1 (AO 1.1b): Uses arcsin to obtain two correct values. Notes: Obtains two correct values for their "
       r"$\sin x=k$",
       r"A1 (AO 1.1b): All four of $x=14.48^\circ,165.52^\circ,-19.47^\circ,-160.53^\circ$. Notes: All four of "
       r"$x=14.48^\circ,165.52^\circ,-19.47^\circ,-160.53^\circ$"],
      False, 16),
    e("12b", "12(b)", TRIG, "5.7", 2, LATEX["12b"],
      [r"M1 (AO 3.1a): Attempts $2\theta-30^\circ=-19.47^\circ$. Notes: For setting $2\theta-30^\circ=$ their "
       r"$\text{‘}-19.47^\circ\text{’}$",
       r"A1ft (AO 1.1b): $\Rightarrow\theta=5.26^\circ$. Notes: $\theta=5.26^\circ$ but allow a follow through on their "
       r"$\text{‘}-19.47^\circ\text{’}$"],
      False, 16),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", TRIG, "5.6", 3, LATEX["13a"],
      [r"B1 (AO 1.1b): $R=\sqrt{109}$. Notes: $R=\sqrt{109}$ Do not allow decimal equivalents",
       r"M1 (AO 1.1b): $\tan\alpha=\frac{3}{10}$. Notes: Allow for $\tan\alpha=\pm\frac{3}{10}$",
       r"A1 (AO 1.1b): $\alpha=16.70^\circ$ so $\sqrt{109}\cos(\theta+16.70^\circ)$. Notes: $\alpha=16.70^\circ$"],
      False, 18),
    e("13b", "13(b)", TRIG, "5.9, 5.6", 2, LATEX["13b"],
      [r"B1 (AO 3.3): (i) e.g $H=11-10\cos(80t)^\circ+3\sin(80t)^\circ$ or $H=11-\sqrt{109}\cos(80t+16.70)^\circ$. "
       r"Notes: see scheme",
       r"B1ft (AO 3.4): (ii) $11+\sqrt{109}$ or 21.44 m. Notes: their $11+$ their $\sqrt{109}$ Allow decimals here."],
      True, 18),
    e("13c", "13(c)", TRIG, "5.9", 3, LATEX["13c"],
      [r"M1 (AO 3.4): Sets $80t+\text{“}16.70\text{”}=540$. Notes: Sets $80t+\text{“}16.70\text{”}=540$. Follow "
       r"through on their 16.70",
       r"M1 (AO 1.1b): $t=\frac{540-\text{“}16.70\text{”}}{80}=(6.54)$. Notes: Solves their "
       r"$80t+\text{“}16.70\text{”}=540$ correctly to find $t$",
       r"A1 (AO 1.1b): $t=6$ mins 32 seconds. Notes: $t=6$ mins 32 seconds"],
      True, 18),
    e("13d", "13(d)", TRIG, "5.9", 1, LATEX["13d"],
      [r"B1 (AO 3.3): Increase the ‘80’ in the formula For example use $H=11-10\cos(90t)^\circ+3\sin(90t)^\circ$ [the "
       r"Marks column is blank for this row; the code is from the notes]. Notes: States that to increase the speed of "
       r"the wheel the 80’s in the equation would need to be increased."],
      True, 18),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", ALG, "2.11", 3, LATEX["14a"],
      [r"B1 (AO 2.1): Sets $500=\pi r^2h$. Notes: Uses the correct volume formula with $V=500$. Accept "
       r"$500=\pi r^2h$",
       r"M1 (AO 2.1): Substitute $h=\frac{500}{\pi r^2}$ into $S=2\pi r^2+2\pi rh=2\pi r^2+2\pi r\times"
       r"\frac{500}{\pi r^2}$. Notes: Substitutes $h=\frac{500}{\pi r^2}$ or $rh=\frac{500}{\pi r}$ into "
       r"$S=2\pi r^2+2\pi rh$ to get $S$ as a function of $r$",
       r"A1* (AO 1.1b): Simplifies to reach given answer $S=2\pi r^2+\frac{1000}{r}$ *. Notes: "
       r"$S=2\pi r^2+\frac{1000}{r}$ Note that this is a given answer."],
      False, 20),
    e("14b", "14(b)", DIFF, "7.3", 5, LATEX["14b"],
      [rf"M1 (AO 3.4): Differentiates $S$ with both indices correct in ${DS}$. Notes: Differentiates the given $S$ to "
       rf"reach ${DS}=Ar\pm Br^{{-2}}$",
       rf"A1 (AO 1.1b): ${DS}=4\pi r-\frac{{1000}}{{r^2}}$. Notes: ${DS}=4\pi r-\frac{{1000}}{{r^2}}$ or exact "
       r"equivalent",
       rf"M1 (AO 2.1): Sets ${DS}=0$ and proceeds to $r^3=k$, $k$ is a constant. Notes: Sets ${DS}=0$ and proceeds "
       r"to $r^3=k$, $k$ is a constant",
       r"A1 (AO 1.1b): Radius $=4.30$cm. Notes: $R=$ awrt 4.30cm",
       r"A1 (AO 1.1b): Substitutes their $r=4.30$ into $h=\frac{500}{\pi r^2}\Rightarrow$ Height $=8.60$cm. Notes: "
       r"$H=$ awrt 8.60 cm"],
      False, 20),
    e("14c", "14(c)", ALG, "2.11", 1, LATEX["14c"],
      [r"B1 (AO 3.2a): States a valid reason such as • The radius is too big for the size of our hands • If $r=4.3$cm "
       r"and $h=8.6$cm the can is square in profile. All drinks cans are taller than they are wide • The radius is too "
       r"big for us to drink from • They have different dimensions to other drinks cans and would be difficult to "
       r"stack on shelves with other drinks cans. Notes: Any valid reason. See scheme for alternatives"],
      False, 20),

    # ---------------- Q15 ----------------
    e("15", "15", INT, "8.3, 7.3, 8.2", 10, LATEX["15"],
      [rf"M1 (AO 3.1a): ${DY}=\frac{{15}}{{2}}x^{{\frac{{1}}{{2}}}}-9$. Notes: Differentiates "
       r"$5x^{\frac{3}{2}}-9x+11$ to a form $Ax^{\frac{1}{2}}+B$",
       rf"A1 (AO 1.1b): ${DY}=\frac{{15}}{{2}}x^{{\frac{{1}}{{2}}}}-9$. Notes: ${DY}=\frac{{15}}{{2}}"
       r"x^{\frac{1}{2}}-9$ but may not be simplified",
       rf"M1 (AO 2.1): Substitutes $x=4\Rightarrow{DY}=6$. Notes: Substitutes $x=4$ in their ${DY}$ to find the "
       r"gradient of the tangent",
       r"M1 (AO 2.1): Uses $(4, 15)$ and gradient $\Rightarrow y-15=6(x-4)$. Notes: Uses their gradient and the point "
       r"$(4, 15)$ to find the equation of the tangent",
       r"A1 (AO 1.1b): Equation of $l$ is $y=6x-9$. Notes: Equation of $l$ is $y=6x-9$",
       r"M1 (AO 3.1a): Area $R=\int_0^4\left(5x^{\frac{3}{2}}-9x+11\right)-(6x-9)\,\mathrm{d}x$. Notes: Uses Area "
       r"$R=\int_0^4\left(5x^{\frac{3}{2}}-9x+11\right)-(6x-9)\,\mathrm{d}x$ following through on their $y=6x-9$ Look "
       r"for a form $Ax^{\frac{5}{2}}+Bx^2+Cx$",
       r"A1 (AO 1.1b): $=\left[2x^{\frac{5}{2}}-\frac{15}{2}x^2+20x(+c)\right]_0^4$. Notes: "
       r"$=\left[2x^{\frac{5}{2}}-\frac{15}{2}x^2+20x(+c)\right]_0^4$ This must be correct but may not be simplified",
       r"M1 (AO 2.1): Uses both limits of 4 and 0 $\left[2x^{\frac{5}{2}}-\frac{15}{2}x^2+20x\right]_0^4="
       r"2\times4^{\frac{5}{2}}-\frac{15}{2}\times4^2+20\times4-0$. Notes: Substitutes in both limits and subtracts",
       r"A1* (AO 1.1b): Area of $R=24$ *. Notes: Correct area for $R=24$",
       r"A1 (AO 2.5): Correct notation with good explanations. Notes: Uses correct notation and produces a well "
       r"explained and accurate solution. Look for • Correct notation used consistently and accurately for both "
       r"differentiation and integration • Correct explanations in producing the equation of $l$. See scheme. • "
       r"Correct explanation in finding the area of $R$. In way 2 a diagram may be used.",
       rf"{Q15ALT} — M1: Area under curve $=\int_0^4\left(5x^{{\frac{{3}}{{2}}}}-9x+11\right)=\left[Ax^{{\frac{{5}}"
       r"{2}}+Bx^2+Cx\right]_0^4$",
       rf"{Q15ALT} — A1: $=\left[2x^{{\frac{{5}}{{2}}}}-\frac{{9}}{{2}}x^2+11x\right]_0^4=36$",
       rf"{Q15ALT} — M1: This requires a full method with all triangles found using a correct method Look for Area "
       r"$R=$ their $36-\frac{1}{2}\times15\times\left(4-\text{their }\frac{3}{2}\right)+\frac{1}{2}\times\text{their }"
       r"9\times\text{their }\frac{3}{2}$"],
      True, 22),

    # ---------------- Q16 ----------------
    e("16a", "16(a)", ALG, "2.10", 3, LATEX["16a"],
      [r"B1 (AO 1.1a): Sets $\frac{1}{P(11-2P)}=\frac{A}{P}+\frac{B}{(11-2P)}$. Notes: Sets "
       r"$\frac{1}{P(11-2P)}=\frac{A}{P}+\frac{B}{(11-2P)}$",
       r"M1 (AO 1.1b): Substitutes either $P=0$ or $P=\frac{11}{2}$ into $1=A(11-2P)+BP\Rightarrow A$ or $B$. Notes: "
       r"Substitutes $P=0$ or $P=\frac{11}{2}$ into $1=A(11-2P)+BP\Rightarrow A$ or $B$ Alternatively compares terms to "
       r"set up and solve two simultaneous equations in $A$ and $B$",
       r"A1 (AO 1.1b): $\frac{1}{P(11-2P)}=\frac{\frac{1}{11}}{P}+\frac{\frac{2}{11}}{(11-2P)}$. Notes: "
       r"$\frac{1}{P(11-2P)}=\frac{\frac{1}{11}}{P}+\frac{\frac{2}{11}}{(11-2P)}$ or equivalent "
       r"$\frac{1}{P(11-2P)}=\frac{1}{11P}+\frac{2}{11(11-2P)}$ Note: The correct answer with no working scores all "
       r"three marks."],
      False, 24),
    e("16b", "16(b)", INT, "8.7, 8.6, 8.8", 6, LATEX["16b"],
      [r"B1 (AO 3.1a): Separates the variables $\int\frac{22}{P(11-2P)}\,\mathrm{d}P=\int1\,\mathrm{d}t$. Notes: "
       r"Separates the variables to reach $\int\frac{22}{P(11-2P)}\,\mathrm{d}P=\int1\,\mathrm{d}t$ or equivalent",
       r"M1 (AO 1.1b): Uses (a) and attempts to integrate $\int\frac{2}{P}+\frac{4}{(11-2P)}\,\mathrm{d}P=t+c$. Notes: "
       r"Uses part (a) and $\int\frac{A}{P}+\frac{B}{(11-2P)}\,\mathrm{d}P=A\ln P\pm C\ln(11-2P)$",
       r"A1 (AO 1.1b): $2\ln P-2\ln(11-2P)=t+c$. Notes: Integrates both sides to form a correct equation including a "
       r"‘$c$’ Eg $2\ln P-2\ln(11-2P)=t+c$",
       r"M1 (AO 3.1a): Substitutes $t=0,P=1\Rightarrow t=0,P=1\Rightarrow c=(-2\ln9)$. Notes: Substitutes $t=0$ and "
       r"$P=1$ to find $c$",
       r"M1 (AO 3.1a): Substitutes $P=2\Rightarrow t=2\ln2+2\ln9-2\ln7$. Notes: Substitutes $P=2$ to find $t$. This is "
       r"dependent upon having scored both previous M's",
       r"A1 (AO 3.2a): Time $=1.89$ years. Notes: Time $=1.89$ years"],
      False, 24),
    e("16c", "16(c)", INT, "8.7, 6.4", 3, LATEX["16c"],
      [r"M1 (AO 2.1): Uses ln laws $2\ln P-2\ln(11-2P)=t-2\ln9\Rightarrow\ln\left(\frac{9P}{11-2P}\right)="
       r"\frac{1}{2}t$. Notes: Uses correct log laws to move from $2\ln P-2\ln(11-2P)=t+c$ to "
       r"$\ln\left(\frac{P}{11-2P}\right)=\frac{1}{2}t+d$ for their numerical ‘$c$’",
       r"M1 (AO 2.1): Makes ‘$P$’ the subject $\Rightarrow\left(\frac{9P}{11-2P}\right)=\mathrm{e}^{\frac{1}{2}t}"
       r"\Rightarrow9P=(11-2P)\mathrm{e}^{\frac{1}{2}t}\Rightarrow P=\mathrm{f}\left(\mathrm{e}^{\frac{1}{2}t}\right)$ or "
       r"$\Rightarrow P=\mathrm{f}\left(\mathrm{e}^{-\frac{1}{2}t}\right)$. Notes: Uses a correct method to get $P$ in "
       r"terms of $\mathrm{e}^{\frac{1}{2}t}$ This can be achieved from $\ln\left(\frac{P}{11-2P}\right)=\frac{1}{2}t+d"
       r"\Rightarrow\frac{P}{11-2P}=\mathrm{e}^{\frac{1}{2}t+d}$ followed by cross multiplication and collection of "
       r"terms in $P$ (See scheme) Alternatively uses a correct method to get $P$ in terms of "
       r"$\mathrm{e}^{-\frac{1}{2}t}$ For example $\frac{P}{11-2P}=\mathrm{e}^{\frac{1}{2}t+d}\Rightarrow"
       r"\frac{11-2P}{P}=\mathrm{e}^{-\left(\frac{1}{2}t+d\right)}\Rightarrow\frac{11}{P}-2=\mathrm{e}^{-\left("
       r"\frac{1}{2}t+d\right)}\Rightarrow\frac{11}{P}=2+\mathrm{e}^{-\left(\frac{1}{2}t+d\right)}$ followed by division",
       r"A1 (AO 1.1b): $\Rightarrow P=\frac{11}{2+9\mathrm{e}^{-\frac{1}{2}t}}\Rightarrow A=11,B=2,C=9$. Notes: Achieves "
       r"the correct answer in the form required. $P=\frac{11}{2+9\mathrm{e}^{-\frac{1}{2}t}}\Rightarrow A=11,B=2,C=9$ "
       r"oe"],
      False, 24),
]

# No examiner report is published for the SAM, so there is nothing to apply.
W = None
REPORT = {}

# No report, so no difficulty can be judged: every part is (None, None).
RATINGS = {q: (None, None) for q in
           ["01", "02a", "02b", "03", "04a", "04b", "05a", "05b", "06i", "06ii", "06iii", "07a", "07b", "08a", "08b",
            "09", "10", "11a", "11b", "11c", "12a", "12b", "13a", "13b", "13c", "13d", "14a", "14b", "14c", "15",
            "16a", "16b", "16c"]}


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
