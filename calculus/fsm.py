def _compare_sai(correct, sel, action, val):
    sai = correct['sai']
    return (sel == sai['selection'] and action == sai['action'] and str(val) == str(sai['input']))

class FSM:
    def __init__(self, _states):
        self.step = 0
        self._states = _states
        self.states = self._states.states[0]
        self.actions = self._states.correct_actions

    def inc_step(self):
        self.step += 1
        # print(f'Go from {self.step-1} to {self.step}')
        if self.step < len(self._states.states):
            self.states = self._states.states[self.step]

    def get_state(self):
        return self.states

    def apply(self, sel, action, input):
        if not _compare_sai(self.hint(), sel, action, input):
            return False
        
        self.inc_step()
        return True
    
    def hint(self):
        return self.actions[self.step]

    @property
    def is_done(self):
        return self.step >= len(self._states.states)
