import pickle
from itertools import chain
from random import choice, sample, shuffle

from apprentice.agents.MemoryAgent import MemoryAgent
from apprentice.agents.ModularAgent import ModularAgent
from apprentice.working_memory.representation import Sai

from memory.shared.config import *
from memory.shared.const import *


def create_agent(name, function_set, alpha, tau, c, s, beta, b_practice, b_study):
    if AGENT_TYPE == 'memory':
        agent = MemoryAgent(
            agent_name=name,
            function_set=function_set,
            # feature_set=["equals"],
            feature_set=[],
            when_learner="decisiontree",
            # when_learner="alwaystrue",
            where_learner="mostspecific",
            planner=PLANNER,
            search_depth=3,
            alpha=alpha,
            tau=tau,
            c=c,
            s=s,
            beta=beta,
            b_practice=b_practice,
            b_study=b_study,
            print_log=DEBUG,
            # use_memory=False
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


def read_problems():
    study = pickle.load(open('../../data/alg-study.pkl', 'rb'))
    post = pickle.load(open('../../data/alg-post.pkl', 'rb'))
    return study, post


def get_post_test_problems(study, post, ktype):
    post_problems = []
    problems_by_concept = []
    for c, problems in study.items():
        if c not in SELECTED_PROBLEMS:
            continue 
        seen = []
        study_problems = []
        if ktype == KTYPE_FACT:
            selected = choice(problems)
            selected['seen'] = True
            seen.append(selected['ans'])
            for _ in range(STUDY_PROBLEM_NUM):
                study_problems.append(selected)
        elif ktype == KTYPE_SKILL:
            problems = sample(problems, STUDY_PROBLEM_NUM)
            # problems = [problems[3], problems[2]]
            seen = [p['ans'] for p in problems]

            selected = problems[0]
            selected['seen'] = True

            study_problems.extend(problems)

        problems_by_concept.append(study_problems)
        problems = sample(post[c], 3)
        while any([True if p['ans'] in seen else False for p in problems]):
            problems = sample(post[c], 3)

        for _ in range(3):
            problems.append(selected)
        post_problems.extend(problems)

    temps = zip(*problems_by_concept)
    study_problems = list(chain(*temps))
    shuffle(post_problems)

    return study_problems, post_problems


def generate_sai(val, selection='answer', action="UpdateTextField"):
    return Sai(selection=selection, action=action, inputs={'value': f'{val}'})


IIDDXX = 0
def random_num():
    global IIDDXX

    IIDDXX += 1
    return (IIDDXX % 15) + 1
    # return randint(1, 15)