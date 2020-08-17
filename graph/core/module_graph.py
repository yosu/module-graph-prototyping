import dataclasses
from typing import List, Set

from graphviz import Digraph

from .module_cluster import ModuleCluster
from .module_edge import ModuleEdge
from .module_edge_list import ModuleEdgeList
from .module_node import ModuleNode


@dataclasses.dataclass
class ModuleGraph:
    nodes: Set[ModuleNode] = dataclasses.field(default_factory=set)
    edges: Set[ModuleEdge] = dataclasses.field(default_factory=set)
    clusters: List[ModuleCluster] = dataclasses.field(default_factory=list)

    def node(self, node: ModuleNode):
        self.nodes.add(node)

    def edge(self, edge: ModuleEdge):
        self.edges.add(edge)

        self.node(edge.tail)
        self.node(edge.head)

    def cluster(self, cl: ModuleCluster):
        self.clusters.append(cl)

    def remove(self, node: ModuleNode):
        if node in self.nodes:
            self.nodes.remove(node)

        edges = list(filter(lambda e: e.has_node(node), self.edges))
        for edge in edges:
            self.edges.remove(edge)

        self._remove_node_from_cluster(node)

    def _remove_node_from_cluster(self, node: ModuleNode):
        for cluster in self.clusters:
            cluster.remove(node)

            if cluster.is_empty:
                self.clusters.remove(cluster)

    def successors(self, node: ModuleNode) -> List[ModuleNode]:
        return [e.head for e in self.edges if e.tail == node]

    def predecessors(self, node: ModuleNode) -> List[ModuleNode]:
        return [e.tail for e in self.edges if e.head == node]

    # TODO: メソッド名の変更
    def dot(self) -> Digraph:
        d = Digraph()

        for node in sorted(self.nodes):
            d.node(name=node.path.name)

        for edge in sorted(self.edges):
            d.edge(edge.tail.name, edge.head.name)

        for cluster in self.clusters:
            cd = cluster.graph()
            d.subgraph(cd)

        return d

    # edgesを受け取るのは仮のインタフェース（テストのため）
    def dig(self, node: ModuleNode, edges: ModuleEdgeList):

        self._dig_successors(node, edges)
        self._dig_predecessors(node, edges)
        self._dig_clustering(node, edges)
        self._dig_inner_edge(node, edges)

        self.remove(node)

    def _dig_inner_edge(self, node: ModuleNode, edge_list: ModuleEdgeList):
        for edge in edge_list.find_edges(node):
            self.edge(edge)

    def _dig_clustering(self, node: ModuleNode, edge_list: ModuleEdgeList):
        cl = ModuleCluster(node=node)
        for n in edge_list.find_nodes(node):
            cl.add(n)

        self.cluster(cl)

    def _dig_successors(self, node: ModuleNode, edge_list: ModuleEdgeList):
        # 現在のnodeからの接続先エッジを取得
        current_edges = ModuleEdgeList([ModuleEdge(node, s) for s in self.successors(node)])

        for new_edge in edge_list:
            parent_edge = current_edges.find_parent_edge(new_edge)

            if parent_edge:
                # ノード分解した新しいノードから、ノード分解していないノードへつなぐ
                edge = ModuleEdge(new_edge.tail, parent_edge.head)
                self.edge(edge)

    def _dig_predecessors(self, node: ModuleNode, edge_list: ModuleEdgeList):
        # 現在のnodeからの接続元エッジを取得
        current_edges = ModuleEdgeList([ModuleEdge(p, node) for p in self.predecessors(node)])

        for new_edge in edge_list:
            parent_edge = current_edges.find_parent_edge(new_edge)

            if parent_edge:
                # ノード分解した新しいノードから、ノード分解していないノードへつなぐ
                edge = ModuleEdge(parent_edge.tail, new_edge.head)
                self.edge(edge)
