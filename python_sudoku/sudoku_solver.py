"""Sudoku Solver."""

import copy
import random

# A region is a row, column, or a box where each number 1-9 will appear once and
# only once.
# A region represent a row.
_ROW_REGION = 0
# A region represent a column.
_COLUMN_REGION = 1
# A region represent a box.
_BOX_REGION = 2


class SudokuSolver:
  """Class for sudoku solver."""

  def __init__(self, sudoku):
    self._sudoku = sudoku
    self._possible_values = [[{}] * 9 for _ in range(9)]
    # A list grouping locations by the number of possible values.
    self._location_groups = [{}] * 10
    # A dictionary mapping the possible locations of a number in a region.
    self._possible_locations = {}
    # A dictionary of unique locations for a number in a region.
    # The key is a tupe of the region type, region number, the value (number),
    # and the value is the only possible location.
    self._unique_locations = {}

  def _remove_possible_values(self, row, col, value):
    """Removes one possible number at a particular location.

    Args:
      row: The row of the location.
      col: The col of the location.
      value: A character between '1' and '9' to remove as a possible value.
    """
    if value in self._possible_values[row][col]:
      orig_len = len(self._possible_values[row][col])
      self._possible_values[row][col].remove(value)
      if (row, col) in self._location_groups[orig_len]:
        self._location_groups[orig_len].remove((row, col))
        self._location_groups[orig_len - 1].add((row, col))
      keys = [(_ROW_REGION, row, value), (_COLUMN_REGION, col, value),
              (_BOX_REGION, int(row / 3) * 3 + int(col / 3), value)]
      for key in keys:
        # print('removing key ', key)
        if key in self._possible_locations:
          locations = self._possible_locations[key]
          if (row, col) in locations:
            locations.remove((row, col))
            if len(locations) == 1:
              for l in locations:
                self._unique_locations[key] = l

  def _update_possible_values(self, row, col, value):
    """Updates possible values when adding a number at a particular location.

    Args:
      row: The row of the location.
      col: The col of the location.
      value: A character between '1' and '9' to be added at the location.
    """
    possible_values = self._possible_values[row][col]
    group = self._location_groups[len(possible_values)]
    if (row, col) in group:
      group.remove((row, col))
    for c in copy.copy(possible_values):
      if c != value:
        self._remove_possible_values(row, col, c)
    self._possible_values[row][col] = {}
    for i in range(9):
      if i != row and self._sudoku.get(i, col) == ' ':
        self._remove_possible_values(i, col, value)
    for i in range(9):
      if i != col and self._sudoku.get(row, i) == ' ':
        self._remove_possible_values(row, i, value)
    low = int(row / 3) * 3
    left = int(col / 3) * 3
    for i in range(low, low + 3):
      for j in range(left, left + 3):
        if (i != row or j != col) and self._sudoku.get(i, j) == ' ':
          self._remove_possible_values(i, j, value)
    keys = [(_ROW_REGION, row, value), (_COLUMN_REGION, col, value),
            (_BOX_REGION, int(row / 3) * 3 + int(col / 3), value)]
    for key in keys:
      # print('key', key)
      if key in self._possible_locations:
        # print('delete')
        del self._possible_locations[key]
      if key in self._unique_locations:
        # print('delete unique')
        del self._unique_locations[key]

  def _initialize_possible_values(self):
    """Initialize possible values at every location."""
    self._possible_values = [[{}] * 9 for _ in range(9)]
    for i in range(9):
      for j in range(9):
        c = self._sudoku.get(i, j)
        if c == ' ':
          self._possible_values[i][j] = {str(i) for i in range(1, 10)}
        else:
          self._possible_values[i][j] = {c}
    for i in range(9):
      for j in range(9):
        c = self._sudoku.get(i, j)
        if c != ' ':
          self._update_possible_values(i, j, c)
    for i in range(10):
      self._location_groups[i] = set()
    for i in range(9):
      for j in range(9):
        if self._sudoku.get(i, j) == ' ':
          self._location_groups[len(self._possible_values[i][j])].add((i, j))

  def _initialize_possible_locations(self):
    """Initialize the possible locations of a number in each region.

    A region is a row, column, or a box where each number 1-9 will appear once
    and only once.
    """
    self._possible_locations = {}
    for i in range(9):
      for j in range(9):
        if self._sudoku.get(i, j) == ' ':
          for value in self._possible_values[i][j]:
            key = (_ROW_REGION, i, value)
            self._possible_locations.setdefault(key, set()).add((i, j))
            key = (_COLUMN_REGION, j, value)
            self._possible_locations.setdefault(key, set()).add((i, j))
            key = (_BOX_REGION, int(i / 3) * 3 + int(j / 3), value)
            self._possible_locations.setdefault(key, set()).add((i, j))
    self._unique_locations = {}
    for key, value in self._possible_locations.items():
      if len(value) == 1:
        for c in value:
          self._unique_locations[key] = c

  def _fast_solve(self):
    """Solving it with fast approaches.

    Returns:
      A list of solutions with each solution as a tuple of row, column and
        value, where value is a character between '1' and '9'.
    """
    # If some location can't have any possible values, there is not solution.
    if self._location_groups[0]:
      return None
    solutions = []
    solution_set = set()
    # for i in range(9):
    # for j in range(9):
    # print(i, j, self._possible_values[i][j])
    # Fill in the locations where only one value is possible.
    unique_group = self._location_groups[1]
    if unique_group:
      for i, j in unique_group:
        for c in self._possible_values[i][j]:
          # print('solutions append ', i, j, c)
          move = (i, j, c)
          if move not in solution_set:
            solution_set.add(move)
            solutions.append(move)
            self._sudoku.set(i, j, c)
          break
    # for key, value in self._possible_locations.items():
    # print(key, value)
    # for key, value in self._unique_locations.items():
    # print(key, value)

    # Fill in the numbers in a region where only one location is possible.
    for key, value in self._unique_locations.items():
      _, _, c = key
      row, col = value
      move = (row, col, c)
      if move not in solutions:
        # print('solutions append row col c ', row, col, c)
        solution_set.add(move)
        solutions.append(move)
        self._sudoku.set(row, col, c)

    # Check if the sudoku is still valid after all the above changes.
    if not self._sudoku.is_valid():
      # print('invalid solutons ', solutions)
      # print('before invert')
      # self._sudoku.print()
      # Revert the changes.
      for row, col, value in solutions:
        # print('revertering row ', row, ' col ', col)
        self._sudoku.set(row, col, ' ')
      # print('after invert')
      # self._sudoku.print()
      return None
    for row, col, c in solutions:
      self._update_possible_values(row, col, c)
    return solutions

  def _recursive_solve(self):
    solutions = []
    for _ in range(81):
      fast_solutions = self._fast_solve()
      # print('fast solutions', fast_solutions)
      if fast_solutions is None:
        # print('here invert ', solutions)
        for row, col, _ in solutions:
          self._sudoku.set(row, col, ' ')
        # print('after invert ')
        # self._sudoku.print()
        return None
      elif not fast_solutions:
        break
      else:
        solutions.extend(fast_solutions)

    # print('fast solutios ', solutions)

    # Try it from the locatin where has the least possible values.
    for i in range(10):
      group = self._location_groups[i]
      if not group:
        continue
      for row, col in group:
        # This is the location with least possible values, try it here.
        possible_values = list(self._possible_values[row][col])
        randomized_values = []
        nr_values = len(possible_values)
        for i in range(nr_values):
          upper = nr_values - i
          index = 0
          if upper > 1:
            index = random.randrange(upper)
          randomized_values.append(possible_values[index])
          if index != upper - 1:
            possible_values[index] = possible_values[upper - 1]
        try_solutions = None
        # Try for every possible values.
        # print('possible values ', possible_values)
        for value in randomized_values:
          # print('try ', row, col, value)
          self._sudoku.set(row, col, value)
          self._update_possible_values(row, col, value)
          try_solutions = self._recursive_solve()
          if try_solutions is None:
            # Fail to get valid solution, rever the try.
            # print('not valid ', row, col, value)
            self._sudoku.set(row, col, ' ')
            # self._sudoku.print()
            self._initialize_possible_values()
            self._initialize_possible_locations()
          else:
            # Get a valid solution.
            solutions.append((row, col, value))
            solutions.extend(try_solutions)
            break
        if try_solutions is None:
          # Can't find valid solution. Revert fast solutions.
          for row, col, _ in solutions:
            self._sudoku.set(row, col, ' ')
            self._update_possible_values(row, col, value)
            self._initialize_possible_locations()
          return None
        break
      break
    return solutions

  def solve(self, fast_solve=False):
    """Solves a sudoku.

    Args:
      fast_solve: If true, use fast solver, otherwise use full solver.

    Returns:
      A list of solutions with each solution as a tuple of row, column and
        value, where value is a character between '1' and '9'.
    """
    self._initialize_possible_values()
    self._initialize_possible_locations()
    if fast_solve:
      return self._fast_solve()
    else:
      return self._recursive_solve()
