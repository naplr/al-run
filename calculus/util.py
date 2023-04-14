# from apprentice.agents.ModularAgent import ModularAgent
# from apprentice.agents.ModularAgent import ModularAgent
from apprentice.agents.cre_agents.cre_agent import CREAgent, SAI
# from apprentice.working_memory.representation import Sai
# from apprentice.working_memory import fo_planner_operators

import colorama
from colorama import Fore, Back, Style

def print_log(color, text):
    if color == "blue":
        print(Back.BLUE + Fore.YELLOW + text + Style.RESET_ALL)
    elif color == "green":
        print(Back.GREEN + Fore.BLACK + text + Style.RESET_ALL)
    elif color =="red":
        print(Back.RED + Fore.BLACK + text + Style.RESET_ALL)
    else:
        raise ValueError("Wrong color option to print_log!")


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
        feature_set=[],
        function_set=["DX", "SPLIT", "COEFF"],
        # where="antiunify",
        where="mostspecific",
        fact_types='tree'

    )
    return agent

def generate_local_sai(sel, action, val):
    return {
        "selection": sel,
        "action": action,
        "input": str(val)
    }

def generate_sai(sel, action, val):
    return {
        "selection": sel,
        "action": action, 
        "inputs": {'value': str(val)}
    }
#    return SAI(sel, action, {'value': str(val)})

def generate_sai_from_sai(sai):
    return {
        "selection": sai['selection'],
        "action": sai['action'], 
        "inputs": {'value': str(sai['input'])}
    }
    # return SAI(sai['selection'], sai['action'], {'value': str(sai['input'])})