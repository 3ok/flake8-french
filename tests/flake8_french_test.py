from __future__ import annotations

import ast
import io
import tokenize

from flake8_french import Plugin


def _tokens(src: str) -> list[tokenize.TokenInfo]:
    sio = io.StringIO(src)
    return list(tokenize.generate_tokens(sio.readline))


def results(s: str) -> set[str]:
    tree = ast.parse(s)
    tokens = _tokens(s)
    return {'{}:{}: {}'.format(*r) for r in Plugin(tree, tokens).run()}


def test_trivial():
    assert not results('')


def test_flaek8_french():
    src = "a = rf'hello hello world'"
    msg, = results(src)
    assert msg == (
        "1:4: FRE001 Use 'fr' to specify a raw f-string instead of 'rf'"
    )
