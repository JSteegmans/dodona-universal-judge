"""
Run the judge manually from code. In this mode, the configs is hardcoded into this
file, allowing rapid testing (and, most importantly, debugging).
"""
import logging
import os
import sys

import shutil
import time
from pathlib import Path

from .configs import DodonaConfig
from .main import run

path = "/home/boris/Documenten/School/2020-2021/Masterproef/TESTed_challenges/exercises/advent of code/2020/tobbogan trajectory - 1/python"

def read_config() -> DodonaConfig:
    """Read the configuration from stdout"""
    return DodonaConfig(**{
        "memory_limit":         536870912,
        "time_limit":           60,
        "programming_language": 'python',
        "natural_language":     'nl',
        "resources":            Path(f'{path}/evaluation'),
        "source":               Path(f'{path}/solution/solution.py'),
        "judge":                Path('.'),
        "workdir":              Path(f'{path}/workdir'),
        "plan_name":            "plan.tson",
        "options":              {
            "parallel": True,
            "mode":     "batch",
            "linter": {
                "python": True
            }
        }
    })


if __name__ == '__main__':
    config = read_config()

    # Enable logging
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # Some modules are very verbose, hide those by default.
    logger = logging.getLogger("tested.judge.collector")
    logger.setLevel(logging.INFO)

    # Create workdir if needed.
    config.workdir.mkdir(exist_ok=True)

    # Delete content in work dir
    # noinspection PyTypeChecker
    for root, dirs, files in os.walk(config.workdir):
        for f in files:
            pass # os.unlink(os.path.join(root, f))
        for d in dirs:
            pass # shutil.rmtree(os.path.join(root, d), ignore_errors=True)

    start = time.time()
    # run(configs, open(os.devnull, "w"))
    # f = open(f"tests/isbn/students/student{STUDENT}/{EXERCISE}.dson", 'w')
    run(config, sys.stdout)
    end = time.time()
    print()
    print(f"Judging took {end - start} seconds (real time)")
