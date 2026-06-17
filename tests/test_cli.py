"""Tests for the CLI."""

from __future__ import annotations

import pytest

from euclidean_rhythm.cli import run


def test_run_son_clave(capsys: pytest.CaptureFixture[str]) -> None:
    code = run(["3", "8"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out.strip() == "x..x..x."


def test_run_bossa_nova(capsys: pytest.CaptureFixture[str]) -> None:
    code = run(["5", "8"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out.strip() == "x.xx.xx."


def test_run_no_args(capsys: pytest.CaptureFixture[str]) -> None:
    code = run([])
    assert code == 1


def test_run_one_arg(capsys: pytest.CaptureFixture[str]) -> None:
    code = run(["3"])
    assert code == 1


def test_run_bad_args(capsys: pytest.CaptureFixture[str]) -> None:
    code = run(["bad", "8"])
    assert code == 1


def test_run_invalid_values(capsys: pytest.CaptureFixture[str]) -> None:
    code = run(["9", "4"])
    assert code == 1
