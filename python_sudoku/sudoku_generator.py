"""Sudoku generator."""

import random
import sudoku_data
import sudoku_solver


class SudokuGenerator(object):
  """Class for sudoku generator."""

  def __init__(self):
    self._level = 0
    self._solver = sudoku_solver.SudokuSolver()
    self._max_solver = sudoku_solver.SudokuSolver(randomize_type='max')
    self._min_solver = sudoku_solver.SudokuSolver(randomize_type='min')
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
      start_row = random.randrange(9)
      start_col = random.randrange(9)
      for i in range(9):
        for j in range(9):
          row = int((start_row + i) % 9)
          col = int((start_col + j) % 9)
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

  def get_sudoku_level(self, sudoku):
    """Gets the level of the generated sudoku."""
    nr_missing = 0
    for row in range(9):
      for col in range(9):
        if sudoku.get(row, col) == ' ':
          nr_missing += 1
    if not self.is_partial_solvable(sudoku) or nr_missing > 52:
      return 'CHALLENGER'
    elif nr_missing <= 46:
      return 'EASY'
    elif nr_missing <= 49:
      return 'MEDIUM'
    else:
      return 'HARD'

  def generate_sudoku(self):
    """Generates a new sudoku and add it to the correct level."""
    min_nr_sudoku = min([len(sudoku) for sudoku in self._sudoku_map.values()])
    # We already have enough sudoku in the cache.
    if min_nr_sudoku > 10:
      return
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
    curr_level = self.get_sudoku_level(sudoku)
    sudoku_list = self._sudoku_map[curr_level]
    if len(sudoku_list) < 100:
      sudoku_list.append(sudoku)

  def _get_sudoku_with_level(self, level):
    sudoku_list = self._sudoku_map[level]
    if not sudoku_list:
      return None
    sudoku = sudoku_list[-1]
    del sudoku_list[-1]
    return sudoku

  def get_sudoku(self, level='EASY'):
    """Generates a random sudoku problem.

    Returns:
      A random generated sudoku problem.
    """
    level = level.upper()
    if level not in {'EASY', 'MEDIUM', 'HARD', 'CHALLENGER'}:
      raise ValueError('Level {} is not valid.'.format(level))
    # Always generates two sudokus for reserves.
    for _ in range(2):
      self.generate_sudoku()
    sudoku = None
    for _ in range(100):
      self.generate_sudoku()
      sudoku = self._get_sudoku_with_level(level)
      if sudoku:
        break
    if not sudoku:
      # If can't get a sudoku with the correct level, just return
      # a sudoku with any level.
      for curr_level, sudoku_list in self._sudoku_map.items():
        if sudoku_list:
          sudoku = self._get_sudoku_with_level(curr_level)
          break
    return sudoku
