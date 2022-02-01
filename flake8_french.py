from __future__ import annotations

import importlib.metadata
import io
import re
import tokenize
from typing import Any
from typing import Iterator


MSG = "FRE001 Use 'fr' to specify a raw f-string instead of 'rf'"
_string_re = re.compile("^([^'\"]*)(.*)$", re.DOTALL)


def parse_string_literal(src: str) -> tuple[str, str]:
    """parse a string literal's source into (prefix, string)."""
    # Credits to https://github.com/asottile/tokenize-rt
    match = _string_re.match(src)
    assert match is not None
    return match.group(1), match.group(2)


class Plugin:
    name = __name__
    version = importlib.metadata.version(__name__)

    def __init__(self, code: str) -> None:
        self.code = code

    def run(self) -> Iterator[tuple[int, int, str, type[Any]]]:
        target = io.StringIO(self.code)
        target.seek(0)

        tokens = tokenize.generate_tokens(target.readline)
        for token in tokens:
            if token.type == 3:  # i.e. string
                prefix, _ = parse_string_literal(token.string)
                if prefix == 'rf':
                    yield token.start[0], token.start[1], MSG, type(self)
