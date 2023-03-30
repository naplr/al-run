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
        state = fsm.get_state()
        res = agent.act(state)

        # h = fsm.hint()
        # h_sai, h_foa = h['sai'], h['foa']
        if len(res) == 0:
            # copied = deepcopy(correct_sai)
            print('[DEMO]')
            h_sai = fsm.get_correct_action()
            correct_sai = util.generate_sai_from_sai(h_sai)
            print(correct_sai)
            exp  = agent.train(state, correct_sai, 1)

            # log_tx(fsm.step, rhs_id, where, exp, None, correct_sai, None)
            log_tx(fsm.step, None, None, None, None, correct_sai, None)
            print(Back.BLUE + Fore.YELLOW + f"[HINT] STEP: {fsm.step}, {h_sai['selection']}-{h_sai['action']}-{h_sai['input']}")
        else:
            sel, act, val = res['selection'], res['action'], res["inputs"]["value"]
            sai = util.generate_sai(sel, act, val)
            local_sai = util.generate_local_sai(sel, act, val)
            print('[ACT]')

            correct = fsm.apply(local_sai)
            # log_tx(fsm.step, res['rhs_id'], info['where'], info['skill'], sai, correct_sai, correct)
            # log_tx(fsm.step, res['rhs_id'], None, None, sai, correct_sai, correct)
            if correct:
                print(Back.GREEN + Fore.BLACK + f"[CORRECT] STEP: {fsm.step}, {sel}-{act}-{val}")
            else:
                print(Back.RED + Fore.BLACK + f"[WRONG] STEP: {fsm.step}, {sel}-{act}-{val}")

            agent.train(state, sai=sai, reward=(1 if correct else -1), rhs_id=res['rhs_id'])


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

if __name__ == '__main__':
    main()
    # debug()
