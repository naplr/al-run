
class Problems:
    def __init__(self, problem_string, actions):
        self.problem_string = problem_string
        self.root = None
        self.node_map = {}
        self.actions = actions

    def get_state(self):
        pass

    def apply(self, sai):
        s, a, i = sai['selection'], sai['action'], sai['input']
        n = self.node_map[s]


class BaseAction:
    def __init__(self):
        pass

    @classmethod
    def condition(cls, node):
        raise NotImplemented

    @classmethod
    def apply(cls, node):
        raise NotImplemented



COMMUTE_OPS = ['multiply', 'add']
class MNode:
    def __init__(self, val, parent):
        val = val.strip().lower()
        try:
            val = str(int(float(val)))
        except ValueError:
            pass
        self.val = val
        self.parent = parent
        self.children = []

        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)
        if self.val in COMMUTE_OPS:
            self.children.sort(key=lambda x: x.val, reverse=True)

    def to_zss(self):
        root = Node(self.val)
        for c in self.children:
            n = c.to_zss()
            root.addkid(n)
        return root

    def __repr__(self):
        print(self.val)
        return f"NODE: {self.val}"