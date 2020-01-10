from yglu.tree import *


def test_constant():
    m = Mapping()
    m['a'] = Scalar(1)
    assert m['a'] == 1

    s = Sequence()
    s.append(Scalar('hello'))
    assert s[0] == 'hello'


def test_content():
    class OneNode(Node):
        version = 0

        def create_content(self):
            self.version += 1
            return self.version

    n = OneNode()
    s = Sequence()
    s.append(n)
    s.append(n)
    m2 = Mapping()
    m2['s'] = s
    m = Mapping()
    m['s'] = s
    m['n'] = n
    m['m2'] = m2

    assert m['s'][0] == 1
    assert m['s'][1] == 1
    assert m['n'] == 1
    assert m['m2']['s'] == [1, 1]

    assert m2.content() == {'s': [1, 1]}