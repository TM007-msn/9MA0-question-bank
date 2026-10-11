"""Draft builder for 9MA0-02 SPEC (A level Pure Paper 2, specimen paper).

Run (from the project root, with the venv active):
    python extraction/9MA0-02_SPEC.py        # writes out/drafts/9MA0-02_SPEC.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-02_SPEC.json

Everything here is transcribed from the source PDFs, read as page images
(figures at 200 dpi). There is no examiner report for the specimen paper, so
examiner_notes, difficulty and difficulty_evidence are all null.
The mark scheme's symbol font shows ⩽ as „ and ⩾ as … ; they are written as
\\leqslant and \\geqslant here. Two other symbols have no glyph at all and
print as an empty box: they are written as \\square. In 13(a) the question
paper shows the symbol is ℤ, so that box carries a [sic] note; in 4(c) nothing
shows which symbol is meant, so those boxes are left as printed.
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

P, S = "9MA0-02", "SPEC"
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
NUM = "Numerical methods"


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


DY = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
DVDH = r"\frac{\mathrm{d}V}{\mathrm{d}h}"
DHDT = r"\frac{\mathrm{d}h}{\mathrm{d}t}"
DVDT = r"\frac{\mathrm{d}V}{\mathrm{d}t}"
DPDT = r"\frac{\mathrm{d}p}{\mathrm{d}t}"

# ---------------- shared stems and parts ----------------
FIG1 = (r"[Figure 1: a circle with centre $O$ and the points $A$ (upper right) and $B$ (lower right) on its "
        r"circumference; the major sector $AOB$ is shaded and the minor sector, on the right, is unshaded.]")

Q2A = [r"Given that $\theta$ is small, use the small angle approximation for $\cos\theta$ to show that",
       r"$$1+4\cos\theta+3\cos^2\theta\approx8-5\theta^2$$"]
Q2W = [r"Adele uses $\theta=5^\circ$ to test the approximation in part (a).", "Adele’s working is shown below.",
       r"$$\boxed{\begin{array}{l}\text{Using my calculator, }1+4\cos(5^\circ)+3\cos^2(5^\circ)=7.962\text{, to 3 "
       r"decimal places.}\\\text{Using the approximation }8-5\theta^2\text{ gives }8-5(5)^2=-117\\\text{Therefore, }"
       r"1+4\cos\theta+3\cos^2\theta\approx8-5\theta^2\text{ is not true for }\theta=5^\circ\end{array}}$$"]

Q3 = [r"A cup of hot tea was placed on a table. At time $t$ minutes after the cup was placed on the table, the "
      r"temperature of the tea in the cup, $\theta$ °C, is modelled by the equation",
      r"$$\theta=25+A\mathrm{e}^{-0.03t}$$", "where $A$ is a constant.",
      r"The temperature of the tea was $75^\circ$C when the cup was placed on the table."]
Q3A = "Find a complete equation for the model."

Q4A = ["Sketch the graph with equation", "$$y=|2x-5|$$",
       "stating the coordinates of any points where the graph cuts or meets the coordinate axes."]

FIG2 = (r"[Figure 2: the curve $y=\mathrm{f}(x)$ rising steeply from below the $x$-axis close to the $y$-axis, crossing "
        r"the $x$-axis at $A$ just to the right of $O$, reaching a maximum at $Q$, then falling to cross the $x$-axis "
        r"at $B$ and continuing downwards.]")
Q6 = [FIG2, r"Figure 2 shows a sketch of the curve with equation $y=\mathrm{f}(x)$, where",
      r"$$\mathrm{f}(x)=(8-x)\ln x,\qquad x>0$$",
      "The curve cuts the $x$-axis at the points $A$ and $B$ and has a maximum turning point at $Q$, as shown in "
      "Figure 2."]
Q6B = ["Show that the $x$ coordinate of $Q$ satisfies", r"$$x=\frac{8}{1+\ln x}$$"]

Q7 = ["A bacterial culture has area $p$ mm$^2$ at time $t$ hours after the culture was placed onto a circular dish.",
      "A scientist states that at time $t$ hours, the rate of increase of the area of the culture can be modelled as "
      "being proportional to the area of the culture."]
Q7A = ["Show that the scientist’s model for $p$ leads to the equation", r"$$p=a\mathrm{e}^{kt}$$",
       "where $a$ and $k$ are constants."]
Q7S = ["The scientist measures the values for $p$ at regular intervals during the first 24 hours after the culture "
       "was placed onto the dish.",
       r"She plots a graph of $\ln p$ against $t$ and finds that the points on the graph lie close to a straight line "
       r"with gradient 0.14 and vertical intercept 3.95"]
Q7B = "Estimate, to 2 significant figures, the value of $a$ and the value of $k$."
Q7C = ["Hence show that the model for $p$ can be rewritten as", "$$p=ab^t$$",
       "stating, to 3 significant figures, the value of the constant $b$."]

FIG3 = (r"[Figure 3: a hemispherical bowl with its flat rim at the top, partly filled with water (shaded); the depth of "
        r"the water, from the lowest point of the bowl up to the water surface, is marked $h$.]")
Q8 = [FIG3, "A bowl is modelled as a hemispherical shell as shown in Figure 3.",
      "Initially the bowl is empty and water begins to flow into the bowl.",
      "When the depth of the water is $h$ cm, the volume of water, $V$ cm$^3$, according to the model is given by",
      r"$$V=\frac{1}{3}\pi h^2(75-h),\qquad0\leqslant h\leqslant24$$",
      r"The flow of water into the bowl is at a constant rate of $160\pi$ cm$^3$ s$^{-1}$ for $0\leqslant h\leqslant12$"]
Q8A = r"Find the rate of change of the depth of the water, in cm s$^{-1}$, when $h=10$"

Q9 = ["A circle with centre $A(3, -1)$ passes through the point $P(-9, 8)$ and the point $Q(15, -10)$"]
Q9A = "Show that $PQ$ is a diameter of the circle."
Q9B = "Find an equation for the circle."
Q9R = ["A point $R$ also lies on the circle.", "Given that the length of the chord $PR$ is 20 units,"]

FIG4 = (r"[Figure 4: the curve $C$ coming down steeply from high up just to the right of the $y$-axis and flattening out "
        r"towards the $x$-axis as $x$ increases; the region $R$ under $C$ between the vertical lines $x=\ln2$ and "
        r"$x=\ln4$ is shaded.]")
Q10 = [FIG4, "Figure 4 shows a sketch of the curve $C$ with parametric equations",
       r"$$x=\ln(t+2),\ y=\frac{1}{t+1},\qquad t>-\frac{2}{3}$$"]

Q13A = ["Show that", r"$$\mathrm{cosec}\,2x+\cot2x\equiv\cot x,\qquad x\neq90n^\circ,\ n\in\mathbb{Z}$$"]

LATEX = {
    "01": L(FIG1, "Figure 1 shows a circle with centre $O$. The points $A$ and $B$ lie on the circumference of the "
                  "circle.",
            "The area of the major sector, shown shaded in Figure 1, is 135 cm$^2$.",
            "The reflex angle $AOB$ is 4.8 radians.",
            r"Find the exact length, in cm, of the minor arc $AB$, giving your answer in the form $a\pi+b$, where $a$ "
            r"and $b$ are integers to be found."),
    "02a": L(*Q2A),
    "02b": L("(a) " + Q2A[0], Q2A[1], *Q2W, "(b) (i) Identify the mistake made by Adele in her working.",
             r"(ii) Show that $8-5\theta^2$ can be used to give a good approximation to $1+4\cos\theta+3\cos^2\theta$ "
             r"for an angle of size $5^\circ$"),
    "03a": L(*Q3, Q3A),
    "03b": L(*Q3, "(a) " + Q3A,
             r"(b) Use the model to find the time taken for the tea to cool from $75^\circ$C to $60^\circ$C, giving "
             r"your answer in minutes to one decimal place."),
    "03c": L(*Q3, "(a) " + Q3A,
             r"Two hours after the cup was placed on the table, the temperature of the tea was measured as "
             r"$20.3^\circ$C.",
             "Using this information,", "(c) evaluate the model, explaining your reasoning."),
    "04a": L(*Q4A),
    "04b": L("Find the values of $x$ which satisfy", "$$|2x-5|>7$$"),
    "04c": L("Find the values of $x$ which satisfy", r"$$|2x-5|>x-\frac{5}{2}$$", "Write your answer in set notation."),
    "05": L("The line $l$ has equation", "$$3x-2y=k$$", "where $k$ is a real constant.",
            "Given that the line $l$ intersects the curve with equation", "$$y=2x^2-5$$",
            "at two distinct points, find the range of possible values for $k$."),
    "06a": L(*Q6, "Find the $x$ coordinate of $A$ and the $x$ coordinate of $B$."),
    "06b": L(*Q6, *Q6B),
    "06c": L(*Q6, "(b) " + Q6B[0], Q6B[1], "(c) Show that the $x$ coordinate of $Q$ lies between 3.5 and 3.6"),
    "06d": L(*Q6, "Use the iterative formula", r"$$x_{n+1}=\frac{8}{1+\ln x_n}\qquad n\in\mathbb{N}$$",
             "with $x_1=3.5$ to", "(i) find the value of $x_5$ to 4 decimal places,",
             "(ii) find the $x$ coordinate of $Q$ accurate to 2 decimal places."),
    "07a": L(*Q7, *Q7A),
    "07b": L(*Q7, "(a) " + Q7A[0], *Q7A[1:], *Q7S, "(b) " + Q7B),
    "07c": L(*Q7, "(a) " + Q7A[0], *Q7A[1:], *Q7S, "(b) " + Q7B, "(c) " + Q7C[0], *Q7C[1:]),
    "07d": L(*Q7, "(a) " + Q7A[0], *Q7A[1:], *Q7S, "(b) " + Q7B, "(c) " + Q7C[0], *Q7C[1:],
             "With reference to this model,", "(d) (i) interpret the value of the constant $a$,",
             "(ii) interpret the value of the constant $b$."),
    "07e": L(*Q7, "(a) " + Q7A[0], *Q7A[1:], *Q7S, "(e) State a long term limitation of the model for $p$."),
    "08a": L(*Q8, Q8A),
    "08b": L(*Q8, "(a) " + Q8A,
             r"Given that the flow of water into the bowl is increased to a constant rate of $300\pi$ cm$^3$ s$^{-1}$ "
             r"for $12<h\leqslant24$",
             r"(b) find the rate of change of the depth of the water, in cm s$^{-1}$, when $h=20$"),
    "09a": L(*Q9, Q9A),
    "09b": L(*Q9, Q9B),
    "09c": L(*Q9, "(b) " + Q9B, *Q9R, "(c) find the length of the shortest distance from $A$ to the chord $PR$.",
             "Give your answer as a surd in its simplest form."),
    "09d": L(*Q9, "(a) " + Q9A, "(b) " + Q9B, *Q9R,
             "(d) Find the size of angle $ARQ$, giving your answer to the nearest 0.1 of a degree."),
    "10a": L(*Q10, "State the domain of values of $x$ for the curve $C$."),
    "10b": L(*Q10, "The finite region $R$, shown shaded in Figure 4, is bounded by the curve $C$, the line with "
                   r"equation $x=\ln2$, the $x$-axis and the line with equation $x=\ln4$",
             r"Use calculus to show that the area of $R$ is $\ln\left(\frac{3}{2}\right)$."),
    "11": L("The second, third and fourth terms of an arithmetic sequence are $2k$, $5k-10$ and $7k-14$ respectively, "
            "where $k$ is a constant.",
            "Show that the sum of the first $n$ terms of the sequence is a square number."),
    "12": L("A curve $C$ is given by the equation",
            r"$$\sin x+\cos y=0.5\qquad-\frac{\pi}{2}\leqslant x<\frac{3\pi}{2},\ -\pi<y<\pi$$",
            "A point $P$ lies on $C$.", "The tangent to $C$ at the point $P$ is parallel to the $x$-axis.",
            "Find the exact coordinates of all possible points $P$, justifying your answer.",
            "(Solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "13a": L(*Q13A),
    "13b": L("(a) " + Q13A[0], Q13A[1], r"(b) Hence, or otherwise, solve, for $0\leqslant\theta<180^\circ$,",
             r"$$\mathrm{cosec}(4\theta+10^\circ)+\cot(4\theta+10^\circ)=\sqrt{3}$$", "You must show your working.",
             "(Solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "14i": L("Kayden claims that", r"$$3^x\geqslant2^x$$",
             "Determine whether Kayden’s claim is always true, sometimes true or never true, justifying your answer."),
    "14ii": L(r"Prove that $\sqrt{3}$ is an irrational number."),
}

Q1ALT = "ALT: 1 Alt"
Q5A1 = "ALT: 5 Alt 1"
Q5A2 = "ALT: 5 Alt 2"
Q9A1 = "ALT: (a) Alt 1"
Q9A2 = "ALT: (a) Alt 2"
Q10A1 = "ALT: (b) Alt 1"
Q10A2 = "ALT: (b) Alt 2"
K169 = r"Critical value obtained of $\frac{169}{16}$. Notes: See scheme"
KANS = r"$k<\frac{169}{16}$ o.e."
AREA = (r"$=(\ln3-\ln4)-(\ln1-\ln2)$ $=\ln3-\ln4+\ln2=\ln\left(\frac{(3)(2)}{4}\right)=\ln\left(\frac{6}{4}\right)$")
SHOW32 = (r"$=\ln\left(\frac{3}{2}\right)$ *. Notes: Correctly shows that the area of $R$ is "
          r"$\ln\left(\frac{3}{2}\right)$, with no errors seen in their working")

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", TRIG, "5.1", 4, LATEX["01"],
      [r"M1 (AO 1.1a): $\frac{1}{2}r^2(4.8)$. Notes: Applies formula for the area of a sector with $\theta=4.8$; i.e. "
       r"$\frac{1}{2}r^2\theta$ with $\theta=4.8$ Note: Allow M1 for considering ratios. E.g. "
       r"$\frac{135}{\pi r^2}=\frac{4.8}{2\pi}$",
       r"A1 (AO 1.1b): $\frac{1}{2}r^2(4.8)=135\Rightarrow r^2=\frac{225}{4}\Rightarrow r=7.5$ o.e. Notes: Uses a "
       r"correct equation $\left(\text{e.g. }\frac{1}{2}r^2(4.8)=135\right)$ to obtain a radius of 7.5",
       r"dM1 (AO 3.1a): length of minor arc $=7.5(2\pi-4.8)$. Notes: Depends on the previous M mark. A complete "
       r"process for finding the length of the minor arc $AB$, by either • (their $r$)$\times(2\pi-4.8)$ • "
       r"$2\pi$(their $r$) $-$ (their $r$)(4.8)",
       r"A1 (AO 1.1b): $=15\pi-36$ $\{a=15,b=-36\}$. Notes: Correct exact answer in its simplest form, e.g. "
       r"$15\pi-36$ or $-36+15\pi$",
       rf"{Q1ALT} — M1 (AO 1.1a): $\frac{{1}}{{2}}r^2(4.8)$",
       rf"{Q1ALT} — A1 (AO 1.1b): $\frac{{1}}{{2}}r^2(4.8)=135\Rightarrow r^2=\frac{{225}}{{4}}\Rightarrow r=7.5$ o.e.",
       rf"{Q1ALT} — (no mark): length of major arc $=7.5(4.8)$ $\{{=36\}}$",
       rf"{Q1ALT} — dM1 (AO 3.1a): length of minor arc $=2\pi(7.5)-36$",
       rf"{Q1ALT} — A1 (AO 1.1b): $=15\pi-36$ $\{{a=15,b=-36\}}$"],
      True, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", TRIG, "5.2", 3, LATEX["02a"],
      [r"M1 (AO 1.1b): Attempts to substitute $\cos\theta\approx1-\frac{1}{2}\theta^2$ into either $1+4\cos\theta$ or "
       r"$3\cos^2\theta$. Notes: See scheme",
       r"M1 (AO 1.1b): $1+4\cos\theta+3\cos^2\theta\approx1+4\left(1-\frac{1}{2}\theta^2\right)+3\left(1-\frac{1}{2}"
       r"\theta^2\right)^2$ $=1+4\left(1-\frac{1}{2}\theta^2\right)+3\left(1-\theta^2+\frac{1}{4}\theta^4\right)$. "
       r"Notes: Substitutes $\cos\theta\approx1-\frac{1}{2}\theta^2$ into $1+4\cos\theta+3\cos^2\theta$ and attempts to "
       r"apply $\left(1-\frac{1}{2}\theta^2\right)^2$ Note: It is not a requirement for this mark to write or refer to "
       r"the term in $\theta^4$",
       r"A1* (AO 2.1): $=1+4-2\theta^2+3-3\theta^2+\frac{3}{4}\theta^4$ $=8-5\theta^2$ *. Notes: Correct proof with no "
       r"errors seen in working. Note: It is not a requirement for this mark to write or refer to the term in "
       r"$\theta^4$"],
      False, 4),
    e("02b", "2(b)", TRIG, "5.2, 5.1", 2, LATEX["02b"],
      [r"B1 (AO 2.3): (i) E.g. • Adele is working in degrees and not radians • Adele should substitute "
       r"$\theta=\frac{5\pi}{180}$ and not $\theta=5$ into the approximation. Notes: See scheme",
       r"B1 (AO 2.4): (ii) $8-5\left(\frac{5\pi}{180}\right)^2=$ awrt 7.962, so $\theta=5^\circ$ gives a good "
       r"approximation. Notes: Substitutes $\theta=\frac{5\pi}{180}$ or $\frac{\pi}{36}$ into $8-5\theta^2$ to give awrt "
       r"7.962 $\textbf{and}$ an appropriate conclusion."],
      False, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", EXP, "6.7", 1, LATEX["03a"],
      [r"B1 (AO 3.3): $\{t=0,\theta=75\Rightarrow75=25+A\Rightarrow A=50\}\Rightarrow\theta=25+50\mathrm{e}^{-0.03t}$. "
       r"Notes: Applies $t=0,\theta=75$ to give the complete model $\theta=25+50\mathrm{e}^{-0.03t}$"],
      False, 6),
    e("03b", "3(b)", EXP, "6.7, 6.3", 2, LATEX["03b"],
      [r"M1 (AO 3.4): $\{\theta=60\Rightarrow\}\Rightarrow60=25+\text{“}50\text{”}\mathrm{e}^{-0.03t}\Rightarrow"
       r"\mathrm{e}^{-0.03t}=\frac{60-25}{\text{“}50\text{”}}$. Notes: Applies $\theta=60$ and their value of $A$ to the "
       r"model and rearranges to make $\mathrm{e}^{-0.03t}$ the subject. Note: Later working can imply this mark.",
       r"A1 (AO 1.1b): $t=\frac{\ln(0.7)}{-0.03}=11.8891648=11.9$ minutes (1 dp). Notes: Obtains 11.9 (minutes) with no "
       r"errors in manipulation seen."],
      False, 6),
    e("03c", "3(c)", EXP, "6.7", 1, LATEX["03c"],
      [r"B1 (AO 3.5a): A valid evaluation of the model, which relates to the large values of $t$. E.g. • As "
       r"$20.3<25$ then the model is not true for large values of $t$ • $\mathrm{e}^{-0.03t}=\frac{20.3-25}"
       r"{\text{“}50\text{”}}=-0.094$ does not have any solutions and so the model predicts that tea in the room will "
       r"never be $20.3^\circ$C. So the model does not work for large values of $t$ • $t=120\Rightarrow\theta=25+"
       r"50e^{-0.03(120)}=26.36\ldots$ which is not approximately equal to 20.3, so the model is not true for large "
       r"values of $t$. Notes: See scheme"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", ALG, "2.7", 2, LATEX["04a"],
      [r"B1 (AO 1.1b): Correct graph in quadrant 1 and quadrant 2 with V on the $x$-axis [the mark scheme shows a "
       r"sketch of $y=|2x-5|$: a V shape with its vertex on the $x$-axis at $\frac{5}{2}$, crossing the $y$-axis at 5]. "
       r"Notes: See scheme",
       r"B1 (AO 1.1b): States $(0, 5)$ and $\left(\frac{5}{2}, 0\right)$ $\textbf{or}$ $\frac{5}{2}$ marked in the "
       r"correct position on the $x$-axis $\textbf{and}$ 5 marked in the correct position on the $y$-axis. Notes: See "
       r"scheme"],
      False, 8),
    e("04b", "4(b)", ALG, "2.7, 2.5", 2, LATEX["04b"],
      [r"M1 (AO 1.1b): $|2x-5|>7$ $2x-5=7\Rightarrow x=\ldots$ $\textbf{and}$ $-(2x-5)=7\Rightarrow x=\ldots$ Notes: "
       r"See scheme",
       r"A1 (AO 1.1b): $\{$critical values are $x=6,-1\Rightarrow\}$ $x<-1$ or $x>6$. Notes: Correct answer, e.g. "
       r"• $x<-1$ or $x>6$ • $x<-1\cup x>6$ • $\{x:x<-1\}\cup\{x:x>6\}$"],
      False, 8),
    e("04c", "4(c)", ALG, "2.7, 2.5", 2, LATEX["04c"],
      [r"M1 (AO 3.1a): $|2x-5|>x-\frac{5}{2}$ E.g. • Solves $2x-5=x-\frac{5}{2}$ to give $x=\frac{5}{2}$ and solves "
       r"$-(2x-5)=x-\frac{5}{2}$ to also give $x=\frac{5}{2}$ • Sketches graphs of $y=|2x-5|$ and "
       r"$y=x-\frac{5}{2}$. Indicates that these graphs meet at the point $\left(\frac{5}{2}, 0\right)$. Notes: A "
       r"complete process of finding that $y=|2x-5|$ and $y=x-\frac{5}{2}$ meet at $\textbf{only}$ one point. This can "
       r"be achieved either algebraically or graphically.",
       r"A1 (AO 2.5): Hence using set notation, e.g. • $\left\{x:x<\frac{5}{2}\right\}\cup\left\{x:x>\frac{5}{2}"
       r"\right\}$ • $\left\{x\in\square,x\neq\frac{5}{2}\right\}$ • $\square-\left\{\frac{5}{2}\right\}$ [the symbol "
       r"shown as $\square$ prints as an empty box in the mark scheme]. Notes: See scheme. Note: Final answer must be "
       r"expressed using set notation."],
      False, 8),

    # ---------------- Q5 ----------------
    e("05", "5", ALG, "2.3, 2.4, 2.5", 5, LATEX["05"],
      [r"M1 (AO 3.1a): $3x-2y=k$ intersects $y=2x^2-5$ at two distinct points Eliminate $y$ and forms quadratic "
       r"equation $=0$ or quadratic expression $\{=0\}$. Notes: Complete strategy of eliminating $x$ or $y$ and "
       r"manipulating the resulting equation to form a quadratic equation $=0$ or a quadratic expression $\{=0\}$",
       r"A1 (AO 1.1b): $\{3x-2(2x^2-5)=k\Rightarrow\}-4x^2+3x+10-k=0$. Notes: Correct algebra leading to either • "
       r"$-4x^2+3x+10-k=0$ or $4x^2-3x-10+k=0$ or a one-sided quadratic of either $-4x^2+3x+10-k$ or "
       r"$4x^2-3x-10+k$",
       r"dM1 (AO 2.1): $\{\text{“}b^2-4ac\text{”}>0\Rightarrow\}$ $3^2-4(-4)(10-k)>0$ $9+16(10-k)>0\Rightarrow"
       r"169-16k>0$. Notes: Depends on the previous M mark. Interprets $3x-2y=k$ intersecting $y=2x^2-5$ at two "
       r"distinct points by applying “$b^2-4ac$” $>0$ to their quadratic equation or one-sided quadratic.",
       r"B1 (AO 1.1b): " + K169,
       r"A1 (AO 1.1b): " + KANS + r". Notes: Correct answer, e.g. • $k<\frac{169}{16}$ • "
       r"$\left\{k:k<\frac{169}{16}\right\}$",
       rf"{Q5A1} — M1 (AO 3.1a): Eliminate $y$ and forms quadratic equation $=0$ or quadratic expression $\{{=0\}}$ "
       r"$y=2\left(\frac{1}{3}(k+2y)\right)^2-5\Rightarrow y=\frac{2}{9}(k^2+4ky+4y^2)-5$",
       rf"{Q5A1} — A1 (AO 1.1b): $8y^2+(8k-9)y+2k^2-45=0$. Notes: • $8y^2+(8k-9)y+2k^2-45=0$ or a one-sided "
       r"quadratic of e.g. $8y^2+(8k-9)y+2k^2-45$",
       rf"{Q5A1} — dM1 (AO 2.1): $\{{\text{{“}}b^2-4ac\text{{”}}>0\Rightarrow\}}$ $(8k-9)^2-4(8)(2k^2-45)>0$ "
       r"$64k^2-144k+81-64k^2+1440>0\Rightarrow-144k+1521>0$",
       rf"{Q5A1} — B1 (AO 1.1b): Critical value obtained of $\frac{{169}}{{16}}$",
       rf"{Q5A1} — A1 (AO 1.1b): {KANS}",
       rf"{Q5A2} — M1 (AO 3.1a): ${DY}=4x$, $m_l=\frac{{3}}{{2}}\Rightarrow4x=\frac{{3}}{{2}}\Rightarrow x=\frac{{3}}"
       r"{8}$. So $y=2\left(\frac{3}{8}\right)^2-5=-\frac{151}{32}$. Notes: Complete strategy of using "
       r"differentiation to find the values of $x$ and $y$ where $3x-2y=k$ is a tangent to $y=2x^2-5$",
       rf"{Q5A2} — A1 (AO 1.1b): ${DY}=4x$, $m_l=\frac{{3}}{{2}}\Rightarrow4x=\frac{{3}}{{2}}\Rightarrow x="
       r"\frac{3}{8}$. So $y=2\left(\frac{3}{8}\right)^2-5=-\frac{151}{32}$. Notes: Correct algebra leading to "
       r"$x=\frac{3}{8}$, $y=-\frac{151}{32}$",
       rf"{Q5A2} — dM1 (AO 2.1): $k=3\left(\frac{{3}}{{8}}\right)-2\left(-\frac{{151}}{{32}}\right)\Rightarrow k="
       r"\ldots$ Notes: Depends on the previous M mark. Full method of substituting their $x=\frac{3}{8}$, "
       r"$y=-\frac{151}{32}$ into $l$ and attempting to find the value for $k$.",
       rf"{Q5A2} — B1 (AO 1.1b): {K169}",
       rf"{Q5A2} — A1 (AO 1.1b): {KANS}. Notes: Deduces correct answer, e.g. • $k<\frac{{169}}{{16}}$ • "
       r"$\left\{k:k<\frac{169}{16}\right\}$"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", EXP, "6.3", 1, LATEX["06a"],
      [r"B1 (AO 1.1b): $\mathrm{f}(x)=(8-x)\ln x$, $x>0$ Crosses $x$-axis $\Rightarrow\mathrm{f}(x)=0\Rightarrow"
       r"(8-x)\ln x=0$ $x$ coordinates are 1 and 8. Notes: Either • 1 and 8 • on Figure 2, marks 1 next to $A$ and 8 "
       r"next to $B$"],
      True, 12),
    e("06b", "6(b)", DIFF, "7.4, 7.3", 4, LATEX["06b"],
      [r"M1 (AO 3.1a): Complete strategy of setting $\mathrm{f}'(x)=0$ and rearranges to make $x=\ldots$ Notes: "
       r"Recognises that $Q$ is a stationary point (and not a root) and applies a complete strategy of setting "
       r"$\mathrm{f}'(x)=0$ and rearranges to make $x=\ldots$",
       r"M1 (AO 1.1b): $\left\{\begin{array}{ll}u=(8-x)&v=\ln x\\\frac{\mathrm{d}u}{\mathrm{d}x}=-1&"
       r"\frac{\mathrm{d}v}{\mathrm{d}x}=\frac{1}{x}\end{array}\right\}$ $\mathrm{f}'(x)=-\ln x+\frac{8-x}{x}$. Notes: "
       r"Applies $vu'+uv'$, where $u=8-x$, $v=\ln x$ Note: This mark can be recovered for work in part (c)",
       r"A1 (AO 1.1b): $\mathrm{f}'(x)=-\ln x+\frac{8-x}{x}$. Notes: $(8-x)\ln x\to-\ln x+\frac{8-x}{x}$, or "
       r"equivalent Note: This mark can be recovered for work in part (c)",
       r"A1* (AO 2.1): $-\ln x+\frac{8-x}{x}=0\Rightarrow-\ln x+\frac{8}{x}-1=0\Rightarrow\frac{8}{x}=1+\ln x"
       r"\Rightarrow x=\frac{8}{1+\ln x}$ *. Notes: Correct proof with no errors seen in working."],
      True, 12),
    e("06c", "6(c)", NUM, "9.1", 2, LATEX["06c"],
      [r"M1 (AO 1.1b): Evaluates both $\mathrm{f}'(3.5)$ and $\mathrm{f}'(3.6)$. Notes: Evaluates both "
       r"$\mathrm{f}'(3.5)$ and $\mathrm{f}'(3.6)$",
       r"A1 (AO 2.4): $\mathrm{f}'(3.5)=0.032951317\ldots$ and $\mathrm{f}'(3.6)=-0.058711623\ldots$ Sign change and as "
       r"$\mathrm{f}'(x)$ is continuous, the $x$ coordinate of $Q$ lies between $x=3.5$ and $x=3.6$. Notes: "
       r"$\mathrm{f}'(3.5)=$ awrt 0.03 and $\mathrm{f}'(3.6)=$ awrt $-0.06$ or $\mathrm{f}'(3.6)=-0.05$ (truncated) "
       r"$\textbf{and}$ a correct conclusion"],
      True, 12),
    e("06d", "6(d)", NUM, "9.2", 2, LATEX["06d"],
      [r"B1 (AO 1.1b): (i) $\{x_5=\}$ 3.5340. Notes: See scheme",
       r"B1 (AO 2.2a): (ii) $\{x_Q=\}$ 3.54 (2 dp). Notes: Deduces (e.g. by the use of further iterations) that the "
       r"$x$ coordinate of $Q$ is 3.54 accurate to 2 dp Note: $3.5\to3.55119\to3.52845\to3.53848\to3.53404\to3.53600"
       r"\to3.53514$ $(\to3.535518\ldots)$"],
      True, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", INT, "8.7, 7.6", 4, LATEX["07a"],
      [rf"B1 (AO 3.3): ${DPDT}\propto p\Rightarrow{DPDT}=kp$. Notes: Translates the scientist’s statement regarding "
       rf"proportionality into a differential equation, which involves a constant of proportionality. e.g. "
       rf"${DPDT}\propto p\Rightarrow{DPDT}=kp$",
       r"M1 (AO 1.1b): $\int\frac{1}{p}\,\mathrm{d}p=\int k\,\mathrm{d}t$. Notes: Correct method of separating the "
       r"variables $p$ and $t$ in their differential equation",
       r"A1 (AO 1.1b): $\ln p=kt\{+c\}$. Notes: $\ln p=kt$, with or without a constant of integration",
       r"A1* (AO 2.1): $\ln p=kt+c\Rightarrow p=\mathrm{e}^{kt+c}=\mathrm{e}^{kt}\mathrm{e}^c\Rightarrow "
       r"p=a\mathrm{e}^{kt}$ *. Notes: Correct proof with no errors seen in working."],
      False, 14),
    e("07b", "7(b)", EXP, "6.6", 3, LATEX["07b"],
      [r"M1 (AO 2.1): $p=a\mathrm{e}^{kt}\Rightarrow\ln p=\ln a+kt$ and evidence of understanding that either • "
       r"gradient $=k$ or “$M$” $=k$ • vertical intercept $=\ln a$ or “$C$” $=\ln a$. Notes: See scheme",
       r"A1 (AO 1.1b): gradient $=k=0.14$. Notes: Correctly finds $k=0.14$",
       r"A1 (AO 1.1b): vertical intercept $=\ln a=3.95\Rightarrow a=\mathrm{e}^{3.95}=51.935=52$ (2 sf). Notes: "
       r"Correctly finds $a=52$"],
      False, 14),
    e("07c", "7(c)", EXP, "6.7, 6.1", 2, LATEX["07c"],
      [r"B1 (AO 2.2a): e.g. • $p=a\mathrm{e}^{kt}\Rightarrow p=a(\mathrm{e}^k)^t=ab^t$, • $p=52\mathrm{e}^{0.14t}"
       r"\Rightarrow p=52(\mathrm{e}^{0.14})^t$. Notes: Uses algebra to correctly deduce either • $p=ab^t$ from "
       r"$p=a\mathrm{e}^{kt}$ • $p=\text{“}52\text{”}(\mathrm{e}^{\text{“}0.14\text{”}})^t$ from "
       r"$p=\text{“}52\text{”}\mathrm{e}^{\text{“}0.14\text{”}t}$",
       r"B1 (AO 1.1b): $b=1.15$ which can be implied by $p=52(1.15)^t$. Notes: See scheme"],
      False, 14),
    e("07d", "7(d)", EXP, "6.7", 2, LATEX["07d"],
      [r"B1 (AO 3.4): (i) Initial area (i.e. “52” mm$^2$) of bacterial culture that was first placed onto the circular "
       r"dish. Notes: See scheme",
       r"B1 (AO 3.4): (ii) E.g. • Rate of increase per hour of the area of bacterial culture • The area of bacterial "
       r"culture increases by “15%” each hour. Notes: See scheme"],
      False, 14),
    e("07e", "7(e)", EXP, "6.7", 1, LATEX["07e"],
      [r"B1 (AO 3.5b): The model predicts that the area of the bacteria culture will increase indefinitely, but the "
       r"size of the circular dish will be a constraint on this area. Notes: Gives a correct long-term limitation of the "
       r"model for $p$. (See scheme)."],
      False, 14),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", DIFF, "7.4, 7.6", 5, LATEX["08a"],
      [rf"M1 (AO 1.1b): ${DVDT}=160\pi$, $V=\frac{{1}}{{3}}\pi h^2(75-h)=25\pi h^2-\frac{{1}}{{3}}\pi h^3$ "
       rf"${DVDH}=50\pi h-\pi h^2$. Notes: Differentiates $V$ with respect to $h$ to give $\pm\alpha h\pm\beta h^2$, "
       r"$\alpha\neq0$, $\beta\neq0$",
       rf"A1 (AO 1.1b): ${DVDH}=50\pi h-\pi h^2$. Notes: $50\pi h-\pi h^2$",
       rf"M1 (AO 3.1a): $\left\{{{DVDH}\times{DHDT}={DVDT}\Rightarrow\right\}}$ $\left(50\pi h-\pi h^2\right){DHDT}="
       rf"160\pi$. Notes: Attempts to solve the problem by applying a complete method of $\left(\text{{their }}{DVDH}"
       rf"\right)\times{DHDT}=160\pi$",
       rf"dM1 (AO 3.4): When $h=10$, $\left\{{{DHDT}={DVDT}\div{DVDH}\Rightarrow\right\}}$ $\frac{{160\pi}}"
       r"{50\pi(10)-\pi(10)^2}$ $\left\{=\frac{160\pi}{400\pi}\right\}$. Notes: [the notes label this mark M1] "
       rf"Depends on the previous M mark. Substitutes $h=10$ into their model for ${DHDT}$ which is in the form "
       rf"$\frac{{160\pi}}{{\left(\text{{their }}{DVDH}\right)}}$",
       rf"A1 (AO 1.1b): ${DHDT}=0.4$ (cms$^{{-1}}$). Notes: Obtains the correct answer 0.4"],
      True, 18),
    e("08b", "8(b)", DIFF, "7.4", 2, LATEX["08b"],
      [rf"M1 (AO 3.4): ${DHDT}=\frac{{300\pi}}{{50\pi(20)-\pi(20)^2}}$. Notes: Realises that rate for of $160\pi$ "
       r"cm$^3$ s$^{-1}$ for $0\leqslant h\leqslant12$ has no effect when the rate is increased to $300\pi$ cm$^3$ "
       rf"s$^{{-1}}$ for $12<h\leqslant24$ and so substitutes $h=20$ into their model for ${DHDT}$ which is in the form "
       rf"$\frac{{300\pi}}{{\left(\text{{their }}{DVDH}\right)}}$",
       rf"A1 (AO 1.1b): ${DHDT}=0.5$ (cms$^{{-1}}$). Notes: Obtains the correct answer 0.5"],
      True, 18),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", COORD, "3.2", 2, LATEX["09a"],
      [r"M1 (AO 1.1b): E.g. midpoint $PQ=\left(\frac{-9+15}{2},\frac{8-10}{2}\right)$. Notes: Uses a correct method to "
       r"find the midpoint of the line segment $PQ$",
       r"A1 (AO 2.1): $=(3,-1)$, which is the centre point $A$, so $PQ$ is the diameter of the circle. Notes: Completes "
       r"proof by obtaining $(3,-1)$ and gives a correct conclusion.",
       rf"{Q9A1} — M1 (AO 1.1b): $m_{{PQ}}=\frac{{-10-8}}{{15--9}}=-\frac{{3}}{{4}}\Rightarrow PQ:y-8=-\frac{{3}}{{4}}"
       r"(x--9)$. Notes: Full attempt to find the equation of the line $PQ$",
       rf"{Q9A1} — A1 (AO 2.1): $PQ:y=-\frac{{3}}{{4}}x+\frac{{5}}{{4}}$. So $x=3\Rightarrow y=-\frac{{3}}{{4}}(3)+"
       r"\frac{5}{4}=-1$ so $PQ$ is the diameter of the circle. Notes: Completes proof by showing that $(3,-1)$ lies on "
       r"$PQ$ and gives a correct conclusion.",
       rf"{Q9A2} — M1 (AO 1.1b): $PQ=\sqrt{{(-9-15)^2+(8--10)^2}}$ $\{{=\sqrt{{900}}=30\}}$ $\textbf{{and either}}$ • "
       r"$AP=\sqrt{(3--9)^2+(-1-8)^2}$ $\{=\sqrt{225}=15\}$ • $AQ=\sqrt{(3-15)^2+(-1--10)^2}$ $\{=\sqrt{225}=15\}$. "
       r"Notes: Attempts to find distance $PQ$ and either one of distance $AP$ or distance $AQ$",
       rf"{Q9A2} — A1 (AO 2.1): e.g. as $PQ=2AP$, then $PQ$ is the diameter of the circle. Notes: Correctly shows "
       r"either • $PQ=2AP$, supported by $PQ=30$, $AP=15$ and gives a correct conclusion • $PQ=2AQ$, supported by "
       r"$PQ=30$, $AQ=15$ and gives a correct conclusion"],
      False, 20),
    e("09b", "9(b)", COORD, "3.2", 3, LATEX["09b"],
      [r"M1 (AO 1.1b): Uses Pythagoras in a correct method to find either the radius or diameter of the circle. Notes: "
       r"Either • uses Pythagoras correctly in order to find the $\textbf{radius}$. Must clearly be identified as the "
       r"$\textbf{radius}$. E.g. $r^2=(-9-3)^2+(8+1)^2$ or $r=\sqrt{(-9-3)^2+(8+1)^2}$ or $r^2=(15-3)^2+(-10+1)^2$ or "
       r"$r=\sqrt{(15-3)^2+(-10+1)^2}$ or • uses Pythagoras correctly in order to find the $\textbf{diameter}$. Must "
       r"clearly be identified as the $\textbf{diameter}$. E.g. $d^2=(15+9)^2+(-10-8)^2$ or "
       r"$d=\sqrt{(15+9)^2+(-10-8)^2}$ Note: This mark can be implied by just 30 clearly seen as the "
       r"$\textbf{diameter}$ or 15 clearly seen as the $\textbf{radius}$ (may be seen or implied in their circle "
       r"equation)",
       r"M1 (AO 1.1b): $(x-3)^2+(y+1)^2=225$ $\left(\text{or }(15)^2\right)$. Notes: Writes down a circle equation in "
       r"the form $(x\pm\text{“}3\text{”})^2+(y\pm\text{“}-1\text{”})^2=(\text{their }r)^2$",
       r"A1 (AO 1.1b): $(x-3)^2+(y+1)^2=225$ $\left(\text{or }(15)^2\right)$. Notes: $(x-3)^2+(y+1)^2=225$ or "
       r"$(x-3)^2+(y+1)^2=15^2$ or $x^2-6x+y^2+2y-215=0$"],
      False, 20),
    e("09c", "9(c)", COORD, "3.2", 2, LATEX["09c"],
      [r"M1 (AO 3.1a): Distance $=\sqrt{(\text{“}15\text{”})^2-(10)^2}$ or $=\frac{1}{2}\sqrt{(2(\text{“}15\text{”}))^2"
       r"-(2(10))^2}$. Notes: Attempts to solve the problem by using the circle property “the perpendicular from the "
       r"centre to a chord bisects the chord” and so applies Pythagoras to write down an expression of the form "
       r"$\sqrt{(\text{their “}15\text{”})^2-(10)^2}$.",
       r"A1 (AO 1.1b): $\left\{=\sqrt{125}\right\}=5\sqrt{5}$. Notes: $5\sqrt{5}$ by correct solution only"],
      False, 20),
    e("09d", "9(d)", COORD, "3.2", 2, LATEX["09d"],
      [r"M1 (AO 3.1a): $\sin(A\hat{R}Q)=\frac{20}{2(\text{“}15\text{”})}$ or $A\hat{R}Q=90-\cos^{-1}\left(\frac{10}"
       r"{\text{“}15\text{”}}\right)$. Notes: Attempts to solve the problem by e.g. using the circle property “the angle "
       r"in a semi-circle is a right angle” and writes down either $\sin(A\hat{R}Q)=\frac{20}{2(\text{their “}15"
       r"\text{”})}$ or $A\hat{R}Q=90-\cos^{-1}\left(\frac{10}{\text{their “}15\text{”}}\right)$ Note: Also allow "
       r"$\cos(A\hat{R}Q)=\frac{15^2+\left(2\left(5\sqrt{5}\right)\right)^2-15^2}{2(15)\left(2\left(5\sqrt{5}\right)"
       r"\right)}$ $\left\{=\frac{\sqrt{5}}{3}\right\}$",
       r"A1 (AO 1.1b): $A\hat{R}Q=41.8103\ldots=41.8^\circ$ (to 0.1 of a degree). Notes: 41.8 by correct solution only"],
      False, 20),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", COORD, "3.3", 1, LATEX["10a"],
      [r"B1 (AO 2.2a): $x>\ln\left(\frac{4}{3}\right)$. Notes: Uses $x=\ln(t+2)$ with $t>-\frac{2}{3}$ to deduce the "
       r"correct domain, $x>\ln\left(\frac{4}{3}\right)$"],
      True, 22),
    e("10b", "10(b)", INT, "8.5, 8.6, 3.3", 8, LATEX["10b"],
      [r"M1 (AO 3.1a): Attempts to apply $\int y\frac{\mathrm{d}x}{\mathrm{d}t}\,\mathrm{d}t$. Notes: Attempts to solve "
       r"the problem by either • a parametric process or • a Cartesian process with a substitution of either "
       r"$u=\mathrm{e}^x-1$ or $v=\mathrm{e}^x$",
       r"A1 (AO 1.1b): $\left\{\int y\frac{\mathrm{d}x}{\mathrm{d}t}\,\mathrm{d}t=\right\}=\int\left(\frac{1}{t+1}"
       r"\right)\left(\frac{1}{t+2}\right)\mathrm{d}t$. Notes: Obtains • $\int\left(\frac{1}{t+1}\right)\left("
       r"\frac{1}{t+2}\right)\mathrm{d}t$ from a parametric approach • $\int\left(\frac{1}{u}\right)\left("
       r"\frac{1}{u+1}\right)\mathrm{d}u$ from a Cartesian approach with $u=\mathrm{e}^x-1$ • $\int\left("
       r"\frac{1}{v-1}\right)\left(\frac{1}{v}\right)\mathrm{d}v$ from a Cartesian approach with $v=\mathrm{e}^x$",
       r"M1 (AO 3.1a): $\frac{1}{(t+1)(t+2)}\equiv\frac{A}{(t+1)}+\frac{B}{(t+2)}\Rightarrow1\equiv A(t+2)+B(t+1)$. "
       r"Notes: Applies a strategy of attempting to express either $\frac{1}{(t+1)(t+2)}$, $\frac{1}{u(u+1)}$ or "
       r"$\frac{1}{(v-1)v}$ as partial fractions",
       r"A1 (AO 1.1b): $\{A=1,B=-1\Rightarrow\}$ gives $\frac{1}{(t+1)}-\frac{1}{(t+2)}$. Notes: Correct partial "
       r"fractions for their method",
       r"M1 (AO 1.1b): $\left\{\int\left(\frac{1}{(t+1)}-\frac{1}{(t+2)}\right)\mathrm{d}t=\right\}\ln(t+1)-\ln(t+2)$. "
       r"Notes: Integrates to give either • $\pm\alpha\ln(t+1)\pm\beta\ln(t+2)$ • $\pm\alpha\ln u\pm\beta\ln(u+1)$; "
       r"$\alpha,\beta\neq0$, where $u=\mathrm{e}^x-1$ • $\pm\alpha\ln(v-1)\pm\beta\ln v$; $\alpha,\beta\neq0$, where "
       r"$v=\mathrm{e}^x$",
       r"A1 (AO 1.1b): $\ln(t+1)-\ln(t+2)$. Notes: Correct integration for their method",
       r"M1 (AO 2.2a): Area$(R)=[\ln(t+1)-\ln(t+2)]_0^2$ " + AREA + r". Notes: Either • Parametric approach: Deduces "
       r"and applies limits of 2 and 0 in $t$ and subtracts the correct way round • Cartesian approach: Deduces and "
       r"applies limits of 3 and 1 in $u$, where $u=\mathrm{e}^x-1$, and subtracts the correct way round • Cartesian "
       r"approach: Deduces and applies limits of 4 and 2 in $v$, where $v=\mathrm{e}^x$, and subtracts the correct way "
       r"round",
       r"A1* (AO 2.1): " + SHOW32,
       rf"{Q10A1} — M1 (AO 3.1a): Attempts to apply $\int y\,\mathrm{{d}}x=\int\frac{{1}}{{\mathrm{{e}}^x-2+1}}\,"
       r"\mathrm{d}x=\int\frac{1}{\mathrm{e}^x-1}\,\mathrm{d}x$, with a substitution of $u=\mathrm{e}^x-1$",
       rf"{Q10A1} — A1 (AO 1.1b): $\left\{{\int y\,\mathrm{{d}}x\right\}}=\int\left(\frac{{1}}{{u}}\right)\left("
       r"\frac{1}{u+1}\right)\mathrm{d}u$",
       rf"{Q10A1} — M1 (AO 3.1a): $\frac{{1}}{{u(u+1)}}\equiv\frac{{A}}{{u}}+\frac{{B}}{{(u+1)}}\Rightarrow1\equiv "
       r"A(u+1)+Bu$",
       rf"{Q10A1} — A1 (AO 1.1b): $\{{A=1,B=-1\Rightarrow\}}$ gives $\frac{{1}}{{u}}-\frac{{1}}{{(u+1)}}$",
       rf"{Q10A1} — M1 (AO 1.1b): $\left\{{\int\left(\frac{{1}}{{u}}-\frac{{1}}{{(u+1)}}\right)\mathrm{{d}}u="
       r"\right\}\ln u-\ln(u+1)$",
       rf"{Q10A1} — A1 (AO 1.1b): $\ln u-\ln(u+1)$",
       rf"{Q10A1} — M1 (AO 2.2a): Area$(R)=[\ln u-\ln(u+1)]_1^3$ " + AREA,
       rf"{Q10A1} — A1* (AO 2.1): $=\ln\left(\frac{{3}}{{2}}\right)$ *",
       rf"{Q10A2} — M1 (AO 3.1a): Attempts to apply $\int y\,\mathrm{{d}}x=\int\frac{{1}}{{\mathrm{{e}}^x-2+1}}\,"
       r"\mathrm{d}x=\int\frac{1}{\mathrm{e}^x-1}\,\mathrm{d}x$, with a substitution of $v=\mathrm{e}^x$",
       rf"{Q10A2} — A1 (AO 1.1b): $\left\{{\int y\,\mathrm{{d}}x\right\}}=\int\left(\frac{{1}}{{v-1}}\right)\left("
       r"\frac{1}{v}\right)\mathrm{d}v$",
       rf"{Q10A2} — M1 (AO 3.1a): $\frac{{1}}{{(v-1)v}}\equiv\frac{{A}}{{(v-1)}}+\frac{{B}}{{v}}\Rightarrow1\equiv "
       r"Av+B(v-1)$",
       rf"{Q10A2} — A1 (AO 1.1b): $\{{A=1,B=-1\Rightarrow\}}$ gives $\frac{{1}}{{(v-1)}}-\frac{{1}}{{v}}$",
       rf"{Q10A2} — M1 (AO 1.1b): $\left\{{\int\left(\frac{{1}}{{(v-1)}}-\frac{{1}}{{v}}\right)\mathrm{{d}}v="
       r"\right\}\ln(v-1)-\ln v$",
       rf"{Q10A2} — A1 (AO 1.1b): $\ln(v-1)-\ln v$",
       rf"{Q10A2} — M1 (AO 2.2a): Area$(R)=[\ln(v-1)-\ln v]_2^4$ " + AREA,
       rf"{Q10A2} — A1* (AO 2.1): $=\ln\left(\frac{{3}}{{2}}\right)$ *"],
      True, 22),

    # ---------------- Q11 ----------------
    e("11", "11", SEQ, "4.4", 5, LATEX["11"],
      [r"M1 (AO 2.1): Arithmetic sequence, $T_2=2k$, $T_3=5k-10$, $T_4=7k-14$ $(5k-10)-(2k)=(7k-14)-(5k-10)"
       r"\Rightarrow k=\ldots$ Notes: Complete method to find the value of $k$",
       r"A1 (AO 1.1b): $\{3k-10=2k-4\Rightarrow\}$ $k=6$. Notes: Uses a correct method to find $k=6$",
       r"M1 (AO 2.2a): $\{k=6\Rightarrow\}$ $T_2=12$, $T_3=20$, $T_4=28$. So $d=8$, $a=4$. Notes: Uses their value of "
       r"$k$ to deduce the common difference and the first term $(\neq T_2)$ of the arithmetic series.",
       r"M1 (AO 1.1b): $S_n=\frac{n}{2}\left(2(4)+(n-1)(8)\right)$. Notes: Applies $S_n=\frac{n}{2}\left(2a+(n-1)d"
       r"\right)$ with their $a\neq T_2$ and their $d$.",
       r"A1 (AO 2.1): $=\frac{n}{2}(8+8n-8)=4n^2=(2n)^2$ which is a square number. Notes: Correctly shows that the sum "
       r"of the series is $(2n)^2$ and makes an appropriate conclusion."],
      False, 24),

    # ---------------- Q12 ----------------
    e("12", "12", DIFF, "7.5, 5.3", 7, LATEX["12"],
      [rf"M1 (AO 3.1a): Complete process to find at least one set of coordinates for $P$. The process must include "
       rf"evidence of • differentiating • setting ${DY}=0$ to find $x=\ldots$ • substituting $x=\ldots$ into "
       r"$\sin x+\cos y=0.5$ to find $y=\ldots$ Notes: See scheme",
       rf"B1 (AO 1.1b): [a braced expression printed as overlapping, crossed-out symbols] $\cos x-\sin y{DY}=0$. "
       rf"Notes: Correct differentiated equation. E.g. $\cos x-\sin y{DY}=0$",
       rf"M1 (AO 2.2a): Applies ${DY}=0$ (e.g. $\cos x=0$ or $\frac{{\cos x}}{{\sin y}}=0\Rightarrow\cos x=0$) "
       rf"$\Rightarrow x=\ldots$ Notes: Uses the information “the tangent to $C$ at the point $P$ is parallel to the "
       rf"$x$-axis” to deduce and apply ${DY}=0$ and finds $x=\ldots$",
       r"A1 (AO 1.1b): giving at least one of either $x=-\frac{\pi}{2}$ or $x=\frac{\pi}{2}$. Notes: See scheme",
       rf"M1 (AO 1.1b): $x=\frac{{\pi}}{{2}}\Rightarrow\sin\left(\frac{{\pi}}{{2}}\right)+\cos y=0.5\Rightarrow\cos y="
       rf"-\frac{{1}}{{2}}\Rightarrow y=\frac{{2\pi}}{{3}}$ or $-\frac{{2\pi}}{{3}}$. Notes: For substituting one of "
       rf"their values from ${DY}=0$ into $\sin x+\cos y=0.5$ and so finds $x=\ldots$, $y=\ldots$",
       rf"A1 (AO 1.1b): So in specified range, $(x, y)=\left(\frac{{\pi}}{{2}},\frac{{2\pi}}{{3}}\right)$ and "
       rf"$\left(\frac{{\pi}}{{2}},-\frac{{2\pi}}{{3}}\right)$, by cso. Notes: Selects coordinates for $P$ on $C$ "
       rf"satisfying ${DY}=0$ and $-\frac{{\pi}}{{2}}\leqslant x<\frac{{3\pi}}{{2}}$, $-\pi<y<\pi$ i.e. finds "
       r"$\left(\frac{\pi}{2},\frac{2\pi}{3}\right)$ and $\left(\frac{\pi}{2},-\frac{2\pi}{3}\right)$ and no other "
       r"points by correct solution only",
       r"B1 (AO 2.1): $x=-\frac{\pi}{2}\Rightarrow\sin\left(-\frac{\pi}{2}\right)+\cos y=0.5\Rightarrow\cos y=1.5$ has "
       r"no solutions, and so there are exactly 2 possible points $P$. Notes: Complete argument to show that there are "
       r"exactly 2 possible points $P$."],
      False, 26),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", TRIG, "5.8, 5.6", 5, LATEX["13a"],
      [r"M1 (AO 1.2): $\mathrm{cosec}\,2x+\cot2x\equiv\cot x$, $x\neq90n^\circ$, $n\in\square$ [sic: the question paper "
       r"has $n\in\mathbb{Z}$] $\mathrm{cosec}\,2x+\cot2x=\frac{1}{\sin2x}+\frac{\cos2x}{\sin2x}$. Notes: Writes "
       r"$\mathrm{cosec}\,2x=\frac{1}{\sin2x}$ and $\cot2x=\frac{\cos2x}{\sin2x}$",
       r"M1 (AO 1.1b): $=\frac{1+\cos2x}{\sin2x}$. Notes: Combines into a single fraction with a common denominator",
       r"M1 (AO 2.1): $=\frac{1+2\cos^2x-1}{2\sin x\cos x}=\frac{2\cos^2x}{2\sin x\cos x}$. Notes: Applies "
       r"$\sin2x=2\sin x\cos x$ to the denominator $\textbf{and}$ applies either • $\cos2x=2\cos^2x-1$ • "
       r"$\cos2x=1-2\sin^2x$ and $\sin^2x+\cos^2x=1$ • $\cos2x=\cos^2x-\sin^2x$ and $\sin^2x+\cos^2x=1$ to the "
       r"numerator and manipulates to give a one term numerator expression",
       r"A1 (AO 1.1b): $=\frac{2\cos^2x}{2\sin x\cos x}$. Notes: Correct algebra leading to "
       r"$\frac{2\cos^2x}{2\sin x\cos x}$ or equivalent.",
       r"A1* (AO 2.1): $=\frac{\cos x}{\sin x}=\cot x$ *. Notes: Correct proof with correct notation and no errors seen "
       r"in working"],
      False, 28),
    e("13b", "13(b)", TRIG, "5.7, 5.4", 5, LATEX["13b"],
      [r"M1 (AO 2.2a): $\mathrm{cosec}(4\theta+10^\circ)+\cot(4\theta+10^\circ)=\sqrt{3}$; $0\leqslant\theta<180^\circ$, "
       r"$\cot(2\theta\pm\ldots^\circ)=\sqrt{3}$. Notes: Uses the result in part (a) in an attempt to deduce either "
       r"$2x=4\theta+10$ or $x=2\theta+\ldots$ and uses $x=2\theta+\ldots$ to write down or imply "
       r"$\cot(2\theta\pm\ldots^\circ)=\sqrt{3}$",
       r"M1 (AO 1.1b): $2\theta\pm\ldots=30^\circ\Rightarrow\theta=12.5^\circ$. Notes: Applies "
       r"$\mathrm{arccot}\left(\sqrt{3}\right)=30^\circ$ or $\arctan\left(\frac{1}{\sqrt{3}}\right)=30^\circ$ and "
       r"attempts to solve $2\theta\pm\ldots=30^\circ$ to give $\theta=\ldots$",
       r"A1 (AO 1.1b): $\theta=12.5^\circ$. Notes: Uses a correct method to obtain $\theta=12.5^\circ$",
       r"M1 (AO 2.1): $2\theta+5^\circ=180^\circ+PV^\circ\Rightarrow\theta=\ldots^\circ$. Notes: Uses "
       r"$2\theta+5=180+$ their $PV^\circ$ in a complete method to find the second solution, $\theta=\ldots$",
       r"A1 (AO 1.1b): $\theta=102.5^\circ$. Notes: Uses a correct method to obtain $\theta=102.5^\circ$, with no extra "
       r"solutions given either inside or outside the required range $0\leqslant\theta<180^\circ$"],
      False, 28),

    # ---------------- Q14 ----------------
    e("14i", "14(i)", PROOF, "1.1, 6.1", 2, LATEX["14i"],
      [r"M1 (AO 2.3): For an explanation or statement to show when the claim $3^x\geqslant2^x$ fails This could be "
       r"e.g. • when $x=-1$, $\frac{1}{3}<\frac{1}{2}$ or $\frac{1}{3}$ is not greater than or equal to $\frac{1}{2}$ • "
       r"when $x<0$, $3^x<2^x$ or $3^x$ is not greater than or equal to $2^x$. Notes: See scheme",
       r"A1 (AO 2.4): followed by an explanation or statement to show when the claim $3^x\geqslant2^x$ is true. This "
       r"could be e.g. • $x=2$, $9\geqslant4$ or 9 is greater than or equal to 4 • when $x\geqslant0$, "
       r"$3^x\geqslant2^x$ and a correct conclusion. E.g. • so the claim $3^x\geqslant2^x$ is sometimes true. Notes: "
       r"See scheme"],
      False, 30),
    e("14ii", "14(ii)", PROOF, "1.1", 6, LATEX["14ii"],
      [r"M1 (AO 2.1): Assume that $\sqrt{3}$ is a rational number So $\sqrt{3}=\frac{p}{q}$, where $p$ and $q$ "
       r"integers, $q\neq0$, and the HCF of $p$ and $q$ is 1. Notes: Uses a method of proof by contradiction by "
       r"initially assuming that $\sqrt{3}$ is rational and expresses $\sqrt{3}$ in the form $\frac{p}{q}$, where $p$ "
       r"and $q$ are correctly defined.",
       r"M1 (AO 1.1b): $\Rightarrow p=\sqrt{3}q\Rightarrow p^2=3q^2$. Notes: Writes $\sqrt{3}=\frac{p}{q}$ and "
       r"rearranges to make $p^2$ the subject",
       r"A1 (AO 2.2a): $\Rightarrow p^2$ is divisible by 3 and so $p$ is divisible by 3. Notes: Uses a logical "
       r"argument to prove that $p$ is divisible by 3",
       r"M1 (AO 2.1): So $p=3c$, where $c$ is an integer From earlier, $p^2=3q^2\Rightarrow(3c)^2=3q^2$. Notes: Uses "
       r"the result that $p$ is divisible by 3, (to construct the initial stage of proving that $q$ is also divisible "
       r"by 3), by substituting $p=3c$ into their expression for $p^2$",
       r"A1 (AO 1.1b): $\Rightarrow q^2=3c^2\Rightarrow q^2$ is divisible by 3 and so $q$ is divisible by 3. Notes: "
       r"Hence uses a correct argument, in the same way as before, to deduce that $q$ is also divisible by 3",
       r"A1 (AO 2.4): As both $p$ and $q$ are both divisible by 3 then the HCF of $p$ and $q$ is not 1 This "
       r"contradiction implies that $\sqrt{3}$ is an irrational number. Notes: Completes the argument (as detailed on "
       r"the scheme) that $\sqrt{3}$ is irrational. Note: All the previous 5 marks need to be scored in order to "
       r"obtain the final A mark."],
      False, 30),
]

# No examiner report is published for the specimen paper, so there is nothing to apply.
W = None
REPORT = {}

# No report, so no difficulty can be judged: every part is (None, None).
RATINGS = {q: (None, None) for q in
           ["01", "02a", "02b", "03a", "03b", "03c", "04a", "04b", "04c", "05", "06a", "06b", "06c", "06d", "07a",
            "07b", "07c", "07d", "07e", "08a", "08b", "09a", "09b", "09c", "09d", "10a", "10b", "11", "12", "13a",
            "13b", "14i", "14ii"]}


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
