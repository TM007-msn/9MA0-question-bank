"""Draft builder for 9MA0-02 2019-06 (A level Pure Paper 2, June 2019).

Run (from the project root, with the venv active):
    python extraction/9MA0-02_2019-06.py        # writes out/drafts/9MA0-02_2019-06.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-02_2019-06.json

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

P, S = "9MA0-02", "2019-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "08ii"); label as printed (e.g. "8(ii)")."""
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


A, B = r"\mathbf{a}", r"\mathbf{b}"
NUMONLY = r"(Solutions based entirely on graphical or numerical methods are not acceptable.)"


def V(x):
    """A vector arrow over two letters, e.g. V("OA")."""
    return r"\overrightarrow{" + x + "}"


# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q2 = ["The speed of a small jet aircraft was measured every 5 seconds, starting from the time it turned onto a "
      "runway, until the time when it left the ground.",
      r"The results are given in the table below with the time in seconds and the speed in $\text{m s}^{-1}$.",
      r"$$\begin{array}{|c|c|c|c|c|c|c|}\hline\text{Time (s)}&0&5&10&15&20&25\\\hline"
      r"\text{Speed (m s}^{-1}\text{)}&2&5&10&18&28&42\\\hline\end{array}$$",
      "Using all of this information,"]
Q2A = "estimate the length of runway used by the jet to take off."
Q3 = [r"[Figure 1: a sector $AOB$ of a circle with centre $O$; the radius $OA$ is labelled 5 cm, the angle $AOB$ "
      r"at $O$ is marked $40^\circ$ and the arc joins $A$ to $B$.]",
      r"Figure 1 shows a sector $AOB$ of a circle with centre $O$, radius 5 cm and angle $AOB=40^\circ$",
      "The attempt of a student to find the area of the sector is shown below.",
      r"$$\begin{aligned}\text{Area of sector}&=\frac{1}{2}r^2\theta\\&=\frac{1}{2}\times5^2\times40\\"
      r"&=500\text{ cm}^2\end{aligned}$$"]
Q6 = [r"[Figure 4: the graph of $y=\mathrm{g}(x)$: for $x\leqslant2$ a parabola-shaped curve comes down from the top "
      r"left, crosses the positive $y$-axis and reaches its lowest point just above the positive $x$-axis; from that "
      r"point a straight line rises steeply to the top right.]",
      r"Figure 4 shows a sketch of the graph of $y=\mathrm{g}(x)$, where",
      r"$$\mathrm{g}(x)=\begin{cases}(x-2)^2+1 & x\leqslant2\\4x-7 & x>2\end{cases}$$"]
Q6H = ["The function h is defined by", r"$$\mathrm{h}(x)=(x-2)^2+1\qquad x\leqslant2$$"]
Q7 = ["A small factory makes bars of soap.",
      r"On any day, the total cost to the factory, £$y$, of making $x$ bars of soap is modelled to be the sum of two "
      r"separate elements:",
      "• a fixed cost",
      "• a cost that is proportional to the number of bars of soap that are made that day"]
Q7I = ["The bars of soap are sold for £2 each.",
       "On a day when 800 bars of soap are made and sold, the factory makes a profit of £500",
       "On a day when 300 bars of soap are made and sold, the factory makes a loss of £80"]
Q7B = ["Using the above information,", r"(b) show that $y=0.84x+428$"]
Q9 = ["A research engineer is testing the effectiveness of the braking system of a car when it is driven in wet "
      "conditions.",
      r"The engineer measures and records the braking distance, $d$ metres, when the brakes are applied from a speed "
      r"of $V\text{ km h}^{-1}$.",
      r"Graphs of $d$ against $V$ and $\log_{10}d$ against $\log_{10}V$ were plotted.",
      "The results are shown below together with a data point from each graph.",
      r"[Figure 5: a graph of $d$ against $V$, with origin $O$: a curve starting at $O$, flat at first and then "
      r"bending upwards ever more steeply, passing through the marked point $(30, 20)$.]",
      r"[Figure 6: a graph of $\log_{10}d$ against $\log_{10}V$, with origin $O$: a straight line with positive "
      r"gradient crossing the $\log_{10}d$-axis below $O$ at the marked point $(0, -1.77)$ and crossing the positive "
      r"$\log_{10}V$-axis.]"]
Q9A = ["Explain how Figure 6 would lead the engineer to believe that the braking distance should be modelled by the "
       "formula",
       r"$$d=kV^n\qquad\text{where }k\text{ and }n\text{ are constants}$$",
       r"with $k\approx0.017$"]
Q9B = [r"Using the information given in Figure 5, with $k=0.017$",
       r"(b) find a complete equation for the model giving the value of $n$ to 3 significant figures."]
Q10 = [r"[Figure 7: a sketch of triangle $OAB$, with $OB$ horizontal, $O$ at the left, $B$ at the right and $A$ "
       r"above $OB$, nearer to $O$ than to $B$.]",
       r"Figure 7 shows a sketch of triangle $OAB$.",
       r"The point $C$ is such that $" + V("OC") + "=2" + V("OA") + "$.",
       r"The point $M$ is the midpoint of $AB$.",
       r"The straight line through $C$ and $M$ cuts $OB$ at the point $N$.",
       r"Given $" + V("OA") + "=" + A + "$ and $" + V("OB") + "=" + B + "$"]
Q10B = (r"Show that $" + V("ON") + r"=\left(2-\frac{3}{2}\lambda\right)" + A + r"+\frac{1}{2}\lambda" + B
        + r"$, where $\lambda$ is a scalar constant.")
Q11 = [r"[Figure 8: the curve $C$ for $x>0$: it starts from a point on the positive $y$-axis, dips slightly to a "
       r"minimum point close to the $y$-axis in the first quadrant, then rises ever more steeply.]",
       r"Figure 8 shows a sketch of the curve $C$ with equation $y=x^x,\ x>0$"]
Q11P = r"The point $P(\alpha, 2)$ lies on $C$."
Q11I = [r"A possible iteration formula that could be used in an attempt to find $\alpha$ is",
        r"$$x_{n+1}=2x_n^{1-x_n}$$",
        r"Using this formula with $x_1=1.5$"]
Q12A = ["Prove",
        r"$$\frac{\cos3\theta}{\sin\theta}+\frac{\sin3\theta}{\cos\theta}\equiv2\cot2\theta\qquad"
        r"\theta\neq(90n)^\circ,\ n\in\mathbb{Z}$$"]
Q13 = [r"[Figure 9: the tank: a vertical circular cylinder of height $h$ m with a hemisphere on top; the radius of the "
       r"top circle and of the base circle is marked $r$ m, and the hidden back halves of both circles are dashed.]",
       r"[A sphere of radius $r$ has volume $\frac{4}{3}\pi r^3$ and surface area $4\pi r^2$]",
       "A manufacturer produces a storage tank.",
       "The tank is modelled in the shape of a hollow circular cylinder closed at one end with a hemispherical shell "
       "at the other end as shown in Figure 9.",
       "The walls of the tank are assumed to have negligible thickness.",
       r"The cylinder has radius $r$ metres and height $h$ metres and the hemisphere has radius $r$ metres.",
       r"The volume of the tank is $6\text{ m}^3$."]
Q13A = [r"Show that, according to the model, the surface area of the tank, in $\text{m}^2$, is given by",
        r"$$\frac{12}{r}+\frac{5}{3}\pi r^2$$"]
Q13M = "The manufacturer needs to minimise the surface area of the tank."
Q14A = [r"Use the substitution $u=4-\sqrt{h}$ to show that",
        r"$$\int\frac{\mathrm{d}h}{4-\sqrt{h}}=-8\ln\left|4-\sqrt{h}\right|-2\sqrt{h}+k$$",
        r"where $k$ is a constant"]
Q14 = ["A team of scientists is studying a species of slow growing tree.",
       "The rate of change in height of a tree in this species is modelled by the differential equation",
       r"$$\frac{\mathrm{d}h}{\mathrm{d}t}=\frac{t^{0.25}\left(4-\sqrt{h}\right)}{20}$$",
       r"where $h$ is the height in metres and $t$ is the time, measured in years, after the tree is planted."]

LATEX = {
    "01": L("Given", r"$$2^x\times4^y=\frac{1}{2\sqrt{2}}$$", r"express $y$ as a function of $x$."),
    "02a": L(*Q2, Q2A),
    "02b": L(*Q2, "(a) " + Q2A, "Given that the jet accelerated smoothly in these 25 seconds,",
             "(b) explain whether your answer to part (a) is an underestimate or an overestimate of the length of "
             "runway used by the jet to take off."),
    "03a": L(*Q3, "Explain the error made by this student."),
    "03b": L(*Q3, "Write out a correct solution."),
    "04": L(r"[Figure 2: axes $x$ and $y$ with origin $O$; the curve $C_1$, an ellipse centred on $O$ that is wider "
            r"than it is tall, and the circle $C_2$, centred on $O$, cross at four points, one in each quadrant; the "
            r"circle reaches further along the $y$-axis and the ellipse further along the $x$-axis; the intersection "
            r"point $S$ in the fourth quadrant is marked with a dot.]",
            r"The curve $C_1$ with parametric equations",
            r"$$x=10\cos t,\qquad y=4\sqrt{2}\sin t,\qquad0\leqslant t<2\pi$$",
            r"meets the circle $C_2$ with equation",
            r"$$x^2+y^2=66$$",
            "at four distinct points as shown in Figure 2.",
            r"Given that one of these points, $S$, lies in the 4th quadrant, find the Cartesian coordinates of $S$."),
    "05": L(r"[Figure 3: the curve $y=\sqrt{x}$ rising from $O$ through the first quadrant, with vertical lines from "
            r"the $x$-axis up to the curve at $x=4$ and $x=9$; between them a thin shaded rectangle, of height $y$ and "
            r"width $\delta x$, reaches up to the point $P$ on the curve.]",
            r"Figure 3 shows a sketch of the curve with equation $y=\sqrt{x}$",
            r"The point $P(x, y)$ lies on the curve.",
            r"The rectangle, shown shaded on Figure 3, has height $y$ and width $\delta x$.",
            "Calculate",
            r"$$\lim_{\delta x\to0}\sum_{x=4}^{9}\sqrt{x}\,\delta x$$"),
    "06a": L(*Q6, r"Find the value of $\mathrm{gg}(0)$."),
    "06b": L(*Q6, r"Find all values of $x$ for which", r"$$\mathrm{g}(x)>28$$"),
    "06c": L(*Q6, *Q6H, "Explain why h has an inverse but g does not."),
    "06d": L(*Q6, *Q6H, "Solve the equation", r"$$\mathrm{h}^{-1}(x)=-\frac{1}{2}$$"),
    "07a": L(*Q7, r"Write down a general equation linking $y$ with $x$, for this model."),
    "07b": L(*Q7, *Q7I, Q7B[0], Q7B[1][4:]),
    "07c": L(*Q7, *Q7I, *Q7B,
             "(c) With reference to the model, interpret the significance of the value 0.84 in the equation."),
    "07d": L(*Q7, *Q7I, *Q7B, "Assuming that each bar of soap is sold on the day it is made,",
             "(d) find the least number of bars of soap that must be made on any given day for the factory to make "
             "a profit that day."),
    "08i": L("Find the value of", r"$$\sum_{r=4}^{\infty}20\times\left(\frac{1}{2}\right)^r$$"),
    "08ii": L("Show that", r"$$\sum_{n=1}^{48}\log_5\left(\frac{n+2}{n+1}\right)=2$$"),
    "09a": L(*Q9, *Q9A),
    "09b": L(*Q9, "(a) " + Q9A[0], *Q9A[1:], *Q9B),
    "09c": L(*Q9, "(a) " + Q9A[0], *Q9A[1:], *Q9B,
             r"Sean is driving this car at $60\text{ km h}^{-1}$ in wet conditions when he notices a large puddle in "
             r"the road 100 m ahead. It takes him 0.8 seconds to react before applying the brakes.",
             "(c) Use your formula to find out if Sean will be able to stop before reaching the puddle."),
    "10a": L(*Q10, r"Find $" + V("CM") + "$ in terms of $" + A + "$ and $" + B + "$"),
    "10b": L(*Q10, Q10B),
    "10c": L(*Q10, "(b) " + Q10B, r"(c) Hence prove that $ON:NB=2:1$"),
    "11a": L(*Q11, r"Find, by firstly taking logarithms, the $x$ coordinate of the turning point of $C$.", NUMONLY),
    "11b": L(*Q11, Q11P, r"Show that $1.5<\alpha<1.6$"),
    "11c": L(*Q11, Q11P, *Q11I, r"find $x_4$ to 3 decimal places,"),
    "11d": L(*Q11, Q11P, *Q11I, r"describe the long-term behaviour of $x_n$"),
    "12a": L(*Q12A),
    "12b": L("(a) " + Q12A[0], Q12A[1],
             r"(b) Hence solve, for $90^\circ<\theta<180^\circ$, the equation",
             r"$$\frac{\cos3\theta}{\sin\theta}+\frac{\sin3\theta}{\cos\theta}=4$$",
             "giving any solutions to one decimal place."),
    "13a": L(*Q13, *Q13A),
    "13b": L(*Q13, "(a) " + Q13A[0], Q13A[1], Q13M,
             "(b) Use calculus to find the radius of the tank for which the surface area is a minimum."),
    "13c": L(*Q13, "(a) " + Q13A[0], Q13A[1], Q13M,
             "(c) Calculate the minimum surface area of the tank, giving your answer to the nearest integer."),
    "14a": L(*Q14A),
    "14b": L(*Q14, "Find, according to the model, the range in heights of trees in this species."),
    "14c": L("(a) " + Q14A[0], *Q14A[1:], *Q14,
             "One of these trees is one metre high when it is first planted.",
             "According to the model,",
             "(c) calculate the time this tree would take to reach a height of 12 metres, giving your answer to 3 "
             "significant figures."),
}

Q1EG = r"E.g. $y=-\frac{1}{2}x-\frac{3}{4}$ or $y=-\frac{1}{4}(2x+3)$"
Q1LOG = r"\log\left(\frac{1}{2\sqrt{2}}\right)"
Q4S = r"$S=(5\sqrt{2}, -4)$ or $x=5\sqrt{2}$, $y=-4$ or $S=(\text{awrt }7.07, -4)$"
Q4SEL = (r"Selects the correct coordinates for $S$ Allow either $S=(5\sqrt{2}, -4)$ or $S=(\text{awrt }7.07, -4)$ "
         r"or $S=(\sqrt{50}, -4)$ or $S=\left(\frac{10}{\sqrt{2}}, -4\right)$")
Q4SUB = (r"Substitutes their solution back into the relevant original equation(s) to get the value of the "
         r"$x$-coordinate and value of the corresponding $y$-coordinate. Note: These may not be in the correct quadrant")
Q4EQ = r"$(10\cos t)^2+(4\sqrt{2}\sin t)^2=66$"
Q4BEG = (r"Begins to solve the problem by applying an appropriate strategy. E.g. Way {w}: A complete process of "
         r"combining equations for $C_1$ and $C_2$ by substituting the parametric equation into the Cartesian equation "
         r"to give an equation in one variable (i.e. $t$) only.")
Q8IA = r"Applies $\frac{a}{1-r}$ for their $r$ (where $-1<\text{their }r<1$) and their value for $a$"
H = r"\left|4-\sqrt{h}\right|"
Q9B1 = (r"$\{k=\}10^{-1.77}=0.017$ or $\log0.017=-1.77$ linked together in the same part of the question. Notes: See "
        r"scheme")
Q11B_COMMON = r"$\left\{\frac{\mathrm{d}y}{\mathrm{d}x}=0\Rightarrow\right\}\frac{x}{x}+\ln x=0$ or $1+\ln x=0\Rightarrow\ln x=k\Rightarrow x=\ldots$. Note: $k\neq0$. Notes: Sets $1+\ln x=0$ and rearranges to make $\ln x=k\Rightarrow x=\ldots$; $k$ is a constant and $k\neq0$"
Q12L = r"\frac{\cos3\theta}{\sin\theta}+\frac{\sin3\theta}{\cos\theta}"
Q12ANS = (r"$\textbf{Only one solution}$ of $\theta=103.3^\circ$ (1 dp) or awrt $103.3^\circ$. Notes: Uses "
          r"$90^\circ<\theta<180^\circ$ to deduce the only solution $\theta=\text{awrt }103.3^\circ$")

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", ALG, "2.1, 6.4", 3, LATEX["01"],
      [r"B1 (AO 1.1b): $2^x\times2^{2y}=2^{-\frac{3}{2}}$. Notes: Way 1: Writes a correct equation in powers of 2 only "
       r"Special Case: If 0 marks are scored on application of the mark scheme then allow Special Case B1 M0 A0 (total "
       r"of 1 mark) for any of • $2^x\times4^y\to2^{x+2y}$ • $2^x\times4^y\to4^{\frac{1}{2}x+y}$ • "
       r"$\frac{1}{2^x2\sqrt{2}}\to2^{-x-\frac{3}{2}}$ • $\log2^x+\log4^y\to x\log2+y\log4$ or $x\log2+2y\log2$ • "
       r"$\ln2^x+\ln4^y\to x\ln2+y\ln4$ or $x\ln2+2y\ln2$ • $y=\log\left(\frac{1}{2^x2\sqrt{2}}\right)$ o.e. {base of 4 "
       r"omitted}",
       r"M1 (AO 2.1): $2^{x+2y}=2^{-\frac{3}{2}}\Rightarrow x+2y=-\frac{3}{2}\Rightarrow y=\ldots$. Notes: Complete "
       r"process of writing a correct equation in powers of 2 only and using correct index laws to obtain $y$ written "
       r"as a function of $x$.",
       r"A1 (AO 1.1b): " + Q1EG + r". Notes: $y=-\frac{1}{2}x-\frac{3}{4}$ o.e. Note: Allow equivalent results for A1 "
       r"where $y$ is written as a function of $x$ Note: You can ignore subsequent working following on from a correct "
       r"answer. Note: Allow B1 for $2^x\times4^y=\frac{1}{2\sqrt{2}}\Rightarrow4^y=\frac{1}{2^x2\sqrt{2}}\Rightarrow"
       r"\log_4(4^y)=\log_4\left(\frac{1}{2^x2\sqrt{2}}\right)$ followed by M1 A1 for $y=\log_4\left(\frac{1}"
       r"{2^x2\sqrt{2}}\right)$ or $y=\log_4\left(\frac{2^{-x}}{2\sqrt{2}}\right)$ or $y=\log_4\left(\frac{\sqrt{2}}"
       r"{4(2^x)}\right)$ or $y=-\log_4\left(2^{x+\frac{3}{2}}\right)$ or $y=-\log_4(\sqrt{2}(2^{x+1}))$",
       r"ALT: Way 2 — B1 (AO 1.1b): $\log(2^x\times4^y)=" + Q1LOG + r"$. Notes: Way 2, Way 3 and Way 4: Writes a "
       r"correct equation involving logarithms",
       r"ALT: Way 2 — M1 (AO 2.1): $\log2^x+\log4^y=" + Q1LOG + r"$ $\Rightarrow x\log2+y\log4=\log1-\log(2\sqrt{2})"
       r"\Rightarrow y=\ldots$. Notes: Way 2, Way 3 and Way 4: Complete process of writing a correct equation involving "
       r"logarithms and using correct log laws to obtain $y$ written as a function of $x$.",
       r"ALT: Way 2 — A1 (AO 1.1b): $y=\frac{-\log(2\sqrt{2})-x\log2}{\log4}$ $\left\{\Rightarrow y=-\frac{1}{2}x-"
       r"\frac{3}{4}\right\}$. Notes: Way 2, Way 3 and Way 4: $y=\frac{-\log(2\sqrt{2})-x\log2}{\log4}$ or "
       r"$y=\frac{-\ln(2\sqrt{2})-x\ln2}{\ln4}$ or $y=\frac{" + Q1LOG + r"-\log(2^x)}{\log4}$ or "
       r"$y=-\frac{1}{2}x-\frac{3}{4}$ or $y=-\frac{1}{4}(2x+3)$ o.e.",
       r"ALT: Way 3 — B1 (AO 1.1b): $\log(2^x\times4^y)=" + Q1LOG + "$",
       r"ALT: Way 3 — M1 (AO 2.1): $\log2^x+\log4^y=" + Q1LOG + r"\Rightarrow\log2^x+y\log4=" + Q1LOG
       + r"\Rightarrow y=\ldots$",
       r"ALT: Way 3 — A1 (AO 1.1b): $y=\frac{" + Q1LOG + r"-\log(2^x)}{\log4}$ $\left\{\Rightarrow y=-\frac{1}{2}x-"
       r"\frac{3}{4}\right\}$",
       r"ALT: Way 4 — B1 (AO 1.1b): $\log_2(2^x\times4^y)=\log_2\left(\frac{1}{2\sqrt{2}}\right)$",
       r"ALT: Way 4 — M1 (AO 2.1): $\log_22^x+\log_24^y=\log_2\left(\frac{1}{2\sqrt{2}}\right)\Rightarrow x+2y=-"
       r"\frac{3}{2}\Rightarrow y=\ldots$",
       r"ALT: Way 4 — A1 (AO 1.1b): " + Q1EG,
       r"ALT: Way 5 — B1 (AO 1.1b): $4^{\frac{1}{2}x}\times4^y=4^{-\frac{3}{4}}$. Notes: Writes a correct equation in "
       r"powers of 4 only",
       r"ALT: Way 5 — M1 (AO 2.1): $4^{\frac{1}{2}x+y}=4^{-\frac{3}{4}}\Rightarrow\frac{1}{2}x+y=-\frac{3}{4}\Rightarrow "
       r"y=\ldots$. Notes: Complete process of writing a correct equation in powers of 4 only and using correct index "
       r"laws to obtain $y$ written as a function of $x$.",
       r"ALT: Way 5 — A1 (AO 1.1b): " + Q1EG + r". Notes: $y=-\frac{1}{2}x-\frac{3}{4}$ o.e."],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", NUM, "9.4, 9.5", 3, LATEX["02a"],
      [r"M1 (AO 3.1a): Uses an allowable method to estimate the area under the curve. E.g. Way 1: an attempt at the "
       r"trapezium rule (see below). Notes: A low-level problem-solving mark for using an allowable method to estimate "
       r"the area under the curve. E.g. Way 1: See scheme. Allow $\lambda(2+2(5+10+18+28)+42)$; $\lambda>0$ for 1st M1 "
       r"Note: Only the 1st M1 can only be scored for Way 2, Way 3, Way 4, Way 5 and Way 7 methods Note: Full marks in "
       r"part (a) can only be scored by using a Way 1 or a Way 6 method. Note: Give M0 M0 A0 for "
       r"$\{d=\}2(5)+5(5)+10(5)+18(5)+28(5)+42(5)$ $\{=105(5)=525\}$ (i.e. using too many rectangles) Note: Give M0 M0 "
       r"A0 for a Simpson’s Rule Method",
       r"M1 (AO 1.1b): $\frac{1}{2}\times(5)\times[2+2(5+10+18+28)+42]$ or $\frac{1}{2}\times[\text{“}315\text{”}+"
       r"\text{“}515\text{”}]$. Notes: Correct trapezium rule method with $h=5$. Condone a slip on one of the speeds. The "
       r"‘2’ and ‘42’ should be in the correct place in the [......].",
       r"A1 (AO 1.1b): $=415$ {m}. Notes: 415 Note: Units do not have to be stated Note: Give final A0 for giving a "
       r"final answer with incorrect units. e.g. give final A0 for 415 km or $415\text{ m s}^{-1}$ Note: Condone M1 M0 "
       r"A0 for $\left[\frac{(2+10)}{2}(10)+\frac{(10+18)}{2}(5)+\frac{(18+28)}{2}(5)+\frac{(28+42)}{2}(5)\right]=395$ m "
       r"Note: Give M1 M1 A1 for $5\left[\frac{(2+5)}{2}+\frac{(5+10)}{2}+\frac{(10+18)}{2}+\frac{(18+28)}{2}+"
       r"\frac{(28+42)}{2}\right]=415$ m Note: Give M1 M1 A1 for $\frac{5}{2}(2+42)+5(5+10+18+28)=415$ m Note: "
       r"Bracketing mistake: $\textbf{Unless the final calculated answer implies that the method has been applied "
       r"correctly}$ give M1 M0 A0 for $\frac{5}{2}(2)+2(5+10+18+28)+42$ $\{=169\}$ give M1 M0 A0 for "
       r"$\frac{5}{2}(2+42)+2(5+10+18+28)$ $\{=232\}$",
       r"ALT: (a) Way 2 — M1 (AO 3.1a): $\{s=\}\left(\frac{2+42}{2}\right)(25)$ $\{=550\}$. Notes: Way 2: Uses "
       r"$s=\left(\frac{u+v}{2}\right)t$ which is equivalent to finding the area of a large trapezium",
       r"ALT: (a) Way 3 — M1 (AO 3.1a): $42=2+25(a)\Rightarrow a=1.6\Rightarrow s=2(25)+(0.5)(1.6)(25)^2$ "
       r"$\{=550\}$. Notes: Way 3: Complete method using a uniform acceleration equation.",
       r"ALT: (a) Way 4 — M1 (AO 3.1a): $\{d=\}(2)(5)+5(5)+10(5)+18(5)+28(5)$ $\{=63(5)=315\}$. Notes: Way 4: Sums "
       r"rectangles lying below the curve. Condone a slip on one of the speeds.",
       r"ALT: (a) Way 5 — M1 (AO 3.1a): $\{d=\}5(5)+10(5)+18(5)+28(5)+42(5)$ $\{=103(5)=515\}$. Notes: Way 5: Sums "
       r"rectangles lying above the curve. Condone a slip on one of the speeds.",
       r"ALT: (a) Way 6 — M1 (AO 3.1a): $\{d=\}\frac{315+515}{2}$ $\{=415\}$. Notes: Way 6: Average the result of Way 3 "
       r"and Way 4. Equivalent to Way 1.",
       r"ALT: (a) Way 7 — M1 (AO 3.1a): $\{d=\}\left(\frac{2+5+10+18+28+42}{6}\right)(25)$ $\{=437.5\}$. Notes: Way 7: "
       r"Applies (average speed)$\times$(time)"],
      False, 4),
    e("02b", "2(b)", NUM, "9.4, 9.5", 1, LATEX["02b"],
      [r"B1ft (AO 2.4): Alt 1: Uses a Way 1, Way 2, Way 3, Way 5, Way 6 or Way 7 method in (a). Overestimate "
       r"$\textbf{and}$ a relevant explanation e.g. • {top of} trapezia lie above the curve • Area of trapezia > area "
       r"under curve • An appropriate diagram which gives reference to the extra area • Curve is convex • "
       r"$\frac{\mathrm{d}^2y}{\mathrm{d}x^2}>0$ • Acceleration is {continually} increasing • The gradient of the curve "
       r"is {continually} increasing • All the rectangles are above the curve (Way 5). Notes: $\textbf{This mark depends "
       r"on both an answer to part (a) being obtained and the first M in part (a)}$ See scheme Note: Allow the "
       r"explanation “curve concaves upwards” Note: Do not allow explanations such as “curve is concave” or “curve "
       r"concaves downwards” Note: Do not allow explanation “gradient of the curve is positive” Note: Do not allow "
       r"explanations which refer to “friction” or “air resistance” Note: The diagram opposite is sufficient as an "
       r"explanation. It must show the top of a trapezium lying above the curve. [diagram: one strip with a straight "
       r"top edge running from its lower left corner to its upper right corner, above a curve that bends upwards "
       r"between the same two points]",
       r"ALT: (b) Alt 2 — B1ft (AO 2.4): Uses a Way 4 method in (a). Underestimate $\textbf{and}$ a relevant "
       r"explanation e.g. • All the rectangles are below the curve. Notes: $\textbf{This mark depends on both an answer "
       r"to part (a) being obtained and the first M in part (a)}$ See scheme Note: Do not allow explanations which "
       r"refer to “friction” or “air-resistance”"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", TRIG, "5.1", 1, LATEX["03a"],
      [r"B1 (AO 2.3): Allow explanations such as • student should have worked in radians • they did not convert "
       r"degrees to radians • 40 should be in radians • $\theta$ should be in radians • angle (or $\theta$) should be "
       r"$\frac{40\pi}{180}$ or $\frac{2\pi}{9}$ • correct formula is $\pi r^2\left(\frac{\theta}{360}\right)$ {where "
       r"$\theta$ is in degrees} • correct formula is $\pi r^2\left(\frac{40}{360}\right)$. Notes: Explains that the "
       r"formula use is only valid when angle $AOB$ is applied in radians. See scheme for examples of suitable "
       r"explanations."],
      True, 6),
    e("03b", "3(b)", TRIG, "5.1", 2, LATEX["03b"],
      [r"M1 (AO 1.1b): {Area of sector $=$} $\frac{1}{2}(5^2)\left(\frac{2\pi}{9}\right)$. Notes: Way 1: Correct "
       r"application of the sector formula using a correct value for $\theta$ in radians Note: Allow exact equivalents "
       r"for $\theta$ e.g. $\theta=\frac{40\pi}{180}$ or $\theta$ in the range [0.68, 0.71]",
       r"A1 (AO 1.1b): $=\frac{25}{9}\pi$ $\{\text{cm}^2\}$ or awrt 8.73 $\{\text{cm}^2\}$. Notes: A1*: Accept "
       r"$\frac{25}{9}\pi$ or awrt 8.73 Note: Ignore the units Note: Allow exact equivalents such as "
       r"$\frac{50}{18}\pi$ Note: Allow M1 A1 for $500\left(\frac{\pi}{180}\right)=\frac{25}{9}\pi$ $\{\text{cm}^2\}$ "
       r"or awrt 8.73 $\{\text{cm}^2\}$",
       r"ALT: (b) Way 2 — M1 (AO 1.1b): {Area of sector $=$} $\pi(5^2)\left(\frac{40}{360}\right)$. Notes: Correct "
       r"application of the sector formula in degrees",
       r"ALT: (b) Way 2 — A1 (AO 1.1b): $=\frac{25}{9}\pi$ $\{\text{cm}^2\}$ or awrt 8.73 $\{\text{cm}^2\}$. Notes: "
       r"Accept $\frac{25}{9}\pi$ or awrt 8.73 Note: Ignore the units."],
      True, 6),

    # ---------------- Q4 ----------------
    e("04", "4", COORD, "3.3, 5.5", 6, LATEX["04"],
      [r"M1 (AO 3.1a): " + Q4EQ + ". Notes: " + Q4BEG.format(w=1),
       r"M1 (AO 2.1): $100(1-\sin^2t)+32\sin^2t=66$ or $100\cos^2t+32(1-\cos^2t)=66$. Notes: Uses the identity "
       r"$\sin^2t+\cos^2t\equiv1$ to achieve an equation in $\sin^2t$ only or $\cos^2t$ only",
       r"A1 (AO 1.1b): $100(1-\sin^2t)+32\sin^2t=66$ or $100\cos^2t+32(1-\cos^2t)=66$. Notes: A correct equation in "
       r"$\sin^2t$ only or $\cos^2t$ only",
       r"dM1 (AO 1.1b): $100-68\sin^2t=66\Rightarrow\sin^2t=\frac{1}{2}\Rightarrow\sin t=\ldots$ or "
       r"$68\cos^2t+32=66\Rightarrow\cos^2t=\frac{1}{2}\Rightarrow\cos t=\ldots$. Notes: $\textbf{dependent on both the "
       r"previous M marks}$ Rearranges to make $\sin t=\ldots$ where $-1\leqslant\sin t\leqslant1$ or $\cos t=\ldots$ "
       r"where $-1\leqslant\cos t\leqslant1$ Note: Condone 3rd M1 for $\sin^2t=\frac{1}{2}\Rightarrow\sin t=\frac{1}{4}$",
       r"M1 (AO 1.1b): " + Q4SUB + ". Notes: See scheme",
       r"A1 (AO 3.2a): " + Q4S + r". Notes: Selects the correct coordinates for $S$ Allow either "
       r"$S=(5\sqrt{2}, -4)$ or $S=(\text{awrt }7.07, -4)$ Note: Give final A0 for writing $x=5\sqrt{2}$, $y=-4$ "
       r"followed by $S=(-4, 5\sqrt{2})$",
       r"ALT: Way 2 — M1 (AO 3.1a): $\{\cos^2t+\sin^2t=1\Rightarrow\}\left(\frac{x}{10}\right)^2+\left(\frac{y}"
       r"{4\sqrt{2}}\right)^2=1$ $\{\Rightarrow32x^2+100y^2=3200\}$. Notes: Begins to solve the problem by applying an "
       r"appropriate strategy. E.g. Way 2: A complete process of using $\cos^2t+\sin^2t\equiv1$ to convert the "
       r"parametric equation for $C_1$ into a Cartesian equation for $C_1$",
       r"ALT: Way 2 — M1 (AO 2.1): $\frac{x^2}{100}+\frac{66-x^2}{32}=1$ or $\frac{66-y^2}{100}+\frac{y^2}{32}=1$. "
       r"Notes: Complete valid attempt to write an equation in terms of $x$ only or $y$ only not involving trigonometry",
       r"ALT: Way 2 — A1 (AO 1.1b): $\frac{x^2}{100}+\frac{66-x^2}{32}=1$ or $\frac{66-y^2}{100}+\frac{y^2}{32}=1$. "
       r"Notes: A correct equation in $x$ only or $y$ only not involving trigonometry",
       r"ALT: Way 2 — dM1 (AO 1.1b): $32x^2+6600-100x^2=3200$, $x^2=50\Rightarrow x=\ldots$ or "
       r"$2112-32y^2+100y^2=3200$, $y^2=16\Rightarrow y=\ldots$. Notes: $\textbf{dependent on both the previous M "
       r"marks}$ Rearranges to make $x=\ldots$ or $y=\ldots$ Note: their $x^2$ or their $y^2$ must be $>0$ for this mark",
       r"ALT: Way 2 — M1 (AO 1.1b): Substitutes their solution back into the relevant original equation(s) to get the "
       r"value of the corresponding $x$-coordinate or $y$-coordinate. Note: These may not be in the correct quadrant. "
       r"Notes: See scheme Note: their $x^2$ and their $y^2$ must be $>0$ for this mark",
       r"ALT: Way 2 — A1 (AO 3.2a): " + Q4S + ". Notes: " + Q4SEL,
       r"ALT: Way 3 — M1 (AO 3.1a): $\{C_2:x^2+y^2=66\Rightarrow\}$ $x=\sqrt{66}\cos\alpha$, $y=\sqrt{66}\sin\alpha$; "
       r"$\{C_1=C_2\Rightarrow\}$ $10\cos t=\sqrt{66}\cos\alpha$, $4\sqrt{2}\sin t=\sqrt{66}\sin\alpha$; "
       r"$\{\cos^2\alpha+\sin^2\alpha=1\Rightarrow\}$ $\left(\frac{10\cos t}{\sqrt{66}}\right)^2+\left(\frac{4\sqrt{2}"
       r"\sin t}{\sqrt{66}}\right)^2=1$; then continue with applying the mark scheme for Way 1. Notes: Begins to solve "
       r"the problem by applying an appropriate strategy. E.g. Way 3: A complete process of writing $C_2$ in parametric "
       r"form, combining the parametric equations of $C_1$ and $C_2$ and applying $\cos^2\alpha+\sin^2\alpha\equiv1$ "
       r"to give an equation in one variable (i.e. $t$) only. Then continue with applying the mark scheme for Way 1",
       r"ALT: Way 4 — M1 (AO 3.1a): " + Q4EQ + ". Notes: " + Q4BEG.format(w=4),
       r"ALT: Way 4 — M1 (AO 2.1): $100\left(\frac{1+\cos2t}{2}\right)+32\left(\frac{1-\cos2t}{2}\right)=66$. Notes: "
       r"Uses the identities $\cos2t\equiv2\cos^2t-1$ and $\cos2t\equiv1-2\sin^2t$ to achieve an equation in "
       r"$\cos2t$ only Note: At least one of $\cos2t\equiv2\cos^2t-1$ or $\cos2t\equiv1-2\sin^2t$ must be correct "
       r"for this mark.",
       r"ALT: Way 4 — A1 (AO 1.1b): $100\left(\frac{1+\cos2t}{2}\right)+32\left(\frac{1-\cos2t}{2}\right)=66$. "
       r"Notes: A correct equation in $\cos2t$ only",
       r"ALT: Way 4 — dM1 (AO 1.1b): $50+50\cos2t+16-16\cos2t=66\Rightarrow34\cos2t+66=66\Rightarrow\cos2t=\ldots$. "
       r"Notes: $\textbf{dependent on both the previous M marks}$ Rearranges to make $\cos2t=\ldots$ where "
       r"$-1\leqslant\cos2t\leqslant1$",
       r"ALT: Way 4 — M1 (AO 1.1b): Substitutes their solution back into the original equation(s) to get the value of "
       r"the $x$-coordinate and value of the $y$-coordinate. Note: These may not be in the correct quadrant. Notes: See "
       r"scheme",
       r"ALT: Way 4 — A1 (AO 3.2a): " + Q4S + ". Notes: " + Q4SEL,
       r"ALT: Way 5 — M1 (AO 3.1a): " + Q4EQ + ". Notes: " + Q4BEG.format(w=5),
       r"ALT: Way 5 — M1 (AO 2.1): $(10\cos t)^2+(4\sqrt{2}\sin t)^2=66(\sin^2t+\cos^2t)$. Notes: Uses the identity "
       r"$\sin^2t+\cos^2t\equiv1$ to achieve an equation in $\sin^2t$ only and $\cos^2t$ only $\textbf{with no "
       r"constant term}$",
       r"ALT: Way 5 — A1 (AO 1.1b): $(10\cos t)^2+(4\sqrt{2}\sin t)^2=66(\sin^2t+\cos^2t)$. Notes: A correct equation "
       r"in $\sin^2t$ and $\cos^2t$ containing no constant term",
       r"ALT: Way 5 — dM1 (AO 1.1b): $100\cos^2t+32\sin^2t=66\sin^2t+66\cos^2t\Rightarrow34\cos^2t=34\sin^2t$ "
       r"$\Rightarrow\tan t=\ldots$. Notes: $\textbf{dependent on both the previous M marks}$ Rearranges to make "
       r"$\tan t=\ldots$",
       r"ALT: Way 5 — M1 (AO 1.1b): " + Q4SUB + ". Notes: See scheme",
       r"ALT: Way 5 — A1 (AO 3.2a): " + Q4S + ". Notes: " + Q4SEL],
      True, 8),

    # ---------------- Q5 ----------------
    e("05", "5", INT, "8.4, 8.3, 8.2", 3, LATEX["05"],
      [r"B1 (AO 1.2): States $\left\{\lim_{\delta x\to0}\sum_{x=4}^{9}\sqrt{x}\,\delta x\text{ is}\right\}$ "
       r"$\int_4^9\sqrt{x}\,\mathrm{d}x$. Notes: States $\int_4^9\sqrt{x}\,\mathrm{d}x$ with or without the "
       r"‘$\mathrm{d}x$’ Note: You can imply B1 for $\left[\lambda x^{\frac{3}{2}}\right]_4^9$ or for "
       r"$\lambda\times9^{\frac{3}{2}}-\lambda\times4^{\frac{3}{2}}$ Note: Give B0 for $\int_1^9\sqrt{x}\,\mathrm{d}x-"
       r"\int_1^3\sqrt{x}\,\mathrm{d}x$ or for $\int_3^9\sqrt{x}\,\mathrm{d}x$ without reference to a correct "
       r"$\int_4^9\sqrt{x}\,\mathrm{d}x$",
       r"M1 (AO 1.1b): $=\left[\frac{2}{3}x^{\frac{3}{2}}\right]_4^9$. Notes: Integrates $\sqrt{x}$ to give "
       r"$\lambda x^{\frac{3}{2}}$; $\lambda\neq0$",
       r"A1 (AO 1.1b): $=\frac{2}{3}\times9^{\frac{3}{2}}-\frac{2}{3}\times4^{\frac{3}{2}}=\frac{54}{3}-\frac{16}{3}$ "
       r"$=\frac{38}{3}$ or $12\frac{2}{3}$ or awrt 12.7. Notes: See scheme Note: Give B1 M1 A1 for no working leading "
       r"to a correct $\frac{38}{3}$ or $12\frac{2}{3}$ or awrt 12.7 Note: Give B1 M1 A1 for $\int_4^9\sqrt{x}\,"
       r"\mathrm{d}x=\frac{38}{3}$ or $12\frac{2}{3}$ or awrt 12.7 Note: Give B1 M1 A1 for $\left[\frac{2}{3}"
       r"x^{\frac{3}{2}}+c\right]_4^9=\frac{38}{3}$ or $12\frac{2}{3}$ or awrt 12.7 Note: Give B1 M1 A1 for no working "
       r"followed by an answer $\frac{38}{3}$ or $12\frac{2}{3}$ or awrt 12.7 Note: Give M0 A0 for use of a trapezium "
       r"rule method to give an answer of awrt 12.7, but allow B1 if $\int_4^9\sqrt{x}\,\mathrm{d}x$ is seen in a "
       r"trapezium rule method Note: Otherwise, give B0 M0 A0 for using the trapezium rule to give an answer of awrt "
       r"12.7",
       r"ALT: Alt — The following method is correct: [hand-drawn sketch: a curve rising from the origin, with 4 and 9 "
       r"marked on the vertical axis and 2 and 3 on the horizontal axis; the region $R$ between the curve and the "
       r"vertical axis from 4 to 9 and the region $A$ under the curve from 2 to 3 are shaded; written beside it: "
       r"$R=27-A-8$; below, a number line from 2 to 3 marked $2+\frac{1}{n}$, $2+\frac{2}{n}$, $2+\frac{3}{n}$, ...] "
       r"Area $(A)=\lim_{n\to\infty}\sum_{i=1}^{n}(x_i-x_{i-1})\mathrm{f}(x_i)=\lim_{n\to\infty}\sum_{i=1}^{n}"
       r"\frac{1}{n}\left(2+\frac{i}{n}\right)^2$ $=\lim_{n\to\infty}\left[\frac{1}{n}\sum_{i=1}^{n}4+\frac{1}{n}"
       r"\sum_{i=1}^{n}\left(\frac{4i}{n}\right)+\frac{1}{n}\sum_{i=1}^{n}\left(\frac{i^2}{n^2}\right)\right]$ "
       r"$=\lim_{n\to\infty}\left[\frac{1}{n}\sum_{i=1}^{n}4+\frac{4}{n^2}\sum_{i=1}^{n}i+\frac{1}{n^3}"
       r"\sum_{i=1}^{n}i^2\right]$ $=\lim_{n\to\infty}\left[\frac{4n}{n}+\frac{4}{n^2}\left(\frac{1}{2}n(n+1)\right)+"
       r"\frac{1}{n^3}\left(\frac{1}{6}n(n+1)(2n+1)\right)\right]$ $=\lim_{n\to\infty}\left[\frac{4}{n}+"
       r"\frac{4n^2+4n}{2n^2}+\frac{2n^3+3n^2+n}{6n^3}\right]$ $=\lim_{n\to\infty}\left[4+2+\frac{2}{n}+\frac{1}{3}+"
       r"\frac{1}{2n}+\frac{1}{6n^2}\right]$ $=4+2+\frac{1}{3}=\frac{19}{3}$ So, $\lim_{\delta x\to0}\sum_{x=4}^{9}"
       r"\sqrt{x}\,\delta x=\text{Area}(R)=(3\times9)-(2\times4)-\frac{19}{3}$ $=\frac{38}{3}$ or $12\frac{2}{3}$ or "
       r"awrt 12.7"],
      True, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", ALG, "2.8", 2, LATEX["06a"],
      [r"M1 (AO 2.1): $\mathrm{gg}(0)=\mathrm{g}((0-2)^2+1)=\mathrm{g}(5)=4(5)-7$. Notes: Uses a complete method to "
       r"find $\mathrm{gg}(0)$. E.g. • Substituting $x=0$ into $(0-2)^2+1$ and the result of this into the relevant "
       r"part of $\mathrm{g}(x)$ • Attempts to substitute $x=0$ into $4((x-2)^2+1)-7$ or $4(x-2)^2-3$",
       r"A1 (AO 1.1b): $=13$. Notes: $\mathrm{gg}(0)=13$"],
      True, 12),
    e("06b", "6(b)", ALG, "2.5", 4, LATEX["06b"],
      [r"M1 (AO 1.1b): Solves either $(x-2)^2+1=28\Rightarrow x=\ldots$ or $4x-7=28\Rightarrow x=\ldots$. Notes: See "
       r"scheme Note: You can ignore inequality symbols for any of the M marks Note: If a 3TQ is formed (e.g. "
       r"$x^2-4x-23=0$) then a correct method for solving a 3TQ is required for the relevant method mark to be given. "
       r"Note: Writing $(x-2)^2+1=28\Rightarrow(x-2)+1=\sqrt{28}\Rightarrow x=-1+\sqrt{28}$ (i.e. taking the "
       r"square-root of each term to solve $(x-2)^2+1=28$ is not considered to be an acceptable method)",
       r"A1 (AO 1.1b): At least one critical value $x=2-3\sqrt{3}$ or $x=\frac{35}{4}$ is correct. Notes: See scheme "
       r"Note: Writing awrt $-3.20$ or a truncated $-3.19$ or a truncated $-3.2$ in place of $2-3\sqrt{3}$ is accepted "
       r"for any of the A marks Note: Writing $2-\sqrt{27}$ in place of $2-3\sqrt{3}$ is accepted for any of the A "
       r"marks",
       r"M1 (AO 1.1b): Solves both $(x-2)^2+1=28\Rightarrow x=\ldots$ and $4x-7=28\Rightarrow x=\ldots$. Notes: See "
       r"scheme",
       r"A1 (AO 2.1): Correct final answer of ‘$x<2-3\sqrt{3}$, $x>\frac{35}{4}$’. Notes: Brings all the strands of "
       r"the problem together to give a correct solution. Note: Allow set notation. E.g. "
       r"$\{x\in\mathbb{R}:x<2-3\sqrt{3}\cup x>8.75\}$ is fine for the final A mark Note: Give final A0 for "
       r"$\{x\in\mathbb{R}:x<2-3\sqrt{3}\cap x>8.75\}$ Note: Give final A0 for $2-3\sqrt{3}>x>8.75$ Note: Allow final "
       r"A1 for their writing a final answer of “$x<2-3\sqrt{3}$ and $x>\frac{35}{4}$” Note: Allow final A1 for a "
       r"final answer of $x<2-3\sqrt{3}$, $x>\frac{35}{4}$ Note: Allow final A1 for a final answer of $x<-3.20$, "
       r"$x>8.75$ Note: Using 29 instead of 28 is M0 A0 M0 A0"],
      True, 12),
    e("06c", "6(c)", ALG, "2.8", 1, LATEX["06c"],
      [r"B1 (AO 2.4): h is a one-one {function (or mapping) so has an inverse} g is a many-one {function (or mapping) "
       r"so does not have an inverse}. Notes: A correct explanation that conveys the underlined points [underlined: "
       r"“h is a one-one” and “g is a many-one”] Note: A minimal acceptable reason is “h is a one-one and g is a "
       r"many-one” Note: Give B1 for “$\mathrm{h}^{-1}$ is one-one and $\mathrm{g}^{-1}$ is one-many” Note: Give B1 for "
       r"“h is a one-one and g is not” Note: Allow B1 for “g is a many-one and h is not”"],
      True, 12),
    e("06d", "6(d)", ALG, "2.8", 3, LATEX["06d"],
      [r"M1 (AO 1.1b): $\left\{\mathrm{h}^{-1}(x)=-\frac{1}{2}\Rightarrow\right\}$ $x=\mathrm{h}\left(-\frac{1}{2}"
       r"\right)$ [B1 on epen]. Notes: Way 1: Writes $x=\mathrm{h}\left(-\frac{1}{2}\right)$",
       r"M1 (AO 1.1b): $x=\left(-\frac{1}{2}-2\right)^2+1$ Note: Condone $x=\left(\frac{1}{2}-2\right)^2+1$. Notes: See "
       r"scheme",
       r"A1 (AO 2.2a): $\Rightarrow x=7.25$ only $\textbf{cso}$. Notes: Uses $x=\mathrm{h}\left(-\frac{1}{2}\right)$ to "
       r"deduce that $x=7.25$ only, $\textbf{cso}$",
       r"ALT: (d) Way 2 — M1 (AO 1.1b): {their $\mathrm{h}^{-1}(x)$} $=\pm2\pm\sqrt{x\pm1}$. Notes: See scheme",
       r"ALT: (d) Way 2 — M1 (AO 1.1b): Attempts to solve $\pm2\pm\sqrt{x\pm1}=-\frac{1}{2}\Rightarrow\pm\sqrt{x\pm1}="
       r"\ldots$. Notes: See scheme",
       r"ALT: (d) Way 2 — A1 (AO 2.2a): $\Rightarrow x=7.25$ only $\textbf{cso}$. Notes: Use a correct "
       r"$\mathrm{h}^{-1}(x)=2-\sqrt{x-1}$ to deduce that $x=7.25$ only, $\textbf{cso}$ Note: Give final A0 cso for "
       r"$2+\sqrt{x-1}=-\frac{1}{2}\Rightarrow\sqrt{x-1}=-\frac{5}{2}\Rightarrow x-1=\frac{25}{4}\Rightarrow x=7.25$ "
       r"Note: Give final A0 cso for $2\pm\sqrt{x-1}=-\frac{1}{2}\Rightarrow\sqrt{x-1}=-\frac{5}{2}\Rightarrow "
       r"x-1=\frac{25}{4}\Rightarrow x=7.25$ Note: Give final A1 cso for $2\pm\sqrt{x-1}=-\frac{1}{2}\Rightarrow"
       r"-\sqrt{x-1}=-\frac{5}{2}\Rightarrow x-1=\frac{25}{4}\Rightarrow x=7.25$ Note: Allow final A1 for "
       r"$2\pm\sqrt{x-1}=-\frac{1}{2}\Rightarrow\pm\sqrt{x-1}=-\frac{5}{2}\Rightarrow x-1=\frac{25}{4}\Rightarrow "
       r"x=7.25$"],
      True, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", ALG, "2.11", 1, LATEX["07a"],
      [r"B1 (AO 3.3): $y=kx+c$ {where $k$ and $c$ are constants} Note: Work for (a) cannot be recovered in (b) or (c). "
       r"Notes: Obtains a correct form of the equation. E.g. $y=kx+c$; $k\neq0$, $c\neq0$. $\textbf{Note:}$ Must be "
       r"seen in (a) Note: Ignore how the constants are labelled – as long as they appear to be constants. e.g. $k$, "
       r"$c$, $m$ etc."],
      False, 16),
    e("07b", "7(b)", ALG, "2.11, 3.1", 3, LATEX["07b"],
      [r"M1 (AO 3.1b): Either • $x=800\Rightarrow y=2(800)-500$ $\{=1100\Rightarrow(x,y)=(800, 1100)\}$ • "
       r"$x=300\Rightarrow y=2(300)+80$ $\{=680\Rightarrow(x,y)=(300, 680)\}$. Notes: Way 1: Translates the problem into "
       r"the model by finding either • $y=2(800)-500$ for $x=800$ • $y=2(300)+80$ for $x=300$ Note: Allow 1st M1 for "
       r"any of • $1600-y=500$ • $600-y=-80$ Note: Give 1st M0 for $500=800k+c$, $80=300k+c\Rightarrow k="
       r"\frac{500-80}{800-300}=0.84$",
       r"dM1 (AO 1.1b): Applies $(800, \text{their }1100)$ and $(300, \text{their }680)$ to give two equations "
       r"$1100=800k+c$ and $680=300k+c\Rightarrow k, c=\ldots$. Notes: $\textbf{dependent on the previous M mark}$ See "
       r"scheme",
       r"A1* (AO 2.1): Solves correctly to find $k=0.84$, $c=428$ and states $y=0.84x+428$ * Note: the answer "
       r"$y=0.84x+428$ must be stated in (b). Notes: See scheme – no errors in their working",
       r"ALT: (b) Way 2 — M1 (AO 3.1b): Either • $x=800\Rightarrow y=2(800)-500$ $\{=1100\Rightarrow(x,y)=(800, 1100)"
       r"\}$ • $x=300\Rightarrow y=2(300)+80$ $\{=680\Rightarrow(x,y)=(300, 680)\}$. Notes: Translates the problem into "
       r"the model by finding either $y=2(800)-500$ for $x=800$ $y=2(300)+80$ for $x=300$",
       r"ALT: (b) Way 2 — dM1 (AO 1.1b): Complete method for finding both $k=\ldots$ and $c=\ldots$ e.g. "
       r"$k=\frac{1100-680}{800-300}$ $\{=0.84\}$ $(800, 1100)\Rightarrow1100=800(0.84)+c\Rightarrow c=\ldots$. Notes: "
       r"$\textbf{dependent on the previous M mark}$ See scheme",
       r"ALT: (b) Way 2 — A1* (AO 2.1): Solves to find $k=0.84$, $c=428$ and states $y=0.84x+428$ * Note: the answer "
       r"$y=0.84x+428$ must be stated in (b). Notes: See scheme – no error in their working",
       r"ALT: (b) Way 3 — M1 (AO 3.1b): Either • $x=800\Rightarrow y=2(800)-500$ $\{=1100\Rightarrow(x,y)=(800, 1100)"
       r"\}$ • $x=300\Rightarrow y=2(300)+80$ $\{=680\Rightarrow(x,y)=(300, 680)\}$. Notes: Translates the problem into "
       r"the model by finding either $y=2(800)-500$ for $x=800$ $y=2(300)+80$ for $x=300$",
       r"ALT: (b) Way 3 — dM1 (AO 1.1b): $\{y=0.84x+428\Rightarrow\}$ $x=800\Rightarrow y=(0.84)(800)+428=1100$ "
       r"$x=300\Rightarrow y=(0.84)(300)+428=680$. Notes: $\textbf{dependent on the previous M mark}$ Uses the model "
       r"to test both points $(800, \text{their }1100)$ and $(300, \text{their }680)$",
       r"ALT: (b) Way 3 — A1* (AO 2.1): Hence $y=0.84x+428$ *. Notes: Confirms $y=0.84x+428$ is true for both "
       r"$(800, 1100)$ and $(300, 680)$ and gives a conclusion Note: Conclusion could be “$y=0.84x+428$” or “QED” or "
       r"“proved”"],
      False, 16),
    e("07c", "7(c)", ALG, "2.11", 1, LATEX["07c"],
      [r"B1 (AO 3.4): Allow any of {0.84, in £s} represents • the $\textbf{cost}$ of {making} each extra bar {of soap} "
       r"• the direct $\textbf{cost}$ of {making} a bar {of soap} • the marginal $\textbf{cost}$ of {making} a bar {of "
       r"soap} • the $\textbf{cost}$ of {making} a bar {of soap} (Condone this answer) $\textbf{Note: Do not allow}$ • "
       r"{0.84, in £s} is the profit per bar {of soap} • {0.84, in £s} is the (selling) price per bar {of soap}. Notes: "
       r"see scheme Note: Also condone B1 for “rate of change of cost”, “cost of {making} a bar”, “constant of "
       r"proportionality for cost per bar of soap” or “rate of increase in cost”, Note: Do not allow reasons such as "
       r"“price increase or decrease”, “rate of change of the bar of soap” or “decrease in cost” Note: Give B0 for "
       r"incorrect use of units. E.g. Give B0 for “the cost of making each extra bar of soap is £84” Condone the use of "
       r"£0.84p"],
      False, 16),
    e("07d", "7(d)", ALG, "2.11, 2.5", 2, LATEX["07d"],
      [r"M1 (AO 3.4): {Let $n$ be the least number of bars required to make a profit} $2n=0.84n+428\Rightarrow "
       r"n=\ldots$ (Condone $2x=0.84x+428\Rightarrow x=\ldots$). Notes: Way 1: Using the model and constructing an "
       r"argument leading to a critical value for the number of bars of soap sold. See scheme. Note: You can ignore "
       r"inequality symbols for the method mark in part (d) Note: Give M1 A1 for no working leading to 369 {bars}",
       r"A1 (AO 3.2a): Answer of 369 {bars}. Notes: 369 only. Do not accept decimal answers. Note: Give final A0 for "
       r"$x>369$ or $x>368$ or $x\geqslant369$ without $x=369$ or 369 stated as their final answer Note: Condone final "
       r"A1 for $\textbf{in words}$ “at least 369 bars must be made/sold” Note: Special Case: Assuming a profit of £1 "
       r"is required and achieving $x=370$ scores special case M1A0",
       r"ALT: (d) Way 2 — M1 (AO 3.4): • Trial 1: $n=368\Rightarrow y=(0.84)(368)+428\Rightarrow y=737.12$ "
       r"{revenue $=2(368)=736$ or loss $=1.12$}. Notes: Uses either 368 or 369 to find the cost $y=\ldots$",
       r"ALT: (d) Way 2 — A1 (AO 3.2a): • Trial 2: $n=369\Rightarrow y=(0.84)(369)+428\Rightarrow y=737.96$ {revenue "
       r"$=2(369)=738$ or profit $=0.04$} leading to an answer of 369 {bars}. Notes: Attempts both trial 1 and trial 2 "
       r"to find both the cost $y=\ldots$ and arrives at an answer of 369 only. Do not accept decimal answers."],
      False, 16),

    # ---------------- Q8 ----------------
    e("08i", "8(i)", SEQ, "4.5, 4.3", 3, LATEX["08i"],
      [r"M1 (AO 1.1b): $\sum_{r=4}^{\infty}20\times\left(\frac{1}{2}\right)^r=20\left(\frac{1}{2}\right)^4+20\left("
       r"\frac{1}{2}\right)^5+20\left(\frac{1}{2}\right)^6+\ldots$ $=\frac{20\left(\frac{1}{2}\right)^4}"
       r"{1-\frac{1}{2}}$. Notes: Way 1: " + Q8IA,
       r"M1 (AO 3.1a): $=\frac{20\left(\frac{1}{2}\right)^4}{1-\frac{1}{2}}$. Notes: Finds the infinite sum by using a "
       r"complete strategy of applying $\frac{20\left(\frac{1}{2}\right)^4}{1-\frac{1}{2}}$",
       r"A1 (AO 1.1b): $\{=(1.25)(2)\}=2.5$ o.e. Notes: 2.5 o.e. Note: Give M1 M1 A1 for a correct answer of 2.5 from "
       r"no working in (i)",
       r"ALT: (i) Way 2 — M1 (AO 1.1b): $\sum_{r=4}^{\infty}20\times\left(\frac{1}{2}\right)^r=\sum_{r=1}^{\infty}20"
       r"\times\left(\frac{1}{2}\right)^r-\sum_{r=1}^{3}20\times\left(\frac{1}{2}\right)^r$ $=\frac{10}{1-\frac{1}{2}}-"
       r"(10+5+2.5)$ or $=\frac{10}{1-\frac{1}{2}}-\frac{10\left(1-\left(\frac{1}{2}\right)^3\right)}{1-\frac{1}{2}}$. "
       r"Notes: " + Q8IA,
       r"ALT: (i) Way 2 — M1 (AO 3.1a): $=\frac{10}{1-\frac{1}{2}}-(10+5+2.5)$ or $=\frac{10}{1-\frac{1}{2}}-"
       r"\frac{10\left(1-\left(\frac{1}{2}\right)^3\right)}{1-\frac{1}{2}}$. Notes: Finds the infinite sum by using a "
       r"completely correct strategy of applying $\frac{10}{1-\frac{1}{2}}-(10+5+2.5)$ or $\frac{10}{1-\frac{1}{2}}-"
       r"\frac{10\left(1-\left(\frac{1}{2}\right)^3\right)}{1-\frac{1}{2}}$",
       r"ALT: (i) Way 2 — A1 (AO 1.1b): $\{=20-17.5\}=2.5$ o.e. Notes: 2.5 o.e.",
       r"ALT: (i) Way 3 — M1 (AO 1.1b): $\sum_{r=4}^{\infty}20\times\left(\frac{1}{2}\right)^r=\sum_{r=0}^{\infty}20"
       r"\times\left(\frac{1}{2}\right)^r-\sum_{r=0}^{3}20\times\left(\frac{1}{2}\right)^r$ $=\frac{20}{1-\frac{1}{2}}-"
       r"(20+10+5+2.5)$ or $=\frac{20}{1-\frac{1}{2}}-\frac{20\left(1-\left(\frac{1}{2}\right)^4\right)}"
       r"{1-\frac{1}{2}}$. Notes: " + Q8IA,
       r"ALT: (i) Way 3 — M1 (AO 3.1a): $=\frac{20}{1-\frac{1}{2}}-(20+10+5+2.5)$ or $=\frac{20}{1-\frac{1}{2}}-"
       r"\frac{20\left(1-\left(\frac{1}{2}\right)^4\right)}{1-\frac{1}{2}}$. Notes: Finds the infinite sum by using a "
       r"completely correct strategy of applying $\frac{20}{1-\frac{1}{2}}-(20+10+5+2.5)$ or "
       r"$\frac{20}{1-\frac{1}{2}}-\frac{20\left(1-\left(\frac{1}{2}\right)^4\right)}{1-\frac{1}{2}}$",
       r"ALT: (i) Way 3 — A1 (AO 1.1b): $\{=40-37.5\}=2.5$ o.e. Notes: 2.5 o.e."],
      False, 20),
    e("08ii", "8(ii)", SEQ, "4.3, 6.4", 3, LATEX["08ii"],
      [r"M1 (AO 1.1b): $\left\{\sum_{n=1}^{48}\log_5\left(\frac{n+2}{n+1}\right)=\right\}$ $=\log_5\left(\frac{3}{2}"
       r"\right)+\log_5\left(\frac{4}{3}\right)+\ldots\ldots+\log_5\left(\frac{50}{49}\right)=\log_5\left(\frac{3}{2}"
       r"\times\frac{4}{3}\times\ldots\times\frac{50}{49}\right)$. Notes: Way 1: Some evidence of applying the addition "
       r"law of logarithms as part of a valid proof",
       r"M1 (AO 3.1a): $=\log_5\left(\frac{3}{2}\right)+\log_5\left(\frac{4}{3}\right)+\ldots\ldots+\log_5\left("
       r"\frac{50}{49}\right)=\log_5\left(\frac{3}{2}\times\frac{4}{3}\times\ldots\times\frac{50}{49}\right)$. Notes: "
       r"Begins to solve the problem by just writing (or by combining) at least three terms including • "
       r"$\textbf{either}$ the first two terms and the last term • $\textbf{or}$ the first term and the last two terms "
       r"Note: The 2nd mark can be gained by writing any of • listing $\log_5\left(\frac{3}{2}\right), \log_5\left("
       r"\frac{4}{3}\right), \log_5\left(\frac{50}{49}\right)$ or $\log_5\left(\frac{3}{2}\right), \log_5\left("
       r"\frac{49}{48}\right), \log_5\left(\frac{50}{49}\right)$ • $\log_5\left(\frac{3}{2}\right)+\log_5\left("
       r"\frac{4}{3}\right)+\ldots\ldots+\log_5\left(\frac{50}{49}\right)$ • $\log_5\left(\frac{3}{2}\right)+\ldots\ldots"
       r"+\log_5\left(\frac{49}{48}\right)+\log_5\left(\frac{50}{49}\right)$ • $\log_5\left(\frac{3}{2}\times\frac{4}{3}"
       r"\times\ldots\times\frac{50}{49}\right)$ {this will also gain the 1st M1 mark} • $\log_5\left(\frac{3}{2}\times"
       r"\ldots\times\frac{49}{48}\times\frac{50}{49}\right)$ {this will also gain the 1st M1 mark} Note: Do not allow "
       r"the 2nd M1 if $\log_5\left(\frac{3}{2}\right), \log_5\left(\frac{4}{3}\right)$ are listed and $\log_5\left("
       r"\frac{50}{49}\right)$ is used for the first time in their applying the formula $S_{48}=\frac{48}{2}\left("
       r"\log_5\left(\frac{3}{2}\right)+\log_5\left(\frac{50}{49}\right)\right)$ Note: Listing all 48 terms: Give M0 M1 "
       r"A0 for $\log_5\left(\frac{3}{2}\right)+\log_5\left(\frac{4}{3}\right)+\log_5\left(\frac{5}{4}\right)+\ldots"
       r"\ldots+\log_5\left(\frac{50}{49}\right)=2$ {lists all terms} Give M0 M0 A0 for $0.2519\ldots+0.1787\ldots+"
       r"0.1386\ldots+\ldots\ldots+0.0125\ldots=2$ {all terms in decimals}",
       r"A1* (AO 2.1): $=\log_5\left(\frac{50}{2}\right)$ or $\log_5(25)=2$ *. Notes: Correct proof leading to a "
       r"correct answer of 2 Note: The base of 5 can be omitted for the M marks in part (ii), but the base of 5 must be "
       r"included in the final line (as shown on the mark scheme) of their solution. Note: If a student uses a mixture "
       r"of a Way 1 or Way 2 method, then award the best Way 1 mark only or the best Way 2 mark only. Note: Give M1 M0 "
       r"A0 (1st M for implied use of subtraction law of logarithms) for $\sum_{n=1}^{48}\log_5\left(\frac{n+2}{n+1}"
       r"\right)=91.8237\ldots-89.8237\ldots=2$ Note: Give M1 M1 A1 for $\sum_{n=1}^{48}\log_5\left(\frac{n+2}{n+1}"
       r"\right)=\sum_{n=1}^{48}(\log_5(n+2)-\log_5(n+1))$ $=\log_5(3\times4\times\ldots\ldots\times50)-\log_5(2\times3"
       r"\times\ldots\ldots\times49)$ $=\log_5\left(\frac{50!}{2}\right)-\log_5(49!)$ or $=\log_5(25\times49!)-"
       r"\log_5(49!)$ $=\log_525=2$",
       r"ALT: (ii) Way 2 — M1 (AO 1.1b): $\left\{\sum_{n=1}^{48}\log_5\left(\frac{n+2}{n+1}\right)=\right\}$ "
       r"$\sum_{n=1}^{48}(\log_5(n+2)-\log_5(n+1))$. Notes: Uses the subtraction law of logarithms to give "
       r"$\log_5\left(\frac{n+2}{n+1}\right)\to\log_5(n+2)-\log_5(n+1)$",
       r"ALT: (ii) Way 2 — M1 (AO 3.1a): $=(\log_53+\log_54+\ldots\ldots+\log_550)-(\log_52+\log_53+\ldots\ldots+"
       r"\log_549)$. Notes: Begins to solve the problem by writing at least three terms for each of $\log_5(n+2)$ and "
       r"$\log_5(n+1)$ including • $\textbf{either}$ the first two terms and the last term for both $\log_5(n+2)$ and "
       r"$\log_5(n+1)$ • $\textbf{or}$ the first term and the last two terms for both $\log_5(n+2)$ and $\log_5(n+1)$ "
       r"Note: This mark can be gained by writing any of • $(\log_53+\log_54+\ldots\ldots+\log_550)-(\log_52+\log_53+"
       r"\ldots\ldots+\log_549)$ • $(\log_53+\ldots\ldots+\log_549+\log_550)-(\log_52+\ldots\ldots+\log_548+\log_549)$ "
       r"• $(\log_53+\log_54+\ldots\ldots+\log_550)-(\log_52+\log_53+\ldots\ldots+\log_549)$ • $(\log_53-\log_52)+"
       r"(\log_54-\log_53)+\ldots\ldots+(\log_550-\log_549)$ • $\log_53-\log_52, \ldots\ldots, \log_549-\log_548, "
       r"\log_550-\log_549$",
       r"ALT: (ii) Way 2 — A1* (AO 2.1): $=\log_550-\log_52$ or $\log_5\left(\frac{50}{2}\right)$ or $\log_5(25)=2$ *. "
       r"Notes: Correct proof leading to a correct answer of 2"],
      False, 20),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", EXP, "6.6, 6.4", 3, LATEX["09a"],
      [r"M1 (AO 2.1): $\{d=kV^n\Rightarrow\}\log_{10}d=\log_{10}k+n\log_{10}V$ or $\log_{10}d=m\log_{10}V+c$ or "
       r"$\log_{10}d=m\log_{10}V-1.77$ seen or used as part of their argument. Notes: Way 1: See scheme Note: In their "
       r"solution to (a) and/or (b) condone writing log in place of $\log_{10}$ Note: ADVICE: Ignore labelling (a), "
       r"(b), (c) when marking this question",
       r"A1 (AO 2.4): Alludes to $d=kV^n$ and gives a full explanation by comparing their result with a linear model "
       r"e.g. $Y=MX+C$. Notes: See scheme",
       r"B1* (AO 1.1b): " + Q9B1 + r" Note: Allow B1 for $\log_{10}0.017=-1.77$ or $\log0.017=-1.77$ Note: Give B0 in "
       r"(a) for $10^{-1.77}=0.01698\ldots$ without reference to 0.017 in the same part",
       r"ALT: (a) Way 2 — M1 (AO 2.1): $\log_{10}d=m\log_{10}V+c$ or $\log_{10}d=m\log_{10}V-1.77$ or "
       r"$\log_{10}d=\log_{10}k+n\log_{10}V$ seen or used as part of their argument. Notes: See scheme",
       r"ALT: (a) Way 2 — A1 (AO 2.4): $\{d=kV^n\Rightarrow\}\log_{10}d=\log_{10}(kV^n)$ $\Rightarrow\log_{10}d="
       r"\log_{10}k+\log_{10}V^n\Rightarrow\log_{10}d=\log_{10}k+n\log_{10}V$. Notes: Starts from $d=kV^n$ (which they "
       r"do not have to state) and progresses to $\log_{10}d=\log_{10}k+n\log_{10}V$ with an intermediate step in their "
       r"working.",
       r"ALT: (a) Way 2 — B1* (AO 1.1b): " + Q9B1,
       r"ALT: (a) Way 3 — M1 (AO 2.1): Starts from $\log_{10}d=m\log_{10}V+c$ or $\log_{10}d=m\log_{10}V-1.77$. Notes: "
       r"Starts their argument from $\log_{10}d=m\log_{10}V+c$ or $\log_{10}d=m\log_{10}V-1.77$",
       r"ALT: (a) Way 3 — A1 (AO 2.4): $\log_{10}d=m\log_{10}V+c\Rightarrow d=10^{m\log_{10}V+c}\Rightarrow d=10^cV^m"
       r"\Rightarrow d=kV^n$ $\textbf{or}$ $\log_{10}d=m\log_{10}V-1.77\Rightarrow d=10^{m\log_{10}V-1.77}\Rightarrow "
       r"d=10^{-1.77}V^m\Rightarrow d=kV^n$. Notes: Mathematical explanation is seen by showing any of either • "
       r"$\log_{10}d=m\log_{10}V+c\to d=10^cV^m$ or $d=kV^n$ • $\log_{10}d=m\log_{10}V-1.77\to d=10^{-1.77}V^m$ or "
       r"$d=kV^n$ with no errors seen in their working",
       r"ALT: (a) Way 3 — B1* (AO 1.1b): " + Q9B1],
      True, 24),
    e("09b", "9(b)", EXP, "6.6, 6.5", 3, LATEX["09b"],
      [r"M1 (AO 3.4): $\{d=20, V=30\Rightarrow\}$ $20=k(30)^n$ or $\log_{10}20=\log_{10}k+n\log_{10}30$. Notes: "
       r"Applies $V=30$ and $d=20$ to their model $\textbf{(correct way round)}$",
       r"M1 (AO 1.1b): $20=k(30)^n\Rightarrow\log20=\log k+n\log30\Rightarrow n=\frac{\log20-\log k}{\log30}"
       r"\Rightarrow n=\ldots$ or $\log_{10}20=\log_{10}k+n\log_{10}30\Rightarrow n=\frac{\log_{10}20-\log_{10}k}"
       r"{\log_{10}30}\Rightarrow n=\ldots$. Notes: Applies $(V, d)=(30, 20)$ or $(20, 30)$ and applies logarithms "
       r"correctly leading to $n=\ldots$",
       r"A1 (AO 1.1b): $\{n=\text{awrt }2.08\Rightarrow\}$ $d=(0.017)V^{2.08}$ $\textbf{or}$ $\log_{10}d=-1.77+"
       r"2.08\log_{10}V$ Note: You can recover the A1 mark for a correct model equation given in part (c). Notes: "
       r"$d=(0.017)V^{2.08}$ or $\log_{10}d=-1.77+2.08\log_{10}V$ or $\log_{10}d=\log_{10}(0.017)+2.08\log_{10}V$ Note: "
       r"Allow $k=$ awrt 0.017 and/or $n=$ awrt 2.08 in their final model equation Note: M0 M1 A0 is a possible score "
       r"for (b)"],
      True, 24),
    e("09c", "9(c)", EXP, "6.6, 2.11", 3, LATEX["09c"],
      [r"M1 (AO 3.4): $d=(0.017)(60)^{2.08}$. Notes: Applies $V=60$ to their exponential model or their logarithmic "
       r"model",
       r"M1 (AO 3.1b): • $13.333\ldots+84.918\ldots=98.251\ldots\Rightarrow$ Sean stops in time. Notes: Uses their "
       r"model in a correct problem-solving process of either • adding a “thinking distance” to their value of their "
       r"$d$ to find an overall stopping distance • applying 100 – “thinking distance” and finds their value of $d$ "
       r"Note: $\frac{1}{75}$ or 48 are examples of acceptable thinking distances Note: The thinking distance must be "
       r"dimensionally correct for the M1 mark. i.e. $0.8\times$ their velocity",
       r"A1ft (AO 3.2a): • $100-13.333\ldots=86.666\ldots$ & $d=84.918\Rightarrow$ Sean stops in time. Notes: "
       r"$\textbf{Either}$ adds 13.3… to their $d$ to find a total stopping distance and gives a correct ft conclusion "
       r"$\textbf{or}$ finds their $d$ and a comparative 86.666…(m) or awrt 87 (m) and gives a correct ft conclusion "
       r"Note: A thinking distance of awrt 13 and a value of $d$ in the range [81.5, 88.5] are required for A1ft Note: "
       r"Allow “Sean stops in time” or “Yes he stops in time” or “he misses the puddle” as relevant conclusions. Note: "
       r"A mark of M0 M1 A0 is possible in (c)"],
      True, 24),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", VEC, "10.3", 2, LATEX["10a"],
      [r"M1 (AO 3.1a): [diagram: triangle $OCB$ with $A$ on $OC$, $M$ on $AB$, and the line from $C$ through $M$ "
       r"meeting $OB$ at $N$] $" + V("OA") + "=" + A + ", " + V("OB") + "=" + B + r"$; $\left\{" + V("CM") + "="
       + V("CA") + "+" + V("AM") + "=" + V("CA") + r"+\frac{1}{2}" + V("AB") + r"\Rightarrow\right\}$ $" + V("CM")
       + r"=-" + A + r"+\frac{1}{2}(" + B + "-" + A + r")$ or $\left\{" + V("CM") + "=" + V("CB") + "+" + V("BM")
       + "=" + V("CB") + r"+\frac{1}{2}" + V("BA") + r"\Rightarrow\right\}$ $" + V("CM") + "=(-2" + A + "+" + B
       + r")+\frac{1}{2}(" + A + "-" + B + r")$. Notes: Valid attempt to find $" + V("CM") + r"$ using a combination "
       r"of known vectors $" + A + "$ and $" + B + r"$ Note: Give M1 for $" + V("CM") + r"=-" + A + r"+\frac{1}{2}("
       + B + "-" + A + ")$ or $" + V("CM") + "=(-2" + A + "+" + B + r")+\frac{1}{2}(" + A + "-" + B + r")$ or for "
       r"$\left\{" + V("CM") + "=" + V("OM") + "-" + V("OC") + r"\Rightarrow\right\}$ $" + V("CM") + r"=\frac{1}{2}("
       + A + "+" + B + ")-2" + A + r"$ $\textbf{only o.e.}$ Note: (a) Special Case where the point $C$ is believed to "
       r"be below the origin $O$ [sketch: triangle $OAB$ with $M$ on $AB$, the line $OM$, and $C$ below $O$ on the line "
       r"$AO$ extended]: Give Special Case M1 A0 in part (a) for $\left\{" + V("CM") + "=" + V("CA") + "+" + V("AM")
       + r"\Rightarrow\right\}$ $" + V("CM") + "=3" + A + r"+\frac{1}{2}(" + B + "-" + A + r")$ $\left\{\text{which "
       r"leads to }" + V("CM") + r"=\frac{5}{2}" + A + r"+\frac{1}{2}" + B + r"\right\}$",
       r"A1 (AO 1.1b): $\Rightarrow" + V("CM") + r"=-\frac{3}{2}" + A + r"+\frac{1}{2}" + B + r"$ $\textit{(needs to be "
       r"simplified and seen in (a) only)}$. Notes: A simplified correct answer for $" + V("CM") + "$"],
      True, 28),
    e("10b", "10(b)", VEC, "10.3, 10.5", 2, LATEX["10b"],
      [r"M1 (AO 1.1b): $" + V("ON") + "=" + V("OC") + "+" + V("CN") + r"\Rightarrow" + V("ON") + "=" + V("OC")
       + r"+\lambda" + V("CM") + r"$. Notes: Uses $" + V("ON") + "=" + V("OC") + r"+\lambda" + V("CM") + r"$ Note: "
       r"Special Case: Give SC M1 A0 for the solution $" + V("ON") + "=" + V("OA") + "+" + V("AM") + "+" + V("MN")
       + r"\Rightarrow" + V("ON") + "=" + V("OA") + "+" + V("AM") + r"+\lambda" + V("CM") + "$ $" + V("ON") + "="
       + A + r"+\frac{1}{2}(" + B + "-" + A + r")+\lambda\left(-\frac{3}{2}" + A + r"+\frac{1}{2}" + B + r"\right)$ "
       r"$\left\{=\left(\frac{1}{2}-\frac{3}{2}\lambda\right)" + A + r"+\left(\frac{1}{2}+\frac{1}{2}\lambda\right)"
       + B + r"\right\}$ Note: Part (b) and part (c) can be marked together.",
       r"A1* (AO 2.1): $" + V("ON") + "=2" + A + r"+\lambda\left(-\frac{3}{2}" + A + r"+\frac{1}{2}" + B + r"\right)"
       r"\Rightarrow" + V("ON") + r"=\left(2-\frac{3}{2}\lambda\right)" + A + r"+\frac{1}{2}\lambda" + B + r"$ *. "
       r"Notes: Correct proof",
       r"ALT: (b) Alternative 1 — M1 A1: Give M1 A1 for the following alternative solution: $" + V("ON") + "="
       + V("OA") + "+" + V("AM") + "+" + V("MN") + r"\Rightarrow" + V("ON") + "=" + V("OA") + "+" + V("AM")
       + r"+\mu" + V("CM") + "$ $" + V("ON") + "=" + A + r"+\frac{1}{2}(" + B + "-" + A + r")+\mu\left(-\frac{3}{2}"
       + A + r"+\frac{1}{2}" + B + r"\right)=\left(\frac{1}{2}-\frac{3}{2}\mu\right)" + A + r"+\left(\frac{1}{2}+"
       r"\frac{1}{2}\mu\right)" + B + r"$ $\mu=\lambda-1\Rightarrow" + V("ON") + r"=\left(\frac{1}{2}-\frac{3}{2}"
       r"(\lambda-1)\right)" + A + r"+\left(\frac{1}{2}+\frac{1}{2}(\lambda-1)\right)" + B + r"\Rightarrow" + V("ON")
       + r"=\left(2-\frac{3}{2}\lambda\right)" + A + r"+\frac{1}{2}\lambda" + B + "$"],
      True, 28),
    e("10c", "10(c)", VEC, "10.5, 10.3", 2, LATEX["10c"],
      [r"M1 (AO 2.2a): $\left(2-\frac{3}{2}\lambda\right)=0\Rightarrow\lambda=\ldots$. Notes: Way 1, Way 2 and Way 3: "
       r"Deduces that $\left(2-\frac{3}{2}\lambda\right)=0$ and attempts to find the value of $\lambda$",
       r"A1* (AO 2.1): $\lambda=\frac{4}{3}\Rightarrow" + V("ON") + r"=\frac{2}{3}" + B + r"$ $\left\{\Rightarrow"
       + V("NB") + r"=\frac{1}{3}" + B + r"\right\}\Rightarrow ON:NB=2:1$ *. Notes: Correct proof",
       r"ALT: (c) Way 2 — M1 (AO 2.2a): $" + V("ON") + r"=\mu" + B + r"\Rightarrow\left(2-\frac{3}{2}\lambda\right)"
       + A + r"+\frac{1}{2}\lambda" + B + r"=\mu" + B + "$; $" + A + r":\left(2-\frac{3}{2}\lambda\right)=0\Rightarrow"
       r"\lambda=\ldots$ $\left\{" + B + r":\frac{1}{2}\lambda=\mu\ \&\ \lambda=\frac{4}{3}\Rightarrow\mu=\frac{2}{3}"
       r"\right\}$. Notes: Deduces that $\left(2-\frac{3}{2}\lambda\right)=0$ and attempts to find the value of "
       r"$\lambda$",
       r"ALT: (c) Way 2 — A1* (AO 2.1): $\lambda=\frac{4}{3}$ or $\mu=\frac{2}{3}\Rightarrow" + V("ON")
       + r"=\frac{2}{3}" + B + r"$ $\left\{\Rightarrow" + V("NB") + r"=\frac{1}{3}" + B + r"\right\}\Rightarrow "
       r"ON:NB=2:1$ *. Notes: Correct proof",
       r"ALT: (c) Way 3 — M1 (AO 2.2a): $" + V("OB") + "=" + V("ON") + "+" + V("NB") + r"\Rightarrow" + B
       + r"=\left(2-\frac{3}{2}\lambda\right)" + A + r"+\frac{1}{2}\lambda" + B + "+K" + B + "$; $" + A
       + r":\left(2-\frac{3}{2}\lambda\right)=0\Rightarrow\lambda=\ldots$ $\left\{" + B + r":1=\frac{1}{2}\lambda+K\ "
       r"\&\ \lambda=\frac{4}{3}\Rightarrow K=\frac{1}{3}\right\}$. Notes: Deduces that $\left(2-\frac{3}{2}\lambda"
       r"\right)=0$ and attempts to find the value of $\lambda$",
       r"ALT: (c) Way 3 — A1 (AO 2.1): $\lambda=\frac{4}{3}$ or $K=\frac{1}{3}\Rightarrow" + V("ON") + r"=\frac{2}{3}"
       + B + "$ or $" + V("NB") + r"=\frac{1}{3}" + B + r"\Rightarrow ON:NB=2:1$ *. Notes: A1*: Correct proof",
       r"ALT: (c) Way 4 — M1 (AO 2.2a): $" + V("ON") + r"=\mu" + B + r"$ & $" + V("CN") + "=k" + V("CM")
       + r"\Rightarrow" + V("CO") + "+" + V("ON") + "=k" + V("CM") + "$; $-2" + A + r"+\mu" + B + r"=k\left(-\frac{3}"
       r"{2}" + A + r"+\frac{1}{2}" + B + r"\right)$; $" + A + r":-2=-\frac{3}{2}k\Rightarrow k=\frac{4}{3}$, $" + B
       + r":\mu=\frac{1}{2}k\Rightarrow\mu=\frac{1}{2}\left(\frac{4}{3}\right)=\ldots$. Notes: Complete attempt to find "
       r"the value of $\mu$",
       r"ALT: (c) Way 4 — A1 (AO 2.1): $\mu=\frac{2}{3}\Rightarrow" + V("ON") + r"=\frac{2}{3}" + B
       + r"$ $\left\{\Rightarrow" + V("NB") + r"=\frac{1}{3}" + B + r"\right\}\Rightarrow ON:NB=2:1$ *. Notes: A1*: "
       r"Correct proof"],
      True, 28),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", DIFF, "7.3, 7.5, 6.4", 5, LATEX["11a"],
      [r"B1 (AO 1.1a): $\{y=x^x\Rightarrow\}\ln y=x\ln x$. Notes: Way 1: $\ln y=x\ln x$. Condone $\log_xy=x\log_xx$ or "
       r"$\log_xy=x$ Note: A common solution: A maximum of 3 marks (i.e. B1 1st M1 and 2nd M1) can be given for the "
       r"solution $\log y=x\log x\Rightarrow\frac{1}{y}\frac{\mathrm{d}y}{\mathrm{d}x}=1+\log x$ "
       r"$\left\{\frac{\mathrm{d}y}{\mathrm{d}x}=0\Rightarrow\right\}1+\log x=0\Rightarrow x=10^{-1}$ • 1st B1 for "
       r"$\log y=x\log x$ • 1st M1 for $\log y\to\lambda\frac{1}{y}\frac{\mathrm{d}y}{\mathrm{d}x}$; $\lambda\neq0$ or "
       r"$x\log x\to1+\log x$ or $\frac{x}{x}+\log x$ • 2nd M1 can be given for $1+\log x=0\Rightarrow\log x=k"
       r"\Rightarrow x=\ldots$; $k\neq0$",
       r"M1 (AO 1.1b): $\frac{1}{y}\frac{\mathrm{d}y}{\mathrm{d}x}=1+\ln x$. Notes: For either $\ln y\to\frac{1}{y}"
       r"\frac{\mathrm{d}y}{\mathrm{d}x}$ or $x\ln x\to1+\ln x$ or $\frac{x}{x}+\ln x$",
       r"A1 (AO 2.1): $\frac{1}{y}\frac{\mathrm{d}y}{\mathrm{d}x}=1+\ln x$. Notes: Correct differentiated equation. "
       r"i.e. $\frac{1}{y}\frac{\mathrm{d}y}{\mathrm{d}x}=1+\ln x$ or $\frac{1}{y}\frac{\mathrm{d}y}{\mathrm{d}x}="
       r"\frac{x}{x}+\ln x$ or $\frac{\mathrm{d}y}{\mathrm{d}x}=y(1+\ln x)$ or $\frac{\mathrm{d}y}{\mathrm{d}x}="
       r"x^x(1+\ln x)$",
       r"M1 (AO 1.1b): " + Q11B_COMMON,
       r"A1 (AO 1.1b): $x=\mathrm{e}^{-1}$ or awrt 0.368. Notes: $x=\mathrm{e}^{-1}$ or awrt 0.368 only (with no other "
       r"solutions for $x$) Note: Give no marks for no working leading to 0.368 Note: Give M0 A0 M0 A0 for "
       r"$\ln y=x\ln x\to x=0.368$ with no intermediate working Note: Give B1 M1 A0 M1 A1 for the following solution: "
       r"$\{y=x^x\Rightarrow\}\ln y=x\ln x\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}x}=1+\ln x\Rightarrow1+\ln x=0"
       r"\Rightarrow x=\mathrm{e}^{-1}$ or awrt 0.368",
       r"ALT: (a) Way 2 — B1 (AO 1.1a): $\{y=x^x\Rightarrow\}y=\mathrm{e}^{x\ln x}$. Notes: $y=\mathrm{e}^{x\ln x}$",
       r"ALT: (a) Way 2 — M1 (AO 1.1b): $\frac{\mathrm{d}y}{\mathrm{d}x}=\left(\frac{x}{x}+\ln x\right)"
       r"\mathrm{e}^{x\ln x}$. Notes: For either $y=\mathrm{e}^{x\ln x}\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}x}="
       r"\mathrm{f}(\ln x)\mathrm{e}^{x\ln x}$ or $x\ln x\to1+\ln x$ or $\frac{x}{x}+\ln x$",
       r"ALT: (a) Way 2 — A1 (AO 2.1): $\frac{\mathrm{d}y}{\mathrm{d}x}=\left(\frac{x}{x}+\ln x\right)"
       r"\mathrm{e}^{x\ln x}$. Notes: Correct differentiated equation. i.e. $\frac{\mathrm{d}y}{\mathrm{d}x}=\left("
       r"\frac{x}{x}+\ln x\right)\mathrm{e}^{x\ln x}$ or $\frac{\mathrm{d}y}{\mathrm{d}x}=(1+\ln x)\mathrm{e}^{x\ln x}$ "
       r"or $\frac{\mathrm{d}y}{\mathrm{d}x}=x^x(1+\ln x)$",
       r"ALT: (a) Way 2 — M1 (AO 1.1b): " + Q11B_COMMON,
       r"ALT: (a) Way 2 — A1 (AO 1.1b): $x=\mathrm{e}^{-1}$ or awrt 0.368. Notes: $x=\mathrm{e}^{-1}$ or awrt 0.368 "
       r"only (with no other solutions for $x$)"],
      True, 32),
    e("11b", "11(b)", NUM, "9.1", 2, LATEX["11b"],
      [r"M1 (AO 1.1b): Attempts both $1.5^{1.5}=1.8\ldots$ and $1.6^{1.6}=2.1\ldots$ and at least one result is "
       r"correct to awrt 1 dp. Notes: Way 1: Attempts both $1.5^{1.5}=1.8\ldots$ and $1.6^{1.6}=2.1\ldots$ and at least "
       r"one result is correct to awrt 1 dp",
       r"A1 (AO 2.1): $1.8\ldots<2$ and $2.1\ldots>2$ and as $C$ is continuous then $1.5<\alpha<1.6$. Notes: Both "
       r"$1.5^{1.5}=\text{awrt }1.8\ldots$ and $1.6^{1.6}=\text{awrt }2.1\ldots$, reason (e.g. $1.8\ldots<2$ and "
       r"$2.1\ldots>2$ or states $C$ cuts through $y=2$), $C$ continuous and conclusion",
       r"ALT: (b) Way 2 — M1 (AO 1.1b): For $x^x-2$, attempts both $1.5^{1.5}-2=-0.16\ldots$ and $1.6^{1.6}-2="
       r"0.12\ldots$ and at least one result is correct to awrt 1 dp. Notes: Attempts both $1.5^{1.5}-2=-0.16\ldots$ "
       r"and $1.6^{1.6}-2=0.12\ldots$ and at least one result is correct to awrt 1 dp",
       r"ALT: (b) Way 2 — A1 (AO 2.1): $-0.16\ldots<0$ and $0.12\ldots>0$ and as $C$ is continuous then "
       r"$1.5<\alpha<1.6$. Notes: Both $1.5^{1.5}-2=-0.16\ldots$ and $1.6^{1.6}-2=0.12\ldots$ correct to awrt 1 dp, "
       r"reason (e.g. $-0.16\ldots<0$ and $0.12\ldots>0$, sign change or states C cuts through $y=0$), $C$ continuous "
       r"and conclusion",
       r"ALT: (b) Way 3 — M1 (AO 1.1b): For $\ln y=x\ln x$, attempts both $1.5\ln1.5=0.608\ldots$ and "
       r"$1.6\ln1.6=0.752\ldots$ and at least one result is correct to awrt 1 dp. Notes: Attempts both "
       r"$1.5\ln1.5=0.608\ldots$ and $1.6\ln1.6=0.752\ldots$ and at least one result is correct to awrt 1 dp",
       r"ALT: (b) Way 3 — A1 (AO 2.1): $0.608\ldots<0.69\ldots$ and $0.752\ldots>0.69\ldots$ and as $C$ is continuous "
       r"then $1.5<\alpha<1.6$. Notes: Both $1.5\ln1.5=0.608\ldots$ and $1.6\ln1.6=0.752\ldots$ correct to awrt 1 dp, "
       r"reason (e.g. $0.608\ldots<0.69\ldots$ and $0.752\ldots>0.69\ldots$ or states they are either side of $\ln2$), "
       r"$C$ continuous and conclusion.",
       r"ALT: (b) Way 4 — M1 (AO 1.1b): For $\log y=x\log x$, attempts both $1.5\log1.5=0.264\ldots$ and "
       r"$1.6\log1.6=0.326\ldots$ and at least one result is correct to awrt 2 dp. Notes: Attempts both "
       r"$1.5\log1.5=0.264\ldots$ and $1.6\log1.6=0.326\ldots$ and at least one result is correct to awrt 2 dp",
       r"ALT: (b) Way 4 — A1 (AO 2.1): $0.264\ldots<0.301\ldots$ and $0.326\ldots>0.301\ldots$ and as $C$ is "
       r"continuous then $1.5<\alpha<1.6$. Notes: Both $1.5\log1.5=0.264\ldots$ and $1.6\log1.6=0.326\ldots$ correct to "
       r"awrt 2 dp, reason (e.g. $0.264\ldots<0.301\ldots$ and $0.326\ldots>0.301\ldots$ or states they are either side "
       r"of $\log2$), $C$ continuous and conclusion."],
      True, 32),
    e("11c", "11(c)", NUM, "9.2", 2, LATEX["11c"],
      [r"M1 (AO 1.1b): Attempts $x_{n+1}=2x_n^{1-x_n}$ at least once with $x_1=1.5$ Can be implied by "
       r"$2(1.5)^{1-1.5}$ or awrt 1.63. Notes: An attempt to use the given or their formula once. Can be implied by "
       r"$2(1.5)^{1-1.5}$ or awrt 1.63 Note: M1 can be implied by stating their final answer $x_4=\text{awrt }1.673$",
       r"A1 (AO 1.1b): $\{x_4=1.67313\ldots\Rightarrow\}$ $x_4=1.673$ (3 dp) $\textbf{cao}$. Notes: States "
       r"$x_4=1.673$ $\textbf{cao}$ (to 3 dp) Note: Give M1 A1 for stating $x_4=1.673$ Note: $x_2=1.63299\ldots$, "
       r"$x_3=1.46626\ldots$, $x_4=1.67313\ldots$"],
      True, 32),
    e("11d", "11(d)", NUM, "9.2, 9.3", 2, LATEX["11d"],
      [r"B1 (AO 2.5): Give 1st B1 for any of • oscillates • periodic • non-convergent • divergent • fluctuates • goes up "
       r"and down • 1, 2, 1, 2, 1, 2 • alternates (condone); Give B1 B1 for any of • periodic {sequence} with period 2 "
       r"• oscillates between 1 and 2. Notes: see scheme Note: Only marks of B1B0 or B1B1 are possible in (d) Note: "
       r"Give B0 B0 for “Converges in a cob-web pattern” or “Converges up and down to $\alpha$”",
       r"B1 (AO 2.5): Condone B1 B1 for any of • fluctuates between 1 and 2 • keep getting 1, 2 • alternates between 1 "
       r"and 2 • goes up and down between 1 and 2 • 1, 2, 1, 2, 1, 2, …. Notes: see scheme"],
      True, 32),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", TRIG, "5.8, 5.6", 4, LATEX["12a"],
      [r"M1 (AO 3.1a): $\{\text{LHS}=\}\frac{\cos3\theta\cos\theta+\sin3\theta\sin\theta}{\sin\theta\cos\theta}$. "
       r"Notes: Way 1 and Way 2: Correct valid method forming a common denominator of $\sin\theta\cos\theta$ i.e. "
       r"correct process of $\frac{(\ldots)\cos\theta+(\ldots)\sin\theta}{\cos\theta\sin\theta}$ Note: Writing $" + Q12L
       + r"=\frac{\cos3\theta\cos\theta}{\sin\theta\cos\theta}+\frac{\sin3\theta\sin\theta}{\sin\theta\cos\theta}$ is "
       r"considered a correct valid method of forming a common denominator of $\sin\theta\cos\theta$ for the 1st M1 mark "
       r"Note: Give 1st M0 e.g. for $" + Q12L + r"=\frac{\cos4\theta+\sin4\theta}{\sin\theta\cos\theta}$ but allow 1st "
       r"M1 for $" + Q12L + r"=\frac{\cos3\theta\cos\theta+\sin3\theta\sin\theta}{\sin\theta\cos\theta}=\frac{\cos4\theta"
       r"+\sin4\theta}{\sin\theta\cos\theta}$ Note: Give 1st M0 e.g. for $" + Q12L + r"=\frac{\cos^23\theta+"
       r"\sin^23\theta}{\sin\theta\cos\theta}$ but allow 1st M1 for $" + Q12L + r"=\frac{\cos3\theta\cos\theta+"
       r"\sin3\theta\sin\theta}{\sin\theta\cos\theta}=\frac{\cos^23\theta+\sin^23\theta}{\sin\theta\cos\theta}$ Note: "
       r"Allow 1st M1 1st A1 (together) for any of $\text{LHS}\to\frac{\cos2\theta}{\sin\theta\cos\theta}$ or "
       r"$\text{LHS}\to\frac{\cos2\theta(\cos^2\theta+\sin^2\theta)}{\sin\theta\cos\theta}$ or $\text{LHS}\to\cos2\theta"
       r"(\cot\theta+\tan\theta)$ or $\text{LHS}\to\cos2\theta\left(\frac{1+\tan^2\theta}{\tan\theta}\right)$ (i.e. "
       r"where $\cos2\theta$ has been factorised out) Note: Allow 1st M1 1st A1 for progressing as far as "
       r"$\text{LHS}=\ldots=\cot x-\tan x$",
       r"A1 (AO 2.1): $=\frac{\cos(3\theta-\theta)}{\sin\theta\cos\theta}$ $\left\{=\frac{\cos2\theta}{\sin\theta"
       r"\cos\theta}\right\}$. Notes: Proceeds to show that the numerator of their resulting fraction simplifies to "
       r"$\cos(3\theta-\theta)$ or $\cos2\theta$ Note: E.g. going from $\frac{\cos2\theta\cos^2\theta-\sin2\theta"
       r"\sin\theta\cos\theta+\sin2\theta\cos\theta\sin\theta+\cos2\theta\sin^2\theta}{\sin\theta\cos\theta}$ to "
       r"$\frac{\cos2\theta}{\sin\theta\cos\theta}$ with no intermediate working is 1st A0",
       r"dM1 (AO 1.1b): $=\frac{\cos2\theta}{\frac{1}{2}\sin2\theta}$. Notes: $\textbf{dependent on the previous M "
       r"mark}$ Applies a correct $\sin2\theta\equiv2\sin\theta\cos\theta$ to the common denominator "
       r"$\sin\theta\cos\theta$ Note: Allow 2nd M1 for stating a correct $\sin2\theta=2\sin\theta\cos\theta$ and for "
       r"attempting to apply it to the common denominator $\sin\theta\cos\theta$",
       r"A1* (AO 2.1): $=2\cot2\theta$ *. Notes: Correct proof",
       r"ALT: (a) Way 2 — M1 (AO 3.1a): $\{\text{LHS}=\}\frac{\cos2\theta\cos\theta-\sin2\theta\sin\theta}{\sin\theta}"
       r"+\frac{\sin2\theta\cos\theta+\cos2\theta\sin\theta}{\cos\theta}$ $=\frac{\cos2\theta\cos^2\theta-\sin2\theta"
       r"\sin\theta\cos\theta+\sin2\theta\cos\theta\sin\theta+\cos2\theta\sin^2\theta}{\sin\theta\cos\theta}$. Notes: "
       r"Correct valid method forming a common denominator of $\sin\theta\cos\theta$",
       r"ALT: (a) Way 2 — A1 (AO 2.1): $=\frac{\cos2\theta(\cos^2\theta+\sin^2\theta)}{\sin\theta\cos\theta}$ "
       r"$\left\{=\frac{\cos2\theta}{\sin\theta\cos\theta}\right\}$. Notes: Proceeds to show that the numerator of their "
       r"resulting fraction simplifies to $\cos(3\theta-\theta)$ or $\cos2\theta$",
       r"ALT: (a) Way 2 — dM1 (AO 1.1b): $=\frac{\cos2\theta}{\frac{1}{2}\sin2\theta}$. Notes: $\textbf{dependent on "
       r"the previous M mark}$ Applies a correct $\sin2\theta\equiv2\sin\theta\cos\theta$ to the common denominator "
       r"$\sin\theta\cos\theta$",
       r"ALT: (a) Way 2 — A1* (AO 2.1): $=2\cot2\theta$ *. Notes: Correct proof",
       r"ALT: (a) Way 3 — M1 (AO 3.1a): $\{\text{RHS}=\}\frac{2\cos2\theta}{\sin2\theta}=\frac{2\cos(3\theta-\theta)}"
       r"{\sin2\theta}=\frac{2(\cos3\theta\cos\theta+\sin3\theta\sin\theta)}{\sin2\theta}$. Notes: Starts from RHS and "
       r"proceeds to expand $\cos2\theta$ in the form $\cos3\theta\cos\theta\pm\sin3\theta\sin\theta$",
       r"ALT: (a) Way 3 — A1 (AO 2.1): $=\frac{2(\cos3\theta\cos\theta+\sin3\theta\sin\theta)}{\sin2\theta}$. Notes: "
       r"Shows, as part of their proof, that $\cos2\theta=\cos3\theta\cos\theta+\sin3\theta\sin\theta$",
       r"ALT: (a) Way 3 — dM1 (AO 1.1b): $=\frac{2(\cos3\theta\cos\theta+\sin3\theta\sin\theta)}{2\sin\theta"
       r"\cos\theta}$. Notes: $\textbf{dependent on the previous M mark}$ Applies $\sin2\theta\equiv2\sin\theta"
       r"\cos\theta$ to their denominator",
       r"ALT: (a) Way 3 — A1* (AO 2.1): $=" + Q12L + r"$ *. Notes: Correct proof",
       r"ALT: (a) correct alternative solution — The following is a correct alternative solution $" + Q12L + r"="
       r"\frac{\cos3\theta\cos\theta+\sin3\theta\sin\theta}{\sin\theta\cos\theta}=\frac{\frac{1}{2}(\cos4\theta+"
       r"\cos2\theta)-\frac{1}{2}(\cos4\theta-\cos2\theta)}{\sin\theta\cos\theta}$ $=\frac{\cos2\theta}{\sin\theta"
       r"\cos\theta}=\frac{\cos2\theta}{\frac{1}{2}\sin2\theta}=2\cot2\theta$ *"],
      False, 36),
    e("12b", "12(b)", TRIG, "5.7, 5.4", 3, LATEX["12b"],
      [r"M1 (AO 1.1b): $\left\{" + Q12L + r"=4\Rightarrow\right\}$ $2\cot2\theta=4\Rightarrow2\left(\frac{1}"
       r"{\tan2\theta}\right)=4$. Notes: Way 1: Evidence of applying $\cot2\theta=\frac{1}{\tan2\theta}$ Note: Give "
       r"M0M0A0 for writing, for example, $\tan2\theta=2$ with no evidence of applying $\cot2\theta=\frac{1}"
       r"{\tan2\theta}$ Note: 1st M1 can be implied by seeing $\tan2\theta=\frac{1}{2}$ Note: Give M1 dM1 A1 for no "
       r"working leading to $\theta=\text{awrt }103.3^\circ$ and no other solutions Note: Give M1 dM1 A0 for no working "
       r"leading to $\theta=\text{awrt }103.3^\circ$ and other solutions which can be either outside or inside the "
       r"range $90^\circ<\theta<180^\circ$",
       r"dM1 (AO 1.1b): Rearranges to give $\tan2\theta=k$; $k\neq0$ and applies $\arctan k$. Notes: "
       r"$\textbf{dependent on the previous M mark}$ Rearranges to give $\tan2\theta=k$, $k\neq0$, and applies "
       r"$\arctan k$ Note: Condone 2nd M1 for applying $\frac{1}{2}\arctan\left(\frac{1}{2}\right)$ $\{=13.28\ldots\}$",
       r"A1 (AO 2.2a): $\left\{90^\circ<\theta<180^\circ, \tan2\theta=\frac{1}{2}\Rightarrow\right\}$ " + Q12ANS,
       r"ALT: (b) Way 2 — M1 (AO 1.1b): $\left\{" + Q12L + r"=4\Rightarrow\right\}$ $2\cot2\theta=4\Rightarrow"
       r"\frac{2}{\tan2\theta}=4$. Notes: Evidence of applying $\cot2\theta=\frac{1}{\tan2\theta}$",
       r"ALT: (b) Way 2 — dM1 (AO 1.1b): $\frac{2}{\left(\frac{2\tan\theta}{1-\tan^2\theta}\right)}=4\Rightarrow"
       r"2(1-\tan^2\theta)=8\tan\theta$ $\Rightarrow\tan^2\theta+4\tan\theta-1=0\Rightarrow\tan\theta=\frac{-4\pm"
       r"\sqrt{(4)^2-4(1)(-1)}}{2(1)}$ $\{\Rightarrow\tan\theta=-2\pm\sqrt{5}\}\Rightarrow\tan\theta=k$; $k\neq0"
       r"\Rightarrow$ applies $\arctan k$. Notes: $\textbf{dependent on the previous M mark}$ Applies $\tan2\theta\equiv"
       r"\frac{2\tan\theta}{1-\tan^2\theta}$, forms and uses a correct method for solving a 3TQ to give "
       r"$\tan\theta=k$, $k\neq0$, and applies $\arctan k$",
       r"ALT: (b) Way 2 — A1 (AO 2.2a): $\{90^\circ<\theta<180^\circ, \tan\theta=-2-\sqrt{5}\Rightarrow\}$ " + Q12ANS],
      False, 36),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", ALG, "2.11", 4, LATEX["13a"],
      [r"B1 (AO 1.1a): States or uses $6=\pi r^2h+\frac{2}{3}\pi r^3$. Notes: See scheme",
       r"M1 (AO 3.1a): $\Rightarrow h=\frac{6}{\pi r^2}-\frac{2}{3}r$, $\pi h=\frac{6}{r^2}-\frac{2}{3}\pi r$, "
       r"$\pi rh=\frac{6}{r}-\frac{2}{3}\pi r^2$, $rh=\frac{6}{\pi r}-\frac{2}{3}r^2$; $A=\pi r^2+2\pi rh+2\pi r^2$ "
       r"$\{\Rightarrow A=3\pi r^2+2\pi rh\}$; $A=2\pi r^2+2\pi r\left(\frac{6}{\pi r^2}-\frac{2}{3}r\right)+\pi r^2$. "
       r"Notes: Complete process of substituting their $h=\ldots$ or $\pi h=\ldots$ or $\pi rh=\ldots$ or "
       r"$rh=\ldots$, where ‘$\ldots$’ $=\mathrm{f}(r)$ into an expression for the surface area which is of the form "
       r"$A=\lambda\pi r^2+\mu\pi rh$; $\lambda, \mu\neq0$",
       r"A1 (AO 1.1b): $A=2\pi r^2+2\pi r\left(\frac{6}{\pi r^2}-\frac{2}{3}r\right)+\pi r^2$. Notes: Obtains correct "
       r"simplified or un-simplified $\{A=\}$ $2\pi r^2+2\pi r\left(\frac{6}{\pi r^2}-\frac{2}{3}r\right)+\pi r^2$ "
       r"Note: Condone the lack of $A=\ldots$ or $S=\ldots$ for any one of the A marks or for both of the A marks",
       r"A1* (AO 2.1): $A=3\pi r^2+\frac{12}{r}-\frac{4}{3}\pi r^2\Rightarrow A=\frac{12}{r}+\frac{5}{3}\pi r^2$ *. "
       r"Notes: Proceeds, using rigorous and careful reasoning, to $A=\frac{12}{r}+\frac{5}{3}\pi r^2$"],
      True, 40),
    e("13b", "13(b)", DIFF, "7.3, 7.2", 4, LATEX["13b"],
      [r"M1 (AO 3.4): $\left\{A=12r^{-1}+\frac{5}{3}\pi r^2\Rightarrow\right\}\frac{\mathrm{d}A}{\mathrm{d}r}="
       r"-12r^{-2}+\frac{10}{3}\pi r$. Notes: Uses the model (or their model) and differentiates $\frac{\lambda}{r}+"
       r"\mu r^2$ to give $\alpha r^{-2}+\beta r$; $\lambda, \mu, \alpha, \beta\neq0$",
       r"A1 (AO 1.1b): $\frac{\mathrm{d}A}{\mathrm{d}r}=-12r^{-2}+\frac{10}{3}\pi r$. Notes: $\left\{\frac{\mathrm{d}A}"
       r"{\mathrm{d}r}=\right\}-12r^{-2}+\frac{10}{3}\pi r$ o.e.",
       r"M1 (AO 2.1): $\left\{\frac{\mathrm{d}A}{\mathrm{d}r}=0\Rightarrow\right\}-\frac{12}{r^2}+\frac{10}{3}\pi r=0"
       r"\Rightarrow-36+10\pi r^3=0\Rightarrow r^{\pm3}=\ldots$ $\left\{=\frac{18}{5\pi}\right\}$. Notes: Sets their "
       r"$\frac{\mathrm{d}A}{\mathrm{d}r}=0$ and rearranges to give $r^{\pm3}=k$, $k\neq0$ ($\textbf{Note:}$ $k$ can be "
       r"positive or negative) Note: This mark can be implied. Give M1 (and A1) for $-36+10\pi r^3=0\to r=\left("
       r"\frac{18}{5\pi}\right)^{\frac{1}{3}}$ or $r=\left(\frac{36}{10\pi}\right)^{\frac{1}{3}}$ or $r=\left("
       r"\frac{3.6}{\pi}\right)^{\frac{1}{3}}$",
       r"A1 (AO 1.1b): $r=1.046447736\ldots\Rightarrow r=1.05$ (m) (3 sf) or awrt 1.05 (m) Note: Give final A1 for "
       r"correct exact values for $r$. Notes: $r=$ awrt 1.05 (ignoring units) or $r=$ awrt 105 cm Note: Give M0 A0 M0 "
       r"A0 where $r=1.05$ (m) (3 sf) or awrt 1.05 (m) is found from no working. Note: Give final A1 for correct exact "
       r"values for $r$. E.g. $r=\left(\frac{18}{5\pi}\right)^{\frac{1}{3}}$ or $r=\left(\frac{36}{10\pi}\right)^{"
       r"\frac{1}{3}}$ or $r=\left(\frac{3.6}{\pi}\right)^{\frac{1}{3}}$ Note: Give final M0 A0 for $-\frac{12}{r^2}+"
       r"\frac{10}{3}\pi r>0\Rightarrow r>1.0464$ Note: Give final M1 A1 for $-\frac{12}{r^2}+\frac{10}{3}\pi r>0"
       r"\Rightarrow r>1.0464\ldots\Rightarrow r=1.0464\ldots$"],
      True, 40),
    e("13c", "13(c)", DIFF, "7.3", 2, LATEX["13c"],
      [r"M1 (AO 3.4): $A_{\min}=\frac{12}{(1.046\ldots)}+\frac{5}{3}\pi(1.046\ldots)^2$. Notes: Substitutes their "
       r"$r=1.046\ldots$, found from solving $\frac{\mathrm{d}A}{\mathrm{d}r}=0$ in part (b), into the model with "
       r"equation $A=\frac{12}{r}+\frac{5}{3}\pi r^2$ Note: Give M0 for substituting their $r$ which has been found from "
       r"solving $\frac{\mathrm{d}^2A}{\mathrm{d}r^2}=0$ or from using $\frac{\mathrm{d}^2A}{\mathrm{d}r^2}$ into the "
       r"model with equation $A=\frac{12}{r}+\frac{5}{3}\pi r^2$",
       r"A1ft (AO 1.1b): $\{A_{\min}=17.20\ldots\Rightarrow\}$ $A=17\ (\text{m}^2)$ or $A=\text{awrt }17\ "
       r"(\text{m}^2)$. Notes: $\{A=\}17$ or $\{A=\}$ awrt 17 (ignoring units) Note: You can only follow through on "
       r"values of $r$ for $0.6\leqslant\text{their }r\leqslant1.3$ (and where their $r$ has been found from solving "
       r"$\frac{\mathrm{d}A}{\mathrm{d}r}=0$ in part (b)) [table of $r$; $A$; $A$ (nearest integer): 0.6; 21.88495…; "
       r"awrt 22 | 0.7; 19.70849…; awrt 20 | 0.8; 18.35103…; awrt 18 | 0.9; 17.57448…; awrt 18 | 1.0; 17.23598…; awrt "
       r"17 | 1.1; 17.24463…; awrt 17 | 1.2; 17.53982…; awrt 18 | 1.3; 18.07958…; awrt 18 | 1.05; 17.20124…; awrt 17 | "
       r"1.04644…; 17.20105…; awrt 17] Note: Give M1 A1 for $A=17\ (\text{m}^2)$ or $A=\text{awrt }17\ (\text{m}^2)$ "
       r"from no working"],
      True, 40),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", INT, "8.5", 6, LATEX["14a"],
      [r"B1 (AO 1.1b): $\{u=4-\sqrt{h}\Rightarrow\}\frac{\mathrm{d}u}{\mathrm{d}h}=-\frac{1}{2}h^{-\frac{1}{2}}$ or "
       r"$\frac{\mathrm{d}h}{\mathrm{d}u}=-2(4-u)$ or $\frac{\mathrm{d}h}{\mathrm{d}u}=-2\sqrt{h}$. Notes: See scheme. "
       r"Allow $\mathrm{d}u=-\frac{1}{2}h^{-\frac{1}{2}}\mathrm{d}h$, $\mathrm{d}h=-2(4-u)\mathrm{d}u$, "
       r"$\mathrm{d}h=-2\sqrt{h}\,\mathrm{d}u$ o.e.",
       r"M1 (AO 2.1): $\left\{\int\frac{\mathrm{d}h}{4-\sqrt{h}}=\right\}\int\frac{-2(4-u)}{u}\,\mathrm{d}u$. Notes: "
       r"Complete method for applying $u=4-\sqrt{h}$ to $\int\frac{\mathrm{d}h}{4-\sqrt{h}}$ to give an expression of "
       r"the form $\int\frac{k(4-u)}{u}\,\mathrm{d}u$; $k\neq0$ Note: Condone the omission of an integral sign and/or "
       r"$\mathrm{d}u$",
       r"M1 (AO 1.1b): $=\int\left(-\frac{8}{u}+2\right)\mathrm{d}u$. Notes: Proceeds to obtain an integral of the form "
       r"$\int\left(\frac{A}{u}+B\right)\{\mathrm{d}u\}$; $A, B\neq0$",
       r"M1 (AO 1.1b): $=-8\ln u+2u\ \{+c\}$. Notes: $\int\left(\frac{A}{u}+B\right)\{\mathrm{d}u\}\to D\ln u+Eu$; "
       r"$A, B, D, E\neq0$; with or without a constant of integration",
       r"A1 (AO 1.1b): $=-8\ln u+2u\ \{+c\}$. Notes: $\int\left(-\frac{8}{u}+2\right)\{\mathrm{d}u\}\to-8\ln u+2u$; "
       r"with or without a constant of integration",
       r"A1* (AO 2.1): $=-8\ln" + H + r"+2(4-\sqrt{h})+c=-8\ln" + H + r"-2\sqrt{h}+k$ *. Notes: $\textbf{dependent on "
       r"all previous marks}$ Substitutes $u=4-\sqrt{h}$ into their integrated result and completes the proof by "
       r"obtaining the printed result $-8\ln" + H + r"-2\sqrt{h}+k$. Condone the use of brackets instead of the modulus "
       r"sign. Note: They must combine 2(4) and their $+c$ correctly to give $+k$ Note: Going from $-8\ln" + H
       + r"+2(4-\sqrt{h})+c$ to $-8\ln" + H + r"-2\sqrt{h}+k$, with no intermediate working or with no incorrect working "
       r"is required for the final A1* mark. Note: Allow A1* for correctly reaching $-8\ln" + H + r"-2\sqrt{h}+c+8$ and "
       r"stating $k=c+8$ Note: Allow A1* for correctly reaching $-8\ln" + H + r"+2(4-\sqrt{h})+k=-8\ln" + H
       + r"-2\sqrt{h}+k$",
       r"ALT: (a) Alternative (integration by parts) method for the 2nd M, 3rd M and 1st A mark — 2nd M1: "
       r"$\left\{\int\frac{-2(4-u)}{u}\,\mathrm{d}u=\int\frac{2u-8}{u}\,\mathrm{d}u\right\}=(2u-8)\ln u-\int2\ln u\,"
       r"\mathrm{d}u=(2u-8)\ln u-2(u\ln u-u)\ \{+c\}$. Notes: Proceeds to obtain an integral of the form "
       r"$(Au+B)\ln u-\int A\ln u\,\{\mathrm{d}u\}$; $A, B\neq0$",
       r"ALT: (a) Alternative (integration by parts) method for the 2nd M, 3rd M and 1st A mark — 3rd M1: Integrates "
       r"to give $D\ln u+Eu$; $D, E\neq0$; which can be simplified or un-simplified with or without a constant of "
       r"integration. Note: Give 3rd M1 for $(2u-8)\ln u-2(u\ln u-u)$ because it is an un-simplified form of "
       r"$D\ln u+Eu$",
       r"ALT: (a) Alternative (integration by parts) method for the 2nd M, 3rd M and 1st A mark — 1st A1: Integrates "
       r"to give $(2u-8)\ln u-2(u\ln u-u)$ or $-8\ln u+2u$ o.e. with or without a constant of integration."],
      False, 44),
    e("14b", "14(b)", INT, "8.8", 2, LATEX["14b"],
      [r"M1 (AO 3.4): $\left\{\frac{\mathrm{d}h}{\mathrm{d}t}=\frac{t^{0.25}(4-\sqrt{h})}{20}=0\Rightarrow\right\}$ "
       r"$4-\sqrt{h}=0$. Notes: Uses the context of the model and has an understanding that the tree keeps growing "
       r"until $\frac{\mathrm{d}h}{\mathrm{d}t}=0\Rightarrow4-\sqrt{h}=0$. Alternatively, they can write "
       r"$\frac{\mathrm{d}h}{\mathrm{d}t}>0\Rightarrow4-\sqrt{h}>0$ Note: Accept $h=16$ or 16 used in their inequality "
       r"statement for this mark.",
       r"A1 (AO 2.2a): Deduces any of $0<h<16$, $0\leqslant h<16$, $0<h\leqslant16$, $0\leqslant h\leqslant16$, "
       r"$h<16$, $h\leqslant16$ or all values up to 16. Notes: See scheme Note: A correct answer can be given M1 A1 from "
       r"any working."],
      False, 44),
    e("14c", "14(c)", INT, "8.7, 8.8, 8.5", 7, LATEX["14c"],
      [r"B1 (AO 1.1b): $\int\frac{1}{(4-\sqrt{h})}\,\mathrm{d}h=\int\frac{1}{20}t^{0.25}\,\mathrm{d}t$. Notes: Way 1: "
       r"Separates the variables correctly. $\mathrm{d}h$ and $\mathrm{d}t$ should not be in the wrong positions, "
       r"although this mark can be implied by later working. Condone absence of integral signs.",
       r"M1 (AO 1.1b): $-8\ln" + H + r"-2\sqrt{h}=\frac{1}{25}t^{1.25}\ \{+c\}$. Notes: Integrates $t^{0.25}$ to give "
       r"$\lambda t^{1.25}$; $\lambda\neq0$",
       r"A1 (AO 1.1b): $-8\ln" + H + r"-2\sqrt{h}=\frac{1}{25}t^{1.25}\ \{+c\}$. Notes: Correct integration. E.g. "
       r"$-8\ln" + H + r"-2\sqrt{h}=\frac{1}{25}t^{1.25}$ or $20\left(-8\ln" + H + r"-2\sqrt{h}\right)=\frac{4}{5}"
       r"t^{1.25}$ $-8\ln" + H + r"+2(4-\sqrt{h})=\frac{1}{25}t^{1.25}$ or $20\left(-8\ln" + H + r"+2(4-\sqrt{h})\right)"
       r"=\frac{4}{5}t^{1.25}$ with or without a constant of integration, e.g. $k$, $c$ or $A$ Note: There is no "
       r"requirement for modulus signs.",
       r"M1 (AO 3.4): $\{t=0, h=1\Rightarrow\}-8\ln(4-1)-2\sqrt{(1)}=\frac{1}{25}(0)^{1.25}+c$. Notes: Some evidence "
       r"of $\textbf{applying}$ both $t=0$ and $h=1$ to their model (which can be a changed equation) which contains a "
       r"constant of integration, e.g. $k$, $c$ or $A$",
       r"dM1 (AO 3.1a): $\Rightarrow c=-8\ln(3)-2\Rightarrow-8\ln" + H + r"-2\sqrt{h}=\frac{1}{25}t^{1.25}-8\ln(3)-2$; "
       r"$\{h=12\Rightarrow\}-8\ln\left|4-\sqrt{12}\right|-2\sqrt{12}=\frac{1}{25}t^{1.25}-8\ln(3)-2$. Notes: "
       r"$\textbf{dependent on the previous M mark}$ Complete process of finding their constant of integration, "
       r"followed by applying $h=12$ and their constant of integration to their changed equation",
       r"M1 (AO 1.1b): $t^{1.25}=221.2795202\ldots\Rightarrow t=\sqrt[1.25]{221.2795\ldots}$ or $t=(221.2795\ldots)"
       r"^{0.8}$. Notes: Rearranges their equation to make $t^{\text{their }1.25}=\ldots$ followed by a correct method "
       r"to give $t=\ldots$; $t>0$ Note: $t^{\text{their }1.25}=\ldots$ can be negative, but their ‘$t=\ldots$’ must be "
       r"positive Note: “their 1.25” cannot be 0 or 1 for this mark Note: Do not give this mark if "
       r"$t^{\text{their }1.25}=\ldots$ (usually $t^{0.25}=\ldots$) is a result of substituting $t=12$ (or $t=11$) into "
       r"the given $\frac{\mathrm{d}h}{\mathrm{d}t}=\frac{t^{0.25}(4-\sqrt{h})}{20}$. $\textbf{Note:}$ They will "
       r"usually write $\frac{\mathrm{d}h}{\mathrm{d}t}$ as either 12 or 11.",
       r"A1 (AO 1.1b): $t=75.154\ldots\Rightarrow t=75.2$ (years) (3 sf) or awrt 75.2 (years) Note: You can recover "
       r"work for part (c) in part (b). Notes: awrt 75.2",
       r"ALT: (c) Way 2 — B1 (AO 1.1b): $\int_1^{12}\frac{20}{(4-\sqrt{h})}\,\mathrm{d}h=\int_0^Tt^{0.25}\,"
       r"\mathrm{d}t$. Notes: Separates the variables correctly. $\mathrm{d}h$ and $\mathrm{d}t$ should not be in the "
       r"wrong positions, although this mark can be implied by later working. Note: Integral signs and limits are not "
       r"required for this mark.",
       r"ALT: (c) Way 2 — M1 (AO 1.1b): $\left[20\left(-8\ln" + H + r"-2\sqrt{h}\right)\right]_1^{12}=\left[\frac{4}{5}"
       r"t^{1.25}\right]_0^T$. Notes: Same as Way 1 (ignore limits)",
       r"ALT: (c) Way 2 — A1 (AO 1.1b): $\left[20\left(-8\ln" + H + r"-2\sqrt{h}\right)\right]_1^{12}=\left[\frac{4}{5}"
       r"t^{1.25}\right]_0^T$. Notes: Same as Way 1 (ignore limits)",
       r"ALT: (c) Way 2 — M1 (AO 3.4): $20\left(-8\ln(4-\sqrt{12})-2\sqrt{12}\right)-20\left(-8\ln(4-1)-2\sqrt{1}"
       r"\right)=\frac{4}{5}T^{1.25}-0$. Notes: Applies limits of 1 and 12 to their model (i.e. to their changed "
       r"expression in $h$) and subtracts",
       r"ALT: (c) Way 2 — dM1 (AO 3.1a): $20\left(-8\ln(4-\sqrt{12})-2\sqrt{12}\right)-20\left(-8\ln(4-1)-2\sqrt{1}"
       r"\right)=\frac{4}{5}T^{1.25}-0$. Notes: $\textbf{dependent on the previous M mark}$ Complete process of "
       r"applying limits of 1 and 12 and 0 and $T$ (or ‘$t$’) appropriately to their changed equation",
       r"ALT: (c) Way 2 — M1 (AO 1.1b): $T^{1.25}=221.2795202\ldots\Rightarrow T=\sqrt[1.25]{221.2795\ldots}$ or "
       r"$T=(221.2795\ldots)^{0.8}$. Notes: Same as Way 1",
       r"ALT: (c) Way 2 — A1 (AO 1.1b): $T=75.154\ldots\Rightarrow T=75.2$ (years) (3 sf) or awrt 75.2 (years) Note: "
       r"You can recover work for part (c) in part (b). Notes: Same as Way 1"],
      False, 44),
]

W = None
NO = {"ref": False}
BACK = {"ref": True}
LIM = r"\lim_{\delta x\to0}\sum_{x=4}^{9}\sqrt{x}\,\delta x"
INT49 = r"\int_4^9\sqrt{x}\,\mathrm{d}x"
REPORT = {
    "01": [
        (W, "Q01 proved challenging for a significant number of candidates."),
        (W, r"This was probably because of the more open-ended nature of the question, allowing candidates to select "
            r"their own problem-solving strategy to express $y$ as a function of $x$.", BACK),
        (W, r"It was not apparent to most candidates that $y$ could be expressed as a linear function of $x$.", NO),
        (W, "More able candidates, however, were able to provide a concise solution."),
        (W, r"Other candidates were still able to achieve full marks but expressed $y$ as a more complicated function "
            r"of $x$."),
        (W, r"A few candidates attempted to express $x$ as a function of $y$, suggesting a lack of understanding of "
            r"the terminology."),
        (W, "It appeared that most candidates failed to realise that Q01 could be solved purely using indices.", NO),
        (W, "Instead, most candidates chose to immediately take logarithms as their first step towards a solution."),
        (W, r"A correct first step, e.g. $\log(2^x\times4^y)=\log\left(\frac{1}{2\sqrt{2}}\right)$, was rewarded by "
            r"the mark scheme."),
        (W, "Unfortunately, some candidates combined taking logarithms with an incorrect application of the addition "
            "law for logarithms as their first step, therefore gaining no marks."),
        (W, r"E.g. $2^x\times4^y\to\log2^x\times\log4^y$."),
        (W, "Most candidates who had a correct first step of work went on to achieve full marks, with some only "
            "failing to do so by making an arithmetic error."),
        (W, "Q01 highlighted some candidates’ weaker algebraic, indices and logarithms skills."),
        (W, r"Common errors included $2^x\times4^y\to8^{xy}$, $2^x\times4^y\to8^{x+y}$, $\frac{1}{2^x2\sqrt{2}}\to"
            r"\frac{1}{4^x\sqrt{2}}$, or $2^x\times4^y=\frac{1}{2\sqrt{2}}\to4^y=\frac{2^x}{2\sqrt{2}}$."),
        (W, r"The most common correct answers were $y=\frac{\log\left(\frac{1}{2\sqrt{2}}\right)-\log(2^x)}{\log4}$, "
            r"$y=\log_4\left(\frac{1}{2^x2\sqrt{2}}\right)$ or $y=\frac{\ln\left(\frac{1}{2^x2\sqrt{2}}\right)}"
            r"{\ln4}$."),
        (W, r"Only a minority of candidates obtained a correct $y=-\frac{1}{2}x-\frac{3}{4}$."),
    ],
    "02": [
        (W, "Q02 proved to be challenging, with a significant number of candidates struggling to realise that the "
            "length of the runway could be estimated by the area under the speed-time curve generated from the table "
            "of values given in the question."),
        ({"a"}, "In Q02(a), only a minority of candidates estimated the length of the runway by applying the "
                "trapezium rule, which was considered the most appropriate method, with many of these giving the "
                "correct answer of 415 m.", NO),
        ({"a"}, r"While the table of values clearly shows an interval width $h=5$, the application of the formula "
                r"$h=\frac{b-a}{n}$ with $n=6$ instead of $n=5$ led some candidates to use an incorrect strip width "
                r"$h=\frac{25}{6}$."),
        ({"a"}, "Other candidates made calculation errors, bracketing errors or transcription errors."),
        ({"a"}, r"Some candidates used the equations of motion with constant acceleration (i.e. the $\textit{suvat}$ "
                r"equations) to estimate the length."),
        ({"a"}, r"Many of the candidates who used this method applied the calculation $\left(\frac{2+42}{2}\right)"
                r"(25)$ to obtain an estimate of 550 m."),
        ({"a"}, r"A few used $v=u+at$ to find the acceleration, followed by $s=ut+\frac{1}{2}at^2$ to estimate the "
                r"length."),
        ({"a"}, r"Some candidates used $u=0$ in their $\textit{suvat}$ calculations, in contradiction to the table of "
                r"values which indicated an initial speed of $2\text{ m s}^{-1}$."),
        ({"a"}, r"A few candidates used a method which was equivalent to the trapezium rule, of applying "
                r"$\textit{suvat}$ to each of the 5 time-intervals, to give the correct answer of 415 m."),
        ({"a"}, r"Other methods seen included: summing up the area of rectangles which enclosed the area above the "
                r"curve for each of the 5 time intervals; summing up areas of rectangles which enclosed the area below "
                r"the curve for each of the 5 time intervals; and applying (average speed)$\times$(total time)."),
        ({"a"}, r"The most common methods which were deemed incorrect included $25\times42=1050$; "
                r"$\frac{1}{2}(25)(42)=525$; $\sum(\text{speed})(\text{time})=(0)(2)+(5)(5)+(10)(10)+\ldots+(25)(42)="
                r"2005$; or a 6 rectangle approach (instead of 5 rectangles)."),
        ({"b"}, r"As for Q02(b), while many candidates who used a trapezium rule or $\textit{suvat}$ method in Q02(a) "
                r"identified their estimate of the length as an overestimate, some found difficulty in articulating a "
                r"reason for this.", NO),
        ({"b"}, "Those who were most successful drew a diagram which showed clearly the extra area generated by the "
                "trapezium rule in relation to the curve.", NO),
        ({"b"}, "Some candidates sketched the speed-time curve and explained that the curve was convex or that the "
                "acceleration was continually increasing."),
        ({"b"}, "Only a few candidates who used a rectangle method were able to give a correct reason."),
        ({"b"}, "Some candidates answered Q02(b) by finding an alternative estimate and comparing it with their "
                "estimate in Q02(a).", NO),
        ({"b"}, "For example, some found 415 in Q02(a) and 550 in Q02(b), and then concluded that ‘415 must be an "
                "underestimate’."),
        ({"b"}, "Other candidates, who also received no credit, gave physical explanations about friction, air "
                "resistance or the shape of the aircraft, while others stated that ‘the jet accelerated smoothly’."),
    ],
    "03": [
        (W, "Q03 proved to be the most accessible question on this paper with many candidates obtaining full marks."),
        ({"a"}, r"In Q03(a), many candidates explained that the angle $40^\circ$ should have been converted to its "
                r"equivalent in radians in order for it to be applied to the formula $\frac{1}{2}r^2\theta$.", NO),
        ({"a"}, "Some candidates’ explanations lacked sufficient detail, e.g. they stated ‘the angle is in degrees’ "
                "but failed to mention that the angle used in the formula should have been expressed in radians."),
        ({"a", "b"}, r"A few candidates did not give a reason in Q03(a), but correctly calculated the area of sector "
                     r"$AOB$ in Q3(b)."),
        ({"b"}, "Q03(b) was also well-answered."),
        ({"b"}, r"Most candidates converted $40^\circ$ to radians and applied a correct $\frac{2\pi}{9}$ to the given "
                r"formula $\frac{1}{2}r^2\theta$."),
        ({"b"}, r"Some candidates applied a correct formula $\pi r^2\left(\frac{\theta}{360}\right)$ with "
                r"$\theta=40^\circ$."),
        ({"b"}, r"Errors included converting $40^\circ$ to either $\frac{40\pi}{360}$ or $\frac{9\pi}{2}$; applying "
                r"$\frac{1}{2}(5^2)\left(\frac{2}{9}\right)$; and applying incorrect formulae such as "
                r"$\frac{1}{2}r^2\sin\theta$ or $\frac{1}{2}\pi r^2\theta$.", NO),
        ({"b"}, r"Most candidates gave the correct answer in exact form as $\frac{25}{9}\pi$, and some gave an answer "
                r"8.73 which was rounded to 3 significant figures, while others gave both exact and rounded answers."),
        ({"b"}, r"Most candidates gave the units $\text{cm}^2$ in their answer to Q03(b)."),
        ({"b"}, "On this occasion, a lack of units in their final answer was condoned.", NO),
    ],
    "04": [
        (W, "Q04 was well attempted by both medium ability and higher ability candidates."),
        (W, "Lower ability candidates struggled to make progress, with most of them scoring no more than one mark."),
        (W, "There were two common methods that were used by candidates."),
        (W, r"The first method, covered by Way 1 in the mark scheme, was the substitution of the parametric equations "
            r"of $C_1$ into the Cartesian equation of $C_2$ to give an equation in $t$ only; the trigonometric "
            r"identity $\sin^2t+\cos^2t\equiv1$ being used to obtain an equation in $\sin^2t$ (or $\cos^2t$) only, "
            r"and a value for $\sin t$ (or $\cos t$) found."),
        (W, r"The second method, covered by Way 2 in the mark scheme, was the application of the trigonometric "
            r"identity $\sin^2t+\cos^2t\equiv1$ to the parametric equations of $C_1$ to give $\left(\frac{x}{10}"
            r"\right)^2+\left(\frac{y}{4\sqrt{2}}\right)^2=1$, the Cartesian equation of $C_2$ being used to obtain "
            r"an equation in $x^2$ (or $y^2$) only, and a value for $x$ (or $y$) found."),
        (W, r"A few candidates used a correct method of progressing from $(10\cos t)^2+(4\sqrt{2}\sin t)^2=66$ to "
            r"either $\tan^2t=1$ or $\cos2t=0$."),
        (W, r"In all these methods, substituting back yielded their coordinates for $S$, with most candidates "
            r"realising that $x_S>0$ and $y_S<0$."),
        (W, r"Some candidates incorrectly stated $S$ as $(5\sqrt{2}, 4)$."),
        (W, r"In the first method, successful candidates used either $t=\frac{7\pi}{4}$ or $t=\frac{\pi}{4}$, and "
            r"then applied symmetry to find the correct coordinates for $S$ as either $(5\sqrt{2}, -4)$ or "
            r"$(7.07, -4)$."),
        (W, "An area of concern centred around arithmetical slips or errors in elementary algebra."),
        (W, r"Examples of the former included $(4\sqrt{2})^2$ becoming 8 or 64; $\sin^2t=\frac{1}{2}$ becoming "
            r"$\sin t=\frac{1}{4}$; and $\frac{x^2}{100}+\frac{y^2}{32}=1$ becoming $32x^2+100y^2=1$ or 100 or 32."),
        (W, r"Examples of the latter included the invalid methods of $y^2=66-x^2$ becoming $y=\sqrt{66}-x$ and "
            r"$\sin^2t=1-\frac{x^2}{100}$ becoming $\sin t=1-\frac{x}{10}$."),
        (W, r"Candidates who made no creditable progress included those who differentiated the parametric equations "
            r"for $C_1$, and those who obtained, e.g. $y=4\sqrt{2}\sin\left(\arccos\left(\frac{x}{10}\right)\right)$ "
            r"leading to $x^2+32\sin^2\left(\arccos\left(\frac{x}{10}\right)\right)=66$.", NO),
    ],
    "05": [
        (W, "Q05 proved challenging for many candidates and some candidates were unfamiliar with the notation that "
            "was used."),
        (W, "Most candidates scored either all three marks or zero marks in this question."),
        (W, "There were a substantial number of blank responses."),
        (W, r"It is noted that section 8.4 (guidance) of the Pure Specification states ‘Recognise $\int_a^b"
            r"\mathrm{f}(x)\,\mathrm{d}x=\lim_{\delta x\to0}\sum_{x=a}^{b}\mathrm{f}(x)\,\delta x$’.", NO),
        (W, "It is also noted that a similar question had not appeared on the 9MA0 June 2018 papers, the SAMs, the "
            "specimen papers or the mock papers.", NO),
        (W, r"Those candidates who recognised that $" + LIM + r"$ was another way of writing $" + INT49 + r"$ "
            r"generally produced a correct solution to score all 3 marks.", NO),
        (W, r"Only a few made errors in their integration of $\sqrt{x}$ or in the application of the limits 4 and 1.",
         {"note": r"the limits are 4 and 9: the question’s sum runs from $x=4$ to $x=9$ and the mark scheme uses "
                  r"$" + INT49 + "$"}),
        (W, "Most candidates, however, made no creditable progress."),
        (W, r"Some applied the trapezium rule with $h=1$, but did not link their trapezium rule attempt with a stated "
            r"$" + INT49 + "$."),
        (W, r"Other candidates attempted to sum $\sqrt{x}$ using integer values from $x=4$ to $x=9$, resulting in "
            r"$\sqrt{4}+\sqrt{5}+\sqrt{6}+\ldots+\sqrt{9}\ (=15.1597\ldots)$."),
        (W, r"Some candidates mistakenly interpreted ‘$\delta x$’ as a trigger to differentiate $\sqrt{x}$, with a "
            r"few of these candidates attempting to differentiate $\sqrt{x}$ from first principles.", NO),
        (W, r"A few candidates applied the incorrect method $\left(\sqrt{4}+\sqrt{5}+\sqrt{6}+\ldots+\sqrt{9}\right)-"
            + INT49 + r"$ to give an answer of 2.49 to 3 significant figures."),
    ],
    "06": [
        (W, "Q06 discriminated well between candidates of all abilities, with only a few candidates gaining full "
            "marks."),
        ({"b", "d"}, "There were some marks in Q06(b) and Q06(d) which were accessible to the majority of "
                     "candidates."),
        ({"a"}, r"In Q06(a), many candidates struggled with the split domain for $\mathrm{g}(x)$ (i.e. for "
                r"$x\leqslant2$, $\mathrm{g}(x)=(x-2)^2+1$ and for $x>2$, $\mathrm{g}(x)=4x-7$) and only a minority "
                r"gained both marks."),
        ({"a"}, r"Many candidates found a correct $\mathrm{g}(0)=5$, but a significant number used the incorrect "
                r"method of substituting ‘5’ to give $\mathrm{gg}(0)=(5-2)^2+1=10$."),
        ({"a"}, r"Only a minority used a correct method and found $\mathrm{gg}(0)=4(5)-3=13$.",
         {"note": r"the mark scheme has $\mathrm{gg}(0)=\mathrm{g}(5)=4(5)-7=13$"}),
        ({"a"}, r"Occasionally candidates found an algebraic expression for $\mathrm{gg}(x)$, although this was often "
                r"incorrect.", NO),
        ({"a"}, r"Very few obtained a correct answer of 13 by substituting $x=0$ into $4((x-2)^2+1)-7$ or "
                r"$4(x-2)^2-3$."),
        ({"b"}, r"In Q06(b), many candidates attempted to solve the inequality $\mathrm{g}(x)>28$ by finding the "
                r"critical values for $x$."),
        ({"b"}, r"Most solved the linear equation to find a correct critical value $x=\frac{35}{4}$, and many solved "
                r"the quadratic equation to find $x=2\pm3\sqrt{3}$."),
        ({"b"}, r"A minority rejected $x=2-3\sqrt{3}$ and deduced that $x=2-3\sqrt{3}$ was the second critical value.",
         {"note": r"the root to reject is $x=2+3\sqrt{3}$, since $(x-2)^2+1$ applies only for $x\leqslant2$; the mark "
                  r"scheme’s critical value is $x=2-3\sqrt{3}$"}),
        ({"b"}, r"Only a few candidates used the critical values and the diagram in Q6 to write down the correct "
                r"solution $x<2-3\sqrt{3}\cup x>\frac{35}{4}$."),
        ({"b"}, r"Some candidates, however, incorrectly gave $x=\frac{35}{4}$, $x=2\pm3\sqrt{3}$ or gave "
                r"$x<2+3\sqrt{3}\cup x>\frac{35}{4}$ as their final answer."),
        ({"b"}, r"A few candidates made no creditable progress in Q06(b) by using a method of equating both parts of "
                r"$\mathrm{g}(x)$ and attempting to solve the equation $(x-2)^2+1=4x-7$."),
        ({"c"}, "Although Q6(c) required a comment for both functions, f and g, some candidates only wrote a comment "
                "about one of the two functions.",
         {"note": "the two functions in Q6(c) are h and g"}),
        ({"c"}, "A significant number of candidates believed that g did not have an inverse due to its being defined "
                "in ‘two parts’."),
        ({"c"}, "Candidates who were successful in Q6(c) usually gave a reason such as, ‘g is a many-one function and "
                "h is a one-one function’.", NO),
        ({"c"}, "A few correctly stated that the inverse of g is one-many, which is not a function, whereas the "
                "inverse of h is one-one, which is a function."),
        ({"c"}, "A few candidates incorrectly described g as a ‘one-many function’."),
        ({"d"}, r"In Q06(d), only a few candidates applied the method of finding $x$ by applying "
                r"$\mathrm{h}\left(-\frac{1}{2}\right)$."),
        ({"d"}, "As this method was less prone to error, most candidates who used it scored full marks.", BACK),
        ({"d"}, r"Most candidates applied a complete method of finding their inverse $\mathrm{h}^{-1}(x)$, followed by "
                r"using their inverse to form and solve the equation $\mathrm{h}^{-1}(x)=-\frac{1}{2}$."),
        ({"d"}, r"Many candidates who found a correct answer $x=7.25$ lost the final mark in Q06(d)."),
        ({"d"}, r"This was because they used the incorrect inverse $\mathrm{h}^{-1}(x)=2+\sqrt{x-1}$ (instead of the "
                r"correct $\mathrm{h}^{-1}(x)=2-\sqrt{x-1}$) which led to their ‘solving’ the incorrect "
                r"$\sqrt{x-1}=-\frac{1}{2}$ (which has no solutions) to give $x=7.25$.", BACK),
        ({"d"}, r"A few candidates in Q06(d) incorrectly believed that $\mathrm{h}^{-1}(x)$ referred to the reciprocal "
                r"of h, or even to the first derivative of h with respect to $x$."),
    ],
    "07": [
        (W, "Q07 discriminated well between the medium and higher ability candidates."),
        (W, "Lower ability candidates struggled to make much progress with this modelling question and most of them "
            "scored no more than one mark.", NO),
        ({"a"}, r"In Q07(a), most candidates wrote down a correct equation for the model in the form $y=kx+c$, with "
                r"constants $k$ and $c$."),
        ({"a"}, r"A minority struggled to give a suitable form of the linear equation, with some omitting the fixed "
                r"cost constant, $c$."),
        ({"a"}, r"Some candidates gave incorrect answers, such as $y\propto x$; equations involving exponential "
                r"models; or differential equations.", NO),
        ({"b"}, r"Q07(b) proved challenging for those candidates who struggled to grasp the concept "
                r"‘$\text{profit}=\text{sales}-\text{cost}$’, with many of them incorrectly assuming that the model "
                r"from Q07(a) was for the profit made.", NO),
        ({"b"}, r"Many of these candidates used $(800, 500)$ and either $(300, 80)$ or $(300, -80)$ to form two linear "
                r"equations, with some erroneously finding a gradient of 0.84.", BACK),
        ({"b"}, "Those candidates who understood the link between profit and cost usually found the total cost to the "
                "factory of £1100 and £680 for 800 and 300 bars of soap respectively.", NO),
        ({"b"}, r"Most used $(800, 1100)$ and $(300, 680)$ to form two linear equations and proceeded to find the "
                r"gradient, 0.84, and $y$-intercept, 428."),
        ({"b"}, r"A large proportion concluded by stating the given equation $y=0.84x+428$."),
        ({"b"}, "A few candidates, however, did not complete their analysis with a suitable conclusion, and so lost "
                "the final mark."),
        ({"b"}, r"Some candidates used $(800, 1100)$ and $(300, 680)$ to verify the model $y=0.84x+428$."),
        ({"b"}, "Many of these were successful but often failed to give a suitable conclusion stating that the given "
                "model was true.", BACK),
        ({"c"}, "Q07(c) gave a significant number of candidates their only creditable access to Q07."),
        ({"c"}, "Some candidates gave a correct interpretation such as 0.84 represented ‘the cost of making an extra "
                "bar of soap’.", NO),
        ({"c"}, "Incorrect explanations included that 0.84 represented ‘the selling price of a bar of soap’ or ‘the "
                "profit per bar of soap made’."),
        ({"d"}, "There was a mixed response to Q07(d)."),
        ({"d"}, r"The most popular approach was to form and solve a correct $2n=0.84n+428$ or $2n>0.84n+428$, which "
                r"mostly led to the correct answer $n=369$."),
        ({"d"}, r"A final answer left as an inequality such as $n>368$ or $n\geqslant369$, without reference to the "
                r"statement that 369 was the number of bars required, was not sufficient for the final mark.", NO),
        ({"d"}, r"Some candidates used trials of both $n=368$ and $n=369$ in a complete trial and error method "
                r"leading to a correct conclusion of $n=369$."),
    ],
    "08": [
        (W, "Q08 was found challenging by many candidates, with Q08(i) more successfully answered than Q08(ii)."),
        (W, "The most successful candidates were the ones who listed the first few terms of the series."),
        (W, r"In other words, those candidates that wrote $20\left(\frac{1}{2}\right)^4+20\left(\frac{1}{2}\right)^5+"
            r"20\left(\frac{1}{2}\right)^6+\ldots$ and $\log_5\left(\frac{3}{2}\right)+\log_5\left(\frac{4}{3}\right)"
            r"+\log_5\left(\frac{5}{4}\right)+\ldots$ gained a better understanding of the series that they were "
            r"required to sum.", BACK),
        (W, "There were, however, many attempts that made no creditable progress and a significant number of blank "
            "responses to either one or both parts of Q08."),
        ({"i"}, r"In Q08(i), many candidates identified that a sum to infinity was required in their solution and "
                r"attempted to apply the formula $\frac{a}{1-r}$."),
        ({"i"}, r"Most used $r=\frac{1}{2}$ in this formula, although some used incorrect values such as "
                r"$r=\frac{1}{4}$ or $r=-\frac{1}{2}$.", NO),
        ({"i"}, r"Disappointingly, a significant number of candidates used $r=4$ from the expression given in the "
                r"question and applied it to the formula $\frac{a}{1-r}$, even though the formula only works when "
                r"$-1<r<1$.", NO),
        ({"i"}, "There were a number of correct strategies that candidates could use."),
        ({"i"}, r"The most successful strategy was to apply $a=20\left(\frac{1}{2}\right)^4$, $r=\frac{1}{2}$ to "
                r"$\frac{a}{1-r}$, and many candidates who used this strategy achieved the correct answer of 2.5.", NO),
        ({"i"}, r"Other complete strategies included applying $\sum_{r=1}^{\infty}20\times\left(\frac{1}{2}\right)^r-"
                r"\sum_{r=1}^{3}20\times\left(\frac{1}{2}\right)^r$ or $\sum_{r=0}^{\infty}20\times\left(\frac{1}{2}"
                r"\right)^r-\sum_{r=0}^{3}20\times\left(\frac{1}{2}\right)^r$ which led to $(20-17.5)$ or "
                r"$(40-37.5)$ respectively."),
        ({"i"}, "Some candidates applied an incorrect overall strategy by subtracting an incorrect number of terms "
                "from their sum to infinity."),
        ({"i"}, r"These candidates gave incorrect answers such as $(20-18.75)$, $(40-38.75)$, $(40-35)$ or "
                r"$(40-17.5)$.", BACK),
        ({"i"}, "A few candidates obtained the correct answer of 2.5 by using their calculator."),
        ({"ii"}, "Only a few candidates produced a correct solution to Q08(ii)."),
        ({"ii"}, "There were two main correct methods that were used by candidates in equal measure."),
        ({"ii"}, r"One was to list the first few terms and the last few terms of the series and use the addition law "
                 r"of logarithms to achieve $\log_5\left(\frac{3}{2}\times\frac{4}{3}\times\ldots\times\frac{50}{49}"
                 r"\right)$."),
        ({"ii"}, r"Many candidates used cancelling to complete their proof correctly by writing "
                 r"$\log_5\left(\frac{50}{2}\right)=\log_5(25)=2$."),
        ({"ii"}, r"The other method was to use the subtraction law of logarithms to give $\sum_{n=1}^{48}"
                 r"(\log_5(n+2)-\log_5(n+1))$ and list terms to give $(\log_53+\log_54+\ldots\ldots+\log_550)-"
                 r"(\log_52+\log_53+\ldots\ldots+\log_549)$."),
        ({"ii"}, r"Again many candidates used cancelling and completed their proof by writing "
                 r"$\log_5(50)-\log_5(2)=\log_5(25)=2$."),
        ({"ii"}, r"A few candidates progressed by writing $\log_5(3\times4\times\ldots\ldots\times50)-\log_5(2\times3"
                 r"\times\ldots\ldots\times49)$ and used factorials to give $\log_5\left(\frac{50!}{2}\right)-"
                 r"\log_5(49!)=\log_5\left(\frac{50!}{2(49!)}\right)=\log_5(25)=2$."),
        ({"ii"}, r"Some candidates incorrectly assumed an arithmetic series and attempted to find its sum by using "
                 r"$\frac{n}{2}(a+l)$ or $\frac{n}{2}[2a+(n-1)d]$ with $n=48$, $a=\log_5\left(\frac{3}{2}\right)$, "
                 r"$l=\log_5\left(\frac{50}{49}\right)$ and $d=\log_5\left(\frac{4}{3}\right)-\log_5\left(\frac{3}{2}"
                 r"\right)$."),
        ({"ii"}, "A few candidates incorrectly assumed a geometric series and attempted to find its sum."),
        ({"ii"}, r"Some candidates, who made no creditable progress, resorted to listing their terms as decimals, or "
                 r"attempted to add all 48 terms as decimals by writing $0.2519\ldots+0.1787\ldots+0.1386\ldots+"
                 r"\ldots\ldots+0.0125\ldots=2$."),
    ],
    "09": [
        (W, "In general, Q09 discriminated well between candidates of all abilities."),
        ({"a", "b", "c"}, "Q09(b) and Q09(c) were more accessible to candidates than Q09(a)."),
        ({"a"}, "Some candidates left Q09(a) blank while others struggled to make any creditable progress."),
        ({"a"}, "In Q09(a), many candidates wrote down a valid log equation as part of their explanation."),
        ({"a"}, r"Those who used mathematical reasoning to progress from $\log_{10}d=\log_{10}k+n\log_{10}V$ to "
                r"$d=kV^n$ (or vice versa) usually showed an intermediate step in their working and so were successful "
                r"in their explanation.", NO),
        ({"a"}, r"A few candidates made errors in progressing between these two equations, such as an incorrect "
                r"method of combining logarithms (e.g. $\log_{10}d=n\log_{10}kV$), or an incorrect use of powers (e.g. "
                r"$d=10^c+V^n$).", BACK),
        ({"a"}, r"Those who made a direct comparison of their log equation with $y=mx+c$ usually did so clearly enough "
                r"but sometimes did not allude to $d=kV^n$ (if using $-1.77$ rather than $\log_{10}k$ in their log "
                r"equation).", NO),
        ({"a"}, r"A significant number of candidates did not apply $10^{-1.77}$ or use logarithms to show that "
                r"$k=0.017$."),
        ({"b"}, r"In Q09(b), the majority of candidates substituted $V=30$ and $d=20$ into $d=kV^n$ and applied "
                r"logarithms correctly, leading to the correct value of $n=2.08$."),
        ({"b"}, r"A few candidates used the incorrect method of simplifying $20=0.017(30)^n$ to give $20=(0.51)^n$."),
        ({"b"}, r"Some candidates substituted in $V$ and $d$ the wrong way around, usually leading to $n=2.50$, and a "
                r"few used both $V$ and $d$ as 20."),
        ({"b"}, r"A small minority substituted $V=30$ and $d=20$ into a correct log equation, while a few others "
                r"correctly found $n$ by finding the gradient between the known points $(0, -1.77)$ and "
                r"$(\log_{10}30, \log_{10}20)$."),
        ({"b"}, r"The most common mistake was not writing a complete equation $d=(0.017)V^{2.08}$ or "
                r"$\log_{10}d=-1.77+2.08\log_{10}V$ after finding a correct $n=2.08$."),
        ({"c"}, r"In Q09(c), most candidates applied $V=60$ to their exponential model and found the braking "
                r"distance."),
        ({"c"}, "Some then used the incorrect method of comparing this breaking distance with the overall stopping "
                "distance.", BACK),
        ({"c"}, r"The majority attempted to calculate the thinking distance and either added it to their breaking "
                r"distance $d$ or subtracted it from 100.", NO),
        ({"c"}, "The main error was due to the units."),
        ({"c"}, r"Some candidates did not attempt to convert $60\text{ km h}^{-1}$ to $\text{m s}^{-1}$ and simply "
                r"multiplied 60 by the thinking time of 0.8 seconds to obtain a thinking distance of 48 metres."),
        ({"c"}, r"Others only managed a partial conversion, with some using $\frac{1}{75}$ metres $\left(\text{instead "
                r"of }13.3\text{ m}\approx\frac{1}{75}\text{ km}\right)$ as their thinking distance."),
        ({"c"}, "In some of the answers, candidates used an incorrect method of combining their values to give a "
                "dimensionally incorrect quantity."),
        ({"c"}, "For example, they might add their breaking distance to either a speed or a time."),
        ({"c"}, "Candidates who obtained a thinking distance of 13.3 m usually reached a correct answer and "
                "conclusion."),
        ({"c"}, r"A few compared the maximum speed needed to stop at the puddle with the given 60, while even fewer "
                r"compared the maximum value of $n$ needed to stop at the puddle with $n=2.08$; and with correct "
                r"conclusions these were valid solutions.", NO),
    ],
    "10": [
        (W, "Q10 discriminated well between the medium and higher ability candidates, with lower ability candidates "
            "struggling to gain any creditable access."),
        (W, "Q10 increased in difficulty as the candidates progressed through the question, and only a small "
            "proportion of candidates scored full marks."),
        ({"a"}, r"In Q10(a), most candidates followed a correct method to achieve the correct answer $" + V("CM")
                + r"=-\frac{3}{2}" + A + r"+\frac{1}{2}" + B + "$."),
        ({"a"}, r"Of the candidates who identified a suitable route from $C$ to $M$, the most common approach was $"
                + V("CM") + "=" + V("CA") + "+" + V("AM") + "=" + V("CA") + r"+\frac{1}{2}" + V("AB") + "$."),
        ({"a"}, r"Less efficient routes such as $" + V("CM") + "=" + V("CO") + "+" + V("OB") + "+" + V("BM")
                + "$ or even $" + V("CM") + "=" + V("CO") + "+" + V("OA") + "+" + V("AM") + "$ were also observed.",
         NO),
        ({"a"}, r"Some candidates struggled to apply the vectors $" + A + "$ and $" + B + "$ to the routes they had "
                r"chosen."),
        ({"a"}, r"Incorrect methods included applying $" + V("CA") + "=" + A + "$ (instead of $" + V("CA") + "=-" + A
                + "$) or applying $" + V("AB") + "=" + A + "-" + B + "$ (instead of $" + V("AB") + "=" + B + "-" + A
                + "$)."),
        ({"a"}, r"There were a few candidates who incorrectly deduced the position of $C$ to be in the opposite "
                r"direction to $" + V("OA") + r"$ and they were mostly able to apply the approach, $" + V("CM") + "="
                + V("CO") + "+" + V("OA") + "+" + V("AM") + "=" + V("CO") + "+" + V("OA") + r"+\frac{1}{2}" + V("AB")
                + "$, to gain some credit."),
        ({"b"}, r"Q10(b) proved to be demanding, with some candidates struggling to understand what the question "
                r"required them to do, and many seemed to be confused by the introduction of the scalar multiple "
                r"$\lambda$."),
        ({"b"}, r"Only a minority deduced that $" + V("CN") + r"=\lambda" + V("CM") + r"$ and applied this deduction "
                r"to the route $" + V("ON") + "=" + V("OC") + "+" + V("CN") + "$.", NO),
        ({"b"}, r"Most of these candidates progressed well to the given answer unless they had found an incorrect $"
                + V("CM") + "$ in Q10(a).", BACK),
        ({"b"}, r"Many candidates used $" + V("ON") + "=" + V("OC") + "+" + V("CM") + "+" + V("MB") + "+" + V("BN")
                + "$ or $" + V("ON") + "=" + V("OA") + "+" + V("AB") + "+" + V("BN") + "$ and made no creditable "
                r"progress."),
        ({"b"}, r"These candidates usually produced solutions which led to the elimination of $\lambda$ from the $"
                + A + "$ component of the resulting vector for $" + V("ON") + "$.", BACK),
        ({"b"}, r"A few candidates used $" + V("ON") + "=" + V("OM") + "+" + V("MN") + r"$ and proceeded to obtain a "
                r"correct expression $" + V("ON") + r"=\frac{1}{2}" + A + r"+\frac{1}{2}" + B + r"+\mu\left(-\frac{3}"
                r"{2}" + A + r"+\frac{1}{2}" + B + r"\right)$ in terms $\mu$ (or $\lambda$), but only a few deduced "
                r"that this could lead to the stated solution by setting $\mu=\lambda-1$ (or $\lambda'=\lambda-1$).",
         NO),
        ({"c"}, "Q10(c) proved to be challenging with many candidates failing to make any creditable progress."),
        ({"c"}, r"The crucial step was to recognise that $" + V("ON") + "$ is parallel to $" + V("OB") + r"$ and "
                r"hence is a multiple of $" + B + "$ with no $" + A + "$ component."),
        ({"c"}, r"Only a few candidates set the $" + A + "$ component $" + V("ON") + r"$ to zero to give the equation "
                r"$2-\frac{3}{2}\lambda=0$."),
        ({"c"}, r"Almost all of these candidates found $\lambda=\frac{4}{3}$, with many finding $" + V("ON")
                + r"=\frac{2}{3}" + B + "$ and giving a correct explanation of the given ratio.", BACK),
    ],
    "11": [
        (W, "In general, Q11 discriminated well between candidates of all abilities."),
        ({"a"}, "Q11(a) was demanding with most candidates scoring no more than one mark."),
        ({"b", "c", "d"}, "Q11(b), Q11(c) and Q11(d) proved accessible to candidates of all abilities."),
        ({"a"}, r"In Q11(a), most candidates took logs, as advised by the question, and many obtained either "
                r"$\ln y=x\ln x$ or $\log y=x\log x$."),
        ({"a"}, "At this point a significant number of candidates made no further creditable progress.", BACK),
        ({"a"}, r"Some candidates used a complete method of applying the product rule on $x\ln x$ and implicit "
                r"differentiation to obtain a correct $\frac{1}{y}\frac{\mathrm{d}y}{\mathrm{d}x}=1+\ln x$."),
        ({"a"}, r"Most of these candidates then applied $\frac{\mathrm{d}y}{\mathrm{d}x}=0$ to obtain "
                r"$x=\mathrm{e}^{-1}$.", BACK),
        ({"a"}, r"Some candidates, who received partial credit, used a ‘$\log_{10}$’ method to obtain $x=0.1$, after "
                r"finding $\frac{1}{y}\frac{\mathrm{d}y}{\mathrm{d}x}=1+\log_{10}x$."),
        ({"a"}, "A few candidates used logarithms without reference to a base."),
        ({"a"}, r"Those who proceeded to obtain $x=0.1$ received partial credit and those who obtained "
                r"$x=\mathrm{e}^{-1}$ were allowed full marks.", BACK),
        ({"a"}, "There were some alternative methods employed by a few candidates in Q11(a)."),
        ({"a"}, r"A few candidates rewrote $y=x^x$ as $y=\mathrm{e}^{x\ln x}$ and applied $\frac{\mathrm{d}y}"
                r"{\mathrm{d}x}=(1+\ln x)\mathrm{e}^{x\ln x}=0$ to give a correct $x=\mathrm{e}^{-1}$."),
        ({"a"}, r"Others differentiated both sides of the equation $\ln y=x\ln x$ with respect to $y$ and usually "
                r"proceeded to find $x=\mathrm{e}^{-1}$."),
        ({"a"}, r"A very few candidates applied the quotient rule to the equation $x=\frac{\ln y}{\ln x}$, but were "
                r"rarely successful with this method."),
        ({"b"}, r"In Q11(b), most candidates evaluated either $x^x$ or $x^x-2$ at both $x=1.5$ and $x=1.6$."),
        ({"b"}, r"Many candidates compared their values with either 2 or 0 (depending on whether they evaluated $x^x$ "
                r"or $x^x-2$)."),
        ({"b"}, r"Although many of these concluded that $1.5<\alpha<1.6$, only a few made any reference to the curve "
                r"being continuous in this interval.", BACK),
        ({"b"}, r"A few candidates, who made no creditable progress, used values of $x$ outside the given range, e.g. "
                r"$x=1.4$ and $x=1.6$."),
        ({"b"}, r"Very few candidates used values within the range e.g. $x=1.51$ and $x=1.59$, which meant that they "
                r"were able to earn both marks."),
        ({"c"}, r"In Q11(c), most candidates found a correct $x_4=1.673$, although a few did not state $x_4$ correct "
                r"to 3 decimal places."),
        ({"c"}, r"Some wrote down the iterates $x_1$, $x_2$ and $x_3$ as part of their solution, while others stated "
                r"$x_4$ with no intermediate work."),
        ({"d"}, "In Q11(d), some candidates gave correct descriptions such as ‘sequence oscillates between 1 and 2’ "
                "or ‘the sequence is periodic with period 2’.", NO),
        ({"d"}, "Other descriptions such as ‘alternates between 1 and 2’, ‘keep getting 1 and 2’ or ‘fluctuates "
                "between 1 and 2’ were condoned.", NO),
        ({"d"}, "Some credit was given for partial explanations such as ‘sequence is non-convergent’, ‘sequence "
                "oscillates’ or ‘sequence is divergent’.", NO),
    ],
    "12": [
        ({"a", "b"}, "Q12(a) discriminated well between the higher ability candidates and it was possible for "
                     "candidates of all abilities to gain access to Q12(b).", NO),
        ({"a"}, r"In Q12(a), many candidates struggled to apply a complete strategy which would help them to make "
                r"significant progress in proceeding from $" + Q12L + r"$, via an intermediate stage of "
                r"$\frac{\cos(3\theta-\theta)}{\sin\theta\cos\theta}$, $\frac{\cos2\theta(\cos^2\theta+\sin^2\theta)}"
                r"{\sin\theta\cos\theta}$ or $\frac{\cos2\theta}{\sin\theta\cos\theta}$, to the given result "
                r"$2\cot2\theta$."),
        ({"a"}, r"Candidates who used Way 1, as described in the mark scheme, gained some credit for rationalising $"
                + Q12L + r"$ to give $\frac{\cos3\theta\cos\theta+\sin3\theta\sin\theta}{\sin\theta\cos\theta}$."),
        ({"a"}, r"Of those candidates who correctly applied $\sin\theta\cos\theta=\frac{1}{2}\sin2\theta$ to the "
                r"denominator, only a few realised that the numerator could be written as $\cos2\theta$.", NO),
        ({"a"}, r"A common error in using Way 1 was to simplify $" + Q12L + r"$ to give $\frac{\cos^23\theta+"
                r"\sin^23\theta}{\sin\theta\cos\theta}$ or $\frac{\cos4\theta+\sin4\theta}{\sin\theta\cos\theta}$."),
        ({"a"}, "Way 2, as described in the mark scheme (and variations of this), was the most popular approach among "
                "candidates who completed the proof successfully.", NO),
        ({"a"}, "Candidates only started to access the marks for Way 2 when they combined their fractions by "
                "rationalising the denominator."),
        ({"a"}, r"Errors using Way 2 included the incorrect expansion of $\cos(2\theta+\theta)$ or "
                r"$\sin(2\theta+\theta)$, bracketing errors, manipulation errors or sign errors."),
        ({"a"}, r"A few candidates started their proof from $2\cot2\theta$."),
        ({"a"}, r"They usually progressed as far as writing either $2\cot2\theta=\frac{2\cos2\theta}{\sin2\theta}$ or "
                r"$2\cot2\theta=\frac{2(1-\tan^2\theta)}{2\tan\theta}$, but could make no creditable progress until "
                r"they applied a Way 3 method as described in the mark scheme."),
        ({"a"}, r"Some candidates spent a considerable amount of time attempting to write $" + Q12L + r"$ in terms of "
                r"$\theta$ to give e.g. $\frac{4\cos^3\theta-3\cos\theta}{\sin\theta}+\frac{3\sin\theta-4\sin^3\theta}"
                r"{\cos\theta}$."),
        ({"a"}, "candidates only started to access the marks for this method when they combined their fractions by "
                "rationalising the denominator."),
        ({"b"}, r"In Q13(b), most candidates used the result given in Q13(a) to deduce the equation "
                r"$2\cot2\theta=4$.",
         {"note": r"this is Q12(b), which uses the result proved in Q12(a)"}),
        ({"b"}, r"Most of these then attempted to solve $\tan2\theta=\frac{1}{2}$, and some obtained the correct "
                r"answer $\theta=103.3^\circ$.", BACK),
        ({"b"}, r"Common errors included attempting to solve $\tan2\theta=2$ and finding more than one value for "
                r"$\theta$."),
        ({"b"}, r"A few candidates obtained $\theta=103.3^\circ$ by solving the equation $\frac{2(1-\tan^2\theta)}"
                r"{2\tan\theta}=4$."),
    ],
    "13": [
        (W, "Q13 discriminated well between the medium and higher ability candidates."),
        (W, "Lower ability candidates, however, struggled to gain any creditable progress."),
        (W, "It was obvious that some candidates had been well prepared for this ‘optimisation’ question and the "
            "quality of their responses reflected this.", NO),
        ({"a", "b", "c"}, "candidates who attempted this question generally found Q13(b) and Q13(c) accessible but "
                          "some struggled to complete the proof in Q13(a)."),
        ({"a", "b", "c"}, "In a few cases, candidates who scored zero marks in Q13(a) went on to achieve full marks in "
                          "the remainder of Q13 by using the given result for the surface area."),
        ({"a", "b", "c"}, "There were, however, many instances where candidates who struggled with Q13(a) then gave "
                          "up and did not attempt the remainder of the question."),
        ({"a"}, r"In Q13(a), successful candidates followed a correct strategy of forming an equation for the volume "
                r"of the tank, rearranging their equation to give an expression for $h$ in terms of $r$ and "
                r"substituting their expression for $h$ into their formula for the surface area of the tank."),
        ({"a"}, "Some candidates did not halve the given sphere formulae so that they could use these for the "
                "hemispherical shell.", NO),
        ({"a"}, "This led to errors in both their volume equation and surface area expression.", BACK),
        ({"a"}, "Other candidates did not include the area of the circular base in their surface area expression."),
        ({"a"}, r"These errors led to an incorrect volume equation $6=\pi r^2h+\frac{4}{3}\pi r^3$ and incorrect "
                r"surface area expressions $A=5\pi r^2+2\pi rh$ and $A=2\pi r^2+2\pi rh$.", BACK),
        ({"a"}, "In other cases, bracketing errors, manipulation errors, or using incorrect formulae for the curved "
                "surface area of a cylinder, prevented candidates from achieving the given result."),
        ({"b"}, r"In Q13(b), many candidates who attempted this part applied a complete method to find their value of "
                r"$r$ for which $\frac{\mathrm{d}A}{\mathrm{d}r}=0$."),
        ({"b"}, r"Most successful candidates found $r=1.05$ metres, with a few giving an exact answer "
                r"$r=\sqrt[3]{\frac{18}{5\pi}}$ metres, which was condoned."),
        ({"b"}, r"Some candidates differentiated $A$ incorrectly to give $\frac{\mathrm{d}A}{\mathrm{d}r}=12\ln r+"
                r"\frac{10}{3}\pi r$, while others used incorrect algebra when solving the correct equation "
                r"$-\frac{12}{r^2}+\frac{10}{3}\pi r=0$."),
        ({"b"}, r"A few candidates used the incorrect method of finding a value of $r$ for which "
                r"$\frac{\mathrm{d}^2A}{\mathrm{d}r^2}=0$."),
        ({"c"}, r"In Q13(c), most candidates who attempted this part correctly substituted their value of $r$, found "
                r"from solving $\frac{\mathrm{d}A}{\mathrm{d}r}=0$, into the model with equation $A=\frac{12}{r}+"
                r"\frac{5}{3}\pi r^2$, with many obtaining a correct minimum surface area of $17\text{ m}^2$."),
        ({"c"}, r"A few candidates, who made no creditable progress, substituted their value for $r$, found from "
                r"solving $\frac{\mathrm{d}^2A}{\mathrm{d}r^2}=0$, into the model for $A$."),
    ],
    "14": [
        (W, "Q14 discriminated well between the higher ability candidates."),
        (W, "Lower and medium ability candidates, however, found this question demanding with most of these "
            "candidates scoring no more than two marks.", NO),
        (W, "There were a few candidates who made no attempt at this question, either because the question was too "
            "demanding, or because their time had run out."),
        ({"a", "b", "c"}, "Most higher ability candidates made good progress in Q14(a) and Q14(c) but they often "
                          "struggled to make progress in Q14(b)."),
        ({"a"}, r"In Q14(a), most candidates who attempted this part differentiated $u=4-\sqrt{h}$ to give a correct "
                r"$\frac{\mathrm{d}u}{\mathrm{d}h}=-\frac{1}{2}h^{-\frac{1}{2}}$, with a few finding a correct "
                r"$\frac{\mathrm{d}h}{\mathrm{d}u}=-2(4-u)$ and some differentiating incorrectly to give "
                r"$\frac{\mathrm{d}u}{\mathrm{d}h}=\frac{1}{2}h^{-\frac{1}{2}}$."),
        ({"a"}, "At this stage, some candidates failed to make further creditable progress.", BACK),
        ({"a"}, r"Many candidates struggled to apply the substitution completely to give an integral of the form "
                r"$\int\frac{k(4-u)}{u}\,\mathrm{d}u$, with some making sign errors in the numerator of this "
                r"integral.", NO),
        ({"a"}, r"Those who progressed this far generally went on to divide each term in the numerator by $u$ to give "
                r"an integral of the form $\int\left(\frac{A}{u}+B\right)\mathrm{d}u$, with many of them obtaining a "
                r"correct $\int\left(-\frac{8}{u}+2\right)\mathrm{d}u$.", BACK),
        ({"a"}, r"Most integrated correctly and applied $u=4-\sqrt{h}$ to obtain a correct $-8\ln" + H
                + r"+2(4-\sqrt{h})+c$."),
        ({"a"}, r"Some candidates could not deal with the transition from $8+c$ to $k$ to achieve the given $-8\ln"
                + H + r"-2\sqrt{h}+k$, and a large number of these candidates incorrectly stated $k=8$.", NO),
        ({"a"}, r"Those few candidates who applied integration by parts on $\int\frac{2u-8}{u}\,\mathrm{d}u$ rarely "
                r"progressed to give a correct solution to this part.", NO),
        ({"b"}, r"In Q14(b), some candidates correctly set $\frac{\mathrm{d}h}{\mathrm{d}t}=0$ but only a few deduced "
                r"the equation $4-\sqrt{h}=0$."),
        ({"b"}, r"Some candidates used $h=16$ to state a correct allowable answer such as $0<h<16$, "
                r"$0\leqslant h\leqslant16$ or $h<16$.", NO),
        ({"b"}, r"A common mistake was to solve $\sqrt{h}=4$ to give $h=2$."),
        ({"b", "c"}, "Material for Q14(c) was sometimes seen in Q14(b)."),
        ({"c"}, "Most candidates who attempted Q14(c) separated the variables correctly."),
        ({"c"}, r"Some candidates integrated $t^{0.25}$ incorrectly to give $\lambda t^{0.25}$, $\lambda t^{-0.75}$ "
                r"or $\frac{5}{4}t^{1.25}$ while others integrated $\frac{1}{(4-\sqrt{h})}$ without reference to the "
                r"result from Q14(a)."),
        ({"c"}, r"Many candidates applied $t=0$, $h=1$ to find their constant of integration."),
        ({"c"}, r"Common errors at this stage included not applying a constant of integration and using either $t=0$, "
                r"$h=0$ or $t=1$, $h=1$ to find their constant of integration.", BACK),
        ({"c"}, r"Most candidates who progressed this far applied a complete process of substituting their constant "
                r"of integration and $h=12$ into their integrated equation and solving this equation to find their "
                r"value for $t$.", BACK),
        ({"c"}, r"In many cases, sign errors, bracketing errors, manipulation errors or an incorrect method of solving "
                r"a correct $t^{1.25}=221.2795202\ldots$, prevented candidates from obtaining the correct answer "
                r"$t=75.2$ years."),
    ],
}

# Difficulty: (rating, (question, index of the REPORT sentence it rests on)).
RATINGS = {
    "01": ("medium", ("01", 0)),
    "02a": ("hard", ("02", 1)),
    "02b": ("medium", ("02", 11)),
    "03a": ("medium", ("03", 1)),
    "03b": ("easy", ("03", 5)),
    "04": ("medium", ("04", 0)),
    "05": ("hard", ("05", 7)),
    "06a": ("hard", ("06", 2)),
    "06b": ("hard", ("06", 10)),
    "06c": ("medium", ("06", 14)),
    "06d": ("medium", ("06", 21)),
    "07a": ("easy", ("07", 2)),
    "07b": ("medium", ("07", 5)),
    "07c": ("medium", ("07", 13)),
    "07d": ("medium", ("07", 16)),
    "08i": ("medium", ("08", 8)),
    "08ii": ("hard", ("08", 13)),
    "09a": ("medium", ("09", 7)),
    "09b": ("easy", ("09", 8)),
    "09c": ("medium", ("09", 15)),
    "10a": ("easy", ("10", 2)),
    "10b": ("hard", ("10", 8)),
    "10c": ("hard", ("10", 14)),
    "11a": ("hard", ("11", 1)),
    "11b": ("medium", ("11", 16)),
    "11c": ("easy", ("11", 19)),
    "11d": ("medium", ("11", 21)),
    "12a": ("hard", ("12", 1)),
    "12b": ("medium", ("12", 13)),
    "13a": ("medium", ("13", 3)),
    "13b": ("medium", ("13", 12)),
    "13c": ("medium", ("13", 16)),
    "14a": ("hard", ("14", 6)),
    "14b": ("hard", ("14", 11)),
    "14c": ("hard", ("14", 20)),
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
