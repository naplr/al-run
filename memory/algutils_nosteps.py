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
        'id': name,
        'value': f'{value}',
        'contentEditable': editable,
        'type': 'TextField'
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
    }

    for idx, a in enumerate(p['args']):
        name = f"arg_{idx+1}_concept_{p['concept']}"
        state[name] = get_state_field(name, a)

    answer = p['ans']
    # for k in state:
    #     state[k]['is_empty'] = state[k]['value'] == ''
    return state, answer

IIDDXX = 0
def random_num():
    global IIDDXX

    IIDDXX += 1
    return (IIDDXX % 15) + 1
    # return randint(1, 15)



solutions = [
    { 
        "mapping": {'?arg0': '?ele-arg_1_concept_1', '?arg1': '?ele-arg_2_concept_1'},
        "input_rule": ('Swap', ('value', ('Power', ('value', '?arg0'), ('value', '?arg1'))))
    },
    {
        "mapping": {
            '?arg0': '?ele-arg_1_concept_2', 
            '?arg1': '?ele-arg_2_concept_2', 
            '?arg2': '?ele-arg_3_concept_2', 
            '?arg3': '?ele-arg_4_concept_2'
        },
        "input_rule": (
            'Divide', 
            ('value', ('Divide', ('value', '?arg0'), ('value', '?arg1'))),
            ('value', ('Divide', ('value', '?arg2'), ('value', '?arg3')))
        )   
    },
    {
        "mapping": {
            '?arg0': '?ele-arg_1_concept_3', 
            '?arg1': '?ele-arg_2_concept_3', 
            '?arg2': '?ele-arg_3_concept_3'
        },
        "input_rule": (
            'Divide',
            ('value', '?arg0'),
            ('value', ('Multiply', ('value', '?arg2'), ('value', '?arg3'))) 
        )
    },
    {
        "mapping": {
            '?arg0': '?ele-arg_1_concept_2', 
            '?arg1': '?ele-arg_2_concept_2', 
        },
        "input_rule": (
            'Add', 
            ('value', ('Divide', ('value', '?arg1'), ('value', '?arg0'))),
            ('value', ('Power', ('value', '?arg1'), ('value', '?arg0')))
        )
    },
    {
        "mapping": {
            '?arg0': '?ele-arg_1_concept_3', 
            '?arg1': '?ele-arg_2_concept_3', 
            '?arg2': '?ele-arg_3_concept_3'
        },
        "input_rule": (
            'Divide', 
            ('value', ('Subtract', ('value', '?arg3'), ('value', '?arg2'))),
            ('value', '?arg0')
        )
    },
]