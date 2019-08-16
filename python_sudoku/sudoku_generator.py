"""Sudoku generator."""

import random
import sudoku_data
import sudoku_solver


class SudokuGenerator:
  """Class for sudoku generator."""

  def __init__(self):
    self._level = 0
    self._solver = sudoku_solver.SudokuSolver()
    self._max_solver = sudoku_solver.SudokuSolver(randomize_type = 'max')
    self._min_solver = sudoku_solver.SudokuSolver(randomize_type = 'min')
    self._sudoku_map = {'EASY': [], 'MEDIUM': [], 'HARD': [], 'CHALLENGER': []}

  def is_partial_solvable(self, sudoku):
    """Whether the sudoku can be solved by partial solver."""
    clone = sudoku_data.SudokuData()
    clone.copy(sudoku)
    for _ in range(80):
      partial_solution = self._solver.solve(clone, partial=True)
      if not partial_solution:
        break
    return clone.is_solved()

  def make_one_solution(self, sudoku, full_sudoku):
    """Make a sudoku has only one solution."""
    for _ in range(80):
      clone1 = sudoku_data.SudokuData()
      clone1.copy(sudoku)
      self._max_solver.solve(clone1)
      clone2 = sudoku_data.SudokuData()
      clone2.copy(sudoku)
      self._min_solver.solve(clone2)
      is_same = True
      for row in range(9):
        for col in range(9):
          if clone1.get(row, col) != clone2.get(row, col):
            is_same = False
            sudoku.set(row, col, full_sudoku.get(row, col))
            break
        if not is_same:
          break
      if is_same:
        return

      
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
    level = level.upper()
    if level not in {'EASY', 'MEDIUM', 'HARD', 'CHALLENGER'}:
      raise ValueError('Level {} is not valid.'.format(level))
    for _ in range(100):
      nr_spaces = 56
      sudoku = sudoku_data.SudokuData()
      self._solver.solve(sudoku)
      full_sudoku = sudoku_data.SudokuData()
      full_sudoku.copy(sudoku)
      nr_removed = 0
      while nr_removed < nr_spaces:
        row = random.randrange(9)
        col = random.randrange(9)
        if sudoku.get(row, col) != ' ':
          sudoku.set(row, col, ' ')
          nr_removed += 1
      self.make_one_solution(sudoku, full_sudoku)
      clone = sudoku_data.SudokuData()
      clone.copy(sudoku)
      solution = self._solver.solve(clone)
      nr_missing = len(solution)
      curr_level = 'EASY'
      if not self.is_partial_solvable(sudoku) or nr_missing > 51:
        curr_level = 'CHALLENGER'
      elif nr_missing <= 45:
        curr_level = 'EASY'
      elif nr_missing <= 48:
        curr_level = 'MEDIUM'
      else:
        curr_level = 'HARD'
      sudoku_list = self._sudoku_map[curr_level]
      if len(sudoku_list) < 100:
        sudoku_list.append(sudoku)
      sudoku_list = self._sudoku_map[level]
      if sudoku_list:
        sudoku = sudoku_list[-1]
        del sudoku_list[-1]
        break
    return sudoku
