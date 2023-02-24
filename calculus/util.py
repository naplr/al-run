# from apprentice.agents.ModularAgent import ModularAgent
from apprentice.agents.ModularAgent import ModularAgent
from apprentice.agents.cre_agents.cre_agent import CREAgent, SAI
# from apprentice.working_memory.representation import Sai
from apprentice.working_memory import fo_planner_operators

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
    agent = ModularAgent(
        agent_name="Calculus-Agent",
        feature_set=['equals'],
        # function_set=["add", "subtract", "multiply", "divide", "pow"],
        function_set=["DX", "SPLIT"],
        where="antiunify",
        # where_args={"use_neg": True}
        # where_learner="mostspecific",
        # where_learner="specifictogeneral",
        # where_learner="versionspace",
    )
    return agent

def generate_sai(sel, action, val):
   return SAI(selection=sel, action=action, inputs={'value': str(val)})

def generate_sai_from_sai(sai):
    return SAI(selection=sai['selection'], action=sai['action'], inputs={'value': str(sai['input'])})