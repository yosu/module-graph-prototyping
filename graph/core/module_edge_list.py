import dataclasses
from typing import List, Tuple, Optional

from graph.core.module_edge import ModuleEdge
from graph.core.module_node import ModuleNode


@dataclasses.dataclass(frozen=True)
class ModuleEdgeList:
    _edges: List[ModuleEdge]

    @classmethod
    def from_tuple_list(cls, edges: List[Tuple[str, str]]) -> "ModuleEdgeList":
        return cls([ModuleEdge.from_str(tail=e[0], head=e[1]) for e in edges])

    def find_parent_edge(self, edge: ModuleEdge) -> Optional[ModuleEdge]:
        for e in self._edges:
            if edge.belongs_to(e):
                return e
        return None

    def find_nodes(self, node: ModuleNode) -> List[ModuleNode]:
        result = []

        for new_edge in self._edges:
            if new_edge.head.belongs_to(node):
                result.append(new_edge.head)
            if new_edge.tail.belongs_to(node):
                result.append(new_edge.tail)

        return result

    def find_edges(self, node: ModuleNode) -> List[ModuleEdge]:
        result = []

        for new_edge in self._edges:
            if new_edge.head.belongs_to(node) and new_edge.tail.belongs_to(node):
                result.append(new_edge)

        return result

    def __iter__(self):
        return iter(self._edges)

    def limit_path_level(self, max_path_level: int) -> "ModuleEdgeList":
        assert max_path_level > 0

        new_edges = [e.limit_path_level(max_path_level) for e in self._edges]
        return ModuleEdgeList(new_edges)
