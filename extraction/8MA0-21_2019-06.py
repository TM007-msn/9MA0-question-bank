"""Draft builder for 8MA0-21 2019-06 (AS Paper 2: Statistics, June 2019).

Run (from the project root, with the venv active):
    python extraction/8MA0-21_2019-06.py        # writes out/drafts/8MA0-21_2019-06.json
then save with:
    python scripts/add_entries.py out/drafts/8MA0-21_2019-06.json

Everything here is transcribed from the source PDFs (read as page images
where the text layer garbles maths; the Venn diagram at 200 dpi). Follow
CLAUDE.md for every field.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from er_notes import apply_report, part_key  # noqa: E402
from mark_codes import main_marks  # noqa: E402
from paths import ensure_out_dir  # noqa: E402

P, S = "8MA0-21", "2019-06"
SRC = f"{P}_{S}_QP.pdf"


def e(q, label, topic, spec, marks, latex, ms, diagram, page):
    """One entry. q is the id tail after Q (e.g. "04d"); label as printed (e.g. "4(d)")."""
    return {"id": f"{P}_{S}_Q{q}", "paper": P, "series": S, "question": label, "topic": topic,
            "spec_ref": spec, "marks": marks, "question_latex": latex, "mark_scheme": ms,
            "examiner_notes": None, "difficulty": None, "difficulty_evidence": None,
            "has_diagram": diagram, "source_page": page, "source_file": SRC}


SAMP = "Statistical sampling"
DATA = "Data presentation and interpretation"
PROB = "Probability"
DIST = "Statistical distributions"
HYP = "Statistical hypothesis testing"


def L(*lines):
    """question_latex from printed lines (CLAUDE.md: question_latex content and order)."""
    return "\n".join(lines)


# ---------------- shared stems and parts ----------------
Q1 = ["A sixth form college has 84 students in Year 12 and 56 students in Year 13",
      "The head teacher selects a stratified sample of 40 students, stratified by year group."]
Q1R = ["The head teacher is investigating the relationship between the amount of sleep, $s$ hours, that each student "
       "had the night before they took an aptitude test and their performance in the test, $p$ marks.",
       "For the sample of 40 students, he finds the equation of the regression line of $p$ on $s$ to be",
       "$$p=26.1+5.60s$$"]

FIGV = (r"[Figure: a Venn diagram in a rectangle with three overlapping circles, $A$ (top left), $B$ (top right) and "
        r"$C$ (bottom). The regions are: $A$ only, 0.10; $B$ only, 0.30; $C$ only, 0.39; $A$ and $B$ but not $C$, $y$; "
        r"$A$ and $C$ but not $B$, $z$; $B$ and $C$ but not $A$, $x$; all three, 0; outside the circles, 0.06.]")

Q3 = ["A fair 5-sided spinner has sides numbered 1, 2, 3, 4 and 5",
      "The spinner is spun once and the score of the side it lands on is recorded."]

Q4 = ["Joshua is investigating the daily total rainfall in Hurn for May to October 2015",
      "Using the information from the large data set, Joshua wishes to calculate the mean of the daily total rainfall "
      "in Hurn for May to October 2015"]
Q4T = ["Using the information from the large data set, he produces the grouped frequency table below.",
       r"$$\begin{array}{|c|c|c|}\hline\text{Daily total rainfall }(r\text{ mm})&\text{Frequency}&\text{Midpoint }"
       r"(x\text{ mm})\\\hline0\leqslant r<0.5&121&0.25\\\hline0.5\leqslant r<1.0&10&0.75\\\hline1.0\leqslant r<5.0&"
       r"24&3.0\\\hline5.0\leqslant r<10.0&12&7.5\\\hline10.0\leqslant r<30.0&17&20.0\\\hline\end{array}$$",
       r"You may use $\sum fx=539.75$ and $\sum fx^2=7704.1875$"]

Q5 = ["Past records show that 15% of customers at a shop buy chocolate. The shopkeeper believes that moving the "
      "chocolate closer to the till will increase the proportion of customers buying chocolate.",
      "After moving the chocolate closer to the till, a random sample of 30 customers is taken and 8 of them are found "
      "to have bought chocolate.",
      "Julie carries out a hypothesis test, at the 5% level of significance, to test the shopkeeper’s belief.",
      "Julie’s hypothesis test is shown below.",
      r"$\mathrm{H_0}:p=0.15$", r"$\mathrm{H_1}:p\geqslant0.15$",
      "Let $X=$ the number of customers who buy chocolate.", r"$X\sim\mathrm{B}(30, 0.15)$",
      r"$\mathrm{P}(X=8)=0.0420$", r"$0.0420<0.05$ so reject $\mathrm{H_0}$",
      "There is sufficient evidence to suggest that the proportion of customers buying chocolate has increased."]
Q5A = "Identify the first two errors that Julie has made in her hypothesis test."
Q5C = ["Find, using a 5% level of significance, the critical region for a one-tailed test of the shopkeeper’s belief. "
       "The probability in the tail should be less than 0.05"]

LATEX = {
    "01a": L(*Q1, "Describe how this sample could be taken."),
    "01b": L(*Q1, *Q1R,
             "With reference to this equation, describe the effect that an extra 0.5 hours of sleep may have, on "
             "average, on a student’s performance in the aptitude test."),
    "01c": L(*Q1, *Q1R, "Describe one limitation of this regression model."),
    "02": L("The Venn diagram shows three events, $A$, $B$ and $C$, and their associated probabilities.", FIGV,
            "Events $B$ and $C$ are mutually exclusive.", "Events $A$ and $C$ are independent.",
            "Showing your working, find the value of $x$, the value of $y$ and the value of $z$."),
    "03a": L(*Q3, "Write down the name of the distribution that can be used to model the score of the side it lands "
                  "on."),
    "03b": L(*Q3, "The spinner is spun 28 times.",
             "The random variable $X$ represents the number of times the spinner lands on 2",
             "(i) Find the probability that the spinner lands on 2 at least 7 times.",
             r"(ii) Find $\mathrm{P}(4\leqslant X<8)$"),
    "04a": L(*Q4, "Using your knowledge of the large data set, explain why Joshua needs to clean the data before "
                  "calculating the mean."),
    "04b": L(*Q4, *Q4T, "Use linear interpolation to calculate an estimate for the upper quartile of the daily total "
                        "rainfall."),
    "04c": L(*Q4, *Q4T, "Calculate an estimate for the standard deviation of the daily total rainfall in Hurn for May "
                        "to October 2015"),
    "04d": L(*Q4, *Q4T, "(i) State the assumption involved with using class midpoints to calculate an estimate of a "
                        "mean from a grouped frequency table.",
             "(ii) Using your knowledge of the large data set, explain why this assumption does not hold in this case.",
             "(iii) State, giving a reason, whether you would expect the actual mean daily total rainfall in Hurn for "
             "May to October 2015 to be larger than, smaller than or the same as an estimate based on the grouped "
             "frequency table."),
    "05a": L(*Q5, Q5A),
    "05b": L(*Q5, "(a) " + Q5A,
             "(b) Explain whether or not these errors will affect the conclusion of her hypothesis test.",
             "Give a reason for your answer."),
    "05c": L(*Q5, *Q5C),
    "05d": L(*Q5, "(c) " + Q5C[0], "(d) Find the actual level of significance of this test."),
}

DRAFT = [
    # ---------------- Q1 ----------------
    e("01a", "1(a)", SAMP, "1.1", 3, LATEX["01a"],
      [r"B1 (AO 1.1b): Label $\textbf{each}$ year group. Notes: for a suitable numbered/labelled/ordered(o.e.) "
       r"list/database/register(o.e.) for $\textbf{each}$ year group. Condone poor numbering but if just one list, then "
       r"the Year 12s must be distinguishable from the Year 13s Note: A description of a systematic sample: only allow "
       r"access to the first mark and therefore may score maximum B1B0B0",
       r"B1 (AO 1.1b): Use random numbers to select a ... Notes: for use of random numbers/sample/selection to choose "
       r"students",
       r"B1 (AO 1.1b): Simple random sample of 24 Year 12s and 16 Year 13s. Notes: for 24 Year 12s, and 16 Year 13s"],
      False, 2),
    e("01b", "1(b)", DATA, "2.2", 1, LATEX["01b"],
      [r"B1 (AO 3.4): Increase by 2.8 marks. Notes: Using the gradient of the regression equation must include "
       r"increase(o.e.) and 2.8 ‘Increase by approximately 3 marks’ is B0 but isw if 2.8 is seen $5.6\div2$ is not "
       r"sufficient"],
      False, 2),
    e("01c", "1(c)", DATA, "2.2", 1, LATEX["01c"],
      [r"B1 (AO 3.5b): e.g. ‘the best performance is predicted for the students who never wake up’. Notes: for any "
       r"suitable limitation of the model e.g. the idea that the longer you sleep the better performance in the test or "
       r"only valid between 0 and 24 hours (within range of the data) or only applicable to the amount of sleep the "
       r"night before the test or only takes sleep into consideration/does not include other variables (factors) or "
       r"cannot score below 26.1 marks on the test or the model might not be linear over the entire range or the model "
       r"might predict more than the maximum mark B0: e.g. might not be correlation between $s$ and $p$ or individual "
       r"student performance may vary"],
      False, 2),

    # ---------------- Q2 ----------------
    e("02", "2", PROB, "3.1", 5, LATEX["02"],
      [r"B1 (AO 2.2a): $x=0$. Notes: for $x=0$, may be seen on Venn diagram",
       r"M1 (AO 2.1): $\mathrm{P}(A)=0.1+z+y$ $\mathrm{P}(C)=0.39+z[+x]$ $\mathrm{P}(A\text{ and }C)=z$. Notes: "
       r"Identifying the probabilities required for independence and at least 2 correct These must be labelled If there "
       r"are no labels, then this may be implied by $z=(0.1+z+y)(0.39+z\,[+x])$, allow one numerical slip Allow e.g. "
       r"$\mathrm{P}(A')=0.39+0.30+0.06[+x]$ $\mathrm{P}(C)=0.39+z[+x]$ $\mathrm{P}(A'\text{ and }C)=0.39$ [Not on "
       r"spec. but you may see use of conditional probabilities]",
       r"M1 (AO 1.1b): $\mathrm{P}(A\text{ and }C)=\mathrm{P}(A)\times\mathrm{P}(C)\to z=(0.1+z+y)\times(0.39+z[+x])$. "
       r"Notes: Use of independence equation with their labelled probabilities in terms $y$, $z$ [and $x$] All their "
       r"probabilities must be substituted into a correct formula Sight of a correct equation e.g. "
       r"$z=(0.1+z+y)(0.39+z\,[+x])$ scores M1M1",
       r"M1 (AO 1.1b): $\left[\sum p=1\right]$ $0.06+0.3+0.39+0.1+z+y[+x]=1\to[z+y[+x]=0.15]$. Notes: Using "
       r"$\Sigma p=1$ Implied by $[x+]\ y+z=0.15$ or their $x+y+z=0.15$ where $x$, $y$, and $z$ are all probabilities "
       r"or e.g. $\mathrm{P}(A)=0.25$",
       r"A1 (AO 1.1b): Solving (simultaneously) leading to $z=0.13$ $y=0.02$. Notes: both $y=0.02$ and $z=0.13$"],
      True, 4),

    # ---------------- Q3 ----------------
    e("03a", "3(a)", DIST, "4.1", 1, LATEX["03a"],
      [r"B1 (AO 1.2): (Discrete) uniform (distribution). Notes: Continuous uniform is B0"],
      False, 6),
    e("03b", "3(b)", DIST, "4.1", 5, LATEX["03b"],
      [r"B1 (AO 3.3): $\mathrm{B}(28, 0.2)$. Notes: for identifying correct model, $\mathrm{B}(28, 0.2)$ allow B, bin "
       r"or binomial may be implied by one correct answer or sight one correct probability i.e. awrt 0.678, awrt 0.818 "
       r"or awrt 0.160 $\mathrm{B}(0.2, 28)$ is B0 unless it is used correctly",
       r"M1 (AO 3.4): (i) $\mathrm{P}(X\geqslant7)=1-\mathrm{P}(X\leqslant6)$ $[=1-0.6784\ldots]$. Notes: Writing or "
       r"using $1-\mathrm{P}(X\leqslant6)$ or $1-\mathrm{P}(X<7)$",
       r"A1 (AO 1.1b): awrt 0.322. Notes: awrt 0.322 (correct answer only scores M1A1)",
       r"M1 (AO 3.1b): (ii) $\mathrm{P}(4\leqslant X<8)=\mathrm{P}(X\leqslant7)-\mathrm{P}(X\leqslant3)$ "
       r"$[=0.818\ldots-0.160\ldots]$. Notes: Writing or using $\mathrm{P}(X\leqslant7)-\mathrm{P}(X\leqslant3)$ or "
       r"$\mathrm{P}(X<8)-\mathrm{P}(X<4)$ or $\mathrm{P}(X=4)+\mathrm{P}(X=5)+\mathrm{P}(X=6)+\mathrm{P}(X=7)$ "
       r"Condone P(4) as $\mathrm{P}(X=4)$, etc.",
       r"A1 (AO 1.1b): awrt 0.658. Notes: awrt 0.658 (correct answer only scores M1A1)"],
      False, 6),

    # ---------------- Q4 ----------------
    e("04a", "4(a)", DATA, "2.4", 1, LATEX["04a"],
      [r"B1 (AO 2.4): Tr(ace) (data needs to be converted to numbers before the calculation can be carried out). Notes: "
       r"Identifying tr(ace) data Ignore comments about n/a, missing data, anomalies, etc."],
      False, 8),
    e("04b", "4(b)", DATA, "2.3", 2, LATEX["04b"],
      [r"M1 (AO 2.1): $[1+]\frac{138-131}{24}\times4$. Notes: Correct fraction $\frac{7}{24}\times4$ allow working down "
       r"$[5]-\frac{155-138}{24}\times4$ allow a correct equation leading to a correct fraction e.g. "
       r"$\frac{x-1}{5-1}=\frac{138-131}{155-131}$ for M1 Use of $(n+1)$ with 138.75 allow $\frac{7.75}{24}\times4$",
       r"A1 (AO 1.1b): $=2.1666\ldots$ awrt 2.17. Notes: awrt 2.17 (condone $\frac{13}{6}$) awrt 2.29 from $(n+1)$ "
       r"(condone $\frac{55}{24}$)"],
      False, 8),
    e("04c", "4(c)", DATA, "2.3", 2, LATEX["04c"],
      [r"M1 (AO 1.1b): $\sigma=\sqrt{\frac{7704.1875}{184}-\left(\frac{539.75}{184}\right)^2}=5.7676\ldots$ Notes: "
       r"Correct expression for standard deviation (allow mean $=$ awrt 2.93)",
       r"A1 (AO 1.1b): $\sigma=$ awrt 5.77. Notes: awrt 5.77 correct answer only scores M1A1 (allow $s=5.78$) SC: 5.76 "
       r"with no working scores M1A0"],
      False, 8),
    e("04d", "4(d)", DATA, "2.3, 2.4", 3, LATEX["04d"],
      [r"B1 (AO 2.4): (i) Using class midpoints to estimate the mean assumes that the values are uniformly distributed "
       r"$\textbf{within the class(es)}$. Notes: Explaining that data assumed to be spread evenly across each class "
       r"(o.e.) e.g. The midpoint of each class is the mean of each class or all the values in the class are located at "
       r"the midpoint condone normally distributed within each class",
       r"B1 (AO 2.3): (ii)&(iii) This is not the case here as the majority of the data (in the first class) are 0. "
       r"Notes: Mark together (ii)&(iii) Demonstrating an understanding of the LDS that the majority of data values (in "
       r"the first class) are at 0 or close to 0 (trace).",
       r"dB1 (AO 2.2b): The actual mean is likely to be smaller than the estimate (since the first group has more "
       r"values at 0 and close to 0). Notes: (dependent upon 2nd B1) Correct inference based on knowledge of the LDS SC: "
       r"If B1 is scored in (i) for ‘The data are spread evenly across each class,’ then in (ii) ‘The data are not "
       r"evenly distributed in the classes’ scores B1 but in (iii) ‘the actual mean is smaller’ with no further "
       r"justification scores B0"],
      False, 8),

    # ---------------- Q5 ----------------
    e("05a", "5(a)", HYP, "5.1, 5.2", 2, LATEX["05a"],
      [r"B1 (AO 2.5): The alternative hypothesis should be $\mathrm{H_1}:p>0.15$. Notes: Identifying that $\geqslant$ "
       r"should be $>$ in the alternative hypothesis",
       r"B1 (AO 2.3): The calculation of the test statistic should be $\mathrm{P}(X\geqslant8)$ $[=0.0698]$. Notes: "
       r"Identifying that $\mathrm{P}(X=8)$ should be $\mathrm{P}(X\geqslant8)$ Stating $\mathrm{P}(X=8)$ is incorrect "
       r"on its own is insufficient Check for errors identified and corrected next to the question"],
      False, 12),
    e("05b", "5(b)", HYP, "5.2, 5.1", 1, LATEX["05b"],
      [r"B1 (AO 2.4): These will affect the conclusion (as the null hypothesis should not be rejected) since "
       r"$\mathrm{P}(X\geqslant8)$ $[=0.0698]$ is greater than 0.05. Notes: Will affect conclusion $\textbf{and}$ "
       r"correct supporting reason"],
      False, 12),
    e("05c", "5(c)", HYP, "5.1, 5.2", 2, LATEX["05c"],
      [r"M1 (AO 2.1): $\mathrm{P}(X\leqslant8)=0.9722\ldots>0.95$ or $\mathrm{P}(X\geqslant9)=0.0277\ldots<0.05$. "
       r"Notes: For use of tables to find probability associated with critical value [$\mathrm{P}(X\leqslant8)$ or "
       r"$\mathrm{P}(X\geqslant9)$ with $\mathrm{B}(30, 0.15)$ (may be implied by either correct probability awrt 0.97 or "
       r"awrt 0.03) or by the correct CR]",
       r"A1 (AO 1.1b): CR: $\{X\geqslant9\}$. Notes: $[30\geqslant]X\geqslant9$ o.e. e.g. $X>8$ Allow ‘9 or more’ or "
       r"‘CR $\geqslant9$’"],
      False, 12),
    e("05d", "5(d)", HYP, "5.1", 1, LATEX["05d"],
      [r"B1ft (AO 1.1b): awrt 0.0278. Notes: awrt 0.0278 (allow awrt 2.78%) or correct ft their one-tailed upper CR "
       r"from $\mathrm{B}(30, 0.15)$ to 3s.f."],
      False, 12),
]

# Examiner report, sentence by sentence, in report order.
W = None
NO = {"ref": False}
BACK = {"ref": True}
INTRO = "Still over a quarter of candidates made no progress at all on Q2, Q3 and Q5."
REPORT = {
    "01": [
        ({"a"}, "This proved to be an accessible start to the paper with most scoring at least 1 mark in part (a) for "
                "a partial description of a stratified sample.", NO),
        ({"a"}, "Very few gained the first mark for clearly describing the method of splitting the population into two "
                "groups and labelling these groups.", NO),
        ({"a"}, "Most realised that a random sample must be taken within each strata and the correct calculation for "
                "the number of candidates for each year group was commonly seen."),
        ({"b"}, "In part (b), most candidates scored the mark for indicating both ‘increase’ and ‘2.8’."),
        ({"b"}, "A minority however worked out the number of points scored when $s = 0.5$."),
        ({"b"}, "Others just mentioned the ‘increase’ but failed to quantify it appropriately.", NO),
        ({"c"}, "Part (c) was very well answered and most gained a mark here by coming up with a plausible limitation "
                "of the model."),
        ({"c"}, "The majority referred to ‘other factors affecting performance’ or ‘not specifying a range so "
                "candidates could not score less than 26.1 marks or could get infinitely high marks’."),
    ],
    "02": [
        (W, INTRO),
        (W, "Only around 10% of candidates achieved full marks on this question, but there were many strong attempts "
            "made."),
        (W, "Most scored the first mark for identifying that $x = 0$."),
        (W, r"The most common error across the question was to ignore the intersections and calculate "
            r"$\mathrm{P}(A)\times\mathrm{P}(C)$ as $0.1\times0.39$."),
        (W, "The majority of candidates scored the final method mark for a correct equation in $y$ and $z$, "
            "demonstrating knowledge of probabilities summing to 1."),
        (W, "Surprisingly, of candidates who did set up all of the equations required, many were unable to manipulate "
            "the algebra to solve them."),
        (W, "Those who confused independent and mutually exclusive events tended to make no progress.", NO),
    ],
    "03": [
        (W, INTRO),
        (W, "Whilst over half of candidates were able to score at least 3 marks on this question, only 3% went on to "
            "achieve full marks."),
        ({"a"}, "Virtually all candidates struggled to name the distribution in part (a) with the vast majority "
                "opting for ‘binomial’."),
        ({"a"}, "It would appear that the ‘uniform’ distribution is a topic unfamiliar to many candidates.", NO),
        ({"b"}, r"Part (b)(i) was well answered as most candidates correctly identified the binomial distribution "
                r"required here and confidently used $1-\mathrm{P}(X\leqslant6)$ to calculate "
                r"$\mathrm{P}(X\geqslant7)$."),
        ({"b"}, r"Usual errors were seen, notably attempting $1-\mathrm{P}(X\leqslant7)$."),
        ({"b"}, "Whilst there was some good use of calculators seen, a significant amount of candidates are still "
                "calculating these probabilities out by hand in full which costs them a large amount of time.", BACK),
        ({"b"}, "Candidates are expected to use their calculators to find binomial probabilities and cumulative "
                "probabilities from the binomial distribution."),
        ({"b"}, "Part (b)(ii) was more discriminating and correct attempts here were rare."),
        ({"b"}, r"The most common mistake was made by those candidates who found $\mathrm{P}(X\leqslant7)$ and "
                r"subtracted $\{1-\mathrm{P}(X\leqslant3)\}$ from it.", NO),
        ({"b"}, r"Those who wrote out the required probabilities in full, i.e. $\mathrm{P}(X=4)+\mathrm{P}(X=5)+"
                r"\mathrm{P}(X=6)+\mathrm{P}(X=7)$, tended to score full marks.", NO),
    ],
    "04": [
        ({"a"}, "In part (a) most candidates referred to data that was n/a, anomalies or outliers with only a small "
                "proportion appreciating that the data set contained trace values for rainfall which needed replacing "
                "with numerical values."),
        ({"b"}, "For part (b) most candidates are familiar with using linear interpolation though slips appear often."),
        ({"b"}, "Errors with endpoints often resulted in multiplication by 5."),
        ({"b"}, "Other mistakes included 23 in the denominator or 6 on the numerator."),
        ({"b"}, "For those using an $(n + 1)$ method, it was not uncommon to see 7.5 being used in the numerator "
                "instead of 7.75.", NO),
        ({"c"}, "In part (c) most candidates were able to use the given information to arrive at the required result."),
        ({"c"}, "There are still a large number of candidates who do not work to the appropriate degree of accuracy "
                "and 5.8 and 5.76 were often seen."),
        ({"c"}, "Candidates are encouraged to write down all figures from their calculator before rounding to ensure "
                "accuracy marks are scored."),
        ({"c"}, "Those who did not achieve full marks here often had an incorrect denominator or forgot to include "
                "the square root.", NO),
        ({"d"}, "The underlying assumption in part (d)(i) was generally identified but not always with sufficient "
                "clarity to gain the mark."),
        ({"d"}, "Common errors were: ‘data uniformly distributed’ (failing to mention within each class); the average "
                "of each class is the midpoint (failing to specify the mean of each class); most of the data is "
                "located at the midpoint (failing to identify that the midpoint is assumed to represent all of the "
                "data)."),
        ({"d"}, "It was clear from the responses seen here that many candidates have little or no experience with the "
                "large data set.", NO),
        ({"d"}, "In (d)(ii) quite a number referred to the data being based on weather which is unpredictable and "
                "that therefore the previous assumption was unrealistic."),
        ({"d"}, "Good explanations involving the distribution of the bottom class were rare with very few making "
                "reference to the majority of data being either 0 or close to 0."),
        ({"d"}, "Little progress was made in (d)(iii) as many mentioned irrelevancies such as the great storm or the "
                "fact that it was during the summer or that the database did not cover a full year.", NO),
        ({"d"}, "Many did not realise that they were comparing an estimated mean with an actual mean for the same "
                "time span and said the actual mean would be higher because the winter months were excluded."),
    ],
    "05": [
        (W, INTRO),
        (W, "Only the most able candidates on the paper made significant progress through this question on "
            "hypothesis testing."),
        ({"a"}, "In part (a) the first error in writing down the alternative hypothesis was identified and corrected "
                "more often than the error in the probability statement."),
        ({"a"}, "Some candidates lost the marks by identifying where the error was but without correctly identifying "
                "what the error was."),
        ({"a"}, "It was not uncommon for candidates to say that the probability distribution was used rather than the "
                "cumulative distribution; likely referring to calculator functions rather than demonstrating a formal "
                "understanding of hypothesis testing.", NO),
        ({"b"}, "Part (b) was less successfully done and where attempted the mark was not always awarded because "
                "insufficient details of the calculation and its implication were given."),
        ({"c"}, "Despite the question stating the test should be one-tailed in part (c) some candidates found a "
                "two-tail critical region or went for the left hand tail rather than the right hand one."),
        ({"c"}, r"Where the upper tail was found the critical region was usually correct although some gave a "
                r"critical value rather than a region or wrote it as a probability i.e. $\mathrm{P}(X\geqslant9)$.",
         NO),
        ({"c"}, "Some candidates rewrote Julia’s hypothesis test correctly at this point, not appreciating the "
                "difference between this and a critical region approach.",
         {"ref": False, "note": "the question paper names her Julie"}),
        ({"d"}, "Part (d) was usually correctly done by those who were successful in part (c).", NO),
        ({"d"}, "On some occasions answers were given only to two significant figures."),
        (W, "Just over 5% of candidates scored full marks on the final question on this paper."),
    ],
}

# Difficulty by judgement (rubric in CLAUDE.md): part key -> (rating, (question, sentence index)).
RATINGS = {
    "01a": ("medium", ("01", 1)),
    "01b": ("easy", ("01", 3)),
    "01c": ("easy", ("01", 6)),
    "02": ("hard", ("02", 1)),
    "03a": ("hard", ("03", 2)),
    "03b": ("hard", ("03", 8)),
    "04a": ("hard", ("04", 0)),
    "04b": ("medium", ("04", 1)),
    "04c": ("easy", ("04", 5)),
    "04d": ("hard", ("04", 13)),
    "05a": ("medium", ("05", 2)),
    "05b": ("hard", ("05", 5)),
    "05c": ("medium", ("05", 7)),
    "05d": ("medium", ("05", 9)),
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
