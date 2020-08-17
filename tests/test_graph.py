from graphviz import Digraph

from graph import Graph
from graph.graph import Cluster


class TestGraph:
    def test_dot(self):
        d = Digraph()
        d.node("A")
        d.node("B")
        d.edge("A", "B")

        g = Graph()
        g.edge("A", "B")
        assert str(g.dot()) == str(d)

    def test_remove(self):
        g = Graph()
        g.edge("A", "B")
        g.remove("B")

        d = Digraph()
        d.node("A")

        assert str(g.dot()) == str(d)

    def test_remove_from_cluster(self):
        g = Graph()
        g.edge("a.1", "b")
        g.edge("a.2", "b")

        # 内部表現が漏れ出しているのであとで直す
        cl = Cluster(name="a", label="a")
        cl.node("a.1")
        cl.node("a.2")

        g.cluster(cl)
        g.remove("a.1")

        d = Digraph()
        d.node("a.2")
        d.node("b")
        d.edge("a.2", "b")

        sub = Digraph(name="cluster_a")
        sub.attr(label="a")
        sub.node("a.2")
        d.subgraph(sub)

        assert str(g.dot()) == str(d)

    def test_remove_all_from_cluster(self):
        g = Graph()
        g.edge("a.1", "b")
        g.edge("a.2", "b")

        # 内部表現が漏れ出しているのであとで直す
        cl = Cluster(name="a", label="a")
        cl.node("a.1")
        cl.node("a.2")

        g.cluster(cl)
        g.remove("a.1")
        g.remove("a.2")

        d = Digraph()
        d.node("b")

        assert str(g.dot()) == str(d)

    def test_dig_pair_tail(self):
        g = Graph()
        g.edge("a", "b")

        m = [("a.1", "b.1"), ("a.2", "b.1"), ("b", "c")]

        g.dig("a", m)

        d = Digraph()
        d.node("a.1")
        d.node("a.2")
        d.node("b")
        d.edge("a.1", "b")
        d.edge("a.2", "b")

        sub = Digraph(name="cluster_a")
        sub.attr(label="a")
        sub.node("a.1")
        sub.node("a.2")
        d.subgraph(sub)

        assert(str(g.dot()) == str(d))

    def test_dig_pair_head(self):
        g = Graph()
        g.edge("a", "b")

        m = [("a.1", "b.1"), ("a.2", "b.2")]

        g.dig("b", m)

        d = Digraph()
        d.node("a")
        d.node("b.1")
        d.node("b.2")
        d.edge("a", "b.1")
        d.edge("a", "b.2")

        sub = Digraph(name="cluster_b")
        sub.attr(label="b")
        sub.node("b.1")
        sub.node("b.2")
        d.subgraph(sub)

        assert(str(g.dot()) == str(d))

    def test_dig_inner_edge(self):
        """内側のノード同士の関連づけが反映されるかどうか"""

        g = Graph()
        g.edge("a", "b")

        m = [("a.1", "b.1"), ("a.2", "b.2"), ("b.1", "b.2")]

        g.dig("b", m)

        d = Digraph()
        d.node("a")
        d.node("b.1")
        d.node("b.2")
        d.edge("a", "b.1")
        d.edge("a", "b.2")
        d.edge("b.1", "b.2")

        sub = Digraph(name="cluster_b")
        sub.attr(label="b")
        sub.node("b.1")
        sub.node("b.2")
        d.subgraph(sub)

        assert(str(g.dot()) == str(d))
