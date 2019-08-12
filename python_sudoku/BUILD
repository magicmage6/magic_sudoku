py_library(
    name = "sudoku_data",
    srcs = ["sudoku_data.py"],
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

py_binary(
    name = "solver_test",
    srcs = ["solver_test.py"],
    data = glob(
        [
            "test_data/fast_solver/*.data",
            "test_data/full_solver/*.data",
        ]
    ),
    python_version = "PY3",
    deps = [
        ":sudoku_data",
        ":sudoku_solver",
    ],
)