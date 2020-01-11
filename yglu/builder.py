from yglu import loader
from yglu.tree import (Scalar, Sequence, Mapping)
from yglu.expression import Expression
from ruamel.yaml.nodes import (ScalarNode, SequenceNode, MappingNode)
from ruamel.yaml.comments import TaggedScalar


def build(source):
    return convert(loader.load(source))


def convert(node, expression=False):
    if isinstance(node, dict):
        return Mapping([(k, convert(v)) for (k, v) in node.items()])
    if isinstance(node, list):
        return Sequence([convert(v) for v in node])
    if isinstance(node, TaggedNode):
        return node.create()
    if expression:
        return Expression(node)
    return Scalar(node)


class TaggedNode:
    def __init__(self, value):
        self.value = value


class InvisibleNode(TaggedNode):
    def create(self):
        result = convert(self.value, expression=True)
        result.visible = False
        return result


class ExpressionNode(TaggedNode):
    def create(self):
        result = Expression(self.value)
        return result


def invisible_constructor(self, node):
    if isinstance(node, ScalarNode):
        return InvisibleNode(self.construct_scalar(node))
    if isinstance(node, MappingNode):
        return InvisibleNode(self.construct_yaml_map(node))
    if isinstance(node, SequenceNode):
        return InvisibleNode(self.construct_sequence(node))


def expression_constructor(self, node):
    if isinstance(node, ScalarNode):
        return ExpressionNode(self.construct_scalar(node))
    assert False, "Expressions must be scalar"


loader.add_constructor('!?', expression_constructor)
loader.add_constructor('!-', invisible_constructor)
