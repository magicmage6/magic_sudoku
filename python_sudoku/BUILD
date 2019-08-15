py_library(
    name = "sudoku_data",
    srcs = ["sudoku_data.py"],
)

py_library(
    name = "sudoku_generator",
    srcs = ["sudoku_generator.py"],
)

py_library(
    name = "sudoku_solver",
    srcs = ["sudoku_solver.py"],
)

py_library(
    name = "sudoku_ui",
    srcs = ["sudoku_ui.py"],
    deps = [
        ":sudoku_data",
        ":sudoku_generator",
        ":sudoku_solver",
    ],
)

py_binary(
    name = "sudoku",
    srcs = ["sudoku.py"],
    python_version = "PY3",
    deps = [
        ":sudoku_ui",
    ],
)

py_library(
    name = "generator_test",
    srcs = ["generator_test.py"],
    deps = [
        ":sudoku_data",
        ":sudoku_solver",
    ],
)

py_library(
    name = "solver_test",
    srcs = ["solver_test.py"],
    data = glob(
        [
            "test_data/partial/*.data",
            "test_data/full/*.data",
        ],
    ),
    deps = [
        ":sudoku_data",
        ":sudoku_solver",
    ],
)

py_binary(
    name = "sudoku_test",
    srcs = ["sudoku_test.py"],
    python_version = "PY3",
    deps = [
        ":generator_test",
        ":solver_test",
    ],
)
