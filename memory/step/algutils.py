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
        # 'type': 'TextField',
        'value': f'{value}',
        'contentEditable': editable,
    }

# Should we get rid of step_i from Fact?
def get_state_and_answer(p):
    state = {
        'concept': get_state_field('concept', f"concept-{p['concept']}"),
        'answer': get_state_field('answer', '', True),
        'arg_1_concept_1': get_state_field('arg_1_concept_1',''),
        'arg_2_concept_1': get_state_field('arg_2_concept_1',''),
        'arg_1_concept_2': get_state_field('arg_1_concept_2',''),
        'arg_2_concept_2': get_state_field('arg_2_concept_2',''),
        'arg_3_concept_2': get_state_field('arg_3_concept_2',''),
        'arg_4_concept_2': get_state_field('arg_4_concept_2',''),
        'arg_1_concept_3': get_state_field('arg_1_concept_3',''),
        'arg_2_concept_3': get_state_field('arg_2_concept_3',''),
        'arg_3_concept_3': get_state_field('arg_3_concept_3',''),
        'arg_1_concept_4': get_state_field('arg_1_concept_4',''),
        'arg_2_concept_4': get_state_field('arg_2_concept_4',''),
        'arg_1_concept_5': get_state_field('arg_1_concept_5',''),
        'arg_2_concept_5': get_state_field('arg_2_concept_5',''),
        'arg_3_concept_5': get_state_field('arg_3_concept_5',''),
        'step_1_concept_1': get_state_field('step_1_concept_1','', True),
        'step_1_concept_2': get_state_field('step_1_concept_2','', True),
        'step_2_concept_2': get_state_field('step_2_concept_2','', True),
        'step_1_concept_3': get_state_field('step_1_concept_3','', True),
        'step_1_concept_4': get_state_field('step_1_concept_4','', True),
        'step_2_concept_4': get_state_field('step_2_concept_4','', True),
        'step_1_concept_5': get_state_field('step_1_concept_5','', True),
    }

    for idx, a in enumerate(p['args']):
        # name = f'arg_{idx+1}'
        name = f"arg_{idx+1}_concept_{p['concept']}"
        state[name] = get_state_field(name, a)

    step_count = step_counts[int(p['concept'])-1]
    for i in range(1, step_count+1):
        name = f"step_{i}_concept_{p['concept']}"
        state[name] = get_state_field(name, '', True)

    answer = p['ans']
    choices = p['choices']

    for k in state:
        state[k]['is_empty'] = state[k]['value'] == ''
    return state, answer, choices, get_steps(p), get_foa(p['concept'])

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
    if p['concept'] == '1':
        return [p['args'][0] ** p['args'][1]]
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
