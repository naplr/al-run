
'''
- Some required functions: get_state(), get_nodes(), parse_from_string(), apply() [action at node]
'''


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

class Node:
    # TODO: Should we have types? Like number, variable, op
    node_count = 0
    def __init__(self, val, parent=None):
        Node.node_count += 1
        self.id = f"e{Node.node_count}"
        self.val = val
        self.parent = parent
        if parent is not None:
            parent.add_child(self)
        self.children = []

    def __repr__(self):
        children = [c.val for c in self.children]
        return f"val: {self.val}, parent: {self.parent.val if self.parent else 'None'}, children: {', '.join(children)}"

    def is_leaf(self):
        return not self.children or len(self.children) <= 0

    # TODO: Add order.
    def add_child(self, child, idx=None):
        child.parent = self
        if idx is None:
            self.children.append(child)
        else:
            self.children.insert(idx, child)

    def delete(self): # Return the new root if the current node is a root
        if self.parent is None:
            if len(self.children) > 1:
                print("[ERROR] delete root node with more than one child")
            else:
                self.children[0].parent = None
                return self.children[0]

        for s in self.children:
            s.parent = self.parent
        idx = self.parent.children.index(self)
        self.parent.children = self.parent.children[:idx] + self.children + self.parent.children[idx+1:]
        return None
    
    def insert(self, new_parent): # Insert parent
        idx = self.parent.children.index(self)
        del self.parent.children[idx]
        # self.parent.children.insert(idx, new_parent)
        self.parent.add_child(new_parent, idx)

        new_parent.add_child(self, idx)
        return new_parent

    def modify(self, val):
        self.val = val

    def show(self):
        s = self._show(self)
        print(s)
        return s
        
    @staticmethod
    def _show(node):
        children_repr = [Node._show(c) for c in node.children]
        s = f"{node.val}"
        if len(children_repr) > 0:
            s += f" ({', '.join(children_repr)})"
        return s


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


if __name__ == '__main__':
    n1 = Node('*')
    n2 = Node('2', n1)
    n3 = Node('3', n1)

    n1.show()
    n4 = n3.insert(Node('+'))
    n4.add_child(Node(5))

    n1.show()

    n2.modify(4)
    n1.show()

    n4.delete()
    n1.show()