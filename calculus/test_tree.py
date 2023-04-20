from calculus.tree import Node

def test_node_basic():
    n1 = Node('*')
    n2 = Node('2', n1)
    n3 = Node('3', n1)

    assert len(n1.children) == 2
    assert not n1.is_leaf()
    assert n2.is_leaf()
    assert n3.is_leaf()

    assert n2.show() == '2'
    assert n1.show() == '* (2, 3)'
