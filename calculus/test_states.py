from calculus.states import States, INT, ADD, POW, DX, SPLIT

def test_basic_single():
    env = States([2, 3])
    assert 1 == 1

def test_init_single():
    env = States([2])
    assert env.show() == f"{INT} ({POW} (x, 2))"

def test_init_multiple():
    env = States([2, 3, 4])
    assert env.show() == f"{INT} ({ADD} ({POW} (x, 2), {POW} (x, 3), {POW} (x, 4)))"

def _print_a(sai):
    print(f"s: {sai['selection']}, a: {sai['action']}, i: {sai['input']}")

def test_correct_actions_single():
    env = States([2])
    while not env.done:
        sai = env.get_correct_action()
        _print_a(sai)
        env.apply(sai)

    # assert sai['selection'] == env.root.id
    # assert sai['action'] == DX

def test_correct_actions_multiple():
    env = States([2, 3, 5, 21])
    while not env.done:
        sai = env.get_correct_action()
        _print_a(sai)
        env.apply(sai)
    # assert sai['selection'] == env.root.id
    # assert sai['action'] == SPLIT

def test_state_map():
    env = States([2, 3])
    print(env.get_state_map())

if __name__ == '__main__':
    test_correct_actions_multiple()