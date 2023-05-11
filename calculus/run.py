import random, util, datetime
from copy import deepcopy
from states import States

import colorama
from colorama import Fore, Back

txlogs =[]
CORRECT, WRONG, HINT = 0, 1, 2
results = []
current_problem = None

def _clean(s):
    if s == None:
        return s
    s = s.replace(', ','&')
    s = s.replace(',','&')
    return s

def log_tx(step, rhs_id, where, how, al_sai, correct_sai, result):
    global current_problem, txlogs, results
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S:%f")[:-4]

    if result == None:
        r = "HINT"
        results[-1][HINT] += 1
    elif result == True:
        r = "CORRECT"
        results[-1][CORRECT] += 1
    elif result == False:
        r = "INCORRECT"
        results[-1][WRONG] += 1
    else:
        r = "???"

    l = f'{_clean(current_problem)},{step},{rhs_id},{_clean(where)},{_clean(how)},{_clean(str(al_sai))},{_clean(str(correct_sai))},{r},{time}\n'
    txlogs.append(l)


def write_txlogs():
    global txlogs
    tlogs = ['Problem,Step,RHS_ID,Where,How,AL_SAI,Correct_SAI,Result,Time\n']
    tlogs.extend(txlogs)
    with open("txlogs.csv", 'w+') as f:
        f.writelines(tlogs)


def _run_problem(agent, fsm):
    global results
    results.append([0, 0, 0])

    while not fsm.done:
        fsm.show()
        state = fsm.get_state()
        res = agent.act(state, json_friendly=True)
        print(res)

        # h = fsm.hint()
        # h_sai, h_foa = h['sai'], h['foa']
        if not res:
            # copied = deepcopy(correct_sai)
            h_sai, foci = fsm.get_correct_action()
            fsm.apply(h_sai)
            correct_sai = util.generate_sai_from_sai(h_sai)
            exp  = agent.train(state, correct_sai, 1, arg_foci=foci)

            # log_tx(fsm.step, rhs_id, where, exp, None, correct_sai, None)
            log_tx(fsm.step, None, None, None, None, correct_sai, None)
            util.print_log("blue", f"[HINT] STEP: {fsm.step}, {h_sai['selection']}-{h_sai['action_type']}-{h_sai['input']}")
        else:
            sel, act, val = res['selection'], res['action_type'], res["inputs"]["value"]
            sai = util.generate_sai(sel, act, val)
            local_sai = util.generate_local_sai(sel, act, val)

            correct = fsm.apply(local_sai)
            # log_tx(fsm.step, res['rhs_id'], info['where'], info['skill'], sai, correct_sai, correct)
            log_tx(fsm.step, None, None, None, sai, "correct_sai", correct)
            if correct:
                util.print_log("green", f"[CORRECT] STEP: {fsm.step}, {sel}-{act}-{val}")
            else:
                util.print_log("red", f"[WRONG] STEP: {fsm.step}, {sel}-{act}-{val}")

            # agent.train(state, sai=sai, reward=(1 if correct else -1), rhs_id=res['rhs_id'])
            agent.train(state, sai=sai, reward=(1 if correct else -1))


def run_problem(agent, ns):
    print(f"ns = {ns}")
    states = States(ns)
    _run_problem(agent, states)

N = 5
def main():
    global current_problem, results
    agent = util.create_agent()

    problems = random.sample(range(2, 100), N)
    for idx in range(N):
        ns = random.sample(range(2, 100), 2)
        current_problem = f'#{idx+1}[n={ns}]'
        run_problem(agent, ns)
        print('=' * 20)

    write_txlogs()
    # agent.show_skills()
    for idx, r in enumerate(results):
        print(f'[#{idx}] Correct: {r[CORRECT]}, Wrong: {r[WRONG]}, HINT: {r[HINT]}')

def random_terms():
    global current_problem, results
    agent = util.create_agent()

    problem_count = []
    for idx in range(20):
        n = random.randint(1, 7)
        ns = random.sample(range(2, 100), n)
        current_problem = f'#{idx+1}[n={ns}][{len(ns)}]'
        problem_count.append(len(ns))
        run_problem(agent, ns)
        print('=' * 20)

    write_txlogs()
    for idx, r in enumerate(results):
        print(f'[#{idx}] ({problem_count[idx]}) Correct: {r[CORRECT]}, Wrong: {r[WRONG]}, HINT: {r[HINT]}')

    skills = agent.get_skills()
    for s in skills:
        print(s)

def main2():
    global current_problem, results
    agent = util.create_agent()

    problem_count = []
    ns = random.sample(range(2, 100), 2)
    current_problem = f'#LAST[n={ns}]'
    problem_count.append(len(ns))
    run_problem(agent, ns)
    print('=' * 20)

    for idx in range(20):
        n = random.randint(1, 7)
        ns = random.sample(range(2, 100), n)
        current_problem = f'#{idx+1}[n={ns}][{len(ns)}]'
        problem_count.append(len(ns))
        run_problem(agent, ns)
        print('=' * 20)

    # for idx in range(20):
    #     ns = random.sample(range(2, 100), 1)
    #     current_problem = f'#{idx+1+20}[n={ns}][{len(ns)}]'
    #     problem_count.append(len(ns))
    #     run_problem(agent, ns)
    #     print('=' * 20)

    # for idx in range(20):
    #     n = random.randint(1, 7)
    #     ns = random.sample(range(2, 100), n)
    #     current_problem = f'#{idx+1+40}[n={ns}][{len(ns)}]'
    #     problem_count.append(len(ns))
    #     run_problem(agent, ns)
    #     print('=' * 20)

    ns = random.sample(range(2, 100), 1)
    current_problem = f'#LAST[n={ns}]'
    problem_count.append(len(ns))
    run_problem(agent, ns)
    print('=' * 20)

    write_txlogs()
    for idx, r in enumerate(results):
        print(f'[#{idx}] ({problem_count[idx]}) Correct: {r[CORRECT]}, Wrong: {r[WRONG]}, HINT: {r[HINT]}')


if __name__ == '__main__':
    # main()
    main2()
    # random_terms()
    # debug()
