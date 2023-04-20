import random, util, datetime
from simple_fsm import FSM
from copy import deepcopy
from states import StatesSingle, StatesTwo, StatesThree

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

    while not fsm.is_done:
        state = fsm.get_state()
        res, info = agent.request(state)

        h = fsm.hint()
        h_sai, h_foa = h['sai'], h['foa']
        correct_sai = util.generate_sai(h_sai['selection'], h_sai['action'], h_sai['input'])
        if len(res) == 0:
            copied = deepcopy(correct_sai)
            # exp = agent.train(state, copied, 1)
            where, exp, rhs_id  = agent.train(state, copied, 1, foci_of_attention=h_foa)
            # agent.train(state, sai, 1, foci_of_attention=h_foa)

            log_tx(fsm.step, rhs_id, where, exp, None, correct_sai, None)
            print(f"[HINT] STEP: {fsm.step}, {h_sai['selection']}-{h_sai['action']}-{h_sai['input']}")
            fsm.inc_step()
        else:
            sel, act, val = res['selection'], res['action'], res["inputs"]["value"]
            sai = util.generate_sai(sel, act, val)

            correct = fsm.apply(sel, act, val)
            step = fsm.step - (1 if correct else 0)
            log_tx(step, res['rhs_id'], info['where'], info['skill'], sai, correct_sai, correct)
            if correct:
                print(f"[CORRECT] STEP: {fsm.step - 1}, {sel}-{act}-{val}")
            else:
                print(f"[WRONG] STEP: {fsm.step}, {sel}-{act}-{val}")

            agent.train(state, sai=sai, reward=(1 if correct else -1), rhs_id=res['rhs_id'])


def run_problem_1(agent, n):
    print(f"n = {n}")
    states = StatesSingle(n)
    fsm = FSM(states)
    _run_problem(agent, fsm)


def run_problem_2(agent, n, m):
    print(f"n = {n}")
    states = StatesTwo(n, m)
    fsm = FSM(states)
    _run_problem(agent, fsm)


def run_problem_3(agent, n, m, o):
    print(f"n = {n}")
    states = StatesThree(n, m, o)
    fsm = FSM(states)
    _run_problem(agent, fsm)


N = 10
def main():
    global current_problem, results
    agent = util.create_agent()

    problems = random.sample(range(2, 100), N)
    for idx, n in enumerate(problems):
        current_problem = f'#{idx}[n={n}]'
        run_problem_1(agent, n)
        print('=' * 20)

    problems = random.sample(range(2, 100), N)
    problems_2 = random.sample(range(2, 100), N)
    for idx, x in enumerate(zip(problems, problems_2)):
        n, m = x
        current_problem = f'#{idx}[n={n},m={m}]'
        run_problem_2(agent, n, m)
        print('=' * 20)

    problems = random.sample(range(2, 100), N)
    problems_2 = random.sample(range(2, 100), N)
    problems_3 = random.sample(range(2, 100), N)
    for idx, x in enumerate(zip(problems, problems_2, problems_3)):
        n, m, o = x
        current_problem = f'#{idx}[n={n},m={m},o={o}]'
        run_problem_3(agent, n, m, o)
        print('=' * 20)

    write_txlogs()
    agent.show_skills()
    for idx, r in enumerate(results):
        print(f'[#{idx}] Correct: {r[CORRECT]}, Wrong: {r[WRONG]}, HINT: {r[HINT]}')

if __name__ == '__main__':
    main()
    # debug()
