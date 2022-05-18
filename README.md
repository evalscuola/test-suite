# Test Suite

**Test Suite** is a set of Python 3 scripts to manage tests.

## maketest qti-export

**maketest** creates a PDF file with
a number of versions of the test from a database of items
with the questions and answers rearranged in a different
order. It uses a LaTeX distribution.

**qti-export** creates the QTI file of the items
from the maketest format, to be used for example
in Tao Testing.


## evaluatest smrt checktest

**evaluatest** is used to compute the scores
and the cheating index of test results.

**smrt** converts students' scores to curved grades,
i.e. whatever the initial distribution of the scores,
the distribution of the grades is a gaussian bell
curve.

**checktest** performs some simple item analysis in
classical test theory. In particular check.py computes
difficulty index and discrimination index for the items
of the test and produces a table with the percentages,
while frequency-graphs.py creates two graphs for the two indices.


## additems

**additems** creates the files of the maketest format.
