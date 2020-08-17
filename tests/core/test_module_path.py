from tests.core.helper import path


class TestModule:
    def test_path_level(self):
        assert path("a").path_level == 1
        assert path("foo").path_level == 1
        assert path("a.b.c").path_level == 3

    def test_belongs_to(self):
        assert path("a").belongs_to(path("a"))
        assert path("a.a").belongs_to(path("a"))
        assert not path("a").belongs_to(path("a.a"))

    def test_limit_path_level(self):
        p1 = path("a.b.c")

        assert p1.limit_path_level(1) == path("a")
        assert p1.limit_path_level(2) == path("a.b")
        assert p1.limit_path_level(3) == path("a.b.c")
        assert p1.limit_path_level(4) == path("a.b.c")
