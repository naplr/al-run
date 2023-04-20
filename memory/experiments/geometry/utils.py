from bs4 import BeautifulSoup
from apprentice.agents.MemoryAgent import MemoryAgent
from apprentice.agents.ModularAgent import ModularAgent
from apprentice.working_memory import fo_planner_operators
from apprentice.working_memory.representation import Sai
from random import randint
from memory.shared.config import *

def create_agent(name, alpha, tau, c, s, beta, b_practice, b_study):
    if AGENT_TYPE == 'memory':
        agent = MemoryAgent(
            agent_name=name,
            feature_set=["equals"],
            function_set=["add", "subtract", "multiply", "divide", "circ_rule", "trap_rule", "tria_rule"],
            when_learner="decisiontree2",
            where_learner="mostspecific",
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
            function_set=["add", "subtract", "multiply", "divide", "circ_rule", "trap_rule", "tria_rule"],
            when_learner="decisiontree2",
            where_learner="mostspecific",
        )
    return agent


def generate_sai(val):
    return Sai(selection='answer', action='UpdateTextField', inputs={'value': str(val)})


def random_num_for_state():
    return randint(1, 15)


def parse_brd(brd):
    with open(brd, 'r') as bf:
        contents = bf.read()
        soup = BeautifulSoup(contents, 'lxml-xml')
        messages = soup.stateGraph.startNodeMessages.find_all('message')
        values = {}
        for m in messages:
            if not m.properties.Selection:
                continue
            field = m.properties.Selection.value.text
            val = m.properties.Input.value.text
            values[field] = val

        answer = soup.edge.actionLabel.message.properties.Input.value.text
        state = _get_state(
            values["knowledge_type"],
            values["shape_type"],
            values["practice_type"],
            values["r"],
            values["l"],
            values["w"],
            values["a"],
            values["b"],
            values["h"],
            values["s1"],
            values["s2"],
            values["d"]
        )

        return state, answer

IIDDXX = 0
def random_num():
    global IIDDXX

    IIDDXX += 1
    return (IIDDXX % 15) + 1
    # return randint(1, 15)

def generate_state_and_answer(knowledge_type, shape_type):
    if knowledge_type == "fact":
        ans = ""
        if shape_type == "circle":
            ans = "A=pi*r^2"
        elif shape_type == "triangle":
            ans = "A=1/2*b*h"
        elif shape_type == "rectangle":
            ans = "A=l*w"
        elif shape_type == "trapezoid":
            ans = "A=1/2*(a+b)*h"
        return _get_state(knowledge_type, shape_type), ans

    elif knowledge_type == "skill":
        if shape_type == "circle":
            r = random_num()
            state = _get_state(knowledge_type, shape_type, r=str(r))
            ans = "{}*pi".format(r*r)
        elif shape_type == "triangle":
            b = random_num()
            h = random_num() * 2
            state = _get_state(knowledge_type, shape_type, b=str(b), h=str(h))
            ans = str(int(1/2*b*h))
        elif shape_type == "rectangle":
            l = random_num()
            w = random_num()
            state = _get_state(knowledge_type, shape_type, l=str(l), w=str(w))
            ans = str(int(l*w))
        elif shape_type == "trapezoid":
            a = random_num() * 2
            b = random_num() * 2
            h = random_num()
            state = _get_state(knowledge_type, shape_type, a=str(a), b=str(b), h=str(h))
            ans = str(int(1/2*(a+b)*h))
        return state, ans

### PRIVATE ###

NA = "NA"
def _get_state(
    knowledge_type,
    shape_type,
    practice_type="retrieval_practice",
    r=None,
    l=None,
    w=None,
    a=None,
    b=None,
    h=None,
    s1=None,
    s2=None,
    d=None
):
    CC = "NA"
    if knowledge_type == "skill":
        CC = "0"

    # if knowledge_type == "skill":
    #     if r is None: r = random_num_for_state()
    #     if l is None: l = random_num_for_state()
    #     if w is None: w = random_num_for_state()
    #     if a is None: a = random_num_for_state()
    #     if b is None: b = random_num_for_state()
    #     if h is None: h = random_num_for_state()
    #     if s1 is None: s1 = random_num_for_state()
    #     if s2 is None: s2 = random_num_for_state()
    #     if d is None: d = random_num_for_state()
    # else:
    if r is None: r = CC
    if l is None: l = CC
    if w is None: w = CC
    if a is None: a = CC
    if b is None: b = CC
    if h is None: h = CC
    if s1 is None: s1 = CC
    if s2 is None: s2 = CC
    if d is None: d = CC


    init = {
        'knowledge_type': {
            'dom_class': 'CTATTextInput',
            'offsetParent': 'background-initial',
            'id': 'knowledge_type',
            'type': 'TextField',
            'value': knowledge_type,
            'contentEditable': False,
            'below': 'r',
            'above': '',
            'to_right': 'practice_type',
            'to_le ft': ''
        },
        'shape_type': {
            'dom_class': 'CTATTextInput',
            'offsetParent': 'background-initial',
            'id': 'shape_type',
            'type': 'TextField',
            'value': shape_type,
            'contentEditable': False,
            'below': 's1',
            'above': '',
            'to_right': '',
            'to_left': 'pr actice_type'
        },
        'practice_type': {
            'dom_class': 'CTATTextInput',
            'offsetParent': 'background-initial',
            'id': 'practice_type',
            'type': 'TextField',
            'value': practice_type,
            'contentEditable': False,
            'below': 'a',
            'above': '',
            'to_right': 'shape_type',
            'to_left': 'knowledge_type'
        },
        'answer': {
            'dom_class': 'CTATTextInput',
            'offsetParent': 'background-initial',
            'id': 'answer',
            'type': 'TextField',
            'value': '',
            'contentEditable': True,
            'below': '',
            'above': 'r',
            'to_right': 'done',
            'to_left': ''
        },
        'done': {
            'dom_class': 'CTATDoneButton',
            'offsetParent': 'background-initial',
            'id': 'done',
            'type': 'Component',
            'below': '',
            'above': 's2',
            'to_right': '',
            'to_left': 'answer'
        }
    }


    def has_var(v):
        return v and v != NA and v != 0 and v != "0"

    init['r'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 'r',
        'type': 'TextField',
        'value': r,
        'contentEditable': False,
        'below': 'answer',
        'above': 'knowledge_type',
        'to_right': 'l',
        'to_left': ''
    }

    init['l'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 'l',
        'type': 'TextField',
        'value': l,
        'contentEditable': False,
        'below': 'answer',
        'above': 'knowledge_type',
        'to_right': 'w',
        'to_left': 'r'
    }

    init['w'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 'w',
        'type': 'TextField',
        'value': w,
        'contentEditable': False,
        'below': 'answer',
        'above': 'knowledge_type',
        'to_right': 'a',
        'to_left': 'l'
    }

    init['a'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 'a',
        'type': 'TextField',
        'value': a,
        'contentEditable': False,
        'below': 'answer',
        'above': 'practice_type',
        'to_right': 'b',
        'to_left': 'w'
    }

    init['b'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 'b',
        'type ': 'TextField',
        'value': b,
        'contentEditable': False,
        'below': 'answer',
        'above': 'practice_type',
        'to_right': 'h',
        'to_left': 'a'
    }

    init['h'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 'h',
        'type': 'TextField ',
        'value': h,
        'contentEditable': False,
        'below': 'answer',
        'above': 'practice_type',
        'to_right': 's1',
        'to_left': 'b'
    }

    init['s1'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 's1',
        'type': 'TextField',
        'value': s1,
        'contentEditable': False,
        'below': '',
        'above': 'shape_type',
        'to_right': 's2',
        'to_left': 'h'
    }

    init['s2'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 's2',
        'type': 'TextField',
        'value': s2,
        'contentEdit able': False,
        'below': 'done',
        'above': 'shape_type',
        'to_right': 'd',
        'to_left': 's1'
    }

    init['d'] = {
        'dom_class': 'CTATTextInput',
        'offsetParent': 'background-initial',
        'id': 'd',
        'type': 'TextField',
        'value': d,
        'contentEditable': False,
        'bel ow': 'done',
        'above': 'shape_type',
        'to_right': '',
        'to_left': 's2'
    }
    
    return init
