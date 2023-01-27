### ALGEBRA ###

STUDY_PROBLEM_NUM = 10
# CONCEPTS = [2, 3, 4]
CONCEPTS = [1, 2, 3, 4, 5]
CONCEPT_NUM = len(CONCEPTS)
SELECTED_PROBLEMS = list(map(str, CONCEPTS))

DEBUG = True
AGENT_TYPE = 'memory'
# AGENT_TYPE = 'modular'
PLANNER = 'numba'

### GEOMETRY ###

FIX = 2
PIKS1 = [["fact", "circle", FIX],
        ["fact", "triangle", FIX],
        ["fact", "rectangle", FIX],
        ["fact", "trapezoid", FIX],
        ["skill", "circle", FIX],
        ["skill", "triangle", FIX],
        ["skill", "rectangle", FIX],
        ["skill", "trapezoid", FIX]]

PIKS2 = [["fact", "circle", 11],
        ["fact", "triangle", 5],
        ["fact", "rectangle", 3],
        ["fact", "trapezoid", 3],
        ["skill", "circle", 3],
        ["skill", "triangle", 3],
        ["skill", "rectangle", 3],
        ["skill", "trapezoid", 3]]

PIKS3 = [["skill", "trapezoid", 3]]

FIX_FACT = 2
FIX_SKILL = 1
PIKS4 = [["fact", "circle", FIX_FACT],
        ["fact", "triangle", FIX_FACT],
        ["fact", "rectangle", FIX_FACT],
        ["fact", "trapezoid", FIX_FACT],
        ["skill", "circle", FIX_SKILL],
        ["skill", "triangle", FIX_SKILL],
        ["skill", "rectangle", FIX_SKILL],
        ["skill", "trapezoid", FIX_SKILL]]

PIKS = PIKS4

SHAPES = ["circle", "triangle", "rectangle", "trapezoid"]

