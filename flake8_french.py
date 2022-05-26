from __future__ import annotations

import ast
import importlib.metadata
import re
import tokenize
from typing import Any
from typing import Iterator


MSG = "FRE001 Use 'fr' to specify a raw f-string instead of 'rf'"
_string_re = re.compile("^([^'\"]*)")


def get_string_prefix(src: str) -> str:
    """parse a string literal to find its prefix."""
    # Credits to https://github.com/asottile/tokenize-rt
    match = _string_re.match(src)
    assert match is not None
    return match[1]


class Plugin:
    name = __name__
    version = importlib.metadata.version(__name__)

    def __init__(
        self,
        tree: ast.AST,
        file_tokens: list[tokenize.TokenInfo],
    ) -> None:
        self.tokens = file_tokens

    def run(self) -> Iterator[tuple[int, int, str, type[Any]]]:
        for token in self.tokens:
            if token.type == tokenize.STRING:
                prefix = get_string_prefix(token.string)
                if prefix == 'rf':
                    yield token.start[0], token.start[1], MSG, type(self)
