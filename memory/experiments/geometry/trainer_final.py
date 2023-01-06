from re import I
import sys, json, pickle, copy, itertools, time, multiprocessing, os
from random import randint, choice, shuffle

from utils import parse_brd, generate_sai, generate_state_and_answer, create_agent
from memory.shared.config import *
from memory.shared.const import *

import colorama
from colorama import Fore, Back

DEBUG = True

logs = {}
agent_logs = {}

### HELPER ###

def log_result(log_type, agent_name, ktype, ttype, info):
    global logs
    if agent_name not in logs:
        logs[agent_name] = {
            "study": { "correct": 0, "incorrect": 0, "hint": 0, "demo": 0 },
            "pre": {
                SKILL: { "correct": 0, "incorrect": 0 },
                FACT: { "correct": 0, "incorrect": 0 }
            },
            "post": { 
                SKILL: { "correct": 0, "incorrect": 0 },
                FACT: { "correct": 0, "incorrect": 0 }
            },
            "type": "", "post_t": 0, "pre_t": 0,
            "results": []
        }

    if (ttype == TT_PRETEST or ttype == TT_POSTTEST) \
        and len(logs[agent_name]['results']) > 0 \
        and logs[agent_name]['results'][-1][0]['info']['problem_name'] == info['problem_name']:
        logs[agent_name]['results'][-1].append({
            "ttype": ttype,
            "ktype": ktype,
            "info": info,
            "ltype": log_type
        })
    else:
        logs[agent_name]['results'].append([{
            "ttype": ttype,
            "ktype": ktype,
            "info": info,
            "ltype": log_type
        }])

    if ttype == TT_PRETRAIN: return

    if log_type == LOG_HINT:
        if ttype == TT_STUDY:
            logs[agent_name][TT_STUDY]['hint'] += 1
        elif ttype == TT_PRETEST or ttype == TT_POSTTEST:
            logs[agent_name][ttype][ktype]['incorrect'] += 1
    elif log_type == LOG_WRONG:
        if ttype == TT_STUDY:
            logs[agent_name][TT_STUDY]['incorrect'] += 1
    elif log_type == LOG_CORRECT:
        if ttype == TT_STUDY:
            logs[agent_name][TT_STUDY]['correct'] += 1
        elif ttype == TT_PRETEST or ttype == TT_POSTTEST:
            logs[agent_name][ttype][ktype]['correct'] += 1
    elif log_type == LOG_DEMO:
        logs[agent_name]["study"]['demo'] += 1


def log(log_type, agent_name, ktype=None, ttype=TT_STUDY, info=None, al_answer="", correct_answer=""):
    log_result(log_type, agent_name, ktype, ttype, info)

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




### PRETRAIN ###

def _run_pretrain_once(state, answer, agent, name):
    problem_info = {'problem_name': name}
    if DEBUG: print(f"[PRE TRAIN]: {name}")

    res, info = agent.request(state, problem_info=problem_info, add_skill_info=True)
    print("pretrain mapping")
    print(res.get("mapping", "No mapping"))
    info['problem_name'] = name
    if len(res) == 0 or res["inputs"]["value"] == None:
        log(LOG_HINT, agent.agent_name, None, TT_PRETRAIN, info)
        sai = generate_sai(answer)
        agent.train(state, sai=sai, reward=1, problem_info=problem_info)
    else:
        rhs_id = res["rhs_id"]
        val = res["inputs"]["value"]
        sai = generate_sai(val)
        rew = 1 if val == answer else -1
        agent.train(state, sai=sai, reward=rew, rhs_id=rhs_id, problem_info=problem_info)
        if rew == 1:
            log(LOG_CORRECT, agent.agent_name, None, TT_PRETRAIN, info, val, answer)
        else:
            log(LOG_WRONG, agent.agent_name, None, TT_PRETRAIN, info, val, answer)


def pre_train(agent, fact_c, skill_c):
    shape_knowledge = list(itertools.product(SHAPES, [SKILL, FACT]))
    while True:
        if fact_c <= 0 and skill_c <= 0:
            return

        shuffle(shape_knowledge)
        for s, k in shape_knowledge:
            if skill_c <= 0 and k == SKILL:
                continue
            if fact_c <= 0 and k == FACT:
                continue

            state, ans = generate_state_and_answer(k, s)
            name = f"pre-train: {k}-{s}-{ans}"
            _run_pretrain_once(state, ans, agent, name)

        fact_c -= 1
        skill_c -= 1


### RUN ###

def run_problem_study(state, answer, examples_only, agent, ttype, problem_name):
    ktype = state['knowledge_type']['value']
    problem_info = {'problem_name': problem_name}
    if examples_only:
        sai = generate_sai(answer)
        agent.train(state, sai=sai, reward=1, problem_info=problem_info)
        log(LOG_DEMO, agent.agent_name, ktype, ttype, {'problem_name': problem_name})
    else:
        run_problem_test(state, answer, agent, ttype)

        # res, info = agent.request(state, problem_info=problem_info)
        # info['problem_name'] = problem_name
        # if len(res) == 0:
        #     log(LOG_HINT, agent.agent_name, ktype, ttype, info)
        # else:
        #     val = res["inputs"]["value"]
        #     sai = generate_sai(val)
        #     if val == answer:
        #         log(LOG_CORRECT, agent.agent_name, ktype, ttype, info, val, answer)
        #     else:
        #         log(LOG_WRONG, agent.agent_name, ktype, ttype, info, val, answer)


def run_problem_test(state, answer, agent, ttype):
    ktype = state['knowledge_type']['value']
    stype = state['shape_type']['value']
    problem_name = f"{ttype}: {ktype}-{stype}-{answer}-check({randint(1, 99999)})"
    if DEBUG: print(f"knowledge: {ktype}, shape: {stype}, [{problem_name}]")

    problem_info = {'problem_name': problem_name}
    attempts = 0
    while True:
        if attempts > 10:
            info = {'problem_name': problem_name, 'selected_skill': 'break'}
            log(LOG_HINT, agent.agent_name, ktype, ttype, info)
            break
        attempts += 1
        res, info = agent.request(state, problem_info=problem_info, add_skill_info=True)
        info['problem_name'] = problem_name
        if len(res) == 0:
            log(LOG_HINT, agent.agent_name, ktype, ttype, info)
            break
        else:
            val = res["inputs"]["value"]
            rhs_id = res["rhs_id"]
            mapping = res["mapping"]
            print(f'{val}, {rhs_id}')
            sai = generate_sai(val)
            if val == answer:
                log(LOG_CORRECT, agent.agent_name, ktype, ttype, info, val, answer)
                agent.train(state, sai=sai, reward=1, rhs_id=rhs_id, problem_info=problem_info)
                break
            else:
                log(LOG_WRONG, agent.agent_name, ktype, ttype, info, val, answer)
                print('Train with -1')
                agent.train(state, sai=sai, reward=-1, rhs_id=rhs_id, problem_info=problem_info, mapping=mapping)


def run_problem_from_json(brd, examples_only, agent, ttype):
    if DEBUG: print(brd)

    brd_fp = "../../../../testing-memory-AL/old-experiment/{}".format(brd)
    state, answer = parse_brd(brd_fp)
    if ttype == TT_STUDY:
        run_problem_study(state, answer, examples_only, agent, ttype, f"study-{brd}")
    elif ttype == TT_POSTTEST:
        run_problem_test(state, answer, agent, ttype)


TESTS = [f"prepost2_{i}.brd" for i in range(2, 18)]
def pre_test(agent):
    shuffle(TESTS)
    for brd in TESTS:
        brd_fp = f"../../../../testing-memory-AL/old-experiment/brds/{brd}"
        state, answer = parse_brd(brd_fp)
        run_problem_test(state, answer, agent, TT_PRETEST)


### RUN AGENT ###

def run_agent(parameters):
    data, alpha, tau, c, s, beta, b_practice, b_study, fact_c, skill_c, idx, total, iteration = parameters
    global logs
    agent_name = data["agent_name"]

    print("Running agent: {} ({}/{})".format(
        data["agent_name"], idx, total
    ) + "=" * 10)

    agent = create_agent(agent_name, alpha, tau, c, s, beta, b_practice, b_study)

    pre_train(agent, fact_c, skill_c)
    pre_test(agent)

    if AGENT_TYPE == 'memory':
        logs[agent_name]['pre_t'] = agent.t
    we_count = 0
    first_post = True
    atype = None
    examples_only = False
    for p in data["problem_set"]:
        if "set_params" in p and "examples_only" in p["set_params"]:
            examples_only = p["set_params"]["examples_only"]
            
        if "question_file" in p:
            qf = p["question_file"]
            if "_we_" in qf: we_count += 1
            if atype == None:
                atype = ATYPE_F if "_f_" in qf else ATYPE_S


            ttype = TT_POSTTEST if "prepost" in qf else TT_STUDY

            if AGENT_TYPE == 'memory' and ttype == TT_POSTTEST and first_post:
                logs[agent_name]['post_t'] = agent.t
                agent.update_activation_for_post_test(2)
                first_post = False

            run_problem_from_json(qf, examples_only, agent, ttype)

    cond = ATYPE_SPPP if we_count == 4 else ATYPE_SPSP
    logs[agent_name]['type'] = atype
    logs[agent_name]['cond'] =cond


    dirname = f"{AGENT_TYPE}-logs"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    pickle.dump(logs, open(f"{dirname}/{atype}-{cond}-{idx}-{iteration}-res.pkl", "wb"))
    # pickle.dump(logs, open(f"logs/{agent_name}-res.pkl", "wb"))
    # agent_logs[agent_name] = agent.get_log()


def show_result():
    all_pre_s_cor, all_pre_f_cor, all_pre_s_tot, all_pre_f_tot, all_pre_cor, all_pre_tot = 0, 0, 0, 0, 0, 0
    all_post_s_cor, all_post_f_cor, all_post_s_tot, all_post_f_tot, all_post_cor, all_post_tot = 0, 0, 0, 0, 0, 0

    global logs
    for name, a in logs.items():
        pre_s_cor = a['pre'][SKILL]['correct']
        pre_f_cor = a['pre'][FACT]['correct']
        pre_cor = pre_s_cor + pre_f_cor
        pre_s_tot = pre_s_cor + a['pre'][SKILL]['incorrect']
        pre_f_tot = pre_f_cor + a['pre'][FACT]['incorrect']
        pre_tot = pre_s_tot + pre_f_tot

        post_s_cor = a['post'][SKILL]['correct']
        post_f_cor = a['post'][FACT]['correct']
        post_cor = post_s_cor + post_f_cor
        post_s_tot = post_s_cor + a['post'][SKILL]['incorrect']
        post_f_tot = post_f_cor + a['post'][FACT]['incorrect']
        post_tot = post_s_tot + post_f_tot


        print(f"Agent: {name}")
        print("pre: {}/{} ({:.2f}), skill: {:.2f}, fact: {:.2f}".format(
            pre_cor, pre_tot, pre_cor / pre_tot,
            pre_s_cor / pre_s_tot, pre_f_cor / pre_f_tot,
        ))
        print("post: {}/{} ({:.2f}), skill: {:.2f}, fact: {:.2f}".format(
            post_cor, post_tot, post_cor / post_tot,
            post_s_cor / post_s_tot, post_f_cor / post_f_tot
        ))

        study_tot = a['study']['correct'] + a['study']['incorrect'] + a['study']['hint']
        print("study: {}, {}, {}, demo: {}".format(
            a['study']['correct'], a['study']['incorrect'], 
            a['study']['hint'], a['study']['demo']
        ))

        all_pre_s_cor += pre_s_cor
        all_pre_s_tot += pre_s_tot
        all_pre_f_cor += pre_f_cor
        all_pre_f_tot += pre_f_tot
        all_pre_cor = all_pre_s_cor + all_pre_f_cor
        all_pre_tot = all_pre_s_tot + all_pre_f_tot

        all_post_s_cor += post_s_cor
        all_post_s_tot += post_s_tot
        all_post_f_cor += post_f_cor
        all_post_f_tot += post_f_tot
        all_post_cor = all_post_s_cor + all_post_f_cor
        all_post_tot = all_post_s_tot + all_post_f_tot

    all_pre_p = all_pre_cor / all_pre_tot
    pre_s_p = all_pre_s_cor / all_pre_s_tot
    pre_f_p = all_pre_f_cor / all_pre_f_tot

    all_post_p = all_post_cor / all_post_tot
    post_s_p = all_post_s_cor / all_post_s_tot
    post_f_p = all_post_f_cor / all_post_f_tot

    print()
    print("Total: ")
    print("Pre: {}/{} ({:.2f}), skill: {}/{} ({:.2f}), fact: {}/{} ({:.2f})".format(
        all_pre_cor, all_pre_tot, all_pre_p, 
        all_pre_s_cor, all_pre_s_tot, pre_s_p, 
        all_pre_f_cor, all_pre_f_tot, pre_f_p
    ))
    print("Post: {}/{} ({:.2f}), skill: {}/{} ({:.2f}), fact: {}/{} ({:.2f})".format(
        all_post_cor, all_post_tot, all_post_p, 
        all_post_s_cor, all_post_s_tot, post_s_p, 
        all_post_f_cor, all_post_f_tot, post_f_p
    ))

def main():
    json_fp = sys.argv[1]
    colorama.init(autoreset=True)

    alpha, tau, c, s = 0.177, -0.7, 0.277, 1 # 0.0786
    beta, b_practice, b_study = 5, 1, 0.01

    fact_c, skill_c = 2, 2
    for i in range(1):
        with open(json_fp, 'r') as jf:
            json_data = json.load(jf)
            total = len(json_data["training_set1"])
            for idx, a in enumerate(json_data["training_set1"]):
                start = time.time()
                run_agent([a, alpha, tau, c, s, beta, b_practice, b_study, fact_c, skill_c, idx, total, i])
                print("\nTime: {:.2f} s".format(
                    time.time() - start
                ))

                if DEBUG: print("\n" + ("=" * 20) + "\n\n")

        # show_result()
        # pickle.dump(agent_logs, open("agent_logs.pkl", "wb"))


def main_multi():
    json_fp = sys.argv[1]
    colorama.init(autoreset=True)

    alpha, tau, c, s = 0.177, -0.7, 0.277, 1 # 0.0786
    beta, b_practice, b_study = 5, 1, 0.01

    fact_c, skill_c = 1, 2

    pool = multiprocessing.Pool()
    agents = []
    for i in range(1):
        with open(json_fp, 'r') as jf:
            json_data = json.load(jf)
            total = len(json_data["training_set1"])
            for idx, a in enumerate(json_data["training_set1"]):
                # if not check_if_f_sppp(a):
                #     continue
                agents.append([a, alpha, tau, c, s, beta, b_practice, b_study, fact_c, skill_c, idx, total, i])

    start = time.time()
    pool.map(run_agent, agents)
    print("\nTime: {:.2f} s".format(time.time() - start))


def check_if_f_sppp(a):
    qf = a['problem_set'][6]['question_file']
    return '_f_we' in qf


if __name__ == "__main__":
    # main()
    main_multi()