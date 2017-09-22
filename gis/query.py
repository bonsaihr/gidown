from io import StringIO


def all_of(words):
    return " ".join(words)


def phrase(words):
    return '"{}"'.format(words)


def any_of(words):
    return " OR ".join(words)


def none_of(words):
    return " ".join("-{}".format(word) for word in words)


def on_site(domain):
    return "site:{}".format(domain)


class QueryBuilder:
    def __init__(self, initial_query=""):
        self._query = StringIO()
        self.add(str(initial_query))

    def add(self, *words):
        print(all_of(words), sep=" ", end=" ", file=self._query)
        return self

    def add_phrase(self, words):
        print(phrase(words), sep=" ", end=" ", file=self._query)
        return self

    def add_choice(self, *words):
        print(any_of(words), sep=" ", end=" ", file=self._query)
        return self

    def exclude(self, *words):
        print(none_of(words), sep=" ", end=" ", file=self._query)
        return self

    def add_site_restriction(self, domain):
        print(on_site(domain), sep=" ", end=" ", file=self._query)
        return self

    def __str__(self):
        return self._query.getvalue().strip()

    def __getattr__(self, name):
        if hasattr(str, name):
            func = getattr(str, name)
            return lambda *args, **kwargs: func(str(self), *args, **kwargs)
        raise AttributeError(name)
