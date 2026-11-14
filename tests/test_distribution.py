"""文書のリンクとコード、サンプル、配布物のマーカーを検証する."""

import re
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
DOCUMENTS = [ROOT / "README.md", ROOT / "README.ja.md"]
EXAMPLES = sorted((ROOT / "examples").glob("*.py"))


LINKS = [
    (document, target)
    for document in DOCUMENTS
    for target in re.findall(r"\]\((?!https?:)([^)#]+)", document.read_text(encoding="utf-8"))
]
CODE_BLOCKS = [
    pytest.param(block, id=f"{document.name}-{index}")
    for document in DOCUMENTS
    for index, block in enumerate(re.findall(r"```python\n(.*?)```", document.read_text(encoding="utf-8"), re.DOTALL))
]


@pytest.mark.parametrize(("document", "target"), LINKS)
def test_relative_links_exist(document, target):
    assert (document.parent / target).exists()


@pytest.mark.parametrize("block", CODE_BLOCKS)
def test_python_code_blocks_run(block):
    exec(compile(block, "<document>", "exec"), {})  # noqa: S102 -- this repository's own documentation


def test_examples_are_present():
    assert EXAMPLES


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda path: path.name)
def test_examples_run(path, capsys):
    runpy.run_path(str(path), run_name="__main__")
    assert capsys.readouterr().out


def test_typing_marker_is_packaged():
    assert (ROOT / "src" / "aulos" / "py.typed").is_file()
