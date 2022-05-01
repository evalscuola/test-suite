#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from collections import OrderedDict
from typing import Dict, Tuple

MATRICES = (
    r"\matrix",
    r"\matrix*",
    r"\pmatrix",
    r"\pmatrix*",
    r"\bmatrix",
    r"\bmatrix*",
    r"\Bmatrix",
    r"\Bmatrix*",
    r"\vmatrix",
    r"\vmatrix*",
    r"\Vmatrix",
    r"\Vmatrix*",
    r"\array",
)

SPACES = (r"\,", r"\:", r"\;", r"\\", r"\quad", r"\qquad")

COMMANDS = {
    # command: (params_count, mathml_equivalent, attributes)
    "_": (2, "m:msub", {}),
    "^": (2, "m:msup", {}),
    "_^": (3, "m:msubsup", {}),
    r"\frac": (2, "m:mfrac", {}),
    r"\sqrt": (1, "m:msqrt", {}),
    r"\root": (2, "m:mroot", {}),
    r"\binom": (2, "m:mfrac", {"linethickness": "0"}),
    r"\left": (
        1,
        "m:mo",
        OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")]),
    ),
    r"\right": (
        1,
        "m:mo",
        OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "postfix")]),
    ),
    r"\overline": (1, "m:mover", {}),
    r"\bar": (1, "m:mover", {}),
    r"\underline": (1, "m:munder", {}),
}  # type: Dict[str, Tuple[int, str, dict]]

for space in SPACES:
    COMMANDS[space] = (0, "m:mspace", {"width": "0.167em"})

for matrix in MATRICES:
    COMMANDS[matrix] = (1, "m:mtable", {})
