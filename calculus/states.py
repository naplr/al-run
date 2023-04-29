from tree import Node
import copy


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
        'action_type': action,
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
# INT, POW, ADD, DIV = '[INT]', '[POW]', '[ADD]', '[DIV]'
INT, POW, ADD, DIV = '∫', '^', '+', '/'
def generate_tree(ns):
    root = Node(INT)
    if len(ns) > 1:
        node = Node(ADD)
        root.add_child(node)
    else:
        node = root

    for n in ns:
        p = Node(POW)
        node.add_child(p)
        x = Node('x')
        e = Node(str(n))
        p.add_child(x)
        p.add_child(e)

    return root

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
        # Node.node_count = 0
        self.root = generate_tree(ns)
        self.step = 0
        self.done = False

    def show(self):
        return self.root.show()

    def get_state_map(self):
        return self._get_state_map(self.root)

    @staticmethod
    def _get_state_map(node):
        acc = {node.id: node}
        for c in node.children:
            acc.update(States._get_state_map(c))
        return acc 

    def get_state(self):
        states = self._get_state(self.root)
        states = {s['id']: s for s in states}
        states['DONE'] = {
            'id': 'DONE',
            'type': 'TreeButton'
        }
        return copy.deepcopy(states)
    
    @staticmethod
    def _get_state(node):
        states = [
            {
                'id': node.id,
                'value': str(node.val) if node.val else 'NONE',
                'parent': node.parent.id if node.parent else None,
                'children': [c.id for c in node.children],
                'type': 'Node'
            }
        ]

        for c in node.children:
            states.extend(States._get_state(c))
        return states

    def inc_idx(self):
        self.lastidx += 1
        return self.lastidx

    def get_correct_action(self):
        if self.root.val == INT:
            if len(self.root.children) > 1:
                print(f"[ERROR] Something wrong! There are more than one child node for {INT}")
            elif self.root.children[0].val == ADD:
                return a(SPLIT, self.root.id)
            elif self.root.children[0].val == POW:
                return a(DX, self.root.id)
        elif self.root.val == ADD:
            for c in self.root.children:
                if c.val == INT and len(c.children) == 1 and c.children[0].val == POW:
                    return a(DX, c.id)
            return a('DONE', 'DONE')
        elif self.root.val == DIV:
            return a('DONE', 'DONE')

    def apply(self, sai):
        correct = self._apply(sai)
        if correct:
            self.step += 1
        return correct

    def _apply(self, sai):
        states = self.get_state_map()
        selection, action, inp = sai['selection'], sai['action_type'], sai['input']
        if action == 'DONE':
            addnodes = [s.id for s in states.values() if (s.val == ADD and s.parent is not None and s.parent.val == INT)]
            pownodes = [s.id for s in states.values() if (s.val == POW and s.parent is not None and s.parent.val == INT)]
            if len(addnodes) == 0 and len(pownodes) == 0:
                self.done = True
                return True
            else:
                print(f"[ERROR] Action: {action}, Not done yet.")
                return False

        selected = states[selection]
        if action == SPLIT:
            if selected.val != INT or len(selected.children) != 1 or selected.children[0].val != ADD:
                print(f"[ERROR] Action: {action}, Wrong Condition")
                return False

            add = selected.children[0]
            for c in add.children:
                c.insert(Node(INT))
            add.parent = None
            self.root = add
            return True

        if action == DX:
            if selected.val != INT or len(selected.children) != 1 or selected.children[0].val != POW:
                print(f"[ERROR] Action: {action}, Wrong Condition")
                return False

            power = selected.children[0]
            exp = power.children[1]
            exp.val = str(int(exp.val) + 1)
            div = Node(DIV)
            power.insert(div)
            div.add_child(Node(exp.val))

            new_root = selected.delete()
            if new_root is not None:
                self.root = new_root
            return True
        
        print(f"[ERROR] Unrecognized action: {action}")
        return False


if __name__ == "__main__":
    env = States([2, 3])
    env.get_state()
