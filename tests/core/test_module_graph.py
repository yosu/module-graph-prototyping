from graph.core.module_graph import ModuleGraph
from tests.core.helper import edge, node


class TestModuleGraph:
    def test_successors(self):
        g = ModuleGraph()
        g.edge(edge("A", "B"))

        assert g.successors(node("A")) == [node("B")]
        assert g.successors(node("B")) == []
        assert g.successors(node("C")) == []

    def test_predecessors(self):
        g = ModuleGraph()
        g.edge(edge("A", "B"))

        assert g.predecessors(node("A")) == []
        assert g.predecessors(node("B")) == [node("A")]
        assert g.predecessors(node("C")) == []
