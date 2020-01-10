import pytest
from yglu.expression import *
from yglu.tree import *


def test_execution():
    set_scope({'a': 1})
    assert ExpressionNode("$.a + 1").content() == 2


def test_simple_reference():
    m = Mapping()
    s = Sequence()
    m['a'] = Scalar(2)
    m['b'] = ExpressionNode('$.a + 1')
    set_scope(m)
    assert m['b'] == 3


def test_sequence_references():
    m = Mapping()
    s = Sequence()
    m['s'] = s
    s.append(ExpressionNode('$.s[1] + 1'))
    s.append(Scalar(2))
    m['a'] = ExpressionNode('$.s[0] + 1')
    set_scope(m)
    assert m['a'] == 4
    assert m == { 's': [3, 2], 'a': 4 }

def test_multiple_references():
    m = Mapping()
    s = Sequence()
    m['s'] = s
    s.append(ExpressionNode('$.s[1] + 1'))
    s.append(Scalar(2))
    m['a'] = ExpressionNode('$.s[0] + 1')
    m['b'] = ExpressionNode('$["a"] * 2')
    set_scope(m)
    assert m['b'] == 8
    assert m == {'s': [3, 2], 'b': 8, 'a': 4}