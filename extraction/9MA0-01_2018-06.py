"""Draft builder for 9MA0-01 2018-06 (A level Pure Paper 1, June 2018).

Run (from the project root, with the venv active):
    python extraction/9MA0-01_2018-06.py        # writes out/drafts/9MA0-01_2018-06.json
then save with:
    python scripts/add_entries.py out/drafts/9MA0-01_2018-06.json

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

P, S = "9MA0-01", "2018-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "12a"); label as printed (e.g. "12(a)")."""
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


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


DY = r"\frac{\mathrm{d}y}{\mathrm{d}x}"
D2Y = r"\frac{\mathrm{d}^2y}{\mathrm{d}x^2}"
DT = r"\frac{\mathrm{d}y}{\mathrm{d}\theta}"

# question_latex per entry: shared stem, then earlier parts this part depends on, then the part.
Q2 = ["A curve $C$ has equation", r"$$y=x^2-2x-24\sqrt{x},\qquad x>0$$"]
Q2B = "Verify that $C$ has a stationary point when $x=4$"
Q4 = [r"The curve with equation $y=2\ln(8-x)$ meets the line $y=x$ at a single point, $x=\alpha$."]
Q6 = [r"[Figure 3: the circle $C$ with centre $A$ in the first quadrant; the straight line $l$ with positive gradient, "
      r"crossing the $y$-axis just above $O$ and touching $C$ at the point $P$ on the upper left of the circle; marked "
      r"“Not to scale”.]",
      "The circle $C$ has centre $A$ with coordinates $(7, 5)$.",
      "The line $l$, with equation $y=2x+1$, is the tangent to $C$ at the point $P$, as shown in Figure 3."]
Q6A = "Show that an equation of the line $PA$ is $2y+x=17$"
Q8 = ["The depth of water, $D$ metres, in a harbour on a particular day is modelled by the formula",
      r"$$D=5+2\sin(30t)^\circ\qquad0\leqslant t<24$$", "where $t$ is the number of hours after midnight.",
      "A boat enters the harbour at 6:30 am and it takes 2 hours to load its cargo.",
      "The boat requires the depth of water to be at least 3.8 metres before it can leave the harbour."]
Q9 = [r"[Figure 4: axes with $x$ pointing East and $y$ pointing North, origin $O$; a closed oval curve around $O$, tilted "
      r"upwards to the right; $P$ is its furthest west point, just below the $x$-axis, and $Q$ its furthest east point, "
      r"just above the $x$-axis; dashed vertical lines pass through $P$ and $Q$.]",
      "Figure 4 shows a sketch of the curve with equation $x^2-2xy+3y^2=50$"]
Q9A = rf"Show that ${DY}=\frac{{y-x}}{{3y-x}}$"
Q9M = ["The curve is used to model the shape of a cycle track with both $x$ and $y$ measured in km.",
       "The points $P$ and $Q$ represent points that are furthest west and furthest east of the origin $O$, as shown in "
       "Figure 4."]
Q10 = ["The height above ground, $H$ metres, of a passenger on a roller coaster can be modelled by the differential "
       "equation", r"$$\frac{\mathrm{d}H}{\mathrm{d}t}=\frac{H\cos(0.25t)}{40}$$",
       "where $t$ is the time, in seconds, from the start of the ride.",
       "Given that the passenger is 5 m above the ground at the start of the ride,"]
Q10A = r"show that $H=5\mathrm{e}^{0.1\sin(0.25t)}$"
Q11A = r"Use binomial expansions to show that $\sqrt{\frac{1+4x}{1-x}}\approx1+\frac{5}{2}x-\frac{5}{8}x^2$"
Q11S = (r"A student substitutes $x=\frac{1}{2}$ into both sides of the approximation shown in part (a) in an attempt to "
        r"find an approximation to $\sqrt{6}$")
Q12 = ["The value, £$V$, of a vintage car $t$ years after it was first valued on 1st January 2001, is modelled by the "
       "equation", r"$$V=Ap^t\qquad\text{where }A\text{ and }p\text{ are constants}$$",
       "Given that the value of the car was £32 000 on 1st January 2005 and £50 000 on 1st January 2012"]
Q12A = ["(i) find $p$ to 4 decimal places,", "(ii) show that $A$ is approximately 24 800"]
Q14 = ["A curve $C$ has parametric equations", r"$$x=3+2\sin t,\qquad y=4+2\cos2t,\qquad0\leqslant t<2\pi$$"]
Q14A = "Show that all points on $C$ satisfy $y=6-(x-3)^2$"

LATEX = {
    "01": L("Given that $\\theta$ is small and is measured in radians, use the small angle approximations to find an "
            "approximate value of", r"$$\frac{1-\cos4\theta}{2\theta\sin3\theta}$$"),
    "02a": L(*Q2, rf"Find (i) ${DY}$", rf"(ii) ${D2Y}$"),
    "02b": L(*Q2, Q2B),
    "02c": L(*Q2, "(b) " + Q2B, "(c) Determine the nature of this stationary point, giving a reason for your answer."),
    "03": L(r"[Figure 1: a sector $AOB$ with centre $O$ on the left, the radii $OA$ and $OB$ each labelled $r$ cm, the "
            r"angle $\theta$ marked at $O$, and the arc $AB$ on the right.]",
            "Figure 1 shows a sector $AOB$ of a circle with centre $O$ and radius $r$ cm.",
            r"The angle $AOB$ is $\theta$ radians.", "The area of the sector $AOB$ is 11 cm$^2$",
            "Given that the perimeter of the sector is 4 times the length of the arc $AB$, find the exact value of $r$."),
    "04a": L(*Q4, r"Show that $3<\alpha<4$"),
    "04b": L(*Q4,
             r"[Figure 2: axes with origin $O$; the straight line $y=x$ through $O$; the curve $y=2\ln(8-x)$ decreasing "
             r"from the upper left, crossing the $y$-axis just above 4, meeting $y=x$ at a point with $x$ a little less "
             r"than 4, then falling more and more steeply to cross the $x$-axis to the right of 4; the value 4 is marked "
             r"on both axes.]",
             r"Figure 2 shows the graph of $y=2\ln(8-x)$ and the graph of $y=x$.",
             "A student uses the iteration formula", r"$$x_{n+1}=2\ln(8-x_n),\quad n\in\mathbb{N}$$",
             r"in an attempt to find an approximation for $\alpha$.", "Using the graph and starting with $x_1=4$",
             r"determine whether or not this iteration formula can be used to find an approximation for $\alpha$, "
             r"justifying your answer."),
    "05": L("Given that", r"$$y=\frac{3\sin\theta}{2\sin\theta+2\cos\theta}\qquad-\frac{\pi}{4}<\theta<\frac{3\pi}{4}$$",
            "show that", rf"$${DT}=\frac{{A}}{{1+\sin2\theta}}\qquad-\frac{{\pi}}{{4}}<\theta<\frac{{3\pi}}{{4}}$$",
            "where $A$ is a rational constant to be found."),
    "06a": L(*Q6, Q6A),
    "06b": L(*Q6, "(a) " + Q6A, "(b) Find an equation for $C$."),
    "06c": L(*Q6, r"The line with equation $y=2x+k,\quad k\neq1$ is also a tangent to $C$.",
             "Find the value of the constant $k$."),
    "07a": L(r"Given that $k\in\mathbb{Z}^+$",
             r"show that $\displaystyle\int_k^{3k}\frac{2}{(3x-k)}\,\mathrm{d}x$ is independent of $k$,"),
    "07b": L(r"Given that $k\in\mathbb{Z}^+$",
             r"show that $\displaystyle\int_k^{2k}\frac{2}{(2x-k)^2}\,\mathrm{d}x$ is inversely proportional to $k$."),
    "08a": L(*Q8, "Find the depth of the water in the harbour when the boat enters the harbour."),
    "08b": L(*Q8, "Find, to the nearest minute, the earliest time the boat can leave the harbour.",
             "(Solutions based entirely on graphical or numerical methods are not acceptable.)"),
    "09a": L(*Q9, Q9A),
    "09b": L(*Q9, "(a) " + Q9A, *Q9M, "Using part (a),", "(b) find the exact coordinates of the point $P$."),
    "09c": L(*Q9, "(a) " + Q9A, *Q9M,
             r"(c) Explain briefly how to find the coordinates of the point that is furthest north of the origin $O$. "
             r"(You $\textbf{do not}$ need to carry out this calculation)."),
    "10a": L(*Q10, Q10A),
    "10b": L(*Q10, "(a) " + Q10A, "(b) State the maximum height of the passenger above the ground."),
    "10c": L(*Q10, "(a) " + Q10A,
             "The passenger reaches the maximum height, for the second time, $T$ seconds after the start of the ride.",
             "(c) Find the value of $T$."),
    "11a": L(Q11A),
    "11b": L("(a) " + Q11A, Q11S, r"(b) Give a reason why the student $\textbf{should not}$ use $x=\frac{1}{2}$"),
    "11c": L(Q11S, r"Substitute $x=\frac{1}{11}$ into", r"$$\sqrt{\frac{1+4x}{1-x}}=1+\frac{5}{2}x-\frac{5}{8}x^2$$",
             r"to obtain an approximation to $\sqrt{6}$. Give your answer as a fraction in its simplest form."),
    "12a": L(*Q12, *Q12A),
    "12b": L(*Q12, "With reference to the model, interpret", "(i) the value of the constant $A$,",
             "(ii) the value of the constant $p$."),
    "12c": L(*Q12, "(a) " + Q12A[0], Q12A[1], "Using the model,",
             "(c) find the year during which the value of the car first exceeds £100 000"),
    "13": L("Show that", r"$$\int_0^2 2x\sqrt{x+2}\,\mathrm{d}x=\frac{32}{15}\left(2+\sqrt{2}\right)$$"),
    "14a": L(*Q14, Q14A),
    "14b": L(*Q14, "(a) " + Q14A, "(b) (i) Sketch the curve $C$.",
             r"(ii) Explain briefly why $C$ does not include all points of $y=6-(x-3)^2,\quad x\in\mathbb{R}$"),
    "14c": L(*Q14, "(a) " + Q14A,
             "The line with equation $x+y=k$, where $k$ is a constant, intersects $C$ at two distinct points.",
             "(c) State the range of values of $k$, writing your answer in set notation."),
}

TH = r"\frac{(4\theta)^2}{2}"
DH = r"\mathrm{d}H"
BY = r"\left(1+\frac{5}{2}x-\frac{5}{8}x^2\right)"
Q11ALT = "ALT: Other equally valid alternative for 11(a)"

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", TRIG, "5.2", 3, LATEX["01"],
      [rf"M1 (AO 1.1b): Attempts either $\sin3\theta\approx3\theta$ or $\cos4\theta\approx1-{TH}$ in "
       rf"$\frac{{1-\cos4\theta}}{{2\theta\sin3\theta}}$. Notes: Attempts either $\sin3\theta\approx3\theta$ or "
       rf"$\cos4\theta\approx1-{TH}$ in the given expression. See below for description of marking of $\cos4\theta$",
       rf"M1 (AO 2.1): Attempts both $\sin3\theta\approx3\theta$ and $\cos4\theta\approx1-{TH}\to"
       rf"\frac{{1-\left(1-{TH}\right)}}{{2\theta\times3\theta}}$ and attempts to simplify. Notes: Attempts to substitute "
       rf"both $\sin3\theta\approx3\theta$ and $\cos4\theta\approx1-{TH}$ $\to\frac{{1-\left(1-{TH}\right)}}"
       rf"{{2\theta\times3\theta}}$ and attempts to simplify. Condone missing bracket on the $4\theta$ so "
       rf"$\cos4\theta\approx1-\frac{{4\theta^2}}{{2}}$ would score the method Expect to see it simplified to a single term "
       rf"which could be in terms of $\theta$ Look for an answer of $k$ but condone $k\theta$ following a slip",
       rf"A1 (AO 1.1b): $=\frac{{4}}{{3}}$ oe. Notes: Uses both identities and simplifies to $\frac{{4}}{{3}}$ or exact "
       rf"equivalent with no incorrect lines BUT allow recovery on missing bracket for "
       rf"$\cos4\theta\approx1-\frac{{4\theta^2}}{{2}}$. Eg. $\frac{{1-\left(1-{TH}\right)}}{{2\theta\times3\theta}}="
       rf"\frac{{8\theta^2}}{{6\theta}}=\frac{{4}}{{3}}$ is M1 M1 A0 Condone awrt 1.33.",
       r"ALT: Alt: $\frac{1-\cos4\theta}{2\theta\sin3\theta}=\frac{1-(1-2\sin^22\theta)}{2\theta\sin3\theta}="
       r"\frac{2\sin^22\theta}{2\theta\sin3\theta}=\frac{2\times(2\theta)^2}{2\theta\times3\theta}=\frac{4}{3}$ — M1 For an "
       r"attempt at $\sin3\theta\approx3\theta$ or the identity $\cos4\theta=1-2\sin^22\theta$ with "
       r"$\sin2\theta\approx2\theta$",
       r"ALT: Alt — M1 For both of the above and attempts to simplify to a single term.",
       r"ALT: Alt — A1 $\frac{4}{3}$ oe"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", DIFF, "7.2", 3, LATEX["02a"],
      [rf"M1 (AO 1.1b): (i) ${DY}=2x-2-12x^{{-\frac{{1}}{{2}}}}$. Notes: Differentiates to "
       rf"${DY}=Ax+B+Cx^{{-\frac{{1}}{{2}}}}$",
       rf"A1 (AO 1.1b): (i) ${DY}=2x-2-12x^{{-\frac{{1}}{{2}}}}$. Notes: ${DY}=2x-2-12x^{{-\frac{{1}}{{2}}}}$ "
       rf"(Coefficients may be unsimplified)",
       rf"B1ft (AO 1.1b): (ii) ${D2Y}=2+6x^{{-\frac{{3}}{{2}}}}$. Notes: Achieves a correct ${D2Y}$ for their ${DY}$ ( Their "
       rf"${DY}$ must have a negative or fractional index)"],
      False, 4),
    e("02b", "2(b)", DIFF, "7.3", 2, LATEX["02b"],
      [rf"M1 (AO 1.1b): Substitutes $x=4$ into their ${DY}=2\times4-2-12\times4^{{-\frac{{1}}{{2}}}}=\ldots$ Notes: "
       rf"Substitutes $x=4$ into their ${DY}$ and attempts to evaluate. There must be evidence "
       rf"$\left.{DY}\right|_{{x=4}}=\ldots$",
       rf"A1 (AO 2.1): Shows ${DY}=0$ and states “hence there is a stationary point” oe. Notes: There must be a reason "
       rf"and a minimal conclusion. Allow ✓, QED for a minimal conclusion Shows ${DY}=0$ and states “hence there is a "
       rf"stationary point” oe",
       rf"ALT: Alternatively — M1 (AO 1.1b): Alternatively substitutes $x=4$ into an equation resulting from ${DY}=0$ "
       rf"Eg. $\frac{{36}}{{x}}=(x-1)^2$ and equates",
       r"ALT: Alt — A1 (AO 2.1): Shows that $x=4$ is a root of the resulting equation and states “hence there is a "
       r"stationary point” All aspects of the proof must be correct including a conclusion"],
      False, 4),
    e("02c", "2(c)", DIFF, "7.3", 2, LATEX["02c"],
      [rf"M1 (AO 1.1b): Substitutes $x=4$ into their ${D2Y}=2+6\times4^{{-\frac{{3}}{{2}}}}=(2.75)$. Notes: Substitutes "
       rf"$x=4$ into their ${D2Y}$ and calculates its value, or implies its sign by a statement such as when "
       rf"$x=4\Rightarrow{D2Y}>0$. This must be seen in (c) and not labelled (b).",
       rf"A1ft (AO 2.2a): ${D2Y}=2.75>0$ and states “hence minimum”. Notes: For a correct calculation, a valid reason "
       rf"and a correct conclusion. Ignore additional work where candidate finds ${D2Y}$ left and right of $x=4$. Follow "
       rf"through on an incorrect ${D2Y}$ but it is dependent upon having a negative or fractional index. Ignore any "
       rf"references to the word convex. The nature of the turning point is “minimum”.",
       r"ALT: Alternatively — M1 (AO 1.1b): Alternatively calculates the gradient of $C$ either side of $x=4$ or "
       r"calculates the value of $y$ either side of $x=4$.",
       r"ALT: Alternatively — A1ft (AO 2.2a): Using the gradient look for correct calculations, a valid reason…. goes "
       r"from negative to positive, and a correct conclusion …minimum."],
      False, 4),

    # ---------------- Q3 ----------------
    e("03", "3", TRIG, "5.1, 2.4", 4, LATEX["03"],
      [r"B1 (AO 1.1b): States or uses $\frac{1}{2}r^2\theta=11$. Notes: States or uses $\frac{1}{2}r^2\theta=11$ This may "
       r"be implied with an embedded found value for $\theta$",
       r"B1 (AO 1.1b): States or uses $2r+r\theta=4r\theta$. Notes: States or uses $2r+r\theta=4r\theta$ or equivalent",
       r"M1 (AO 3.1a): Attempts to solve, full method $r=\ldots$ Notes: Full method to find $r=\ldots$ This involves "
       r"combining the equations to eliminate $\theta$ or find $\theta$ The initial equations must be of the same “form” "
       r"(see **) but condone slips when attempting to solve. It cannot be scored from impossible values for $\theta$ "
       r"Hence only score if $0<\theta<2\pi$ FYI $\theta=\frac{2}{3}$ radians Allow this to be scored from equations such "
       r"as $\ldots r^2\theta=11$ and ones that simplify to $\ldots r=\ldots r\theta$ ** Allow their "
       r"$2r+r\theta=4r\theta\Rightarrow\theta=\ldots$ then substitute this into their $\frac{1}{2}r^2\theta=11$ Allow "
       r"their $2r+r\theta=4r\theta\Rightarrow r\theta=\ldots$ then substitute this into their "
       r"$\frac{1}{2}r^2\theta=11$ Allow their $\frac{1}{2}r^2\theta=11\Rightarrow\theta=\frac{\ldots}{r^2}$ then "
       r"substitute into their $2r+r\theta=4r\theta\Rightarrow r=\ldots$",
       r"A1 (AO 1.1b): $r=\sqrt{33}$. Notes: $r=\sqrt{33}$ only but isw after a correct answer.",
       r"ALT: The whole question can be attempted using $\theta$ in degrees. — B1: States or uses "
       r"$\frac{\theta}{360}\times\pi r^2=11$",
       r"ALT: The whole question can be attempted using $\theta$ in degrees. — B1: States or uses "
       r"$2r+\frac{\theta}{360}\times2\pi r=4\times\frac{\theta}{360}\times2\pi r$"],
      True, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", NUM, "9.1", 2, LATEX["04a"],
      [r"M1 (AO 2.1): Attempts $\mathrm{f}(3)=$ and $\mathrm{f}(4)=$ where $\mathrm{f}(x)=\pm(2\ln(8-x)-x)$. Notes: "
       r"Attempts $\mathrm{f}(3)=$ and $\mathrm{f}(4)=$ where $\mathrm{f}(x)=\pm(2\ln(8-x)-x)$. This is not routine and "
       r"cannot be scored by substituting 3 and 4 in both functions",
       r"A1* (AO 2.4): $\mathrm{f}(3)=(2\ln(5)-x)=(+)0.22$ and $\mathrm{f}(4)=(2\ln(4)-4)=-1.23$ Change of sign and "
       r"function continuous in interval $[3,4]\Rightarrow$ Root *. Notes: Both values (calculations) correct to at "
       r"least 1 sf with correct explanation and conclusion. (See underlined statements)",
       r"ALT: Alternatively — M1 (AO 2.1): or alternatively compares $2\ln5$ to 3 and $2\ln4$ to 4.",
       r"ALT: Alternatively — A1* (AO 2.4): When comparing terms, allow reasons to be $2\ln8=3.21>3$, "
       r"$2\ln4=2.77<4$ or similar [sic: at $x=3$ the main scheme evaluates $2\ln(5)$]"],
      False, 8),
    e("04b", "4(b)", NUM, "9.2", 2, LATEX["04b"],
      [r"M1 (AO 2.4): For annotating the graph by drawing a cobweb diagram starting at $x_1=4$ It should have at least "
       r"two spirals. Notes: For an attempt at using a cobweb diagram. Look for 5 or more correct straight lines. It may "
       r"not start at 4 but it must show an understanding of the method. If there is no graph then it is M0 A0 [The mark "
       r"scheme shows the graph on a grid with a cobweb starting at $x=4$ and spiralling in towards the intersection.]",
       r"A1 (AO 2.2a): Deduces that the iteration formula can be used to find an approximation for $\alpha$ because the "
       r"cobweb spirals inwards for the cobweb diagram. Notes: For a correct attempt starting at 4 and deducing that the "
       r"iteration can be used as the iterations converge to the root. You must statement that it can be used with a "
       r"suitable reason. Suitable reasons could be “ it spirals inwards”, it gets closer to the root”, it converges ”"],
      True, 8),

    # ---------------- Q5 ----------------
    e("05", "5", DIFF, "7.4, 5.5, 5.6", 5, LATEX["05"],
      [rf"M1 (AO 1.1b): ${DT}=\frac{{(2\sin\theta+2\cos\theta)3\cos\theta-3\sin\theta(2\cos\theta-2\sin\theta)}}"
       rf"{{(2\sin\theta+2\cos\theta)^2}}$. Notes: For choosing either the quotient, product rule or implicit "
       rf"differentiation and applying it to the given function. Look for the correct form of ${DT}$ (condone it being "
       rf"stated as ${DY}$) but tolerate slips on the coefficients and also condone "
       rf"$\frac{{\mathrm{{d}}(\sin\theta)}}{{\mathrm{{d}}\theta}}=\pm\cos\theta$ and "
       rf"$\frac{{\mathrm{{d}}(\cos\theta)}}{{\mathrm{{d}}\theta}}=\pm\sin\theta$ For quotient rule look for "
       rf"${DT}=\frac{{(2\sin\theta+2\cos\theta)\times\pm\ldots\cos\theta-3\sin\theta(\pm\ldots\cos\theta\pm\ldots"
       rf"\sin\theta)}}{{(2\sin\theta+2\cos\theta)^2}}$ For product rule look for ${DT}=(2\sin\theta+2\cos\theta)^{{-1}}"
       rf"\times\pm\ldots\cos\theta\pm3\sin\theta\times(2\sin\theta+2\cos\theta)^{{-2}}\times(\pm\ldots\cos\theta\pm\ldots"
       rf"\sin\theta)$ Implicit differentiation look for $(\ldots\cos\theta\pm\ldots\sin\theta)y+(2\sin\theta+"
       rf"2\cos\theta){DT}=\ldots\cos\theta$",
       rf"A1 (AO 1.1b): ${DT}=\frac{{(2\sin\theta+2\cos\theta)3\cos\theta-3\sin\theta(2\cos\theta-2\sin\theta)}}"
       rf"{{(2\sin\theta+2\cos\theta)^2}}$. Notes: A correct expression involving ${DT}$ condoning it appearing as ${DY}$",
       rf"M1 (AO 3.1a): Expands and uses $\sin^2\theta+\cos^2\theta=1$ at least once in the numerator or the "
       rf"denominator or uses $2\sin\theta\cos\theta=\sin2\theta$ in $\Rightarrow{DT}=\frac{{\ldots}}{{\ldots C\sin\theta"
       rf"\cos\theta}}$. Notes: Expands and uses $\sin^2\theta+\cos^2\theta=1$ at least once in the numerator or the "
       rf"denominator OR uses $2\sin\theta\cos\theta=\sin2\theta$ in $\Rightarrow{DT}=\frac{{\ldots}}{{\ldots C\sin\theta"
       rf"\cos\theta}}$",
       rf"M1 (AO 2.1): Expands and uses $\sin^2\theta+\cos^2\theta=1$ the numerator and the denominator AND uses "
       rf"$2\sin\theta\cos\theta=\sin2\theta$ in $\Rightarrow{DT}=\frac{{P}}{{Q+R\sin2\theta}}$. Notes: Expands and uses "
       rf"$\sin^2\theta+\cos^2\theta=1$ in the numerator and the denominator AND uses $2\sin\theta\cos\theta=\sin2\theta$ "
       rf"in the denominator to reach an expression of the form ${DT}=\frac{{P}}{{Q+R\sin2\theta}}$ .",
       rf"A1 (AO 1.1b): $\Rightarrow{DT}=\frac{{3}}{{2+2\sin2\theta}}=\frac{{3/2}}{{1+\sin2\theta}}$. Notes: Fully "
       rf"correct proof with $A=\frac{{3}}{{2}}$ stated but allow for example $\frac{{3/2}}{{1+\sin2\theta}}$ Allow recovery "
       rf"from missing brackets. Condone notation slips. This is not a given answer"],
      False, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", COORD, "3.1", 3, LATEX["06a"],
      [r"M1 (AO 2.2a): Deduces that gradient of $PA$ is $-\frac{1}{2}$. Notes: Uses the idea of perpendicular gradients "
       r"to deduce that gradient of $PA$ is $-\frac{1}{2}$. Condone $-\frac{1}{2}x$ if followed by correct work. You may "
       r"well see the perpendicular line set up as $y=-\frac{1}{2}x+c$ which scored this mark",
       r"M1 (AO 1.1b): Finding the equation of a line with gradient “$-\frac{1}{2}$” and point $(7,5)$ "
       r"$y-5=-\frac{1}{2}(x-7)$. Notes: Award for the method of finding the equation of a line with a changed gradient "
       r"and the point $(7,5)$ So sight of $y-5=\frac{1}{2}(x-7)$ would score this mark If the form $y=mx+c$ is used "
       r"expect the candidates to proceed as far as $c=\ldots$ to score this mark.",
       r"A1* (AO 1.1b): Completes proof $2y+x=17$ *. Notes: Completes proof with no errors or omissions $2y+x=17$"],
      True, 12),
    e("06b", "6(b)", COORD, "3.2, 2.4", 4, LATEX["06b"],
      [r"M1 (AO 2.1): Solves $2y+x=17$ and $y=2x+1$ simultaneously. Notes: Awarded for an attempt at the key step of "
       r"finding the coordinates of point $P$. ie for an attempt at solving $2y+x=17$ and $y=2x+1$ simultaneously. Allow "
       r"any methods (including use of a calculator) but it must be a valid attempt to find both coordinates. Do not "
       r"allow where they start $17-x=2x+1$ as they have set $2y=y$ but condone bracketing errors, eg $2\times2x+1+x=17$",
       r"A1 (AO 1.1b): $P=(3,7)$. Notes: $P=(3,7)$",
       r"M1 (AO 1.1b): Length $PA=\sqrt{(3-7)^2+(7-5)^2}=\left(\sqrt{20}\right)$. Notes: Uses Pythagoras’ Theorem to find "
       r"the radius or radius$^2$ using their $P=(3,7)$ and $(7,5)$. There must be an attempt to find the difference "
       r"between the coordinates in the use of Pythagoras",
       r"A1 (AO 1.1b): Equation of C is $(x-7)^2+(y-5)^2=20$. Notes: $(x-7)^2+(y-5)^2=20$. Do not accept "
       r"$(x-7)^2+(y-5)^2=\left(\sqrt{20}\right)^2$"],
      True, 12),
    e("06c", "6(c)", COORD, "3.2, 2.3", 3, LATEX["06c"],
      [r"M1 (AO 3.1a): Attempts to find where $y=2x+k$ meets $C$ using $\overrightarrow{OA}+\overrightarrow{PA}$. Notes: "
       r"Attempts to find where $y=2x+k$ meets $C$. Awarded for using $\overrightarrow{OA}+\overrightarrow{PA}$. $(11,3)$ "
       r"or one correct coordinate of $(11,3)$ is evidence of this award.",
       r"M1 (AO 2.1): Substitutes their $(11,3)$ in $y=2x+k$ to find $k$. Notes: For a full method leading to $k$. Scored "
       r"for either substituting their $(11,3)$ in $y=2x+k$",
       r"A1 (AO 1.1b): $k=-19$. Notes: $k=-19$ only. Other method are possible using trigonometry.",
       r"ALT: Alternative I (second scheme table) — M1 (AO 3.1a): Attempts to find where $y=2x+k$ meets $C$ via "
       r"simultaneous equations proceeding to a 3TQ in $x$ (or $y$) FYI $5x^2+(4k-34)x+k^2-10k+54=0$. Notes: For solving "
       r"$y=2x+k$ with their $(x-7)^2+(y-5)^2=20$ and creating a quadratic eqn of the form $ax^2+bx+c=0$ where both $b$ "
       r"and $c$ are dependent upon $k$. The terms in $x^2$ and $x$ must be collected together or implied to have been "
       r"collected by their correct use in “$b^2-4ac$” FYI the correct quadratic is $5x^2+(4k-34)x+k^2-10k+54=0$",
       r"ALT: Alternative I (second scheme table) — M1 (AO 2.1): Uses $b^2-4ac=0$ oe and proceeds to $k=\ldots$ Notes: "
       r"For using the discriminant condition $b^2-4ac=0$ to find $k$. It is not dependent upon the previous M and may be "
       r"awarded from only one term in $k$. $(4k-34)^2-4\times5\times(k^2-10k+54)=0\Rightarrow k=\ldots$ Allow use of a "
       r"calculator here to find roots. Award if you see use of correct formula but it would be implied by $\pm$ correct "
       r"roots. (From the main notes: or, in the alternative, for solving their "
       r"$(4k-34)^2-4\times5\times(k^2-10k+54)=0\Rightarrow k=\ldots$)",
       r"ALT: Alternative I (second scheme table) — A1 (AO 1.1b): $k=-19$. Notes: $k=-19$ only",
       r"ALT: Alternative II — M1: For solving $2y+x=17$ with their $(x-7)^2+(y-5)^2=20$, creating a 3TQ and solving.",
       r"ALT: Alternative II — M1: For substituting their $(11,3)$ into $y=2x+k$ and finding $k$",
       r"ALT: Alternative II — A1: $k=-19$ only"],
      True, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", INT, "8.3, 8.2, 6.4", 4, LATEX["07a"],
      [r"M1 (AO 1.1a): $\int\frac{2}{(3x-k)}\,\mathrm{d}x=\frac{2}{3}\ln(3x-k)$. Notes: "
       r"$\int\frac{2}{(3x-k)}\,\mathrm{d}x=A\ln(3x-k)$ Condone a missing bracket",
       r"A1 (AO 1.1b): $\int\frac{2}{(3x-k)}\,\mathrm{d}x=\frac{2}{3}\ln(3x-k)$. Notes: "
       r"$\int\frac{2}{(3x-k)}\,\mathrm{d}x=\frac{2}{3}\ln(3x-k)$ Allow recovery from a missing bracket if in subsequent "
       r"work $A\ln9k-k\to A\ln8k$",
       r"dM1 (AO 1.1b): $\int_k^{3k}\frac{2}{(3x-k)}\,\mathrm{d}x=\frac{2}{3}\ln(9k-k)-\frac{2}{3}\ln(3k-k)$. Notes: For "
       r"substituting $k$ and $3k$ into their $A\ln(3x-k)$ and subtracting either way around",
       r"A1 (AO 2.1): $=\frac{2}{3}\ln\left(\frac{8k}{2k}\right)=\frac{2}{3}\ln4$ oe. Notes: Uses correct ln work and "
       r"notation to show that $\mathrm{I}=\frac{2}{3}\ln\left(\frac{8}{2}\right)$ or $\frac{2}{3}\ln4$ oe (ie independent "
       r"of $k$)"],
      False, 16),
    e("07b", "7(b)", INT, "8.3, 8.2", 3, LATEX["07b"],
      [r"M1 (AO 1.1b): $\int\frac{2}{(2x-k)^2}\,\mathrm{d}x=-\frac{1}{(2x-k)}$. Notes: "
       r"$\int\frac{2}{(2x-k)^2}\,\mathrm{d}x=\frac{C}{(2x-k)}$",
       r"dM1 (AO 1.1b): $\int_k^{2k}\frac{2}{(2x-k)^2}\,\mathrm{d}x=-\frac{1}{(4k-k)}+\frac{1}{(2k-k)}$. Notes: For "
       r"substituting $k$ and $2k$ into their $\frac{C}{(2x-k)}$ and subtracting",
       r"A1 (AO 2.1): $=\frac{2}{3k}\ \left(\propto\frac{1}{k}\right)$. Notes: Shows that it is inversely proportional to "
       r"$k$ Eg proceeds to the answer is of the form $\frac{A}{k}$ with $A=\frac{2}{3}$ There is no need to perform the "
       r"whole calculation. Accept from $-\frac{1}{(3k)}+\frac{1}{(k)}=\left(-\frac{1}{3}+1\right)\times\frac{1}{k}"
       r"\propto\frac{1}{k}$ If the calculation is performed it must be correct. Do not isw here. They should know when "
       r"they have an expression that is inversely proportional to $k$. You may see substitution used but the mark is "
       r"scored for the same result. See below $u=2x-k\to\left[\frac{C}{u}\right]$ for M1 with limits $3k$ and $k$ used "
       r"for dM1"],
      False, 16),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", TRIG, "5.9", 1, LATEX["08a"],
      [r"B1 (AO 3.4): $D=5+2\sin(30\times6.5)^\circ=$ awrt 4.48 m with units. Notes: Scored for using the model ie. "
       r"substituting $t=6.5$ into $D=5+2\sin(30t)^\circ$ and stating $D=$ awrt 4.48 m. The units must be seen somewhere "
       r"in (a) . So allow when $D=4.482..=4.5$ m Allow the mark for a correct answer without any working."],
      False, 20),
    e("08b", "8(b)", TRIG, "5.9, 5.7", 4, LATEX["08b"],
      [r"M1 (AO 1.1b): $3.8=5+2\sin(30t)^\circ\Rightarrow\sin(30t)^\circ=-0.6$. Notes: For using $D=3.8$ and proceeding "
       r"to $\sin(30t)^\circ=k$, $|k|\leqslant1$",
       r"A1 (AO 1.1b): $3.8=5+2\sin(30t)^\circ\Rightarrow\sin(30t)^\circ=-0.6$. Notes: $\sin(30t)^\circ=-0.6$ This may be "
       r"implied by any correct answer for $t$ such as $t=7.2$ If the A1 implied, the calculation must be performed in "
       r"degrees.",
       r"dM1 (AO 3.1a): $t=10.77$. Notes: For finding the first value of $t$ for their $\sin(30t)^\circ=k$ after $t=8.5$. "
       r"You may well see other values as well which is not an issue for this dM mark (Note that "
       r"$\sin(30t)^\circ=-0.6\Rightarrow30t=216.9^\circ$ as well but this gives $t=7.2$) For the correct "
       r"$\sin(30t)^\circ=-0.6\Rightarrow30t=323.1\Rightarrow t=$ awrt 10.8 For the incorrect "
       r"$\sin(30t)^\circ=+0.6\Rightarrow30t=396.9\Rightarrow t=$ awrt 13.2 So award this mark if you see "
       r"$30t=\text{inv}\sin\text{their}-0.6$ to give the first value of $t$ where $30t>255$",
       r"A1 (AO 3.2a): 10:46 a.m. or 10:47 a.m. Notes: Allow 10:46 a.m. (12 hour clock notation) or 10:46 (24 hour clock "
       r"notation ) oe Allow 10:47 a.m. (12 hour clock notation) or 10:47 (24 hour clock notation ) oe DO NOT allow 646 "
       r"minutes or 10 hours 46 minutes."],
      False, 20),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", DIFF, "7.5", 4, LATEX["09a"],
      [rf"M1 (AO 2.1): Either $3y^2\to Ay{DY}$ or $2xy\to2x{DY}+2y$. Notes: For selecting the appropriate method of "
       rf"differentiating either $3y^2\to Ay{DY}$ or $2xy\to2x{DY}+2y$ It may be quite difficult awarding it for the "
       rf"product rule but condone $-2xy\to-2x{DY}+2y$ unless you see evidence that they have used the incorrect law "
       rf"$vu'-uv'$",
       rf"A1 (AO 1.1b): $2x-2x{DY}-2y+6y{DY}=0$. Notes: Fully correct derivative $2x-2x{DY}-2y+6y{DY}=0$ Allow attempts "
       rf"where candidates write $2x\mathrm{{d}}x-2x\mathrm{{d}}y-2y\mathrm{{d}}x+6y\mathrm{{d}}y=0$ but watch for students "
       rf"who write ${DY}=2x-2x{DY}-2y+6y{DY}$ This, on its own, is A0 unless you are convinced that this is just their "
       rf"notation. Eg ${DY}=2x-2x{DY}-2y+6y{DY}=0$",
       rf"M1 (AO 2.1): $(6y-2x){DY}=2y-2x$. Notes: For a valid attempt at making ${DY}$ the subject. with two terms in "
       rf"${DY}$ coming from $3y^2$ and $2xy$ Look for $(\ldots\pm\ldots){DY}=\ldots\ldots$ It is implied by "
       rf"${DY}=\frac{{2y-2x}}{{6y-2x}}$ This cannot be scored from attempts such as ${DY}=2x-2x{DY}-2y+6y$ which only has "
       rf"one correct term.",
       rf"A1* (AO 1.1b): ${DY}=\frac{{2y-2x}}{{6y-2x}}=\frac{{y-x}}{{3y-x}}$ *. Notes: ${DY}=\frac{{y-x}}{{3y-x}}$ with no "
       rf"errors or omissions. The previous line ${DY}=\frac{{2y-2x}}{{6y-2x}}$ or equivalent must be seen."],
      True, 22),
    e("09b", "9(b)", DIFF, "7.5, 7.3, 2.4", 5, LATEX["09b"],
      [rf"M1 (AO 2.2a): $\left(\text{{At }}P\text{{ and }}Q\ {DY}\to\infty\Rightarrow\right)$ Deduces that $3y-x=0$. Notes: "
       rf"Deduces that $3y-x=0$ oe",
       r"M1 (AO 3.1a): Solves $y=\frac{1}{3}x$ and $x^2-2xy+3y^2=50$ simultaneously. Notes: Attempts to find either the "
       r"$x$ or $y$ coordinates of $P$ and $Q$ by solving their $y=\frac{1}{3}x$ with $x^2-2xy+3y^2=50$ simultaneously. "
       r"Allow for finding a quadratic equation in $x$ or $y$ and solving to find at least one value for $x$ or $y$. This "
       r"may be awarded when candidates make the numerator $=0$ ie using $y=x$",
       r"A1 (AO 1.1b): $\Rightarrow x=(\pm)5\sqrt{3}$ OR $\Rightarrow y=(\pm)\frac{5}{3}\sqrt{3}$. Notes: "
       r"$\Rightarrow x=(\pm)5\sqrt{3}$ OR $\Rightarrow y=(\pm)\frac{5}{3}\sqrt{3}$",
       r"dM1 (AO 1.1b): Using $y=\frac{1}{3}x\Rightarrow x=\ldots$ AND $y=\ldots$ Notes: Dependent upon the previous M, it "
       r"is for finding the $y$ coordinate from their $x$ (or vice versa) This may also be scored following the numerator "
       r"being set to 0 ie using $y=x$",
       r"A1 (AO 2.2a): $P=\left(-5\sqrt{3},-\frac{5}{3}\sqrt{3}\right)$. Notes: Deduces that "
       r"$P=\left(-5\sqrt{3},-\frac{5}{3}\sqrt{3}\right)$ OE. Allow to be $x=\ldots$ $y=\ldots$"],
      True, 22),
    e("09c", "9(c)", DIFF, "7.5, 7.3", 1, LATEX["09c"],
      [rf"B1ft (AO 2.4): Explains that you need to solve $y=x$ and $x^2-2xy+3y^2=50$ simultaneously and choose the "
       rf"positive solution. Notes: Explains that this is where ${DY}=0$ and so you need to solve $y=x$ and "
       rf"$x^2-2xy+3y^2=50$ simultaneously and choose the positive solution (or larger solution). Allow a follow through "
       rf"for candidates who mix up parts (b) and (c)",
       r"ALT: Alternatively — B1ft (AO 2.4): Alternatively candidates could complete the square $(x-y)^2+2y^2=50$ and "
       r"state that $y$ would reach a maximum value when $x=y$ and choose the positive solution from $2y^2=50$"],
      True, 22),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", INT, "8.7, 7.6", 5, LATEX["10a"],
      [rf"M1 (AO 3.1a): $\frac{{{DH}}}{{\mathrm{{d}}t}}=\frac{{H\cos0.25t}}{{40}}\Rightarrow\int\frac{{1}}{{H}}\,{DH}="
       rf"\int\frac{{\cos0.25t}}{{40}}\,\mathrm{{d}}t$. Notes: Separates the variables to reach $\int\frac{{1}}{{H}}\,{DH}="
       rf"\int\frac{{\cos0.25t}}{{40}}\,\mathrm{{d}}t$ or equivalent. The integral signs need to be present on both sides "
       rf"and the ${DH}$ AND $\mathrm{{d}}t$ need to be in the correct positions.",
       r"M1 (AO 1.1b): $\ln H=\frac{1}{10}\sin0.25t\ (+c)$. Notes: Integrates both sides to reach $\ln H=A\sin0.25t$ or "
       r"equivalent with or without the $+c$",
       r"A1 (AO 1.1b): $\ln H=\frac{1}{10}\sin0.25t\ (+c)$. Notes: $\ln H=\frac{1}{10}\sin0.25t+c$ or equivalent with or "
       r"without the $+c$. Allow two constants, one either side If the 40 was on the lhs look for "
       r"$40\ln H=4\sin0.25t+c$ or equivalent.",
       r"dM1 (AO 3.4): Substitutes $t=0,H=5\Rightarrow c=\ln(5)$. Notes: Substitutes $t=0,H=5\Rightarrow c=\ldots$ There "
       r"needs to have been a single “$+c$” to find. It is dependent upon the previous M mark. You may allow even if you "
       r"don’t explicitly see “$t=0,H=5$” as it may be implied from their previous line If the candidate has attempted to "
       r"change the subject and made an error/ slip then condone it for this M but not the final A. Eg. "
       r"$40\ln H=4\sin0.25t+c\Rightarrow H^{40}=\mathrm{e}^{4\sin0.25t}+\mathrm{e}^c\Rightarrow5^{40}=1+\mathrm{e}^c"
       r"\Rightarrow c=\ldots$ Also many students will be attempting to get to the given answer so condone the method of "
       r"finding c =... These students will lose the A1* mark",
       r"A1* (AO 2.1): $\ln\left(\frac{H}{5}\right)=\frac{1}{10}\sin0.25t\Rightarrow H=5\mathrm{e}^{0.1\sin0.25t}$ *. "
       r"Notes: Proceeds via $\ln H=\frac{1}{10}\sin0.25t+\ln5$ or equivalent to the given answer "
       r"$H=5\mathrm{e}^{0.1\sin0.25t}$ with at least one correct intermediate line and no incorrect work. DO NOT condone "
       r"$c$’s going to $c$’s when they should be $\mathrm{e}^c$ or $A$ Accept as a minimum "
       r"$\ln H=\frac{1}{10}\sin0.25t+\ln5\Rightarrow H=\mathrm{e}^{\frac{1}{10}\sin0.25t+\ln5}$ or "
       r"$H=\mathrm{e}^{\frac{1}{10}\sin0.25t}\times\mathrm{e}^{+\ln5}$ before sight of the given answer If the only error "
       r"was to omit the integration signs on line 1, thus losing the first M1, allow the candidate to have access to "
       r"this mark following a correct intermediate line (see above). If they attempt to change the subject first then "
       r"the constant of integration must have been adapted if the A1* is to be awarded. "
       r"$\ln H=\frac{1}{10}\sin0.25t+c\Rightarrow H=\mathrm{e}^{\frac{1}{10}\sin0.25t+c}\Rightarrow "
       r"H=A\mathrm{e}^{\frac{1}{10}\sin0.25t}$ The dM1 and A1* under this method are awarded at virtually the same time. "
       r"Also, for the final two marks, you may see a proof from $\int_0^H\frac{40}{H}\,\mathrm{d}H="
       r"\int_5^t\cos0.25t\,\mathrm{d}t$ [sic: the main scheme's boundary condition is $t=0$, $H=5$]",
       r"ALT: There is an alternative via the use of an integrating factor."],
      False, 26),
    e("10b", "10(b)", INT, "8.8", 1, LATEX["10b"],
      [r"B1 (AO 3.4): Max height $=5\mathrm{e}^{0.1}=5.53$ m (Condone lack of units). Notes: States that the maximum "
       r"height is 5.53 m Accept $5\mathrm{e}^{0.1}$ Condone a lack of units here, but penalise if incorrect units are "
       r"used."],
      False, 26),
    e("10c", "10(c)", INT, "8.8, 5.7", 2, LATEX["10c"],
      [r"M1 (AO 3.1b): Sets $0.25t=\frac{5\pi}{2}$. Notes: For identifying that it would reach the maximum height for the "
       r"2nd time when $0.25t=\frac{5\pi}{2}$ or 450",
       r"A1 (AO 1.1b): 31.4. Notes: Accept awrt 31.4 or $10\pi$ Allow if units are seen"],
      False, 26),

    # ---------------- Q11 ----------------
    e("11a", "11(a)", SEQ, "4.1", 6, LATEX["11a"],
      [r"B1 (AO 3.1a): $\sqrt{\frac{1+4x}{1-x}}=(1+4x)^{0.5}\times(1-x)^{-0.5}$. Notes: Scored for key step in setting up "
       r"the process so that it can be attempted using binomial expansions This could be achieved by "
       r"$\sqrt{\frac{1+4x}{1-x}}=(1+4x)^{0.5}\times(1-x)^{-0.5}$ See end for other alternatives It may be implied by later "
       r"work.",
       r"M1 (AO 1.1b): $(1+4x)^{0.5}=1+0.5\times(4x)+\frac{0.5\times-0.5}{2}\times(4x)^2$. Notes: Award for an attempt at "
       r"the binomial expansion $(1+4x)^{0.5}=1+0.5\times(4x)+\frac{(0.5)\times(-0.5)}{2}\times(4x)^2$ There must be three "
       r"(or more) terms. Allow a missing bracket on the $(4x)^2$ and a sign slip so the correct application may be "
       r"implied by $1+2x\pm0.5x^2$",
       r"M1 (AO 1.1b): $(1-x)^{-0.5}=1+(-0.5)(-x)+\frac{(-0.5)\times(-1.5)}{2}(-x)^2$. Notes: Award for an attempt at the "
       r"binomial expansion $(1-x)^{-0.5}=1+(-0.5)(-x)+\frac{(-0.5)\times(-1.5)}{2}(-x)^2$ There must be three (or more) "
       r"terms. Allow a missing bracket on the $(-x)^2$ and a sign slips so the method may be awarded on "
       r"$1\pm0.5x\pm0.375x^2$",
       r"A1 (AO 1.1b): $(1+4x)^{0.5}=1+2x-2x^2$ and $(1-x)^{-0.5}=1+0.5x+0.375x^2$ oe. Notes: Both correct and simplified. "
       r"This may be awarded for a correct final answer if a candidate does all their simplification at the end",
       r"dM1 (AO 2.1): $(1+4x)^{0.5}\times(1-x)^{-0.5}=\left(1+2x-2x^2\ldots\right)\times\left(1+\frac{1}{2}x+"
       r"\frac{3}{8}x^2\ldots\right)=1+\frac{1}{2}x+\frac{3}{8}x^2+2x+x^2-2x^2+\ldots=A+Bx+Cx^2$. Notes: In the main "
       r"scheme it is for multiplying their two expansions to reach a quadratic. It is for the key step in adding ‘six’ "
       r"terms to produce the quadratic expression. Higher power terms may be seen. Condone slips on the multiplication "
       r"on one term only. It is dependent upon having scored the first B and one of the other two M’s",
       r"A1* (AO 1.1b): $=1+\frac{5}{2}x-\frac{5}{8}x^2\ldots$ *. Notes: Completes proof with no errors or omissions.",
       rf"{Q11ALT} — B1: $(1+4x)^{{0.5}}\approx{BY}(1-x)^{{0.5}}$ then the M’s are for $(1+4x)^{{0.5}}$ and "
       rf"$(1-x)^{{0.5}}$",
       rf"{Q11ALT} — M1: $(1-x)^{{0.5}}=1+(0.5)(-x)+\frac{{(0.5)\times(-0.5)}}{{2}}(-x)^2$",
       rf"{Q11ALT} — dM1: In the alternative it is for multiplying ${BY}(1-x)^{{0.5}}$ and comparing it to "
       rf"$(1+4x)^{{0.5}}$ It is for the key step in adding ‘six’ terms to produce the quadratic expression.",
       rf"{Q11ALT} — A1*: In the alternative there must be some reference to the fact that both sides are equal.",
       rf"{Q11ALT} (Or) — B1: $\sqrt{{\frac{{1+4x}}{{1-x}}}}=\sqrt{{1+\frac{{5x}}{{1-x}}}}=\left(1+5x(1-x)^{{-1}}"
       rf"\right)^{{\frac{{1}}{{2}}}}$ then the first M1 for one application of binomial and the second would be for both "
       rf"$(1-x)^{{-1}}$ and $(1-x)^{{-2}}$",
       rf"{Q11ALT} (Or) — B1: $\sqrt{{\frac{{1+4x}}{{1-x}}\times\frac{{\sqrt{{1-x}}}}{{\sqrt{{1-x}}}}}}="
       rf"\sqrt{{(1+3x-4x^2)\times(1-x)^{{-1}}}}=\left(1+(3x-4x^2)\right)^{{\frac{{1}}{{2}}}}\times(1-x)^{{-1}}$"],
      False, 30),
    e("11b", "11(b)", SEQ, "4.1", 1, LATEX["11b"],
      [r"B1 (AO 2.3): Expression is valid $|x|<\frac{1}{4}$ Should not use $x=\frac{1}{2}$ as $\frac{1}{2}>\frac{1}{4}$. "
       r"Notes: States that the expansion may not / is not valid when $|x|>\frac{1}{4}$ This may be implied by a "
       r"statement such as $\frac{1}{2}>\frac{1}{4}$ or stating that the expansion is only valid when "
       r"$|x|<\frac{1}{4}$ Condone, for this mark a candidate who substitutes $x=\frac{1}{2}$ into the $4x$ and states it "
       r"is not valid as 2 > 1 oe Don’t award for candidates who state that $\frac{1}{2}$ is too big without any "
       r"reference to the validity of the expansion. As a rule you should see some reference to $\frac{1}{4}$ or $4x$"],
      False, 30),
    e("11c", "11(c)", SEQ, "4.1, 2.2", 3, LATEX["11c"],
      [r"M1 (AO 1.1b): Substitutes $x=\frac{1}{11}$ into $\sqrt{\frac{1+4x}{1-x}}\approx1+\frac{5}{2}x-\frac{5}{8}x^2$. "
       r"Notes: Substitutes $x=\frac{1}{11}$ into BOTH sides $\sqrt{\frac{1+4x}{1-x}}\approx1+\frac{5}{2}x-\frac{5}{8}x^2$ "
       r"and attempts to find at least one side. As the left hand side is $\frac{\sqrt{6}}{2}$ they may multiply by 2 "
       r"first which is acceptable",
       r"A1 (AO 1.1b): $\sqrt{\frac{3}{2}}=\frac{1183}{968}$. Notes: Finds both sides leading to a correct "
       r"equation/statement $\sqrt{\frac{15}{10}}=\frac{1183}{968}$ oe $\sqrt{6}=2\times\frac{1183}{968}$",
       r"A1 (AO 2.1): ( so $\sqrt{6}$ is ) $\frac{1183}{484}$ or $\frac{2904}{1183}$. Notes: $\sqrt{6}=\frac{1183}{484}$ "
       r"or $\sqrt{6}=\frac{2904}{1183}$ $\sqrt{6}=2\times\frac{1183}{968}=\frac{1183}{484}$ would imply all 3 marks"],
      False, 30),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", EXP, "6.7, 6.5", 4, LATEX["12a"],
      [r"M1 (AO 3.1a): (i) Method to find $p$ Eg. Divides $32000=Ap^4$ by $50000=Ap^{11}$ "
       r"$p^7=\frac{50000}{32000}\Rightarrow p=\sqrt[7]{\frac{50000}{32000}}=\ldots$ Notes: Attempts to use both pieces of "
       r"information within $V=Ap^t$, eliminates $A$ correctly and solves an equation of the form $p^n=k$ to reach a "
       r"value for $p$. Allow for slips on the 32 000 and 50 000 and the values of $t$.",
       r"A1 (AO 1.1b): $p=1.0658$. Notes: $p=$ awrt 1.0658 Both marks can be awarded from incorrect but consistent "
       r"interpretations of $t$. Eg. $32000=Ap^5$, $50000=Ap^{12}$",
       r"M1 (AO 1.1b): (ii) Substitutes their $p=1.0658$ into either equation and finds $A$ "
       r"$A=\frac{32000}{\text{‘}1.0658\text{’}^4}$ or $A=\frac{50000}{\text{‘}1.0658\text{’}^{11}}$. Notes: Substitutes "
       r"their $p=1.0658$ into either of their equations and finds $A$ Eg $A=\frac{32000}{1.0658^4}$ or "
       r"$A=\frac{50000}{1.0658^7}$ [sic: the main scheme divides 50000 by $1.0658^{11}$] but you may follow through on "
       r"incorrect equations from part (i)",
       r"A1* (AO 1.1b): $A=24795\to24805=24\,800$ *. Notes: Shows that $A$ is between 24 795 and 24 805 before you see "
       r"‘$=24\,800$’ or ‘$\approx24800$’. Accept with or without units.",
       r"ALT: An alternative to (ii) is to start with the given answer. — M1: Attempts "
       r"$24800\times\text{‘}1.0658\text{’}^4=(32000.34)$",
       r"ALT: An alternative to (ii) is to start with the given answer. — A1: $24800\times1.0658^4$, achieves a value "
       r"between 31095 and 32005 followed by $\approx32\,000$ hence $A$ must be $\approx24\,800$"],
      False, 34),
    e("12b", "12(b)", EXP, "6.7", 2, LATEX["12b"],
      [r"B1 (AO 3.4): $A$ / (£)24 800 is the value of the car on 1st January 2001. Notes: States that $A$ is the value of "
       r"the car on 1st January 2001. The statement must reference the car, its cost/value, and “0” time Allow ‘it is the "
       r"initial value of the car’ “it is the cost of the car at $t=0$” “it is the cars starting value”",
       r"B1 (AO 3.4): $p$ /1.0658 is the factor by which the value rises each year. Accept that the value rises by 6.6 % "
       r"a year (ft on their $p$). Notes: States that $p$ is the rate at which the value of the car rises each year. The "
       r"statement must reference a yearly rate and an increase in value or multiplier. They could reference the 1.0658 "
       r"Eg “The cars value rises by 6.5 % each year.” Allow “$p$ is the rate the cars value is rising each year” “it is "
       r"the proportional increase in value of the car each year” “the factor by which the value of the car is rising "
       r"each year” ‘its value appreciates by 6.5% per year’ Allow ‘ the value of the car multiplies by $p$ each year’ Do "
       r"not allow “by how much the value of the car rises each year ” or “it is the rate of inflation”"],
      False, 34),
    e("12c", "12(c)", EXP, "6.7, 6.5, 6.4", 4, LATEX["12c"],
      [r"M1 (AO 3.4): Attempts $100000=\text{‘}24800\text{’}\times\text{‘}1.0658\text{’}^t$ "
       r"$\text{‘}1.0658\text{’}^t=\frac{100000}{24800}$. Notes: Uses the model "
       r"$100000=\text{‘}24800\text{’}\times\text{‘}1.0658\text{’}^t$ and proceeds to their $\text{‘}1.0658\text{’}^t=k$ "
       r"Allow use of any inequality here.",
       r"dM1 (AO 1.1b): $t=\log_{1.0658}\left(\frac{100000}{24800}\right)$. Notes: For the complete method of (i) using the "
       r"information given with their equation of the model and (ii) translating the situation into a correct method to "
       r"find ‘$t$’",
       r"A1 (AO 1.1b): $t=21.8$ or 21.9. Notes: $(t)=$ awrt 21.8 or 21.9 or "
       r"$\log_{1.0658}\left(\frac{100000}{24800}\right)$ oe",
       r"A1 (AO 3.2a): cso 2022. Notes: States in the year 2022. A candidate using a GP formula can be awarded full marks "
       r"Allow different methods in part (c).",
       r"ALT: Eg Via GP a formula — M1: $24800\times\text{‘}1.0658\text{’}^{n-1}=100000\Rightarrow"
       r"\text{‘}1.0658\text{’}^{n-1}=K$",
       r"ALT: Eg Via GP a formula — dM1: Uses a correct method to find $n$.",
       r"ALT: Eg Via GP a formula — A2: 2022",
       r"ALT: Via (trial and improvement) — M1: Uses the model by substituting integer values of $t$ into their $V=Ap^t$ "
       r"so that for $t=n,V<100\,000$ or $t=n+1,V>100\,000$ (So for the correct $A$ and $p$ this would be scored for "
       r"$t=21,V\approx$ £95000 or $t=21,V\approx$ £101 000)",
       r"ALT: Via (trial and improvement) — dM1: For a complete method showing that this is the least value. So both of "
       r"the above values",
       r"ALT: Via (trial and improvement) — A1: Allow for 22 following correct and accurate results (awrt nearest £1000 is "
       r"sufficient accuracy)",
       r"ALT: Via (trial and improvement) — A1: As before"],
      False, 34),

    # ---------------- Q13 ----------------
    e("13", "13", INT, "8.5, 8.3", 7, LATEX["13"],
      [r"M1 (AO 3.1a): Chooses a suitable method for $\int_0^2 2x\sqrt{x+2}\,\mathrm{d}x$ Award for • Using a valid "
       r"substitution $u=\ldots$, changing the terms to $u$’s • integrating and using appropriate limts . Notes: For "
       r"attempting to integrate using substitution. Look for • terms and limits changed to $u$’s. Condone slips and "
       r"errors/omissions on changing $\mathrm{d}x\to\mathrm{d}u$ • attempted multiplication of terms and raising of at "
       r"least one power of $u$ by one. Condone slips • Use of at least the top correct limit. For instance if they go "
       r"back to $x$’s the limit is 2",
       r"B1 (AO 1.1b): Substitution $u=\sqrt{x+2}\Rightarrow\frac{\mathrm{d}x}{\mathrm{d}u}=2u$ oe. Notes: For "
       r"substitution it is for giving the substitution and stating a correct $\frac{\mathrm{d}x}{\mathrm{d}u}$ Eg, "
       r"$u=\sqrt{x+2}\Rightarrow\frac{\mathrm{d}x}{\mathrm{d}u}=2u$ or equivalent such as "
       r"$\frac{\mathrm{d}u}{\mathrm{d}x}=\frac{1}{2\sqrt{x+2}}$",
       r"M1 (AO 1.1b): $\int2x\sqrt{x+2}\,\mathrm{d}x=\int A(u^2\pm2)u^2\,\mathrm{d}u$. Notes: It is for attempting to get "
       r"all aspects of the integral in terms of ‘$u$’. All terms must be attempted including the $\mathrm{d}x$. You are "
       r"only condoning slips on signs and coefficients",
       r"dM1 (AO 2.1): $=Pu^5\pm Qu^3$. Notes: It is for using a correct method of expanding and integrating each term "
       r"(seen at least once) . It is dependent upon the previous M",
       r"A1 (AO 1.1b): $=\frac{4}{5}u^5-\frac{8}{3}u^3$. Notes: Correct answer in $x$ or $u$ See scheme",
       r"ddM1 (AO 1.1b): Uses limits 2 and $\sqrt{2}$ the correct way around. Notes: Dependent upon the previous M, it is "
       r"for using the correct limits for their integral, the correct way around",
       r"A1* (AO 2.1): $=\frac{32}{15}\left(2+\sqrt{2}\right)$ *. Notes: Proceeds correctly to "
       r"$=\frac{32}{15}\left(2+\sqrt{2}\right)$. Note that this is a given answer There must be at one least correct "
       r"intermediate line between $\left[\frac{4}{5}u^5-\frac{8}{3}u^3\right]_{\sqrt{2}}^2$ and "
       r"$\frac{32}{15}\left(2+\sqrt{2}\right)$",
       r"ALT: Second scheme column (substitution $u=x+2$) — B1 (AO 1.1b): Substitution "
       r"$u=x+2\Rightarrow\frac{\mathrm{d}x}{\mathrm{d}u}=1$ oe",
       r"ALT: Second scheme column (substitution $u=x+2$) — M1 (AO 1.1b): $\int2x\sqrt{x+2}\,\mathrm{d}x="
       r"\int A(u\pm2)\sqrt{u}\,\mathrm{d}u$",
       r"ALT: Second scheme column (substitution $u=x+2$) — dM1 (AO 2.1): $=Su^{\frac{5}{2}}\pm Tu^{\frac{3}{2}}$",
       r"ALT: Second scheme column (substitution $u=x+2$) — A1 (AO 1.1b): $=\frac{4}{5}u^{\frac{5}{2}}-"
       r"\frac{8}{3}u^{\frac{3}{2}}$",
       r"ALT: Second scheme column (substitution $u=x+2$) — ddM1 (AO 1.1b): Uses limits 4 and 2 the correct way around",
       r"ALT: Alt Scheme for by parts — M1 (AO 3.1a): Chooses a suitable method for "
       r"$\int_0^2 2x\sqrt{x+2}\,\mathrm{d}x$ Award for • using by parts the correct way around • and using limits. Notes: "
       r"For attempting using by parts to solve It is a problem- solving mark and all elements do not have to be "
       r"correct. • the formula applied the correct way around. You may condone incorrect attempts at integrating "
       r"$\sqrt{x+2}$ for this problem solving mark • further integration, again, this may not be correct, and the use "
       r"of at least the top limit of 2",
       r"ALT: Alt Scheme for by parts — B1 (AO 1.1b): $\int\left(\sqrt{x+2}\right)\mathrm{d}x=\frac{2}{3}(x+2)^{\frac{3}{2}}$. "
       r"Notes: For $\int\left(\sqrt{x+2}\right)\mathrm{d}x=\frac{2}{3}(x+2)^{\frac{3}{2}}$ oe May be awarded "
       r"$\int_0^2 2x\sqrt{x+2}\,\mathrm{d}x\to x^2\times\frac{2(x+2)^{\frac{3}{2}}}{3}$",
       r"ALT: Alt Scheme for by parts — M1 (AO 1.1b): $\int2x\sqrt{x+2}\,\mathrm{d}x=Ax(x+2)^{\frac{3}{2}}-"
       r"\int B(x+2)^{\frac{3}{2}}(\mathrm{d}x)$. Notes: For integration by parts the right way around. Award for "
       r"$Ax(x+2)^{\frac{3}{2}}-\int B(x+2)^{\frac{3}{2}}(\mathrm{d}x)$",
       r"ALT: Alt Scheme for by parts — dM1 (AO 2.1): $=Ax(x+2)^{\frac{3}{2}}-C(x+2)^{\frac{5}{2}}$. Notes: For "
       r"integrating a second time. Award for $Ax(x+2)^{\frac{3}{2}}-C(x+2)^{\frac{5}{2}}$",
       r"ALT: Alt Scheme for by parts — A1 (AO 1.1b): $=\frac{4}{3}x(x+2)^{\frac{3}{2}}-\frac{8}{15}(x+2)^{\frac{5}{2}}$. "
       r"Notes: $\frac{4}{3}x(x+2)^{\frac{3}{2}}-\frac{8}{15}(x+2)^{\frac{5}{2}}$ which may be un simplified",
       r"ALT: Alt Scheme for by parts — ddM1 (AO 1.1b): Uses limits 2 and 0 the correct way around. Notes: Dependent "
       r"upon the previous M, it is for using the limits 2 and 0 the correct way around",
       r"ALT: Alt Scheme for by parts — A1* (AO 2.1): $=\frac{32}{15}\left(2+\sqrt{2}\right)$. Notes: Proceeds to "
       r"$=\frac{32}{15}\left(2+\sqrt{2}\right)$. Note that this is a given answer. At least one correct intermediate line "
       r"must be seen. (See substitution). You would condone missing $\mathrm{d}x$’s"],
      False, 38),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", COORD, "3.3, 5.6", 2, LATEX["14a"],
      [r"M1 (AO 2.1): Attempts to use $\cos2t=1-2\sin^2t\Rightarrow\frac{y-4}{2}=1-2\left(\frac{x-3}{2}\right)^2$. Notes: "
       r"Uses $\cos2t=1-2\sin^2t$ in an attempt to eliminate $t$",
       r"A1* (AO 1.1b): $\Rightarrow y-4=2-4\times\frac{(x-3)^2}{4}\Rightarrow y=6-(x-3)^2$ *. Notes: Proceeds to "
       r"$y=6-(x-3)^2$ without any errors Allow a proof where they start with $y=6-(x-3)^2$ and substitute the parametric "
       r"coordinates. M1 is scored for a correct $\cos2t=1-2\sin^2t$ but A1 is only scored when both sides are seen to be "
       r"the same AND a comment is made, hence proven, or similar ."],
      False, 42),
    e("14b", "14(b)", COORD, "3.3, 2.7", 3, LATEX["14b"],
      [r"M1 (AO 1.1b): $\cap$ shaped parabola [Sketch: an $\cap$-shaped parabola with maximum at $(3,6)$ and ends at "
       r"$(1,2)$ and $(5,2)$.] Notes: For sketching a $\cap$ parabola with a maximum in quadrant one. It does not need to "
       r"be symmetrical",
       r"A1 (AO 1.1b): Fully correct with ‘ends’ at $(1,2)$ & $(5,2)$. Notes: For sketching a $\cap$ parabola with a "
       r"maximum in quadrant one and with end coordinates of $(1,2)$ and $(5,2)$",
       r"B1 (AO 2.4): Suitable reason : Eg states as $x=3+2\sin t$, $1\leqslant x\leqslant5$. Notes: Any suitable "
       r"explanation as to why $C$ does not include all points of $y=6-(x-3)^2,\quad x\in\mathbb{R}$ This should include a "
       r"reference to the limits on sin or cos with a link to a restriction on $x$ or $y$. For example ‘As "
       r"$-1\leqslant\sin t\leqslant1$ then $1\leqslant x\leqslant5$’ Condone in words ‘$x$ lies between 1 and 5’ and "
       r"strict inequalities ‘As $\sin t\leqslant1$ then $x\leqslant5$’ Condone in words ‘$x$ is less than 5’ ‘As "
       r"$-1\leqslant\cos(2t)\leqslant1$ then $2\leqslant y\leqslant6$’ Condone in words ‘$y$ lies between 2 and 6’ "
       r"Withhold if the statement is incorrect Eg “because the domain is $2\leqslant x\leqslant5$” Do not allow a "
       r"statement on the top limit of $y$ as this is the same for both curves"],
      False, 42),
    e("14c", "14(c)", COORD, "3.3, 2.3, 2.5", 5, LATEX["14c"],
      [r"B1 (AO 2.2a): Either finds the lower value for $k=7$ or deduces that $k<\frac{37}{4}$. Notes: Deduces either • "
       r"the correct that the lower value of $k=7$ This can be found by substituting into $(5,2)$ "
       r"$x+y=k\Rightarrow k=7$ or substituting $x=5$ into $x^2-7x+(k+3)=0\Rightarrow25-35+k+3=0\Rightarrow k=7$ • or "
       r"deduces that $k<\frac{37}{4}$ This may be awarded from later work",
       r"M1 (AO 3.1a): Finds where $x+y=k$ meets $y=6-(x-3)^2$ $\Rightarrow k-x=6-(x-3)^2$ and proceeds to 3TQ in $x$ or "
       r"$y$. Notes: For an attempt at the upper value for $k$. Finds where $x+y=k$ meets $y=6-(x-3)^2$ once by using an "
       r"appropriate method. Eg. Sets $k-x=6-(x-3)^2$ and proceeds to a 3TQ",
       r"A1 (AO 1.1b): Correct 3TQ in $x$ $x^2-7x+(k+3)=0$ Or $y$ $y^2+(7-2k)y+(k^2-6k+3)=0$. Notes: Correct 3TQ "
       r"$x^2-7x+(k+3)=0$ The $=0$ may be implied by subsequent work",
       r"M1 (AO 2.1): Uses $b^2-4ac=0\Rightarrow49-4\times1\times(k+3)=0\Rightarrow k=\left(\frac{37}{4}\right)$ or "
       r"$(7-2k)^2-4\times1\times(k^2-6k+3)=0\Rightarrow k=\left(\frac{37}{4}\right)$. Notes: Uses the “discriminant” "
       r"condition. Accept use of $b^2=4ac$ oe or $b^2\ldots4ac$ where ... is any inequality leading to a critical value "
       r"for $k$. Eg. one root $\Rightarrow49-4\times1\times(k+3)=0\Rightarrow k=\frac{37}{4}$",
       r"A1 (AO 2.5): Range of values for $k=\left\{k:7\leqslant k<\frac{37}{4}\right\}$. Notes: Range of values for "
       r"$k=\left\{k:7\leqslant k<\frac{37}{4}\right\}$ Accept $k\in\left[7,\frac{37}{4}\right)$ or exact equivalent",
       r"ALT: ALT table — B1 (AO 2.2a): As above",
       r"ALT: ALT table — M1 (AO 3.1a): Finds where $x+y=k$ meets $y=6-(x-3)^2$ once by using an appropriate method. Eg. "
       r"Sets gradient of $y=6-(x-3)^2$ equal to $-1$",
       r"ALT: ALT table — A1 (AO 1.1b): $-2x+6=-1\Rightarrow x=3.5$",
       r"ALT: ALT table — M1 (AO 2.1): Finds point of intersection and uses this to find upper value of $k$. "
       r"$y=6-(3.5-3)^2=5.75$ Hence using $k=3.5+5.75=9.25$",
       r"ALT: ALT table — A1 (AO 2.5): Range of values for $k=\{k:7\leqslant k<9.25\}$"],
      False, 42),
]

# Examiner report, sentence by sentence, in report order (the Introduction is
# not attached to any question). A sentence that mentions another part only in
# passing is tagged with the part it is about.
W = None
NO = {"ref": False}
BACK = {"ref": True}
DYS = r"$\mathrm{d}y/\mathrm{d}x$"
REPORT = {
    "01": [
        (W, "This question was accessible to most students and many gave fully correct solutions."),
        (W, r"Almost all students were able to score a mark for $\sin3\theta\approx3\theta$ but there were a number who "
            r"simplified the denominator to $6\theta$ instead of $6\theta^2$ resulting in a final solution of "
            r"$\frac{4\theta}{3}$."),
        (W, r"Replacing the $\cos4\theta$ proved more problematic with common incorrect attempts on the numerator including "
            r"$1-4\left(1-\frac{\theta^2}{2}\right)$ and more frequently $1-\left(1-\frac{4\theta^2}{2}\right)$ where the "
            r"$4\theta$ was not squared leading to an incorrect answer of 1/3."),
        (W, r"Other common incorrect attempts involved simplifying $1-\cos4\theta$ to $-8\theta^2$ rather than "
            r"$+8\theta^2$ leading to the incorrect answer of - 4/3."),
        (W, "Even in cases where both substitutions were performed correctly many careless errors were made when "
            "simplifying."),
        (W, r"There were a small number of students who tried to expand and simplify the expression using the double "
            r"angle formula for $\cos4\theta$, but in most cases this resulted in an incorrect expression which did not "
            r"lead to the correct answer.", NO),
    ],
    "02": [
        ({"a"}, "Part (a) of this question allowed the demonstration of good skills in differentiation and was well "
                "answered by the majority of students."),
        ({"a"}, r"A small minority made careless errors on the indices, for example writing $\sqrt{x}$ as $x^{-2}$, "
                r"leading to the loss of both marks as their derivative was not of the required form."),
        ({"a"}, "Others dealt with the index correctly, but made arithmetic errors on the coefficient when "
                "differentiating the term."),
        ({"a"}, "The second derivative was almost always either correct, or a correct follow through, from the students "
                "first derivative."),
        ({"b"}, rf"In part (b) a significant number of students were seen attempting to solve the equation {DYS} = 0 "
                rf"although most quickly realised that they could substitute $x=4$ into {DYS} to obtain 0."),
        ({"b"}, rf"To be awarded the final mark of part (b), students were required to interpret their value of {DYS} at "
                rf"$x=4$ and conclude that the point was a stationary point of the curve."),
        ({"b"}, "Many students omitted this final step thus failing to fully answer the question.", BACK),
        ({"c"}, "For part (c) there was a little more variation."),
        ({"c"}, rf"Most students were aware of the need to substitute $x=4$ into their second derivative and evaluate "
                rf"its sign, although some failed to do this and instead considered the sign of either $y$, {DYS} and/or "
                rf"$\mathrm{{d}}^2y/\mathrm{{d}}x^2$ either side of $x=4$ (usually at 4.1 and 3.9).", NO),
        ({"c"}, "A follow through mark enabled students with an incorrect negative or fractional index from part (a) to "
                "achieve both marks in the last part of the question."),
        ({"c"}, "A significant proportion of students seemed unable to interpret what they had proven from their "
                "calculations, and many seemed to think they were looking for an inflection point, or else determining "
                "that the curve was either convex or concave."),
        ({"c"}, "As with part (b), the most common source of lost marks was therefore a lack of correct reasoning before "
                "making a conclusion."),
    ],
    "03": [
        (W, "This question was well answered by the vast majority of students."),
        (W, "The formulae for arc length and area of a sector were well known and applied, and although the 4 was "
            "occasionally seen on the incorrect side of the equation, this was rare.", NO),
        (W, r"Most students worked in radians and used simultaneous equations to find the value of $\theta$ before "
            r"proceeding to find an exact (positive) value for $r$."),
        (W, "Algebraic and numerical slips, however, when manipulating equations were not an uncommon reason for losing "
            "marks."),
        (W, "If method errors were made in this question, it was usually to miss the half from the sector area or to "
            "confuse the area of a sector with that of a triangle.", NO),
    ],
    "04": [
        (W, "This was perhaps the most poorly attempted question on the whole of the paper.", NO),
        ({"a"}, r"Part (a) should have been familiar to centres but one which required the students to set up their own "
                r"function, usually $\mathrm{f}(x)=2\ln(8-x)-x$, before substituting in the $x$ values of 3 and 4."),
        ({"a"}, "This was well done, but also quite commonly, the only mark gained in the question.", BACK),
        ({"a"}, r"To show that $3<\alpha<4$, a student needed two correct calculations, give a valid reason, which "
                r"required both a change in sign and a mention of continuity, as well as giving a brief deduction."),
        ({"a"}, "Explanations rarely mentioned the fact that the function needed to be continuous in this interval.",
         BACK),
        ({"b"}, "Fully correct solutions to part (b) were very rare."),
        ({"b"}, "Many students assumed that this was a question on continued iteration and gave all values of $x$ from "
                "$x_1$ to $x_8$ without any consideration of the demand of the question.", BACK),
        ({"b"}, r"Students were required to “use the graph” to show whether or not the iteration formula could be used "
                r"to find an approximation for $\alpha$."),
        ({"b"}, r"Hence, to satisfy this demand, a cobweb diagram starting at $x_1=4$ was required followed by an "
                r"explanation that “it can be used” because “the cobweb spirals inwards towards $\alpha$.", BACK),
    ],
    "05": [
        (W, "The majority of students knew to use the quotient rule in this question, although the slips on signs and "
            "bracketing in the terms of the numerator were commonplace."),
        (W, r"We would encourage all students to state the formula being used, with their expressions for ‘$u$’ ‘$v$’ "
            r"‘$\mathrm{d}u$’ and ‘$\mathrm{d}v$’, to ensure that their method is made clear to examiners."),
        (W, "Getting a correct derivative into the required form using trigonometric identities proved to be more "
            "challenging than the differentiation in this question."),
        (W, r"Students recognised the need to use the Pythagorean identity for sine and cosine to simplify their "
            r"numerator and denominator but were less confident when applying the double angle formula for sine, and it "
            r"was not uncommon for a final answer to be left as $\frac{3}{2+2\sin2\theta}$, or for there to be errors in "
            r"an attempt to write this fraction in the required form.", NO),
    ],
    "06": [
        ({"a"}, "Part (a) was a “show that” question in which students used the idea of perpendicular gradients to find "
                "the equation of line $PA$."),
        ({"a"}, "It was very straightforward and well done with almost all students scoring the 3 marks.", BACK),
        ({"b"}, "Part (b) required the students to find the equation of the circle $C$ using the information given."),
        ({"b"}, "Again most students attempted this with ease, finding firstly the coordinates of point $P$, and then the "
                "radius $PA$, before writing down the equation of the circle.", BACK),
        ({"b"}, r"Errors witnessed tended to be arithmetic, although some students complicated the question by "
                r"attempting to solve $(x-7)^2+(y-5)^2=r^2$ and $y=2x+1$ simultaneously in an attempt to find $r$."),
        ({"c"}, "There were numerous ways to find the value of $k$ in part (c)."),
        ({"c"}, "One of the best involved using vector geometry to find the coordinates of the point $N$ on $C$, where "
                "$y=2x+k$ meets $C$."),
        ({"c"}, r"Using the fact that $\overrightarrow{PA}=\overrightarrow{AN}$ enabled students to find $N$ = (11,3) and "
                r"then $k$ by substituting this point into $y=2x+k$.", NO),
        ({"c"}, "Again simultaneous equation methods were common, some more successful than other."),
        ({"c"}, "The most common correct attempt involved solving $y=2x+k$ with $(x-7)^2+(y-5)^2=20$ and then finding "
                "where the resulting equation had one root."),
        ({"c"}, "Care was required with the algebra, especially the squaring of terms, as well as the application of the "
                "discriminant $b^2-4ac=0$."),
        ({"c"}, "This proved to be too great a challenge for many.", BACK),
    ],
    "07": [
        (W, "Both parts of this question were answered well, allowing students to demonstrate their confidence in "
            "integrating fractional expressions in $x$ and working with unknown constants."),
        ({"a", "b"}, "The majority of students failed to make any statement regarding the integral in (a) being "
                     "independent of $k$, or in (b) inversely proportional to $k$."),
        ({"a", "b"}, "Whilst not a requirement for the final A mark in either part, the logical completion of the "
                     "question would have been to make these conclusions and show an understanding of these "
                     "mathematical terms.", BACK),
        ({"b"}, "Common method errors in this question included integrating to obtain a natural logarithm in part (b) as "
                "well as part (a)."),
        (W, "Additionally, despite the successful implementation of limits, some careless and disappointing algebra was "
            "seen in simplifying their final expressions in an attempt to answer the question."),
        (W, "A more unusual but not uncommon error was related to the fact that ‘$k$’ occurred both in the integral and "
            "in the limits."),
        (W, "Some students integrated with respect to $k$ whilst others substituted the limits for the term in $k$ "
            "rather than the term in $x$."),
        ({"b"}, "Other unusual attempts were seen by students attempting to use partial fractions within part (b)."),
    ],
    "08": [
        (W, "This question involved modelling the depth of water in a harbour using a trigonometric function."),
        ({"a"}, "The mark in part (a) was usually scored, although some students did forget to include the units for the "
                "answer of 4.48 metres."),
        ({"a"}, "Other errors seen were as a result of substituting incorrect values of $t$, usually $t=0$, into the "
                "equation for $D$ or prematurely rounding their answer to 4.5 metres."),
        ({"b"}, "Most students also started part (b) correctly and were able to proceed to the intermediate point of "
                "$\\sin30t=-0.6$ without much difficulty."),
        ({"b"}, "The final part of the question, however, proved to be much more difficult, with many students not "
                "finding a value of $t$ greater than 8.5, giving $t=7.2$ then a time of 7:14am."),
        ({"b"}, "Of those who correctly found $t=10.77$ a large number failed to give their final answer as a time, with "
                "10 hours and 46 minutes being common.", NO),
        ({"b"}, "A number of successful students were noteworthy in terms of the clear presentation and communication of "
                "their solutions, often producing sketch graphs of the sine curve to aid their understanding."),
    ],
    "09": [
        ({"a"}, "Question 9(a) was well answered."),
        ({"a"}, "Students generally demonstrated a good understanding of implicit differentiation as well as the chain "
                "and product rules."),
        ({"a"}, "Most reached the given result scoring all 4 marks."),
        ({"b"}, "In question 9(b) however, many made the numerator of the fraction equal zero (i.e. $y=x$) instead of "
                "the denominator ($x=3y$)."),
        ({"b"}, "This kind of error usually resulted in only two of the five marks being scored.", BACK),
        ({"b"}, "There were however many full and accurate solutions, with very few students unable to pick out the "
                "coordinates of the point $P$ from the two solutions to their simultaneous equations."),
        ({"c"}, "Only a small number of students gained the B1 mark in question 9(c)."),
        ({"c"}, "They simply needed to state that the point furthest north can be found by substituting $y=x$ into the "
                "equation of the curve and picking out the positive solution."),
        ({"c"}, "Explanations tended to be incorrect or incomplete, with many stating that it could be found by putting "
                "either $x=0$ or $y=0$.", NO),
    ],
    "10": [
        (W, "This was another modelling question, this time modelling the height of a roller coaster above the ground "
            "by a differential equation.", NO),
        ({"a"}, "In part (a), the majority of students were able to separate the variables of $H$ and $t$ and thus "
                "integrate both sides."),
        ({"a"}, r"Integrating $\cos0.25t$ was done well with most dividing by 0.25 or multiplying by 4."),
        ({"a"}, r"Almost all students were then able to proceed with ease to $\ln H=0.1\sin(0.25t)$."),
        ({"a"}, "The last two marks proved harder to score."),
        ({"a"}, r"Quite a sizeable proportion of students failed to include the constant of integration in "
                r"$\ln H=0.1\sin(0.25t)+c$ and so were unable to apply the boundary condition $t=0,H=5$ in an attempt "
                r"to find $c$."),
        ({"a"}, "The final mark was the hardest to gain."),
        ({"a"}, "The answer was given and many students merely copied down the result on the examination paper."),
        ({"a"}, "There had to be clear evidence that the constant they found was processed correctly and that their log "
                "work was sound."),
        ({"a"}, "The requirement of at least one correct line of working between their working and the given equation, "
                "with no incorrect working, was fair to those who showed a clear argument.", NO),
        ({"b"}, "Part (b) was found by almost all students, even those who could not attempt part (a).", NO),
        ({"b"}, r"In this case the exact answer $5\mathrm{e}^{0.1}$ was accepted as well as 5.53 metres.", BACK),
        ({"c"}, "Fewer students scored both marks in (c), but many were aware that it would occur when "
                "$\\sin(0.25t)=1$.", NO),
        ({"c"}, r"The most common errors were to find the first value using $\frac{\pi}{2}$, or else use 450 rather than "
                r"$\frac{5\pi}{2}$, thus arriving at the incorrect answer of 1800 seconds."),
    ],
    "11": [
        ({"a", "b"}, "This question on the binomial expansion was well attempted by many students, although showing "
                     "sufficient detail to prove the given result in part (a) and providing a comprehensive explanation "
                     "in part (b) proved difficult."),
        ({"a"}, r"In part (a), the majority of students started by attempting to expand $(1+4x)^{0.5}\times(1-x)^{-0.5}$."),
        ({"a"}, "As mentioned in previous years, it is good practice to give the unsimplified version (of each "
                "expansion) before attempting to find the simplified form.", NO),
        ({"a"}, "Those who did find the correct simplified forms of both expansions often lost the last two marks as "
                "many proceeded to just write down the given answer.", NO),
        ({"a"}, "This is a show that question and there was a requirement to show the six key terms that when collected "
                "together formed the given expression.", NO),
        ({"a"}, "Strangely there were a number of cases where the correct expansions were added, and in other cases "
                "divided, in an attempt to find the given answer."),
        ({"b"}, "As with other “explain” questions on this paper, (b) was the worst attempted part of the question."),
        ({"b"}, r"Many merely pointed out that 1/2 was too big or could not be used to find $\sqrt{6}$, rather than "
                r"focussing in on the range in values of $x$ for which the expansion was valid."),
        ({"c"}, "Part c was the most successful part of this question for many students with many gaining all three "
                "marks."),
        ({"c"}, r"Errors seen were mostly arithmetic, with the incorrect fraction $\frac{1183}{968}$ commonly seen"),
    ],
    "12": [
        (W, "This question, based upon the formula $V=ap^t$, modelled the value of a car in £'s against the time in "
            "years after 1st January 2001.", {"note": "the question paper writes the model as $V=Ap^t$"}),
        ({"a"}, "Part (a) was very well answered by the majority of students."),
        ({"a"}, "Most chose the correct values of $t$ and $V$ and successfully solved a pair of simultaneous equations."),
        ({"a"}, "Common errors involved using incorrect values for $t$ or failing to show that $A$ was approximately "
                "24 800."),
        ({"b"}, "It is important in answering questions such as (b) that students are precise about the language and "
                "words that they choose.", NO),
        ({"b"}, "For example, for (b)(i) the statement was required to reference “the car”, “its value” and the "
                "“initial time”."),
        ({"b"}, "In part (b)(ii), “the amount the value of the car was increasing by” was common and scored 0 marks."),
        ({"b"}, "For this part, a clear answer would be “it is the rate at which the cars value is increasing each year” "
                "or “the cars value is increasing by 6.6% a year”.", NO),
        ({"c"}, "In part (c), students generally scored the first 3 marks by correctly using logarithms and proceeding "
                "to $t=21.8$ or 21.9."),
        ({"c"}, "Most students then thought that the year must be 2023 instead of 2022 as they had rounded 21.8 to 22 and "
                "added it to 2001.", NO),
    ],
    "13": [
        (W, "This was an open ended question on integration.", NO),
        (W, "The three most common methods seen are shown the mark scheme, two methods using substitution and one using "
            "integration by parts."),
        (W, "Integration by parts was popular and well understood by the majority of students."),
        (W, r"Most knew that $\int\sqrt{x+2}\,\mathrm{d}x\to\frac{2}{3}(x+2)^{\frac{3}{2}}$ and were able to integrate to "
            r"an expression of the form $Ax(x+2)^{\frac{3}{2}}-C(x+2)^{\frac{5}{2}}$"),
        (W, "Slips in the values of the constants $A$ and $C$ were rare."),
        (W, r"However, as with earlier questions, there was a lack of clarity in moving from "
            r"$\left[\frac{4}{3}x(x+2)^{\frac{3}{2}}-\frac{8}{15}(x+2)^{\frac{5}{2}}\right]_0^2$ to the given answer of "
            r"$\frac{32}{15}\left(2+\sqrt{2}\right)$"),
        (W, r"Substitution was also well understood with $u=x+2$ more common than $u=\sqrt{x+2}$."),
        (W, r"Errors here included the omission of finding $\mathrm{d}x$ in terms of $\mathrm{d}u$, poor expansion of "
            r"expressions such as $2(u-2)\sqrt{u}$ within the integral, and, as with parts, a lack of acceptable working "
            r"shown when proceeding to the given answer.", NO),
    ],
    "14": [
        (W, "The final question on the paper was a challenge to all."),
        ({"a"}, r"Part (a) was straightforward with most recognising the need to use the identity $\cos2t=1-2\sin^2t$ in "
                r"some form to prove the required result."),
        ({"a"}, "This was one of the more successful “show that” parts of the paper.", BACK),
        ({"b"}, "Only stronger students, however, were able to understand and explain why the curve $C$ did not include "
                "all points of the curve $y=6-(x-3)^2$."),
        ({"b"}, "Many drew the whole of the parabola in part (b) scoring one out of the three marks."),
        ({"b"}, "Those who managed to sketch the correct part of the parabola rarely were able to explain why the domain "
                "(and range) were restricted.", NO),
        ({"b"}, r"Stating that “because $0\leqslant t\leqslant2\pi$ ” was not enough to explain why for instance "
                r"$1\leqslant x\leqslant5$."),
        ({"b"}, r"The best students were able to explain that as $-1\leqslant\sin t\leqslant1$ then $3+2\sin t$ would "
                r"have a maximum value of $3+2=5$ and a minimum value of $3-2=1$."),
        ({"c"}, "Part (c) was also demanding and better students annotated their graphs to help their understanding of "
                "the question (See Figure 1).",
         {"note": "Figure 1 here is a sketch printed in the examiner report; the question paper's Figure 1 belongs to "
                  "Question 3"}),
        ({"c"}, "Most however used the discriminant condition $b^2-4ac>0$ for two roots and were able to proceed to two "
                "values."),
        ({"c"}, "Arithmetic errors were quite common using this method.", BACK),
        ({"c"}, "Most students who proceeded to the answer were well versed in writing their answer using set notation."),
    ],
}

# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
RATINGS = {
    "01": ("easy", ("01", 0)),
    "02a": ("easy", ("02", 0)),
    "02b": ("medium", ("02", 6)),
    "02c": ("medium", ("02", 7)),
    "03": ("easy", ("03", 0)),
    "04a": ("hard", ("04", 4)),
    "04b": ("hard", ("04", 5)),
    "05": ("medium", ("05", 2)),
    "06a": ("easy", ("06", 1)),
    "06b": ("easy", ("06", 3)),
    "06c": ("hard", ("06", 11)),
    "07a": ("easy", ("07", 0)),
    "07b": ("easy", ("07", 0)),
    "08a": ("easy", ("08", 1)),
    "08b": ("hard", ("08", 4)),
    "09a": ("easy", ("09", 0)),
    "09b": ("medium", ("09", 5)),
    "09c": ("hard", ("09", 6)),
    "10a": ("medium", ("10", 4)),
    "10b": ("easy", ("10", 10)),
    "10c": ("medium", ("10", 12)),
    "11a": ("medium", ("11", 3)),
    "11b": ("hard", ("11", 6)),
    "11c": ("easy", ("11", 8)),
    "12a": ("easy", ("12", 1)),
    "12b": ("medium", ("12", 6)),
    "12c": ("hard", ("12", 9)),
    "13": ("medium", ("13", 5)),
    "14a": ("easy", ("14", 1)),
    "14b": ("hard", ("14", 3)),
    "14c": ("hard", ("14", 8)),
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
