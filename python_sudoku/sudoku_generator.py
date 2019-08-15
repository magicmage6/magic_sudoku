"""Sudoku generator."""

import random
import sudoku_data
import sudoku_solver

_NR_SPACES_DICT = {'EASY': 45, 'MEDIUM': 48, 'HARD': 52, 'CHALLENGER': 56}


class SudokuGenerator:
  """Class for sudoku generator."""

  def __init__(self):
    self._level = 0
    self._solver = sudoku_solver.SudokuSolver()

  def is_partial_solvable(self, sudoku):
    """Whether the sudoku can be solved by partial solver."""
    clone = sudoku_data.SudokuData()
    clone.copy(sudoku)
    for _ in range(80):
      partial_solution = self._solver.solve(clone, partial=True)
      if not partial_solution:
        break
    return clone.is_solved()

  def get_sudoku(self, level='EASY'):
    """Generates a random sudoku problem.

    Returns:
      A random generated sudoku problem.
    """
    sudoku = sudoku_data.SudokuData()
    self._solver.solve(sudoku)
    level = level.upper()
    if level not in _NR_SPACES_DICT:
      raise ValueError('Level {} is not valid. Valid levels are {}.'.format(
          level, _NR_SPACES_DICT.keys()))
    nr_spaces = _NR_SPACES_DICT[level]
    for _ in range(100):
      nr_removed = 0
      while nr_removed < nr_spaces:
        row = random.randrange(9)
        col = random.randrange(9)
        if sudoku.get(row, col) != ' ':
          sudoku.set(row, col, ' ')
          nr_removed += 1
      if level == 'EASY' or level == 'MEDIUM':
        if self.is_partial_solvable(sudoku):
          break
      else:
        break
      self._solver.solve(sudoku)
    return sudoku
