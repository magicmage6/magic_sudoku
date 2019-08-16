# Magic Sudoku

A Sudoku program written with Python. It is a starter project to learn Python curses library.

# How to run it

```shell
cd python_sudoku
python3 sudoku.py
```

or if you know how to use bazel

```shell
bazel run //python_sudoku:sudoku
```

# Menus to play it

| Key   | Effect |
| ----- | -------- |
|q      | Quit |
|m      | Show menu |
|n      | New sudoku |
|Up     | Cursor up |
|Down   | Cursor down |
|Left   | Cursor left |
|Right  | Cursor right |
|1 - 9  | Fill in a number |
|Space  | Erase a number |
|+      | Increase size |
|-      | Decrease size |
|c      | Change color |
|b      | Change color back |
|a      | Auto solve |
|h      | Hint |
|u      | Undo changes |
|r      | Redo changes |
|Mouse  | Move cursor |

# How to test it

```shell
cd python_sudoku
python3 sudoku_test.py
```

or if you know how to use bazel

```shell
bazel run //python_sudoku:sudoku_test
```
