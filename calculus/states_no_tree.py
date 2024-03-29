def st(name, value, parent):
    return {
        # 'dom_class': 'CTATTextInput',
        # 'type': 'TextField',
        'id': name,
        'value': str(value) if value else 'NONE',
        # 'contentEditable': True,
        'parent': parent,
        'type': 'Node'
        # 'children': children
    }

DEL = 'DELETE'
MOD = 'MODIFY'
IT = 'INSERT-TOP'
IB = 'INSERT-BOTTOM'
IR = 'INSERT-RIGHT'
DX = 'DX'
SPLIT = 'SPLIT'
TIME = 'TIME'

def a(action, sel, input=None):
    if input == None:
        input = f"[{action}]"
    return {
        'selection': sel,
        'action': action,
        'input': input
    }

# def _generate_states_with_coeff(ns):
#     states = { 'e1': s('e1', '[INT]', None) }
#     if len(ns) == 1:
#         return {
#             **states,
#             'e2': s('e2', '[POW]', 'e1'),
#             'e3': s('e3', 'x', 'e2'),
#             'e4': s('e4', str(ns[0]), 'e2'),
#         }

#     states['e2'] = s('e2', '[ADD]', 'e1')
#     for idx, (c, n) in enumerate(ns):
#         tidx = idx*3+3
#         states[f'e{tidx}'] = s(f'e{tidx}', '[MUL]', 'e2')
#         states[f'e{tidx+1}'] = s(f'e{tidx+1}', 'x', f'e{tidx}')
#         states[f'e{tidx+2}'] = s(f'e{tidx+2}', str(n), f'e{tidx}')
#         states[f'e{tidx}'] = s(f'e{tidx}', '[POW]', 'e2')
#         states[f'e{tidx+1}'] = s(f'e{tidx+1}', 'x', f'e{tidx}')
#         states[f'e{tidx+2}'] = s(f'e{tidx+2}', str(n), f'e{tidx}')

#     return states

def generate_states(ns):
    states = { 'e1': st('e1', '[INT]', None) }
    if len(ns) == 1:
        return {
            **states,
            'e2': st('e2', '[POW]', 'e1'),
            'e3': st('e3', 'x', 'e2'),
            'e4': st('e4', str(ns[0]), 'e2'),
        }

    states['e2'] = st('e2', '[ADD]', 'e1')
    for idx, n in enumerate(ns):
        tidx = idx*3+3
        states[f'e{tidx}'] = st(f'e{tidx}', '[POW]', 'e2')
        states[f'e{tidx+1}'] = st(f'e{tidx+1}', 'x', f'e{tidx}')
        states[f'e{tidx+2}'] = st(f'e{tidx+2}', str(n), f'e{tidx}')

    return states

# def generate_correct_actions(self, ns):
#     # Check for SPLIT
#     addnodes = [for s in self.states]

#     # Check for DX
#     if len(ns) == 1:
#         return [{'sai': a(DX, 'e1', None), 'foa': []}]

#     actions = [{'sai': a(SPLIT, 'e1', None), 'foa': []}]
#     for idx, n in enumerate(ns):
#         actions.append({'sai': a(DX, 'e1', None), 'foa': []})
#     return actions
#     return [
#         {'sai': a(DX, 'e1', None), 'foa': []},
#         {'sai': a(DX, 'e', str(n+1)), 'foa': ['orig']},
#         {'sai': a(IR, 'e1', str(n+1)), 'foa': ['e4']},
#         {'sai': a('DONE', 'DONE'), 'foa': None}
#     ]

class States:
    def __init__(self, ns):
        self.ns = ns
        self.states = generate_states(ns)
        # for s in self.states.values():
        #     print(s)
        self.lastidx = len(self.states)
        self.step = 0
        self.done = False
        self.show()

    def show(self):
        for s in self.states.values():
            print(f"{s['id']}: parent={s['parent']}, val={s['value']}")

        # roots = [s for s in self.states.values() if s['parent'] == None]
        # print(len(roots))
        # root = roots[0]
        # print(_show(root))

    # def _show(node):
    #     for c in node.children
    #     return children_repr

    def get_state(self):
        return self.states

    def inc_idx(self):
        self.lastidx += 1
        return self.lastidx

    def get_correct_action(self):
        # Check for SPLIT
        targets = [s for s in self.states.values() if (s['value'] == '[ADD]' and s['parent'] is not None and self.states[s['parent']]['value'] == '[INT]')]
        if len(targets) == 1:
            sai = a(SPLIT, targets[0]['parent'])
            self.apply(sai)
            return sai
        elif len(targets) > 1:
            print("[ERROR] Something wrong! There are more than one add node inside [INT]")

        # Check for DX
        targets = [s for s in self.states.values() if (s['value'] == '[POW]' and s['parent'] is not None and self.states[s['parent']]['value'] == '[INT]')]
        if len(targets) == 0:
            sai = a('DONE', 'DONE')
            self.apply(sai)
            return sai

        target = targets[0]
        sai = a(DX, target['parent'])
        self.apply(sai)
        return sai

    def apply(self, sai):
        correct = self._apply(sai)
        if correct:
            self.step += 1
            self.show()

    def _apply(self, sai):
        print(sai)
        selection, action, inp = sai['selection'], sai['action'], sai['input']
        if action == 'DONE':
            addnodes = [s for s in self.states.values() if (s['value'] == '[ADD]' and s['parent'] is not None and self.states[s['parent']]['value'] == '[INT]')]
            pownodes = [s for s in self.states.values() if (s['value'] == '[POW]' and s['parent'] is not None and self.states[s['parent']]['value'] == '[INT]')]
            if len(addnodes) == 0 and len(pownodes) == 0:
                self.done = True
                return True
            else:
                print(f"[ERROR] Action: {action}, Not done yet.")
                return False

        selected = self.states[selection]
        print([s['parent'] for s in self.states.values()])
        print(selection)
        childs = [s for s in self.states.values() if s['parent'] == selection]
        child = childs[0] if len(childs) > 0 else None

        if action == SPLIT:
            if selected['value'] != '[INT]' or child == None or child['value'] != '[ADD]':
                print(f"[ERROR] Action: {action}, Wrong Condition")
                return False

            del selected
            child['parent'] = None
            terms = [s for s in self.states.values() if s['parent'] and s['parent'] == child['id']]
            for t in terms:
                nodeid = f'e{self.inc_idx()}'
                new_node = st(nodeid, '[INT]', child['id'])
                self.states[nodeid] = new_node
                t['parent'] = new_node['id']
            return True

        if action == DX:
            if selected['value'] != '[INT]' or child['value'] != '[POW]':
                print(f"[ERROR] Action: {action}, Wrong Condition")
                return False

            nodeid = f'e{self.inc_idx()}'
            divnode = st(nodeid, '[DIV]', selected['parent']) 
            self.states[nodeid] = divnode
            expnode = [s for s in self.states.values() if (s['parent'] == child['id'] and s['value'] != 'x')][0]
            expnode['value'] = int(expnode['value']) + 1

            nodeid = f'e{self.inc_idx()}'
            dennode = st(nodeid, expnode['value'], divnode['id'])
            self.states[nodeid] = dennode
            child['parent'] = divnode['id']
            del selected
            return True
        
        print(f"[ERROR] Unrecognized action: {action}")
        return False


if __name__ == "__main__":
    env = States([2, 3])
    env.print()
