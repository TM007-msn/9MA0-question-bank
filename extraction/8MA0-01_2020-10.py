"""Draft builder for 8MA0-01 2020-10 (AS Pure, October 2020).

Run (from the project root, with the venv active):
    python extraction/8MA0-01_2020-10.py        # writes out/drafts/8MA0-01_2020-10.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-01_2020-10.json

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

P, S = "8MA0-01", "2020-10"
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

# Shared stems go in variables so each part's question_latex stands alone.
Q2 = (r"[In this question the unit vectors $\mathbf{i}$ and $\mathbf{j}$ are due east and due north respectively.] "
      r"A coastguard station $O$ monitors the movements of a small boat. At 10:00 the boat is at the point "
      r"$(4\mathbf{i}-2\mathbf{j})$ km relative to $O$. At 12:45 the boat is at the point $(-3\mathbf{i}-5\mathbf{j})$ "
      r"km relative to $O$. The motion of the boat is modelled as that of a particle moving in a straight line at "
      r"constant speed. ")
Q3 = (r"In this question you must show all stages of your working. Solutions relying on calculator technology are "
      r"not acceptable. ")
Q4 = (r"In 1997 the average CO$_2$ emissions of new cars in the UK was 190 g/km. In 2005 the average CO$_2$ "
      r"emissions of new cars in the UK had fallen to 169 g/km. Given $A$ g/km is the average CO$_2$ emissions of new "
      r"cars in the UK $n$ years after 1997 and using a linear model, ")
FIG1 = (r"[Figure 1 (not to scale): triangle $ABD$ with $AB$ as the horizontal base and $C$ on $AD$ between $A$ and "
        r"$D$; the angle of $27^\circ$ at $A$ is marked, and beams $BC$ and $BD$ join $B$ to $C$ and $D$.]" "\n")
Q5 = (FIG1 + r"Figure 1 shows the design for a structure used to support a roof. The structure consists of four steel "
      r"beams, $AB$, $BD$, $BC$ and $AD$. Given $AB=12$ m, $BC=BD=7$ m and angle $BAC=27^\circ$ ")
Q6A = (r"Find the first 4 terms, in ascending powers of $x$, in the binomial expansion of $$(1+kx)^{10}$$ where $k$ "
       r"is a non-zero constant. Write each coefficient as simply as possible.")
Q7 = r"Given that $k$ is a positive constant and $\int_1^k\left(\frac{5}{2\sqrt{x}}+3\right)\mathrm{d}x=4$ "
Q8 = (r"The temperature, $\theta\,^\circ$C, of a cup of tea $t$ minutes after it was placed on a table in a room, is "
      r"modelled by the equation $$\theta=18+65\mathrm{e}^{-\frac{t}{8}}\qquad t\geqslant0$$ Find, according to the "
      r"model, ")
FIG2 = (r"[Figure 2: sketch of $\mu$ against $t$: a decreasing curve starting at the point $(0, 94)$ on the $\mu$-axis, "
        r"passing through $(8, 50)$, and approaching the dashed horizontal line $l$ above the $t$-axis.]" "\n")
FIG3 = (r"[Figure 3: part of the curve $y=3\cos x^\circ$, with a maximum on the $y$-axis and minimum points either "
        r"side of it; the minimum point $P(c, d)$ to the left of the $y$-axis is marked.]" "\n")
Q9 = (FIG3 + r"Figure 3 shows part of the curve with equation $y=3\cos x^\circ$. The point $P(c, d)$ is a minimum point "
      r"on the curve with $c$ being the smallest negative value of $x$ at which a minimum occurs. ")
Q10 = r"$$\mathrm{g}(x)=2x^3+x^2-41x-70$$ "
Q12 = (r"An advertising agency is monitoring the number of views of an online advert. The equation "
       r"$$\log_{10}V=0.072t+2.379\qquad1\leqslant t\leqslant30,\ t\in\mathbb{N}$$ is used to model the total number "
       r"of views of the advert, $V$, in the first $t$ days after the advert went live. ")
Q12A = (r"(a) Show that $V=ab^t$ where $a$ and $b$ are constants to be found. Give the value of $a$ to the nearest "
        r"whole number and give the value of $b$ to 3 significant figures. ")
Q13A = r"(a) Prove that for all positive values of $a$ and $b$ $$\frac{4a}{b}+\frac{b}{a}\geqslant4$$ "
Q14 = (r"A curve has equation $y=\mathrm{g}(x)$. Given that: $\mathrm{g}(x)$ is a cubic expression in which the "
       r"coefficient of $x^3$ is equal to the coefficient of $x$; the curve with equation $y=\mathrm{g}(x)$ passes "
       r"through the origin; the curve with equation $y=\mathrm{g}(x)$ has a stationary point at $(2, 9)$, ")

TOGETHER = "Score these two parts together. "

DRAFT = [
    # ---------------- Q1 ----------------
    e("01", "1", DIFF, "7.3, 7.2, 3.1", 5,
      r"A curve has equation $$y=2x^3-4x+5$$ Find the equation of the tangent to the curve at the point $P(2, 13)$. "
      r"Write your answer in the form $y=mx+c$, where $m$ and $c$ are integers to be found. Solutions relying on "
      r"calculator technology are not acceptable.",
      [r"M1 (AO 1.1b): Attempts to differentiate $x^n\to x^{n-1}$ seen once. Notes: Attempts to differentiate "
       r"$x^n\to x^{n-1}$ seen once. Score for $x^3\to x^2$ or $\pm4x\to4$ or $+5\to0$",
       r"A1 (AO 1.1b): $y=2x^3-4x+5\Rightarrow\frac{\mathrm{d}y}{\mathrm{d}x}=6x^2-4$. Notes: "
       r"$\left(\frac{\mathrm{d}y}{\mathrm{d}x}=\right)6x^2-4$ which may be unsimplified. $6x^2-4+C$ is A0",
       r"dM1 (AO 1.1b): For substituting $x=2$ into their $\frac{\mathrm{d}y}{\mathrm{d}x}=6x^2-4$. Notes: Substitutes "
       r"$x=2$ into their $\frac{\mathrm{d}y}{\mathrm{d}x}$. The first M must have been awarded. Score for sight of "
       r"embedded values, or sight of \"$\frac{\mathrm{d}y}{\mathrm{d}x}$ at $x=2$ is\" or a correct follow through. "
       r"Note that 20 on its own is not enough as this can be done on a calculator.",
       r"ddM1 (AO 1.1b): For a correct method of finding a tangent at $P(2,13)$. Score for $y-13=\text{\"}20\text{\"}(x-2)$. "
       r"Notes: For a correct method of finding a tangent at $P(2,13)$. Score for $y-13=\text{\"}20\text{\"}(x-2)$. It is "
       r"dependent upon both previous M's. If the form $y=mx+c$ is used they must proceed as far as $c=\ldots$",
       r"A1 (AO 1.1b): $y=20x-27$. Notes: Completely correct $y=20x-27$ (and in this form)"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02a", "2(a)", VEC, "9.2, 9.5", 3,
      Q2 + r"Calculate the bearing on which the boat is moving, giving your answer in degrees to one decimal place.",
      [r"M1 (AO 1.1b): Attempts to find an \"allowable\" angle Eg $\tan\theta=\frac{7}{3}$ (beside a sketch on a grid of "
       r"the two positions and the displacement, with lengths $\sqrt{20}$, $\sqrt{34}$, $\sqrt{58}$, 7 and 3 and angles "
       r"$63.4^\circ$, $49.8^\circ$, $66.8^\circ$ and $23.2^\circ$). Notes: " + TOGETHER + r"Attempts an allowable "
       r"angle. (Either the \"66.8\", \"23.2\" or (\"49.8\" and \"63.4\")) $\tan\theta=\pm\frac{7}{3}$, "
       r"$\tan\theta=\pm\frac{3}{7}$, $\tan\theta=\pm\frac{-2--5}{4--3}$ etc. There must be an attempt to subtract the "
       r"coordinates (seen or applied at least once). If part (b) is attempted first, look for example for "
       r"$\sin\theta=\pm\frac{7}{\text{\"}\sqrt{58}\text{\"}}$, $\cos\theta=\pm\frac{7}{\text{\"}\sqrt{58}\text{\"}}$, "
       r"etc. They may use the cosine rule and trigonometry to find the two angles in the scheme. See above. Eg award "
       r"for $\cos\theta=\frac{\text{\"}58\text{\"}+\text{\"}20\text{\"}-\text{\"}34\text{\"}}"
       r"{2\times\text{\"}\sqrt{58}\text{\"}\times\text{\"}\sqrt{20}\text{\"}}$ and $\tan\theta=\pm\frac{4}{2}$ or "
       r"equivalent.",
       r"dM1 (AO 3.1b): A full attempt to find the bearing Eg $180^\circ+$\"$67^\circ$\". Notes: A full attempt to find "
       r"the bearing. $180^\circ+\arctan\frac{7}{3}$, $270^\circ-\arctan\frac{3}{7}$, "
       r"$360^\circ-$\"$49.8^\circ$\"$-$\"$63.4^\circ$\". It is dependent on the previous method mark.",
       r"A1 (AO 1.1b): Bearing = awrt $246.8^\circ$. Notes: Bearing = awrt $246.8^\circ$ oe. Allow S $66.8^\circ$ W"],
      False, 4),
    e("02b", "2(b)", VEC, "9.4, 9.5", 3,
      Q2 + r"Calculate the speed of the boat, giving your answer in km h$^{-1}$",
      [r"M1 (AO 1.1b): Attempts to find the distance travelled $=\sqrt{(4--3)^2+(-2+5)^2}=(\sqrt{58})$. Notes: "
       + TOGETHER + r"Attempts to find the distance travelled. Allow for $d^2=(4--3)^2+(-2+5)^2$. You may see this on "
       r"a diagram and allow if they attempt to find the magnitude from their \"resultant vector\" found in part (a).",
       r"dM1 (AO 3.1b): Attempts to find the speed $=\frac{\sqrt{58}}{2.75}$. Notes: Attempts to find the speed. There "
       r"must have been an attempt to find the distance using the coordinates and then divide it by 2.75.",
       r"A1 (AO 1.1b): = awrt 2.77 km h$^{-1}$. Notes: awrt 2.77 km h$^{-1}$",
       r"ALT: Alternatively (b) — dM1 (AO 3.1b): Alternatively they could find the speed in km min$^{-1}$ and then "
       r"multiply by 60"],
      False, 4),

    # ---------------- Q3 ----------------
    e("03i", "3(i)", ALG, "2.2", 3,
      Q3 + r"Solve the equation $$x\sqrt{2}-\sqrt{18}=x$$ writing the answer as a surd in simplest form.",
      [r"M1 (AO 1.1b): $x\sqrt{2}-\sqrt{18}=x\Rightarrow x(\sqrt{2}-1)=\sqrt{18}\Rightarrow x=\frac{\sqrt{18}}{\sqrt{2}-1}$. "
       r"Notes: Combines the terms in $x$, factorises and divides to find $x$. Condone sign slips and ignore any attempts "
       r"to simplify $\sqrt{18}$",
       r"dM1 (AO 3.1a): $\Rightarrow x=\frac{\sqrt{18}}{\sqrt{2}-1}\times\frac{\sqrt{2}+1}{\sqrt{2}+1}$. Notes: Scored for "
       r"a complete method to find $x$. In the main scheme it is for making $x$ the subject and then multiplying both "
       r"numerator and denominator by $\sqrt{2}+1$",
       r"A1 (AO 1.1b): $x=\frac{\sqrt{18}(\sqrt{2}+1)}{1}=6+3\sqrt{2}$. Notes: $x=6+3\sqrt{2}$ only following a correct "
       r"intermediate line. Allow $\frac{6+3\sqrt{2}}{1}$ as an intermediate line.",
       r"ALT: Alternatively (i), squaring both sides — M1 (AO 1.1b): Alternatively squares both sides "
       r"$x\sqrt{2}-\sqrt{18}=x\Rightarrow2x^2-12x+18=x^2$",
       r"ALT: Alternatively (i), squaring both sides — dM1 (AO 3.1a): In the alternative it is for squaring both sides "
       r"to produce a 3TQ and then factorising their quadratic equation to find $x$. (usual rules apply for solving "
       r"quadratics)",
       r"ALT: Alternatively (i), squaring both sides — A1 (AO 1.1b): In the alternative method the $6-3\sqrt{2}$ must be "
       r"discarded."],
      False, 6),
    e("03ii", "3(ii)", ALG, "2.1, 2.2", 3,
      Q3 + r"Solve the equation $$4^{3x-2}=\frac{1}{2\sqrt{2}}$$",
      [r"M1 (AO 2.5): $4^{3x-2}=\frac{1}{2\sqrt{2}}\Rightarrow2^{6x-4}=2^{-\frac{3}{2}}$. Notes: Uses correct "
       r"mathematical notation and attempts to set both sides as powers of 2 or 4. Eg $2^{ax+b}=2^c$ or "
       r"$4^{dx+e}=4^f$ is sufficient for this mark.",
       r"dM1 (AO 1.1b): $6x-4=-\frac{3}{2}\Rightarrow x=\ldots$ Notes: Scored for a complete method to find $x$. Scored "
       r"for setting the indices of 2 or 4 equal to each other and then solving to find $x$. There must be an attempt on "
       r"both sides. You can condone slips for this mark Eg bracketing errors $4^{3x-2}=2^{2\times3x-2}$ or "
       r"$\frac{1}{2\sqrt{2}}=2^{-1+\frac{1}{2}}$",
       r"A1 (AO 1.1b): $x=\frac{5}{12}$. Notes: $x=\frac{5}{12}$ with correct intermediate work",
       r"ALT: Alternatively (ii), logs — M1 (AO 2.5): Alternatively uses logs (base 2 or 4) to get a linear equation "
       r"in $x$. $4^{3x-2}=\frac{1}{2\sqrt{2}}\Rightarrow\log_24^{3x-2}=\log_2\frac{1}{2\sqrt{2}}\Rightarrow2(3x-2)"
       r"=\log_2\frac{1}{2\sqrt{2}}$. Or $4^{3x-2}=\frac{1}{2\sqrt{2}}\Rightarrow3x-2=\log_4\frac{1}{2\sqrt{2}}$. Or "
       r"$4^{3x-2}=\frac{1}{2\sqrt{2}}\Rightarrow4^{3x}=4\sqrt{2}\Rightarrow3x=\log_44\sqrt{2}$",
       r"ALT: Alternatively (ii), logs — dM1 (AO 1.1b): In the alternative method candidates cannot just write down "
       r"the answer to the rhs. So expect some justification. E.g. "
       r"$\log_2\frac{1}{2\sqrt{2}}=\log_22^{-\frac{3}{2}}=-\frac{3}{2}$ or "
       r"$\log_4\frac{1}{2\sqrt{2}}=\log_42^{-\frac{3}{2}}=-\frac{3}{2}\times\frac{1}{2}$ condoning slips as per main "
       r"scheme or $3x=\log_44\sqrt{2}\Rightarrow3x=1+\frac{1}{4}$"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", COORD, "3.1", 3, Q4 + r"form an equation linking $A$ with $n$.",
      [r"M1 (AO 3.3): Attempts $A=mn+c$ with either $(0,190)$ or $(8,169)$ Or attempts gradient eg "
       r"$m=\pm\frac{190-169}{8}(=-2.625)$. Notes: Attempts $A=mn+c$ with either $(0,190)$ or $(8,169)$ considered. "
       r"Eg Accept sight of $190=0n+c$ or $169=8m+c$ or $A-169=m(n-8)$ or $A=190+mn$ where $m$ could be a value. "
       r"Also accept an attempt to find the gradient $\pm\frac{190-169}{8}$ or sight of $\pm2.625$ or "
       r"$\pm\frac{21}{8}$ oe",
       r"dM1 (AO 3.1b): Full method to find a linear equation linking $A$ with $n$ E.g. Solves $190=0n+c$ and "
       r"$169=8n+c$ simultaneously. Notes: A full method to find both constants of a linear equation. Method 1: Solves "
       r"$190=0n+c$ and $169=8n+c$ simultaneously. Condone different variables for this mark. Eg. $y$ in terms of $x$.",
       r"A1 (AO 1.1b): $A=-2.625n+190$. Notes: $A=-2.625n+190$ or $A=-\frac{21}{8}n+190$ oe",
       r"ALT: Method 2 (a) — dM1 (AO 3.1b): Uses gradient and a point Eg $m=\pm\frac{190-169}{8}(=-2.625)$ and "
       r"$c=190$"],
      False, 8),
    e("04b", "4(b)", COORD, "3.1", 3,
      Q4 + r"(a) form an equation linking $A$ with $n$. In 2016 the average CO$_2$ emissions of new cars in the UK was "
      r"120 g/km. (b) Comment on the suitability of your model in light of this information.",
      [r"M1 (AO 3.4): Attempts $A=-2.625\times19+190=\ldots$ Notes: Attempts to substitute \"$n$\" $=19$ into their "
       r"linear model to find $A$. They may call it $x=19$",
       r"A1 (AO 1.1b): $A=140.125$ g km$^{-1}$. Notes: $A=140.125$ from $n=19$. Allow $A=140$",
       r"B1ft (AO 3.5a): It is predicting a much higher value and so is not suitable. Notes: Requires a correct "
       r"calculation for their model, a correct statement and a conclusion E.g For correct (a) $A=140$ is (much) higher "
       r"than 120 so the model is not suitable/appropriate. Follow through on a correct statement for their equation. As "
       r"a guide allow anything within [114,126] to be regarded as suitable. Anything less than 108 or more than 132 "
       r"should be justified as unsuitable. Note B0 Recorded value is not the same as/does not equal/does not match the "
       r"value predicted",
       r"ALT: Alternatively (b) — M1 (AO 3.4): Alternatively substitutes $A=120$ into their linear model to find $n$.",
       r"ALT: Alternatively (b) — A1 (AO 1.1b): or $n=26/27$ following $A=120$"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", TRIG, "5.1", 3, Q5 + r"find, to one decimal place, the size of angle $ACB$.",
      [r"M1 (AO 1.1b): States $\frac{\sin\theta}{12}=\frac{\sin27}{7}$. Notes: States "
       r"$\frac{\sin\theta}{12}=\frac{\sin27}{7}$ oe with the sides and angles in the correct positions",
       r"A1 (AO 1.1b): Finds $\theta=$ awrt $51^\circ$ or awrt $129^\circ$. Notes: awrt $51^\circ$ or awrt $129^\circ$",
       r"A1 (AO 1.1b): = awrt $128.9^\circ$. Notes: Awrt $128.9^\circ$ only (must be seen in part a))",
       r"ALT: Alternatively (a) — M1 (AO 1.1b): Alternatively they may use the cosine rule on $\angle ACB$ and then "
       r"solve the subsequent quadratic to find $AC$ and then use the cosine rule again"],
      True, 10),
    e("05b", "5(b)", TRIG, "5.1", 3,
      Q5 + r"(a) find, to one decimal place, the size of angle $ACB$. The steel beams can only be bought in whole metre "
      r"lengths. (b) Find the minimum length of steel that needs to be bought to make the complete structure.",
      [r"M1 (AO 1.1b): Attempts to find part or all of $AD$ Eg $AD^2=7^2+12^2-2\times12\times7\cos101.9=(AD=15.09)$ Eg "
       r"$(AC)^2=7^2+12^2-2\times12\times7\cos(180-\text{\"}128.9\text{\"}-27)$ Eg $12\cos27$ or "
       r"$7\cos\text{\"}51\text{\"}$. Notes: Attempts a \"correct\" method of finding either $AD$ or a part of $AD$ eg "
       r"($AC$ or $CD$ or forming a perpendicular to split the triangle into two right angled triangles to find $AX$ or "
       r"$XD$) which may be seen in (a). You should condone incorrect labelling of the side. Look for attempted "
       r"application of the cosine rule $(AD)^2=7^2+12^2-2\times12\times7\cos(\text{\"}128.9\text{\"}-27)$ or "
       r"$(AC)^2=7^2+12^2-2\times12\times7\cos(180-\text{\"}128.9\text{\"}-27)$ Or an attempted application of the sine "
       r"rule $\frac{(AD)}{\sin(\text{\"}128.9\text{\"}-27)}=\frac{7}{\sin27}$ Or "
       r"$\frac{(AC)}{\sin(180-\text{\"}128.9\text{\"}-27)}=\frac{7}{\sin27}$ Or an attempt using trigonometry on a "
       r"right-angled triangle to find part of $AD$: $12\cos27$ or $7\cos\text{\"}51\text{\"}$. This method can be "
       r"implied by sight of awrt 15.1 or awrt 6.3 or awrt 8.8 or awrt 10.7 or awrt 4.4",
       r"dM1 (AO 3.1a): Full method for the total length $=12+7+7+\text{\"}15.09\text{\"}=$. Notes: A complete method of "
       r"finding the TOTAL length. There must have been an attempt to use the correct combination of angles and sides. "
       r"Expect to see $7+7+12+\text{\"}AD\text{\"}$ found using a correct method. This is scored by either "
       r"$7+7+12+\text{\"}AD\text{\"}$ if $\angle ACB=128.9^\circ$ in a) or $7+7+12+$ awrt 15.1 by candidates who may "
       r"have assumed $\angle ACB=51.1^\circ$ in a)",
       r"A1 (AO 3.2a): = 42 m. Notes: Rounds correct 41.09 m (or correct expression) up to 42 m to find steel bought. "
       r"Candidates who assumed $\angle ACB=51.1^\circ$ (acute) in (a): Full marks can still be achieved as candidates "
       r"may have restarted in (b) or not used the acute angle in their calculation which is often unclear. We are "
       r"condoning any reference to $AC=15.1$ so ignore any labelling of the lengths they are finding. [The mark scheme "
       r"shows two diagrams: the correct triangle, with $AC=6.3$, $CD=8.8$, $BC=BD=7$, $AB=12$, angles $128.9^\circ$ "
       r"and $51.1^\circ$ at $C$, $51.1^\circ$ at $D$, $24.1^\circ$ and $77.8^\circ$ at $B$ ($=101.9^\circ$); and the "
       r"triangle using the incorrect acute angle, with $AC=15.1$, $51.1^\circ$ and $128.9^\circ$ at $C$, $128.9^\circ$ "
       r"at $D$ and $101.9^\circ$ at $B$ ($=24.1^\circ$).]"],
      True, 10),

    # ---------------- Q6 ----------------
    e("06a", "6(a)", SEQ, "4.1", 3, Q6A,
      [r"M1 (AO 1.1b): $(1+kx)^{10}=1+\binom{10}{1}(kx)^1+\binom{10}{2}(kx)^2+\binom{10}{3}(kx)^3\ldots$ Notes: An "
       r"attempt at the binomial expansion. This may be awarded for either the second or third term or fourth term. The "
       r"coefficients may be of the form ${}^{10}C_1$, $\binom{10}{2}$ etc or eg $\frac{10\times9\times8}{3!}$",
       r"A1 (AO 1.1b): $(1+kx)^{10}=1+\binom{10}{1}(kx)^1+\binom{10}{2}(kx)^2+\binom{10}{3}(kx)^3\ldots$ Notes: A correct "
       r"unsimplified binomial expansion. The coefficients must be numerical so cannot be of the form ${}^{10}C_1$, "
       r"$\binom{10}{2}$. Coefficients of the form $\frac{10\times9\times8}{3!}$ are acceptable for this mark. The "
       r"bracketing must be correct on $(kx)^2$ but allow recovery",
       r"A1 (AO 1.1b): $=1+10kx+45k^2x^2+120k^3x^3\ldots$ Notes: $1+10kx+45k^2x^2+120k^3x^3\ldots$ or "
       r"$1+10(kx)+45(kx)^2+120(kx)^3\ldots$ Allow if written as a list."],
      False, 12),
    e("06b", "6(b)", SEQ, "4.1, 2.6", 3,
      "(a) " + Q6A + r" Given that in the expansion of $(1+kx)^{10}$ the coefficient $x^3$ is 3 times the coefficient "
      r"of $x$, (b) find the possible values of $k$.",
      [r"B1 (AO 1.2): Sets $120k^3=3\times10k$. Notes: Sets their $120k^3=3\times$ their $10k$ (Seen or implied). For "
       r"candidates who haven't cubed allow $120k=3\times$ their $10k$. If they write $120k^3x^3=3\times$ their $10kx$ "
       r"only allow recovery of this mark if $x$ disappears afterwards.",
       r"M1 (AO 1.1b): $4k^2=1\Rightarrow k=\ldots$ Notes: Solves a cubic of the form $Ak^3=Bk$ by factorising "
       r"out/cancelling the $k$ and proceeding correctly to at least one value for $k$. Usually $k=\sqrt{\frac{B}{A}}$",
       r"A1 (AO 1.1b): $k=\pm\frac{1}{2}$. Notes: $k=\pm\frac{1}{2}$ o.e ignoring any reference to 0"],
      False, 12),

    # ---------------- Q7 ----------------
    e("07a", "7(a)", INT, "8.3, 8.2, 2.1", 4, Q7 + r"show that $3k+5\sqrt{k}-12=0$",
      [r"M1 (AO 1.1b): $x^n\to x^{n+1}$. Notes: For $x^n\to x^{n+1}$ on correct indices. This can be implied by the "
       r"sight of either $x^{\frac{1}{2}}$ or $x$",
       r"A1 (AO 1.1b): $\int\left(\frac{5}{2\sqrt{x}}+3\right)\mathrm{d}x=5\sqrt{x}+3x$. Notes: $5\sqrt{x}+3x$ or "
       r"$5x^{\frac{1}{2}}+3x$ but may be unsimplified. Also allow with $+c$ and condone any spurious notation.",
       r"dM1 (AO 1.1b): $\left[5\sqrt{x}+3x\right]_1^k=4\Rightarrow5\sqrt{k}+3k-8=4$. Notes: Uses both limits, "
       r"subtracts, and sets equal to 4. They cannot proceed to the given answer without a line of working showing this.",
       r"A1* (AO 2.1): $3k+5\sqrt{k}-12=0$ *. Notes: Fully correct proof with no errors (bracketing or otherwise) "
       r"leading to given answer."],
      False, 14),
    e("07b", "7(b)", ALG, "2.3, 2.1", 4,
      Q7 + r"(a) show that $3k+5\sqrt{k}-12=0$ (b) Hence, using algebra, find any values of $k$ such that "
      r"$$\int_1^k\left(\frac{5}{2\sqrt{x}}+3\right)\mathrm{d}x=4$$",
      [r"M1 (AO 3.1a): $3k+5\sqrt{k}-12=0\Rightarrow(3\sqrt{k}-4)(\sqrt{k}+3)=0$. Notes: For a correct method of "
       r"solving. This could be as the scheme, treating as a quadratic in $\sqrt{k}$ and using allowable method to solve "
       r"including factorisation, formula etc. Allow values for $\sqrt{k}$ to be just written down, e.g. allow "
       r"$\sqrt{k}=\pm\frac{4}{3},(\pm3)$",
       r"A1 (AO 1.1b): $\sqrt{k}=\frac{4}{3},(-3)$. Notes: $\sqrt{k}=\frac{4}{3},(-3)$",
       r"dM1 (AO 1.1b): $\sqrt{k}=\ldots\Rightarrow k=\ldots$ oe. Notes: For solving to find at least one value for $k$. "
       r"It is dependent upon the first M mark. In the main method it is scored for squaring their value(s) of "
       r"$\sqrt{k}$",
       r"A1 (AO 2.3): $k=\frac{16}{9}$ (with 9 crossed out). Notes: Full and rigorous method leading to "
       r"$k=\frac{16}{9}$ only. The 9 must be rejected.",
       r"ALT: Alternatively (b), squaring — M1 (AO 3.1a): Alternatively score for rearranging to $5\sqrt{k}=12-3k$ and "
       r"then squaring to get $\ldots k=(12-3k)^2$",
       r"ALT: Alternatively (b), squaring — A1 (AO 1.1b): Or in the alt method it is for reaching a correct 3TQ "
       r"equation $9k^2-97k+144=0$",
       r"ALT: Alternatively (b), squaring — dM1 (AO 1.1b): In the alternative scored for solving their 3TQ by an "
       r"appropriate method"],
      False, 14),

    # ---------------- Q8 ----------------
    e("08a", "8(a)", EXP, "6.7", 1, Q8 + r"the temperature of the cup of tea when it was placed on the table,",
      [r"B1 (AO 3.4): Temperature $=83^\circ$C. Notes: Uses the model to state that the temperature $=83^\circ$C "
       r"Requires units as well"],
      False, 16),
    e("08b", "8(b)", EXP, "6.7, 6.3", 3,
      Q8 + r"the value of $t$, to one decimal place, when the temperature of the cup of tea was $35\,^\circ$C.",
      [r"M1 (AO 1.1b): $18+65\mathrm{e}^{-\frac{t}{8}}=35\Rightarrow65\mathrm{e}^{-\frac{t}{8}}=17$. Notes: Uses the "
       r"information and proceeds to $P\mathrm{e}^{\pm\frac{t}{8}}=Q$ condoning slips",
       r"dM1 (AO 1.1b): $t=-8\ln\left(\frac{17}{65}\right)$. Notes: A full method using correct log laws and a "
       r"knowledge that $\mathrm{e}^x$ and $\ln x$ are inverse functions. This cannot be scored from unsolvable "
       r"equations, e.g $P>0, Q<0$. Condone one error in their solution.",
       r"A1 (AO 1.1b): $t=10.7$. Notes: $t=$ awrt 10.7",
       r"ALT: Second scheme column — dM1 (AO 1.1b): $\ln65-\frac{t}{8}=\ln17\Rightarrow t=\ldots$"],
      False, 16),
    e("08c", "8(c)", EXP, "6.7, 6.1", 1,
      Q8 + r"Explain why, according to this model, the temperature of the cup of tea could not fall to $15\,^\circ$C.",
      [r"B1 (AO 2.4): States a suitable reason: As $t\to\infty, \theta\to18$ from above; the minimum temperature is "
       r"$18^\circ$C. Notes: States a suitable reason with minimal conclusion: As $t\to\infty, \theta\to18$ from above; "
       r"The minimum temperature is $18^\circ$C (so it cannot drop to $15^\circ$C); Substitutes $\theta=15$ (or a value "
       r"between 15 and 18) into $18+65\mathrm{e}^{-\frac{t}{8}}=15$ (may be impied by $15-18=-3$ or similar) and makes "
       r"a statement that $\mathrm{e}^{-\frac{t}{8}}$ cannot be less than zero or else that $\ln(-ve)$ is undefined and "
       r"hence $\theta\neq15$. All calculations must be correct; (According to the model) the room temperature is "
       r"$18^\circ$C (so cannot fall below this)"],
      False, 16),
    e("08d", "8(d)", EXP, "6.7, 6.1", 4,
      FIG2 + r"The temperature, $\mu\,^\circ$C, of a second cup of tea $t$ minutes after it was placed on a table in a "
      r"different room, is modelled by the equation $$\mu=A+B\mathrm{e}^{-\frac{t}{8}}\qquad t\geqslant0$$ where $A$ "
      r"and $B$ are constants. Figure 2 shows a sketch of $\mu$ against $t$ with two data points that lie on the curve. "
      r"The line $l$, also shown on Figure 2, is the asymptote to the curve. Using the equation of this model and the "
      r"information given in Figure 2, find an equation for the asymptote $l$.",
      [r"M1 (AO 3.4): $A+B=94$ or $A+B\mathrm{e}^{-1}=50$. Notes: Attempts to use $(0,94)$ or $(8,50)$ in order to "
       r"form at least one equation in $A$ and $B$. Allow this to be scored with an equation containing $\mathrm{e}^0$",
       r"A1 (AO 1.1b): $A+B=94$ and $A+B\mathrm{e}^{-1}=50$. Notes: Correct equations $A+B=94$ and "
       r"$A+B\mathrm{e}^{-1}=50$ or equivalent. $\mathrm{e}^0=1$ must have been processed. Condone $A+B=94$ and "
       r"$A+0.37B=50$ where $\mathrm{e}^{-1}=$ awrt 0.37",
       r"dM1 (AO 2.1): Full method to find at least a value for $A$. Notes: Dependent upon having two equations in $A$ "
       r"and $B$ formed from the information given. It is a full and correct method leading to a value of $A$. Allow "
       r"this to be solved from a calculator. Note $B=69.6..$ or $\frac{44}{1-\mathrm{e}^{-1}}\Rightarrow A=94-$\"$B$\"",
       r"A1 (AO 2.2a): Deduces $\mu=\frac{50\mathrm{e}-94}{\mathrm{e}-1}$ or accept $\mu=$ awrt 24.4. Notes: Deduces "
       r"that $\mu=\frac{50\mathrm{e}-94}{\mathrm{e}-1}$ or accept $\mu=$ awrt 24.4. Condone $y=\ldots$"],
      True, 16),

    # ---------------- Q9 ----------------
    e("09a", "9(a)", TRIG, "5.2", 1, Q9 + r"State the value of $c$ and the value of $d$.",
      [r"B1 (AO 1.1b): $(-180^\circ, -3)$. Notes: Deduces that $P(-180^\circ,-3)$ or $c=-180^{(\circ)}, d=-3$"],
      True, 20),
    e("09b", "9(b)", ALG, "2.8, 5.2", 2,
      Q9 + r"State the coordinates of the point to which $P$ is mapped by the transformation which transforms the curve "
      r"with equation $y=3\cos x^\circ$ to the curve with equation (i) $y=3\cos\left(\frac{x^\circ}{4}\right)$ "
      r"(ii) $y=3\cos(x-36)^\circ$",
      [r"B1ft (AO 2.2a): (i) $(-720^\circ, -3)$. Notes: Deduces that $P'(-720^\circ,-3)$ Follow through on their "
       r"$(c,d)\to(4c,d)$ where $d$ is negative",
       r"B1ft (AO 2.2a): (ii) $(-144^\circ, -3)$. Notes: Deduces that $P'(-144^\circ,-3)$ Follow through on their "
       r"$(c,d)\to(c+36^\circ,d)$ where $d$ is negative"],
      True, 20),
    e("09c", "9(c)", TRIG, "5.4, 5.3", 5,
      Q9 + r"Solve, for $450^\circ\leqslant\theta<720^\circ$, $$3\cos\theta=8\tan\theta$$ giving your solution to one "
      r"decimal place. In part (c) you must show all stages of your working. Solutions relying entirely on calculator "
      r"technology are not acceptable.",
      [r"M1 (AO 3.1a): Attempts to use both $\tan\theta=\frac{\sin\theta}{\cos\theta}$, $\sin^2\theta+\cos^2\theta=1$ "
       r"and solves a quadratic equation in $\sin\theta$ to find at least one value of $\theta$. Notes: An overall "
       r"problem solving mark, condoning slips, for an attempt to: use $\tan\theta=\frac{\sin\theta}{\cos\theta}$; use "
       r"$\pm\sin^2\theta\pm\cos^2\theta=\pm1$; find at least one value of $\theta$ from a quadratic equation in "
       r"$\sin\theta$",
       r"B1 (AO 1.1b): $3\cos\theta=8\tan\theta\Rightarrow3\cos^2\theta=8\sin\theta$. Notes: Uses the correct identity "
       r"and multiplies across to give $3\cos\theta=8\tan\theta\Rightarrow3\cos^2\theta=8\sin\theta$ oe",
       r"M1 (AO 1.1b): $3\sin^2\theta+8\sin\theta-3=0$, $(3\sin\theta-1)(\sin\theta+3)=0$. Notes: Uses the correct "
       r"identity $\sin^2\theta+\cos^2\theta=1$ to form a 3TQ in $\sin\theta$ which they attempt to solve using an "
       r"appropriate method. It is OK to use a calculator to solve this",
       r"A1 (AO 2.2a): $\sin\theta=\frac{1}{3}$. Notes: $\sin\theta=\frac{1}{3}$ Accept sight of $\frac{1}{3}$. Ignore "
       r"any reference to the other root even if it is \"used\"",
       r"A1 (AO 2.1): awrt $520.5^\circ$ only. Notes: Full method with all identities correct leading to the answer of "
       r"awrt $520.5^\circ$ and no other values."],
      True, 20),

    # ---------------- Q10 ----------------
    e("10a", "10(a)", ALG, "2.6", 2, Q10 + r"Use the factor theorem to show that $\mathrm{g}(x)$ is divisible by $(x-5)$.",
      [r"M1 (AO 1.1a): $\mathrm{g}(5)=2\times5^3+5^2-41\times5-70=\ldots$ Notes: Attempts to calculate $\mathrm{g}(5)$. "
       r"Attempted division by $(x-5)$ is M0. Look for evidence of embedded values or two correct terms of "
       r"$\mathrm{g}(5)=250+25-205-70=\ldots$",
       r"A1 (AO 2.4): $\mathrm{g}(5)=0\Rightarrow(x-5)$ is a factor, hence $\mathrm{g}(x)$ is divisible by $(x-5)$. "
       r"Notes: Correct calculation, reason and conclusion. It must follow M1. Accept, for example, "
       r"$\mathrm{g}(5)=0\Rightarrow(x-5)$ is a factor, hence divisible by $(x-5)$; $\mathrm{g}(5)=0\Rightarrow(x-5)$ "
       r"is a factor ✓. Do not allow if candidate states $\mathrm{f}(5)=0\Rightarrow(x-5)$ is a factor, hence divisible "
       r"by $(x-5)$ (It is not f); $\mathrm{g}(x)=0\Rightarrow(x-5)$ is a factor (It is not g(x) and there is no "
       r"conclusion). This may be seen in a preamble before finding $\mathrm{g}(5)=0$ but in these cases there must be "
       r"a minimal statement ie QED, \"proved\", tick etc."],
      False, 24),
    e("10b", "10(b)", ALG, "2.6", 4,
      Q10 + r"(a) Use the factor theorem to show that $\mathrm{g}(x)$ is divisible by $(x-5)$. (b) Hence, showing all "
      r"your working, write $\mathrm{g}(x)$ as a product of three linear factors.",
      [r"M1 (AO 1.1b): $2x^3+x^2-41x-70=(x-5)(2x^2\ldots x\pm14)$. Notes: Attempts to find the quadratic factor by "
       r"inspection (correct coefficients of first term and $\pm$ last term) or by division (correct coefficients of "
       r"first term and $\pm$ second term). Allow this to be scored from division in part (a)",
       r"A1 (AO 1.1b): $=(x-5)(2x^2+11x+14)$. Notes: $(2x^2+11x+14)$ You may not see the $(x-5)$ which can be condoned",
       r"dM1 (AO 1.1b): Attempts to factorise quadratic factor. Notes: Correct attempt to factorise their "
       r"$(2x^2+11x+14)$",
       r"A1 (AO 1.1b): $(\mathrm{g}(x))=(x-5)(2x+7)(x+2)$. Notes: $(\mathrm{g}(x)=)\,(x-5)(2x+7)(x+2)$ or "
       r"$(\mathrm{g}(x)=)\,(x-5)(x+3.5)(2x+4)$. It is for the product of factors and not just a statement of the three "
       r"factors. Attempts with calculators via the three roots are likely to score 0 marks. The question was \"Hence\" "
       r"so the two M's must be awarded."],
      False, 24),
    e("10c", "10(c)", INT, "8.3, 8.2", 4,
      Q10 + r"The finite region $R$ is bounded by the curve with equation $y=\mathrm{g}(x)$ and the $x$-axis, and lies "
      r"below the $x$-axis. Find, using algebraic integration, the exact value of the area of $R$.",
      [r"M1 (AO 1.1b): $\int2x^3+x^2-41x-70\,\mathrm{d}x=\frac{1}{2}x^4+\frac{1}{3}x^3-\frac{41}{2}x^2-70x$. Notes: For "
       r"$x^n\to x^{n+1}$ for any of the terms in $x$ for $\mathrm{g}(x)$ so $2x^3\to\ldots x^4$, $x^2\to\ldots x^3$, "
       r"$-41x\to\ldots x^2$, $-70\to\ldots x$",
       r"A1 (AO 1.1b): $\int2x^3+x^2-41x-70\,\mathrm{d}x=\frac{1}{2}x^4+\frac{1}{3}x^3-\frac{41}{2}x^2-70x$. Notes: "
       r"$\int2x^3+x^2-41x-70\,\mathrm{d}x=\frac{1}{2}x^4+\frac{1}{3}x^3-\frac{41}{2}x^2-70x$ which may be left "
       r"unsimplified (ignore any reference to $+C$)",
       r"M1 (AO 2.2a): Deduces the need to use $\int_{-2}^{5}\mathrm{g}(x)\,\mathrm{d}x$; "
       r"$-\frac{1525}{3}-\frac{190}{3}$. Notes: Deduces the need to use $\int_{-2}^{5}\mathrm{g}(x)\,\mathrm{d}x$. This "
       r"may be awarded from the limits on their integral (either way round) or from embedded values which can be "
       r"subtracted either way round.",
       r"A1 (AO 2.1): Area $=571\frac{2}{3}$. Notes: For clear work showing all algebraic steps leading to area "
       r"$=571\frac{2}{3}$ oe. So allow $\int_{-2}^{5}2x^3+x^2-41x-70\,\mathrm{d}x=\left[\frac{1}{2}x^4+\frac{1}{3}x^3"
       r"-\frac{41}{2}x^2-70x\right]_{-2}^{5}=-\frac{1715}{3}\Rightarrow$ area $=\frac{1715}{3}$ for 4 marks. Condone "
       r"spurious notation, as long as the algebraic steps are correct. If they find $\int_{-2}^{5}\mathrm{g}(x)\,"
       r"\mathrm{d}x$ then withhold the final mark if they just write a positive value to this integral since "
       r"$\int_{-2}^{5}\mathrm{g}(x)\,\mathrm{d}x=-\frac{1715}{3}$. Note "
       r"$\int_{-2}^{5}2x^3+x^2-41x-70\,\mathrm{d}x\Rightarrow\frac{1715}{3}$ with no algebraic integration seen scores "
       r"M0A0M1A0"],
      False, 24),

    # ---------------- Q11 ----------------
    e("11i", "11(i)", COORD, "3.2, 3.1", 5,
      r"A circle $C_1$ has equation $$x^2+y^2+18x-2y+30=0$$ The line $l$ is the tangent to $C_1$ at the point "
      r"$P(-5, 7)$. Find an equation of $l$ in the form $ax+by+c=0$, where $a$, $b$ and $c$ are integers to be found.",
      [r"M1 (AO 1.1b): $x^2+y^2+18x-2y+30=0\Rightarrow(x+9)^2+(y-1)^2=\ldots$ Notes: Attempts $(x\pm9)^2\ldots(y\pm1)^2"
       r"=\ldots$ It is implied by a centre of $(\pm9,\pm1)$",
       r"A1 (AO 1.1b): Centre $(-9,1)$. Notes: States or uses the centre of $C$ is $(-9,1)$",
       r"M1 (AO 1.1b): Gradient of line from $P(-5,7)$ to \"$(-9,1)$\" $=\frac{7-1}{-5+9}=\left(\frac{3}{2}\right)$. "
       r"Notes: A correct attempt to find the gradient of the radius using their $(-9,1)$ and $P$. E.g. "
       r"$\frac{7-\text{\"}1\text{\"}}{-5-\text{\"}-9\text{\"}}$",
       r"dM1 (AO 3.1a): Equation of tangent is $y-7=-\frac{2}{3}(x+5)$. Notes: For the complete strategy of using "
       r"perpendicular gradients and finding the equation of the tangent to the circle. It is dependent upon both "
       r"previous M's. $y-7=-\frac{1}{\text{gradient }CP}(x+5)$ Condone a sign slip on one of the $-7$ or the 5.",
       r"A1 (AO 1.1b): $3y-21=-2x-10\Rightarrow2x+3y-11=0$. Notes: $2x+3y-11=0$ oe such as $k(2x+3y-11)=0, "
       r"k\in\mathbb{Z}$",
       r"ALT: Attempt via implicit differentiation (the first three marks are awarded) — M1: Differentiates "
       r"$x^2+y^2+18x-2y+30=0\Rightarrow\ldots x+\ldots y\frac{\mathrm{d}y}{\mathrm{d}x}+18-2\frac{\mathrm{d}y}"
       r"{\mathrm{d}x}\ldots=0$",
       r"ALT: Attempt via implicit differentiation — A1: Differentiates $x^2+y^2+18x-2y+30=0\Rightarrow2x+2y"
       r"\frac{\mathrm{d}y}{\mathrm{d}x}+18-2\frac{\mathrm{d}y}{\mathrm{d}x}=0$",
       r"ALT: Attempt via implicit differentiation — M1: Substitutes $P(-5,7)$ into their equation involving "
       r"$\frac{\mathrm{d}y}{\mathrm{d}x}$"],
      False, 28),
    e("11ii", "11(ii)", COORD, "3.2, 2.5", 4,
      r"A different circle $C_2$ has equation $$x^2+y^2-8x+12y+k=0$$ where $k$ is a constant. Given that $C_2$ lies "
      r"entirely in the 4th quadrant, find the range of possible values for $k$.",
      [r"M1 (AO 1.1b): $x^2+y^2-8x+12y+k=0\Rightarrow(x-4)^2+(y+6)^2=52-k$. Notes: For reaching "
       r"$(x\pm4)^2+(y\pm6)^2=P-k$ where $P$ is a positive constant. Seen or implied by centre coordinates "
       r"$(\mp4,\mp6)$ and a radius of $\sqrt{P-k}$",
       r"M1 (AO 3.1a): Lies in Quadrant 4 if radius $<4\Rightarrow$ \"$52-k$\" $<4^2$. Notes: Applying the strategy that "
       r"it lies entirely within quadrant if \"their radius\" $<4$ and proceeding to obtain an inequality in k only (See "
       r"scheme). Condone $\ldots\leqslant4$ for this mark.",
       r"A1 (AO 1.1b): $\Rightarrow k>36$. Notes: Deduces that $k>36$",
       r"A1 (AO 3.2a): Deduces $52-k>0\Rightarrow$ Full solution $36<k<52$. Notes: A rigorous argument leading to a full "
       r"solution. In the context of the question the circle exists so that as well as $k>36$ "
       r"$52-k>0\Rightarrow36<k<52$. Allow $36<k\leqslant52$"],
      False, 28),

    # ---------------- Q12 ----------------
    e("12a", "12(a)", EXP, "6.6, 6.4", 4, Q12 + Q12A,
      [r"B1 (AO 2.1): $\log_{10}V=0.072t+2.379\Rightarrow V=10^{0.072t+2.379}\Rightarrow V=10^{0.072t}\times10^{2.379}$. "
       r"Notes: (a) Condone $\log_{10}$ written log or lg written throughout the question. Scored for showing that "
       r"$\log_{10}V=0.072t+2.379$ can be written in the form $V=ab^t$ or vice versa. Either starts with "
       r"$\log_{10}V=0.072t+2.379$ (may be implied) and shows lines $V=10^{0.072t+2.379}$ and "
       r"$V=10^{0.072t}\times10^{2.379}$. Or starts with $V=ab^t$ (implied) and shows the lines "
       r"$\log_{10}V=\log_{10}a+\log_{10}b^t$ and $\log_{10}V=\log_{10}a+t\log_{10}b$",
       r"M1 (AO 1.1b): States either $a=10^{2.379}$ or $b=10^{0.072}$. Notes: For a correct equation in $a$ or a correct "
       r"equation in $b$",
       r"A1 (AO 1.1b): $a=239$ or $b=1.18$. Notes: Finds either constant. Allow $a=$ awrt 240 or $b=$ awrt 1.2 following "
       r"a correct method",
       r"A1 (AO 1.1b): Either $V=239\times1.18^t$ or imply by $a=239, b=1.18$. Notes: Correct solution: Look for "
       r"$V=239\times1.18^t$ or $a=239, b=1.18$. Note that this is NOT awrt",
       r"ALT: Second scheme column — B1 (AO 2.1): $V=ab^t\Rightarrow\log_{10}V=\log_{10}a+\log_{10}b^t\Rightarrow"
       r"\log_{10}V=\log_{10}a+t\log_{10}b$",
       r"ALT: Second scheme column — M1 (AO 1.1b): States either $\log_{10}a=2.379$ or $\log_{10}b=0.072$",
       r"ALT: Second scheme column — A1 (AO 1.1b): $a=239$ or $b=1.18$"],
      False, 32),
    e("12b", "12(b)", EXP, "6.7", 1,
      Q12 + Q12A + r"(b) Interpret, with reference to the model, the value of $ab$.",
      [r"B1 (AO 3.4): The value of $ab$ is the (total) number of views of the advert 1 day after it went live. Notes: "
       r"See scheme. Condone not seeing total. Do not allow number of views at the start or similar."],
      False, 32),
    e("12c", "12(c)", EXP, "6.7", 2,
      Q12 + r"Using this model, calculate the total number of views of the advert in the first 20 days after the "
      r"advert went live. Give your answer to 2 significant figures.",
      [r"M1 (AO 3.4): Substitutes $t=20$ in either equation and finds $V$ Eg $V=239\times1.18^{20}$. Notes: "
       r"Substitutes $t=20$ in either their $V=239\times1.18^t$ or $\log_{10}V=0.072t+2.379$ and uses a correct method "
       r"to find $V$",
       r"A1 (AO 1.1b): Awrt 6500 or 6600. Notes: Awrt 6500 or 6600"],
      False, 32),

    # ---------------- Q13 ----------------
    e("13a", "13(a)", PROOF, "1.1", 4, Q13A,
      [r"M1 (AO 2.1): States $(2a-b)^2\geqslant0$. Notes: (a) (condone the use of $>$ for the first three marks) For the "
       r"key step in stating that $(2a-b)^2\geqslant0$",
       r"A1 (AO 1.1b): $4a^2+b^2\geqslant4ab$. Notes: Reaches $4a^2+b^2\geqslant4ab$",
       r"M1 (AO 2.2a): (As $a>0, b>0$) $\frac{4a^2}{ab}+\frac{b^2}{ab}\geqslant\frac{4ab}{ab}$. Notes: Divides each term "
       r"by $ab\Rightarrow\frac{4a^2}{ab}+\frac{b^2}{ab}\geqslant\frac{4ab}{ab}$",
       r"A1* (AO 1.1b): Hence $\frac{4a}{b}+\frac{b}{a}\geqslant4$ * CSO. Notes: Fully correct proof with steps in the "
       r"correct order and gives the reasons why this is true: when you square any (real) number it is always greater "
       r"than or equal to zero; dividing by $ab$ does not change the inequality as $a>0$ and $b>0$",
       r"ALT: Proof by contradiction (scores all marks) — M1: Assume that there exists an $a,b>0$ such that "
       r"$\frac{4a}{b}+\frac{b}{a}<4$",
       r"ALT: Proof by contradiction — A1: $4a^2+b^2<4ab\Rightarrow4a^2+b^2-4ab<0$",
       r"ALT: Proof by contradiction — M1: $(2a-b)^2<0$",
       r"ALT: Proof by contradiction — A1*: States that this is not true, hence we have a contradiction so "
       r"$\frac{4a}{b}+\frac{b}{a}\geqslant4$ with the following reasons given: when you square any (real) number it is "
       r"always greater than or equal to zero; dividing by $ab$ does not change the inequality as $a>0$ and $b>0$",
       r"ALT: Attempt starting with the left-hand side — M1: "
       r"$(\text{lhs}=)\,\frac{4a}{b}+\frac{b}{a}-4=\frac{4a^2+b^2-4ab}{ab}$",
       r"ALT: Attempt starting with the left-hand side — A1: $=\frac{(2a-b)^2}{ab}$",
       r"ALT: Attempt starting with the left-hand side — M1: $=\frac{(2a-b)^2}{ab}\geqslant0$",
       r"ALT: Attempt starting with the left-hand side — A1*: Hence $\frac{4a}{b}+\frac{b}{a}-4\geqslant0\Rightarrow"
       r"\frac{4a}{b}+\frac{b}{a}\geqslant4$ with the following reasons given: when you square any (real) number it is "
       r"always greater than or equal to zero; $ab$ is positive as $a>0$ and $b>0$",
       r"ALT: Attempt using given result (for 3 out of 4) — M1: $\frac{4a}{b}+\frac{b}{a}\geqslant4\Rightarrow"
       r"4a^2+b^2\geqslant4ab\Rightarrow4a^2+b^2-4ab\geqslant0$",
       r"ALT: Attempt using given result — A1: $\Rightarrow(2a-b)^2\geqslant0$ oe",
       r"ALT: Attempt using given result — M1: gives both reasons why this is true: \"square numbers are greater than or "
       r"equal to 0\"; \"multiplying by $ab$ does not change the sign of the inequality because $a$ and $b$ are "
       r"positive\""],
      False, 36),
    e("13b", "13(b)", PROOF, "1.1", 1,
      Q13A + r"(b) Prove, by counter example, that this is not true for all values of $a$ and $b$.",
      [r"B1 (AO 2.4): $a=5, b=-1\Rightarrow\frac{4a}{b}+\frac{b}{a}=-20-\frac{1}{5}$ which is less than 4. Notes: "
       r"Provides a counter example and shows it is not true. This requires values, a calculation or embedded values "
       r"(see scheme) and a conclusion. The conclusion must be in words eg the result does not hold or not true. Allow 0 "
       r"to be used as long as they explain or show that it is undefined so the statement is not true."],
      False, 36),

    # ---------------- Q14 ----------------
    e("14a", "14(a)", DIFF, "7.3, 2.4", 7, Q14 + r"find $\mathrm{g}(x)$,",
      [r"B1 (AO 2.2a): Deduces $\mathrm{g}(x)=ax^3+bx^2+ax$. Notes: Uses the information given to deduce that "
       r"$\mathrm{g}(x)=ax^3+bx^2+ax$. (Seen or implied)",
       r"M1 (AO 2.1): Uses $(2,9)\Rightarrow9=8a+4b+2a$. Notes: Uses the fact that $(2,9)$ lies on the curve so uses "
       r"$x=2, y=9$ within a cubic function",
       r"A1 (AO 1.1b): $\Rightarrow10a+4b=9$. Notes: For a simplified equation in just two variables. E.g. $10a+4b=9$",
       r"M1 (AO 2.1): Uses $\mathrm{g}'(2)=0\Rightarrow0=12a+4b+a$. Notes: Differentiates their cubic to a quadratic and "
       r"uses the fact that $\mathrm{g}'(2)=0$ to obtain an equation in $a$ and $b$.",
       r"A1 (AO 1.1b): $\Rightarrow13a+4b=0$. Notes: For a different simplified equation in two variables E.g. "
       r"$13a+4b=0$",
       r"dM1 (AO 1.1b): Solves simultaneously $\Rightarrow a,b$. Notes: Solves simultaneously $\Rightarrow a=\ldots, "
       r"b=\ldots$ It is dependent upon the B and both M's",
       r"A1 (AO 1.1b): $\mathrm{g}(x)=-3x^3+\frac{39}{4}x^2-3x$. Notes: $\mathrm{g}(x)=-3x^3+\frac{39}{4}x^2-3x$"],
      False, 38),
    e("14b", "14(b)", DIFF, "7.3", 2, Q14 + r"(a) find $\mathrm{g}(x)$, (b) prove that the stationary point at "
      r"$(2, 9)$ is a maximum.",
      [r"M1 (AO 1.1b): Attempts $\mathrm{g}''(x)=-18x+\frac{39}{2}$ and substitutes $x=2$. Notes: Attempts "
       r"$\mathrm{g}''(x)=-18x+\frac{39}{2}$ and substitutes $x=2$. Award for second derivatives of the form "
       r"$\mathrm{g}''(x)=Ax+B$ with $x=2$ substituted in.",
       r"A1 (AO 2.4): $\mathrm{g}''(2)=-\frac{33}{2}<0$ hence maximum. Notes: $\mathrm{g}''(2)=-\frac{33}{2}<0$ hence "
       r"maximum. (allow embedded values but they must refer to the sign or that it is less than zero). Note If they "
       r"only sketch the cubic function $\mathrm{g}(x)=-3x^3+\frac{39}{4}x^2-3x$ then award M1A0",
       r"ALT: Alternatively (b) — M1 (AO 1.1b): Alternatively attempts to find the value of their $\mathrm{g}'(x)$ or "
       r"$\mathrm{g}(x)$ either side of $x=2$ (by substituting a value for $x$ within 0.5 either side of 2)",
       r"ALT: Alternatively (b) — A1 (AO 2.4): If $\mathrm{g}'(x)=-9x^2+\frac{39}{2}x-3$ or "
       r"$\mathrm{g}(x)=-3x^3+\frac{39}{4}x^2-3x$ is calculated either side of $x=2$ then the values must be correct or "
       r"embedded correctly (you will need to check these) they need to compare $\mathrm{g}'(x)>0$ to the left of $x=2$ "
       r"and $\mathrm{g}'(x)<0$ to the right of $x=2$ or $\mathrm{g}(x)<9$ to the left and $\mathrm{g}(x)>9$ to the "
       r"right of $x=2$ hence maximum."],
      False, 38),
]

# Examiner report, sentence by sentence, in report order.
# Bulleted lists are joined into the sentence that introduces them, with "; ".
# A sentence that mentions another part only in passing is tagged with the
# part it is about. The report calls Q3's parts (a) and (b); the paper
# numbers them (i) and (ii).
W = None
NO = {"ref": False}
BACK = {"ref": True}
REPORT = {
    "01": [
        (W, "This question was generally answered well with most candidates scoring full marks."),
        (W, r"Most candidates were confident in differentiating the cubic correctly and substituting in $x=2$ to find "
            r"the gradient, although a few incorrectly set their gradient equal to 0 and attempted to solve to find $x$."),
        (W, r"The majority of candidates were then able to use their gradient and the given point to correctly find the "
            r"equation of the tangent, although a few candidates incorrectly thought that they needed to use the "
            r"negative reciprocal of their gradient instead to find the equation of the normal at $P$."),
    ],
    "02": [
        ({"a", "b"}, "Candidates found the first part of this question challenging, but they were more successful "
                     "with the second part, with many fully correct responses."),
        ({"a"}, "There were a number of common mistakes in candidates’ approaches to part (a)."),
        ({"a"}, "Firstly, many candidates tried to find the resultant vector by adding the two given vectors, rather "
                "than subtracting them."),
        ({"a"}, "Secondly, candidates seemed unclear on exactly what angle the question was looking for, with lots of "
                "time being spent on finding various different (but unfortunately not relevant) angles in their "
                "diagrams."),
        ({"a"}, r"Finally, some candidates took a rather long-winded approach to find the correct angles (through use "
                r"of the cosine rule to find one part of the required answer, then additional work using tan) as they "
                r"had not spotted the more straightforward use of $\arctan\frac{7}{3}$."),
        ({"a"}, "Even those who found a relevant angle were often unable to proceed to find a bearing.", NO),
        ({"b"}, "Part (b) was generally answered successfully, with a few candidates mistakenly stating that 2 hours "
                "and 45 minutes was equal to 2.45 hours, rather than 2.75 hours."),
    ],
    "03": [
        (W, "This question really highlighted the dependence on calculators amongst candidates."),
        ({"i", "ii"}, "Part (a) required simple rationalisation of a denominator and part (b) wanted candidates to "
                      "work with indices/bases."),
        ({"i", "ii"}, "In part (a) they perhaps did not fully appreciate the wording at the top of the question "
                      "‘Solutions relying on calculator technology are not acceptable’, whilst in part (b) they did "
                      "not have the algebra skills to solve on their own."),
        ({"i"}, r"In part (a), when squaring both sides many candidates squared each individual term before combining "
                r"the $x^2$; they seemed happier factorising the $x$ out when the coefficients were rational numbers."),
        ({"i"}, r"In a similar vein, many instead simplified the $\sqrt{18}$ and then factored out a common $\sqrt{2}$, "
                r"leaving multiple $x$ terms in the equation."),
        ({"i"}, "Some candidates opted to square both sides."),
        ({"i"}, "Where a correct quadratic was built and solved, candidates gave both roots and lost the final mark."),
        ({"i"}, r"Where $x$ was found with an irrational denominator, most candidates then went on to rationalise the "
                r"denominator, but neglected to show the steps."),
        ({"i"}, "In many cases it was clear they had typed into the calculator and read off the simplified display.", BACK),
        ({"i"}, "When the question says ‘not relying on calculator technology’ candidates should be showing each step "
                "to secure the marks."),
        ({"i"}, r"The $\sqrt{18}$ must also be simplified when writing in simplest form."),
        ({"ii"}, "In part (b) log base 10 or natural logs were commonly used, and these could only be evaluated on "
                 "the calculator.", NO),
        ({"ii"}, "These scored no marks.", BACK),
        ({"ii"}, r"Even where attempts were made to use logs to base 4 or 2 there was an over reliance on calculators "
                 r"to find $\log_4\frac{1}{2\sqrt{2}}$."),
        ({"ii"}, "The most common approach was to immediately take log base 4 and simplify the left-hand side."),
        ({"ii"}, r"There was then often little evidence of how they got from $\log_4\frac{1}{2\sqrt{2}}$ to "
                 r"$-\frac{3}{4}$."),
        ({"ii"}, "Those who chose to rewrite as common bases more often led to full marks; base 2 was most common.",
         NO),
        (W, "Whilst the use of calculator technology is encouraged on the new specification, candidates should make "
            "sure that they are confident of working without one when required."),
    ],
    "04": [
        (W, "This question focussed largely on the problem-solving assessment objective, AO3, and was those "
            "candidates who were familiar with linear models scored full marks.", NO),
        ({"b"}, "The algebra was generally well done, whilst the written component in part (b) really assessed who "
                "knew what the modelling aspect was all about."),
        ({"a"}, "In part (a) the first part of the question was generally well done with most finding at least the "
                "gradient or the intercept."),
        ({"a"}, r"Some candidates worked using $x$ and $y$, although they should make sure that their final answer is "
                r"in terms of the given variables."),
        ({"a"}, r"One area of confusion was in the definition of the variable $n$."),
        ({"a"}, r"Some candidates did not read the detail of the question which stated that $n$ was the number of "
                r"years past 1997- not simply the date (number of years AD)."),
        ({"a"}, r"Whilst they still found a linear equation, it was not the correct one linking $A$ and $n$.", NO),
        ({"a"}, "There were some candidates who tried to form an arithmetic sequence, too."),
        ({"b"}, r"In part (b) the common approach was to substitute $n=19$ in to the model found in part (a), scoring "
                r"2 marks for a correct answer."),
        ({"b"}, "Where candidates used the dates in part (a), they could still find the correct value for the year "
                "2016 with their model."),
        ({"b"}, "When commenting on the suitability of the model candidates need to make sure they comment on the "
                "model, as opposed to explaining what external factors may have been resulted in the figures being "
                "different."),
        ({"b"}, "It was pleasing to see that less candidates made the comment that the model is not suitable because "
                "the value predicted and the actual value are not the same which does not demonstrate an "
                "understanding of a model.", NO),
        ({"b"}, "Equally, just comparing the values without making a judgement on suitability is also insufficient."),
    ],
    "05": [
        (W, "With the exception of the first 2 marks, this was quite a polarising question that either scored very "
            "well or little at all.", NO),
        (W, "Those who went through to part (b) with an incorrect diagram and understanding of the question found it "
            "very difficult to make sense of the sides.", NO),
        (W, "It was only after abandoning this line of thought and starting afresh did some candidates manage to "
            "salvage the question.", BACK),
        ({"a"}, "In part (a), the first couple of marks were scored by the vast majority of candidates using the sine "
                "rule to find 51.1 degrees."),
        ({"a"}, "From there, an overwhelming number neglected to solve for the obtuse angle; those who did left both "
                "answers.", BACK),
        ({"a"}, "Many even labelled their obtuse angle on the diagram as 51.1 degrees."),
        ({"a"}, "Candidates should always be checking solutions to equations to ensure they make sense in context and "
                "are well defined."),
        ({"a"}, "As the 128.9 degrees was appearing as a complementary angle in part (b), it was important to state it "
                "unambiguously here as credit could not be gained for it seen later in the question.", NO),
        ({"b"}, "In part (b), depending on the answer to part (a), there were a couple of possible configurations that "
                "would lead to different answers."),
        ({"b"}, r"After labelling the triangle, candidates had the choice of the sine rule or cosine rule to find the "
                r"missing side $AD$."),
        ({"b"}, r"Those who mislabelled in part (a) tended to over work this, believing they had only found $AC$ and "
                r"still had to find another side, so it was condoned that they may have started again, allowing full "
                r"marks to be achieved if they reached the answer of 42 m.", NO),
        ({"b"}, "Candidates should keep sight of the bigger picture by looking at the sum of angles in the right most "
                "triangle."),
        ({"b"}, "Hardly any noticed that they had two base angles of the isosceles triangle of 128.9 degrees."),
        ({"b"}, "There should always be an internal consistency, even when some individual value might have been "
                "calculated incorrectly."),
    ],
    "06": [
        ({"a"}, "The binomial expansion seemed a welcome relief with many candidates achieving full marks in part (a)."),
        ({"a"}, "The usual problems with exponents crept in but fortunately there were no ‘negatives raised to "
                "powers’ to contend with."),
        ({"b"}, "The simple equation in part (b) was not answered quite as well but coefficients were followed through "
                "from part (a) allowing some marks if they multiplied the correct expression by 3."),
        ({"a"}, r"In part (a), candidates answered this well with a mix of methods due to the expression being of the "
                r"form $(1+\ldots)^n$.", NO),
        ({"a"}, r"The most common mistake was to not raise $k$ to the various powers as well as the $x$."),
        ({"a"}, "Some candidates were one step out in their binomial expansion such that the coefficients did not "
                "match the term.", NO),
        ({"a"}, r"A few candidates found expansions in decreasing powers of $x$ and could not score any marks."),
        ({"b"}, "In part (b), those who got an answer for part (a) would usually achieve at least the first mark in "
                "part (b).", NO),
        ({"b"}, "Some candidates were unable to form a correct equation for the coefficients and simply set them equal "
                "to each other without multiplying the linear term by 3."),
        ({"b"}, "There was a small number of cases where the wrong side was multiplied by 3."),
        ({"b"}, r"It was disappointing that a large number are still uncomfortable with the term “coefficient” as there "
                r"were a lot of scripts that kept the $x$ and $x^3$ in the equation and even tried to solve to find "
                r"$x$.", NO),
        ({"b"}, r"Others removed the $x$ and $x^3$ later on, but this should be discouraged as a general approach.",
         NO),
    ],
    "07": [
        ({"a", "b"}, "The first part of this question was generally answered well with many candidates scoring full "
                     "marks, but the second part proved to be more challenging for a disappointing number of them.",
         NO),
        ({"a"}, r"In part (a), some candidates struggled with either rearranging the $\frac{5}{2\sqrt{x}}$ term to the "
                r"form $\frac{5}{2}x^{-\frac{1}{2}}$ or with getting the correct coefficient when integrating this to "
                r"$5x^{\frac{1}{2}}$.", NO),
        ({"a"}, "However, the majority of candidates were then confident in substituting both limits into their "
                "expression, subtracting and setting their result equal to 4, then rearranging correctly to get the "
                "required equation."),
        ({"b"}, r"In part (b), some candidates struggled with identifying the given equation as a hidden three term "
                r"quadratic, with a few trying unsuccessfully to simplify by multiplying every term by $k$, for "
                r"example."),
        ({"b"}, "Some candidates tried to square both sides but were mostly let down in this approach by mistakes in "
                "expanding out the brackets or simply squaring individual terms."),
        ({"b"}, r"Those candidates who were successful often proceeded by setting $y=\sqrt{k}$, for example, and "
                r"proceeding correctly to two values, which they then squared, but a number did not realise that they "
                r"needed to discard the solution of $\sqrt{k}=-3$.", NO),
        ({"b"}, r"Some candidates confused themselves by setting $\sqrt{k}=k$ to produce a three term quadratic in $k$ "
                r"but then failed to realise they had not found the actual value for $k$."),
    ],
    "08": [
        (W, "This question was another which focussed on problem solving, with the majority of candidates only able "
            "to score around half of the marks available."),
        ({"d"}, "Part (d), in particular proved to be too difficult for most candidates so it was rare to see full "
                "marks.", NO),
        ({"a"}, "In part (a), many candidates could score at least one mark here by calculating the value of 83, "
                "however, it was not uncommon for units to be omitted which meant that the mark was not awarded.", NO),
        ({"b"}, "In part (b), the majority of candidates scored full marks here and seemed very comfortable with the "
                "fact that ln is the inverse."),
        ({"b"}, "There were some slips with rearrangements of the equation, which was often dividing by 8 rather than "
                "multiplying by 8."),
        ({"b"}, "It was evident that some candidates used their calculators to solve the equation without "
                "demonstrating any method.", NO),
        ({"b"}, "Candidates should be encouraged to show all of their working, to ensure that full marks can be "
                "scored."),
        ({"c"}, "Most candidates were successful in part (c), which may have been due to the graph having been "
                "provided."),
        ({"c"}, r"Many stated $18\,^\circ$C as being the minimum temperature of the model which was condoned for the "
                r"mark, although a significant number stated that “$15\,^\circ$C is the room temperature” which did "
                r"not show an understanding of the model."),
        ({"c"}, "The other most popular way to answer the question was to substitute 15 into the equation and "
                "concluded that you cannot log a negative."),
        ({"c"}, "Just stating that “you can’t log a negative” without providing the working to back this up was not "
                "sufficient as it was not enough evidence that the candidate had engaged with the model.", NO),
        ({"d"}, "Part (d) caused more issues than the rest of the question for candidates."),
        ({"d"}, r"Several of them assumed $A$ was equal to 94 and therefore did not score highly in this part."),
        ({"d"}, "Some candidates attempted to find the gradient between the given coordinates and therefore did not "
                "score any marks."),
        ({"d"}, r"However, once candidates formed the two simultaneous equations, they seemed to find it quite easy to "
                r"use the elimination method to eliminate $A$, and then go on to correctly solve for $A$ and $B$ and "
                r"therefore work out the equation of the asymptote.", NO),
    ],
    "09": [
        ({"c"}, "This question was attempted by most candidates with many being able to secure nearly all the marks in "
                "part (c)."),
        ({"b"}, "It was rare, however, for full marks to be scored overall, with most struggling with the "
                "transformations in part (b).", NO),
        ({"a"}, r"In part (a), candidates occasionally got their signs mixed up, or did not appreciate the vertical "
                r"stretch of scale factor 3 and therefore $d=-1$."),
        ({"a"}, r"Some even had their $d$ being positive, despite the diagram showing that $P$ was below the "
                r"horizontal axis."),
        ({"b"}, r"In part (b), candidates could still score marks for acceptable follow throughs as long as $d$ was a "
                r"negative value."),
        ({"b"}, "This enabled some candidates to score usually one of the marks.", BACK),
        ({"b"}, r"Some mixed up the horizontal stretch of scale factor 4 and scale factor $\frac{1}{4}$ in part (i) and "
                r"mixed up a translation of 36 units in the positive $x$-direction with 36 units in the negative "
                r"$x$-direction."),
        ({"b"}, r"There were some candidates who only stated the $x$ coordinate whereas the question asked for the "
                r"coordinates, so they were unable to score in this part."),
        ({"c"}, "Part (c) proved to be high scoring for many candidates, however, some did not recall the identities "
                "correctly and made little progress."),
        ({"c"}, r"In particular, candidates made errors with rearranging $\sin^2x+\cos^2x=1$ or missing the square from "
                r"either or both terms."),
        ({"c"}, r"The given interval was unusual, although it was pleasing to see many of the candidates who proceeded "
                r"to find a value for $\theta$ were able to find the one that was in the required interval.", NO),
    ],
    "10": [
        (W, "This question was answered well by the majority of candidates."),
        (W, "However, the question highlights the need for detail in proof and ‘show that’ questions which candidates "
            "are clearly still getting used to; it appeared to be even the more able candidates were neglecting to "
            "state facts that were needed.", NO),
        (W, "Candidates should be encouraged to make sure they provide sufficient reasoning when demonstrating a "
            "result or writing a proof."),
        ({"c"}, "The final part requiring integration, whilst not penalised, brought out a lot of poor notation."),
        ({"c"}, "Candidates were able to score most marks, however."),
        ({"c"}, "Those who understood the nature of the curve and the importance of the factors and roots found "
                "earlier were able to choose the correct bounds and, usually, go on to achieve full marks.", NO),
        ({"a"}, "In part (a), there were 2 main errors on this question, with almost all candidates getting only 1 "
                "mark."),
        ({"a"}, "The question asked candidates to use the factor theorem, however, there were a significant number "
                "who still chose to use polynomial division and could not score marks in this part."),
        ({"a"}, r"Those who found $\mathrm{g}(5)$ to equal 0 then stopped (or simply stated hence it is a factor) were "
                r"also not actually answering the question.", NO),
        ({"a"}, "This was about divisibility which was a slight change to many of the questions on this topic in the "
                "past.", NO),
        ({"a"}, r"Therefore, not only did candidates need to show that $\mathrm{g}(5)=0$ means that $x-5$ is a factor, "
                r"but also some acknowledgement and understanding that a factor divides perfectly and without this the "
                r"answer was incomplete.", NO),
        ({"b"}, "In part (b), whether they used polynomial division or used their calculator to solve and work back, "
                "most candidates were able to find the 3 factors."),
        ({"b"}, "The biggest problem was when candidates worked backwards from the roots given by their calculator and "
                "did not expand to check."),
        ({"b"}, r"They wrote $(x+3.5)$ rather than $(2x+7)$ (or equivalent)."),
        ({"b"}, "The question clearly asked candidates to use algebra and they should make sure their working "
                "demonstrates that.", NO),
        ({"c"}, "In part (c), those who attempted the question typically integrated correctly; however, it was very "
                "mixed when it came to evaluating.", NO),
        ({"c"}, "There were a number of poor graph sketches and some did not recognise which area they were actually "
                "finding and chose the wrong bounds for the integral."),
        ({"c"}, "When evaluating the integral there were solutions lacking brackets which resulted in sign errors."),
        ({"c"}, "Although the integral evaluates to be negative, the area is the magnitude of this.", NO),
        ({"c"}, "If the bounds were used in ascending order, then it was expected to see the negative answer before "
                "the positive solution.", NO),
        ({"c"}, "It was acceptable, following candidates carrying out algebraic integration visibly, that they used "
                "their calculator to substitute in their limits and could still score full marks.", NO),
    ],
    "11": [
        ({"i", "ii"}, "Candidates were generally successful in answering the first part of this question, but found "
                      "the second part more challenging, with only a few gaining full marks."),
        ({"i"}, "In part (i), most candidates were confident in completing the square to find the coordinates of the "
                "centre of the circle, and many could then successfully find the gradient of the line from the centre "
                "to the given point."),
        ({"i"}, "There were still a number of candidates who made sign errors when finding the gradient, however."),
        ({"i"}, "Some candidates forgot to then find the negative reciprocal of this gradient in order to find the "
                "tangent, and a few did not give their final answer in the requested form, but this was generally "
                "answered well.", NO),
        ({"i"}, "Candidates should be reminded to check the form that the answer should be given in to ensure that "
                "they score marks that they are more than capable of achieving.", NO),
        ({"ii"}, r"In part (ii), again most candidates were confident in completing the square and finding the radius "
                 r"of this circle in terms of $k$, but a number then stated this radius needed to be less than 6, rather "
                 r"than saying it needed to be less than 4.", NO),
        ({"ii"}, r"There were a large number who made errors just rearranging the equation resulting in the radius as "
                 r"$\sqrt{52+k}$."),
        ({"ii"}, r"Only a very small number of candidates picked up the final mark for realising that, in addition to "
                 r"$k>36$, we also required $k<52$ in order for the circle to actually exist."),
    ],
    "12": [
        (W, "This question proved to be more challenging for candidates than was anticipated."),
        (W, r"There were a large number of candidates who did not attempt the question at all, or of those who did, "
            r"most seemed to struggle with showing the relationship between the log form of the equation and "
            r"$V=ab^t$.", NO),
        (W, "It was very rare for full marks to be achieved, with most securing around half of the available marks "
            "in total for the question.", NO),
        ({"a"}, "In part (a) many candidates were able to correctly calculate the value for ‘a’ and ‘b’, however, they "
                "lost marks due to the fact that they did not appreciate the “show that” nature of the question."),
        ({"a"}, r"Missing out writing both $\log V=\log a+\log b^t$ and $\log V=\log a+t\log b$ was common and this "
                r"resulted in the first mark.", NO),
        ({"a"}, "As it was an incomplete solution, candidates also lost the final mark, too.", NO),
        ({"a"}, r"A number of candidates rounded both of their values to the nearest whole number, which was only "
                r"required for $a$."),
        ({"a"}, r"This was only penalised if they never had $b=1.18$ at some point.", BACK),
        ({"a"}, "Usually, candidates had lost the first mark anyway from insufficient working, so it rarely was the "
                "reason for not achieving full marks.", BACK),
        ({"b"}, "Very few candidates were successful in part (b)."),
        ({"b"}, r"Most went with a standard response of stating it was the “the initial number of views” which was "
                r"incorrect as $t$ could not be 0.", NO),
        ({"b"}, r"Had they just copied the relevant part at the start of the question replacing $t$ with one, they "
                r"would have scored the mark."),
        ({"c"}, "In part (c) candidates could either use their formula from part (a) or use the formula given in the "
                "question, so it did not rely on the candidates getting correct answers to part (a) or (b).", NO),
        ({"c"}, r"The majority of candidates who attempted this question were successful, or at least gained the method "
                r"mark, if their values for $a$ and $b$ were incorrect."),
        ({"c"}, r"When using the given formula, several candidates were able to calculate the value of $\log_{10}V$, "
                r"however, they did not know how to then proceed to calculate the value of $V$."),
    ],
    "13": [
        ({"a", "b"}, "This proved to be a challenging question with only a few candidates scoring full marks in the "
                     "first part, although more candidates were successful with the second part.", NO),
        ({"a"}, r"In part (a), the expected approach was to begin with some known true statement, such as "
                r"$(2a-b)^2\geqslant0$, and then to argue logically, step by step, until you arrived at the statement "
                r"given in the question.", NO),
        ({"a"}, "Most candidates incorrectly began by using the given statement and then proceeding, which meant that "
                "they could not score full marks."),
        ({"a"}, r"The algebraic processing was generally well done, meaning most candidates scored 2 out of the "
                r"available 4 marks, but most lost the final mark by not including full detail of their reasoning "
                r"(squaring a real number will always give an answer greater than or equal to zero and, since both $a$ "
                r"and $b$ are positive, multiplying the inequality through by $ab$ will not change the inequality "
                r"sign)."),
        ({"b"}, "In part (b), many candidates realised that the result does not hold if one value is positive and one "
                "is negative."),
        ({"b"}, "However, a calculation is not enough for a proof, and a conclusion in words was necessary in order to "
                "obtain the mark."),
        ({"b"}, "It was disappointing that many still opted to just state the inequality the other way round or not "
                "provide a conclusion at all.", NO),
        ({"b"}, "Other candidates did not substitute their values in correctly, or their answer for the expression on "
                "the left-hand side was incorrect."),
    ],
    "14": [
        (W, "The final question was not attempted in a significant number of cases."),
        (W, "This may have been due to the demand of the question for the majority of candidates.", BACK),
        (W, "Of those candidates who did attempt this question, it was rare for full marks to be achieved.", NO),
        ({"a"}, "In part (a), candidates struggled with getting started which then cost them dearly."),
        ({"a"}, "They seemed to struggle with forming an equation without being given one, despite it being a cubic "
                "equation, which then meant they lacked the confidence to pursue any further.", NO),
        ({"a"}, "Common errors were not appreciating that there was no constant term which meant they produced "
                "simultaneous equations with too many unknowns."),
        ({"a"}, r"Others knew they needed to differentiate $\mathrm{g}(x)$ and sub in $x=2$ but then they equated it to "
                r"9 and not 0.", NO),
        ({"a"}, "Clearly having lots of information provided at the same time and having to select which is "
                "appropriate for each stage of their working the majority of candidates found difficult."),
        ({"a"}, r"The lack of understanding surrounding coefficients may have led to not being able to set up the cubic "
                r"with the coefficients for $x^3$ and $x$ being the same."),
        ({"a"}, "Some even assigned numerical values rather than unknowns."),
        ({"a"}, r"There were some candidates who were able to form two simultaneous equations, however, and most of "
                r"these successfully found $a$ and $b$.", NO),
        ({"a"}, "They were asked to find the function, so it was essential that they did state their answer at the "
                "end to score full marks in this part.", NO),
        ({"b"}, r"In part (b), if candidates were able to come up with a cubic for part (a), they usually appreciated "
                r"the need to differentiate to find the second derivative and substitute in $x=2$."),
        ({"b"}, "Their knowledge on second derivatives meant they knew it would need to be negative to prove it was a "
                "maximum.", NO),
        ({"b"}, "However, there were a number of candidates who had incorrect derivatives or evaluated incorrectly and "
                "still stated they had a maximum, even though their answer would have been positive."),
        ({"b"}, "This, for some, should have prompted further investigation into their earlier work.", BACK),
        ({"b"}, r"Some candidates still substituted in a value of $x$ either side of $x=2$ into either $\mathrm{g}(x)$ "
                r"or $\mathrm{g}'(x)$."),
        ({"b"}, "This was far more working to score both marks, so candidates should be encouraged with this type of "
                "question to prove the nature of the turning points using second derivatives.", BACK),
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
    "01": ("easy", at("01", "This question was generally answered well")),
    "02a": ("hard", at("02", "Candidates found the first part")),
    "02b": ("easy", at("02", "Part (b) was generally answered successfully")),
    "03i": ("medium", at("03", "Where $x$ was found with an irrational denominator")),
    "03ii": ("hard", at("03", "In part (b) log base 10")),
    "04a": ("easy", at("04", "In part (a) the first part of the question was generally well done")),
    "04b": ("medium", at("04", "In part (b) the common approach")),
    "05a": ("hard", at("05", "From there, an overwhelming number")),
    "05b": ("medium", at("05", "With the exception of the first 2 marks")),
    "06a": ("easy", at("06", "The binomial expansion seemed a welcome relief")),
    "06b": ("medium", at("06", "The simple equation in part (b)")),
    "07a": ("easy", at("07", "However, the majority of candidates were then confident")),
    "07b": ("medium", at("07", "The first part of this question")),
    "08a": ("medium", at("08", "In part (a), many candidates could score")),
    "08b": ("easy", at("08", "In part (b), the majority of candidates scored full marks")),
    "08c": ("easy", at("08", "Most candidates were successful in part (c)")),
    "08d": ("hard", at("08", "Part (d), in particular proved to be too difficult")),
    "09a": ("easy", at("09", "In part (a), candidates occasionally")),
    "09b": ("hard", at("09", "It was rare, however, for full marks")),
    "09c": ("easy", at("09", "Part (c) proved to be high scoring")),
    "10a": ("hard", at("10", "In part (a), there were 2 main errors")),
    "10b": ("easy", at("10", "In part (b), whether they used polynomial division")),
    "10c": ("medium", at("10", "In part (c), those who attempted the question")),
    "11i": ("easy", at("11", "Some candidates forgot to then find the negative reciprocal")),
    "11ii": ("hard", at("11", "Only a very small number of candidates")),
    "12a": ("hard", at("12", "In part (a) many candidates were able")),
    "12b": ("hard", at("12", "Very few candidates were successful in part (b)")),
    "12c": ("easy", at("12", "The majority of candidates who attempted this question")),
    "13a": ("hard", at("13", "The algebraic processing was generally well done")),
    "13b": ("medium", at("13", "In part (b), many candidates realised")),
    "14a": ("hard", at("14", "In part (a), candidates struggled")),
    "14b": ("medium", at("14", "In part (b), if candidates were able")),
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
