import time
import memory.shared.runner as runner
from memory.shared.helper import get_state_field


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
        # 'r2c4': get_state_field('r2c4', '', True),
        # 'r2c5': get_state_field('r2c5', '', True),
        # 'r2c6': get_state_field('r2c6', '', True),
        # 'r2c7': get_state_field('r2c7', '', True),
        # 'r2c8': get_state_field('r2c8', '', True),
        # 'r2c9': get_state_field('r2c9', '', True),
        # 'r2c10': get_state_field('r2c10', '', True),
        # 'r2c11': get_state_field('r2c11', '', True),
        'r3c1': get_state_field('r3c1', '', True),
        'r3c2': get_state_field('r3c2', '', True),
        'r3c3': get_state_field('r3c3', '', True),
        # 'r3c4': get_state_field('r3c4', '', True),
        # 'r3c5': get_state_field('r3c5', '', True),
        # 'r3c6': get_state_field('r3c6', '', True),
        # 'r3c7': get_state_field('r3c7', '', True),
        # 'r3c8': get_state_field('r3c8', '', True),
        # 'r3c9': get_state_field('r3c9', '', True),
        # 'r3c10': get_state_field('r3c10', '', True),
        # 'r3c11': get_state_field('r3c11', '', True),
        'r4c1': get_state_field('r4c1', '', True),
        'r4c2': get_state_field('r4c2', '', True),
        'r4c3': get_state_field('r4c3', '', True),
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
    state['r1c1'] = get_state_field('r1c1', args[0], False)
    state['r1c2'] = get_state_field('r1c2', 'DIAMOND', False)
    state['r1c3'] = get_state_field('r1c3', args[1], False)


def populate_2(args, state):
    state['r1c1'] = get_state_field('r1c1', '(', False)
    state['r1c2'] = get_state_field('r1c2',args[0], False)
    state['r1c3'] = get_state_field('r1c3',',', False)
    state['r1c4'] = get_state_field('r1c4',args[1], False)
    state['r1c5'] = get_state_field('r1c5',')', False)
    state['r1c6'] = get_state_field('r1c6','SUN', False)
    state['r1c7'] = get_state_field('r1c7','(', False)
    state['r1c8'] = get_state_field('r1c8',args[2], False)
    state['r1c9'] = get_state_field('r1c9',',', False)
    state['r1c10'] = get_state_field('r1c10',args[3], False)
    state['r1c11'] = get_state_field('r1c11',')', False)

def populate_3(args, state):
    state['r1c1'] = get_state_field('r1c1', args[0], False)
    state['r1c2'] = get_state_field('r1c2', 'SQUARE', False)
    state['r1c3'] = get_state_field('r1c3','(', False)
    state['r1c4'] = get_state_field('r1c4',args[1], False)
    state['r1c5'] = get_state_field('r1c5',',', False)
    state['r1c6'] = get_state_field('r1c6',args[2], False)
    state['r1c7'] = get_state_field('r1c7',')', False)

def populate_4(args, state):
    state['r1c1'] = get_state_field('r1c1', args[0], False)
    state['r1c2'] = get_state_field('r1c2', 'CIRCLE', False)
    state['r1c3'] = get_state_field('r1c3', args[1], False)


def _populate_2(args, state):
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


populate_funcs = [populate_1, populate_2, populate_3, populate_4]
def populate_states(p, state):
    concept = p['concept']
    populate_funcs[int(concept)-1](p['args'], state)


def get_steps(p):
    args = p['args']
    answer = p['ans']
    if p['concept'] == '1':
        return [
            ('r2c1', args[0], ('r1c1', )),
            ('r2c2', '^', None),
            ('r2c3', args[1], ('r1c3', )),
            ('r3c1', args[0] ** args[1], ('r2c1', 'r2c3')),
            ('answer', answer, ('r4c1', ))
        ]

    elif p['concept'] == '2':
        s1 = str(int(args[0]/args[1]))
        s2 = str(int(args[2]/args[3]))
        return [
            ('r2c1', f'{args[0]}/{args[1]}', ('r1c2', 'r1c4')),
            ('r2c2', '/', None),
            ('r2c3', f'{args[2]}/{args[3]}', ('r1c8', 'r1c10')),
            ('r3c1', s1, ('r2c1', )),
            ('r3c2', '/', ('r2c2', )),
            ('r3c3', s2, ('r2c3', )),
            # ('r4c1', f'{s1}/{s2}', ('r3c1', 'r3c2', 'r3c3')),
            ('r4c1', f'{s1}/{s2}', ('r3c1', 'r3c3')),
            ('answer', answer, ('r4c1', ))
        ]
        
    elif p['concept'] == '3':
        s1 = str(int(args[1]*args[2]))
        return [
            ('r2c1', f'{args[0]}', ('r1c1',)),
            ('r2c2', '/', None),
            ('r2c3', f'{args[1]}*{args[2]}', ('r1c4', 'r1c6')),
            ('r3c1', f'{args[0]}', ('r2c1', )),
            ('r3c2', '/', ('r2c2', )),
            ('r3c3', s1, ('r2c3', )),
            ('r4c1', f'{args[0]}/{s1}', ('r3c1', 'r3c3')),
            ('answer', answer, ('r4c1', ))
        ]

    elif p['concept'] == '4':
        s1 = str(int(args[1]/args[0]))
        s2 = str(int(args[1]**args[0]))
        return [
            ('r2c1', f'{args[1]}/{args[0]}', ('r1c1', 'r1c3')),
            ('r2c2', '+', None),
            ('r2c3', f'{args[1]}^{args[0]}', ('r1c1', 'r1c3')),
            ('r3c1', s1, ('r2c1', )),
            ('r3c2', '+', ('r2c2', )),
            ('r3c3', s2, ('r2c3', )),
            ('r4c1', f'{s1}+{s2}', ('r3c1', 'r3c3')),
            ('answer', answer, ('r4c1', ))
        ]

    elif p['concept'] == '5':
        return [p['args'][2] - p['args'][1]]


def main():
    # function_set=["concatenate2", "concatenate3", "solve", "ripfloatvalue"],
    # function_set=["division", "concatenate3", "solve", "ripfloatvalue"],
    # function_set=["division", "concatenate3", "solve", "ripfloatvalue", "ripstrvalue"],
    function_set=["addition", "multiplication", "division", "powering", "solve", "ripstrvalue", "strtofloat"]
    runner.run(function_set, get_state_and_answer)


if __name__ == "__main__":
    tic = time.time()
    main()
    toc = time.time()
    print(f'[loop] Done in {toc-tic:.4f} seconds')
