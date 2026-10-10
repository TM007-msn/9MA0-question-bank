"""Draft builder for 9MA0-01 SPEC (A level Pure Paper 1, specimen paper).

Run (from the project root, with the venv active):
    python extraction/9MA0-01_SPEC.py        # writes out/drafts/9MA0-01_SPEC.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-01_SPEC.json

Everything here is transcribed from the source PDFs, read as page images
(figures at 200 dpi). There is no examiner report for the specimen paper, so
examiner_notes, difficulty and difficulty_evidence are all null.
Follow CLAUDE.md for every field.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report, part_key  # noqa: E402
from mark_codes import main_marks  # noqa: E402
from paths import ensure_out_dir  # noqa: E402

P, S = "9MA0-01", "SPEC"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "13e"); label as printed (e.g. "13(e)")."""
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
NUM = "Numerical methods"
VEC = "Vectors"


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


DY = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
I, J, K = r"\mathbf{i}", r"\mathbf{j}", r"\mathbf{k}"

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q1 = [r"[Figure 1: the curve $y=\frac{x}{1+\sqrt{x}}$ rising from $O$ and flattening slightly as $x$ increases; the "
      r"region $R$ under the curve between $x=1$ and $x=3$ is shaded.]",
      r"Figure 1 shows a sketch of the curve with equation $y=\frac{x}{1+\sqrt{x}},\quad x\geqslant0$",
      "The finite region $R$, shown shaded in Figure 1, is bounded by the curve, the line with equation $x=1$, the "
      "$x$-axis and the line with equation $x=3$",
      r"The table below shows corresponding values of $x$ and $y$ for $y=\frac{x}{1+\sqrt{x}}$",
      r"$$\begin{array}{|c|c|c|c|c|c|}\hline x&1&1.5&2&2.5&3\\\hline y&0.5&0.6742&0.8284&0.9686&1.0981\\"
      r"\hline\end{array}$$"]
Q1A = ("Use the trapezium rule, with all the values of $y$ in the table, to find an estimate for the area of $R$, "
       "giving your answer to 3 decimal places.")
Q2A = ["Show that the binomial expansion of", r"$$(4+5x)^{\frac{1}{2}}$$",
       "in ascending powers of $x$, up to and including the term in $x^2$ is", r"$$2+\frac{5}{4}x+kx^2$$",
       "giving the value of the constant $k$ as a simplified fraction."]
Q3 = [r"A sequence of numbers $a_1,a_2,a_3,\ldots$ is defined by", "$$a_1=3$$",
      r"$$a_{n+1}=\frac{a_n-3}{a_n-2},\qquad n\in\mathbb{N}$$"]
Q3A = r"Find $\displaystyle\sum_{r=1}^{100}a_r$"
Q4 = ["Relative to a fixed origin $O$,", rf"the point $A$ has position vector ${I}+7{J}-2{K}$,",
      rf"the point $B$ has position vector $4{I}+3{J}+3{K}$,",
      rf"and the point $C$ has position vector $2{I}+10{J}+9{K}$."]
Q5 = [r"$$\mathrm{f}(x)=x^3+ax^2-ax+48,\quad\text{where }a\text{ is a constant}$$"]
Q5G = r"Given that $2\log_2(x+2)+\log_2x-\log_2(x-6)=3$"
Q5B = "show that $x^3+4x^2-4x+48=0$"
Q6 = [r"[Figure 2: a photograph of the entrance to a road tunnel, an arch with its maximum height marked 5 m and the "
      r"width of its base marked 6 m.] [Figure 3: the same photograph with axes added: the $x$-axis along the ground "
      r"through $A$, $O$ and $B$, the $y$-axis through $O$ and the top of the arch $C$, and a quadratic curve $BCA$ drawn "
      r"over the arch.]",
      "Figure 2 shows the entrance to a road tunnel. The maximum height of the tunnel is measured as 5 metres and the "
      "width of the base of the tunnel is measured as 6 metres.",
      "Figure 3 shows a quadratic curve $BCA$ used to model this entrance.",
      "The points $A$, $O$, $B$ and $C$ are assumed to lie in the same vertical plane and the ground $AOB$ is assumed to "
      "be horizontal."]
Q6A = "Find an equation for curve $BCA$."
Q6C = "A coach has height 4.1 m and width 2.4 m."
Q8 = ["There were 2100 tonnes of wheat harvested on a farm during 2017.",
      "The mass of wheat harvested during each subsequent year is expected to increase by 1.2% per year."]
Q8A = ("Find the total mass of wheat expected to be harvested from 2017 to 2030 inclusive, giving your answer to 3 "
       "significant figures.")
Q10 = ["The function f is defined by", r"$$\mathrm{f}:x\mapsto\frac{3x-5}{x+1},\quad x\in\mathbb{R},\ x\neq-1$$"]
Q10G = ["The function g is defined by", r"$$\mathrm{g}:x\mapsto x^2-3x,\quad x\in\mathbb{R},\ 0\leqslant x\leqslant5$$"]
Q10D = "Find the range of g."
Q11 = [r"[Figure 5: the curve $C$, a cubic coming down from the upper left through $A$ on the negative $x$-axis to a "
       r"minimum below the axis, rising through $O$ to a maximum, then falling through $B$ on the positive $x$-axis.]",
       r"Figure 5 shows a sketch of the curve $C$ with equation $y=\mathrm{f}(x)$.",
       "The curve $C$ crosses the $x$-axis at the origin, $O$, and at the points $A$ and $B$ as shown in Figure 5.",
       "Given that", r"$$\mathrm{f}'(x)=k-4x-3x^2$$", "where $k$ is constant,"]
Q13A = [r"Express $2\sin\theta-1.5\cos\theta$ in the form $R\sin(\theta-\alpha)$, where $R>0$ and "
        r"$0<\alpha<\frac{\pi}{2}$",
        r"State the value of $R$ and give the value of $\alpha$ to 4 decimal places."]
Q13M = ["Tom models the depth of water, $D$ metres, at Southview harbour on 18th October 2017 by the formula",
        r"$$D=6+2\sin\left(\frac{4\pi t}{25}\right)-1.5\cos\left(\frac{4\pi t}{25}\right),\qquad0\leqslant t\leqslant24$$",
        "where $t$ is the time, in hours, after 00:00 hours on 18th October 2017.", "Use Tom’s model to"]

LATEX = {
    "01a": L(*Q1, Q1A),
    "01b": L(*Q1, "Explain how the trapezium rule can be used to give a better approximation for the area of $R$."),
    "01c": L(*Q1, "(a) " + Q1A,
             "(c) Giving your answer to 3 decimal places in each case, use your answer to part (a) to deduce an estimate "
             "for", r"(i) $\displaystyle\int_1^3\frac{5x}{1+\sqrt{x}}\,\mathrm{d}x$",
             r"(ii) $\displaystyle\int_1^3\left(6+\frac{x}{1+\sqrt{x}}\right)\mathrm{d}x$"),
    "02a": L(*Q2A),
    "02b": L("(a) " + Q2A[0], *Q2A[1:],
             r"(b) (i) Use the expansion from part (a), with $x=\frac{1}{10}$, to find an approximate value for $\sqrt{2}$",
             r"Give your answer in the form $\frac{p}{q}$ where $p$ and $q$ are integers.",
             r"(ii) Explain why substituting $x=\frac{1}{10}$ into this binomial expansion leads to a valid "
             r"approximation."),
    "03a": L(*Q3, Q3A),
    "03b": L(*Q3, "(a) " + Q3A,
             r"(b) Hence find $\displaystyle\sum_{r=1}^{100}a_r+\sum_{r=1}^{99}a_r$"),
    "04a": L(*Q4, "Given that $ABCD$ is a parallelogram,", "find the position vector of point $D$."),
    "04b": L(*Q4, r"The vector $\overrightarrow{AX}$ has the same direction as $\overrightarrow{AB}$.",
             r"Given that $\left|\overrightarrow{AX}\right|=10\sqrt{2}$,", "find the position vector of $X$."),
    "05a": L(*Q5, r"Given that $\mathrm{f}(-6)=0$", "(i) show that $a=4$",
             r"(ii) express $\mathrm{f}(x)$ as a product of two algebraic factors."),
    "05b": L(*Q5, Q5G, Q5B),
    "05c": L(*Q5, r"Given that $\mathrm{f}(-6)=0$", "(a) (i) show that $a=4$",
             r"(ii) express $\mathrm{f}(x)$ as a product of two algebraic factors.", Q5G, "(b) " + Q5B,
             "(c) hence explain why", r"$$2\log_2(x+2)+\log_2x-\log_2(x-6)=3$$", "has no real roots."),
    "06a": L(*Q6, Q6A),
    "06b": L(*Q6, "(a) " + Q6A, Q6C, "(b) Determine whether or not it is possible for the coach to enter the tunnel."),
    "06c": L(*Q6, Q6C, "Suggest a reason why this model may not be suitable to determine whether or not the coach can "
                       "pass through the tunnel."),
    "07": L(r"[Figure 4: the curve $y=2\mathrm{e}^{2x}-x\mathrm{e}^{2x}$, close to the negative $x$-axis on the left, "
            r"crossing the positive $y$-axis, rising to a maximum and then falling steeply to cross the positive "
            r"$x$-axis; the region $R$ between the curve, the $x$-axis and the $y$-axis is shaded.]",
            "Figure 4 shows a sketch of part of the curve with equation",
            r"$$y=2\mathrm{e}^{2x}-x\mathrm{e}^{2x},\qquad x\in\mathbb{R}$$",
            "The finite region $R$, shown shaded in Figure 4, is bounded by the curve, the $x$-axis and the $y$-axis.",
            r"Use calculus to show that the exact area of $R$ can be written in the form $p\mathrm{e}^4+q$, where $p$ "
            r"and $q$ are rational constants to be found.",
            "(Solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, "(a) " + Q8A, "Each year it costs", "• £5.15 per tonne to harvest the first 2000 tonnes of wheat",
             "• £6.45 per tonne to harvest wheat in excess of 2000 tonnes",
             "(b) Use this information to find the expected cost of harvesting the wheat from 2017 to 2030 inclusive. "
             "Give your answer to the nearest £1000"),
    "09": L("The curve $C$ has equation", "$$y=2x^3+5$$", "The curve $C$ passes through the point $P(1, 7)$.",
            "Use differentiation from first principles to find the value of the gradient of the tangent to $C$ at "
            "$P$."),
    "10a": L(*Q10, r"Find $\mathrm{f}^{-1}(x)$."),
    "10b": L(*Q10, "Show that", r"$$\mathrm{ff}(x)=\frac{x+a}{x-1},\quad x\in\mathbb{R},\ x\neq\pm1$$",
             "where $a$ is an integer to be found."),
    "10c": L(*Q10, *Q10G, r"Find the value of $\mathrm{fg}(2)$."),
    "10d": L(*Q10G, Q10D),
    "10e": L(*Q10G, "Explain why the function g does not have an inverse."),
    "11a": L(*Q11, r"show that $C$ has a point of inflection at $x=-\frac{2}{3}$"),
    "11b": L(*Q11, r"Given also that the distance $AB=4\sqrt{2}$",
             "find, showing your working, the integer value of $k$."),
    "12": L("Show that", r"$$\int_0^{\frac{\pi}{2}}\frac{\sin2\theta}{1+\cos\theta}\,\mathrm{d}\theta=2-2\ln2$$"),
    "13a": L(*Q13A),
    "13b": L(*Q13M, "find the depth of water at 00:00 hours on 18th October 2017,"),
    "13c": L("(a) " + Q13A[0], Q13A[1], *Q13M, "(c) find the maximum depth of water,"),
    "13d": L("(a) " + Q13A[0], Q13A[1], *Q13M,
             "(d) find the time, in the afternoon, when the maximum depth of water occurs.",
             "Give your answer to the nearest minute."),
    "13e": L(*Q13M[:3],
             "Tom’s model is supported by measurements of $D$ taken at regular intervals on 18th October 2017. Jolene "
             "attempts to use a similar model in order to model the depth of water at Southview harbour on 19th October "
             "2017.",
             "Jolene models the depth of water, $H$ metres, at Southview harbour on 19th October 2017 by the formula",
             r"$$H=6+2\sin\left(\frac{4\pi x}{25}\right)-1.5\cos\left(\frac{4\pi x}{25}\right),\qquad0\leqslant x\leqslant24$$",
             "where $x$ is the time, in hours, after 00:00 hours on 19th October 2017.",
             "By considering the depth of water at 00:00 hours on 19th October 2017 for both models,",
             "(i) explain why Jolene’s model is not correct,", "(ii) hence find a suitable model for $H$ in terms of $x$."),
    "14": L(r"[Figure 6: the curve $C$, a closed oval tilted down to the right, centred on $O$ and crossing both axes "
            r"twice.]",
            "Figure 6 shows a sketch of the curve $C$ with parametric equations",
            r"$$x=4\cos\left(t+\frac{\pi}{6}\right),\ y=2\sin t,\qquad0<t\leqslant2\pi$$",
            "Show that a Cartesian equation of $C$ can be written in the form", "$$(x+y)^2+ay^2=b$$",
            "where $a$ and $b$ are integers to be found."),
}

PT = r"\left(t+\frac{\pi}{6}\right)"
COS = rf"4\left(\cos t\cos\left(\frac{{\pi}}{{6}}\right)-\sin t\sin\left(\frac{{\pi}}{{6}}\right)\right)"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", NUM, "9.4", 3, LATEX["01a"],
      [r"B1 (AO 1.1b): $\text{Area}(R)\approx\frac{1}{2}\times0.5\times\ldots$ Notes: Outside brackets "
       r"$\frac{1}{2}\times0.5$ or $\frac{0.5}{2}$ or 0.25 or $\frac{1}{4}$",
       r"M1 (AO 1.1b): $\left[0.5+2(0.6742+0.8284+0.9686)+1.0981\right]$. Notes: For structure of trapezium rule "
       r"$[\ldots\ldots\ldots]$. No errors are allowed, e.g. an omission of a $y$-ordinate or an extra $y$-ordinate or a "
       r"repeated $y$-ordinate.",
       r"A1 (AO 1.1b): $\left\{=\frac{1}{4}\times6.5405\right\}=1.635125=1.635$ (3 dp). Notes: Correct method leading to a "
       r"correct answer only of 1.635"],
      True, 2),
    e("01b", "1(b)", NUM, "9.4", 1, LATEX["01b"],
      [r"B1 (AO 2.4): Any valid reason, for example • Increase the number of strips • Decrease the width of the strips • "
       r"Use more trapezia between $x=1$ and $x=3$. Notes: See scheme"],
      True, 2),
    e("01c", "1(c)", NUM, "9.4, 8.3", 2, LATEX["01c"],
      [r"B1ft (AO 2.2a): (i) $\left\{\int_1^3\frac{5x}{1+\sqrt{x}}\,\mathrm{d}x\right\}=5(\text{“}1.635\text{”})=8.175$. "
       r"Notes: 8.175 or a value which is $5\times$ their answer to part (a) Note: Allow B1ft for 8.176 (to 3 dp) which is "
       r"found from $5(1.63125)=8.175625$ Note: Do not allow an answer of 8.1886… which is found directly from "
       r"integration",
       r"B1ft (AO 2.2a): (ii) $\left\{\int_1^3\left(6+\frac{x}{1+\sqrt{x}}\right)\mathrm{d}x\right\}=6(2)+"
       r"(\text{“}1.635\text{”})=13.635$. Notes: 13.635 or a value which is 12 + their answer to part (a) Note: Do not "
       r"allow an answer of 13.6377… which is found directly from integration"],
      True, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", SEQ, "4.1", 4, LATEX["02a"],
      [r"B1 (AO 1.1b): $(4+5x)^{\frac{1}{2}}=(4)^{\frac{1}{2}}\left(1+\frac{5x}{4}\right)^{\frac{1}{2}}="
       r"2\left(1+\frac{5x}{4}\right)^{\frac{1}{2}}$. Notes: Manipulates $(4+5x)^{\frac{1}{2}}$ by taking out a factor of "
       r"$(4)^{\frac{1}{2}}$ or 2",
       r"M1 (AO 1.1b): $=\{2\}\left[1+\left(\frac{1}{2}\right)\left(\frac{5x}{4}\right)+\frac{\left(\frac{1}{2}\right)"
       r"\left(-\frac{1}{2}\right)}{2!}\left(\frac{5x}{4}\right)^2+\ldots\right]$. Notes: Expands $(\ldots+\lambda x)^{"
       r"\frac{1}{2}}$ to give at least 2 terms which can be simplified or un-simplified, E.g. "
       r"$1+\left(\frac{1}{2}\right)(\lambda x)$ or $\left(\frac{1}{2}\right)(\lambda x)+\frac{\left(\frac{1}{2}\right)"
       r"\left(-\frac{1}{2}\right)}{2!}(\lambda x)^2$ or $1+\ldots+\frac{\left(\frac{1}{2}\right)\left(-\frac{1}{2}"
       r"\right)}{2!}(\lambda x)^2$ where $\lambda$ is a numerical value and where $\lambda\neq1$.",
       r"A1ft (AO 1.1b): $=\{2\}\left[1+\left(\frac{1}{2}\right)\left(\frac{5x}{4}\right)+\frac{\left(\frac{1}{2}\right)"
       r"\left(-\frac{1}{2}\right)}{2!}\left(\frac{5x}{4}\right)^2+\ldots\right]$. Notes: A correct simplified or "
       r"un-simplified $1+\left(\frac{1}{2}\right)(\lambda x)+\frac{\left(\frac{1}{2}\right)\left(-\frac{1}{2}\right)}{2!}"
       r"(\lambda x)^2$ expansion with consistent $(\lambda x)$",
       r"A1 (AO 2.1): $=2+\frac{5}{4}x-\frac{25}{64}x^2+\ldots$ Notes: Fully correct solution leading to "
       r"$2+\frac{5}{4}x+kx^2$, where $k=-\frac{25}{64}$"],
      False, 4),
    e("02b", "2(b)", SEQ, "4.1", 4, LATEX["02b"],
      [r"M1 (AO 1.1b): (i) $\left\{x=\frac{1}{10}\Rightarrow\right\}(4+5(0.1))^{\frac{1}{2}}=\sqrt{4.5}="
       r"\frac{3}{2}\sqrt{2}$ or $\frac{3}{\sqrt{2}}$. Notes: Attempts to substitute $x=\frac{1}{10}$ or 0.1 into "
       r"$(4+5x)^{\frac{1}{2}}$",
       r"M1 (AO 3.1a): $\frac{3}{2}\sqrt{2}$ or $1.5\sqrt{2}$ or $\frac{3}{\sqrt{2}}=2+\frac{5}{4}\left(\frac{1}{10}\right)-"
       r"\frac{25}{64}\left(\frac{1}{10}\right)^2+\ldots\ \{=2.121\ldots\}$ $\Rightarrow\frac{3}{2}\sqrt{2}=\frac{543}{256}$ "
       r"or $\frac{3}{\sqrt{2}}=\frac{543}{256}\Rightarrow\sqrt{2}=\ldots$ Notes: A complete method of finding an approximate "
       r"value for $\sqrt{2}$. E.g. • substituting $x=\frac{1}{10}$ or 0.1 into their part (a) binomial expansion and "
       r"equating the result to an expression of the form $\alpha\sqrt{2}$ or $\frac{\beta}{\sqrt{2}}$ ; "
       r"$\alpha,\beta\neq0$ • followed by re-arranging to give $\sqrt{2}=\ldots$",
       r"A1 (AO 1.1b): So, $\sqrt{2}=\frac{181}{128}$ or $\sqrt{2}=\frac{256}{181}$. Notes: $\frac{181}{128}$ or any "
       r"equivalent fraction, e.g. $\frac{362}{256}$ or $\frac{543}{384}$ Also allow $\frac{256}{181}$ or any equivalent "
       r"fraction",
       r"B1 (AO 2.3): (ii) $x=\frac{1}{10}$ satisfies $|x|<\frac{4}{5}$ (o.e.), so the approximation is valid. Notes: "
       r"Explains that the approximation is valid because $x=\frac{1}{10}$ satisfies $|x|<\frac{4}{5}$"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", SEQ, "4.2, 4.3", 3, LATEX["03a"],
      [r"M1 (AO 1.1b): $a_1=3$, $a_2=0$, $a_3=1.5$, $a_4=3$. Notes: Uses the formula $a_{n+1}=\frac{a_n-3}{a_n-2}$, with "
       r"$a_1=3$ to generate values for $a_2$, $a_3$ and $a_4$",
       r"M1 (AO 2.2a): $\sum_{r=1}^{100}a_r=33(4.5)+3$. Notes: Finds $a_4=3$ and deduces $\sum_{r=1}^{100}a_r="
       r"33(\text{“}3\text{”}+\text{“}0\text{”}+\text{“}1.5\text{”})+\text{“}3\text{”}$",
       r"A1 (AO 1.1b): $=151.5$. Notes: which leads to a correct answer of 151.5"],
      False, 6),
    e("03b", "3(b)", SEQ, "4.3, 4.2", 1, LATEX["03b"],
      [r"B1ft (AO 2.2a): $\sum_{r=1}^{100}a_r+\sum_{r=1}^{99}a_r=(2)(151.5)-3=300$. Notes: Follow through on their periodic "
       r"function. Deduces that either • $\sum_{r=1}^{100}a_r+\sum_{r=1}^{99}a_r=(2)(\text{“}151.5\text{”})-3=300$ • "
       r"$\sum_{r=1}^{100}a_r+\sum_{r=1}^{99}a_r=\text{“}151.5\text{”}+(33)(\text{“}3\text{”}+\text{“}0\text{”}+"
       r"\text{“}1.5\text{”})=151.5+148.5=300$"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", VEC, "10.4, 10.3", 2, LATEX["04a"],
      [rf"M1 (AO 3.1a): $\overrightarrow{{OA}}={I}+7{J}-2{K}$, $\overrightarrow{{OB}}=4{I}+3{J}+3{K}$, "
       rf"$\overrightarrow{{OC}}=2{I}+10{J}+9{K}$ $\overrightarrow{{OD}}=\overrightarrow{{OC}}+\overrightarrow{{BA}}="
       rf"(2{I}+10{J}+9{K})+(-3{I}+4{J}-5{K})$ or $\overrightarrow{{OD}}=\overrightarrow{{OA}}+\overrightarrow{{BC}}="
       rf"({I}+7{J}-2{K})+(-2{I}+7{J}+6{K})$. Notes: A complete method for finding the position vector of $D$",
       rf"A1 (AO 1.1b): So $\overrightarrow{{OD}}=-{I}+14{J}+4{K}$. Notes: $-{I}+14{J}+4{K}$ or "
       rf"$\begin{{pmatrix}}-1\\14\\4\end{{pmatrix}}$"],
      False, 8),
    e("04b", "4(b)", VEC, "10.2, 10.4, 10.3", 3, LATEX["04b"],
      [rf"M1 (AO 1.1b): $\left\{{\overrightarrow{{AB}}=3{I}-4{J}+5{K}\Rightarrow\right\}}\left|\overrightarrow{{AB}}\right|="
       rf"\sqrt{{(3)^2+(-4)^2+(5)^2}}\ \left\{{=\sqrt{{50}}=5\sqrt{{2}}\right\}}$. Notes: A complete attempt to find "
       rf"$\left|\overrightarrow{{AB}}\right|$ or $\left|\overrightarrow{{BA}}\right|$",
       rf"M1 (AO 3.1a): As $\left|\overrightarrow{{AX}}\right|=10\sqrt{{2}}$ then $\left|\overrightarrow{{AX}}\right|="
       rf"2\left|\overrightarrow{{AB}}\right|\Rightarrow\overrightarrow{{AX}}=2\overrightarrow{{AB}}$ "
       rf"$\overrightarrow{{OX}}=\overrightarrow{{OA}}+2\overrightarrow{{AB}}=({I}+7{J}-2{K})+2(3{I}-4{J}+5{K})$ or "
       rf"$\overrightarrow{{OX}}=\overrightarrow{{OB}}+\overrightarrow{{AB}}=(4{I}+3{J}+3{K})+(3{I}-4{J}+5{K})$. Notes: A "
       rf"complete process for finding the position vector of $X$",
       rf"A1 (AO 1.1b): So $\overrightarrow{{OX}}=7{I}-{J}+8{K}$ only. Notes: $7{I}-{J}+8{K}$ or "
       rf"$\begin{{pmatrix}}7\\-1\\8\end{{pmatrix}}$"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", ALG, "2.6", 4, LATEX["05a"],
      [r"M1 (AO 1.1b): (i) $\mathrm{f}(x)=x^3+ax^2-ax+48$, $x\in\mathbb{R}$ $\mathrm{f}(-6)=(-6)^3+a(-6)^2-a(-6)+48$. Notes: "
       r"Applies $\mathrm{f}(-6)$",
       r"A1* (AO 1.1b): $=-216+36a+6a+48=0\Rightarrow42a=168\Rightarrow a=4$ *. Notes: Applies $\mathrm{f}(-6)=0$ to show "
       r"that $a=4$",
       r"M1 (AO 2.2a): (ii) Hence, $\mathrm{f}(x)=(x+6)(x^2-2x+8)$. Notes: Deduces $(x+6)$ is a factor of $\mathrm{f}(x)$ "
       r"and attempts to find a quadratic factor of $\mathrm{f}(x)$ by either equating coefficients or by algebraic long "
       r"division",
       r"A1 (AO 1.1b): Hence, $\mathrm{f}(x)=(x+6)(x^2-2x+8)$. Notes: $(x+6)(x^2-2x+8)$"],
      False, 10),
    e("05b", "5(b)", EXP, "6.4, 6.3", 4, LATEX["05b"],
      [r"M1 (AO 1.2): $2\log_2(x+2)+\log_2x-\log_2(x-6)=3$ E.g. • $\log_2(x+2)^2+\log_2x-\log_2(x-6)=3$ • "
       r"$2\log_2(x+2)+\log_2\left(\frac{x}{x-6}\right)=3$. Notes: Evidence of applying a correct law of logarithms",
       r"M1 (AO 1.1b): $\log_2\left(\frac{x(x+2)^2}{(x-6)}\right)=3$ $\left[\text{or }\log_2\left(x(x+2)^2\right)="
       r"\log_2\left(8(x-6)\right)\right]$. Notes: Uses correct laws of logarithms to give either • an expression of the "
       r"form $\log_2(\mathrm{h}(x))=k$, where $k$ is a constant • an expression of the form "
       r"$\log_2(\mathrm{g}(x))=\log_2(\mathrm{h}(x))$",
       r"B1 (AO 1.1b): $\left(\frac{x(x+2)^2}{(x-6)}\right)=2^3$ $\left\{\text{i.e. }\log_2a=3\Rightarrow a=2^3\text{ or }8"
       r"\right\}$. Notes: Evidence in their working of $\log_2a=3\Rightarrow a=2^3$ or 8",
       r"A1* (AO 2.1): $x(x+2)^2=8(x-6)\Rightarrow x(x^2+4x+4)=8x-48\Rightarrow x^3+4x^3+4x=8x-48\Rightarrow x^3+4x^3-4x+"
       r"48=0$ *. Notes: Correctly proves $x^3+4x^3-4x+48=0$ with no errors seen [sic: the question has "
       r"$x^3+4x^2-4x+48=0$]"],
      False, 10),
    e("05c", "5(c)", EXP, "6.3, 2.3, 2.6", 2, LATEX["05c"],
      [r"B1 (AO 2.4): $2\log_2(x+2)+\log_2x-\log_2(x-6)=3\Rightarrow x^3+4x^3-4x+48=0$ [sic: the question has $x^3+4x^2-4x+48=0$] $\Rightarrow(x+6)(x^2-2x+8)=0$ Reason 1: "
       r"E.g. • $\log_2x$ is not defined when $x=-6$ • $\log_2(x-6)$ is not defined when $x=-6$ • $x=-6$, but $\log_2x$ is "
       r"only defined for $x>0$ Reason 2: • $b^2-4ac=-28<0$, so $(x^2-2x+8)=0$ has no (real) roots At least one of Reason "
       r"1 or Reason 2. Notes: See scheme",
       r"B1 (AO 2.1): Both Reason 1 and Reason 2. Notes: See scheme"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", ALG, "2.11, 2.3", 3, LATEX["06a"],
      [r"M1 (AO 3.3): Attempts to use an appropriate model; e.g. $y=A(3-x)(3+x)$ or $y=A(9-x^2)$. Notes: Translates the "
       r"given situation into an appropriate quadratic model – see scheme",
       r"M1 (AO 3.1b): e.g. $y=A(9-x^2)$ Substitutes $x=0$, $y=5\Rightarrow5=A(9-0)\Rightarrow A=\frac{5}{9}$. Notes: "
       r"Applies the maximum height constraint in an attempt to find the equation of the model – see scheme",
       r"A1 (AO 1.1b): $y=\frac{5}{9}(9-x^2)$ or $y=\frac{5}{9}(3-x)(3+x)$, $\{-3\leqslant x\leqslant3\}$. Notes: Finds a "
       r"suitable equation – see scheme"],
      True, 12),
    e("06b", "6(b)", ALG, "2.11", 2, LATEX["06b"],
      [r"M1 (AO 3.4): Substitutes $x=\frac{2.4}{2}$ into their $y=\frac{5}{9}(9-x^2)$. Notes: See scheme",
       r"A1 (AO 2.2b): $y=\frac{5}{9}(9-x^2)=4.2>4.1\Rightarrow$ Coach can enter the tunnel. Notes: Applies a fully "
       r"correct argument to infer {by assuming that curve $BCA$ is quadratic and the given measurements are correct}, "
       r"that is possible for the coach to enter the tunnel",
       r"ALT: (b) Alt 1 — M1 (AO 3.4): $4.1=\frac{5}{9}(9-x^2)\Rightarrow x=\frac{9\sqrt{2}}{10}$, so maximum width "
       r"$=2\left(\frac{9\sqrt{2}}{10}\right)$",
       r"ALT: (b) Alt 1 — A1 (AO 2.2b): $=2.545\ldots>2.4\Rightarrow$ Coach can enter the tunnel"],
      True, 12),
    e("06c", "6(c)", ALG, "2.11", 1, LATEX["06c"],
      [r"B1 (AO 3.5b): E.g. • Coach needs to enter through the centre of the tunnel. This will only be possible if it is a "
       r"one-way tunnel • In real-life the road may be cambered (and not horizontal) • The quadratic curve $BCA$ is "
       r"modelled for the entrance to the tunnel but we do not know if this curve is valid throughout the entire length "
       r"of the tunnel • There may be overhead lights in the tunnel which may block the path of the coach. Notes: See "
       r"scheme"],
      True, 12),

    # ---------------- Q7 ----------------
    e("07", "7", INT, "8.5, 8.3", 5, LATEX["07"],
      [r"M1 (AO 3.1a): $\left\{\int x\mathrm{e}^{2x}\,\mathrm{d}x\right\}$, $\left\{u=x\Rightarrow\frac{\mathrm{d}u}"
       r"{\mathrm{d}x}=1,\ \frac{\mathrm{d}v}{\mathrm{d}x}=\mathrm{e}^{2x}\Rightarrow v=\frac{1}{2}\mathrm{e}^{2x}\right\}$ "
       r"$\left\{\int x\mathrm{e}^{2x}\,\mathrm{d}x\right\}=\frac{1}{2}x\mathrm{e}^{2x}-\int\frac{1}{2}\mathrm{e}^{2x}"
       r"\{\mathrm{d}x\}$. Notes: Attempts to solve the problem by recognising the need to apply a method of integration "
       r"by parts on either $x\mathrm{e}^{2x}$ or $(2-x)\mathrm{e}^{2x}$. Allow this mark for either • "
       r"$\pm x\mathrm{e}^{2x}\to\pm\lambda x\mathrm{e}^{2x}\pm\int\mu\mathrm{e}^{2x}\{\mathrm{d}x\}$ • "
       r"$(2-x)\mathrm{e}^{2x}\to\pm\lambda(2-x)\mathrm{e}^{2x}\pm\int\mu\mathrm{e}^{2x}\{\mathrm{d}x\}$ where "
       r"$\lambda,\mu\neq0$ are constants.",
       r"M1 (AO 1.1b): $\left\{\int2\mathrm{e}^{2x}-x\mathrm{e}^{2x}\,\mathrm{d}x\right\}=\mathrm{e}^{2x}-\left(\frac{1}{2}x"
       r"\mathrm{e}^{2x}-\int\frac{1}{2}\mathrm{e}^{2x}\{\mathrm{d}x\}\right)$. Notes: For either • "
       r"$2\mathrm{e}^{2x}-x\mathrm{e}^{2x}\to\mathrm{e}^{2x}\pm\frac{1}{2}x\mathrm{e}^{2x}\pm\int\frac{1}{2}\mathrm{e}^{2x}"
       r"\{\mathrm{d}x\}$ • $(2-x)\mathrm{e}^{2x}\to\pm\frac{1}{2}(2-x)\mathrm{e}^{2x}\pm\int\frac{1}{2}\mathrm{e}^{2x}"
       r"\{\mathrm{d}x\}$",
       r"A1 (AO 1.1b): $=\mathrm{e}^{2x}-\left(\frac{1}{2}x\mathrm{e}^{2x}-\frac{1}{4}\mathrm{e}^{2x}\right)$. Notes: Correct "
       r"integration which can be simplified or un-simplified. E.g. • $2\mathrm{e}^{2x}-x\mathrm{e}^{2x}\to\mathrm{e}^{2x}-"
       r"\left(\frac{1}{2}x\mathrm{e}^{2x}-\frac{1}{4}\mathrm{e}^{2x}\right)$ • $2\mathrm{e}^{2x}-x\mathrm{e}^{2x}\to"
       r"\mathrm{e}^{2x}-\frac{1}{2}x\mathrm{e}^{2x}+\frac{1}{4}\mathrm{e}^{2x}$ • $2\mathrm{e}^{2x}-x\mathrm{e}^{2x}\to"
       r"\frac{5}{4}\mathrm{e}^{2x}-\frac{1}{2}x\mathrm{e}^{2x}$ • $(2-x)\mathrm{e}^{2x}\to\frac{1}{2}(2-x)\mathrm{e}^{2x}+"
       r"\frac{1}{4}\mathrm{e}^{2x}$",
       r"M1 (AO 2.2a): $\text{Area}(R)=\int_0^22\mathrm{e}^{2x}-x\mathrm{e}^{2x}\,\mathrm{d}x=\left[\frac{5}{4}\mathrm{e}^{2x}-"
       r"\frac{1}{2}x\mathrm{e}^{2x}\right]_0^2$. Notes: Deduces that the upper limit is 2 and uses limits of 2 and 0 on "
       r"their integrated function",
       r"A1 (AO 2.1): $=\left(\frac{5}{4}\mathrm{e}^4-\mathrm{e}^4\right)-\left(\frac{5}{4}\mathrm{e}^{2(0)}-\frac{1}{2}(0)"
       r"\mathrm{e}^0\right)=\frac{1}{4}\mathrm{e}^4-\frac{5}{4}$. Notes: Correct proof leading to $p\mathrm{e}^4+q$, where "
       r"$p=\frac{1}{4}$, $q=-\frac{5}{4}$",
       r"ALT: 7 Alt 1 — M1 (AO 3.1a): $\left\{\int2\mathrm{e}^{2x}-x\mathrm{e}^{2x}\,\mathrm{d}x=\int(2-x)\mathrm{e}^{2x}\,"
       r"\mathrm{d}x\right\}$, $\left\{u=2-x\Rightarrow\frac{\mathrm{d}u}{\mathrm{d}x}=-1,\ \frac{\mathrm{d}v}{\mathrm{d}x}="
       r"\mathrm{e}^{2x}\Rightarrow v=\frac{1}{2}\mathrm{e}^{2x}\right\}$ $=\frac{1}{2}(2-x)\mathrm{e}^{2x}-\int-\frac{1}{2}"
       r"\mathrm{e}^{2x}\{\mathrm{d}x\}$",
       r"ALT: 7 Alt 1 — M1 (AO 1.1b): $=\frac{1}{2}(2-x)\mathrm{e}^{2x}-\int-\frac{1}{2}\mathrm{e}^{2x}\{\mathrm{d}x\}$",
       r"ALT: 7 Alt 1 — A1 (AO 1.1b): $=\frac{1}{2}(2-x)\mathrm{e}^{2x}+\frac{1}{4}\mathrm{e}^{2x}$",
       r"ALT: 7 Alt 1 — M1 (AO 2.2a): $\left\{\text{Area}(R)=\int_0^2(2-x)\mathrm{e}^{2x}\,\mathrm{d}x=\right\}"
       r"\left[\frac{1}{2}(2-x)\mathrm{e}^{2x}+\frac{1}{4}\mathrm{e}^{2x}\right]_0^2$",
       r"ALT: 7 Alt 1 — A1 (AO 2.1): $=\left(0+\frac{1}{4}\mathrm{e}^4\right)-\left(\frac{1}{2}(2)\mathrm{e}^0+\frac{1}{4}"
       r"\mathrm{e}^0\right)=\frac{1}{4}\mathrm{e}^4-\frac{5}{4}$"],
      True, 14),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", SEQ, "4.5, 4.6", 2, LATEX["08a"],
      [r"M1 (AO 3.1b): Total amount $=\frac{2100(1-(1.012)^{14})}{1-1.012}$ or $\frac{2100((1.012)^{14}-1)}{1.012-1}$. "
       r"Notes: Attempts to apply the correct geometric summation formula with either $n=13$ or $n=14$, $a=2100$ and "
       r"$r=1.012$ (Condone $r=1.12$)",
       r"A1 (AO 1.1b): $=31806.9948\ldots=31800$ (tonnes) (3 sf). Notes: Correct answer of 31800 (tonnes)"],
      False, 16),
    e("08b", "8(b)", SEQ, "4.5, 4.6", 3, LATEX["08b"],
      [r"M1 (AO 3.1b): Total Cost $=5.15(2000(14))+6.45(31806.9948\ldots-(2000)(14))$. Notes: Fully correct method to find "
       r"the total cost",
       r"M1 (AO 1.1b): Total Cost $=5.15(2000(14))+6.45(31806.9948\ldots-(2000)(14))$ $=5.15(28000)+6.45(3806.9948\ldots)="
       r"144200+24555.116\ldots$ Notes: For either • $5.15(2000(14))\ \{=144200\}$ • $6.45(\text{“}31806.9948\ldots"
       r"\text{”}-(2000)(14))\ \{=24555.116\ldots\}$ • $5.15(2000(13))\ \{=133900\}$ • $6.45(\text{“}29354.73794\ldots"
       r"\text{”}-(2000)(13))\ \{=21638.059\ldots\}$",
       r"A1 (AO 3.2a): $=168755.116\ldots=£169000$ (nearest £1000). Notes: Correct answer of £169000 Note: Using rounded "
       r"answer in part (a) gives 168710 which becomes £169000 (nearest £1000)"],
      False, 16),

    # ---------------- Q9 ----------------
    e("09", "9", DIFF, "7.1", 5, LATEX["09"],
      [r"B1 (AO 1.1b): Gradient of chord $=\frac{(2(x+h)^3+5)-(2x^3+5)}{x+h-h}$. Notes: $2(x+h)^3+5$, seen or implied",
       r"M1 (AO 2.1): Gradient of chord $=\frac{(2(x+h)^3+5)-(2x^3+5)}{x+h-h}$. Notes: Begins the proof by attempting to "
       r"write the gradient of the chord in terms of $x$ and $h$",
       r"B1 (AO 1.1b): $(x+h)^3=x^3+3x^2h+3xh^2+h^3$. Notes: $(x+h)^3\to x^3+3x^2h+3xh^2+h^3$, by expanding brackets or by "
       r"using a correct binomial expansion",
       r"A1 (AO 1.1b): Gradient of chord $=\frac{(2(x^3+3x^2h+3xh^2+h^3)+5)-(2x^3+5)}{1+h-1}=\frac{2x^3+6x^2h+6xh^2+2h^3+5-"
       r"2x^3-5}{1+h-1}=\frac{6x^2h+6xh^2+2h^3}{h}=6x^2+6xh+2h^2$. Notes: [labelled M1 in the notes] Correct process to "
       r"obtain the gradient of the chord as $\alpha x^2+\beta xh+\gamma h^2$, $\alpha,\beta,\gamma\neq0$",
       r"A1 (AO 2.2a): $\frac{\mathrm{d}y}{\mathrm{d}x}=\lim_{h\to0}(6x^2+6xh+2h^2)=6x^2$ and so at $P$, "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}=6(1)^2=6$. Notes: Correctly shows that the gradient of the chord is "
       r"$6x^2+6xh+2h^2$ and applies a limiting argument to deduce when $y=2x^3+5$, $\frac{\mathrm{d}y}{\mathrm{d}x}=6x^2$. "
       r"E.g. $\lim_{h\to0}(6x^2+6xh+2h^2)=6x^2$. Finally, deduces that at the point $P$, $\frac{\mathrm{d}y}{\mathrm{d}x}=6$. "
       r"Note: $\delta x$ can be used in place of $h$",
       r"ALT: 9 Alt 1 — B1 (AO 1.1b): Let a point $Q$ have $x$ coordinate $1+h$, so $y_Q=2(1+h)^3+5$ "
       r"$\{P(1,7),Q(1+h,2(1+h)^3+3)\Rightarrow\}$ [sic: the same line gives $y_Q=2(1+h)^3+5$]. Notes: Writes down the $y$ coordinate of a point close to $P$.",
       r"ALT: 9 Alt 1 — M1 (AO 2.1): Gradient $PQ=\frac{2(1+h)^3+5-7}{1+h-1}$. Notes: Begins the proof by attempting to "
       r"write the gradient of the chord $PQ$ in terms of $h$",
       r"ALT: 9 Alt 1 — B1 (AO 1.1b): $(1+h)^3=1+3h+3h^2+h^3$",
       r"ALT: 9 Alt 1 — A1 (AO 1.1b): Gradient $PQ=\frac{2(1+3h+3h^2+h^3)+5-7}{1+h-1}=\frac{6h+6h^2+2h^3}{h}=6+6h+2h^2$. "
       r"Notes: [labelled M1 in the notes] Correct process to obtain the gradient of the chord $PQ$ as "
       r"$\alpha+\beta h+\gamma h^2$, $\alpha,\beta,\gamma\neq0$",
       r"ALT: 9 Alt 1 — A1 (AO 2.2a): $\frac{\mathrm{d}y}{\mathrm{d}x}=\lim_{h\to0}(6+6h+2h^2)=6$. Notes: Correctly shows "
       r"that the gradient of $PQ$ is $6+6h+2h^2$ and applies a limiting argument to deduce that at the point $P$ on "
       r"$y=2x^3+5$, $\frac{\mathrm{d}y}{\mathrm{d}x}=6$. Note: For Alt 1, $\delta x$ can be used in place of $h$"],
      False, 18),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", ALG, "2.8", 3, LATEX["10a"],
      [r"M1 (AO 1.1b): $y=\frac{3x-5}{x+1}\Rightarrow y(x+1)=3x-5\Rightarrow xy+y=3x-5\Rightarrow y+5=3x-xy$. Notes: Attempts "
       r"to find the inverse by cross-multiplying and an attempt to collect all the $x$-terms (or swapped $y$-terms) onto "
       r"one side",
       r"M1 (AO 2.1): $\Rightarrow y+5=x(3-y)\Rightarrow\frac{y+5}{3-y}=x$. Notes: A fully correct method to find the inverse",
       r"A1 (AO 2.5): Hence $\mathrm{f}^{-1}(x)=\frac{x+5}{3-x}$, $x\in\mathbb{R}$, $x\neq3$. Notes: A correct "
       r"$\mathrm{f}^{-1}(x)=\frac{x+5}{3-x}$, $x\in\mathbb{R}$, $x\neq3$, expressed fully in function notation (including "
       r"the domain)"],
      False, 20),
    e("10b", "10(b)", ALG, "2.8", 4, LATEX["10b"],
      [r"M1 (AO 1.1a): $\mathrm{ff}(x)=\frac{3\left(\frac{3x-5}{x+1}\right)-5}{\left(\frac{3x-5}{x+1}\right)+1}$. Notes: "
       r"Attempts to substitute $\mathrm{f}(x)=\frac{3x-5}{x+1}$ into $\frac{3\mathrm{f}(x)-5}{\mathrm{f}(x)+1}$",
       r"M1 (AO 1.1b): $=\frac{\frac{3(3x-5)-5(x+1)}{x+1}}{\frac{(3x-5)+(x+1)}{x+1}}$. Notes: Applies a method of "
       r"“rationalising the denominator” for both their numerator and their denominator.",
       r"A1 (AO 1.1b): $=\frac{\frac{3(3x-5)-5(x+1)}{x+1}}{\frac{(3x-5)+(x+1)}{x+1}}$. Notes: "
       r"$\frac{\frac{3(3x-5)-5(x+1)}{x+1}}{\frac{(3x-5)+(x+1)}{x+1}}$ which can be simplified or un-simplified",
       r"A1 (AO 2.1): $=\frac{9x-15-5x-5}{3x-5+x+1}=\frac{4x-20}{4x-4}=\frac{x-5}{x-1}$ (note that $a=-5$). Notes: Shows "
       r"$\mathrm{ff}(x)=\frac{x+a}{x-1}$ where $a=-5$ or $\mathrm{ff}(x)=\frac{x-5}{x-1}$, with no errors seen."],
      False, 20),
    e("10c", "10(c)", ALG, "2.8", 2, LATEX["10c"],
      [r"M1 (AO 1.1b): $\mathrm{fg}(2)=\mathrm{f}(4-6)=\mathrm{f}(-2)=\frac{3(-2)-5}{-2+1}$. Notes: Attempts to substitute "
       r"the result of $\mathrm{g}(2)$ into f",
       r"A1 (AO 1.1b): $=11$. Notes: Correctly obtains $\mathrm{fg}(2)=11$"],
      False, 20),
    e("10d", "10(d)", ALG, "2.8, 2.3", 3, LATEX["10d"],
      [r"M1 (AO 2.1): $\mathrm{g}(x)=x^2-3x=(x-1.5)^2-2.25$. Hence $\mathrm{g}_{\min}=-2.25$. Notes: Full method to "
       r"establish the minimum of g. E.g. • $(x\pm\alpha)^2+\beta$ leading to $\mathrm{g}_{\min}=\beta$ • Finds the value "
       r"of $x$ for which $\mathrm{g}'(x)=0$ and inserts this value of $x$ back into $\mathrm{g}(x)$ in order to find to "
       r"$\mathrm{g}_{\min}$",
       r"B1 (AO 1.1b): Either $\mathrm{g}_{\min}=-2.25$ or $\mathrm{g}(x)\geqslant-2.25$ or $\mathrm{g}(5)=25-15=10$. Notes: "
       r"For either • finding the correct minimum value of g (Can be implied by $\mathrm{g}(x)\geqslant-2.25$ or "
       r"$\mathrm{g}(x)>-2.25$) • stating $\mathrm{g}(5)=25-15=10$",
       r"A1 (AO 1.1b): $-2.25\leqslant\mathrm{g}(x)\leqslant10$ or $-2.25\leqslant y\leqslant10$. Notes: States the correct "
       r"range for g. E.g. $-2.25\leqslant\mathrm{g}(x)\leqslant10$ or $-2.25\leqslant y\leqslant10$"],
      False, 20),
    e("10e", "10(e)", ALG, "2.8", 1, LATEX["10e"],
      [r"B1 (AO 2.4): E.g. • the function g is many-one • the function g is not one-one • the inverse is one-many • "
       r"$\mathrm{g}(0)=\mathrm{g}(3)=0$. Notes: See scheme"],
      False, 20),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", DIFF, "7.3", 3, LATEX["11a"],
      [r"M1 (AO 1.1b): $\mathrm{f}'(x)=k-4x-3x^2$ $\mathrm{f}''(x)=-4-6x=0$. Notes: E.g. • attempts to find "
       r"$\mathrm{f}''\left(-\frac{2}{3}\right)$ • finds $\mathrm{f}''(x)$ and sets the result equal to 0",
       r"B1 (AO 2.4): Criteria 1 Either $\mathrm{f}''(x)=-4-6x=0\Rightarrow x=\frac{4}{-6}\Rightarrow x=-\frac{2}{3}$ or "
       r"$\mathrm{f}''\left(-\frac{2}{3}\right)=-4-6\left(-\frac{2}{3}\right)=0$ Criteria 2 Either • "
       r"$\mathrm{f}''(-0.7)=-4-6(-0.7)=0.2>0$ $\mathrm{f}''(-0.6)=-4-6(-0.6)=-0.4<0$ or • "
       r"$\mathrm{f}'''\left(-\frac{2}{3}\right)=-6\neq0$ At least one of Criteria 1 or Criteria 2. Notes: See scheme",
       r"A1 (AO 2.1): Both Criteria 1 and Criteria 2 and concludes $C$ has a point of inflection at $x=-\frac{2}{3}$. "
       r"Notes: See scheme"],
      True, 22),
    e("11b", "11(b)", INT, "8.2, 2.3, 2.6", 7, LATEX["11b"],
      [r"M1 (AO 1.1b): $\mathrm{f}'(x)=k-4x-3x^2$, $AB=4\sqrt{2}$ $\mathrm{f}(x)=kx-2x^2-x^3\ \{+c\}$. Notes: Integrates "
       r"$\mathrm{f}'(x)$ to give $\mathrm{f}(x)=\pm kx\pm\alpha x^2\pm\beta x^3$, $\alpha,\beta\neq0$ with or without the "
       r"constant of integration",
       r"A1 (AO 1.1b): $\mathrm{f}(x)=kx-2x^2-x^3\ \{+c\}$. Notes: $\mathrm{f}(x)=kx-2x^2-x^3$, with or without the constant "
       r"of integration",
       r"A1 (AO 2.2a): $\mathrm{f}(0)=0$ or $(0,0)\Rightarrow c=0\Rightarrow\mathrm{f}(x)=kx-2x^2-x^3$ "
       r"$\{\mathrm{f}(x)=0\Rightarrow\}\ \mathrm{f}(x)=x(k-2x-x^2)=0\Rightarrow\{x=0,\}\ k-2x-x^2=0$. Notes: Finds "
       r"$\mathrm{f}(x)=kx-2x^2-x^3+c$, and makes some reference to $y=\mathrm{f}(x)$ passing through the origin to deduce "
       r"$c=0$. Proceeds to produce the result $k-2x-x^2=0$ or $x^2+2x-k=0$",
       r"M1 (AO 2.1): $\{x^2+2x-k=0\}\Rightarrow(x+1)^2-1-k=0$, $x=\ldots$ Notes: Uses a valid method to solve the quadratic "
       r"equation to give $x$ in terms of $k$",
       r"A1 (AO 1.1b): $\Rightarrow x=-1\pm\sqrt{k+1}$. Notes: Correct roots for $x$ in terms of $k$. i.e. "
       r"$x=-1\pm\sqrt{k+1}$",
       r"M1 (AO 2.1): $AB=\left(-1+\sqrt{k+1}\right)-\left(-1-\sqrt{k+1}\right)=4\sqrt{2}\Rightarrow k=\ldots$ Notes: Applies "
       r"$AB=4\sqrt{2}$ on $x=-1\pm\sqrt{k+1}$ in a complete method to find $k=\ldots$",
       r"A1 (AO 1.1b): So, $2\sqrt{k+1}=4\sqrt{2}\Rightarrow k=7$. Notes: Finds $k=7$ from correct solution only"],
      True, 22),

    # ---------------- Q12 ----------------
    e("12", "12", INT, "8.5, 5.6", 7, LATEX["12"],
      [r"M1 (AO 3.1a): Attempts this question by applying the substitution $u=1+\cos\theta$ and progresses as far as "
       r"achieving $\int\ldots\frac{(u-1)}{u}\ldots$ Notes: See scheme",
       r"M1 (AO 1.1b): $u=1+\cos\theta\Rightarrow\frac{\mathrm{d}u}{\mathrm{d}\theta}=-\sin\theta$ and "
       r"$\sin2\theta=2\sin\theta\cos\theta$. Notes: Attempts to differentiate $u=1+\cos\theta$ to give "
       r"$\frac{\mathrm{d}u}{\mathrm{d}\theta}=\ldots$ and applies $\sin2\theta=2\sin\theta\cos\theta$",
       r"A1 (AO 2.1): $\left\{\int\frac{\sin2\theta}{1+\cos\theta}\,\mathrm{d}\theta=\right\}\int\frac{2\sin\theta\cos\theta}"
       r"{1+\cos\theta}\,\mathrm{d}\theta=\int\frac{-2(u-1)}{u}\,\mathrm{d}u$. Notes: Applies $u=1+\cos\theta$ to show that "
       r"the integral becomes $\int\frac{-2(u-1)}{u}\,\mathrm{d}u$",
       r"M1 (AO 1.1b): $-2\int\left(1-\frac{1}{u}\right)\mathrm{d}u=-2(u-\ln u)$. Notes: Achieves an expression in $u$ that "
       r"can be directly integrated (e.g. dividing each term by $u$ or applying partial fractions) and integrates to give "
       r"an expression in $u$ of the form $\pm\lambda u\pm\mu\ln u$, $\lambda,\mu\neq0$",
       r"M1 (AO 1.1b): $-2\int\left(1-\frac{1}{u}\right)\mathrm{d}u=-2(u-\ln u)$. Notes: For integration in $u$ of the form "
       r"$\pm2(u-\ln u)$",
       r"M1 (AO 1.1b): $\left\{\int_0^{\frac{\pi}{2}}\frac{\sin2\theta}{1+\cos\theta}\,\mathrm{d}\theta=\right\}=-2\left[u-"
       r"\ln u\right]_2^1=-2((1-\ln1)-(2-\ln2))$. Notes: Applies $u$-limits of 1 and 2 to an expression of the form "
       r"$\pm\lambda u\pm\mu\ln u$, $\lambda,\mu\neq0$ and subtracts either way round",
       r"A1* (AO 2.1): $=-2(-1+\ln2)=2-2\ln2$ *. Notes: Applies $u$-limits the right way round, i.e. • "
       r"$\int_2^1\frac{-2(u-1)}{u}\,\mathrm{d}u=-2\int_2^1\left(1-\frac{1}{u}\right)\mathrm{d}u=-2\left[u-\ln u\right]_2^1="
       r"-2((1-\ln1)-(2-\ln2))$ • $\int_2^1\frac{-2(u-1)}{u}\,\mathrm{d}u=2\int_1^2\left(1-\frac{1}{u}\right)\mathrm{d}u="
       r"2\left[u-\ln u\right]_1^2=2((2-\ln2)-(1-\ln1))$ and correctly proves $\int_0^{\frac{\pi}{2}}\frac{\sin2\theta}"
       r"{1+\cos\theta}\,\mathrm{d}\theta=2-2\ln2$, with no errors seen",
       r"ALT: 12 Alt 1 — M1 (AO 3.1a): Attempts this question by applying the substitution $u=\cos\theta$ and progresses "
       r"as far as achieving $\int\ldots\frac{u}{u+1}\ldots$",
       r"ALT: 12 Alt 1 — M1 (AO 1.1b): $u=\cos\theta\Rightarrow\frac{\mathrm{d}u}{\mathrm{d}\theta}=-\sin\theta$ and "
       r"$\sin2\theta=2\sin\theta\cos\theta$",
       r"ALT: 12 Alt 1 — A1 (AO 2.1): $\int\frac{2\sin\theta\cos\theta}{1+\cos\theta}\,\mathrm{d}\theta=\int\frac{-2u}{u+1}\,"
       r"\mathrm{d}u$",
       r"ALT: 12 Alt 1 — M1 (AO 1.1b): $\left\{=-2\int\frac{(u+1)-1}{u+1}\,\mathrm{d}u=-2\int1-\frac{1}{u+1}\,\mathrm{d}u"
       r"\right\}=-2(u-\ln(u+1))$. Notes: Achieves an expression in $u$ that can be directly integrated (e.g. by applying "
       r"partial fractions or a substitution $v=u+1$) and integrates to give an expression in $u$ of the form "
       r"$\pm\lambda u\pm\mu\ln(u+1)$, $\lambda,\mu\neq0$ or $\pm\lambda v\pm\mu\ln v$, $\lambda,\mu\neq0$, where $v=u+1$",
       r"ALT: 12 Alt 1 — M1 (AO 1.1b): For integration in $u$ in the form $\pm2(u-\ln(u+1))$",
       r"ALT: 12 Alt 1 — M1 (AO 1.1b): $=-2\left[u-\ln(u+1)\right]_1^0=-2((0-\ln1)-(1-\ln2))$",
       r"ALT: 12 Alt 1 — A1* (AO 2.1): $=-2(-1+\ln2)=2-2\ln2$ *"],
      False, 24),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", TRIG, "5.6", 3, LATEX["13a"],
      [r"B1 (AO 1.1b): $R=2.5$. Notes: $R=2.5$ Condone $R=\sqrt{6.25}$",
       r"M1 (AO 1.1b): $\tan\alpha=\frac{1.5}{2}$ o.e. Notes: For either $\tan\alpha=\frac{1.5}{2}$ or "
       r"$\tan\alpha=-\frac{1.5}{2}$ or $\tan\alpha=\frac{2}{1.5}$ or $\tan\alpha=-\frac{2}{1.5}$",
       r"A1 (AO 1.1b): $\alpha=0.6435$, so $2.5\sin(\theta-0.6435)$. Notes: $\alpha=$ awrt 0.6435"],
      False, 26),
    e("13b", "13(b)", TRIG, "5.9", 1, LATEX["13b"],
      [r"B1 (AO 3.4): e.g. $D=6+2\sin\left(\frac{4\pi(0)}{25}\right)-1.5\cos\left(\frac{4\pi(0)}{25}\right)=4.5$m or "
       r"$D=6+2.5\sin\left(\frac{4\pi(0)}{25}-0.6435\right)=4.5$m. Notes: Uses Tom’s model to find $D=4.5$ (m) at 00:00 on "
       r"18th October 2017"],
      False, 26),
    e("13c", "13(c)", TRIG, "5.9, 5.6", 1, LATEX["13c"],
      [r"B1ft (AO 3.4): $D_{\max}=6+2.5=8.5$ m. Notes: Either 8.5 or follow through “6 + their $R$ ” (by using their $R$ "
       r"found in part (a))"],
      False, 26),
    e("13d", "13(d)", TRIG, "5.9, 5.7", 3, LATEX["13d"],
      [r"M1 (AO 1.1b): Sets $\frac{4\pi t}{25}-\text{“}0.6435\text{”}=\frac{5\pi}{2}$ or $\frac{\pi}{2}$. Notes: Realises "
       r"that $D=6+2\sin\left(\frac{4\pi t}{25}\right)-1.5\cos\left(\frac{4\pi t}{25}\right)=6+\text{“}2.5\text{”}\sin"
       r"\left(\frac{4\pi t}{25}-\text{“}0.6435\text{”}\right)$ and so maximum depth occurs when "
       r"$\sin\left(\frac{4\pi t}{25}-\text{“}0.6435\text{”}\right)=1\Rightarrow\frac{4\pi t}{25}-\text{“}0.6435\text{”}="
       r"\frac{\pi}{2}$ or $\frac{5\pi}{2}$",
       r"M1 (AO 3.1b): Afternoon solution $\Rightarrow\frac{4\pi t}{25}-\text{“}0.6435\text{”}=\frac{5\pi}{2}\Rightarrow "
       r"t=\frac{25}{4\pi}\left(\frac{5\pi}{2}+\text{“}0.6435\text{”}\right)$. Notes: Uses the model to deduce that a p.m. "
       r"solution occurs when $\frac{4\pi t}{25}-\text{“}0.6435\text{”}=\frac{5\pi}{2}$ and rearranges this equation to make "
       r"$t=\ldots$",
       r"A1 (AO 3.2a): $\Rightarrow t=16.9052\ldots\Rightarrow$ Time $=16:54$ or 4:54 pm. Notes: Finds that maximum depth "
       r"occurs in the afternoon at 16:54 or 4:54 pm",
       r"ALT: 13 (d) Alt 1 — M1 (AO 1.1b): Sets $\frac{4\pi t}{25}-\text{“}0.6435\text{”}=\frac{\pi}{2}$. Notes: Maximum "
       r"depth occurs when $\sin\left(\frac{4\pi t}{25}-\text{“}0.6435\text{”}\right)=1\Rightarrow\frac{4\pi t}{25}-"
       r"\text{“}0.6435\text{”}=\frac{\pi}{2}$",
       r"ALT: 13 (d) Alt 1 — M1 (AO 3.1b): Period $=2\pi\div\left(\frac{4\pi}{25}\right)=12.5$ Afternoon solution "
       r"$\Rightarrow t=12.5+\frac{25}{4\pi}\left(\frac{\pi}{2}+\text{“}0.6435\text{”}\right)$. Notes: Rearranges to make "
       r"$t=\ldots$ and adds on the period, where period $=2\pi\div\left(\frac{4\pi}{25}\right)\{=12.5\}$",
       r"ALT: 13 (d) Alt 1 — A1 (AO 3.2a): $\Rightarrow t=16.9052\ldots\Rightarrow$ Time $=16:54$ or 4:54 pm"],
      False, 26),
    e("13e", "13(e)", TRIG, "5.9, 2.11", 3, LATEX["13e"],
      [r"M1 (AO 3.4): (i) • An attempt to find the depth of water at 00:00 on 19th October 2017 for at least one of either "
       r"Tom’s model or Jolene’s model. Notes: See scheme",
       r"A1 (AO 3.5a): (i) • At 00:00 on 19th October 2017, Tom: $D=3.72\ldots$ m and Jolene: $H=4.5$ m and e.g. • As "
       r"$4.5\neq3.72$ then Jolene’s model is not true • Jolene’s model is not continuous at 00:00 on 19th October 2017 • "
       r"Jolene’s model does not continue on from where Tom’s model has ended. Notes: See scheme Note: Allow Special Case "
       r"M1 for a candidate who just states that Jolene’s model is not continuous at 00:00 on 19th October 2017 o.e.",
       r"B1 (AO 3.3): (ii) To make the model continuous, e.g. • $H=5.22+2\sin\left(\frac{4\pi x}{25}\right)-1.5\cos"
       r"\left(\frac{4\pi x}{25}\right)$, $0\leqslant x<24$ • $H=6+2\sin\left(\frac{4\pi(x+24)}{25}\right)-1.5\cos"
       r"\left(\frac{4\pi(x+24)}{25}\right)$, $0\leqslant x<24$. Notes: Uses the information to set up a new model for "
       r"$H$. (See scheme)"],
      False, 26),

    # ---------------- Q14 ----------------
    e("14", "14", COORD, "3.3, 5.6, 5.5", 5, LATEX["14"],
      [rf"M1 (AO 3.1a): $x=4\cos{PT}$, $y=2\sin t$ $x+y={COS}+2\sin t$. Notes: Looks ahead to the final result and uses "
       rf"the compound angle formula in a full attempt to write down an expression for $x+y$ which is in terms of $t$ "
       rf"only.",
       rf"M1 (AO 1.1b): $x+y={COS}+2\sin t$. Notes: Applies the compound angle formula on their term in $x$. E.g. "
       rf"$\cos{PT}\to\cos t\cos\left(\frac{{\pi}}{{6}}\right)\pm\sin t\sin\left(\frac{{\pi}}{{6}}\right)$",
       r"A1 (AO 1.1b): $x+y=2\sqrt{3}\cos t$. Notes: Uses correct algebra to find $x+y=2\sqrt{3}\cos t$",
       r"M1 (AO 3.1a): $\left(\frac{x+y}{2\sqrt{3}}\right)^2+\left(\frac{y}{2}\right)^2=1$. Notes: Complete strategy of "
       r"applying $\cos^2t+\sin^2t=1$ on a rearranged $x+y=\text{“}2\sqrt{3}\cos t\text{”}$, $y=2\sin t$ to achieve an "
       r"equation in $x$ and $y$ only",
       r"A1 (AO 2.1): $\frac{(x+y)^2}{12}+\frac{y^2}{4}=1$ $(x+y)^2+3y^2=12$. Notes: Correctly proves $(x+y)^2+ay^2=b$ with "
       r"both $a=3$, $b=12$, and no errors seen",
       rf"ALT: 14 Alt 1 — M1 (AO 3.1a): $(x+y)^2=\left(4\cos{PT}+2\sin t\right)^2$ $=\left({COS}+2\sin t\right)^2$. Notes: "
       rf"Apply in the same way as in the main scheme",
       rf"ALT: 14 Alt 1 — M1 (AO 1.1b): $=\left({COS}+2\sin t\right)^2$. Notes: Apply in the same way as in the main "
       rf"scheme",
       r"ALT: 14 Alt 1 — A1 (AO 1.1b): $=\left(2\sqrt{3}\cos t\right)^2$ or $12\cos^2t$. Notes: Uses correct algebra to "
       r"find $(x+y)^2=\left(2\sqrt{3}\cos t\right)^2$ or $(x+y)^2=12\cos^2t$",
       r"ALT: 14 Alt 1 — M1 (AO 3.1a): So, $(x+y)^2=12(1-\sin^2t)=12-12\sin^2t=12-12\left(\frac{y}{2}\right)^2$. Notes: "
       r"Complete strategy of applying $\cos^2t+\sin^2t=1$ on $(x+y)^2=\left(\text{“}2\sqrt{3}\cos t\text{”}\right)^2$ to "
       r"achieve an equation in $x$ and $y$ only",
       r"ALT: 14 Alt 1 — A1 (AO 2.1): $(x+y)^2+3y^2=12$. Notes: Correctly proves $(x+y)^2+ay^2=b$ with both $a=3$, "
       r"$b=12$, and no errors seen"],
      True, 30),
]

# No examiner report is published for the specimen paper, so there is nothing to apply.
W = None
REPORT = {}

# No report, so no difficulty can be judged: every part is (None, None).
RATINGS = {q: (None, None) for q in
           ["01a", "01b", "01c", "02a", "02b", "03a", "03b", "04a", "04b", "05a", "05b", "05c", "06a", "06b", "06c", "07",
            "08a", "08b", "09", "10a", "10b", "10c", "10d", "10e", "11a", "11b", "12", "13a", "13b", "13c", "13d", "13e",
            "14"]}


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
