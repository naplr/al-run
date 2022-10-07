from apprentice.working_memory.representation import Sai
from random import randint

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


def generate_sai(val, selection='answer', action="UpdateTextField"):
    return Sai(selection=selection, action=action, inputs={'value': f'{val}'})


def get_state_field(name, value, editable=False):
    return {
        # 'dom_class': 'CTATTextInput',
        # 'offsetParent': 'background-initial',
        'id': name,
        'type': 'TextField',
        'value': f'{value}',
        'contentEditable': editable,
    }

# Should we get rid of step_i from Fact?
def get_state_and_answer(p):
    state = {
        'r1c1': get_state_field('r1c1', '', False),
        'r1c2': get_state_field('r1c2', '', False),
        'r1c3': get_state_field('r1c3', '', False),
        'r1c4': get_state_field('r1c4', '', False),
        'r1c5': get_state_field('r1c5', '', False),
        'r1c6': get_state_field('r1c6', '', False),
        'r1c7': get_state_field('r1c7', '', False),
        'r1c8': get_state_field('r1c8', '', False),
        'r1c9': get_state_field('r1c9', '', False),
        'r1c10': get_state_field('r1c10', '', False),
        'r1c11': get_state_field('r1c11', '', False),
        'r2c1': get_state_field('r2c1', '', True),
        'r2c2': get_state_field('r2c2', '', True),
        'r2c3': get_state_field('r2c3', '', True),
        'r2c4': get_state_field('r2c4', '', True),
        'r2c5': get_state_field('r2c5', '', True),
        'r2c6': get_state_field('r2c6', '', True),
        'r2c7': get_state_field('r2c7', '', True),
        'r2c8': get_state_field('r2c8', '', True),
        'r2c9': get_state_field('r2c9', '', True),
        'r2c10': get_state_field('r2c10', '', True),
        'r2c11': get_state_field('r2c11', '', True),
        'r3c1': get_state_field('r3c1', '', True),
        'r3c2': get_state_field('r3c2', '', True),
        'r3c3': get_state_field('r3c3', '', True),
        'r3c4': get_state_field('r3c4', '', True),
        'r3c5': get_state_field('r3c5', '', True),
        'r3c6': get_state_field('r3c6', '', True),
        'r3c7': get_state_field('r3c7', '', True),
        'r3c8': get_state_field('r3c8', '', True),
        'r3c9': get_state_field('r3c9', '', True),
        'r3c10': get_state_field('r3c10', '', True),
        'r3c11': get_state_field('r3c11', '', True),
        'answer': get_state_field('answer', '', True),
        # 'concept': get_state_field('concept', f"concept-{p['concept']}"),
    }

    populate_states(p, state)
    answer = p['ans']
    choices = p['choices']

    # for k in state:
    #     state[k]['is_empty'] = state[k]['value'] == ''

    return state, answer, choices, get_steps(p)


def populate_1(args, state):
    state['r1c1'] = args[0]
    state['r1c2'] = 'DIAMOND'
    state['r1c3'] = args[1]


def populate_2(args, state):
    state['r1c1'] = get_state_field('r1c1', '(', False)
    state['r1c2'] = get_state_field('r1c1',args[0], False)
    state['r1c3'] = get_state_field('r1c1',',', False)
    state['r1c4'] = get_state_field('r1c1',args[1], False)
    state['r1c5'] = get_state_field('r1c1',')', False)
    state['r1c6'] = get_state_field('r1c1','SUN', False)
    state['r1c7'] = get_state_field('r1c1','(', False)
    state['r1c8'] = get_state_field('r1c1',args[2], False)
    state['r1c9'] = get_state_field('r1c1',',', False)
    state['r1c10'] = get_state_field('r1c1',args[3], False)
    state['r1c11'] = get_state_field('r1c1',')', False)


populate_funcs = [populate_1, populate_2]
def populate_states(p, state):
    concept = p['concept']
    populate_funcs[int(concept)-1](p['args'], state)

def get_foa(concept):
    if concept == '1':
        return [
            ('arg_1_concept_1', 'arg_2_concept_1'),
            ('step_1_concept_1', ),
        ]

    if concept == '2':
        return [
            ('arg_1_concept_2', 'arg_2_concept_2'),
            ('arg_3_concept_2', 'arg_4_concept_2'),
            ('step_1_concept_2', 'step_2_concept_2'),
        ]

    if concept == '3':
        return [
            ('arg_2_concept_3', 'arg_3_concept_3'),
            ('arg_1_concept_3', 'step_1_concept_3'),
        ]

    if concept == '4':
        return [
            ('arg_1_concept_4', 'arg_2_concept_4'),
            ('arg_1_concept_4', 'arg_2_concept_4'),
            ('step_1_concept_4', 'step_2_concept_4'),
        ]

    if concept == '5':
        return [
            ('arg_2_concept_5', 'arg_3_concept_5'),
            ('arg_1_concept_5', 'step_1_concept_5'),
        ]


def get_steps(p):
    args = p['args']
    answer = p['ans']
    if p['concept'] == '1':
        return [
            ('r2c1', args[0], ('r1c1')),
            ('r2c2', '^', None),
            ('r2c3', args[1], ('r1c3')),
            ('r3c1', args[0] ** args[1])
            ('r4c1', p['args'][0] ** p['args'][1], ('r2c1', 'r2c2'))
            ('answer', answer, ('r4c1'))
        ]

    elif p['concept'] == '2':
        return [
            p['args'][0] / p['args'][1],
            p['args'][2] / p['args'][3]
        ]
    elif p['concept'] == '3':
        return [p['args'][1] * p['args'][2]]
    elif p['concept'] == '4':
        return [
            p['args'][1] / p['args'][0],
            p['args'][1] ** p['args'][0]
        ]
    elif p['concept'] == '5':
        return [p['args'][2] - p['args'][1]]


IIDDXX = 0
def random_num():
    global IIDDXX

    IIDDXX += 1
    return (IIDDXX % 15) + 1
    # return randint(1, 15)
