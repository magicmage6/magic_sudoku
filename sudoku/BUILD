py_library(
	name = "sudoku_data",
	srcs = ["sudoku_data.py"],
)

py_library(
	name = "sudoku_ui",
	srcs = ["sudoku_ui.py"],
	deps = [
		":sudoku_data",
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
