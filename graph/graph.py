import dataclasses
from typing import List, Set, Tuple

from graphviz import Digraph

from graph.core.module_graph import ModuleGraph
from graph.core.module_edge_list import ModuleEdgeList
from graph.core.module_edge import ModuleEdge
from graph.core.module_node import ModuleNode
from graph.core.module_cluster import ModuleCluster


@dataclasses.dataclass
class Cluster:
    name: str
    label: str
    nodes: Set[str] = dataclasses.field(default_factory=set)

    @property
    def is_empty(self) -> bool:
        return not bool(self.nodes)

    def node(self, node: str):
        self.nodes.add(node)

    def remove(self, node: str):
        if node in self.nodes:
            self.nodes.remove(node)

    def graph(self):
        g = Digraph(name=f"cluster_{self.name}")
        g.attr(label=self.label)

        for node in sorted(self.nodes):
            g.node(node)

        return g


@dataclasses.dataclass
class Graph:
    _graph: ModuleGraph = dataclasses.field(default_factory=ModuleGraph)

    def node(self, name: str):
        node = ModuleNode.from_str(name)
        self._graph.node(node)

    def edge(self, tail_name: str, head_name: str):
        edge = ModuleEdge.from_str(tail_name, head_name)
        self._graph.edge(edge)

    def cluster(self, cl: Cluster):
        mcl = ModuleCluster(
            node=ModuleNode.from_str(cl.name),
            children=set([ModuleNode.from_str(node) for node in cl.nodes])
        )
        self._graph.cluster(mcl)

    # TODO: メソッド名の変更
    def dot(self) -> Digraph:
        return self._graph.dot()

    def remove(self, node: str):
        self._graph.remove(ModuleNode.from_str(node))

    # edgesを受け取るのは仮のインタフェース（テストのため）
    def dig(self, node: str, edges: List[Tuple[str, str]]):
        mod = ModuleNode.from_str(node)
        edge_list = ModuleEdgeList.from_tuple_list(edges)

        self._graph.dig(node=mod, edges=edge_list)
