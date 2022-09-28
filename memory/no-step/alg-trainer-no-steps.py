import sys, json, pickle, copy, time, multiprocessing
from random import randint, choice, shuffle, sample
from itertools import chain
from datetime import datetime

from apprentice.agents.MemoryAgent import MemoryAgent
from apprentice.agents.ModularAgent import ModularAgent
from apprentice.working_memory import fo_planner_operators

from algutils_nosteps import get_state_and_answer, generate_sai, solutions
from config import KTYPE_SKILL, KTYPE_FACT, COND_SPPP, COND_SPSP, TT_POSTTEST, TT_STUDY, PTYPE_PRACTICE, PTYPE_DEMO

import colorama
from colorama import Fore, Back

DEBUG = False
AGENT_TYPE = 'memory'
# AGENT_TYPE = 'modular'

LOG_CORRECT = "LOG_CORRECT"
LOG_WRONG = "LOG_WRONG"
LOG_HINT = "LOG_HINT"
LOG_DEMO = "LOG_DEMO"
LOG_POST = "LOG_POST"
# LOG_PRACTICE = "LOG_PRACT"

ATYPE_SPPP = "SPPP_TYPE"
ATYPE_SPSP = "SPSP_TYPE"
ATYPE_F = "F_TYPE"
ATYPE_S = "S_TYPE"

'''
2 Types -> facts and skills

fact -> get numbers + symbol -> answer
skill -> get numbers + symbol -> do the immediate value -> answer

study -> post-test

'''

logs = {}
agent_logs = {}
transaction_logs = []

current_agent = ""
current_problem = ""
current_concept = ""
current_ktype = ""
current_ttype = ""
current_ptype = ""

def log_result(log_type, agent_name, ktype, ttype, info, seen):
    global logs
    if agent_name not in logs:
        logs[agent_name] = {
            "study": { "correct": 0, "incorrect": 0, "hint": 0, "demo": 0 },
            "post": {
                KTYPE_SKILL: {
                    "seen": {"correct": 0, "incorrect": 0 },
                    "unseen": {"correct": 0, "incorrect": 0 },
                },
                KTYPE_FACT: {
                    "seen": {"correct": 0, "incorrect": 0 },
                    "unseen": {"correct": 0, "incorrect": 0 },
                }
            },
            "type": "", "post_t": 0, "pre_t": 0,
            "results": []
        }

    # if (ttype == TT_POSTTEST) \
    #     and len(logs[agent_name]['results']) > 0 \
    #     and logs[agent_name]['results'][-1][0]['info']['problem_name'] == info['problem_name']:
    #     logs[agent_name]['results'][-1].append({
    #         "ttype": ttype,
    #         "ktype": ktype,
    #         "info": info,
    #         "ltype": log_type
    #     })
    # else:
    logs[agent_name]['results'].append([{
        "ttype": ttype,
        "ktype": ktype,
        "info": info,
        "ltype": log_type
    }])

    novelty = "seen" if seen else "unseen"

    if log_type == LOG_HINT:
        if ttype == TT_STUDY:
            logs[agent_name][TT_STUDY]['hint'] += 1
        elif ttype == TT_POSTTEST:
            logs[agent_name][ttype][ktype][novelty]['incorrect'] += 1
    elif log_type == LOG_WRONG:
        if ttype == TT_STUDY:
            logs[agent_name][TT_STUDY]['incorrect'] += 1
        elif ttype == TT_POSTTEST:
            logs[agent_name][ttype][ktype][novelty]['incorrect'] += 1
    elif log_type == LOG_CORRECT:
        if ttype == TT_STUDY:
            logs[agent_name][TT_STUDY]['correct'] += 1
        elif ttype == TT_POSTTEST:
            logs[agent_name][ttype][ktype][novelty]['correct'] += 1
    elif log_type == LOG_DEMO:
        logs[agent_name]["study"]['demo'] += 1



def log(log_type, agent_name, ktype=None, ttype=TT_STUDY, info=None, al_answer="", correct_answer="", seen=False):
    log_result(log_type, agent_name, ktype, ttype, info, seen)

    if not DEBUG: return

    if log_type == LOG_HINT:
        print(Back.BLUE + Fore.YELLOW + "HINT")
    elif log_type == LOG_WRONG:
        print(Back.RED + Fore.BLACK + f"WRONG: {al_answer}, {correct_answer}")
    elif log_type == LOG_CORRECT:
        print(Back.GREEN + Fore.BLACK + f"CORRECT: {al_answer}, {correct_answer}")
    elif log_type == LOG_DEMO:
        print(Back.YELLOW + Fore.BLACK + "DEMO")
    else:
        print(Back.RED + Fore.WHITE + "SOMETHING WRONG !!!!")


def log_transaction(result, action, when_part, where_part, how_part, isInt, al_answer, correct_answer, seen):
    global current_agent, current_concept, current_problem, current_ktype, current_ttype, current_ptype, transaction_logs
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    # print(f"result: {str(result)}")
    if result == None:
        r = "NA"
    elif result == True:
        r = "CORRECT"
    elif result == False:
        r = "INCORRECT"
    else:
        r = "???"

    if current_ttype == TT_POSTTEST:
        ttype = 'posttest'
    elif current_ttype == TT_STUDY and current_ptype == PTYPE_DEMO:
        ttype = 'study'
    elif current_ttype == TT_STUDY and current_ptype == PTYPE_PRACTICE:
        ttype = 'practice'
    else:
        ttype = '???'

    ktype = 'Fact' if current_ktype == KTYPE_FACT else 'Skill'
    how_part = how_part.replace(', ','&')
    how_part = how_part.replace(',','&')
    where_part = str(where_part)
    where_part = where_part.replace(', ','&')
    where_part = where_part.replace(',','&')
    when_part = str(when_part)
    when_part = when_part.replace(', ','&')
    when_part = when_part.replace(',','&')
    when_part = when_part.replace('\n', 'CHAR(13)')

    l = f'{current_agent},{current_concept},{current_problem},{ktype},{ttype},{r},{action},{when_part},{where_part},{how_part},{isInt},{seen},{al_answer},{correct_answer},{time}\n'
    transaction_logs.append(l)


def create_agent(name, alpha, tau, c, s, beta, b_practice, b_study):
    if AGENT_TYPE == 'memory':
        agent = MemoryAgent(
            agent_name=name,
            # feature_set=["equals"],
            # function_set=["add", "subtract", "multiply", "divide", "pow", "inverse", "ripfloatvalue"],
            function_set=["add", "subtract", "multiply", "divide", "pow", "ripfloatvalue"],
            feature_set=[],
            when_learner="decisiontree",
            where_learner="mostspecific",
            planner="numba",
            search_depth=3,
            alpha=alpha,
            tau=tau,
            c=c,
            s=s,
            beta=beta,
            b_practice=b_practice,
            b_study=b_study,
            print_log=DEBUG,
            use_memory=True
        )
    else:
        agent = ModularAgent(
            agent_name=name,
            feature_set=["equals"],
            function_set=["add", "subtract", "multiply", "divide", "pow"],
            when_learner="decisiontree",
            where_learner="mostspecific",
        )
    return agent


def run_problem(agent, p, ptype, ktype, ttype):
    global current_agent, current_concept, current_problem, current_ktype, current_ttype, current_ptype
    state, answer, foa = get_state_and_answer(p)
    name = f"{p['concept']}, args: {str(p['args'])}, ans: {p['ans']}, {ktype}, {ttype}"
    seen = p.get('seen', False)

    current_agent = agent.agent_name
    current_concept = p['concept']
    current_problem = f"[{p['concept']}][args:{'-'.join([str(a) for a in p['args']])}]"
    current_ktype = ktype
    current_ttype = ttype
    current_ptype = ptype

    solution = solutions[int(p['concept']) - 1]
    if DEBUG: print(name)
    if ktype == KTYPE_FACT:
        _run_problem_fact(agent, state, answer, ptype, ttype, name, seen)
    elif ktype == KTYPE_SKILL:
        _run_problem_skill(agent, state, answer, ptype, ttype, name, seen, solution, foa)

    print('-' * 20)


def _run_problem_fact(agent, state, answer, ptype, ttype, name, seen):
    problem_info = {'problem_name': name}
    if ptype == PTYPE_DEMO:
        sai = generate_sai(answer)
        when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info)
        log_transaction(None, 'Train', when, where, exp, False, None, answer, seen)
        log(LOG_DEMO, agent.agent_name, correct_answer=answer, seen=seen)
    elif ptype == PTYPE_PRACTICE:
        res, info = agent.request(state, problem_info=problem_info)
        info['problem_name'] = name
        if len(res) == 0:
            # Can't answer
            log(LOG_HINT, agent.agent_name, KTYPE_FACT, ttype, info, seen=seen)
            log_transaction(False, 'Request', info['when'], info['where'], 'HINT', False, None, answer, seen)
            if ttype == TT_STUDY:
                sai = generate_sai(answer)
                when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info)
                log_transaction(None, 'Train', when, where, exp, False, None, answer, seen)
        else:
            val = res["inputs"]["value"]
            selection = res['selection']
            correct = str(val) == str(answer)
            log_transaction(correct, 'Request', info['when'], info['where'], info['skill'], False, val, answer, seen)
            if ttype == TT_STUDY:
                rhs_id = res["rhs_id"]
                sai = generate_sai(val)
                rew = 1 if correct else -1
                agent.train(state, sai=sai, reward=rew, rhs_id=rhs_id, problem_info=problem_info, ret_train_expl=True)
            if correct:
                log(LOG_CORRECT, agent.agent_name, KTYPE_FACT, ttype, info, val, answer, seen=seen)
            else:
                log(LOG_WRONG, agent.agent_name, KTYPE_FACT, ttype, info, val, answer, seen=seen)
                if ttype == TT_STUDY:
                    sai = generate_sai(answer)
                    when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True)
                    log_transaction(None, 'Train', when, where, exp, False, None, answer, seen)



def _run_problem_skill(agent, state, answer, ptype, ttype, name, seen, solution, foa):
    problem_info = {'problem_name': name}
    if ptype == PTYPE_DEMO:
        log(LOG_DEMO, agent.agent_name, correct_answer=answer, seen=seen)
        sai = generate_sai(answer)
        print(solution)
        # agent.train(state, sai=sai, reward=1, problem_info=problem_info, solution=solution)
        
        when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True)

        log_transaction(None, 'Train', when, where, exp, False, None, answer, seen)

    elif ptype == PTYPE_PRACTICE:
        res, info = agent.request(state, problem_info=problem_info)
        print(info)
        info['problem_name'] = name
        if len(res) == 0:
            log(LOG_HINT, agent.agent_name, KTYPE_SKILL, ttype, info, correct_answer=answer, seen=seen)
            if ttype == TT_STUDY:
                # TODO: Also need to provide step by step here?
                sai = generate_sai(answer)
                agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True)
            log_transaction(False, 'Request', info['when'], info['where'], 'HINT', False, None, answer, seen)
            return

        val = res["inputs"]["value"]
        selection = res['selection']
        rhs_id = res["rhs_id"]
        
        if selection == 'answer':
            correct = val == str(answer) and selection == 'answer'
            log_transaction(correct, 'Request', info['when'], info['where'], info['skill'], False, val, answer, seen)

            if ttype == TT_STUDY:
                sai = generate_sai(val)
                rew = 1 if correct else -1
                agent.train(state, sai=sai, reward=rew, rhs_id=rhs_id, problem_info=problem_info, ret_train_expl=True)

            if correct:
                log(LOG_CORRECT, agent.agent_name, KTYPE_SKILL, ttype, info, val, answer, seen=seen)
            else:
                log(LOG_WRONG, agent.agent_name, KTYPE_SKILL, ttype, info, val, answer, seen=seen)
                if ttype == TT_STUDY:
                    sai = generate_sai(answer)
                    when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True)

                    log_transaction(None, 'Train', when, where, exp, False, None, answer, seen)
        else:
            log(LOG_WRONG, agent.agent_name, KTYPE_SKILL, ttype, info, val, answer, seen=seen)
            log_transaction(False, 'Request', info['when'], info['where'], info['skill'], None, val, answer, seen)
        return


def show_result():
    all_post_s_cor, all_post_f_cor, all_post_s_tot, all_post_f_tot, all_post_cor, all_post_tot = 0, 0, 0, 0, 0, 0

    global logs
    for name, a in logs.items():
        
        post_s_cor = a['post'][KTYPE_SKILL]['correct']
        post_f_cor = a['post'][KTYPE_FACT]['correct']
        post_cor = post_s_cor + post_f_cor
        post_s_tot = post_s_cor + a['post'][KTYPE_SKILL]['incorrect']
        post_f_tot = post_f_cor + a['post'][KTYPE_FACT]['incorrect']
        post_tot = post_s_tot + post_f_tot

        print(f"Agent: {name}")
        print("post: {}/{} ({:.2f}), skill: {:.2f}, fact: {:.2f}".format(
            post_cor, post_tot, post_cor / post_tot,
            post_s_cor / post_s_tot if post_s_tot > 0 else -1, 
            post_f_cor / post_f_tot if post_f_tot > 0 else -1
        ))

        study_tot = a['study']['correct'] + a['study']['incorrect'] + a['study']['hint']
        print("study: {}, {}, {}, demo: {}".format(
            a['study']['correct'], a['study']['incorrect'], 
            a['study']['hint'], a['study']['demo']
        ))

        all_post_s_cor += post_s_cor
        all_post_s_tot += post_s_tot
        all_post_f_cor += post_f_cor
        all_post_f_tot += post_f_tot
        all_post_cor = all_post_s_cor + all_post_f_cor
        all_post_tot = all_post_s_tot + all_post_f_tot

    all_post_p = all_post_cor / all_post_tot if all_post_tot > 0 else -1
    post_s_p = all_post_s_cor / all_post_s_tot if all_post_s_tot > 0 else -1
    post_f_p = all_post_f_cor / all_post_f_tot if all_post_f_tot > 0 else -1

    print()
    print("Total: ")
    print("Post: {}/{} ({:.2f}), skill: {}/{} ({:.2f}), fact: {}/{} ({:.2f})".format(
        all_post_cor, all_post_tot, all_post_p, 
        all_post_s_cor, all_post_s_tot, post_s_p, 
        all_post_f_cor, all_post_f_tot, post_f_p
    ))


def read_problems():
    study = pickle.load(open('./alg-study.pkl', 'rb'))
    post = pickle.load(open('./alg-post.pkl', 'rb'))
    return study, post


STUDY_PROBLEM_NUM = 10
CONCEPT_NUM = 4
def get_post_test_problems(study, post, ktype):
    post_problems = []

    problems_by_concept = []
    for c, problems in study.items():
        if c in [1, '1']:
        # if c in [1, 2, 4, 5, '1', '2', '4', '5']:
            continue 
        study_problems = []
        if ktype == KTYPE_FACT:
            selected = choice(problems)
            selected['seen'] = True
            for _ in range(STUDY_PROBLEM_NUM):
                study_problems.append(selected)
        elif ktype == KTYPE_SKILL:
            problems = sample(problems, STUDY_PROBLEM_NUM)
            study_problems.extend(problems)

            selected = problems[0]
            selected['seen'] = True

        problems_by_concept.append(study_problems)

        problems = sample(post[c], 3)
        for _ in range(3):
            problems.append(selected)
        post_problems.extend(problems)
    
    temps = zip(*problems_by_concept) 
    study_problems = list(chain(*temps))
    shuffle(post_problems)

    return study_problems, post_problems


def run_agent(parameters):
    agent_name, alpha, tau, c, s, beta, b_practice, b_study, condition, knowledge_type, study_problems, post_problems = parameters
    print(f"RUNNING: {agent_name}")
    agent = create_agent(agent_name, alpha, tau, c, s, beta, b_practice, b_study)
    study, post = get_post_test_problems(study_problems, post_problems, knowledge_type)

    # run study
    for idx, p in enumerate(study):
        if condition == COND_SPPP:
            ptype = PTYPE_DEMO if idx < int(idx / CONCEPT_NUM) == 0 else PTYPE_PRACTICE
        elif condition == COND_SPSP:
            ptype = PTYPE_DEMO if int(idx / CONCEPT_NUM) % 2 == 0 else PTYPE_PRACTICE
        run_problem(agent, p, ptype, knowledge_type, TT_STUDY)

    # run post
    for p in post:
        run_problem(agent, p, PTYPE_PRACTICE, knowledge_type, TT_POSTTEST)

    logs[agent_name]['type'] = knowledge_type
    logs[agent_name]['cond'] = condition

    pickle.dump(logs, open(f'logs/{agent_name}-res.pkl', "wb"))

    global transaction_logs
    tlogs = ['Agent,Concept,Problem,Knowledge,Type,Result,Action,When-Part,Where-Part,How-Part,Intermediate,Seen,AL Ans,Correct Ans,Time\n']
    tlogs.extend(transaction_logs)
    with open(f"logs/{agent_name}-transaction_logs.csv", 'w+') as f:
        f.writelines(tlogs)


def run_debug(agent, a, b, c):
    print(f'{a}, {b}, {c}')
    ans = (a + c) * b
    ans = str(ans)
    state = {
        'a': { 'id': 'a', 'value': str(a), 'contentEditable': False, 'type': 'TextField' },
        'b': { 'id': 'b', 'value': str(b), 'contentEditable': False, 'type': 'TextField' },
        'c': { 'id': 'c', 'value': str(c), 'contentEditable': False, 'type': 'TextField' },
        'ans': { 'id': 'ans', 'value': '', 'contentEditable': True, 'type': 'TextField' },
    }
    res, _ = agent.request(state)
    if len(res) == 0:
        print(f"HINT {ans}")
        sai = generate_sai(ans, 'ans', 'Update')
        # agent.train(state, sai, 1, foci_of_attention=['a', 'c'])
        agent.train(state, sai=sai, reward=1, operators=['add', 'multiply', "ripfloatvalue"])
    else:
        sel, act, val = res['selection'], res['action'], res["inputs"]["value"]
        sai = generate_sai(val, sel, act)

        correct = str(int(val)) == ans
        if correct:
            print(f"[CORRECT] {sel}-{act}-{val} ({res['rhs_id']})")
            agent.train(state, sai=sai, reward=1, rhs_id=res['rhs_id'], operators=['add', 'multiply', "ripfloatvalue"])
        else:
            print(f"[WRONG] {sel}-{act}-{val} ({res['rhs_id']})")
            agent.train(state, sai=sai, reward=-1, rhs_id=res['rhs_id'], operators=['add', 'multiply', "ripfloatvalue"])

            sai = generate_sai(ans, 'ans', 'Update')
            # agent.train(state, sai, 1, foci_of_attention=['a', 'c'])
            agent.train(state, sai=sai, reward=1, operators=['add', 'multiply', "ripfloatvalue"])
            print(f"DEMONSTRATE {ans}")

N = 2
def _debug():
    alpha, tau, c, s = 0.177, -0.7, 0.277, 1 # 0.0786
    beta, b_practice, b_study = 5, 1, 0.01
    agent = create_agent("TEST_DEBUG", alpha, tau, c, s, beta, b_practice, b_study)
    for _ in range(N):
        a, b, c = sample(range(1, 50), 3)
        run_debug(agent, a, b, c)
        print("==" * 20)


def main():
    colorama.init(autoreset=True)

    alpha, tau, c, s = 0.177, -0.7, 0.277, 1 # 0.0786
    beta, b_practice, b_study = 5, 1, 0.01

    study_problems, post_problems = read_problems()
    print(study_problems['1'])
    outname = f"res.pkl"
    num_set = 15
    for i in range(num_set):
        print("Running agent set: {}/{}".format(i+1, num_set))
        run_agent([f'SPPP-F-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_FACT, study_problems, post_problems])
        run_agent([f'SPSP-F-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_FACT, study_problems, post_problems])
        run_agent([f'SPPP-S-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_SKILL, study_problems, post_problems])
        run_agent([f'SPSP-S-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_SKILL, study_problems, post_problems])

        if DEBUG:
            print()
            print("=" * 20)
            print()
            print()

        show_result()
        pickle.dump(logs, open(outname, "wb"))

        global transaction_logs
        tlogs = ['Agent,Concept,Problem,Knowledge,Type,Result,Action,When-Part,Where-Part,How-Part,Intermediate,Seen,AL Ans,Correct Ans,Time\n']
        tlogs.extend(transaction_logs)
        with open("transaction_logs.csv", 'w+') as f:
            f.writelines(tlogs)
        # pickle.dump(logs, open(outname, "wb"))
        # pickle.dump(agent_logs, open("agent_logs.pkl", "wb"))

def run_loop():
    colorama.init(autoreset=True)

    alpha, tau, c, s = 0.177, -0.7, 0.277, 1 # 0.0786
    beta, b_practice, b_study = 5, 1, 0.01

    study_problems, post_problems = read_problems()
    num_set = 15
    for i in range(num_set):
        print("Running agent set: {}/{}".format(i+1, num_set))
        # run_agent([f'SPPP-F-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_FACT, study_problems, post_problems])
        # run_agent([f'SPSP-F-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_FACT, study_problems, post_problems])
        run_agent([f'SPPP-S-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_SKILL, study_problems, post_problems])
        run_agent([f'SPSP-S-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_SKILL, study_problems, post_problems])

        show_result()

def run_pool():
    colorama.init(autoreset=True)

    alpha, tau, c, s = 0.177, -0.7, 0.277, 1 # 0.0786
    beta, b_practice, b_study = 5, 1, 0.01

    study_problems, post_problems = read_problems()
    num_set = 15
    pool = multiprocessing.Pool()
    
    agents = []
    for i in range(num_set):
        agents.append([f'SPPP-F-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_FACT, study_problems, post_problems])
        agents.append([f'SPSP-F-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_FACT, study_problems, post_problems])
        agents.append([f'SPPP-S-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_SKILL, study_problems, post_problems])
        agents.append([f'SPSP-S-{i+1}', alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_SKILL, study_problems, post_problems])


    pool.map(run_agent, agents)
    show_result()


def check_problems():
    study_problems, post_problems = read_problems()
    for concept, v in study_problems.items():
        for p in v:
            print(p['args'])
    for concept, v in post_problems.items():
        for p in v:
            print(p['args'])


if __name__ == "__main__":
    # tic = time.time()
    # # main()
    # run_loop()
    # toc = time.time()
    # print(f'[loop] Done in {tic-toc:.4f} seconds')

    tic = time.time()
    # run_pool()
    _debug()
    toc = time.time()
    print(f'[loop] Done in {toc-tic:.4f} seconds')