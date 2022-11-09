from memory.shared.config import *

def concept1(x, y):
    temp = str(x ** y)
    temp = temp[::-1]
    return int(temp)

def concept2(a, b, c, d):
    return (a / b) / (c / d)

def concept3(a, b, c):
    return a / (b * c)

def concept4(a, b):
    return (b / a) + (b ** a)

def concept5(a, b, c):
    return (c - b) / a

step_counts = [1, 2, 1, 2, 1]

concepts = [
    concept1,
    concept2,
    concept3,
    concept4,
    concept5
]

def get_state_field(name, value, editable=False):
    s = {
        'id': name,
        'value': f'{value}',
        'contentEditable': editable,
    }
    if PLANNER == "numba":
      s['type'] = 'TextField' # Needed for numba planner

    return s