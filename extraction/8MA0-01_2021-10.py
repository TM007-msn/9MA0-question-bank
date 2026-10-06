"""Draft builder for 8MA0-01 2021-10 (AS Pure, October/November 2021).

Run (from the project root, with the venv active):
    python extraction/8MA0-01_2021-10.py        # writes out/drafts/8MA0-01_2021-10.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-01_2021-10.json

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

P, S = "8MA0-01", "2021-10"
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

SHOW = (r"In this question you should show all stages of your working. Solutions relying on calculator technology "
        r"are not acceptable. ")

# Shared stems go in variables so each part's question_latex stands alone.
Q4 = (r"[In this question the unit vectors $\mathbf{i}$ and $\mathbf{j}$ are due east and due north respectively.] "
      r"A stone slides horizontally across ice. Initially the stone is at the point $A(-24\mathbf{i}-10\mathbf{j})$ m "
      r"relative to a fixed point $O$. After 4 seconds the stone is at the point $B(12\mathbf{i}+5\mathbf{j})$ m "
      r"relative to the fixed point $O$. The motion of the stone is modelled as that of a particle moving in a "
      r"straight line at constant speed. Using the model, ")
FIG1 = (r"[Figure 1: part of the curve $y=3x^2-2$, a U-shaped parabola with its minimum on the $y$-axis just below "
        r"$O$; the point $P(2, 10)$ is marked on the right-hand branch, with the point $Q$ above it on the same "
        r"branch.]" "\n")
Q5 = FIG1 + r"Figure 1 shows part of the curve with equation $y=3x^2-2$ The point $P(2, 10)$ lies on the curve. "
Q5B = r"The point $Q$ with $x$ coordinate $2+h$ also lies on the curve. "
Q6A = r"(a) Using algebra, find all solutions of the equation $$3x^3-17x^2-6x=0$$ "
Q7 = (r"A parallelogram $PQRS$ has area 50 cm$^2$ Given: $PQ$ has length 14 cm; $QR$ has length 7 cm; angle $SPQ$ is "
      r"obtuse, find ")
Q8 = (r"$$\mathrm{g}(x)=(2+ax)^8\qquad\text{where }a\text{ is a constant}$$ Given that one of the terms in the binomial "
      r"expansion of $\mathrm{g}(x)$ is $3402x^5$ ")
Q10 = r"A student is investigating the following statement about natural numbers. “$n^3-n$ is a multiple of 4” "
Q11 = (r"The owners of a nature reserve decided to increase the area of the reserve covered by trees. Tree planting "
       r"started on 1st January 2005. The area of the nature reserve covered by trees, $A$ km$^2$, is modelled by the "
       r"equation $$A=80-45\mathrm{e}^{ct}$$ where $c$ is a constant and $t$ is the number of years after 1st January "
       r"2005. Using the model, ")
Q11B = r"On 1st January 2019 an area of 60 km$^2$ of the nature reserve was covered by trees. "
Q12 = (r"In this question you should show all stages of your working. Solutions relying entirely on calculator "
       r"technology are not acceptable. ")
FIG2 = (r"[Figure 2: a straight line on axes $\log_{10}m$ (horizontal) and $\log_{10}h$ (vertical), meeting the "
        r"$\log_{10}h$ axis at 2.25 and sloping downwards to the right.]" "\n")
Q13 = (FIG2 + r"The resting heart rate, $h$, of a mammal, measured in beats per minute, is modelled by the equation "
       r"$$h=pm^q$$ where $p$ and $q$ are constants and $m$ is the mass of the mammal measured in kg. Figure 2 "
       r"illustrates the linear relationship between $\log_{10}h$ and $\log_{10}m$ The line meets the vertical "
       r"$\log_{10}h$ axis at 2.25 and has a gradient of $-0.235$ ")
Q14 = r"A curve $C$ has equation $y=\mathrm{f}(x)$ where $$\mathrm{f}(x)=-3x^2+12x+8$$ "
FIG3 = (r"[Figure 3: sketch of the curve $C$, an inverted parabola crossing the positive $y$-axis and both sides of "
        r"the $x$-axis, with maximum point $M$ to the right of the $y$-axis; the horizontal line $l$ through $M$; the "
        r"region $R$ between $C$, $l$ and the $y$-axis is shaded.]" "\n")
FIG4 = (r"[Figure 4: circle $C$ with centre $N$ in the first quadrant, and the line $l$ through $O$ touching $C$ at the "
        r"point $P$, below and to the right of $N$.]" "\n")
Q15 = (FIG4 + r"Figure 4 shows a sketch of a circle $C$ with centre $N(7, 4)$ The line $l$ with equation $y=\frac{1}{3}x$ "
       r"is a tangent to $C$ at the point $P$. Find ")
Q16 = (r"The curve $C$ has equation $y=\mathrm{f}(x)$ where $$\mathrm{f}(x)=ax^3+15x^2-39x+b$$ and $a$ and $b$ are "
       r"constants. Given: the point $(2, 10)$ lies on $C$; the gradient of the curve at $(2, 10)$ is $-3$ ")
Q16A = r"(a) (i) show that the value of $a$ is $-2$ (ii) find the value of $b$. "
Q16C = r"(c) Write $\mathrm{f}(x)$ in the form $(x-4)\mathrm{Q}(x)$ where $\mathrm{Q}(x)$ is a quadratic expression to be found. "

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", ALG, "2.5", 3,
      SHOW + r"Using algebra, solve the inequality $$x^2-x>20$$ writing your answer in set notation.",
      [r"M1 (AO 1.1b): Finds critical values $x^2-x>20\Rightarrow x^2-x-20>0\Rightarrow x=(5,-4)$. Notes: Attempts to "
       r"find the critical values using an algebraic method. Condone slips but an allowable method should be used and "
       r"two critical values should be found",
       r"M1 (AO 1.1b): Chooses outside region for their values Eg. $x>5$, $x<-4$. Notes: Chooses the outside region for "
       r"their critical values. This may appear in incorrect inequalities such as $5<x<-4$",
       r"A1 (AO 2.5): Presents solution in set notation $\{x:x<-4\}\cup\{x:x>5\}$ oe. Notes: Presents in set notation as "
       r"required $\{x:x<-4\}\cup\{x:x>5\}$ Accept $\{x<-4\cup x>5\}$. Do not accept $\{x<-4, x>5\}$. Note: If there is "
       r"a contradiction of their solution on different lines of working do not penalise intermediate working and mark "
       r"what appears to be their final answer."],
      False, 2),

    # ---------------- Q2 ----------------
    e("02", "2", ALG, "2.1", 3,
      SHOW + r"Given $$\frac{9^{x-1}}{3^{y+2}}=81$$ express $y$ in terms of $x$, writing your answer in simplest form.",
      [r"M1 (AO 1.1b): $\frac{9^{x-1}}{3^{y+2}}=81\Rightarrow\frac{3^{2x-2}}{3^{y+2}}=3^4$ or "
       r"$\frac{9^{x-1}}{3^{y+2}}=81\Rightarrow\frac{9^{x-1}}{9^{\frac{1}{2}(y+2)}}=9^2$. Notes: Attempts to set $9^{x-1}$ "
       r"and 81 as powers of 3. Condone $9^{x-1}=3^{2x-1}$ and $9^{x-1}=3^{3x-3}$.",
       r"dM1 (AO 1.1b): $\Rightarrow2x-2-y-2=4\Rightarrow y=$ or $\Rightarrow x-1-\frac{1}{2}y-1=2\Rightarrow y=$. Notes: "
       r"Attempts to use the addition (or subtraction) index law, or laws or logarithms, correctly and rearranges the "
       r"equation to reach $y$ in terms of $x$. Condone slips in their rearrangement.",
       r"A1 (AO 1.1b): $\Rightarrow y=2x-8$. Notes: $y=2x-8$",
       r"ALT: Alt — M1 (AO 1.1b): Eg. $\log_3\left(\frac{9^{x-1}}{3^{y+2}}\right)=\log_381$. Notes: Alternatively attempts "
       r"to write each term as a logarithm of base 3 or 9. You must see the base written to award this mark.",
       r"ALT: Alt — dM1 (AO 1.1b): $\Rightarrow(x-1)\log_3(9^{x-1})-(y+2)\log_3(3^{y+2})=4\Rightarrow2(x-1)-y-2=4"
       r"\Rightarrow y=$",
       r"ALT: Alt — A1 (AO 1.1b): $\Rightarrow y=2x-8$"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03", "3", INT, "8.2, 2.1", 4,
      r"Find $$\int\frac{3x^4-4}{2x^3}\,\mathrm{d}x$$ writing your answer in simplest form.",
      [r"M1 (AO 1.1b): $\int\frac{3x^4-4}{2x^3}\,\mathrm{d}x=\int\frac{3}{2}x-2x^{-3}\,\mathrm{d}x$. Notes: Attempts to "
       r"divide to form a sum of terms. Implied by two terms with one correct index. "
       r"$\int\frac{3x^4}{2x^3}-\frac{4}{2x^3}\,\mathrm{d}x$ scores this mark.",
       r"A1 (AO 1.1b): $\int\frac{3x^4-4}{2x^3}\,\mathrm{d}x=\int\frac{3}{2}x-2x^{-3}\,\mathrm{d}x$. Notes: "
       r"$\int\frac{3}{2}x-2x^{-3}\,\mathrm{d}x$ o.e such as $\frac{1}{2}\int(3x-4x^{-3})\,\mathrm{d}x$. The indices must "
       r"have been processed on both terms. Condone spurious notation or lack of the integral sign for this mark.",
       r"dM1 (AO 3.1a): $=\frac{3}{2}\times\frac{x^2}{2}-2\times\frac{x^{-2}}{-2}\,(+c)$. Notes: For the full strategy to "
       r"integrate the expression. It requires two terms with one correct index. Look for $=ax^p+bx^q$ where $p=2$ or "
       r"$q=-2$",
       r"A1 (AO 1.1b): $=\frac{3}{4}x^2+\frac{1}{x^2}+c$ o.e. Notes: Correct answer $\frac{3}{4}x^2+\frac{1}{x^2}+c$ "
       r"o.e. such as $\frac{3}{4}x^2+x^{-2}+c$"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", VEC, "9.3, 9.4", 2, Q4 + r"prove that the stone passes through $O$,",
      [r"M1 (AO 1.1b): Attempts to compare the two position vectors. Allow an attempt using two of "
       r"$\overrightarrow{AO}$, $\overrightarrow{OB}$ or $\overrightarrow{AB}$ E.g. "
       r"$(-24\mathbf{i}-10\mathbf{j})=-2\times(12\mathbf{i}+5\mathbf{j})$. Notes: Attempts to compare the two position "
       r"vectors. Allow an attempt using two of $\overrightarrow{AO}$, $\overrightarrow{OB}$ or $\overrightarrow{AB}$ "
       r"either way around. E.g. States that $(-24\mathbf{i}-10\mathbf{j})=-2\times(12\mathbf{i}+5\mathbf{j})$",
       r"A1 (AO 2.4): Explains that as $\overrightarrow{AO}$ is parallel to $\overrightarrow{OB}$ (and the stone is "
       r"travelling in a straight line) the stone passes through the point $O$. Notes: States that as "
       r"$\overrightarrow{AO}$ is parallel to $\overrightarrow{OB}$ or as $AO$ is parallel to $OB$ (and the stone is "
       r"travelling in a straight line) the stone passes through the point $O$.",
       r"ALT: Alt(a) — M1 (AO 1.1b): Attempts to find the equation of the line which passes through $A$ and $B$ E.g. "
       r"$y-5=\frac{5+10}{12+24}(x-12)$ $\left(y=\frac{5}{12}x\right)$. Notes: Alternatively attempts to find the "
       r"equation of the line through $A$ and $B$ proceeding as far as $y=\ldots x$ Condone sign slips.",
       r"ALT: Alt(a) — A1 (AO 2.4): Shows that when $x=0$, $y=0$ and concludes the stone passes through the point $O$. "
       r"Notes: Alternatively, shows that the point $(0,0)$ is on the line and concludes (the stone) passes through the "
       r"point $O$.",
       r"ALT: Alternatively (a), gradients — M1 (AO 1.1b): Alternatively, allow an attempt finding the gradient using "
       r"any two of $AO$, $OB$ or $AB$"],
      False, 8),
    e("04b", "4(b)", VEC, "9.4, 9.5", 3, Q4 + r"calculate the speed of the stone.",
      [r"M1 (AO 1.1b): Attempts distance $AB=\sqrt{(12+24)^2+(10+5)^2}$. Notes: Attempts to find the distance $AB$ using "
       r"a correct method. Condone slips but expect to see an attempt at $\sqrt{a^2+b^2}$ where $a$ or $b$ is correct",
       r"dM1 (AO 3.1a): Attempts speed $=\frac{\sqrt{(12+24)^2+(10+5)^2}}{4}$. Notes: Dependent upon the previous mark. "
       r"Look for an attempt at $\frac{\text{distance }AB}{4}$",
       r"A1 (AO 3.2a): Speed $=9.75$ ms$^{-1}$. Notes: 9.75 ms$^{-1}$ Requires units"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", DIFF, "7.3, 7.2", 2, Q5 + r"Find the gradient of the tangent to the curve at $P$.",
      [r"M1 (AO 1.1b): Attempts to find the value of $\frac{\mathrm{d}y}{\mathrm{d}x}$ at $x=2$. Notes: Attempts to "
       r"differentiate, allow $3x^2-2\to\ldots x$ and substitutes $x=2$ into their answer",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}y}{\mathrm{d}x}=6x\Rightarrow$ gradient of tangent at $P$ is 12. Notes: cso "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}=6x\Rightarrow$ gradient of tangent at $P$ is 12"],
      True, 10),
    e("05b", "5(b)", DIFF, "7.1", 3,
      Q5 + Q5B + r"Find the gradient of the line $PQ$, giving your answer in terms of $h$ in simplest form.",
      [r"B1 (AO 1.1b): Gradient $PQ=\frac{3(2+h)^2-2-10}{(2+h)-2}$ oe. Notes: Correct expression for the gradient of the "
       r"chord seen or implied.",
       r"M1 (AO 1.1b): $=\frac{3(2+h)^2-12}{(2+h)-2}=\frac{12h+3h^2}{h}$. Notes: Attempts $\frac{\delta y}{\delta x}$, "
       r"condoning slips, and attempts to simplify the numerator. The denominator must be $h$",
       r"A1 (AO 2.1): $=12+3h$. Notes: cso $12+3h$"],
      True, 10),
    e("05c", "5(c)", DIFF, "7.1", 1,
      Q5 + r"(a) Find the gradient of the tangent to the curve at $P$. " + Q5B + r"(b) Find the gradient of the line "
      r"$PQ$, giving your answer in terms of $h$ in simplest form. (c) Explain briefly the relationship between part (b) "
      r"and the answer to part (a).",
      [r"B1 (AO 2.4): Explains that as $h\to0$, $12+3h\to12$ and states that the gradient of the chord tends to the "
       r"gradient of (the tangent to) the curve. Notes: Explains that as $h\to0$, $12+3h\to12$ and states that the "
       r"gradient of the chord tends to the gradient of the curve"],
      True, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", ALG, "2.6, 2.3", 3, SHOW + Q6A,
      [r"M1 (AO 1.1a): $3x^3-17x^2-6x=0\Rightarrow x(3x^2-17x-6)=0$. Notes: Factorises out or cancels by $x$ to form a "
       r"quadratic equation.",
       r"dM1 (AO 1.1b): $\Rightarrow x(3x+1)(x-6)=0$. Notes: Scored for an attempt to find $x$. May be awarded for "
       r"factorisation of the quadratic or use of the quadratic formula.",
       r"A1 (AO 1.1b): $\Rightarrow x=0,-\frac{1}{3},6$. Notes: $x=0,-\frac{1}{3},6$ and no extras"],
      False, 12),
    e("06b", "6(b)", ALG, "2.6, 2.3", 3,
      SHOW + Q6A + r"(b) Hence find all real solutions of $$3(y-2)^6-17(y-2)^4-6(y-2)^2=0$$",
      [r"M1 (AO 2.2a): Attempts to solve $(y-2)^2=n$ where $n$ is any solution $\geqslant0$ to (a). Notes: Attempts to "
       r"solve $(y-2)^2=n$ where $n$ is any solution $\geqslant0$ to (a). At least one stage of working must be seen to "
       r"award this mark. Eg $(y-2)^2=0\Rightarrow y=2$",
       r"A1ft (AO 1.1b): Two of $2, 2\pm\sqrt{6}$. Notes: Two of $2, 2\pm\sqrt{6}$ but follow through on "
       r"$(y-2)^2=n\Rightarrow y=2\pm\sqrt{n}$ where $n$ is a positive solution to part (a). (Provided M1 has been scored)",
       r"A1 (AO 2.1): All three of $2, 2\pm\sqrt{6}$. Notes: All three of $2, 2\pm\sqrt{6}$ and no extra solutions. "
       r"(Provided M1A1 has been scored)"],
      False, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", TRIG, "5.1", 3, Q7 + r"the size of angle $SPQ$, in degrees, to 2 decimal places,",
      [r"B1 (AO 1.2): Sets $50=7\times14\sin(SPQ)$ oe. Notes: Sets $50=7\times14\sin(SPQ)$ oe",
       r"M1 (AO 1.1b): Finds $180^\circ-\arcsin\left(\text{\"}\frac{50}{98}\text{\"}\right)$. Notes: Attempts the correct "
       r"method of finding obtuse $\angle SPQ$. See scheme.",
       r"A1 (AO 1.1b): $=149.32^\circ$. Notes: awrt $149.32^\circ$",
       r"ALT: Alt(a) (with a diagram of the parallelogram $PQRS$, $PS=7$, $PQ=14$, and heights $h$ from $S$ to $PQ$ and "
       r"$h_1$ from $P$ to $QR$) — B1 (AO 1.2): States or uses $14h=50$ or $7h_1=50$",
       r"ALT: Alt(a) — M1 (AO 1.1b): Full method to find obtuse $\angle SPQ$. In this case it is "
       r"$90^\circ+\arccos\left(\frac{h}{7}\right)$ or $90^\circ+\arccos\left(\frac{h_1}{14}\right)$",
       r"ALT: Alt(a) — A1 (AO 1.1b): awrt $149.32^\circ$"],
      False, 14),
    e("07b", "7(b)", TRIG, "5.1", 2, Q7 + r"the length of the diagonal $SQ$, in cm, to one decimal place.",
      [r"M1 (AO 1.1b): Method of finding $SQ$: $SQ^2=14^2+7^2-2\times14\times7\cos\text{\"}149.32\text{\"}$. Notes: A "
       r"correct method of finding $SQ$ using their $\angle SPQ$. $SQ^2=14^2+7^2-2\times14\times7\cos\text{\"}149.32"
       r"\text{\"}$ scores this mark.",
       r"A1 (AO 1.1b): $=20.3$ cm. Notes: awrt 20.3 cm (condone lack of units)"],
      False, 14),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", SEQ, "4.1", 4, Q8 + r"find the value of $a$.",
      [r"M1 (AO 1.1a): $(2+ax)^8$ Attempts the term in $x^5={}^8C_5\,2^3(ax)^5=448a^5x^5$. Notes: An attempt at selecting "
       r"the correct term of the binomial expansion. If all terms are given then the correct term must be used. Allow "
       r"with a missing bracket ${}^8C_5\,2^3ax^5$ and left without the binomial coefficient expanded",
       r"A1 (AO 1.1b): $448a^5x^5$. Notes: $448a^5x^5$ Allow unsimplified but ${}^8C_5$ must be \"numerical\"",
       r"M1 (AO 1.1b): Sets $448a^5=3402\Rightarrow a^5=\frac{243}{32}$. Notes: Sets their $448a^5=3402$ and proceeds to "
       r"$\Rightarrow a^k=\ldots$ where $k\in\mathbb{N}$ $k\neq1$",
       r"A1 (AO 1.1b): $\Rightarrow a=\frac{3}{2}$. Notes: Correct work leading to $a=\frac{3}{2}$"],
      False, 16),
    e("08b", "8(b)", SEQ, "4.1", 3,
      Q8 + r"(a) find the value of $a$. Using this value of $a$, (b) find the constant term in the expansion of "
      r"$$\left(1+\frac{1}{x^4}\right)(2+ax)^8$$",
      [r"M1 (AO 1.1b): Attempts either term. So allow for $2^8$ or ${}^8C_4\,2^4a^4$. Notes: Finds either term required. "
       r"So allow for $2^8$ or ${}^8C_4\,2^4a^4$ (even allowing with $a$)",
       r"dM1 (AO 2.1): Attempts the sum of both terms $2^8+{}^8C_4\,2^4a^4$. Notes: Attempts the sum of both terms "
       r"$2^8+{}^8C_4\,2^4a^4$",
       r"A1 (AO 1.1b): $=256+5670=5926$. Notes: cso 5926"],
      False, 16),

    # ---------------- Q9 ----------------
    e("09", "9", INT, "8.3, 8.2, 2.1", 4,
      r"Find the value of the constant $k$, $0<k<9$, such that $$\int_k^9\frac{6}{\sqrt{x}}\,\mathrm{d}x=20$$",
      [r"M1 (AO 1.1b): $\int_k^9\frac{6}{\sqrt{x}}\,\mathrm{d}x=\left[ax^{\frac{1}{2}}\right]_k^9=20\Rightarrow"
       r"36-12\sqrt{k}=20$. Notes: For setting $\left[ax^{\frac{1}{2}}\right]_k^9=20$",
       r"A1 (AO 1.1b): $36-12\sqrt{k}=20$. Notes: A correct equation involving p Eg. $36-12\sqrt{k}=20$",
       r"dM1 (AO 3.1a): Correct method of solving Eg. $36-12\sqrt{k}=20\Rightarrow k=$. Notes: For a whole strategy to "
       r"find $k$. In the scheme it is awarded for setting $\left[ax^{\frac{1}{2}}\right]_k^9=20$, using both limits and "
       r"proceeding using correct index work to find $k$. It cannot be scored if $k^{\frac{1}{2}}<0$",
       r"A1 (AO 1.1b): $\Rightarrow k=\frac{16}{9}$ oe. Notes: $k=\frac{16}{9}$"],
      False, 18),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", PROOF, "1.1", 4, Q10 + r"Prove, using algebra, that the statement is true for all odd numbers.",
      [r"B1 (AO 3.1a): Selects a correct strategy. E.g uses an odd number is $2k\pm1$. Notes: Note: May be in any "
       r"variable (condone use of $n$). Selects a correct strategy. E.g uses an odd number is $2k\pm1$",
       r"M1 (AO 2.1): Attempts to simplify $(2k\pm1)^3-(2k\pm1)=\ldots$ Notes: Attempts $(2k\pm1)^3-(2k\pm1)=\ldots$ "
       r"Condone errors in multiplying out the brackets and invisible brackets for this mark. Either the coefficient of "
       r"the $k$ term or the constant of $(2k\pm1)^3$ must have changed from attempting to simplify.",
       r"dM1 (AO 1.1b): ...and factorise $8k^3\pm12k^2\pm4k=4k(2k^2\pm3k\pm1)=$. Notes: Attempts to take a factor of 4 "
       r"or $4k$ from their cubic",
       r"A1 (AO 2.4): Correct work with statement $4\times\ldots$ is a multiple of 4. Notes: Correct work with statement "
       r"$4\times\ldots$ is a multiple of 4",
       r"ALT: Alt (a) — B1 (AO 3.1a): Selects a correct strategy. Factorises $k^3-k=k(k-1)(k+1)$",
       r"ALT: Alt (a) — M1 (AO 2.1): States that if $k$ is odd then both $k-1$ and $k+1$ are even",
       r"ALT: Alt (a) — dM1 (AO 1.1b): States that $k-1$ multiplied by $k+1$ is therefore a multiple of 4",
       r"ALT: Alt (a) — A1 (AO 2.4): Concludes that $k^3-k$ is a multiple of 4 as it is odd $\times$ multiple of 4"],
      False, 20),
    e("10b", "10(b)", PROOF, "1.1", 1, Q10 + r"Use a counterexample to show that the statement is not always true.",
      [r"B1 (AO 2.4): Any counter example with correct statement. Eg. $2^3-2=6$ which is not a multiple of 4. Notes: Any "
       r"counter example with correct statement."],
      False, 20),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", EXP, "6.7", 1,
      Q11 + r"find the area of the nature reserve that was covered by trees just before tree planting started.",
      [r"B1 (AO 3.4): 35 (km$^2$). Notes: Uses the equation of the model to find that 35 (km$^2$) of the reserve was "
       r"covered on 1st January 2005. Do not accept eg. 35 m$^2$"],
      False, 24),
    e("11b", "11(b)", EXP, "6.7, 6.3", 4,
      Q11 + Q11B + r"Use this information to find a complete equation for the model, giving your value of $c$ to 3 "
      r"significant figures.",
      [r"M1 (AO 1.1b): Sets their $60=80-45\mathrm{e}^{14c}\Rightarrow45\mathrm{e}^{14c}=20$. Notes: Sets their "
       r"$60=80-45\mathrm{e}^{14c}\Rightarrow A\mathrm{e}^{14c}=B$",
       r"A1 (AO 1.1b): $45\mathrm{e}^{14c}=20$. Notes: $45\mathrm{e}^{14c}=20$ or equivalent.",
       r"dM1 (AO 3.1b): $\Rightarrow c=\frac{1}{14}\ln\left(\frac{20}{45}\right)=\cdots-0.0579$. Notes: A full and careful "
       r"method using precise algebra, correct log laws and a knowledge that $\mathrm{e}^x$ and $\ln x$ are inverse "
       r"functions and proceeds to a value for $c$.",
       r"A1 (AO 3.3): $A=80-45\mathrm{e}^{-0.0579t}$. Notes: Gives a complete equation for the model "
       r"$A=80-45\mathrm{e}^{-0.0579t}$"],
      False, 24),
    e("11c", "11(c)", EXP, "6.7", 1,
      Q11 + Q11B + r"On 1st January 2020, the owners of the nature reserve announced a long-term plan to have 100 km$^2$ "
      r"of the nature reserve covered by trees. State a reason why the model is not appropriate for this plan.",
      [r"B1 (AO 3.5b): Gives a suitable answer: The maximum area covered by trees is only 80 km$^2$; The \"80\" would need "
       r"to be \"100\"; Substitutes 100 into the equation of the model and shows that the formula fails with a reason eg. "
       r"you cannot take a log of a negative number. Notes: Gives a suitable interpretation (See scheme)"],
      False, 24),

    # ---------------- Q12 ----------------
    e("12i", "12(i)", TRIG, "5.4, 5.3", 5,
      Q12 + r"Solve, for $0<\theta\leqslant450^\circ$, the equation $$5\cos^2\theta=6\sin\theta$$ giving your answers to "
      r"one decimal place.",
      [r"M1 (AO 1.2): Uses $\cos^2\theta=1-\sin^2\theta$: $5\cos^2\theta=6\sin\theta\Rightarrow5\sin^2\theta+6\sin\theta"
       r"-5=0$. Notes: Uses $\cos^2\theta=1-\sin^2\theta$ to form a 3TQ in $\sin\theta$",
       r"A1 (AO 1.1b): $5\sin^2\theta+6\sin\theta-5=0$. Notes: Correct 3TQ=0 $5\sin^2\theta+6\sin\theta-5=0$",
       r"dM1 (AO 3.1a): $\Rightarrow\sin\theta=\frac{-3+\sqrt{34}}{5}\Rightarrow\theta=\ldots$ Notes: Solves their 3TQ in "
       r"$\sin\theta$ to produce one value for $\theta$. It is dependent upon having used $\cos^2\theta=\pm1\pm"
       r"\sin^2\theta$",
       r"A1 (AO 1.1b): $\Rightarrow\theta=34.5^\circ,145.5^\circ,394.5^\circ$. Notes: Two of awrt "
       r"$\theta=34.5^\circ,145.5^\circ,394.5^\circ$ (or if in radians two of awrt 0.60, 2.54, 6.89)",
       r"A1 (AO 1.1b): $\Rightarrow\theta=34.5^\circ,145.5^\circ,394.5^\circ$. Notes: All three of awrt "
       r"$\theta=34.5^\circ,145.5^\circ,394.5^\circ$ and no other values"],
      False, 26),
    e("12iia", "12(ii)(a)", TRIG, "5.4, 5.3", 2,
      Q12 + r"A student’s attempt to solve the question “Solve, for $-90^\circ<x<90^\circ$, the equation "
      r"$3\tan x-5\sin x=0$” is set out below. "
      r"$$\begin{aligned}3\tan x-5\sin x&=0\\3\frac{\sin x}{\cos x}-5\sin x&=0\\3\sin x-5\sin x\cos x&=0\\"
      r"3-5\cos x&=0\\\cos x&=\frac{3}{5}\\x&=53.1^\circ\end{aligned}$$ "
      r"Identify two errors or omissions made by this student, giving a brief explanation of each.",
      [r"B1 (AO 2.3): One of: They cancel by $\sin x$ (and hence they miss the solution $\sin x=0\Rightarrow x=0$); They "
       r"do not find all the solutions of $\cos x=\frac{3}{5}$ (in the given range) or they missed the solution "
       r"$x=-53.1^\circ$. Notes: See scheme",
       r"B1 (AO 2.3): Both of the above. Notes: See scheme"],
      False, 26),
    e("12iib", "12(ii)(b)", TRIG, "5.4, 5.2", 2,
      Q12 + r"The first four positive solutions, in order of size, of the equation "
      r"$$\cos(5\alpha+40^\circ)=\frac{3}{5}$$ are $\alpha_1$, $\alpha_2$, $\alpha_3$ and $\alpha_4$ Find, to the nearest "
      r"degree, the value of $\alpha_4$",
      [r"M1 (AO 3.1a): Sets $5\alpha+40^\circ=720^\circ-53.1^\circ$. Notes: Sets $5\alpha+40^\circ=666.9^\circ$ o.e.",
       r"A1 (AO 1.1b): $\alpha=125^\circ$. Notes: awrt $\alpha=125^\circ$"],
      False, 26),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", EXP, "6.6, 6.4", 3, Q13 + r"Find, to 3 significant figures, the value of $p$ and the value of $q$.",
      [r"M1 (AO 1.1b): $\log_{10}h=2.25-0.235\log_{10}m\Rightarrow h=10^{2.25-0.235\log_{10}m}\Rightarrow"
       r"h=10^{2.25}\times m^{-0.235}$. Notes: Establishes a link between $h=pm^q$ and $\log_{10}h=2.25-0.235\log_{10}m$. "
       r"May be implied by a correct equation in $p$ or $q$",
       r"A1 (AO 1.1b): Either one of $p=10^{2.25}$, $q=-0.235$. Notes: For a correct equation in $p$ or $q$",
       r"A1 (AO 2.2a): $\Rightarrow p=178$ and $q=-0.235$. Notes: $p=178$ and $q=-0.235$",
       r"ALT: Second scheme column — M1 (AO 1.1b): $h=pm^q\Rightarrow\log_{10}h=\log_{10}p+\log_{10}m^q\Rightarrow"
       r"\log_{10}h=\log_{10}p+q\log_{10}m$",
       r"ALT: Second scheme column — A1 (AO 1.1b): Or either one of $\log_{10}p=2.25$, $q=-0.235$"],
      True, 30),
    e("13b", "13(b)", EXP, "6.7, 6.6", 3,
      Q13 + r"(a) Find, to 3 significant figures, the value of $p$ and the value of $q$. A particular mammal has a mass "
      r"of 5 kg and a resting heart rate of 119 beats per minute. (b) Comment on the suitability of the model for this "
      r"mammal.",
      [r"M1 (AO 3.1b): $h=\text{\"}178\text{\"}\times5^{\text{\"}-0.235\text{\"}}$. Notes: Uses either model to set up an "
       r"equation in $h$ (or $m$)",
       r"A1 (AO 1.1b): $h=122$. Notes: $h=$ awrt 122. Condone $h=$ awrt 122 bpm",
       r"A1ft (AO 3.2b): Reasonably accurate (to 2 sf) so suitable. Notes: Comments on the suitability of the model. "
       r"Follow through on their answer. Requires a comment consistent with their answer from using the model. E.g. It "
       r"is a suitable model as it is only “3” bpm away from the real value ✓ Do not allow an argument stating that it "
       r"should be the same. It is an unsuitable model as “122” bpm is not equal to 119 bpm ✗",
       r"ALT: Second scheme column — M1 (AO 3.1b): $\log_{10}h=\text{\"}2.25\text{\"}-\text{\"}0.235\text{\"}\log_{10}5$",
       r"ALT: Second scheme column — A1 (AO 1.1b): $h=122$"],
      True, 30),
    e("13c", "13(c)", EXP, "6.7", 1, Q13 + r"With reference to the model, interpret the value of the constant $p$.",
      [r"B1 (AO 3.4): \"$p$\" would be the (resting) heart rate (in bpm) of a mammal with a mass of 1 kg. Notes: \"$p$\" "
       r"would be the (resting) heart rate of a mammal with a mass of 1 kg"],
      True, 30),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", ALG, "2.3", 3,
      Q14 + r"Write $\mathrm{f}(x)$ in the form $$a(x+b)^2+c$$ where $a$, $b$ and $c$ are constants to be found.",
      [r"M1 (AO 1.1b): $\mathrm{f}(x)=-3x^2+12x+8=-3(x\pm2)^2+\ldots$ Notes: Attempts to take out a common factor and "
       r"complete the square. Award for $-3(x\pm2)^2+\ldots$",
       r"A1 (AO 1.1b): $=-3(x-2)^2+\ldots$ Notes: Proceeds to a form $-3(x-2)^2+\ldots$",
       r"A1 (AO 1.1b): $=-3(x-2)^2+20$. Notes: $-3(x-2)^2+20$",
       r"ALT: Alternatively (a), comparing coefficients — M1 (AO 1.1b): Alternatively attempt to compare $-3x^2+12x+8$ "
       r"to $ax^2+2abx+ab^2+c$ to find values of a and b",
       r"ALT: Alternatively (a), comparing coefficients — A1 (AO 1.1b): or via comparison finds $a=-3, b=-2$"],
      False, 34),
    e("14b", "14(b)", ALG, "2.3", 2,
      Q14 + r"(a) Write $\mathrm{f}(x)$ in the form $a(x+b)^2+c$ where $a$, $b$ and $c$ are constants to be found. "
      r"The curve $C$ has a maximum turning point at $M$. (b) Find the coordinates of $M$.",
      [r"B1ft (AO 1.1b): Coordinates of $M=(2,20)$. Notes: One correct coordinate",
       r"B1ft (AO 2.2a): Coordinates of $M=(2,20)$. Notes: Correct coordinates. Allow as $x=\ldots, y=\ldots$ Follow "
       r"through on their $(-b,c)$"],
      False, 34),
    e("14c", "14(c)", INT, "8.3, 8.2", 5,
      Q14 + r"The curve $C$ has a maximum turning point at $M$. " + FIG3 + r"Figure 3 shows a sketch of the curve $C$. "
      r"The line $l$ passes through $M$ and is parallel to the $x$-axis. The region $R$, shown shaded in Figure 3, is "
      r"bounded by $C$, $l$ and the $y$-axis. Using algebraic integration, find the area of $R$.",
      [r"M1 (AO 1.1b): $\int-3x^2+12x+8\,\mathrm{d}x=-x^3+6x^2+8x$. Notes: Attempts to integrate. Award for any correct "
       r"index",
       r"A1 (AO 1.1b): $\int-3x^2+12x+8\,\mathrm{d}x=-x^3+6x^2+8x$. Notes: $\int-3x^2+12x+8\,\mathrm{d}x=-x^3+6x^2+8x"
       r"\,(+c)$ (which may be unsimplified)",
       r"M1 (AO 3.1a): Method to find $R=$ their $2\times20-\int_0^2(-3x^2+12x+8)\,\mathrm{d}x$. Notes: Method to find "
       r"area of $R$. Look for their $2\times\text{\"}20\text{\"}-\int_0^{\text{\"}2\text{\"}}\mathrm{f}(x)\,\mathrm{d}x$",
       r"dM1 (AO 1.1b): $R=40-\left[-2^3+24+16\right]$. Notes: Correct application of limits on their integrated "
       r"function. Their 2 must be used",
       r"A1 (AO 1.1b): $=8$. Notes: Shows that area of $R=8$",
       r"ALT: Alt(c) — M1 (AO 1.1b): $\int3x^2-12x+12\,\mathrm{d}x=x^3-6x^2+12x$",
       r"ALT: Alt(c) — A1 (AO 1.1b): $\int3x^2-12x+12\,\mathrm{d}x=x^3-6x^2+12x$",
       r"ALT: Alt(c) — M1 (AO 3.1a): Method to find $R=\int_0^2 3x^2-12x+12\,\mathrm{d}x$",
       r"ALT: Alt(c) — dM1 (AO 1.1b): $R=2^3-6\times2^2+12\times2$",
       r"ALT: Alt(c) — A1 (AO 1.1b): $=8$"],
      True, 34),

    # ---------------- Q15 ----------------
    e("15a", "15(a)", COORD, "3.1", 2, Q15 + r"the equation of line $PN$ in the form $y=mx+c$, where $m$ and $c$ are constants,",
      [r"M1 (AO 2.2a): Deduces the line has gradient \"$-3$\" and point $(7,4)$ Eg $y-4=-3(x-7)$. Notes: Uses the idea "
       r"of perpendicular gradients to deduce that gradient of $PN$ is $-3$ with point $(7,4)$ to find the equation of "
       r"line $PN$. So sight of $y-4=-3(x-7)$ would score this mark. If the form $y=mx+c$ is used expect the candidates "
       r"to proceed as far as $c=\ldots$ to score this mark.",
       r"A1 (AO 1.1b): $y=-3x+25$. Notes: Achieves $y=-3x+25$"],
      True, 38),
    e("15b", "15(b)", COORD, "3.2, 3.1, 2.4", 4, Q15 + r"an equation for $C$.",
      [r"M1 (AO 3.1a): Solves $y=-3x+25$ and $y=\frac{1}{3}x$ simultaneously. Notes: Awarded for an attempt at the key "
       r"step of finding the coordinates of point $P$. ie for an attempt at solving their $y=-3x+25$ and "
       r"$y=\frac{1}{3}x$ simultaneously. Allow any methods (including use of a calculator) but it must be a valid "
       r"attempt to find both coordinates.",
       r"A1 (AO 1.1b): $P=\left(\frac{15}{2},\frac{5}{2}\right)$ oe. Notes: $P=\left(\frac{15}{2},\frac{5}{2}\right)$",
       r"M1 (AO 1.1b): Length $PN=\sqrt{\left(\frac{15}{2}-7\right)^2+\left(4-\frac{5}{2}\right)^2}=\left(\sqrt{\frac{5}"
       r"{2}}\right)$. Notes: Uses Pythagoras' Theorem to find the radius or radius$^2$ using their "
       r"$P=\left(\frac{15}{2},\frac{5}{2}\right)$ and $(7,4)$. There must be an attempt to find the difference between "
       r"the coordinates in the use of Pythagoras",
       r"A1 (AO 1.1b): Equation of $C$ is $(x-7)^2+(y-4)^2=\frac{5}{2}$ o.e. Notes: Full and careful work leading to a "
       r"correct equation. Eg $(x-7)^2+(y-4)^2=\frac{5}{2}$ or its expanded form. Do not accept "
       r"$(x-7)^2+(y-4)^2=\left(\sqrt{\frac{5}{2}}\right)^2$"],
      True, 38),
    e("15c", "15(c)", COORD, "3.2, 2.3", 3,
      Q15 + r"(a) the equation of line $PN$ in the form $y=mx+c$, where $m$ and $c$ are constants, (b) an equation for "
      r"$C$. The line with equation $y=\frac{1}{3}x+k$, where $k$ is a non-zero constant, is also a tangent to $C$. "
      r"(c) Find the value of $k$.",
      [r"M1 (AO 3.1a): Attempts to find where $y=\frac{1}{3}x+k$ meets $C$ using vectors Eg: "
       r"$\begin{pmatrix}7.5\\2.5\end{pmatrix}+2\times\begin{pmatrix}-0.5\\1.5\end{pmatrix}$. Notes: Attempts to find "
       r"where $y=\frac{1}{3}x+k$ meets $C$ using a vector approach",
       r"M1 (AO 2.1): Substitutes their $\left(\frac{13}{2},\frac{11}{2}\right)$ in $y=\frac{1}{3}x+k$ to find $k$. Notes: "
       r"For a full method leading to $k$. Scored for substituting their $\left(\frac{13}{2},\frac{11}{2}\right)$ in "
       r"$y=\frac{1}{3}x+k$",
       r"A1 (AO 1.1b): $k=\frac{10}{3}$. Notes: $k=\frac{10}{3}$ only",
       r"ALT: Alternative I (second scheme table) — M1 (AO 3.1a): Attempts to find where $y=\frac{1}{3}x+k$ meets $C$ via "
       r"simultaneous equations proceeding to a 3TQ in $x$ (or $y$). FYI $\frac{10}{9}x^2+\left(\frac{2}{3}k-\frac{50}{3}"
       r"\right)x+k^2-8k+\frac{125}{2}=0$. Notes: For solving $y=\frac{1}{3}x+k$ with their $(x-7)^2+(y-4)^2=\frac{5}{2}$ "
       r"and creating a quadratic eqn of the form $ax^2+bx+c=0$ where both b and c are dependent upon k. The terms in "
       r"$x^2$ and $x$ must be collected together or implied to have been collected by their correct use in "
       r"\"$b^2-4ac$\"",
       r"ALT: Alternative I — M1 (AO 2.1): Uses $b^2-4ac=0$ oe and proceeds to $k=\ldots$ Notes: For using the "
       r"discriminant condition $b^2-4ac=0$ to find $k$. It is not dependent upon the previous M and may be awarded from "
       r"only one term in $k$. Award if you see use of correct formula but it would be implied by $\pm$ correct roots",
       r"ALT: Alternative I — A1 (AO 1.1b): $k=\frac{10}{3}$ only",
       r"ALT: Alternative II — M1: For solving $y=-3x+25$ with their $(x-7)^2+(y-4)^2=\frac{5}{2}$, creating a 3TQ and "
       r"solving.",
       r"ALT: Alternative II — M1: For substituting their $\left(\frac{13}{2},\frac{11}{2}\right)$ into "
       r"$y=\frac{1}{3}x+k$ and finding $k$",
       r"ALT: Alternative II — A1: $k=\frac{10}{3}$ only"],
      True, 38),

    # ---------------- Q16 ----------------
    e("16a", "16(a)", DIFF, "7.2, 7.1", 4, Q16 + Q16A,
      [r"M1 (AO 1.1b): (i) Uses $\frac{\mathrm{d}y}{\mathrm{d}x}=-3$ at $x=2\Rightarrow12a+60-39=-3$. Notes: Attempts to "
       r"use $\frac{\mathrm{d}y}{\mathrm{d}x}=-3$ at $x=2$ to form an equation in $a$. Condone slips but expect to see two "
       r"of the powers reduced correctly",
       r"A1* (AO 2.1): Solves a correct equation and shows one correct intermediate step "
       r"$12a+60-39=-3\Rightarrow12a=-24\Rightarrow a=-2$ *. Notes: Correct differentiation with one correct intermediate "
       r"step before $a=-2$",
       r"M1 (AO 3.1a): (ii) Uses the fact that $(2,10)$ lies on $C$: $10=8a+60-78+b$. Notes: Attempts to use the fact that "
       r"$(2,10)$ lies on $C$ by setting up an equation in $a$ and $b$ with $a=-2$ leading to $b=\ldots$",
       r"A1 (AO 1.1b): Subs $a=-2$ into $10=8a+60-78+b\Rightarrow b=44$. Notes: $b=44$"],
      False, 42),
    e("16b", "16(b)", DIFF, "7.3, 2.3", 3, Q16 + Q16A + r"(b) Hence show that $C$ has no stationary points.",
      [r"B1 (AO 1.1b): $\mathrm{f}(x)=-2x^3+15x^2-39x+44\Rightarrow\mathrm{f}'(x)=-6x^2+30x-39$. Notes: "
       r"$\mathrm{f}'(x)=-6x^2+30x-39$ oe",
       r"M1 (AO 3.1a): Attempts to show that $-6x^2+30x-39$ has no roots Eg. calculates "
       r"$b^2-4ac=30^2-4\times-6\times-39=-36$. Notes: Correct attempt to show that \"$-6x^2+30x-39$\" has no roots. This "
       r"could involve an attempt at: finding the numerical value of $b^2-4ac$; finding the roots of $-6x^2+30x-39$ using "
       r"the quadratic formula (or their calculator); completing the square for $-6x^2+30x-39$",
       r"A1* (AO 2.4): States that as $\mathrm{f}'(x)\neq0\Rightarrow$ hence $\mathrm{f}(x)$ has no turning points *. "
       r"Notes: A fully correct method with reason and conclusion. Eg as $b^2-4ac=-36<0$, $\mathrm{f}'(x)\neq0$ meaning "
       r"that no stationary points exist"],
      False, 42),
    e("16c", "16(c)", ALG, "2.6", 2, Q16 + Q16A + Q16C,
      [r"M1 (AO 1.1b): $-2x^3+15x^2-39x+44\equiv(x-4)(-2x^2+7x-11)$. Notes: For an attempt at division (seen or implied) "
       r"Eg $-2x^3+15x^2-39x+b\equiv(x-4)\left(-2x^2\ldots\pm\frac{b}{4}\right)$",
       r"A1 (AO 1.1b): $-2x^3+15x^2-39x+44\equiv(x-4)(-2x^2+7x-11)$. Notes: $(x-4)(-2x^2+7x-11)$ Sight of the quadratic "
       r"with no incorrect working seen can score both marks."],
      False, 42),
    e("16d", "16(d)", ALG, "2.8, 2.6", 2,
      Q16 + Q16A + Q16C + r"(d) Hence deduce the coordinates of the points of intersection of the curve with equation "
      r"$$y=\mathrm{f}(0.2x)$$ and the coordinate axes.",
      [r"B1ft (AO 1.1b): Deduces either intercept. $(0,44)$ or $(20,0)$. Notes: See scheme. You can follow through on "
       r"their value for $b$",
       r"B1ft (AO 2.2a): Deduces both intercepts $(0,44)$ and $(20,0)$. Notes: See scheme. You can follow through on "
       r"their value for $b$"],
      False, 42),
]

# Examiner report, sentence by sentence, in report order.
# A sentence that mentions another part only in passing is tagged with the
# part it is about.
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "This was a short opening question to the paper, which enabled nearly all candidates to score at least one "
            "mark.", NO),
        (W, "However, several candidates did not find their critical values correctly, sometimes equating to 20 rather "
            "than rearranging and equating to 0 or making errors when factorising."),
        (W, r"Most, however, were able to find 5 and $-4$."),
        (W, "Typically, most realised that they needed to select the outside region, although there were a few "
            "responses with incorrect inequalities."),
        (W, "It was very rare for candidates to correctly give their answer using set notation, and very few being "
            "able to score full marks.", NO),
    ],
    "02": [
        (W, "This question proved to be one of the most challenging questions on the paper."),
        (W, "Most were able to score one mark, however, it was very rare for a candidate to achieve the correct final "
            "answer.", NO),
        (W, "A good number appreciated the need to make each of the terms as a 3 to the power of something."),
        (W, r"However, errors were often made in multiplying the power together on $3^{2(x-1)}$ or 9 was written as "
            r"$3^3$."),
        (W, "Others opted to try and log both sides, but those who did not state the base were unable to score as "
            "working in base 10 would not be possible without a calculator.", NO),
        (W, "Those who selected a suitable base were often able to score at least one mark, although a significant "
            "number of candidates either applied index laws or laws of logarithms incorrectly.", NO),
        (W, r"It was disappointing that several candidates rearranged by multiplying both sides by $3^{y+2}$ such that "
            r"the left-hand side became $243^{4y+8}$ thinking that the two base numbers could be multiplied together "
            r"and that the powers would also be multiplied.", NO),
        (W, r"Those who did achieve an equation where all the terms were 3 to the power of something were typically "
            r"able to equate the powers and proceed to find an equation for $y$ in terms of $x$.", NO),
        (W, "However, some poor rearrangements by applying incorrect inverse operations meant that a correct final "
            "answer was rarely seen."),
    ],
    "03": [
        (W, "This question was very accessible; however, it was surprising that the majority were unable to score full "
            "marks on this question.", NO),
        (W, "This should have been a very straight forward question for those who had understood integration.", NO),
        (W, "However, a significant number thought that you could integrate the numerator and denominator of the "
            "fraction."),
        (W, "Another significant number made errors when splitting the fraction into two separate terms."),
        (W, "Errors often occurred in dealing with the 2 on the denominator and, as such, this restricted the maximum "
            "marks to 2 out of 4.", NO),
        (W, "Those who were able to separate the fraction correctly, were often able to score 3 out of 4, with "
            "typically the omission of the constant of integration being the reason for not scoring full marks.", NO),
    ],
    "04": [
        (W, "This question using vectors was generally well answered with most candidates scoring more than half of the "
            "marks available."),
        ({"a"}, "In part (a) candidates seemed unsure how to go about proving that the stone passed through the origin."),
        ({"a"}, r"The most successful attempts typically involved finding the equation of the line for the stone which "
                r"was $y=\frac{5}{12}x$ and showed that the origin was on this line or stated that this linear equation "
                r"would pass through the origin.", NO),
        ({"a"}, "Other attempts which candidates proceeded with involved either comparing the position vectors and "
                "showing that one was a multiple of the other or showing that the gradients of the position vectors "
                "were the same."),
        ({"a"}, "Plotting the points on a graph was not an acceptable method to prove."),
        ({"b"}, r"In part (b) most candidates were able to find the vector $\overrightarrow{AB}$ and proceeded to find the "
                r"magnitude of their vector."),
        ({"b"}, "Some forgot to then find the speed by dividing by 9, whilst others omitted or gave the wrong unit, or "
                "just gave the generic units per second as their unit for speed.",
         {"note": "the stone moves for 4 seconds and the mark scheme divides by 4"}),
    ],
    "05": [
        (W, "This question was generally well attempted, although it was rare for candidates to score full marks.", NO),
        ({"a"}, r"In part (a), candidates knew that they needed to differentiate, and most had read the question "
                r"carefully to realise that they also needed to substitute $x=2$ into their "
                r"$\frac{\mathrm{d}y}{\mathrm{d}x}$, enabling them to proceed often to the correct answer."),
        ({"b"}, "Part (b) was completed to a high degree of success."),
        ({"b"}, r"Candidates are clearly more comfortable with the idea of finding the gradient of a chord in terms of "
                r"$h$ and most were able to proceed to the correct answer."),
        ({"b"}, r"Some made slips in their multiplying out of the brackets and there was the occasional response where "
                r"the candidate had differentiated again and substituted in $2+h$ which could not score."),
        ({"c"}, "In part (c) candidates still struggled with bringing the concept of the gradient of a chord tending to "
                "the gradient at a point on a curve it was extremely rare to see a correct response, although this "
                "could be due to candidates having made an error in (a) or (b) so they were unable to see clearly what "
                "the link was between them anyway.", NO),
    ],
    "06": [
        (W, "This was a question which was completed to a high degree of accuracy by a pleasing number of candidates.",
         NO),
        (W, "There seemed to be more notice taken by many candidates regarding showing all stages of their working."),
        ({"a"}, "In part (a) it was common for candidates to score full marks.", NO),
        ({"a"}, r"Typically, candidates factorised out the $x$ and then they proceeded to correctly factorise the "
                r"resulting quadratic proceeding to the correct solutions."),
        ({"a"}, r"It was rare for a candidate to divide by $x$ and hence lose the solution of 0.", NO),
        ({"b"}, "Part (b) proved to be a good discriminator."),
        ({"b"}, "Some candidates tackled this part well recognising the link from (a) and showing sufficient working of "
                "using their solutions to proceed to correct ones in (b)."),
        ({"b"}, "However, a significant number came unstuck with this part and tried to multiply out the brackets and "
                "start again."),
        ({"b"}, r"Some also tried to set $(y-2)^2$ equal to their solution, but then multiplied out the brackets and "
                r"solve using the formula or factorising a new quadratic, rather than just square rooting and adding 2."),
        ({"b"}, "It was rare for candidates to just use their calculator which could not score.", NO),
        ({"b"}, "Some squared rather than square rooted, and some forgot the negative solution from square rooting."),
        ({"b"}, "Others thought you could square root a negative."),
    ],
    "07": [
        (W, "Question 7 was testing a candidate’s ability to apply trigonometry to solve a problem relating to a "
            "parallelogram."),
        (W, "This was one of the most challenging questions on the paper and was largely as a result of the candidates "
            "having to draw their own diagram.", NO),
        ({"a"}, "In part (a) there were many incorrect diagrams to begin with, which included incorrect labelling of the "
                "vertices."),
        ({"a"}, "Some tried to find the required angle by splitting the parallelogram into a rectangle and two "
                "triangles."),
        ({"a"}, "However, they made little progress with this and often just stopped.", BACK),
        ({"a"}, "Other candidates who did correctly set up an equation using the sine rule, then forgot to find the "
                "obtuse angle."),
        ({"a"}, r"Some subtracted the acute angle from $360^\circ$."),
        ({"b"}, "In part (b) candidates often tried to apply Pythagoras to the two given sides when there was not a right "
                "angle and although some did proceed with the intention of applying the cosine rule, the sine function "
                "or omission of the square root sometimes prevented a correct answer being achieved."),
    ],
    "08": [
        ({"b"}, "The binomial expansion question proved to be very accessible to begin with, but for many, part (b) was "
                "too challenging so full marks was extremely rare on this question."),
        ({"a"}, r"In part (a), candidates were usually very successful in finding that $a=\frac{3}{2}$."),
        ({"a"}, r"Candidates typically wrote out all the terms up to the coefficient for $x^5$, although some did proceed "
                r"straight to the required term."),
        ({"a"}, "The small minority made errors with the correct binomial coefficient."),
        ({"a"}, r"Candidates were often able to equate their coefficient for $x^5$ to the coefficient given in the "
                r"question, although bracket errors meant that the most frequent error was not achieving $a^5$ so no "
                r"further marks could be scored in this part as they had simplified the question."),
        ({"b"}, r"In part (b) candidates often recognised that $2^8$ was a required term, but very few found the other "
                r"term, and hardly any attempted to add the two required terms together."),
    ],
    "09": [
        (W, "This question was typically answered well by most candidates and was possibly the most successful question "
            "on the paper."),
        (W, r"Candidates typically were able to manipulate the integral to achieve $\ldots x^{-\frac{1}{2}}$, although "
            r"those who omitted the negative did not score any marks on this question.", NO),
        (W, "Some candidates made errors dealing with the coefficient, but they were typically able to score half of the "
            "available marks on the paper."),
        (W, r"Whilst most proceeded to the correct answer, some incorrectly square rooted to find $k$ rather than "
            r"squaring."),
    ],
    "10": [
        (W, "This question tested both proof by deduction and proof by counter-example."),
        (W, "It was pleasing to see improved attempts made on this type of question.", NO),
        ({"a"}, r"In part (a) candidates were usually able to set up their proof using $2k+1$ or similar."),
        ({"a"}, r"Some continue to set $n=2n+1$ which was condoned on this occasion.", NO),
        ({"a"}, r"Some candidates unfortunately set up their proof with $4k+1$ or $n^2+1$ which could not score."),
        ({"a"}, "Candidates were usually successful in substituting into the expression, multiplying out and "
                "simplifying."),
        ({"a"}, r"Some candidates did forget later to subtract $2k+1$ or similar as they had become to engrossed in the "
                r"multiplying out of the cubic, although most then knew they needed to take a factor of 4 out of their "
                r"expression."),
        ({"a"}, "The final mark was typically lost for bracket errors, or the omission of them, in their proof at some "
                "point in their working so candidates should be encouraged to check their work carefully."),
        ({"a"}, "Most candidates knew that they needed to conclude at the end."),
        ({"b"}, "In part (b), this proved to be harder work for many candidates.", NO),
        ({"b"}, "A significant number seemed to not understand what a natural number was and opted to substitute a "
                "negative number, or a fraction, into the expression."),
        ({"b"}, "There was also some confusion regarding whether 0 was a multiple of 4 as well."),
    ],
    "11": [
        (W, "This question was generally answered well by most candidates."),
        (W, "It was typically silly mistakes or not reading the question which resulted in full marks not being "
            "scored.", NO),
        ({"a"}, r"In part (a), most candidates were successful in finding the area to be 35 km$^2$."),
        ({"a"}, "Some just opted for 80 and the units were also incorrect, at times, such as being given as trees.", NO),
        ({"b"}, "In part (b), candidates typically were able to equate the expression to 60 and rearrange correctly."),
        ({"b"}, r"A pleasing number were able to proceed to the correct value for $c$, although a significant number did "
                r"not then state the equation which the question asked the candidates to find a complete equation."),
        ({"b"}, r"Some over rounded the value of $c$, whilst others tried to take logs of each term."),
        ({"c"}, "Part (c) was answered well by many candidates."),
        ({"c"}, r"It was really pleasing to see so many comments where the candidate had clearly engaged with the model "
                r"and recognised that the maximum area was 80 km$^2$.", NO),
        ({"c"}, "This type of response was much more frequent than last time when most opted to just substitute in the "
                "value given in the question and show that you cannot take logs of a negative number.", BACK),
        ({"c"}, "Whilst this was accepted as a valid response, the engaging of candidates with the context of models "
                "should continue to be encouraged.", BACK),
    ],
    "12": [
        (W, "Candidates were usually able to make good progress on the first half of this question on solving "
            "trigonometric equations, but they tended to run into problems halfway through."),
        (W, "It was rare for full marks to be scored, although most were able to score around half of the available "
            "marks.", NO),
        ({"i"}, r"In part (i), nearly all candidates were able to proceed to the correct quadratic in $\sin\theta$, "
                r"although the occasional candidate tried to incorrectly substitute $\sin\theta=1-\cos\theta$ into the "
                r"right-hand side of the equation."),
        ({"i"}, "Most candidates were able to apply the quadratic formula and proceed to finding all three angles."),
        ({"i"}, "Some found additional angles, which even if they are outside the range, prevent full marks from being "
                "scored.", NO),
        ({"i"}, "Most candidates seemed to opt for sketching trigonometric graphs to find the other angles as opposed to "
                "using the CAST diagram."),
        ({"iia"}, "Part (ii)(a) was poorly answered, however."),
        ({"iia"}, r"Most candidates failed to score either mark, although those who did were usually able to make some "
                  r"reference to cancelling out $\sin x$.", NO),
        ({"iia"}, "Just stating that not all the angles had been found was insufficient explanation as to the errors "
                  "made so candidates should be encouraged to provide greater detail if they are able to do so.", NO),
        ({"iib"}, "Part (ii)(b) was attempted by most candidates, with many able to equate to the correct angle, "
                  "rearrange and proceed to the correct answer."),
        ({"iib"}, "There were a number who equated to several angles, but either did not make their final answer clear, "
                  "or did not rearrange to find the required angle."),
    ],
    "13": [
        (W, "This question testing exponential decay and the relationship with logarithmic graphs was poorly answered.",
         NO),
        (W, "Very few were able to score even half of the available marks and it was clear that many candidates still "
            "struggle with this topic.", NO),
        ({"a"}, r"In part (a) candidates found forming a correct relationship between the linear graph and the given "
                r"exponential model too difficult."),
        ({"a"}, r"Many produced incorrect equations and poor working with logarithms followed, resulting in incorrect "
                r"values for $p$ and $q$."),
        ({"b"}, "As part (a) was not completed successfully in many cases, part (b) automatically was limited in its "
                "accessibility."),
        ({"b"}, r"Some candidates just made a comment, rather than use the model as they did not have values for $p$ and "
                r"$q$, or even those who did seemed unsure what they were finding.", NO),
        ({"c"}, "Part (c) had a range of responses, but it was extremely rare for a mark to be scored and most failed to "
                "appreciate that the resting heart rate related to a mammal with a mass of 1 kg.", NO),
    ],
    "14": [
        (W, "This question was one of the most successful on the paper."),
        (W, "It tested aspects such as completing the square, simple integration to find an area and finding a turning "
            "point which candidates seemed comfortable finding in nearly all cases.", BACK),
        ({"a"}, "Part (a) was typically correctly answered."),
        ({"a"}, r"Most opted to complete the square rather than equate coefficients and it was only the minority who made "
                r"slips with the $-3$ coefficient for $a$.", NO),
        ({"a"}, r"Where errors occurred, it was usually in multiplying out to get the coefficient for $c$, but they were "
                r"still able to score 2 marks.", NO),
        ({"b"}, "Part (b) required candidates to find the turning point."),
        ({"b"}, "Whilst the intention was for candidates to use their part (a) answer, and follow through was allowed on "
                "this, it was much more common for candidates to differentiate the quadratic and find the turning "
                "point.", NO),
        ({"b"}, "Therefore, nearly all candidates score both marks on this part as most seemed more confident using "
                "calculus and proceeded to the correct answer anyway.", NO),
        ({"c"}, "Part (c) was typically completed correctly."),
        ({"c"}, r"Candidates usually opted to integrate the curve and find the area between $x=0$ and $x=2$ and then "
                r"subtracted this area from 40.", NO),
        ({"c"}, "Those candidates who tried to form a single integral to solve the problem were the ones were errors "
                "typically occurred.", NO),
        ({"c"}, r"Some candidates equated the line $y=20$ to the curve and rearranged to one side and integrated this "
                r"expression.", NO),
        ({"c"}, "This method can work, although some responses did not appear that the candidates were that sure as to "
                "why they had achieved a negative value for the integral if they collected terms on the wrong side."),
        ({"c"}, "In addition, errors in collecting terms resulted in an incorrect integrated expression and, ultimately, "
                "an incorrect final answer."),
    ],
    "15": [
        ({"c"}, "This question provided a good range of marks between the candidates, although nearly all candidates "
                "struggled to proceed to the final answer in part (c)."),
        (W, "There were also several blank responses on this question which may have been down to candidates either "
            "running out of time or just getting overwhelmed towards the end of a paper."),
        ({"a"}, "In part (a), candidates were usually able to find the equation of the line."),
        ({"a"}, r"The odd error in rearranging their equation of the line or incorrectly sub substituting in the "
                r"coordinates for $x$ and $y$ were the few situations where full marks were not scored."),
        ({"b"}, "Part (b) was generally attempted well."),
        ({"b"}, r"Most knew and attempted to find the point where the two lines intersected each other and found the "
                r"point $P$ correctly."),
        ({"b"}, "They were then able to find the radius and usually proceeded to find the equation of the circle."),
        ({"b"}, r"Sometimes the equation of the circle had the squared missing from the brackets or it was equated to the "
                r"radius rather than $r^2$.", NO),
        ({"c"}, "Part (c) was either not attempted at all or candidates made an attempted but abandoned due to the "
                "expressions formed appearing so complicated that it seemed as though they were convinced they had gone "
                "wrong.", NO),
        ({"c"}, "Usually, candidates opted to substitute their part (a) answer into their part (b) equation of the "
                "circle."),
        ({"c"}, r"To score the first mark candidates had to multiply out the brackets and collect terms together to form "
                r"a 3TQ where $k$ was in both the $b$ and $c$ coefficients of the quadratic."),
        ({"c"}, "Some candidates stopped before getting this far, although it was pleasing that some continued to "
                "persevere and pick up the first mark.", NO),
        ({"c"}, r"Those who continued, realised the discriminant needed to be used, but disappointingly once they had "
                r"their expression also decided to stop even if they had a quadratic in $k$ which they could solve.", NO),
        ({"c"}, "Therefore only 1 or no marks was scored in nearly all responses.", BACK),
        ({"c"}, "The easiest way was the vector approach, which was seen, but far too frequently, and even then, it was "
                "only a few candidates who were able to score full marks on this question.", NO),
    ],
    "16": [
        (W, "The last question on the paper was attempted by most candidates, although there were a significant number "
            "of blank responses."),
        (W, "Again, this was possibly either due to time, or more likely due to candidates just feeling overwhelmed as "
            "the question was the longest on the paper.", BACK),
        ({"a"}, "In part (a) candidates struggled with the information being presented in reverse order."),
        ({"a"}, r"As a result, candidates typically formed the equation in $a$ and $b$ but then got stuck as they could "
                r"not see how they would find $a$.", NO),
        ({"a"}, r"It was those who differentiated and equated to $-3$ who were able to fully complete part (a) "
                r"correctly.", NO),
        ({"a"}, "It was noted that a large number did not seem to be that confident with turning points and derivatives "
                "and it may have been that this had not been covered which prevented candidates from doing this question "
                "particularly well.", NO),
        ({"b"}, "Part (b) also demonstrated the lack of confidence with using calculus in relation to turning points."),
        ({"b"}, r"Quite often they were able to differentiate to get a quadratic in $x$, however they seemed unsure where "
                r"to go from there and often just state that there were no solutions or that it would not factorise.",
         NO),
        ({"b"}, "It was typical for candidates to only score 1 mark in this part.", NO),
        ({"c"}, "Part (c) was completed to a much higher degree of success with the majority able to find the quadratic "
                "Q."),
        ({"c"}, "Most opted to carry out algebraic division, although errors were seen with the subtraction lines in "
                "their method which demonstrated a lack of confidence with their method."),
        ({"c"}, "They then proceeded to have a remainder value, but still stated the quadratic they had found."),
        ({"c"}, r"Where their value for $b$ was incorrect this was condoned.", NO),
        ({"d"}, r"Most candidates did not attempt part (d), whilst some were able to find that $x=20$ they failed to "
                r"state the coordinates so hardly any candidates scored any marks on this part."),
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
    "01": ("hard", at("01", "It was very rare for candidates to correctly give")),
    "02": ("hard", at("02", "Most were able to score one mark")),
    "03": ("medium", at("03", "This question was very accessible")),
    "04a": ("medium", at("04", "In part (a) candidates seemed unsure")),
    "04b": ("medium", at("04", "Some forgot to then find the speed")),
    "05a": ("easy", at("05", "In part (a), candidates knew")),
    "05b": ("easy", at("05", "Part (b) was completed to a high degree")),
    "05c": ("hard", at("05", "In part (c) candidates still struggled")),
    "06a": ("easy", at("06", "In part (a) it was common for candidates to score full marks")),
    "06b": ("medium", at("06", "Part (b) proved to be a good discriminator")),
    "07a": ("hard", at("07", "This was one of the most challenging questions")),
    "07b": ("hard", at("07", "This was one of the most challenging questions")),
    "08a": ("easy", at("08", "In part (a), candidates were usually very successful")),
    "08b": ("hard", at("08", "In part (b) candidates often recognised")),
    "09": ("easy", at("09", "This question was typically answered well")),
    "10a": ("medium", at("10", "The final mark was typically lost")),
    "10b": ("medium", at("10", "In part (b), this proved to be harder work")),
    "11a": ("easy", at("11", "In part (a), most candidates were successful")),
    "11b": ("medium", at("11", "A pleasing number were able")),
    "11c": ("easy", at("11", "Part (c) was answered well by many")),
    "12i": ("easy", at("12", "Most candidates were able to apply the quadratic formula")),
    "12iia": ("hard", at("12", "Most candidates failed to score either mark")),
    "12iib": ("medium", at("12", "Part (ii)(b) was attempted by most")),
    "13a": ("hard", at("13", "In part (a) candidates found forming")),
    "13b": ("hard", at("13", "As part (a) was not completed successfully")),
    "13c": ("hard", at("13", "Part (c) had a range of responses")),
    "14a": ("easy", at("14", "Part (a) was typically correctly answered")),
    "14b": ("easy", at("14", "Therefore, nearly all candidates score both marks")),
    "14c": ("easy", at("14", "Part (c) was typically completed correctly")),
    "15a": ("easy", at("15", "In part (a), candidates were usually able")),
    "15b": ("easy", at("15", "Part (b) was generally attempted well")),
    "15c": ("hard", at("15", "Therefore only 1 or no marks")),
    "16a": ("hard", at("16", "In part (a) candidates struggled")),
    "16b": ("hard", at("16", "It was typical for candidates to only score 1 mark")),
    "16c": ("easy", at("16", "Part (c) was completed to a much higher degree")),
    "16d": ("hard", at("16", "Most candidates did not attempt part (d)")),
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
