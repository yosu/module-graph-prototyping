from typing import List, Tuple

from graph.core.module_edge import ModuleEdge
from graph.core.module_edge_list import ModuleEdgeList
from graph.core.module_node import ModuleNode
from graph.core.module_path import ModulePath


def path(name: str):
    return ModulePath(name)


def node(name: str) -> ModuleNode:
    return ModuleNode.from_str(name)


def edge(tail: str, head: str) -> ModuleEdge:
    return ModuleEdge.from_str(tail, head)


def edge_list(edges: List[Tuple[str, str]]) -> ModuleEdgeList:
    return ModuleEdgeList.from_tuple_list(edges)
