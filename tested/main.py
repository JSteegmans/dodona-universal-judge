"""
Main file, responsible for running TESTed based on the input given by Dodona.
"""
import os

from typing import IO
from .configs import DodonaConfig, create_bundle
from .testsuite import parse_test_suite
from .dsl import parse_dsl


def run(config: DodonaConfig, judge_output: IO):
    """
    Run the TESTed judge.

    :param config: The configuration, as received from Dodona.
    :param judge_output: Where the judge output will be written to.
    """
    with open(f"{config.resources}/{config.test_suite}", "r") as t:
        textual_suite = t.read()

    _, ext = os.path.splitext(config.test_suite)
    is_yaml = ext.lower() in (".yaml", ".yml")
    if is_yaml:
        suite = parse_dsl(textual_suite)
    else:
        suite = parse_test_suite(textual_suite)
    pack = create_bundle(config, judge_output, suite)
    from .judge import judge

    judge(pack)
