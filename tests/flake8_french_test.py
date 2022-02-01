from flake8_french import Plugin


def results(s):
    return {'{}:{}: {}'.format(*r) for r in Plugin(s).run()}


def test_trivial():
    assert not results('')


def test_flaek8_french():
    src = """a = rf'hello hello world'"""
    msg, = results(src)
    assert msg == (
        "1:4: FRE001 Use 'fr' to specify "
        "a raw f-string instead of 'rf'"
    )
