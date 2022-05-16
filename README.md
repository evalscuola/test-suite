# evaluatest

It is used to compute the scores and the cheating index of test results.


# maketest

From a database of questions the program creates
a number of versions of the test in pdf with the
questions and answers rearranged in a different
order.

It is written in Python 2.7 on a Mac, uses the
library pdfrw and a LaTeX distribution.


# smrt

Smrt converts students' scores to curved grades,
i.e. whatever the initial distribution of the scores,
the distribution of the grades is a gaussian bell
curve.

# checktest

Checktest performs some simple item analysis in classical test theory. In particular check.py computes difficulty index and discrimination index for the items of the test and produces a table with the percentages, while frequency-graphs.py creates two graphs for the two indices.

It is written in Python 3 on a Mac computer and there is really a lot of space for improvement.
