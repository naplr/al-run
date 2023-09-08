import sys, json, pickle, copy, multiprocessing
from datetime import datetime
# from sklearn import tree
# from matplotlib import pyplot as plt
# from itertools import chain

from memory.shared.config import *
from memory.shared.const import *
import memory.shared.helper as helper

import colorama
from colorama import Fore, Back


logs = {}
agent_logs = {}
seen_answers = []
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
    # log_result(log_type, agent_name, ktype, ttype, info, str(correct_answer) in seen_answers)
    print(seen)
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


def run_problem(agent, p, ptype, ktype, ttype, state_func):
    global current_agent, current_concept, current_problem, current_ktype, current_ttype, current_ptype

    state, answer, choices, steps = state_func(p)
    name = f"{p['concept']}, args: {str(p['args'])}, ans: {p['ans']}, {ktype}, {ttype}, {ptype}"
    seen = p.get('seen', False)

    current_agent = agent.agent_name
    current_concept = p['concept']
    current_problem = f"[{p['concept']}][args:{'-'.join([str(a) for a in p['args']])}]"
    current_ktype = ktype
    current_ttype = ttype
    current_ptype = ptype

    concept = p['concept']

    if DEBUG: print(name)
    if ktype == KTYPE_FACT:
        _run_problem_fact(agent, concept, state, answer, ptype, ttype, name, seen)
    elif ktype == KTYPE_SKILL:
        _run_problem_skill(agent, concept, state, answer, steps, ptype, ttype, name, seen)

    print('-' * 20)


def _run_problem_fact(agent, concept, state, answer, ptype, ttype, name, seen):
    problem_info = {'problem_name': name}
    if ptype == PTYPE_DEMO:
        sai = helper.generate_sai(answer)

        # when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True)
        # log_transaction(None, 'Train', when, where, exp, False, None, answer, seen)

        agent.train(state, sai=sai, reward=1, problem_info=problem_info)

        log(LOG_DEMO, agent.agent_name, correct_answer=answer)
    elif ptype == PTYPE_PRACTICE:
        res, info = agent.request(state, problem_info=problem_info)
        info['problem_name'] = name

        if not res:
            # Can't answer
            log(LOG_HINT, agent.agent_name, KTYPE_FACT, ttype, info, correct_answer=answer, seen=seen)
            # log_transaction(False, 'Request', info['when'], info['where'], 'HINT', False, None, answer, seen)
            if ttype == TT_STUDY:
                sai = helper.generate_sai(answer)
                # when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True)
                # log_transaction(None, 'Train', when, where, exp, False, None, answer, seen)

                agent.train(state, sai=sai, reward=1, problem_info=problem_info)
        else:
            val = res["inputs"]["value"]
            selection = res['selection'].id
            # correct = str(val) == str(answer) and selection == 'answer'
            try:
                correct = (val != None) and (str(int(val)) == str(answer)) and selection == 'answer'
            except:
                correct = False
            # log_transaction(correct, 'Request', info['when'], info['where'], info['skill'], False, val, answer, seen)
            if ttype == TT_STUDY:
                # rhs_id = res["rhs_id"]
                sai = helper.generate_sai(val)
                rew = 1 if correct else -1
                # exp = agent.train(state, sai=sai, reward=rew, rhs_id=rhs_id, problem_info=problem_info, ret_train_expl=True)

                agent.train(state, sai=sai, reward=rew, problem_info=problem_info)
            if correct:
                log(LOG_CORRECT, agent.agent_name, KTYPE_FACT, ttype, info, val, answer, seen)
            else:
                log(LOG_WRONG, agent.agent_name, KTYPE_FACT, ttype, info, val, answer, seen)
                if ttype == TT_STUDY:
                    sai = helper.generate_sai(answer)
                    # exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True)
                    agent.train(state, sai=sai, reward=1, problem_info=problem_info)


    # log_transaction(result, action, skill, isInt, al_answer="", correct_answer=""):
def _run_problem_skill(agent, concept, state, answer, steps, ptype, ttype, name, seen):
    problem_info = {'problem_name': name}
    if ptype == PTYPE_DEMO:
        log(LOG_DEMO, agent.agent_name, correct_answer=answer)
        for idx, s in enumerate(steps):
            selection, value, foas = s
            sai = helper.generate_sai(value, selection)
            print(f'[[TRAIN INT]]: {value}, {selection}')
            # print(sai)

            # when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True, foci_of_attention=foas)
            # print(f'[[Explanation]]: {exp}')
            # log_transaction(None, 'Train', when, where, exp, idx+1 == len(steps), None, s, seen)

            agent.train(state, sai=sai, reward=1, problem_info=problem_info, foci_of_attention=foas)

            state[selection]['value'] = str(value)
            state[selection]['contentEditable'] = False
            state[selection]['is_empty'] = False

        # sai = helper.generate_sai(answer)
        # when, where, exp = agent.train(state, sai=sai, reward=1, problem_info=problem_info, ret_train_expl=True, foci_of_attention=None)
        # log_transaction(None, 'Train', when, where, exp, False, None, answer, seen)
    elif ptype == PTYPE_PRACTICE:
        # ss = {f"step_{idx+1}_concept_{concept}": f'{step}' for idx, step in enumerate(steps)}
        prev_actions = []
        while True:
            res, info = agent.request(state, problem_info=problem_info)
            info['problem_name'] = name
            if not res:
                log(LOG_HINT, agent.agent_name, KTYPE_SKILL, ttype, info, correct_answer=answer, seen=seen)
                # log_transaction(False, 'Request', info['when'], info['where'], 'HINT', False, None, answer, seen)

                # if ttype == TT_STUDY:
                #     # TODO: Also need to provide step by step here?
                #     sai = helper.generate_sai(answer)
                #     agent.train(state, sai=sai, reward=1, problem_info=problem_info)
                return

            val = res["inputs"]["value"]
            selection = res['selection'].id
            skill_id = info['skill_id']
            # rhs_id = res["rhs_id"]
            if selection == 'answer':
                try:
                    correct = (val != None) and (str(int(val)) == str(answer))
                except:
                    correct = False

                # log_transaction(correct, 'Request', info['when'], info['where'], info['skill'], False, val, answer, seen)
                if ttype == TT_STUDY:
                    skill_id = info['skill_id']
                    # rhs_id = res["rhs_id"]
                    sai = helper.generate_sai(val)
                    rew = 1 if correct else -1
                    agent.train(state, sai=sai, reward=rew, skill_uid=skill_id, problem_info=problem_info)

                    for (st, sai, uid) in prev_actions:
                        agent.train(st, sai=sai, reward=rew, skill_uid=uid, problem_info=problem_info)

                if correct:
                    log(LOG_CORRECT, agent.agent_name, KTYPE_SKILL, ttype, info, val, answer, seen)
                else:
                    log(LOG_WRONG, agent.agent_name, KTYPE_SKILL, ttype, info, val, answer, seen)
                    # if ttype == TT_STUDY:
                    #     sai = helper.generate_sai(answer)
                    #     agent.train(state, sai=sai, reward=1, problem_info=problem_info)
            else:
                print(f'INTERMEDIATE SEL: {selection}')
                # log_transaction(None, 'Request', info['when'], info['where'], info['skill'], True, val, None, seen)

                cur_state = copy.deepcopy(state)
                sai = helper.generate_sai(val, selection)

                prev_actions.append((cur_state, sai, skill_id))

                print('+++++')
                print(selection)
                state[selection]['value'] = str(val)
                state[selection]['contentEditable'] = False
                state[selection]['is_empty'] = False
                continue

                # log(LOG_WRONG, agent.agent_name, KTYPE_SKILL, ttype, info, val, answer, seen)
                # log_transaction(False, 'Request', info['when'], info['where'], info['skill'], None, val, answer, seen)
            return


def show_result():
    all_post_s_cor, all_post_f_cor, all_post_s_tot, all_post_f_tot, all_post_cor, all_post_tot = 0, 0, 0, 0, 0, 0

    global logs
    for name, a in logs.items():

        post_s_cor = a['post'][KTYPE_SKILL]['seen']['correct'] + a['post'][KTYPE_SKILL]['unseen']['correct']
        post_f_cor = a['post'][KTYPE_FACT]['seen']['correct'] + a['post'][KTYPE_FACT]['unseen']['correct']
        post_cor = post_s_cor + post_f_cor
        post_s_tot = post_s_cor + a['post'][KTYPE_SKILL]['seen']['incorrect'] + a['post'][KTYPE_SKILL]['unseen']['incorrect']
        post_f_tot = post_f_cor + a['post'][KTYPE_FACT]['seen']['incorrect'] + a['post'][KTYPE_FACT]['unseen']['incorrect']
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


def run_agent(parameters):
    agent_name, function_set, alpha, tau, c, s, beta, b_practice, b_study, condition, knowledge_type, study_problems, post_problems, state_func = parameters

    print(f"RUNNING: {agent_name}")
    agent = helper.create_agent(agent_name, function_set, alpha, tau, c, s, beta, b_practice, b_study)
    study, post = helper.get_post_test_problems(study_problems, post_problems, knowledge_type)

    # run study
    for idx, p in enumerate(study):
        if condition == COND_SPPP:
            ptype = PTYPE_DEMO if int(idx / CONCEPT_NUM) == 0 else PTYPE_PRACTICE
        elif condition == COND_SPSP:
            ptype = PTYPE_DEMO if int(idx / CONCEPT_NUM) % 2 == 0 else PTYPE_PRACTICE
        run_problem(agent, p, ptype, knowledge_type, TT_STUDY, state_func)

    ft = 0.625
    st = 0.2
    wait_time = ft if knowledge_type == KTYPE_FACT else st

    # agent.update_activation_for_post_test(wait_time*2)

    # run post
    for p in post:
        run_problem(agent, p, PTYPE_PRACTICE, knowledge_type, TT_POSTTEST, state_func)

    logs[agent_name]['type'] = knowledge_type
    logs[agent_name]['cond'] = condition

    pickle.dump(logs, open(f'logs/{agent_name}-res.pkl', "wb"))

    global transaction_logs
    tlogs = ['Agent,Concept,Problem,Knowledge,Type,Result,Action,When-Part,Where-Part,How-Part,Intermediate,Seen,AL Ans,Correct Ans,Time\n']
    tlogs.extend(transaction_logs)
    with open(f"logs/{agent_name}-txlogs.csv", 'w+') as f:
        f.writelines(tlogs)


def run(function_set, state_func):
    colorama.init(autoreset=True)

    alpha, tau, c, s = 0.177, -0.7, 0.277, 1 # 0.0786
    beta, b_practice, b_study = 5, 1, 0.01

    study_problems, post_problems = helper.read_problems()
    num_set = 5

    # run_agent([f'SPPP-F-0', function_set, alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_FACT, study_problems, post_problems, state_func])
    # run_agent([f'SPSP-F-0', function_set, alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_FACT, study_problems, post_problems, state_func])
    # run_agent([f'SPPP-S-1', function_set, alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_SKILL, study_problems, post_problems, state_func])
    # run_agent([f'SPSP-S-1', function_set, alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_SKILL, study_problems, post_problems, state_func])
    # show_result()
    # return

    pool = multiprocessing.Pool()
    agents = []
    for i in range(num_set):
        # agents.append([f'SPPP-F-{i+1}', function_set, alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_FACT, study_problems, post_problems, state_func])
        # agents.append([f'SPSP-F-{i+1}', function_set, alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_FACT, study_problems, post_problems, state_func])
        # agents.append([f'SPPP-S-{i+1}', function_set, alpha, tau, c, s, beta, b_practice, b_study, COND_SPPP, KTYPE_SKILL, study_problems, post_problems, state_func])
        agents.append([f'SPSP-S-{i+1}', function_set, alpha, tau, c, s, beta, b_practice, b_study, COND_SPSP, KTYPE_SKILL, study_problems, post_problems, state_func])

    pool.map(run_agent, agents)
    show_result()
