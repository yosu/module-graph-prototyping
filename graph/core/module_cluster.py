import dataclasses
from typing import Set

from graphviz import Digraph

from graph.core.module_node import ModuleNode


@dataclasses.dataclass
class ModuleCluster:
    node: ModuleNode
    children: Set[ModuleNode] = dataclasses.field(default_factory=set)

    @property
    def is_empty(self) -> bool:
        return not bool(self.children)

    def add(self, node: ModuleNode):
        self.children.add(node)

    def remove(self, node: ModuleNode):
        if node in self.children:
            self.children.remove(node)

    def graph(self) -> Digraph:
        g = Digraph(name=f"cluster_{self.node.name}")
        g.attr(label=self.node.name)

        for node in sorted(self.children):
            g.node(node.name)

        return g
