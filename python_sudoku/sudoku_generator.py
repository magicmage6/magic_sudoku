"""Sudoku generator."""

import random
import sudoku_data
import sudoku_solver

_NR_SPACES_DICT = {'EASY': 45, 'MEDIUM': 47, 'HARD': 50, 'CHALLENGER': 52}


class SudokuGenerator:
  """Class for sudoku generator."""

  def __init__(self):
    self._level = 0
    self._solver = sudoku_solver.SudokuSolver()
    self._max_solver = sudoku_solver.SudokuSolver(randomize_type = 'max')
    self._min_solver = sudoku_solver.SudokuSolver(randomize_type = 'min')

  def is_partial_solvable(self, sudoku):
    """Whether the sudoku can be solved by partial solver."""
    clone = sudoku_data.SudokuData()
    clone.copy(sudoku)
    for _ in range(80):
      partial_solution = self._solver.solve(clone, partial=True)
      if not partial_solution:
        break
    return clone.is_solved()

  def has_only_one_solution(self, sudoku):
    """Whether the sudoku has only one solution."""
    clone1 = sudoku_data.SudokuData()
    clone1.copy(sudoku)
    self._max_solver.solve(clone1)
    clone2 = sudoku_data.SudokuData()
    clone2.copy(sudoku)
    self._min_solver.solve(clone2)
    return clone1.is_same(clone2)

  def get_sudoku(self, level='EASY'):
    """Generates a random sudoku problem.

    Returns:
      A random generated sudoku problem.
    """
    sudoku = sudoku_data.SudokuData()
    level = level.upper()
    if level not in _NR_SPACES_DICT:
      raise ValueError('Level {} is not valid. Valid levels are {}.'.format(
          level, _NR_SPACES_DICT.keys()))
    nr_spaces = _NR_SPACES_DICT[level]
    for _ in range(1000):
      sudoku = sudoku_data.SudokuData()
      self._solver.solve(sudoku)
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
      elif level == 'HARD':
        if self.has_only_one_solution(sudoku):
          break
      else:
        if self.has_only_one_solution(sudoku) and not self.is_partial_solvable(sudoku):
          break
    return sudoku
