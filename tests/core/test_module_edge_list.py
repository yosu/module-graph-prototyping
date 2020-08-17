from tests.core.helper import edge_list


class TestModuleEdgeList:
    def test_limit_path_level(self):
        edges = edge_list([("a.b", "x.y.z"), ("m.n.o", "p.q")])

        assert edges.limit_path_level(1) == edge_list([("a", "x"), ("m", "p")])
        assert edges.limit_path_level(2) == edge_list([("a.b", "x.y"), ("m.n", "p.q")])
        assert edges.limit_path_level(3) == edge_list([("a.b", "x.y.z"), ("m.n.o", "p.q")])
        assert edges.limit_path_level(4) == edge_list([("a.b", "x.y.z"), ("m.n.o", "p.q")])
