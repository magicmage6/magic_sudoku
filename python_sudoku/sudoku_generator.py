"""Sudoku generator."""

import random
import sudoku_data
import sudoku_solver

_NR_SPACES_DICT = {'EASY': 45, 'MEDIUM': 48, 'HARD': 52, 'CHALLENGER': 56}


class SudokuGenerator:
  """Class for sudoku generator."""

  def __init__(self):
    self._level = 0

  def get_sudoku(self, level='EASY'):
    """Generates a random sudoku problem.

    Returns:
      A random generated sudoku problem.
    """
    solver = sudoku_solver.SudokuSolver()
    sudoku = sudoku_data.SudokuData()
    solver.solve(sudoku)
    if level not in _NR_SPACES_DICT:
      raise ValueError('Level {} is not valid. Valid levels are {}.'.format(
          level, _NR_SPACES_DICT.keys()))
    nr_spaces = _NR_SPACES_DICT[level]
    nr_removed = 0
    while nr_removed < nr_spaces:
      random_number = random.randrange(81)
      row = random_number / 9
      col = random_number % 9
      if sudoku.get(row, col) != ' ':
        sudoku.set(row, col, ' ')
        nr_removed += 1
    return sudoku
