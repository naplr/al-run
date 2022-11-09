import time

import memory.shared.runner as runner
import memory.shared.helper as helper
from memory.shared.helper import get_state_field


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

    for k in state:
        state[k]['is_empty'] = state[k]['value'] == ''
    return state, p['ans'], p['choices'], get_steps(p)


def get_steps(p):
    args = p['args']
    answer = p['ans']
    def a(n):
        return helper.append(n, p)

    if p['concept'] == '1':
        return [
            (a('step_1'), args[0] ** args[1], (a('arg_1'), a('arg_2'))),
            (a('answer'), answer, (a('step_1'), ))
        ]
    elif p['concept'] == '2':
        return [
            (a('step_1'), args[0] / args[1], (a('arg_1'), a('arg_2'))),
            (a('step_2'), args[2] / args[3] , (a('arg_3'), a('arg_4'))),
            (a('answer'), answer, (a('step_1'), a('step_2')))
        ]

    elif p['concept'] == '3':
        return [
            (a('step_1'), args[1] * args[2], (a('arg_2'), a('arg_3'))),
            (a('answer'), answer, (a('step_1'), a('arg_1')))
        ]
    elif p['concept'] == '4':
        return [
            (a('step_1'), args[1] / args[0], (a('arg_1'), a('arg_2'))),
            (a('step_2'), args[1] ** args[0] , (a('arg_1'), a('arg_2'))),
            (a('answer'), answer, (a('step_1'), a('step_2')))
        ]
    elif p['concept'] == '5':
        return [
            (a('step_1'), args[2] - args[1], (a('arg_2'), a('arg_3'))),
            (a('answer'), answer, (a('step_1'), a('arg_1')))
        ]

def main():
    function_set=["add", "subtract", "multiply", "divide", "pow", "inverse", "ripfloatvalue"]
    runner.run(function_set, get_state_and_answer)

if __name__ == "__main__":
    tic = time.time()
    main()
    toc = time.time()
    print(f'[loop] Done in {toc-tic:.4f} seconds')