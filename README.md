# TESTed: universal judge for educational software testing

Organization of the repository:

- `exercise`: contains a series of test exercises, useful as examples and for the test suite
- `tested`: Python project containing the code of the actual judge that will be run by Dodona
- `tests`: Tests for TESTed
- `run` (file): Needed for the Docker image, starts the judge

## Setup

The run TESTed, you need to set up various programming languages and libraries.
See the [dependencies.md](./dependencies.md) file for more information.

## Judge

This is the judge for the TESTed framework.

The source code resides under `src`. The whole judge is implemented as a Python package called `tested`.

This means it should be run as one:

```shell script
python -m tested
```

This will execute the judge expecting a configuration on `stdin` and will print Dodona-output on `stdout`.

Other modes are also available:

- `python -m tested.testplan` will print the JSON Schema of the testplan.
- `python -m tested.manual` will run a hard-coded exercise and solution with logs enabled.
- `python -m tested.serialisation` will print the JSON Schema for only the serialization format (this is also included if you print the testplan schema).
- `python -m tested.translate_dsl` will a DSL testplan to a JSON testplan


Tests should also be run from this directory:

```shell script
python -m pytest tests/test_functionality.py
```
