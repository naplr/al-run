def s(name, value, parent):
    return {
        # 'dom_class': 'CTATTextInput',
        # 'type': 'TextField',
        'id': name,
        'value': value,
        'contentEditable': True,
        'parent': parent,
        # 'children': children
    }

def state0(n):
    return {
        'e1': s('e1', '[INT]', None),
        'e2': s('e2', '[POW]', 'e1'),
        'e3': s('e3', 'x', 'e2'),
        'e4': s('e4', str(n), 'e2')
    }

def state1(n):
    return {
        'e2': s('e2', '[POW]', None),
        'e3': s('e3', 'x', 'e2'),
        'e4': s('e4', str(n), 'e2')
    }

def state2(n):
    return {
        'e2': s('e2', '[POW]', None),
        'e3': s('e3', 'x', 'e2'),
        'e4': s('e4', str(n+1), 'e2')
    }

def state3(n):
    return {
        'e2': s('e2', '[POW]', 'e5'),
        'e3': s('e3', 'x', 'e2'),
        'e4': s('e4', str(n+1), 'e2'),
        'e5': s('e5', '[DIV]', None)
    }

def state4(n):
    return {
        'e2': s('e2', '[POW]', 'e5'),
        'e3': s('e3', 'x', 'e2'),
        'e4': s('e4', str(n+1), 'e2'),
        'e5': s('e5', '[DIV]', None),
        'e6': s('e6', (n+1), 'e5'),
    }

states = [state0, state1, state2, state3, state4]

DEL = 'DELETE'
MOD = 'MODIFY'
IT = 'INSERT-TOP'
IR = 'INSERT-RIGHT'

def a(action, sel, input=None):
    return {
        'selection': sel,
        'action': action,
        'input': input
    }

def get_correct_actions(n):
    return [
        {'sai': a(DEL, 'e1'), 'foa': ['e1']},
        {'sai': a(MOD, 'e4', str(n+1)), 'foa': ['e4']},
        {'sai': a(IT, 'e2', '[DIV]'), 'foa': ['e2']},
        {'sai': a(IR, 'e5', str(n+1)), 'foa': ['e4', 'e5']},
        {'sai': a('DONE', 'DONE'), 'foa': None}
    ]