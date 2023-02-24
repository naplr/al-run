def s(name, value, parent):
    return {
        # 'dom_class': 'CTATTextInput',
        # 'type': 'TextField',
        'id': name,
        'value': str(value) if value else 'NONE',
        'contentEditable': True,
        'parent': parent,
        'type': 'Node'
        # 'children': children
    }

DEL = 'DELETE'
MOD = 'MODIFY'
IT = 'INSERT-TOP'
IB = 'INSERT-BOTTOM'
IR = 'INSERT-RIGHT'

def a(action, sel, input=None):
    return {
        'selection': sel,
        'action': action,
        'input': input
    }

class StatesSingle:
    def __init__(self, n):
        self.n = n
        self.states = self.generate_states(n)
        self.correct_actions = self.get_correct_actions(n)

    def generate_states(self, n):
        return [
            {
                'orig': s('orig', str(n), None),
                'e1': s('e1', '[INT]', None),
                'e2': s('e2', '[POW]', 'e1'),
                'e3': s('e3', 'x', 'e2'),
                'e4': s('e4', str(n), 'e2'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig': s('orig', str(n), None),
                'e1': s('e1', '[DIV]', None),
                'e2': s('e2', '[POW]', None),
                'e3': s('e3', 'x', 'e2'),
                'e4': s('e4', str(n), 'e2'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig': s('orig', str(n), None),
                'e1': s('e1', '[DIV]', None),
                'e2': s('e2', '[POW]', None),
                'e3': s('e3', 'x', 'e2'),
                'e4': s('e4', str(n+1), 'e2'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig': s('orig', str(n), None),
                'e1': s('e1', '[DIV]', None),
                'e2': s('e2', '[POW]', 'e5'),
                'e3': s('e3', 'x', 'e2'),
                'e4': s('e4', str(n+1), 'e2'),
                'e5': s('e6', (n+1), 'e1'),
                'DONE': s('DONE', None, None)
            },
        ]

    def get_correct_actions(self, n):
        return [
            {'sai': a(MOD, 'e1', '[DIV]'), 'foa': []},
            {'sai': a(MOD, 'e4', str(n+1)), 'foa': ['orig']},
            {'sai': a(IR, 'e1', str(n+1)), 'foa': ['e4']},
            {'sai': a('DONE', 'DONE'), 'foa': None}
        ]

class StatesTwo:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.states = self.generate_states(n, m)
        self.correct_actions = self.get_correct_actions(n, m)

    def generate_states(self, n, m):
        return [
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e1': s('e1', '[INT]', None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e3': s('e3', '[POW]', 'e2'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e3': s('e3', '[POW]', 'e2'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e9': s('e9', '[INT]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e9': s('e9', '[INT]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e10': s('e10', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e10'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e9': s('e9', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e10': s('e10', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e10'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e9': s('e9', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e10': s('e10', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e10'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e9': s('e9', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e11': s('e11', str(n+1), 'e9'),
                'e10': s('e10', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e10'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e9': s('e9', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e11': s('e11', str(n+1), 'e9'),
                'e10': s('e10', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e10'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e9': s('e9', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e11': s('e11', str(n+1), 'e9'),
                'e10': s('e10', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e10'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m+1), 'e6'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e9': s('e9', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e11': s('e11', str(n+1), 'e9'),
                'e10': s('e10', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e10'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m+1), 'e6'),
                'e12': s('e12', str(m+1), 'e10'),
                'DONE': s('DONE', None, None)
            },
        ]

    def get_correct_actions(self, n, m):
        return [
            {'sai': a(DEL, 'e1', None), 'foa': []},
            {'sai': a(IT, 'e3', '[INT]'), 'foa': []},
            {'sai': a(IT, 'e6', '[INT]'), 'foa': []},
            {'sai': a(MOD, 'e9', '[DIV]'), 'foa': []},
            {'sai': a(MOD, 'e5', str(n+1)), 'foa': []},
            {'sai': a(IR, 'e9', str(n+1)), 'foa': []},
            {'sai': a(MOD, 'e10', '[DIV]'), 'foa': []},
            {'sai': a(MOD, 'e8', str(m+1)), 'foa': []},
            {'sai': a(IR, 'e10', str(m+1)), 'foa': []},
            {'sai': a('DONE', 'DONE'), 'foa': []}
        ]


class StatesThree:
    def __init__(self, n, m, o):
        self.n = n
        self.m = m
        self.o = o
        self.states = self.generate_states(n, m, o)
        self.correct_actions = self.get_correct_actions(n, m, o)

    def generate_states(self, n, m, o):
        return [
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e1': s('e1', '[INT]', None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e3': s('e3', '[POW]', 'e2'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e3': s('e3', '[POW]', 'e2'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[INT]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[INT]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e13': s('e13', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[INT]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e13': s('e13', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e14': s('e14', '[INT]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n), 'e3'),
                'e13': s('e13', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e14': s('e14', '[INT]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e13': s('e13', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e14': s('e14', '[INT]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e15': s('e15', str(n+1), 'e12'),
                'e13': s('e13', '[INT]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e14': s('e14', '[INT]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e15': s('e15', str(n+1), 'e12'),
                'e13': s('e13', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m), 'e6'),
                'e14': s('e14', '[INT]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e15': s('e15', str(n+1), 'e12'),
                'e13': s('e13', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m+1), 'e6'),
                'e14': s('e14', '[INT]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e15': s('e15', str(n+1), 'e12'),
                'e13': s('e13', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m+1), 'e6'),
                'e16': s('e16', str(m+1), 'e13'),
                'e14': s('e14', '[INT]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e15': s('e15', str(n+1), 'e12'),
                'e13': s('e13', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m+1), 'e6'),
                'e16': s('e16', str(m+1), 'e13'),
                'e14': s('e14', '[DIV]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e15': s('e15', str(n+1), 'e12'),
                'e13': s('e13', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m+1), 'e6'),
                'e16': s('e16', str(m+1), 'e13'),
                'e14': s('e14', '[DIV]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o+1), 'e9'),
                'DONE': s('DONE', None, None)
            },
            {
                'orig1': s('orig1', str(n), None),
                'orig2': s('orig2', str(m), None),
                'orig3': s('orig3', str(o), None),
                'e2': s('e2', '[ADD]', 'e1'),
                'e12': s('e12', '[DIV]', 'e2'),
                'e3': s('e3', '[POW]', 'e9'),
                'e4': s('e4', 'x', 'e3'),
                'e5': s('e5', str(n+1), 'e3'),
                'e15': s('e15', str(n+1), 'e12'),
                'e13': s('e13', '[DIV]', 'e2'),
                'e6': s('e6', '[POW]', 'e2'),
                'e7': s('e7', 'x', 'e6'),
                'e8': s('e8', str(m+1), 'e6'),
                'e16': s('e16', str(m+1), 'e13'),
                'e14': s('e14', '[DIV]', 'e2'),
                'e9': s('e9', '[POW]', 'e2'),
                'e10': s('e10', 'x', 'e9'),
                'e11': s('e11', str(o+1), 'e9'),
                'e17': s('e17', str(o+1), 'e14'),
                'DONE': s('DONE', None, None)
            },
        ]

    def get_correct_actions(self, n, m, o):
        return [
            {'sai': a(DEL, 'e1', None), 'foa': []},
            {'sai': a(IT, 'e3', '[INT]'), 'foa': []},
            {'sai': a(IT, 'e6', '[INT]'), 'foa': []},
            {'sai': a(IT, 'e9', '[INT]'), 'foa': []},

            {'sai': a(MOD, 'e12', '[DIV]'), 'foa': []},
            {'sai': a(MOD, 'e5', str(n+1)), 'foa': []},
            {'sai': a(IR, 'e12', str(n+1)), 'foa': []},

            {'sai': a(MOD, 'e13', '[DIV]'), 'foa': []},
            {'sai': a(MOD, 'e8', str(m+1)), 'foa': []},
            {'sai': a(IR, 'e13', str(m+1)), 'foa': []},

            {'sai': a(MOD, 'e14', '[DIV]'), 'foa': []},
            {'sai': a(MOD, 'e11', str(o+1)), 'foa': []},
            {'sai': a(IR, 'e14', str(o+1)), 'foa': []},

            {'sai': a('DONE', 'DONE'), 'foa': []}
        ]