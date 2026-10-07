"""Draft builder for 8MA0-01 2024-06 (AS Pure, June 2024).

Run (from the project root, with the venv active):
    python extraction/8MA0-01_2024-06.py        # writes out/drafts/8MA0-01_2024-06.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-01_2024-06.json

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

P, S = "8MA0-01", "2024-06"
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
        "Solutions relying entirely on calculator technology are not acceptable."]
Q2 = SHOW + [r"$$\mathrm{f}(x)=2x^3-3ax^2+bx+8a$$", "where $a$ and $b$ are constants.",
             r"Given that $(x-4)$ is a factor of $\mathrm{f}(x)$,"]
Q2A = ["use the factor theorem to show that", "$$10a=32+b$$"]
Q2G = r"Given also that $(x-2)$ is a factor of $\mathrm{f}(x)$,"
Q2B = [r"express $\mathrm{f}(x)$ in the form", r"$$\mathrm{f}(x)=(2x+k)(x-4)(x-2)$$", "where $k$ is a constant to be found."]
Q3 = ["Relative to a fixed origin $O$,", r"• point $P$ has position vector $9\mathbf{i}-8\mathbf{j}$",
      r"• point $Q$ has position vector $3\mathbf{i}-5\mathbf{j}$"]
Q3G = r"Given that $R$ is the point such that $\overrightarrow{QR}=9\mathbf{i}+18\mathbf{j}$"
Q3B = r"show that angle $PQR=90^\circ$"
Q4 = [r"[Figure 1: points $A$, $D$ and $C$ on a horizontal line, with $AD=(x-2)$ cm; $B$ above and to the right of $C$, "
      r"joined to $A$, $D$ and $C$; $BD=(x+3)$ cm with angle $BDC=30^\circ$ marked at $D$, and $BC=x$ cm with angle "
      r"$BCD=140^\circ$ marked at $C$.]",
      "Figure 1 shows a sketch of triangle $ABD$ and triangle $BCD$", "Given that", "• $ADC$ is a straight line",
      "• $BD=(x+3)$ cm", "• $BC=x$ cm", r"• angle $BDC=30^\circ$", r"• angle $BCD=140^\circ$"]
Q4A = "show that $x=10.5$ correct to 3 significant figures."
Q5 = ["The curve $C_1$ has equation", r"$$y=\frac{6}{x}+3$$"]
Q5C2 = ["The curve $C_2$ has equation", "$$y=3x^2-4x-10$$"]
Q5B = ["Show that $C_1$ and $C_2$ intersect when", "$$3x^3-4x^2-13x-6=0$$"]
Q6 = ["The binomial expansion of", "$$(1+ax)^{12}$$", "up to and including the term in $x^2$ is",
      r"$$1-\frac{15}{2}x+kx^2$$", "where $a$ and $k$ are constants."]
Q6A = r"Show that $a=-\frac{5}{8}$"
Q6B = "Hence find the value of $k$"
Q7 = [r"[Figure 2: a straight line on axes $x$ (horizontal) and $\log_{10}P$ (vertical), from the point $(0, 3.3)$ on the "
      r"vertical axis sloping down to the point $(6, 2.1)$.]",
      "A chimney emits smoke particles.",
      "On a particular day, the concentration of smoke particles in the air emitted by this chimney, $P$ parts per "
      "million, is measured at various distances, $x$ km, from the chimney.",
      r"Figure 2 shows a sketch of the linear relationship between $\log_{10}P$ and $x$ that is used to model this "
      r"situation.",
      "The line passes through the point $(0, 3.3)$ and the point $(6, 2.1)$"]
Q7A = ["Find a complete equation for the model in the form", "$$P=ab^x$$",
       "where $a$ and $b$ are constants. Give the value of $a$ and the value of $b$ each to 4 significant figures."]
Q8 = [r"[Figure 3: the curve $C$, a cubic with a maximum to the left of the $y$-axis and a minimum at $A$ just right of "
      r"the $y$-axis, touching the line $l$ at $A$; the line $l$, with negative gradient, meets $C$ again at $B$ to the "
      r"left of the $y$-axis; the region $R$ between $C$ and $l$, from $B$ to $A$, is shaded.]"] + SHOW + [
      "Figure 3 shows a sketch of the curve $C$ with equation", "$$y=x^3-14x+23$$",
      "The line $l$ is the tangent to $C$ at the point $A$, also shown in Figure 3.",
      "Given that $l$ has equation $y=-2x+7$"]
Q8A = "show, using calculus, that the $x$ coordinate of $A$ is 2"
Q8B = ["The line $l$ cuts $C$ again at the point $B$.", "Verify that the $x$ coordinate of $B$ is $-4$"]
Q9 = [r"$$p=\log_a16$$", r"$$q=\log_a25$$", "where $a$ is a constant.", "Find in terms of $p$ and/or $q$,"]
Q10 = [r"[Figure 4: the circle $C$ with centre $P$ to the left of the $y$-axis and above the $x$-axis, and the line $l$ "
       r"with negative gradient touching $C$ at the point $Q$, which is to the right of the $y$-axis.]",
       "Figure 4 shows a sketch of the circle $C$",
       "• the point $P(-1, k+8)$ is the centre of $C$", "• the point $Q(3, k^2-2k)$ lies on $C$",
       "• $k$ is a positive constant", "• the line $l$ is the tangent to $C$ at $Q$",
       "Given that the gradient of $l$ is $-2$"]
Q10A = ["show that", "$$k^2-3k-10=0$$"]
Q11 = ["The prices of two precious metals are being monitored.",
       "The price per gram of metal $A$, £$V_A$, is modelled by the equation", r"$$V_A=100+20\mathrm{e}^{0.04t}$$",
       "where $t$ is the number of months after monitoring began.",
       "The price per gram of metal $B$, £$V_B$, is modelled by the equation", r"$$V_B=p\mathrm{e}^{-0.02t}$$",
       "where $p$ is a positive constant and $t$ is the number of months after monitoring began.",
       "Given that $V_B=2V_A$ when $t=0$"]
Q12 = [r"[Figure 5: plan view of the pool: a quarter circle in the top left, joined to a rectangle on its right (width "
       r"$y$, height $x$) and a rectangle below it (length $x$, height $y$), the two rectangles meeting at the corner; the "
       r"side $AB$ is the bottom edge of the right-hand rectangle.]",
       "Figure 5 shows the plan view of the design for a swimming pool.",
       "The pool is modelled as a quarter of a circle joined to two equal sized rectangles as shown.",
       "Given that", "• the quarter circle has radius $x$ metres",
       "• the rectangles each have length $x$ metres and width $y$ metres",
       "• the total surface area of the swimming pool is 100 m$^2$"]
Q12A = ["show that, according to the model, the perimeter $P$ metres of the swimming pool is given by",
        r"$$P=2x+\frac{200}{x}$$"]
Q12B = "Use calculus to find the value of $x$ for which $P$ has a stationary value."
Q12C = "Prove, by further calculus, that this value of $x$ gives a minimum value for $P$"
Q13A = ["Show that the equation", r"$$\sin\theta(7\sin\theta-4\cos\theta)=4$$", "can be written as",
        r"$$3\tan^2\theta-4\tan\theta-4=0$$"]
Q13B = [r"Hence solve, for $0<x<360^\circ$", r"$$\sin x(7\sin x-4\cos x)=4$$", "giving your answers to one decimal place."]

LATEX = {
    "01": L("Find", r"$$\int\frac{2\sqrt{x}-3}{x^2}\,\mathrm{d}x$$", "giving your answer in simplest form."),
    "02a": L(*Q2, *Q2A),
    "02b": L(*Q2, "(a) " + Q2A[0], Q2A[1], Q2G, "(b) " + Q2B[0], *Q2B[1:]),
    "02c": L(*Q2, "(a) " + Q2A[0], Q2A[1], Q2G, "(b) " + Q2B[0], *Q2B[1:], "(c) Hence,",
             r"(i) state the number of real roots of the equation $\mathrm{f}(x)=0$",
             r"(ii) write down the largest root of the equation $\mathrm{f}\left(\frac{1}{3}x\right)=0$"),
    "03a": L(*Q3, r"Find $\overrightarrow{PQ}$"),
    "03b": L(*Q3, Q3G, Q3B),
    "03c": L(*Q3, Q3G, "(b) " + Q3B, r"Given also that $S$ is the point such that $\overrightarrow{PS}=3\overrightarrow{QR}$",
             "(c) find the exact area of $PQRS$"),
    "04a": L(*Q4, Q4A),
    "04b": L(*Q4, "(a) " + Q4A, "Given also that $AD=(x-2)$ cm",
             "(b) find the length of $AB$, giving your answer to 3 significant figures."),
    "05a": L(*Q5, "(i) Sketch $C_1$ stating the coordinates of any points where the curve cuts the coordinate axes.",
             "(ii) State the equations of any asymptotes to the curve $C_1$"),
    "05b": L(*Q5, *Q5C2, *Q5B),
    "05c": L(*Q5, *Q5C2, "(b) " + Q5B[0], Q5B[1],
             r"Given that the $x$ coordinate of one of the points of intersection is $-\frac{2}{3}$",
             "(c) use algebra to find the $x$ coordinates of the other points of intersection between $C_1$ and $C_2$",
             "(Solutions relying on calculator technology are not acceptable.)"),
    "06a": L(*Q6, Q6A),
    "06b": L(*Q6, "(a) " + Q6A, "(b) " + Q6B),
    "06c": L(*Q6, "(a) " + Q6A, "(b) " + Q6B, "Using the expansion and making your method clear,",
             r"(c) find an estimate for the value of $\left(\frac{17}{16}\right)^{12}$, giving your answer to 4 decimal "
             r"places."),
    "07a": L(*Q7, *Q7A),
    "07b": L(*Q7, "(a) " + Q7A[0], *Q7A[1:], "(b) With reference to the model, interpret the value of $ab$"),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, *Q8B),
    "08c": L(*Q8, "(a) " + Q8A, Q8B[0], "(b) " + Q8B[1],
             "The finite region, $R$, shown shaded in Figure 3, is bounded by $C$ and $l$.",
             "Using algebraic integration,", "(c) show that the area of $R$ is 108"),
    "09a": L(*Q9, r"$\log_a256$"),
    "09b": L(*Q9, r"$\log_a100$"),
    "09c": L(*Q9, r"$\log_a80\times\log_a3.2$"),
    "10a": L(*Q10, *Q10A),
    "10b": L(*Q10, "(a) " + Q10A[0], Q10A[1], "(b) Hence find an equation for $C$"),
    "11a": L(*Q11, "find the value of $p$"),
    "11b": L(*Q11, r"When $t=T$, the rate of $\textbf{increase}$ in the price per gram of metal $A$ was equal to the rate "
             r"of $\textbf{decrease}$ in the price per gram of metal $B$",
             "Find the value of $T$, giving your answer to one decimal place.",
             "(Solutions based entirely on calculator technology are not acceptable.)"),
    "12a": L(*Q12, *Q12A),
    "12b": L(*Q12, "(a) " + Q12A[0], Q12A[1], "(b) " + Q12B),
    "12c": L(*Q12, "(a) " + Q12A[0], Q12A[1], "(b) " + Q12B, "(c) " + Q12C),
    "12d": L(*Q12, "(a) " + Q12A[0], Q12A[1], "(b) " + Q12B, "(c) " + Q12C,
             "Access to the pool is by side $AB$ shown in Figure 5.", "Given that $AB$ must be at least one metre,",
             "(d) determine, according to the model, whether the swimming pool with the minimum perimeter would be "
             "suitable."),
    "13a": L(*SHOW, *Q13A),
    "13b": L(*SHOW, "(a) " + Q13A[0], *Q13A[1:], "(b) " + Q13B[0], *Q13B[1:]),
    "13c": L(*SHOW, "(a) " + Q13A[0], *Q13A[1:], "(b) " + Q13B[0], *Q13B[1:],
             "(c) Hence find the smallest solution of the equation", r"$$\sin4\alpha(7\sin4\alpha-4\cos4\alpha)=4$$",
             r"in the range $720^\circ<\alpha<1080^\circ$, giving your answer to one decimal place."),
    "14": L("Prove, using algebra, that", "$$n^2+5n$$", r"is even for all $n\in\mathbb{N}$"),
}

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", INT, "8.2, 2.1", 4, LATEX["01"],
      [r"M1 (AO 1.1b): $\frac{2\sqrt{x}}{x^2}\to\ldots x^{-\frac{3}{2}}$ or $\frac{-3}{x^2}\to\ldots x^{-2}$. Notes: For "
       r"separating the fraction into two separate terms. Award for one correct index (which does not need to be processed. "
       r"e.g. $\ldots x^{\frac{1}{2}-2}$) Note $-\frac{3}{x^2}$ is insufficient. They must write as $\ldots x^{-2}$ or may be "
       r"implied by further work. Beware of candidates who integrate the numerator and denominator which results in a "
       r"correct index but is an incorrect method and scores M0A0dM0A0",
       r"A1 (AO 1.1b): $\int\frac{2\sqrt{x}-3}{x^2}\,\mathrm{d}x=\int2x^{-\frac{3}{2}}-3x^{-2}\,\mathrm{d}x$. Notes: "
       r"$2x^{-\frac{3}{2}}-3x^{-2}$ o.e. where the indices have been processed (may be implied by further work)",
       r"dM1 (AO 1.1b): $\ldots x^{-\frac{3}{2}}\to\ldots x^{-\frac{1}{2}}$ or $\ldots x^{-2}\to\ldots x^{-1}$. Notes: For "
       r"raising the power by one on at least one term with a correct index. It is dependent on the previous method mark. "
       r"The index does not need to be processed. e.g. $\ldots x^{-\frac{3}{2}}\to\ldots x^{-\frac{3}{2}+1}$. It is not for "
       r"$+c$.",
       r"A1 (AO 1.1b): $\int2x^{-\frac{3}{2}}-3x^{-2}\,\mathrm{d}x=-4x^{-\frac{1}{2}}+3x^{-1}+c$. Notes: All correct, "
       r"simplified and on one line including $+c$. Allow other simplified equivalent terms such eg. $-\frac{4}{\sqrt{x}}$ "
       r"for $-4x^{-\frac{1}{2}}$ or e.g. $\frac{3}{x}$ for $3x^{-1}$ but do not allow e.g. $+-4x^{-\frac{1}{2}}$ or "
       r"$-\frac{4}{1}x^{-\frac{1}{2}}$. Award once a correct expression is seen and isw but if there is any "
       r"additional/incorrect notation and no correct expression has been seen on its own, withhold the final mark. e.g. "
       r"$\int-4x^{-\frac{1}{2}}+3x^{-1}+c\,\mathrm{d}x$ or $-4x^{-\frac{1}{2}}+3x^{-1}+c=0$ with no correct expression seen "
       r"earlier are both A0. Ignore $y=\ldots$",
       r"ALT: Alternative method: integration by parts (e.g. $\int\frac{2\sqrt{x}-3}{x^2}\,\mathrm{d}x=\int(2\sqrt{x}-3)"
       r"x^{-2}\,\mathrm{d}x=-(2x^{\frac{1}{2}}-3)x^{-1}+\int x^{-\frac{3}{2}}\,\mathrm{d}x=-2x^{-\frac{1}{2}}+3x^{-1}"
       r"-2x^{-\frac{1}{2}}+c=-4x^{-\frac{1}{2}}+3x^{-1}+c$) — M1: For attempting integration by parts and achieving the "
       r"correct structure for the intermediate stage e.g. $\pm(\ldots x^{\frac{1}{2}}\pm\ldots)x^{-1}\pm\int x^{-\frac{3}{2}}"
       r"\,\mathrm{d}x$ or equivalent. Indices do not need to be processed e.g. $x^{-2}\left(\ldots x^{\frac{3}{2}}\pm"
       r"\ldots x\right)\pm\int\ldots x^{-3}\left(\ldots x^{\frac{3}{2}}\pm\ldots x\right)\mathrm{d}x$",
       r"ALT: Alternative method: integration by parts — A1: $-(2x^{\frac{1}{2}}-3)x^{-1}+\int x^{-\frac{3}{2}}\,\mathrm{d}x$ "
       r"or $x^{-2}\left(\frac{4}{3}x^{\frac{3}{2}}-3x\right)-\int-2x^{-3}\left(\frac{4}{3}x^{\frac{3}{2}}-3x\right)"
       r"\mathrm{d}x$ o.e.",
       r"ALT: Alternative method: integration by parts — dM1: For completing the integration by parts method achieving at "
       r"least one term with a correct index (the index does not need to be processed) and terms with the same index do not "
       r"need to be collected for this mark",
       r"ALT: Alternative method: integration by parts — A1: As above in the main scheme (see notes)"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", ALG, "2.6", 2, LATEX["02a"],
      [r"M1 (AO 1.1b): $(\mathrm{f}(4)=)\ 2\times4^3-3a\times4^2+4b+8a=0$. Notes: Attempts $\mathrm{f}(4)=0$ leading to an "
       r"equation in $a$ and $b$ only. Condone slips. The $=0$ may be implied by further work for this mark. Attempts using "
       r"algebraic division score M0A0.",
       r"A1* (AO 1.1b): $128+4b=40a\Rightarrow32+b=10a$ *. Notes: Simplifies and rearranges to the given answer with no "
       r"errors. There must be at least one intermediate stage of working between their first expression or equation and "
       r"the given answer and $=0$ must be correctly seen at some point in their solution or at the start e.g. stating "
       r"$\mathrm{f}(4)=0$. Isw if they achieve the given answer but then attempt to make $a$ or $b$ the subject. Minimum "
       r"acceptable is e.g. $128-48a+4b+8a\Rightarrow128-40a+4b=0\Rightarrow32+b=10a$. Note: "
       r"$128-48a+4b+8a\Rightarrow128+4b=40a\Rightarrow32+b=10a$ is M1A0* (we do not see $=0$ correctly at some point or "
       r"e.g. $\mathrm{f}(4)=0$)"],
      False, 4),
    e("02b", "2(b)", ALG, "2.6, 2.4", 4, LATEX["02b"],
      [r"M1 (AO 1.1b): $\mathrm{f}(2)=2\times2^3-3a\times2^2+2b+8a=0\Rightarrow8+b=2a$. Notes: Note that there are many "
       r"different equations which can be formed. Sight of $a=3$ or $b=-2$ or $k=3$ scores the first 3 marks BUT answers "
       r"with no working – send to review. Attempts $\mathrm{f}(2)=0$ to form another equation in $a$ and $b$. Does not need "
       r"to be simplified. Condone slips substituting in 2 (but not if there is a clear intention to substitute in $-2$) and "
       r"$=0$ may be implied by further work. Accept attempts to divide algebraically by $x-2$: e.g. condone slips but they "
       r"must have a quadratic quotient $2x^2\pm(\ldots a\pm\ldots)x$ and proceed as far as a remainder of the form "
       r"$\ldots a\pm\ldots b\pm\ldots$ which is then set equal to 0. [The mark scheme shows the long division of "
       r"$2x^3-3ax^2+bx+8a$ by $x-2$, with quotient $2x^2+(-3a+4)x+(b-6a+8)$ and remainder $-4a+2b+16=0$.] You may also see "
       r"an attempt at the grid method: in this method condone slips but they need to proceed as far as a quadratic quotient "
       r"of the form $2x^2\pm(\ldots a\pm\ldots)x$ and the bottom right cell of the form $\ldots a\pm\ldots b\pm\ldots$ which "
       r"is then set equal to $8a$. Look out for other valid methods such as: multiplying out $\mathrm{f}(x)=(2x+k)(x-4)"
       r"(x-2)$ to achieve a cubic where the coefficients of $x^2$ and $x$, and the constant term are all in terms of $k$, "
       r"and equating coefficients to form two more simultaneous equations; algebraically dividing $2x^3-3ax^2+bx+8a$ by "
       r"$x^2-6x+8$ and setting their remainder equal to zero. Look for a quotient of the form $2x\pm\ldots a\pm\ldots$; "
       r"substituting $b=10a-32$ into $\mathrm{f}(x)$ so that the polynomial coefficients are in terms of $a$ only (or "
       r"equivalently all in $b$ only) and using $\mathrm{f}(2)=0$ to form an equation in one variable. Send to review if "
       r"you are unsure.",
       r"dM1 (AO 2.1): Solve simultaneously $\Rightarrow a=\ldots$ or $\Rightarrow b=\ldots$ Notes: Attempts to solve their "
       r"equations simultaneously to find a value for $a$ or $b$ (or they may proceed directly to finding a value for $k$). "
       r"This may be done on a calculator. You do not need to check their method for solving. It is dependent on the "
       r"previous method mark.",
       r"A1 (AO 1.1b): $a=3$ or $b=-2$ or $k=3$. Notes: $a=3$ or $b=-2$ or $k=3$",
       r"A1 (AO 1.1b): $(\mathrm{f}(x)=)\ (2x+3)(x-4)(x-2)$. Notes: $(\mathrm{f}(x)=)\ (2x+3)(x-4)(x-2)$ (All on one line) "
       r"(Stating the values of $a$, $b$ and $k$ alone does not score this mark). Allow to be scored if seen in (c).",
       r"ALT: Alternative Further Maths method using the sum and product of the roots — M1: "
       r"$\alpha+\beta+\gamma=\frac{3a}{2}\Rightarrow4+2-\frac{k}{2}=\frac{3a}{2}$ or $\alpha\beta\gamma=-\frac{8a}{2}"
       r"\Rightarrow4\times2\times\left(-\frac{k}{2}\right)=-\frac{8a}{2}$",
       r"ALT: Alternative Further Maths method using the sum and product of the roots — A1: "
       r"$\alpha+\beta+\gamma=\frac{3a}{2}\Rightarrow4+2-\frac{k}{2}=\frac{3a}{2}$ and $\alpha\beta\gamma=-\frac{8a}{2}"
       r"\Rightarrow4\times2\times\left(-\frac{k}{2}\right)=-\frac{8a}{2}$ (Less likely but possible to see "
       r"$\alpha\beta+\beta\gamma+\alpha\gamma=\frac{b}{2}\Rightarrow4\times2+2\times\left(-\frac{k}{2}\right)+4\times"
       r"\left(-\frac{k}{2}\right)=\frac{b}{2}$)",
       r"ALT: Alternative Further Maths method using the sum and product of the roots — dM1 A1 A1: See notes above"],
      False, 4),
    e("02c", "2(c)", ALG, "2.6, 2.8", 2, LATEX["02c"],
      [r"B1 (AO 1.1b): (i) 3. Notes: 3 (listing the actual roots only is B0)",
       r"B1ft (AO 2.2a): (ii) 12. Notes: 12 only. Follow through on their $2x+k\Rightarrow-\frac{3k}{2}$ if $k<-8$"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", VEC, "9.3", 2, LATEX["03a"],
      [r"M1 (AO 1.1a): $\overrightarrow{PQ}=(3-9)\mathbf{i}+(-5+8)\mathbf{j}$. Notes: Note that work seen must be used in "
       r"the relevant part. If there is a lack of labelling of parts then award the marks to the parts which leads to the "
       r"highest total overall. Attempts subtraction either way round (does not need to be evaluated). It cannot be awarded "
       r"for adding the two vectors. If no method shown it may be implied by one correct component or sight of "
       r"$\mp6\mathbf{i}\pm3\mathbf{j}$.",
       r"A1 (AO 1.1b): $=-6\mathbf{i}+3\mathbf{j}$. Notes: Correct answer. Allow $-6\mathbf{i}+3\mathbf{j}$ or "
       r"$\begin{pmatrix}-6\\3\end{pmatrix}$ but do not allow $\begin{pmatrix}-6\mathbf{i}\\3\mathbf{j}\end{pmatrix}$ isw "
       r"once a correct answer is seen."],
      False, 8),
    e("03b", "3(b)", VEC, "9.5, 9.2, 3.1", 2, LATEX["03b"],
      [r"M1 (AO 3.1a): Gradient of $PQ=\frac{-5--8}{3-9}\left(=-\frac{1}{2}\right)$ and Gradient of $QR=\frac{18}{9}(=2)$ "
       r"or $\left|\overrightarrow{PQ}\right|=\sqrt{\text{“}(-6)\text{”}^2+\text{“}3\text{”}^2}\ (=3\sqrt{5})$ and "
       r"$\left|\overrightarrow{QR}\right|=\sqrt{9^2+18^2}\ (=9\sqrt{5})$ and $\left|\overrightarrow{PR}\right|="
       r"\sqrt{\text{“}3\text{”}^2+\text{“}21\text{”}^2}\ (=15\sqrt{2})$. Notes: Condone lack of labelling / poor notation "
       r"for lengths/angles provided the intention is clear. Attempts to find the gradient of the line $PQ$ and the gradient "
       r"of the line $QR$. If they find the reciprocals of both they must be labelled e.g. $\frac{\mathrm{d}x}{\mathrm{d}y}$ "
       r"o.e. (but not gradient or $m$). Do not allow sign slips for this mark. Alternatively they may find the lengths "
       r"$PQ$, $QR$ and $PR$ or $PQ^2$, $QR^2$ and $PR^2$. Be aware of Further Maths methods such as attempting the dot "
       r"product $\begin{pmatrix}-6\\3\end{pmatrix}\cdot\begin{pmatrix}9\\18\end{pmatrix}=(-6\times9)+(3\times18)$",
       r"A1* (AO 2.4): e.g. shows that $-\frac{1}{2}\times2=-1$ and deduces angle $PQR=90^\circ$ * or e.g. shows "
       r"$\left|\overrightarrow{PQ}\right|^2+\left|\overrightarrow{QR}\right|^2=\left|\overrightarrow{PR}\right|^2$ and "
       r"deduces angle $PQR=90^\circ$ *. Notes: Correct working and conclusion that angle $PQR=90^\circ$: using gradients or "
       r"their reciprocals they need to state or show that the product is equal to -1 o.e. or refer to the values being "
       r"negative reciprocals of each other; using Pythagoras’ Theorem they must state or show that "
       r"$\left|\overrightarrow{PQ}\right|^2+\left|\overrightarrow{QR}\right|^2=\left|\overrightarrow{PR}\right|^2$; using the "
       r"cosine rule and finding angle $PQR=90^\circ$; using the scalar dot product they must show that "
       r"$\begin{pmatrix}-6\\3\end{pmatrix}\cdot\begin{pmatrix}9\\18\end{pmatrix}=0$. In all cases there must be some sort "
       r"of minimal conclusion that angle $PQR=90^\circ$ e.g. “hence right angle” or if they start with a preamble it is "
       r"acceptable to state “hence proven”, “QED” or a tick. Use of e.g. cosine rule resulting in $90^\circ$ is "
       r"sufficient."],
      False, 8),
    e("03c", "3(c)", VEC, "9.5, 9.2", 4, LATEX["03c"],
      [r"M1 (AO 2.1): Attempts to find the length $PQ$ and at least one of $QR$ or $PS$ using Pythagoras’ Theorem correctly "
       r"e.g. $\left|\overrightarrow{PQ}\right|=\sqrt{\text{“}(-6)\text{”}^2+\text{“}3\text{”}^2}$ and either "
       r"$\left|\overrightarrow{QR}\right|=\sqrt{9^2+18^2}$ or $\left|\overrightarrow{PS}\right|=\sqrt{\text{“}27\text{”}^2"
       r"+\text{“}54\text{”}^2}$. Notes: Condone lack of labelling / poor notation for lengths provided the intention is "
       r"clear. Correct use of Pythagoras’ Theorem to find the length of $PQ$ and at least one of $QR$ or $PS$. Must be used "
       r"or seen in (c) to score this mark. Condone working using rounded or truncated values.",
       r"A1ft (AO 1.1b): $\left|\overrightarrow{PQ}\right|=\text{“}\sqrt{45}\text{”}\ \left(=3\sqrt{5}\right)$ and either "
       r"$\left|\overrightarrow{QR}\right|=\sqrt{405}\ \left(=9\sqrt{5}\right)$ or $\left|\overrightarrow{PS}\right|="
       r"27\sqrt{5}$. Notes: Correct length of $PQ$ and at least one of $QR$ or $PS$. Follow through on their vectors for "
       r"$PQ$ and $PS$ but $QR$ must be $\sqrt{405}$ or equivalent. Lengths do not need to be simplified but they must be "
       r"exact. Must be used or seen in (c) to score this mark.",
       r"dM1 (AO 3.1a): e.g. Area $=\frac{1}{2}\times\left(\text{“}9\sqrt{5}\text{”}+\text{“}27\sqrt{5}\text{”}\right)\times"
       r"\text{“}\sqrt{45}\text{”}$ or $\frac{1}{2}\times4\times\text{“}9\sqrt{5}\text{”}\times\text{“}3\sqrt{5}\text{”}$. "
       r"Notes: Correct method to find the area of the trapezium. It is dependent on the first method mark and the method to "
       r"find any lengths must be correct. This may be achieved by calculating $\frac{1}{2}\times4\left|QR\right|\times"
       r"\left|PQ\right|$. Alternatively, they may find the area of a rectangle + triangle so look for: e.g. "
       r"$\left|PQ\right|\times\left|QR\right|+\frac{1}{2}\times(\left|PS\right|-\left|QR\right|)\times\left|PQ\right|="
       r"\text{“}\sqrt{45}\text{”}\times\text{“}9\sqrt{5}\text{”}+\frac{1}{2}\times\text{“}18\sqrt{5}\text{”}\times"
       r"\text{“}\sqrt{45}\text{”}$. Note that there are other combinations of lengths to find the area of a rectangle and "
       r"either add or subtract triangles as appropriate. Condone working using rounded values.",
       r"A1 (AO 1.1b): $=270$. Notes: 270",
       r"ALT: Alt (c) “Shoelace method” or other methods using position vectors (the mark scheme's diagram shows "
       r"$P(9,-8)$, $Q(3,-5)$, $R(12,13)$ and $S(36,46)$, with $QR\parallel PS$, $PQ=3\sqrt{5}$, $QR=9\sqrt{5}$, "
       r"$PS=27\sqrt{5}$ and $PR=15\sqrt{2}$) — M1: Correct method to find either the position vector of $R$ or the position "
       r"vector of $S$. May be seen as coordinates. Check any diagram drawn.",
       r"ALT: Alt (c) “Shoelace method” — A1: $R$ has position vector $12\mathbf{i}+13\mathbf{j}$ and $S$ has position vector "
       r"$36\mathbf{i}+46\mathbf{j}$ (or equivalent). May be seen as coordinates. Check any diagram drawn.",
       r"ALT: Alt (c) “Shoelace method” — dM1: Correct method to find the area of the trapezium via the “shoelace” method: "
       r"$\frac{1}{2}\left|(9\times(-5)+3\times13+12\times46+36\times(-8))-(3\times(-8)+12\times(-5)+36\times13+9\times46)"
       r"\right|=\frac{1}{2}\left|258-798\right|$",
       r"ALT: Alt (c) “Shoelace method” — A1: 270"],
      False, 8),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", TRIG, "5.1", 3, LATEX["04a"],
      [r"M1 (AO 1.1b): $\frac{x}{\sin30^\circ}=\frac{x+3}{\sin140^\circ}$. Notes: Do not allow verification attempts using "
       r"$x=10.5$ by substituting into formulae. Recognises the need to apply the sine rule and attempts to use it with the "
       r"sides in the correct positions to form an equation in $x$. Alternatively, uses trigonometric ratios twice to form "
       r"an equation in $x$ e.g. $BE=x\sin40^\circ\Rightarrow\sin30^\circ=\frac{x\sin40^\circ}{x+3}$ or e.g. "
       r"$AF=x\sin40^\circ\Rightarrow\cos60^\circ=\frac{x\sin40^\circ}{x+3}$. May also see an attempt at Pythagoras’ "
       r"Theorem: $BD^2=BE^2+DE^2\Rightarrow(x+3)^2=((x+3)\cos30^\circ)^2+(x\sin40^\circ)^2$. [The mark scheme's diagram "
       r"adds $E$ on $AC$ extended below $B$ and $F$ above $A$, with $BE=AF=(x\sin40)$ cm and the angle $40^\circ$ at $C$.]",
       r"dM1 (AO 3.1a): $2x\sin140-x=3$. Notes: Attempts to rearrange the equation by collecting terms in $x$ on one side of "
       r"the equation and non $x$ terms on the other. It is dependent on the previous method mark. Condone sign slips only "
       r"in their rearrangement but allow miscopying/arithmetical slips when rounding. Do not allow this mark to be scored "
       r"for proceeding directly to a numerical value for $x$. In the attempt using Pythagoras’ Theorem, look for an attempt "
       r"to multiply out and rearrange to form a three-term quadratic.",
       r"A1* (AO 1.1b): $x=10.5$ *. Notes: Achieves 10.5 with sufficient working shown. Condone invisible brackets to be "
       r"recovered. They must have achieved either a correct expression for $x$ or $x(2\sin140^\circ-1)=3$ o.e. before "
       r"stating 10.5 or better. It is acceptable to use rounded decimals for trigonometric values provided they are "
       r"correct to at least 3sf. e.g. $\sin140^\circ=0.64278\ldots$ e.g. $2x=\frac{x+3}{\sin140^\circ}\Rightarrow "
       r"x=\frac{1.5}{\sin40^\circ-0.5}=10.5$ scores M1dM1A1* (allow 0.5 in their initial equation for sin30 and allow "
       r"interchanging of equivalent angles such as sin140 and sin40) e.g. $x\sin140=(x+3)\sin30^\circ\Rightarrow "
       r"x=\frac{3\sin30^\circ}{0.643-\sin30^\circ}=10.5$ scores M1dM1A1* e.g. $\frac{x}{\sin30^\circ}=\frac{x+3}"
       r"{\sin140^\circ}\Rightarrow x\sin140^\circ=(x+3)\sin30^\circ\Rightarrow x=10.505\ldots$ is M1dM0A0* (insufficient "
       r"working shown as they do not reach an expression for $x$ or $x(2\sin140^\circ-1)=3$ o.e.) In the method using "
       r"Pythagoras’ Theorem usual rules apply for solving a quadratic but it cannot be awarded for proceeding to the answer "
       r"via a calculator (e.g. must see use of the quadratic formula or completing the square)."],
      True, 10),
    e("04b", "4(b)", TRIG, "5.1", 2, LATEX["04b"],
      [r"M1 (AO 3.1a): $AB^2=8.5^2+13.5^2-2\times8.5\times13.5\times\cos\text{“}150\text{”}\Rightarrow AB=\ldots$ Notes: "
       r"Applies the cosine rule correctly using $150^\circ$ (or $180^\circ-30^\circ$ seen if incorrect) for angle $ADB$ "
       r"with the correct numerical lengths by attempting to substitute in $x=10.5$ or better and proceeds to obtain a value "
       r"for $AB$. Look for other methods such as finding lengths $DC$ and $CE$ followed by using trigonometry or "
       r"Pythagoras’ Theorem on triangle $ABE$.",
       r"A1 (AO 1.1b): $AB=$ awrt 21.3 (cm). Notes: awrt 21.3 (cm) Units not required but if they are given they must be "
       r"correct. (Using full calculator display 21.29959497/using $x=10.5$ gives 21.28…)",
       r"ALT: Alt (b) (various longer methods; the mark scheme's diagram shows $AD=8.5$ cm, $BD=13.5$ cm, $BC=10.5$ cm, "
       r"$DC=3.648\ldots$ cm, $CE=8.047\ldots$ cm, $BE=6.75\ldots$ cm, with angle $ADB=150^\circ$) — M1: A complete attempt to "
       r"find a value for $AB$, but condone slips. The angles and lengths in formulae should be in the correct positions, but "
       r"allow slips when rearranging or calculating values. e.g. $BE=6.75\ldots$, $AE=8.5+3.648\ldots+8.047\ldots=20\ldots"
       r"\Rightarrow AB=\sqrt{6.75\ldots^2+20\ldots^2}=\ldots$",
       r"ALT: Alt (b) — A1: awrt 21.3 (cm) Units not required but if they are given they must be correct. (Using full "
       r"calculator display 21.29959497/using $x=10.5$ gives 21.28…)"],
      True, 10),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", ALG, "2.7", 3, LATEX["05a"],
      [r"M1 (AO 1.1b): (i) [Sketch: a positive reciprocal curve, branches in quadrants 1 and 3, shifted up with asymptote "
       r"$y=3$ and crossing the $x$-axis at $-2$.] Notes: Either: a correct positive reciprocal graph shape with both branches "
       r"anywhere on a set of axes (ignore any dashed lines / scale and just look at the graph shape drawn); $x=-2$ is the "
       r"only point of intersection of their graph with the axes. Condone labelled as $(0,-2)$. Allow if they state the "
       r"coordinates $(-2, 0)$ next to the graph instead but not just $x=-2$. Condone poor curvature provided there is not an "
       r"intention to draw a maximum or minimum for either of the branches. Condone where the branches approach an undrawn "
       r"horizontal asymptote if the left-hand branch is slightly above the right-hand branch as long as it does not appear "
       r"intentional.",
       r"A1 (AO 1.1b): (i) Correct sketch. Notes: Fully correct graph with an intersection labelled at $x=-2$ on the graph "
       r"(condone labelled as $(0,-2)$). If two horizontal or vertical asymptotes are drawn or a vertical asymptote which is "
       r"not the $y$-axis then this mark cannot be scored. (unless the vertical asymptote is labelled as 0 or $x=0$) Allow if "
       r"they state the coordinates $(-2, 0)$ next to the graph instead but not just $x=-2$. [The mark scheme then shows "
       r"example candidate sketches marked M1A1 and M1A0.]",
       r"B1 (AO 1.1b): (ii) Asymptotes: $y=3$, $x=0$. Notes: If no graph is drawn then this mark cannot be scored. $y=3$, "
       r"$x=0$ cao (not $x\neq0$) which must be correct for their graph. Check by the question but if there is a "
       r"contradiction then the equations stated in (ii) of the work takes precedence. Cannot be for just stating 0 "
       r"underneath the $y$ axis and 3 on a dashed horizontal line if present."],
      False, 12),
    e("05b", "5(b)", ALG, "2.4", 2, LATEX["05b"],
      [r"M1 (AO 1.1b): e.g. $\frac{6}{x}+3=3x^2-4x-10\Rightarrow6+3x=3x^3-4x^2-10x$. Notes: Sets "
       r"$\frac{6}{x}+3=3x^2-4x-10$ and rearranges to form a cubic equation. Terms do not need to be collected or all on one "
       r"side.",
       r"A1* (AO 1.1b): $3x^3-4x^2-13x-6=0$ *. Notes: $3x^3-4x^2-13x-6=0$ with no errors seen. There must be at least one "
       r"stage of intermediate working before achieving the given answer. e.g. $\frac{6}{x}+3=3x^2-4x-10\Rightarrow "
       r"3x^3-4x^2-13x-6=0$ is M1A0*. e.g. $\frac{6}{x}+3=3x^2-4x-10\Rightarrow6+3x=3x^3-4x^2-10x\Rightarrow "
       r"3x^3-4x^2-13x-6=0$ is M1A1*"],
      False, 12),
    e("05c", "5(c)", ALG, "2.6, 2.3", 4, LATEX["05c"],
      [r"M1 (AO 3.1a): e.g. dividing $3x^3-4x^2-13x-6$ by $3x+2$ to get a quotient $x^2-2x\pm\ldots$ Notes: Note that "
       r"proceeding to three linear factors with no working is M0A0dM0A0. A quadratic factor is required first. Attempts to "
       r"algebraically divide $3x^3-4x^2-13x-6$ by $3x+2$ or compare coefficients to achieve $(x^2-2x\ldots)$ or "
       r"$(x^2\pm\ldots x-3)$ (or via inspection). Alternatively, attempts to algebraically divide $3x^3-4x^2-13x-6$ by "
       r"$x+\frac{2}{3}$ or compare coefficients to achieve $(3x^2-6x\pm\ldots)$ or $(3x^2\pm\ldots x-9)$ (or via "
       r"inspection). May use the grid method so they must proceed as far as the diagonal for $x^2$ being correct and "
       r"achieving $x^2-2x$ on the top. (They should reach the same point if dividing by $x+\frac{2}{3}$) Any attempts to "
       r"use $(x+1)$ or $(x-3)$ rather than $(3x+2)$ from the given root please send to review.",
       r"A1 (AO 1.1b): $x^2-2x-3\ (=0)$ or $3x^2-6x-9\ (=0)$. Notes: $x^2-2x-3\ (=0)$ or $3x^2-6x-9\ (=0)$",
       r"dM1 (AO 1.1b): e.g. $(3x+2)(x-3)(x+1)=0\Rightarrow x=\ldots$ Notes: Attempts to solve their resulting quadratic by "
       r"factorising, using the formula or completing the square. Usual rules apply for solving a quadratic by either of "
       r"these methods. They cannot simply write down the roots. It is dependent on the previous method mark. Note "
       r"$(3x^2-6x-9)\Rightarrow(x-3)(x+1)\Rightarrow x=\ldots$ is dM0A0",
       r"A1cso (AO 1.1b): $x=-1$, $x=3$. Notes: $x=-1$, $x=3$ only (ignore any reference to $x=-\frac{2}{3}$) Condone "
       r"invisible brackets if recovered or implied by further work. Withhold this mark if they reject one of the two "
       r"solutions."],
      False, 12),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", SEQ, "4.1", 2, LATEX["06a"],
      [r"M1 (AO 1.1b): e.g. ${}^{12}C_1\times a=-\frac{15}{2}$. Notes: Correct equation to find $a$ e.g. "
       r"$12a=-\frac{15}{2}$ or ${}^{12}C_1\times a=-7.5$ or $\frac{12!}{11!}a=-\frac{15}{2}$. Condone if $x$ is present on "
       r"both sides of their equation. Also allow attempts using $a=-\frac{5}{8}$ e.g. ${}^{12}C_1\times-\frac{5}{8}="
       r"-\frac{15}{2}$",
       r"A1* (AO 1.1b): $12a=-\frac{15}{2}\Rightarrow a=-\frac{5}{8}$ *. Notes: Rearranges to achieve the given answer with "
       r"no errors and sufficient steps shown i.e. the binomial coefficient must have been evaluated first. e.g. "
       r"$\binom{12}{1}\times a=-\frac{15}{2}\Rightarrow12a=-\frac{15}{2}\Rightarrow a=-\frac{5}{8}$ is M1A1*. Minimum "
       r"acceptable $12a=-\frac{15}{2}\Rightarrow a=-\frac{5}{8}$ is M1A1*. ${}^{12}C_1\times a=-7.5\Rightarrow "
       r"a=-\frac{5}{8}$ is M1A0*. Do not penalise if solutions contain $x$ as well e.g. $12ax=-\frac{15}{2}x\Rightarrow "
       r"a=-\frac{5}{8}$ is M1A1*. Attempts using $a=-\frac{5}{8}$ must show the binomial coefficient evaluated and there "
       r"must be a conclusion such as “hence shown”, QED. $12\times-\frac{5}{8}x=-\frac{15}{2}x$ with e.g. hence shown is "
       r"M1A1*. We do not need to be concerned with any workings related to other terms."],
      False, 16),
    e("06b", "6(b)", SEQ, "4.1", 2, LATEX["06b"],
      [r"M1 (AO 1.1b): ${}^{12}C_2\times a^2=k\Rightarrow k=\ldots$ Notes: If the expression is seen in (a) it must be used "
       r"in (b) to score. Correct expression or equation to find $k$ and proceeds to find a value for $k$ e.g. "
       r"$66a^2=k\Rightarrow k=\ldots$ May be implied by a correct answer or $\frac{825}{32}x^2$. Allow use of $\frac{5}{8}$ "
       r"for $a$.",
       r"A1 (AO 1.1b): $k=\frac{825}{32}$. Notes: $\frac{825}{32}$ o.e. e.g. 25.78125. isw if they round after a correct "
       r"answer is seen. Do not accept $\frac{825}{32}x^2$ but allow the coefficient to be circled or underlined to identify "
       r"the answer."],
      False, 16),
    e("06c", "6(c)", SEQ, "4.1", 2, LATEX["06c"],
      [r"M1 (AO 3.1a): $1-\frac{5}{8}x=\frac{17}{16}\Rightarrow x\ (=-0.1)\Rightarrow1-\frac{15}{2}\times(\text{“}-0.1"
       r"\text{”})+\text{“}\frac{825}{32}\text{”}\times(\text{“}-0.1\text{”})^2$. Notes: A correct strategy to find the "
       r"appropriate value of $x$ e.g. $1-\frac{5}{8}x=\frac{17}{16}\Rightarrow x=\ldots(=-0.1)$ and substitutes their value "
       r"of $x$ into $1-\frac{15}{2}x+kx^2$ using their value for $k$. Their $x=-0.1$ embedded in the expression is "
       r"sufficient. Accept a sign slip on the substitution of their $x$ and/or $k$ provided the embedded values are seen. "
       r"Maybe implied by their value for the expression (you may need to check this on your calculator if the substitution "
       r"is not seen). Alternatively, attempts $\left(1+\frac{1}{16}\right)^{12}=1+12\times\frac{1}{16}+\frac{12\times11}{2}"
       r"\times\left(\frac{1}{16}\right)^2$. Do not withhold this mark if they attempt incorrectly to find additional terms "
       r"of the binomial expansion.",
       r"A1 (AO 1.1b): = awrt 2.0078. Notes: awrt 2.0078 (full answer on calculation is 2.0078125 or allow "
       r"$\frac{257}{128}$). This value with no working seen can score both marks. isw if they round after a correct answer "
       r"is seen. Note that if they find the term in $x^3$ this is $-\frac{6875}{128}x^3$ which using $x=-0.1$ in the "
       r"expansion up to and including this would give awrt 2.0615 which can score both marks. Note that $2.06988999\ldots$ "
       r"is the value from the calculator for $\left(\frac{17}{16}\right)^{12}$ which is likely to score M0A0 (unless some "
       r"method is shown for finding the value of $x$ and substituting in)"],
      False, 16),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", EXP, "6.6, 3.1", 4, LATEX["07a"],
      [r"M1 (AO 1.1b): $\log_{10}a=3.3$ or $\log_{10}b=\frac{2.1-3.3}{6}\ (=-0.2)$. Notes: Attempts an equation in $a$ or "
       r"$b$. Score for $\log_{10}a=3.3$ or $\log_{10}b=\frac{2.1-3.3}{6}\ (=-0.2)$. Condone an incorrectly evaluated "
       r"gradient provided $\frac{2.1-3.3}{6}$ o.e. was attempted (may be seen as two simultaneous equations). "
       r"Alternatively, forms a correct linear equation in $\log_{10}P$ and $x$. Do not penalise if base 10 is missing. May "
       r"be implied by a correct unsimplified value for $a$ or $b$. (which could be truncated rather than rounded for $b$)",
       r"A1 (AO 1.1b): $a=10^{3.3}$ or $b=10^{-0.2}$. Notes: A correct unsimplified value for $a$ or $b$. This may be within "
       r"the linear equation in the alternative method e.g. $P=10^{3.3}\times10^{-0.2x}$",
       r"dM1 (AO 3.1a): $a=10^{3.3}$ and $b=10^{\text{“}-0.2\text{”}}$. Notes: A correct method to find unsimplified values "
       r"for $a$ and $b$. Allow use of their $-0.2$ found from a correct attempt at the gradient of the line. Alternatively, "
       r"correctly uses laws of indices to achieve $P=10^{3.3}\times10^{\text{“}-0.2\text{”}x}$. It is dependent on the "
       r"previous method mark. May be implied by their final correct equation.",
       r"A1 (AO 3.3): $P=1995\times0.6310^x$. Notes: Complete equation with $a=$ awrt 1995 and $b=$ awrt 0.6310 (condone "
       r"0.631)",
       r"ALT: Second scheme column — M1 (AO 1.1b): e.g. $\log_{10}P=3.3-0.2x$ or $\log_{10}P=3.3+\frac{2.1-3.3}{6}x$",
       r"ALT: Second scheme column — dM1 (AO 3.1a): $P=10^{3.3-0.2x}=10^{3.3}\times10^{-0.2x}$"],
      True, 18),
    e("07b", "7(b)", EXP, "6.7", 1, LATEX["07b"],
      [r"B1 (AO 3.2a): The concentration (in parts per million) 1 km from the chimney. Notes: Must refer to concentration "
       r"(or e.g. parts per million) and 1km o.e. Condone use of emitted for measured e.g. “concentration of smoke particles "
       r"emitted 1km from the chimney” Do not accept “amount of smoke particles” or referring to when $x=1$ (not in "
       r"context)"],
      True, 18),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", DIFF, "7.3, 7.2", 3, LATEX["08a"],
      [r"M1 (AO 3.1a): $\left(\frac{\mathrm{d}y}{\mathrm{d}x}=\right)3x^2-14=-2$ or $\frac{\mathrm{d}}{\mathrm{d}x}"
       r"(\pm(\text{curve}-\text{line}))=\pm(3x^2-12)=0$. Notes: On EPEN this is M1A1A1* we are marking this as M1dM1A1*. "
       r"Differentiates the cubic to achieve $px^2+q$ and sets equal to $-2$. Note setting the linear and cubic equations "
       r"equal to each other and solving is M0 (no use of calculus) but, they may differentiate $\pm$(cubic-line) to achieve "
       r"$px^2+q$ and set equal to 0 which is M1. Alternatively, in either approach, differentiates to achieve $px^2+q$ and "
       r"substitutes in $x=2$",
       r"dM1 (AO 1.1b): e.g. $3x^2-14=-2\Rightarrow3x^2=12\Rightarrow x=\ldots$ Notes: Proceeds from their equation to find a "
       r"real value for $x$ with at least one intermediate stage of working. e.g. $px^2=-q\Rightarrow x=\ldots$ or e.g. via "
       r"factorisation $(3)(x+2)(x-2)=0\Rightarrow x=\ldots$ Accept proceeding directly to $x=\sqrt{\frac{14-2}{3}}$ or "
       r"$\pm2$. In the alternative, it is for substituting in 2 into their $3(2)^2-14=\ldots$ or $3(2)^2-12=\ldots$",
       r"A1* (AO 2.2a): $x=2$ only *. Notes: 2 only (the solution of $-2$ does not need to be found) $\pm2$ without selecting "
       r"2/ rejecting $-2$ is A0*. In the alternative they conclude that $x=2$."],
      True, 20),
    e("08b", "8(b)", ALG, "2.4, 2.6", 2, LATEX["08b"],
      [r"M1 (AO 1.1b): e.g. Substitutes $x=-4$ into $y=x^3-14x+23$ and $y=-2x+7$. Notes: Work may be seen in (a) but must "
       r"be used in (b) to score. Mark the general method / do not be concerned by slips in their working. Either e.g. "
       r"substitutes $x=-4$ into $y=x^3-14x+23$ and $y=-2x+7$. Sight of $-4$ embedded in the equations is sufficient; "
       r"substitutes $x=-4$ into one equation to find $y$ and then uses this value to find $x$ in the other equation; equates "
       r"the cubic and the linear expressions, rearranges ($=0$) and then substitutes $x=-4$ into the equation or expression, "
       r"factorises using $(x-2)^2$ to find a linear factor (e.g. inspection / division), algebraically divides by $(x+4)$ at "
       r"some point to get a remainder of 0, or factorises using $(x-2)$ to find a quadratic factor which they attempt to "
       r"factorise",
       r"A1* (AO 2.4): Correct solution + conclusion *. Notes: A correct solution with conclusion but allow recovery of "
       r"missing/invisible brackets. Either: finds $y=15$ when $x=-4$ for both equations; finds $y=15$ using one equation and "
       r"uses this to find that $x=-4$ for the other; verifies that $x=-4$ is a solution of the cubic – linear $=0$ with no "
       r"errors seen; solves cubic – linear $=0$ and finds the linear factor $(x+4)$ leading to the root $x=-4$. There must "
       r"be a conclusion: if they find $x=-4$ then a tick, QED, underline, proven. If they find e.g. $y=15$ for both they "
       r"must state $x=-4$ e.g.“(same $y$ values so) $x=-4$” Note that stating the coordinates $(-4, 15)$ is insufficient. "
       r"SC: $-2x+7=x^3-14x+23\Rightarrow x^3-12x+16\ (=0)\Rightarrow x=-4,2$ so $x=-4$ scores M1A0*"],
      True, 20),
    e("08c", "8(c)", INT, "8.3, 8.2", 5, LATEX["08c"],
      [r"M1 (AO 1.1b): $\int\left(x^3-14x+23\right)\mathrm{d}x=\frac{x^4}{4}-7x^2+23x\ (+c)$. Notes: No integration seen "
       r"(using the integration button on a calculator) will score 0 marks. Integrates the equation of the curve or in the "
       r"alternative method it is for integrating curve-line and achieving at least two terms with a correct index out of "
       r"$\ldots x^4\pm\ldots x^2\pm\ldots x$. Also look out for a transformation approach translating the cubic down 3 units "
       r"and integrating $\int\left(x^3-14x+20\right)\mathrm{d}x=\frac{x^4}{4}-7x^2+20x$",
       r"A1 (AO 1.1b): $\int\left(x^3-14x+23\right)\mathrm{d}x=\frac{x^4}{4}-7x^2+23x\ (+c)$. Notes: "
       r"$\frac{x^4}{4}-7x^2+23x$ or $\frac{x^4}{4}-6x^2+16x$ (ignore any constant of integration). Allow unsimplified but "
       r"the indices must be processed. Look out for $\frac{x^4}{4}-7x^2+20x$ if the cubic has been translated down 3 units. "
       r"Do not penalise poor notation for this mark.",
       r"dM1 (AO 1.1b): $=\left(\frac{2^4}{4}-7\times2^2+23\times2\right)-\left(\frac{(-4)^4}{4}-7(-4)^2+23(-4)\right)$. "
       r"Notes: Correct limits of 2 and $-4$ used for their integral (which may be for the line or curve). It is dependent on "
       r"the previous method mark. Evidence of substituting in 2 and $-4$ into their integrated expression must be seen. "
       r"(e.g. $22-(-140)$). In the alternative method the dM1 (and next dM1) are scored at the same time for substituting "
       r"in the correct limits.",
       r"dM1 (AO 3.1a): Area $=\int_{-4}^{2}\left(x^3-14x+23\right)\mathrm{d}x-\frac{1}{2}\times(15+3)\times(2--4)="
       r"\left(\frac{2^4}{4}-7\times2^2+23\times2\right)-\left(\frac{(-4)^4}{4}-7(-4)^2+23(-4)\right)-54$. Notes: Correct "
       r"strategy to find the shaded area. It is dependent on the first method mark only but the limits must be correct. In "
       r"the alternative method this mark is scored for sight of 2 and $-4$ for their integral which do not have to be "
       r"substituted in. The method to find any areas e.g. trapezium, rectangle, triangle must be correct and the method of "
       r"adding or subtracting to find the shaded area must be correct. Condone slips in evaluating. Note using the "
       r"transformation approach they will need to subtract the area of the triangle $0.5\times6\times(15-3)$",
       r"A1* (AO 2.1): Area $=108$ *. Notes: 108 following from a rigorous argument showing all stages and correct notation "
       r"used when integrating (the integral sign and the $\mathrm{d}x$ either side of their expression seen at least once "
       r"and should not be present after integration has been completed)",
       r"ALT: Alt(c) — M1 (AO 3.1a): $\int\left(x^3-14x+23\right)-(-2x+7)\,\mathrm{d}x=\int\left(x^3-12x+16\right)"
       r"\mathrm{d}x$",
       r"ALT: Alt(c) — A1 (AO 1.1b): $=\frac{x^4}{4}-6x^2+16x\ (+c)$",
       r"ALT: Alt(c) — dM1 dM1 (AO 1.1b, 1.1b): Area $=\left(\frac{2^4}{4}-6\times2^2+16\times2\right)-\left(\frac{(-4)^4}{4}"
       r"-6(-4)^2+16(-4)\right)$",
       r"ALT: Alt(c) — A1* (AO 2.1): Area $=108$ *"],
      True, 20),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", EXP, "6.4", 1, LATEX["09a"],
      [r"B1 (AO 1.1b): $2p$. Notes: $2p$ o.e."],
      False, 24),
    e("09b", "9(b)", EXP, "6.4", 2, LATEX["09b"],
      [r"M1 (AO 1.2): $\log_a100=\log_a4+\log_a25$. Notes: Uses the laws of logs to write $\log_a100$ correctly as a sum of "
       r"logs e.g. $\log_a100=\log_a4+\log_a25$ e.g. $\log_a100=\log_a4+\log_aa^q$ e.g. $\log_a100=2\log_a2+2\log_a5$ e.g. "
       r"$\log_a100=\frac{1}{2}\log_a16+\frac{1}{2}\log_a625$ e.g. $\log_a100=\log_a50+\log_a2$. May also be implied by "
       r"expressions in $p$ or $q$ or a mixture of both e.g. $(p+q=)\ \log_a16+\log_a25=\log_a400=\log_a4+\log_a100"
       r"\Rightarrow p+q-\log_a4=\log_a100$. Look out for more complex versions of above e.g. e.g. "
       r"$\log_a100=\log_a4+\log_aa^q$ which are acceptable. Do not penalise the omission of base $a$",
       r"A1 (AO 1.1b): $\log_a16^{\frac{1}{2}}+\log_a25=\frac{1}{2}p+q$. Notes: $\frac{1}{2}p+q$ o.e. Correct answer scores "
       r"full marks but withhold this mark if incorrect log work is seen e.g. $\log_a100=\log_a4\times\log_a25$ or "
       r"$\log_a100=4\log_a25$"],
      False, 24),
    e("09c", "9(c)", EXP, "6.4", 2, LATEX["09c"],
      [r"M1 (AO 3.1a): e.g. $\log_a80\times\log_a3.2=(\log_a16+\log_a5)\times(\log_a16-\log_a5)$. Notes: Uses both the "
       r"addition and subtraction laws of logs to write the full expression of $\log_a80\times\log_a3.2$ correctly in terms "
       r"of any of the following: $\log_a16\ (=p)$; $\log_a4\ \left(=\frac{p}{2}\right)$; $\log_a2\ \left(=\frac{p}{4}"
       r"\right)$; $\log_a5\ \left(=\frac{q}{2}\right)$; $\log_a25\ (=q)$ e.g. $\log_a80\times\log_a3.2=(2\log_a4+\log_a5)"
       r"\times(\log_a16-\log_a5)$. You may see other viable solutions using e.g. $\log_a\frac{1}{5}$, $\log_a\frac{1}{4}$ "
       r"but they will need to proceed to either e.g. $\log_a5$ (an integer value) or proceed to an expression in terms of "
       r"$p$ or $q$. Do not penalise the omission of base $a$. May be implied by equivalent expressions in $p$ or $q$ or a "
       r"mixture of both.",
       r"A1 (AO 1.1b): $\left(p+\frac{1}{2}q\right)\times\left(p-\frac{1}{2}q\right)$ or $p^2-\frac{1}{4}q^2$. Notes: "
       r"$\left(p+\frac{1}{2}q\right)\times\left(p-\frac{1}{2}q\right)$ or $p^2-\frac{1}{4}q^2$ o.e. (does not need to be "
       r"simplified) Correct answer scores full marks but withhold this mark if incorrect log work is seen in their "
       r"solution. isw once a correct answer in terms of $p$ and $q$ is seen."],
      False, 24),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", COORD, "3.2, 3.1", 4, LATEX["10a"],
      [r"B1 (AO 2.2a): tangent $=-2\to$ normal $=\frac{1}{2}$. Notes: Attempts to implicitly differentiate the equation of "
       r"the circle please send to review. Deduces that the gradient between $P$ and $Q$ is $\frac{1}{2}$. Condone this mark "
       r"to be scored for sight of $\frac{1}{2}$ o.e which may be on the diagram / by the question. May be implied by further "
       r"work or seen in an equation. Look out for e.g. $\frac{-(3--1)}{k^2-2k-k-8}=-2$ o.e. (negative reciprocal of the "
       r"gradient $PQ$ set equal to $-2$) which implies this mark.",
       r"M1 (AO 1.1b): $\frac{k^2-2k-k-8}{3--1}$. Notes: Attempts to find an expression for the gradient of $PQ$ in terms of "
       r"$k$ (may be implied) Score for the expression which may be seen in their working. Condone one sign slip in their "
       r"expression. May be seen in $(y_2-y_1)=m(x_2-x_1)$ which does not need to be rearranged.",
       r"dM1 (AO 1.1b): $\frac{1}{2}=\frac{k^2-2k-k-8}{3--1}\Rightarrow\frac{1}{2}=\frac{k^2}{4}-\frac{2k}{4}-\frac{k}{4}-2$. "
       r"Notes: Sets their gradient of $PQ$ equal to $\frac{1}{2}$ (or the negative reciprocal of the gradient $PQ$ set "
       r"equal to $-2$) and proceeds to a quadratic so that the fraction for the gradient has been split up into separate "
       r"terms. e.g. $k^2-2k-k-8=2$. Terms do not need to be collected for this mark and they do not all need to be on the "
       r"same side of the equation. Coefficients do not need to be integers. Condone slips in their rearrangement. It is "
       r"dependent on the first method mark. If using $(y_2-y_1)=m(x_2-x_1)$ the mark would be scored substituting "
       r"$m=\frac{1}{2}$",
       r"A1* (AO 2.1): $\Rightarrow k^2-3k-10=0$ *. Notes: Achieves given answer with no errors seen. Must see $=0$. They "
       r"must have achieved a quadratic which is not the given answer before proceeding to the given answer.",
       r"ALT: Alt(a) forming/using linear equations with the coordinates of $P$ and $Q$ — B1: As above in the main scheme / "
       r"notes",
       r"ALT: Alt(a) forming/using linear equations with the coordinates of $P$ and $Q$ — M1: Uses one pair of coordinates "
       r"to form the equation of a straight line with a gradient of $\frac{1}{2}$ e.g. $k^2-2k=\frac{3}{2}+c$ or "
       r"$k+8=-\frac{1}{2}+c$ (Condone one sign slip) e.g. $y-k-8=\frac{1}{2}(x+1)$. May use the coordinates for $Q$ to form "
       r"the equation of a straight line with a gradient of $-2$",
       r"ALT: Alt(a) forming/using linear equations with the coordinates of $P$ and $Q$ — dM1: Uses both pairs of "
       r"coordinates and proceeds via a correct method to an equation in $k$ only e.g. $k+8=-\frac{1}{2}+c\Rightarrow "
       r"c=k+8.5$, $k^2-2k=\frac{3}{2}+c\Rightarrow k^2-2k=\frac{3}{2}+\text{“}k+8.5\text{”}$. Condone slips in their "
       r"rearrangement. You will need to look carefully at how they use the coordinates and equations. It is dependent on "
       r"the first method mark.",
       r"ALT: Alt(a) forming/using linear equations with the coordinates of $P$ and $Q$ — A1*: As above in the main scheme / "
       r"notes"],
      True, 26),
    e("10b", "10(b)", COORD, "3.2, 2.3", 4, LATEX["10b"],
      [r"B1 (AO 2.3): $k=5$. Notes: Deduces that $k$ is 5 only. May be seen by the question or in (a) which is fine but if "
       r"both roots are found then 5 must be selected/used in further work or the negative root is rejected. May be implied "
       r"by the $y$ coordinate of $P$. Note that B0B1ftM1A0 is possible",
       r"B1ft (AO 1.1b): $y$ coordinate of $P$ is 13. Notes: $y$ coordinate of $P$ is 13 Check on the diagram or may be "
       r"implied by further work such as in the equation of the circle. If there is a contradiction between the diagram and "
       r"the main body of the work then the main body of the work takes precedence. Follow through on their positive value "
       r"of $k$ (add 8 to their value for $k$). Ignore if they find a value for $P$ using their negative value of $k$ as well",
       r"M1 (AO 3.1a): Attempts $PQ\ \left(=\sqrt{(3--1)^2+(\text{“}25-15-8\text{”})^2}\right)$ (or $PQ^2$). Notes: Finds the "
       r"distance $PQ$ (or $PQ^2$) using their $y$ coordinates from their chosen value of $k$ (which may be negative). The "
       r"value of $k$ must be consistently used to find $P$ and $Q$. If they find the distance $PQ$ twice (using each value "
       r"of $k$ to find coordinates of $P$ and $Q$) then condone this mark to be scored. The expression is sufficient, but "
       r"they must be attempting $\sqrt{(3--1)^2+(y_2-y_1)^2}$ o.e. (or $(3--1)^2+(y_2-y_1)^2$ o.e). May be implied by sight "
       r"of 20 or $\sqrt{20}$",
       r"A1 (AO 1.1b): $(x+1)^2+(y-13)^2=20$. Notes: $(x+1)^2+(y-13)^2=20$ only or equivalent e.g. "
       r"$x^2+y^2+2x-26y+150=0$"],
      True, 26),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", EXP, "6.7, 6.1", 2, LATEX["11a"],
      [r"M1 (AO 1.1b): At $t=0$, $V_A=100+20=120\Rightarrow p=2\times\text{“}120\text{”}$. Notes: Attempts to find the price "
       r"per gram of metal $A$ at $t=0$, and then doubles this to find the value of $p$. Can be implied by 240. An expression "
       r"must be evaluated to score this mark",
       r"A1 (AO 1.1b): $(p=)\ 240$. Notes: 240 only (withhold this mark if they find $V_B=240$ but proceed to state $p$ as a "
       r"different value)"],
      False, 30),
    e("11b", "11(b)", EXP, "6.2, 6.7, 6.3", 4, LATEX["11b"],
      [r"M1 (AO 3.1b): $\ldots\mathrm{e}^{0.04T}=\ldots\mathrm{e}^{-0.02T}$. Notes: Candidates who state that "
       r"$\frac{\mathrm{d}V_B}{\mathrm{d}t}=\text{“}4.8\text{”}\mathrm{e}^{-0.02T}$ can still score full marks question (they "
       r"had already determined that they needed to take the modulus of the gradient function) May be in terms of $t$ or "
       r"$T$. Attempts to set $\pm\frac{\mathrm{d}V_A}{\mathrm{d}t}$ equal to $\pm\frac{\mathrm{d}V_B}{\mathrm{d}t}$. Look for "
       r"an equation of the form $p\mathrm{e}^{0.04T}=q\mathrm{e}^{-0.02T}$ where $p$ and $q$ are constants or may be implied "
       r"by further work. e.g. $\mathrm{e}^{\pm0.06T}=\ldots$ (it cannot be for awrt 29.9). Do not allow "
       r"$\ldots T\mathrm{e}^{0.04T}=\ldots T\mathrm{e}^{-0.02T}$",
       r"A1ft (AO 1.1b): $0.8\mathrm{e}^{0.04T}=\text{“}4.8\text{”}\mathrm{e}^{-0.02T}$. Notes: "
       r"$0.8\mathrm{e}^{0.04T}=\text{“}4.8\text{”}\mathrm{e}^{-0.02T}$. Follow through on their positive value for $p$. May "
       r"be implied by further work which is not awrt 29.9.",
       r"dM1 (AO 3.1a): $\ldots\mathrm{e}^{0.04T}=\ldots\mathrm{e}^{-0.02T}\Rightarrow\mathrm{e}^{\pm0.06T}=\ldots$ Notes: "
       r"Rearranges their $\frac{\mathrm{d}V_A}{\mathrm{d}t}=-\frac{\mathrm{d}V_B}{\mathrm{d}t}$ which cannot be the original "
       r"functions to $r\mathrm{e}^{\pm0.06T}=s$ where $r\times s>0$. $\frac{\mathrm{d}V_B}{\mathrm{d}t}=\text{“}4.8\text{”}"
       r"\mathrm{e}^{-0.02T}\Rightarrow0.8\mathrm{e}^{0.04T}=\text{“}4.8\text{”}\mathrm{e}^{-0.02T}$ is allowed (see note at "
       r"the start of (b)). Condone slips. It is dependent on the first method mark. If they take lns of both sides first e.g. "
       r"$0.8\mathrm{e}^{0.04T}=\text{“}4.8\text{”}\mathrm{e}^{-0.02T}\Rightarrow\ln0.8+0.04T=\ln\text{“}4.8\text{”}-0.02T$ "
       r"they need to rearrange to $\pm0.06T=\ldots$ by adding / subtracting.",
       r"A1cso (AO 1.1b): $(T=)$ awrt 29.9 (months). Notes: awrt 29.9 provided evidence of solving "
       r"$0.8\mathrm{e}^{0.04T}=4.8\mathrm{e}^{-0.02T}$ is seen. i.e. they cannot proceed from $\mathrm{e}^{\pm0.06T}=\ldots$ "
       r"to the awrt 29.9 in one step. We must see either an expression for $t$ or e.g. taking lns of both sides. Condone "
       r"$(T=)\ \frac{50\ln6}{3}$ or others in the form $(T=)\ a\ln b$ where $a$ and $b$ are rational constants e.g. "
       r"$\frac{\ln6}{0.06}$. It cannot be scored for an expression."],
      False, 30),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", ALG, "2.6, 2.1", 5, LATEX["12a"],
      [r"B1 (AO 1.1b): (Surface area $=$) $2xy+\frac{\pi x^2}{4}$. Notes: Note that different sections of the perimeter may "
       r"be completed separately and brought together in a final line. Most marks will only be scored at this point – send "
       r"to review if unsure. Correct expression for the surface area in terms of $x$ and $y$ only (may be in an equivalent "
       r"form). May be implied by their equation set equal to 100 or their rearranged form.",
       r"M1 (AO 3.4): $2xy+\frac{\pi x^2}{4}=100\Rightarrow y=\frac{400-\pi x^2}{8x}=\frac{50}{x}-\frac{\pi x}{8}$. Notes: "
       r"Sets their expression in $x$ and $y$ equal to 100 and rearranges to make $y$ (or $2y$ or $4y$) the subject. Do not "
       r"be concerned by the mechanics of their rearrangement. May be implied by further work or can be scored for a "
       r"different valid substitution into their expression for the perimeter.",
       r"B1 (AO 1.1b): $(P=)\ 2x+4y+\frac{2\pi x}{4}$. Notes: Correct expression for the perimeter in terms of $x$ and $y$ "
       r"(may be in an equivalent form) and may be implied by an expression for the perimeter in terms of $x$ if they have "
       r"substituted in for their $y$ straight away (which may be incorrect or have been rearranged incorrectly)",
       r"M1 (AO 3.4): $(P=)\ 2x+4\left(\frac{400-\pi x^2}{8x}\right)+\frac{2\pi x}{4}$. Notes: Attempts to substitute their "
       r"$y$ into their perimeter to produce an expression or equation in just $x$. Condone invisible brackets for this mark. "
       r"Condone slips provided the intention is clear.",
       r"A1* (AO 2.1): $P=2x+\frac{200}{x}$ *. Notes: $P=2x+\frac{200}{x}$ cso (Condone the omission of $P=$ on the final "
       r"line if it is seen on an earlier line of working) Allow Perimeter $=$. Do not withhold this mark if missing/invisible "
       r"brackets are recovered in their working."],
      True, 34),
    e("12b", "12(b)", DIFF, "7.3, 7.2", 4, LATEX["12b"],
      [r"M1 (AO 1.1b): $\left(\frac{\mathrm{d}P}{\mathrm{d}x}=\right)2-200x^{-2}$. Notes: Attempts to differentiate the given "
       r"expression for $P$ achieving an answer of the form $A\pm Bx^{-2}$. Condone candidates who do not achieve the given "
       r"answer but their derivative differentiates to the required form to score this mark (and possibly dM1)",
       r"A1 (AO 1.1b): $\left(\frac{\mathrm{d}P}{\mathrm{d}x}=\right)2-200x^{-2}$. Notes: $2-200x^{-2}$ o.e.",
       r"dM1 (AO 3.1b): $2-200x^{-2}=0\Rightarrow x=\ldots$ Notes: Sets their derivative of the form $A-Bx^{-2}$, "
       r"$A\times B>0$ equal to 0 and rearranges to find a value for $x$. It is dependent on the previous method mark. Condone "
       r"slips in their rearrangement. May proceed directly to the answer.",
       r"A1 (AO 1.1b): $x=10$. Notes: 10 cao (provided a correct derivative is seen) $\pm10$ is A0 isw if they attempt to "
       r"find $P$"],
      True, 34),
    e("12c", "12(c)", DIFF, "7.3", 2, LATEX["12c"],
      [r"M1 (AO 1.1b): $\left(\frac{\mathrm{d}^2P}{\mathrm{d}x^2}=\right)\text{“}400\text{”}x^{-3}\Rightarrow\text{“}400"
       r"\text{”}\times10^{-3}>0$. Notes: Note that attempts only evaluating the gradient either side of $x=10$ is M0A0. Finds "
       r"$\frac{\mathrm{d}^2P}{\mathrm{d}x^2}$ of the form $Ax^{-3}$ o.e. and either considers the sign or evaluates for their "
       r"positive $x$",
       r"A1 (AO 2.4): e.g. $\frac{\mathrm{d}^2P}{\mathrm{d}x^2}\ (=0.4)>0$ hence minimum (perimeter). Notes: Requires: "
       r"$\left(\frac{\mathrm{d}^2P}{\mathrm{d}x^2}=\right)400x^{-3}$ (condone this mark if "
       r"$\frac{\mathrm{d}^2y}{\mathrm{d}x^2}$ is written or any other incorrect notation); reference to $400x^{-3}$ being "
       r"$>0$ for $x>0$, or by using either a correct calculation (0.4 o.e.), a correct numerical expression or the algebraic "
       r"expression and referencing that it is $>0$ for $x=10$; correct conclusion e.g. hence min, shown, tick, QED. Condone "
       r"“minimum value of $x$”"],
      True, 34),
    e("12d", "12(d)", ALG, "2.6, 2.4", 2, LATEX["12d"],
      [r"M1 (AO 3.4): e.g. $y=\frac{400-\pi\times\text{“}10\text{”}^2}{8\times\text{“}10\text{”}}$. Notes: Either: "
       r"substitutes their value of $x$ into any of their equations involving $y$ or their expression for $y$ from part (a) "
       r"(unless restarted) to find a value for $y$; uses their value of $x$ to find their minimum value of $P$ using the "
       r"given expression for $P$, and then uses their $x$ and their $P$ to find a value for $y$; attempts to find the value "
       r"of $x$ when $y=1$ (allow to be solved directly from a calculator once a three-term quadratic has been formed); "
       r"attempts to find the value of $P$ using the given expression for $P$, their value for $x$ and $y=1$. Condone slips "
       r"provided the intention is clear of their intended method.",
       r"A1 (AO 2.2a): e.g. $y=1.07$ (m) so yes this would be suitable. Notes: awrt 1.1 m and concludes would be suitable "
       r"(yes is sufficient or a tick) Note that “yes suitable because e.g.1.07 > 0 is A0” (it had to be greater than 1). If "
       r"they find the value for $x$ when $y=1$ it requires a correct comparison of awrt 10.1 with 10 so yes suitable. If they "
       r"find the value of $P$ using $x=10$ and $y=1$ it requires a correct comparison of awrt 39.7 with 40 so yes suitable"],
      True, 34),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", TRIG, "5.3", 4, LATEX["13a"],
      [r"M1 (AO 1.1b): $7\sin^2\theta-4\sin\theta\cos\theta=4\Rightarrow7\tan^2\theta-4\tan\theta=\frac{4}{\cos^2\theta}$. "
       r"Notes: There are various ways of proceeding to the given answer. May work in $\theta$ or another variable which is "
       r"acceptable. Condone a mixture of $\theta$ and e.g. $x$ in the same equation or expression within their working. "
       r"Condone poor notation e.g. $\cos\theta^2$, $\sin^2+\cos^2=1$ provided the intention is clear. You may see multiple "
       r"attempts so score the attempt which is most complete. Score for any one of the following (somewhere in their same "
       r"attempt which may already have errors in their working): divides all terms by $\cos^2\theta$; uses "
       r"$\tan\theta=\frac{\sin\theta}{\cos\theta}$ (or $\sec\theta=\frac{1}{\cos\theta}$); uses the identity "
       r"$\pm\sin^2\theta\pm\cos^2\theta=\pm1$ (or $\pm1\pm\tan^2\theta=\pm\sec^2\theta$)",
       r"dM1 (AO 1.1b): $\Rightarrow3\tan^2\theta-4\tan\theta+\frac{4\sin^2\theta}{\cos^2\theta}-\frac{4}{\cos^2\theta}=0$. "
       r"Notes: Score for any two of the following (somewhere in their same attempt which may already have errors in their "
       r"working): divides all terms by $\cos^2\theta$; uses $\tan\theta=\frac{\sin\theta}{\cos\theta}$ (or "
       r"$\sec\theta=\frac{1}{\cos\theta}$); uses the identity $\pm\sin^2\theta\pm\cos^2\theta=\pm1$ (or "
       r"$\pm1\pm\tan^2\theta=\pm\sec^2\theta$). It is dependent on the previous method mark.",
       r"ddM1 (AO 2.1): $\frac{4\sin^2\theta-4}{\cos^2\theta}=-4\frac{\cos^2\theta}{\cos^2\theta}=-4\Rightarrow "
       r"3\tan^2\theta-4\tan\theta-4=0$. Notes: A full attempt to rearrange the equation to the form "
       r"$a\tan^2\theta+b\tan\theta+c=0$. It is dependent on the previous two method marks. When rearranging condone sign "
       r"slips or a missing trailing bracket only.",
       r"A1* (AO 1.1b): $3\tan^2\theta-4\tan\theta-4=0$ *. Notes: Proceeds to the given answer with all steps shown and no "
       r"errors other than what is condoned (see above). Condone a missing trailing bracket only. The final answer must be in "
       r"terms of $\theta$ and written using the correct notation. Note they may work in reverse from "
       r"$3\tan^2\theta-4\tan\theta-4=0$ to $7\sin^2\theta-4\sin\theta\cos\theta=4$ or meet somewhere in the middle. In these "
       r"cases there must be some minimal conclusion e.g. QED or tick. The first two method marks should be applied in the "
       r"same way as the main scheme. The dM1 mark will be scored for reaching a form of $\sin\theta(d\sin\theta+e\cos\theta)"
       r"=f$"],
      False, 38),
    e("13b", "13(b)", TRIG, "5.4", 4, LATEX["13b"],
      [r"B1 (AO 1.1b): Roots: $-\frac{2}{3}$, 2. Notes: Answers with no working scores 0 marks. Beware of correct angles "
       r"following incorrect roots which cannot score the A marks. Roots: $-\frac{2}{3}$, 2",
       r"M1 (AO 1.1b): $\tan^{-1}\left(\text{“}-\frac{2}{3}\text{”}\right)=\ldots$ or $\tan^{-1}(\text{“}2\text{”})=\ldots$ "
       r"Notes: Attempts to find at least one of the angles for one of their roots. This may be implied by a correct answer. "
       r"You may need to check this on your calculator.",
       r"A1 (AO 1.1b): Two of awrt 63, awrt 146, awrt 243, awrt 326. Notes: Two of awrt 63, awrt 146, awrt 243, awrt 326 "
       r"(must come from a correct root)",
       r"A1 (AO 1.1b): All four of awrt 63.4, awrt 146.3, awrt 243.4, awrt 326.3. Notes: All four of awrt 63.4, awrt 146.3, "
       r"awrt 243.4, awrt 326.3 and no others in the range. Withhold the final mark if they solve for $4\alpha$ (and "
       r"subsequently divide their angles by 4)"],
      False, 38),
    e("13c", "13(c)", TRIG, "5.4, 2.8", 1, LATEX["13c"],
      [r"B1 (AO 2.2a): awrt 735.9. Notes: awrt 735.9"],
      False, 38),

    # ---------------- Q14 ----------------
    e("14", "14", PROOF, "1.1, 2.6", 4, LATEX["14"],
      [r"M1 (AO 1.1b): Sets up the proof by exploring when $n=2k$ or $n=2k+1$ e.g. $(2k)^2+5(2k)=\ldots k^2+\ldots k$ or "
       r"$(2k+1)^2+5(2k+1)=\ldots k^2+\ldots k+\ldots$ Notes: Main scheme algebraic method using e.g. $n=2k$ and "
       r"$n=2k\pm1$. You will need to look at both cases and mark the one which is fully correct first. Allow a different "
       r"variable to $k$ and may be different letters for odd and even. Condone use of $n$ as a variable for the first three "
       r"marks. There should be no errors in the algebra for the A marks but allow e.g. invisible brackets to be "
       r"“recovered”. Sets up the proof by exploring when $n$ is odd or even e.g. $n=2k$ or $n=2k+1$ (or equivalent), and "
       r"either expands and achieves a quadratic expression (which may be unsimplified) or allow to factorise e.g. "
       r"$2k(2k+5)$ or e.g. $(2k+2)(2k+7)$. Condone slips. e.g. $2k(2k+5)=2k^2+10k$ or slips when collecting terms.",
       r"A1 (AO 2.2a): e.g. $4k^2+10k$ or $4k^2+14k+6$ and shows or gives a reason why the expression is even (see notes). "
       r"Notes: Correct quadratic expression (which may be unsimplified) for $n^2+5n$ for either odds or evens and shows or "
       r"gives a reason why the expression is even. They must have fully multiplied out or the quadratic expression must be "
       r"factorised completely. e.g. $4k^2+10k=2(2k^2+5k)$ (which is even) e.g. $4k^2+14k+6=2(2k^2+7k+3)$ (which is even) "
       r"e.g. $\frac{4k^2+10k}{2}=2k^2+5k$ (hence even) e.g. “2 is a factor of both terms”, “all divisible by 2” (so even). "
       r"If a reason is given as well as an algebraic expression it must be correct e.g. $4k^2+10k=2(2k^2+5k)$ so even as "
       r"can be multiplied by 2 can score M1A1 but $\frac{4k^2+10k}{2}=2k^2+5k$ so it can be divided by 2 so even is M1A0 "
       r"(needs to say divisible by 2). Do not isw if they simplify their quadratic incorrectly. Note that they do not have "
       r"to state that the expression is even if they conclude for all cases at the end.",
       r"dM1 (AO 2.1): Explores when $n=2k$ and $n=2k+1$ eg $(2k)^2+5(2k)=\ldots k^2+\ldots k$ and $(2k+1)^2+5(2k+1)="
       r"\ldots k^2+\ldots k+\ldots$ Notes: Explores when $n$ is odd and when $n$ is even leading to two quadratic "
       r"expressions (may be factorised) for when $n=2k$ and $n=2k+1$ (or equivalent) (see first M1 for guidance)",
       r"A1* (AO 2.4): e.g. $4k^2+10k$ and $4k^2+14k+6$ and shows or gives a reason why both of the expressions are even "
       r"(see notes) hence $n^2+5n$ is even for all $n\ (\in\mathbb{N})$ (or equivalent). Notes: Requires: correct quadratic "
       r"expression for $n^2+5n$ for both odds and evens; shows or gives a reason for each why the expressions are even (see "
       r"first A1 for guidance); makes a concluding overall statement. “Hence $n^2+5n$ is even for all "
       r"$n\ (\in\mathbb{N})$” (or equivalent). Note that if they have stated for each separate case that the expression is "
       r"even then allow minimal statements of “hence proven”, “statement proved”, “QED”, tick. Do not isw this mark if they "
       r"simplify their quadratic incorrectly. [The mark scheme tabulates $n^2+5n$ for $n=2k-3,\ldots,2k+3$: "
       r"$4k^2-2k-6$, $4k^2+2k-6$, $4k^2+6k-4$, $4k^2+10k$, $4k^2+14k+6$, $4k^2+18k+14$, $4k^2+22k+24$.]",
       r"ALT: Alternative methods: Algebraic with logic example — SC 1010: e.g. $n^2+5n=n(n+5)$. When $n$ is odd then $n+5$ "
       r"is even so odd x even is even. When $n$ is even then $n+5$ is odd so even x odd is even. Both cases must be "
       r"considered to score any marks and scores SC 1010 if fully correct",
       r"ALT: Further Maths method (proof by induction) – you may see these but please send to review for TLs or above to "
       r"mark — M1: Assumes true for $n=k$, substitutes $n=k+1$ into $n^2+5n$, multiplies out the brackets and attempts to "
       r"simplify to a quadratic expression (which may be unsimplified) e.g. $k^2+7k+6$ Condone arithmetical slips",
       r"ALT: Further Maths method (proof by induction) — A1: $(\mathrm{f}(k+1)=3k^2+3k+1+6(k+1)=)\ "
       r"k^2+5k+2k+6=\mathrm{f}(k)+2(k+3)$ which is even + even = even",
       r"ALT: Further Maths method (proof by induction) — dM1: Attempts to substitute $n=1\Rightarrow1^2+5\times1=6$ (which "
       r"is true) (Condone arithmetical slips evaluating)",
       r"ALT: Further Maths method (proof by induction) — A1*: Explains that it is true when $n=1$; if it is true for $n=k$ "
       r"then it is true for $n=k+1$; therefore it is true for all $n\ (\in\mathbb{N})$"],
      False, 42),
]

# Examiner report, sentence by sentence, in report order (the General Comments
# are not attached to any question). A sentence that mentions another part
# only in passing is tagged with the part it is about.
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "This was a very accessible question on integration to start the paper and most candidates were able to "
            "score well.", NO),
        (W, "Most candidates attempted to separate the fraction into two terms and achieved at least one correct index."),
        (W, r"The first term caused problems for some with errors such as $x^{-\frac{5}{2}}$, $x^{\frac{3}{2}}$, "
            r"$x^{\frac{1}{2}}$.", NO),
        (W, "A few ended up with three terms as they had added or subtracted $x^{-2}$."),
        (W, r"A few tried to integrate the numerator and denominator or wrote $(2\sqrt{x}-3)x^{-2}$ but did not expand the "
            r"brackets and integrated both inside and outside separately."),
        (W, "Those who had scored the first M1 usually were able to raise the power by one on at least one term with a "
            "correct index and score the next method mark.", NO),
        (W, "Several made errors when processing the indices and ended up subtracting by one on at least one of the "
            "terms."),
        (W, "A few made errors with the coefficients."),
        (W, "The most common mistake was to forget the $+c$."),
    ],
    "02": [
        (W, "This question which required use of the factor theorem and solving simultaneous equations provided an "
            "opportunity to score a good number of marks."),
        (W, "Some candidates found this question to be accessible and scored full marks or nearly full marks."),
        ({"b"}, "Others however, encountered difficulties, particularly with part (b) and dropped marks accordingly."),
        (W, "Some candidates lost marks because they did not pay heed to the instruction to show all stages of their "
            "working."),
        ({"a"}, r"In part (a), most candidates made progress and attempted to employ the factor theorem, as the question "
                r"had instructed, and used $\mathrm{f}(4)=0$ to obtain the given answer."),
        ({"a"}, "Some lost the second mark for not including ‘$=0$’ anywhere in their proof or for algebraic slips."),
        ({"a"}, "A few candidates attempted algebraic division and scored nothing in part (a)."),
        ({"b"}, r"For part (b), many candidates continued with the theme of the question and applied the factor theorem a "
                r"second time using $\mathrm{f}(2)=0$, obtaining a second equation in $a$ and $b$."),
        ({"b"}, "This was the easiest way to proceed.", BACK),
        ({"b"}, "Surprisingly however, a significant number of candidates chose more difficult routes and progressed "
                "instead with entirely different methods."),
        ({"b"}, "Many candidates had some success by expanding $(2x+k)(x-4)(x-2)$ and then comparing coefficients with "
                "the original function, obtaining further equations."),
        ({"b"}, "Others attempted to divide the original function by $(x-2)$ or sometimes by $x^2-6x+8$, using long "
                "division."),
        ({"b"}, "This approach was less successful because of the algebra involved and few reached a second equation.",
         BACK),
        ({"b"}, "There were also a few attempts using the sum and product of the roots of a cubic equation."),
        ({"b"}, r"Some candidates attempted to use $\mathrm{f}(2)=0$ with $\mathrm{f}(x)=(2x+k)(x-4)(x-2)$ and made no "
                r"progress in part (b)."),
        ({"b"}, "Generally, when candidates obtained further correct equations in part (b), they were then able to "
                "successfully solve them simultaneously to obtain values of $a$, $b$ or $k$ which were usually correct."),
        ({"b"}, r"This was often followed by the correct factorised expression for $\mathrm{f}(x)$, although a number of "
                r"candidates failed to write this down and lost the final mark.", BACK),
        ({"b"}, "A few correct answers were presented with no working, which gained no credit in part (b)."),
        ({"c"}, "Part (c) was answered quite well, even by those who had made little or no progress in part (a) or part "
                "(b).", NO),
        ({"c"}, "In part (i) many identified that there were three real roots, although stating that there were two real "
                "roots was a common incorrect answer."),
        ({"c"}, "Some also lost the mark because they listed the roots without stating how many there were."),
        ({"c"}, r"In part (ii) many realised that the largest root was 12, although $\frac{4}{3}$ was a common incorrect "
                r"answer."),
    ],
    "03": [
        (W, "Overall, this question proved fairly tricky with lots of candidates losing marks throughout.", NO),
        ({"a"}, r"In part (a), most candidates knew they needed to subtract the vectors, there were a few signs slips when "
                r"doing this and quite a few candidates subtracted the wrong way round so found $\overrightarrow{QP}$ "
                r"instead.", NO),
        ({"a"}, "There were a small but significant number who added the vectors."),
        ({"b"}, r"In part (b), quite a few candidates seemed unclear as to how to show $PQR=90^\circ$; some made no attempt "
                r"whilst others used the given fact within their proof often finding two angles in a triangle and showing "
                r"that they were complementary, but they had assumed a right angle in order to utilise trigonometry which "
                r"achieved no marks."),
        ({"b"}, "The candidates who tended to be most successful at this were the ones who attempted to show the required "
                "property using gradients.", NO),
        ({"b"}, "There were a small number of signs slips and incorrect attempts at gradients but overall, this approach "
                "was usually successful.", NO),
        ({"b"}, r"Quite a lot attempted to use Pythagoras’ theorem but there were a significant number who would only find "
                r"$\left|\overrightarrow{PQ}\right|$ and $\left|\overrightarrow{QR}\right|$ and either did not attempt to "
                r"find $\left|\overrightarrow{PR}\right|$ or had a poor attempt at finding it.", NO),
        ({"b"}, "It is of note that for those who successfully used Pythagoras’ theorem to complete the proof, diagrams "
                "proved useful.", NO),
        ({"b"}, "There were a small number who attempted the dot product or cosine rule and usually these attempts were "
                "good enough to achieve the marks.", NO),
        ({"b"}, "It was disappointing that the most common reasons for the M1A0 score were due to incorrect/incomplete "
                "solutions or simply a lack of conclusion.", NO),
        ({"c"}, "Part (c) proved quite tricky for a lot of candidates many of whom did not seem to have fully understood "
                "the shape with which they were working."),
        ({"c"}, "Those who were successful usually had a good diagram identifying it as a trapezium and were able to find "
                "the area.", NO),
        ({"c"}, "There were a number of attempts at splitting the shape up into a rectangle and triangle or 2 triangles, "
                "but often there was a misunderstanding about which lengths were which and how they should be combined to "
                "find the area."),
        ({"c"}, "The most common error in the rectangle and triangle approach was that the candidates failed to spot that "
                r"the triangle was a right-angled triangle so could use $\left|\overrightarrow{QP}\right|$ as the "
                r"‘height.’"),
        ({"c"}, "The two triangles approach would also often have the same issue."),
        ({"c"}, "There were quite a few attempts that treated the shape either as just a rectangle or just a triangle."),
        ({"c"}, "It was pleasing however to see that whilst a large number of candidates were unsure of how to proceed to "
                "find the area many did at least acknowledge the need to attempt the lengths of various vectors, which "
                "generally resulted in two marks being awarded.", NO),
    ],
    "04": [
        ({"a", "b"}, "This question using advanced trigonometry was generally answered well and as part (a) was a “show” "
                     "question, this provided great accessibility for part (b), which candidates were typically more "
                     "successful in completing.", NO),
        ({"a"}, "In part (a), whilst the vast majority of candidates were able to correctly state, and substitute into, "
                "the sine rule, a large proportion of them demonstrated a poor understanding of algebra and were unable "
                "to rearrange the equation to make $x$ the subject."),
        ({"a"}, "Many candidates, whilst arriving at the correct answer via valid algebra, used inefficient or inelegant "
                "techniques."),
        ({"a"}, r"Only a few students misquoted the sine rule e.g. misplacing the angle/opposite side pairings, using "
                r"$30^\circ$ and $140^\circ$ instead of $\sin30^\circ$ and $\sin140^\circ$, and writing $\sin x$ and "
                r"$\sin(x+3)$."),
        ({"a"}, r"It was disappointing that for a “show” question where the focus is on providing a rigorous argument, "
                r"that some candidates failed to work to at least 3 significant figures, instead approximating values "
                r"such as $\sin140^\circ$ too much and/or too early, which led to the answer mark being lost.", NO),
        ({"a"}, "Candidates should also be discouraged from working with approximated values when answering these types "
                "of questions."),
        ({"a"}, "There was evidence of candidates resorting to using the equation solver on the calculator to find the "
                "correct value for $x$ after having got stuck, or having made an error, whilst attempting to solve their "
                "equation, too, hence the requirement for ideally rearranging to find an expression for $x$ before "
                "achieving the given answer."),
        ({"b"}, "Candidates were more confident when using the cosine rule and so part (b) resulted in many achieving the "
                "correct answer."),
        ({"b"}, "This may reflect the fact that they simply needed to substitute in the given correct value for $x$ into "
                "the formula and then do the numeric processing i.e. no algebraic work was required.", BACK),
        ({"b"}, r"The vast majority of candidates realised that the most efficient solution used triangle $ABD$ with an "
                r"angle of $150^\circ$."),
        ({"b"}, "Those that chose to use triangle $ABC$ tended to arrive at the correct answer, although they probably "
                "took longer to do so, as there was an additional side length to calculate.", NO),
        ({"b"}, "A number of candidates did not substitute side lengths into the cosine rule, instead working with $x$ and "
                "$x+3$."),
        ({"b"}, "They then attempted to manipulate the resulting algebraic expressions.", BACK),
        ({"b"}, "Some failed to realise that the value of $x$ was given; others noticed this at the last minute, after "
                "considerable algebra.", NO),
        ({"b"}, "This was another example where, had candidates read the question carefully and realised the requirement "
                "was to give the answer to 3 significant figures, then the need to work algebraically was no longer "
                "necessary as an exact answer would not need be required.", BACK),
    ],
    "05": [
        (W, "This question tested candidates’ ability to sketch graphs and to be able to divide polynomials."),
        ({"c"}, "Many candidates did not heed the warning in part (c) that “solutions relying on calculator technology "
                "are not acceptable” and this cost them marks.", NO),
        (W, "Overall, this question had a wide spread of marks."),
        ({"a"}, "Part (a) required the sketching of a reciprocal graph."),
        ({"a"}, "A significant proportion of candidates did not even attempt to sketch the graph; those that did often "
                "produced a good positive reciprocal graph with both branches, scoring the first mark.", NO),
        ({"a"}, "The second mark proved harder with many graphs being in the wrong place, with an extra asymptote and the "
                "$x$ intercept not labelled."),
        ({"a"}, "The $y$-axis with a dashed line next to it also resulted in losing the second mark as candidates were not "
                "aware that this was implying that their asymptote was not the $y$-axis.", NO),
        ({"a"}, "Part (a)(ii) required both the equations of both asymptotes: $y=3$ was common but $x=0$ was not seen as "
                "often."),
        ({"b"}, "In part (b), candidates were required to equate both curves and rearrange to obtain a given answer."),
        ({"b"}, "This was very well answered with the most common error being slips on the indices and not equating the "
                "final answer to zero.", BACK),
        ({"b"}, "Those who were unsure what was being asked just proceeded to solve the cubic on their calculator.", NO),
        ({"c"}, "Part (c) proved more difficult, and this is where the calculator warning was ignored.", NO),
        ({"c"}, "Many candidates simply stated the three roots with no working which scored no marks."),
        ({"c"}, "Others tried to work backwards and failed to appreciate the requirement to use the given information."),
        ({"c"}, "It is not acceptable to just use the calculator to solve to find the three roots, then above write the "
                "factorised version and then multiply out above this to achieve the cubic equation as there is not "
                "sufficient evidence that the given information had been used.", NO),
        ({"c"}, "If it was not factorised into $(3x+2)$(quadratic) or evidence that another factor had been found, "
                "demonstrated by an algebraic technique such as algebraic division, or using the factor theorem then full "
                "marks could not be awarded.", NO),
        ({"c"}, "Just factorising by inspection using one of the other factors which have mysteriously appeared was not "
                "accepted and these approaches should be discouraged.", NO),
        ({"c"}, r"Those that realised that algebraic division was required scored well, a significant number of candidates "
                r"choose to divide by $x+\frac{2}{3}$ rather than the expected $3x+2$.", NO),
        ({"c"}, "The resultant quadratic was then factorised to give the additional points of intersection."),
    ],
    "06": [
        ({"a", "b", "c"}, "This was a very accessible question and candidates clearly felt comfortable with this topic.", NO),
        ({"a", "b", "c"}, "In particular, parts (a) and (b) were well answered, although part (c) did provide much more "
                          "challenge and discriminated candidates well."),
        ({"a"}, "Part (a) was generally done well with most candidates able to form a correct equation and proceed to "
                "find $a$."),
        ({"a"}, r"Those who used $a=-\frac{5}{8}$ usually forgot to write a conclusion.", NO),
        ({"a"}, "There were a few who expanded and achieved $1+12ax+66a^2x^2$ but then did not equate the terms or "
                "substitute in $a$ and did not score any marks."),
        ({"b"}, "In part (b), many candidates achieved the correct value for $k$."),
        ({"b"}, r"The most common mistake was to not square the $a$ and ended up with $k=-\frac{164}{4}$."),
        ({"b"}, "A few who just gave the answer as a decimal had rounded and lost the A mark."),
        ({"c"}, "In part (c), a minority of candidates achieved both marks."),
        ({"c"}, r"A common mistake was to solve $1-\frac{5}{8}x=\frac{17}{16}$ to find an appropriate value of $x$ but to "
                r"stop there and not substitute it into their expansion.", NO),
        ({"c"}, r"A few substituted it back into $\left(1-\frac{5}{8}x\right)^{12}$ and ended up just evaluating "
                r"$\left(\frac{17}{16}\right)^{12}$.", NO),
        ({"c"}, "For those who did substitute their $x$ into the expansion, several had made errors when solving the "
                "equation and had an incorrect value of $x$.", NO),
        ({"c"}, "Again a few made rounding errors and lost the accuracy mark."),
        ({"c"}, "Some candidates also found the next term in $x^3$ which was not required and took up additional time, "
                "however, successful responses were credited with both marks."),
    ],
    "07": [
        (W, "This question tested the understanding of logarithmic graphs and exponential growth."),
        (W, "This was successful in differentiating between candidates, although surprisingly candidates still struggle "
            "with this relationship.", NO),
        ({"b"}, "In addition, part (b) provided challenging for most who were unable to interpret in context."),
        ({"a"}, r"Many candidates lacked confidence in relating the exponential form of the model $P=ab^x$ to the "
                r"straight-line graph of $\log_{10}P$ against $x$."),
        ({"a"}, r"Whilst some very poor log work was seen, some candidates also made fundamental errors whilst forming the "
                r"equation of a straight line, for example, an incorrect method for calculating the gradient, e.g. "
                r"$\frac{6-0}{2.1-3.3}=-5$"),
        ({"a"}, r"Many candidates used $y$ instead of $\log_{10}P$ when writing down the equation of the straight line."),
        ({"a"}, r"Some candidates appeared confused as to whether they should use 3.3 or $\log_{10}3.3$ within their "
                r"equation, whilst others also showed a lack of robust understanding in manipulating indices after "
                r"achieving a correct equation for $P$."),
        ({"a"}, "A significant minority of candidates who achieved the correct values for both $a$ and $b$ failed to then "
                "write down the complete equation required."),
        ({"b"}, "In part (b), the vast majority of candidates were unable to correctly explain the meaning of “$ab$”."),
        ({"b"}, r"Some thought that they simply had to calculate its value i.e $ab=1005\times0.6310=1259$.",
         {"note": "the mark scheme's $a$ is awrt 1995"}),
        ({"b"}, "Many others assumed they needed to give the meanings of each of $a$ and $b$ separately, as on previous "
                "papers."),
    ],
    "08": [
        (W, "Marks awarded in this question were generally quite varied."),
        ({"a", "b", "c"}, "Often candidates made progress in (c) only, by attempting some integration with little correct "
                          "work seen in (a) or (b)."),
        (W, "Each part of this question presented a given answer, and candidates who failed to observe the warning in the "
            "question about showing all stages of their working, or relying entirely on calculator technology, often "
            "lost marks."),
        ({"a"}, "In part (a) candidates who identified how to proceed attempted two approaches."),
        ({"a"}, "Some differentiated the equation of the given curve and set the answer equal to $-2$ to obtain "
                "$3x^2-14=-2$."),
        ({"a"}, "Others subtracted the equations of the curve and the line to obtain $x^3-12x+16$ and used the derivative "
                "of this to obtain $3x^2-12=0$.", NO),
        ({"a"}, "A common error was attempting to solve $3x^2-14=0$ instead."),
        ({"a"}, r"Candidates then proceeded either to solve their equation to obtain $x=2$, or substituted $x=2$ into their "
                r"equation to verify the solution."),
        ({"a"}, r"Some candidates lost the final mark in part (a) for reaching $x=\pm2$ and failing to select $x=2$."),
        ({"a"}, "Other candidates often failed to make any progress in part (a) at all."),
        ({"a"}, "These often attempted to substitute $x=2$ into both the equations for the curve and the line or tried to "
                "solve $x^3-12x+16=0$.", BACK),
        ({"a"}, "Neither of these approaches gained credit because of the requirement of the question for use of "
                "calculus.", BACK),
        ({"b"}, "Those who attempted part (b) employed many varied methods.", NO),
        ({"b"}, "The easiest approach was to simply to verify that both the line and the curve passed through the point "
                "$(-4, 15)$ showing sufficient working."),
        ({"b"}, "Many though, subtracted the equations of the line and the curve again to obtain $y=x^3-12x+16$."),
        ({"b"}, "Candidates then either verified that $x=-4$ was a solution of $x^3-12x+16=0$, or attempted to solve this "
                "equation.", NO),
        ({"b"}, "Those who reached $x=-4$ by factorising via $(x+4)(x-2)^2=0$ were in a position to score both marks, but a "
                "number relied on their calculator equation solver, and could only be awarded the first mark in part "
                "(b).", NO),
        ({"b"}, "Candidates often lost the final mark for not writing a full conclusion."),
        ({"b"}, "To score full marks, candidates needed to reach $x=-4$ showing sufficient working using a valid method, "
                "and also indicate that they had completed the proof."),
        ({"c"}, "In part (c) candidates generally knew that they needed to proceed with integration, and often the first "
                "two marks were scored for correctly integrating even if they made no further progress."),
        ({"c"}, r"Successful candidates usually attempted to evaluate $\int_{-4}^{2}x^3-14x+23\,\mathrm{d}x$ and then "
                r"subtracted $\int_{-4}^{2}-2x+7\,\mathrm{d}x$."),
        ({"c"}, r"Some used the area of a trapezium to give $\frac{1}{2}(3+15)\times6$ instead of integrating the equation "
                r"of the line."),
        ({"c"}, r"Alternatively, some attempted to evaluate $\int_{-4}^{2}x^3-12x+16\,\mathrm{d}x$ reaching the required "
                r"area of 108 in one step."),
        ({"c"}, "Candidates were required to make their method clear, including showing the use of the limits $-4$ and 2."),
        ({"c"}, "Some failed to do so, clearly relying on calculator technology to evaluate the integrals."),
        ({"c"}, "Others failed to show the complete correct strategy for finding the area and often incorrectly "
                "identified the trapezium as a triangle."),
        ({"c"}, "Also, correct notation was required and appropriate use of the integral sign and the ‘$\\mathrm{d}x$’ on "
                "either side."),
    ],
    "09": [
        ({"b", "c"}, "This question, testing the topic of logarithms, was poorly answered with the majority of candidates "
                     "simply unable to engage with parts (b) and (c)."),
        (W, "Some candidates did not appear to understand what was being asked of them."),
        (W, "This portrayed both a lack of understanding of logarithms, and also a lack of practice on similar past paper "
            "questions.", BACK),
        ({"a"}, "Part (a) however, was answered relatively well, with many candidates reaching the correct answer of "
                "$2p$."),
        ({"a"}, r"Errors included, for example, candidates writing $\log_a256=2\log_a16$ without going onto write this in "
                r"terms of $p$.", NO),
        ({"a"}, r"Many appeared to think they had fully answered the question because it is given that $p=\log_a16$.", NO),
        ({"b"}, r"Similarly, in part (b), many candidates wrote $\log_a100=\log_a25+\log_a4$ but never proceeded further "
                r"than this.", NO),
        ({"b"}, "These candidates lost the A mark, seemingly thinking they had given a complete correct answer.", BACK),
        ({"c"}, "It was rare in part (c) for candidates to make any progress, having already struggled on part (b).", NO),
        ({"c"}, "The lack of the use of brackets often caused issues, too."),
        ({"c"}, r"It was rare for candidates to progress to the impressive, simplified solution of "
                r"$p^2-\frac{1}{4}q^2$.", NO),
        (W, "The general understanding of the laws of logarithms was very poor."),
        (W, r"Examples of conceptual misunderstandings were numerous. E.g. $\log_a256=(\log_a16)^2=p^2$, "
            r"$p=\log_a16$ so $\log_a256=16p$, $\log_a25\times4=q\times4=4q$, "
            r"$\log_a(80\times3.2)=\log_a256=2p$."),
        (W, "There were, of course, some excellent solutions, too."),
    ],
    "10": [
        (W, "This question required problem solving skills and focused on coordinate geometry and circles."),
        ({"a"}, "Part (a) required candidates to obtain a given equation."),
        ({"a"}, "The most common route for this was to work out the gradient between $P$ and $Q$ and to set this equal to "
                "the negative reciprocal of the gradient of the tangent.", NO),
        ({"a"}, "Candidates attempting this route scored well.", NO),
        ({"a"}, r"The other common route was to find two equations for radius using the coordinates of $P$ and $Q$ and the "
                r"gradient of $\frac{1}{2}$."),
        ({"a"}, "In general, candidates who had a strategy for the question did well on this part with just bracketing "
                "and sign errors being the major problem."),
        ({"a"}, "Unfortunately, many did not appreciate the relevance of the gradient of the tangent of $l$ would enable "
                "them to find the gradient of the normal to the curve at $Q$ (hence the equation of the line between $P$ "
                "and $Q$) and only typically scored one mark for being able to form an equation using the coordinates "
                "for $Q$ with the given gradient of $-2$ and not knowing where to go from there."),
        ({"b"}, "Part (b) required candidates to find the equation of the circle."),
        ({"b"}, "Most candidates found both values of $k$ but ignored the information in the question that $k$ was a "
                "positive constant."),
        ({"b"}, "Those who did appreciate this and used $k=5$ went on with good success to find the coordinates of $P$, "
                "giving them the centre of the circle and $Q$ which allowed them to calculate the radius and complete the "
                "question.", NO),
        ({"a", "b"}, "This part was more often successfully answered than the “show” part (a), which showed good "
                     "accessibility, as well as good exam technique by many candidates to still attempt a later part, even "
                     "if they were unable to successfully answer the earlier part."),
    ],
    "11": [
        (W, "This question was a modelling one relating to the price per gram of two different metals."),
        (W, "It enabled candidates to demonstrate understanding of working with exponential functions and differentiating "
            "them.", BACK),
        ({"a"}, "In part (a), a significant proportion of candidates scored both marks, achieving the correct answer of "
                "240."),
        ({"a"}, "A few candidates halved instead of doubled and got 60 and a few left $p$ as 120."),
        ({"a"}, r"A few made errors when evaluating $20\mathrm{e}^0$ or $40\mathrm{e}^0$ thinking this was equal to 1 (or "
                r"making a careless slip).", NO),
        ({"b"}, "Part (b) was generally poorly answered, and a number of candidates made no attempt to answer this part."),
        ({"b"}, "A common error was to set $V_A=V_B$."),
        ({"b"}, r"For those that found $\frac{\mathrm{d}V_A}{\mathrm{d}t}$ and $\frac{\mathrm{d}V_B}{\mathrm{d}t}$ some did "
                r"not put them equal to each other, or they set one or both equal to 0 instead, but the most common "
                r"mistake was to keep the negative and write $0.8\mathrm{e}^{0.04t}=-4.8\mathrm{e}^{-0.02t}$ thus "
                r"forfeiting the last three marks.", NO),
        ({"b"}, r"The minority who did set $\frac{\mathrm{d}V_A}{\mathrm{d}t}=-\frac{\mathrm{d}V_B}{\mathrm{d}t}$ were "
                r"usually able to use a correct method to solve the equation."),
        ({"b"}, "Some candidates did appreciate the issue of trying to take logs of a negative was not possible, but "
                "rather than go back to the original equation, they opted to either ignore it or scribble out the "
                "negative at some point of the solution which was not acceptable to score these final marks.", NO),
    ],
    "12": [
        (W, "This question provided a number of valuable entry points to provide candidates with the opportunity to "
            "progress in later parts of the question even if earlier parts proved challenging."),
        (W, "As a result, the question provided a good spread of marks amongst the cohort."),
        (W, "A significant minority of candidates abandoned the question, however, after coming unstuck on part (a) "
            "without an attempt at later parts."),
        (W, "This was a shame particularly as later parts of the question provided a good source of marks for many "
            "candidates.", BACK),
        ({"a"}, "In part (a) attempts to find expressions for the surface area and perimeter of the given shape were often "
                "successful, although errors and slips were not uncommon."),
        ({"a"}, "A correct expression for the perimeter was perhaps more often successfully achieved than a correct "
                "expression for the area."),
        ({"a"}, "A relatively common error was in setting $x$ as the diameter of the sector rather than the radius."),
        ({"a"}, "A significant number of candidates found expressions in terms of $r$ and could earn no marks until $r$ "
                "was replaced by x."),
        ({"a"}, "A minority of candidates equated the perimeter, rather than the area, to 100, but the vast majority made "
                "an attempt at the key step of rearranging their equation to find an expression for $y$ in terms of $x$."),
        ({"a"}, r"Some candidates were more unusual in their choice of substitution: rather than finding an expression for "
                r"$y$ or $2y$, they used effective and efficient substitutions for functions such as $\frac{100}{x}$.",
         NO),
        ({"a"}, "Once the critical substitution was achieved, most candidates went on to successfully obtain the required "
                "result, although occasionally marks were lost due to arithmetical and/or sign errors, or for the "
                "omission of ‘$P=$.’"),
        ({"b"}, "Part (b) required differentiation to determine the position of a stationary point and the vast majority "
                "of candidates were well versed in this process; the majority earning full marks in this part.", NO),
        ({"b"}, r"There were a few errors arising from errors in differentiation for example in the sign or the coefficient "
                r"of the $\frac{200}{x}$ term."),
        ({"b"}, r"Other errors arose from poor rearrangement of the equation $\frac{\mathrm{d}P}{\mathrm{d}x}$, resulting in "
                r"$x=-0.1$, or in the inclusion of the $x=-10$ root or stating a spurious $x=0$."),
        ({"c"}, "In part (c), differentiation to obtain the second derivative was commonly successfully achieved."),
        ({"c"}, "However, it was surprising that a significant minority of candidates felt that determining the second "
                "derivative was sufficient, neither evaluating it for their value of x, nor reasoning why it was positive "
                "for all positive x.", NO),
        ({"c"}, "Others lost the final mark in this part for a lack of conclusion."),
        ({"d"}, "A number of approaches to part (d) were observed."),
        ({"d"}, "Most commonly, candidates evaluated $y$ using their value of x and the relationship derived in part (a), "
                "to determine whether $y$ was greater than the required lower limit of 1."),
        ({"d"}, "This approach was usually the most successful.", BACK),
        ({"d"}, "Slightly more circuitous routes were also seen which involved employing the given expression for $P$ to "
                "determine the minimum perimeter and then an additional expression for $P$ in terms of $x$ and $y$, used "
                "with $y=1$ and either $x=10$ (to find $P$) or $P=40$ (to find $x$)."),
        ({"d"}, "Often this approach fell slightly short of being complete as a final comparison of $x$ with the value 10, "
                "or a comparison of $P$ with the value 40 was required to justify whether the swimming pool dimensions "
                "were suitable.", BACK),
        ({"d"}, "Some candidates tried to draw conclusions but gave insufficient supporting statements such as ‘10.8 is "
                "close to 10, so suitable’, or ‘10.8 > 0, so suitable’ rather than the relevant ‘10.8 > 10, so "
                "suitable’.", NO),
        ({"d"}, "Other candidates were unable to gain marks here for irrelevant statements unsupported by calculation such "
                "as ‘suitable, although the pool might be a bit small.’", NO),
        ({"d"}, "Others were confused about what value of $x$ they should use and erroneously substituted $x=0.4$ (the "
                "result value of the second derivative at $x=10$) into either their expression for $y$ or their "
                "expression for $P$."),
    ],
    "13": [
        (W, "The trigonometric equation, again, demonstrated how candidates are usually successful in solving these "
            "types of equations, however, they often struggle with the manipulation to show a given result.", NO),
        ({"a"}, "Part (a) held one of the highest demands in the paper and showed a clear differentiation between the most "
                "capable mathematicians and those who were familiar with trigonometric identities but struggled to apply "
                "and manipulate them.", NO),
        ({"a"}, "Overall, this proved to be difficult for most candidates with quite a few gaining one or two marks but "
                "very few were able to gain all four marks.", NO),
        ({"a"}, "Multiple attempts were seen which showed good resilience but further evidenced the complexity of the "
                "question."),
        ({"a"}, r"Most candidates were able to gain the first M mark which usually was for using "
                r"$\tan\theta=\frac{\sin\theta}{\cos\theta}$, (even if this followed from incorrect work which was quite "
                r"often) quite a few candidates attempted to divide by $\cos\theta$ as they seemed to spot it would give "
                r"them a $\tan\theta$ in their working, however not many recognised the need to divide by $\cos^2\theta$ "
                r"and those that did would often forget to divide the 4 on the right hand side by it as well; they also "
                r"tended to replace $\frac{7\sin^2\theta}{\cos^2\theta}$ with $3\tan^2\theta$.", NO),
        ({"a"}, r"Of the candidates who did manage to pick up the first two marks, many could not reach a 3TQ in "
                r"$\tan\theta$ and thus the required answer."),
        ({"a"}, r"The successful approaches would often start with using $\sin^2\theta+\cos^2\theta=1$ on the right-hand "
                r"side and proceed from there or work backwards from the given answer."),
        ({"b"}, "Part (b) was much more accessible due to the given answer in (a) not being a “show” which required "
                "constants to be found."),
        ({"b"}, "Candidates achieved much more success with this part with most able to find the required roots and use "
                "these to find at least two of the required angles.", NO),
        ({"b"}, "There were occasional sign errors and a very small number attempted to solve the original equation from "
                "(a) without success."),
        ({"b"}, "There were quite a few candidates who did not find all the required angles."),
        ({"b"}, r"This would often be because they would reject one of the solutions, $-\frac{2}{3}$ or the angle it gave "
                r"being negative seemed to be a reason that candidates ruled it out.", BACK),
        ({"b"}, r"The other root, 2, would often be ruled out presumably because of a misconception that the range of all "
                r"trigonometric graphs was $|y|\leqslant1$."),
        ({"b"}, "There were a small number who used an incorrect method to find other values, such as adding 90, or "
                "subtracting from 180 from their angles.", NO),
        ({"b"}, "Quite a lot of candidates did manage to find all the required angles, however."),
        ({"c"}, "Part (c) was usually poorly attempted with the vast majority not evidencing an understanding of graph "
                "transformations and just adding 63.4 to 720 or multiplying 243.4 by 4 as this would give an angle in the "
                "required range.", NO),
    ],
    "14": [
        (W, "This question proved to be a challenge for the majority of candidates and full marks were not common."),
        (W, "The instruction to ‘use algebra’ was lost on a number of candidates who employed logical approaches or "
            "attempted to test an array of integer values for $n$."),
        (W, "Perhaps a casualty of being the last question on the paper, there were also a number of blank responses "
            "seen."),
        (W, "For those employing a logical approach, some credit was given when algebra was used to factorise the "
            "quadratic followed by a consideration of the parity of the factors.", NO),
        (W, "This was often left incomplete however, and so rarely scored the two marks out of four for a complete "
            "attempt via this approach.", BACK),
        (W, "The majority of candidates who attempted the question did grasp the need to consider the general form for "
            "odd and even integers and made a reasonable attempt."),
        (W, "Although some candidates incorrectly used ‘$k+1$’ or considered even integers twice e.g. ‘$2k$’ and "
            "‘$2k+2$’."),
        (W, "Unfortunately, marks were very commonly, yet surprisingly, lost due to basic mistakes in simple algebraic "
            "manipulation."),
        (W, "These errors occurred in both the expansion and the factorisation of brackets and included errors such as "
            "$5(2k+1)=10k+1$ or $4k^2+10k=2(k^2+5k)$.", BACK),
        (W, "It was surprisingly common for candidates to use $n$ in their general form i.e. ‘$n=2n$’ which led to the "
            "loss of the final mark, especially since this has been in previous mark schemes that this would not garner "
            "full marks.", NO),
        (W, "A large proportion of candidates failed to give an overall conclusion to their proof which was also "
            "penalised with the final mark.", NO),
        (W, "A small minority of candidates employed proof by induction and, when seen, this was usually confidently "
            "executed.", NO),
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
    "01": ("easy", at("01", "This was a very accessible question")),
    "02a": ("easy", at("02", "In part (a), most candidates made progress")),
    "02b": ("medium", at("02", "Others however, encountered difficulties")),
    "02c": ("easy", at("02", "Part (c) was answered quite well")),
    "03a": ("medium", at("03", "In part (a), most candidates knew")),
    "03b": ("medium", at("03", "In part (b), quite a few candidates seemed unclear")),
    "03c": ("hard", at("03", "Part (c) proved quite tricky")),
    "04a": ("medium", at("04", "In part (a), whilst the vast majority")),
    "04b": ("easy", at("04", "Candidates were more confident when using the cosine rule")),
    "05a": ("hard", at("05", "The second mark proved harder")),
    "05b": ("easy", at("05", "This was very well answered")),
    "05c": ("medium", at("05", "Part (c) proved more difficult")),
    "06a": ("easy", at("06", "Part (a) was generally done well")),
    "06b": ("easy", at("06", "In part (b), many candidates achieved")),
    "06c": ("hard", at("06", "In part (c), a minority of candidates achieved both marks")),
    "07a": ("medium", at("07", "Many candidates lacked confidence")),
    "07b": ("hard", at("07", "In part (b), the vast majority")),
    "08a": ("hard", at("08", "Often candidates made progress in (c) only")),
    "08b": ("medium", at("08", "Candidates often lost the final mark")),
    "08c": ("medium", at("08", "In part (c) candidates generally knew")),
    "09a": ("easy", at("09", "Part (a) however, was answered relatively well")),
    "09b": ("hard", at("09", "This question, testing the topic of logarithms")),
    "09c": ("hard", at("09", "It was rare in part (c)")),
    "10a": ("medium", at("10", "Unfortunately, many did not appreciate")),
    "10b": ("medium", at("10", "Most candidates found both values of $k$")),
    "11a": ("easy", at("11", "In part (a), a significant proportion")),
    "11b": ("hard", at("11", "Part (b) was generally poorly answered")),
    "12a": ("medium", at("12", "In part (a) attempts to find expressions")),
    "12b": ("easy", at("12", "Part (b) required differentiation")),
    "12c": ("medium", at("12", "However, it was surprising that a significant minority")),
    "12d": ("medium", at("12", "Most commonly, candidates evaluated")),
    "13a": ("hard", at("13", "Overall, this proved to be difficult")),
    "13b": ("medium", at("13", "There were quite a few candidates who did not find all")),
    "13c": ("hard", at("13", "Part (c) was usually poorly attempted")),
    "14": ("hard", at("14", "This question proved to be a challenge")),
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
