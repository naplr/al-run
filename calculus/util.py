# from apprentice.agents.ModularAgent import ModularAgent
# from apprentice.agents.ModularAgent import ModularAgent
from apprentice.agents.cre_agents.cre_agent import CREAgent, SAI
# from apprentice.working_memory.representation import Sai
# from apprentice.working_memory import fo_planner_operators

import colorama
from colorama import Fore, Back, Style
from states import INT, ADD, POW

def print_log(color, text):
    if color == "blue":
        print(Back.BLUE + Fore.YELLOW + text + Style.RESET_ALL)
    elif color == "green":
        print(Back.GREEN + Fore.BLACK + text + Style.RESET_ALL)
    elif color =="red":
        print(Back.RED + Fore.BLACK + text + Style.RESET_ALL)
    else:
        raise ValueError("Wrong color option to print_log!")

# -----------------------------------------------
# : Enviornment Configuration        

from apprentice.agents.cre_agents.funcs import register_all_funcs
from apprentice.agents.cre_agents.environment import ( Button, Component,
    register_fact_set, register_all_facts, define_action_type, register_all_action_types, register_action_type_set
    )
from cre import define_fact, CREFunc
from numba.types import string, boolean

with register_all_action_types as Tree_action_type_set:
    @define_action_type("SPLIT", {
        'value' : {'type' : string, "semantic" : False}
        })
    def SPLIT(wm, selection, inputs):
        pass

    @define_action_type("DX", {
        'value' : {'type' : string, "semantic" : False}
        })
    def DX(wm, selection, inputs):
        pass

    @define_action_type("COEFF", {
        'value' : {'type' : string, "semantic" : False}
        })
    def COEFF(wm, selection, inputs):
        pass

    @define_action_type("DONE", {
        'value' : {'type' : string, "semantic" : False}
        })
    def DONE(wm, selection, inputs):
        pass


Tree_action_type_set = {x.name: x for x in Tree_action_type_set}
register_action_type_set(name='tree')(Tree_action_type_set)

with register_all_facts as Tree_fact_types:
    Node = define_fact("Node", {
        "id": str,
        "parent": "Node",
        "children": "List(Node)",
        "value" : {"type" : str, "visible" : True, "semantic": True}

    })

    TreeButton = define_fact("TreeButton", {
        "inherit_from": Node, 
    })

register_fact_set(name='tree')(Tree_fact_types)

@CREFunc(signature=boolean(string, string),
    shorthand = '[IntAndPow]')
def IntAndPow(a, b):
    return a == POW and b == INT

@CREFunc(signature=boolean(string, string),
    shorthand = '[IntAndAdd]')
def IntAndAdd(a, b):
    return a == ADD and b == INT

@CREFunc(signature=string(string),
    shorthand = '[DX]')
def DX(a):
    if a == POW:
        return "[DX]"
    return "[ERROR]"

@CREFunc(signature=string(string),
    shorthand = '[SPLIT]')
def SPLIT(a):
    if a == ADD:
        return "[SPLIT]"
    return "[ERROR]"
    
@CREFunc(signature=string(),
    shorthand = '[COEFF]')
def COEFF():
    return "[COEFF]"

register_all_funcs()


# -- END ENVIRONMENT CONFIG --

def create_agent():
    # agent = ModularAgent(
    #     agent_name="Calculus-Agent",
    #     feature_set=['equals'],
    #     # function_set=["add", "subtract", "multiply", "divide", "pow"],
    #     function_set=["add", "addOne"],
    #     planner="numba",
    #     when_learner="decisiontree",
    #     # where_args={"use_neg": True}
    #     # where_learner="mostspecific",
    #     # where_learner="specifictogeneral",
    #     # where_learner="versionspace",
    # )
    agent = CREAgent(
        agent_name="Calculus-Agent",
        feature_set=["IntAndPow", "IntAndAdd"],
        # feature_set=[],
        function_set=["DX", "SPLIT", "COEFF"],
        where="antiunify",
        when="decisiontree",
        when_args={"encode_relative" : True},
        # where="mostspecific",
        fact_types='tree',
        action_types='tree',
        

    )
    return agent

def generate_local_sai(sel, action_type, val):
    return {
        "selection": sel,
        "action_type": action_type,
        "input": str(val)
    }

def generate_sai(sel, action_type, val):
    return {
        "selection": sel,
        "action_type": action_type, 
        "inputs": {'value': str(val)}
    }
#    return SAI(sel, action, {'value': str(val)})

def generate_sai_from_sai(sai):
    return {
        "selection": sai['selection'],
        "action_type": sai['action_type'], 
        "inputs": {'value': str(sai['input'])}
    }
    # return SAI(sai['selection'], sai['action'], {'value': str(sai['input'])})
