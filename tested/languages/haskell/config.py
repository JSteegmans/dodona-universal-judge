import re
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Mapping, Set, Tuple

from tested.datatypes import AllTypes
from tested.dodona import AnnotateCode, Message
from tested.features import Construct, TypeSupport
from tested.languages.config import CallbackResult, Command, Language
from tested.languages.conventionalize import (
    Conventionable,
    NamingConventions,
    submission_file,
)
from tested.languages.utils import (
    cleanup_description,
    executable_name,
    haskell_solution,
)
from tested.serialisation import FunctionCall, Statement, Value

if TYPE_CHECKING:
    from tested.languages.generation import PreparedExecutionUnit


class Haskell(Language):
    def initial_dependencies(self) -> List[str]:
        return ["Values.hs", "EvaluationUtils.hs"]

    def needs_selector(self):
        return True

    def file_extension(self) -> str:
        return "hs"

    def naming_conventions(self) -> Dict[Conventionable, NamingConventions]:
        return {
            "namespace": "pascal_case",
            "identifier": "camel_case",
            "global_identifier": "camel_case",
            "function": "camel_case",
        }

    def datatype_support(self) -> Mapping[AllTypes, TypeSupport]:
        return {
            "integer": "supported",
            "real": "supported",
            "char": "supported",
            "text": "supported",
            "boolean": "supported",
            "sequence": "supported",
            "nothing": "supported",
            "undefined": "reduced",
            "int8": "supported",
            "uint8": "supported",
            "int16": "supported",
            "uint16": "supported",
            "int32": "supported",
            "uint32": "supported",
            "int64": "supported",
            "uint64": "supported",
            "bigint": "supported",
            "single_precision": "supported",
            "double_precision": "supported",
            "list": "supported",
            "tuple": "supported",
        }

    def supported_constructs(self) -> Set[Construct]:
        return {
            Construct.EXCEPTIONS,
            Construct.FUNCTION_CALLS,
            Construct.ASSIGNMENTS,
            Construct.EVALUATION,
            Construct.GLOBAL_VARIABLES,
        }

    def compilation(self, files: List[str]) -> CallbackResult:
        main_ = files[-1]
        exec_ = main_.rstrip(".hs")
        return [
            "ghc",
            "-fno-cse",
            "-fno-full-laziness",
            "-O3" if self.config.options.compiler_optimizations else "-O0",
            main_,
            "-main-is",
            exec_,
        ], [executable_name(exec_)]

    def execution(self, cwd: Path, file: str, arguments: List[str]) -> Command:
        local_file = cwd / file
        return [str(local_file.absolute()), *arguments]

    def modify_solution(self, solution: Path):
        haskell_solution(self, solution)

    def linter(self, remaining: float) -> Tuple[List[Message], List[AnnotateCode]]:
        # Import locally to prevent errors.
        from tested.languages.haskell import linter

        return linter.run_hlint(self.config.dodona, remaining)

    def cleanup_description(self, description: str) -> str:
        return cleanup_description(self, description)

    def cleanup_stacktrace(self, traceback: str) -> str:
        filename = submission_file(self)
        context_file_regex = re.compile(r"(Context[0-9]+|Selector)")
        compile_line_regex = re.compile(r"^([0-9]+)(\s*\|.*)$")
        type_conflict_regex = re.compile(
            r"Couldn't match expected type (.*) with actual type (.*)"
        )
        parse_module = r"error: parse error on input ‘module’"
        replace_module = r"error: unexpected ‘module’"
        traceback = traceback.splitlines()
        skip_line, lines = False, []
        for line in traceback:
            if not line or line == "undefined":
                continue

            # skip line if not a new File line is started
            if context_file_regex.search(line):
                skip_line = True
                continue
            elif skip_line and (line.startswith(" ") or line[0].isdigit()):
                match = type_conflict_regex.search(line)
                if match:
                    lines.append(
                        "Argument type conflict: Couldn't match expected type "
                        f"{match.group(2)} with actual type "
                        f"{match.group(1)}\n"
                    )
                continue

            # replace references to local names
            if filename in line:
                line = line.replace(f"./{filename}", "<code>").replace(
                    filename, "<code>"
                )
            elif "at " in line:
                skip_line = True
                continue
            skip_line = False

            if parse_module in line:
                line = line.replace(parse_module, replace_module)
            else:
                match = compile_line_regex.match(line)
                if match:
                    line = f"{int(match.group(1)) - 1}{match.group(2)}"

            lines.append(line + "\n")
        return "".join(lines)

    def generate_statement(self, statement: Statement) -> str:
        from tested.languages.haskell import generators

        return generators.convert_statement(statement)

    def generate_execution_unit(self, execution_unit: "PreparedExecutionUnit") -> str:
        from tested.languages.haskell import generators

        return generators.convert_execution_unit(execution_unit)

    def generate_selector(self, contexts: List[str]) -> str:
        from tested.languages.haskell import generators

        return generators.convert_selector(contexts)

    def generate_check_function(self, name: str, function: FunctionCall) -> str:
        from tested.languages.haskell import generators

        return generators.convert_check_function(name, function)

    def generate_encoder(self, values: List[Value]) -> str:
        from tested.languages.haskell import generators

        return generators.convert_encoder(values)
