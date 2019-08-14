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
      if key in self._possible_locations:
        del self._possible_locations[key]
      if key in self._unique_locations:
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
    """Solving a sudoku with fast approaches.

    This function mimic the common strategies that human uses to solve sudoku
    without guessing any numbers. It can solve many easy problems, but may not
    be able to solve difficult problems.

    Returns:
      A solution as a list of moves with each move as a tuple of row, column and
        value, where value is a character between '1' and '9'.
    """
    # If some location can't have any possible values, there is not solution.
    if self._location_groups[0]:
      return None
    solutions = []
    solution_set = set()
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

    # Fill in the numbers in a region where only one location is possible.
    for key, value in self._unique_locations.items():
      _, _, c = key
      row, col = value
      move = (row, col, c)
      if move not in solutions:
        solution_set.add(move)
        solutions.append(move)
        self._sudoku.set(row, col, c)

    # Check if the sudoku is still valid after all the above changes.
    if not self._sudoku.is_valid():
      # Revert the changes.
      for row, col, value in solutions:
        self._sudoku.set(row, col, ' ')
      return None
    for row, col, c in solutions:
      self._update_possible_values(row, col, c)
    return solutions

  def _full_solve(self):
    """Solving a sudoku combining fast approaches and guessing numbers.

    This function combines the common approaches that human uses with number
    guessing when those approaches are not able to solve the problems.

    Returns:
      A solution as a list of moves with each move as a tuple of row, column and
        value, where value is a character between '1' and '9'.
    """
    solutions = []
    # Apply fast approaches.
    for _ in range(81):
      fast_solutions = self._fast_solve()
      if fast_solutions is None:
        for row, col, _ in solutions:
          self._sudoku.set(row, col, ' ')
        return None
      elif not fast_solutions:
        break
      else:
        solutions.extend(fast_solutions)

    # Try it from the location where has the least number of possible values.
    for i in range(10):
      group = self._location_groups[i]
      if not group:
        continue
      for row, col in group:
        # This is the location with the least number of possible values, try it
        # here.
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
        for value in randomized_values:
          self._sudoku.set(row, col, value)
          self._update_possible_values(row, col, value)
          try_solutions = self._full_solve()
          if try_solutions is None:
            # Fail to get valid solution, rever the try.
            self._sudoku.set(row, col, ' ')
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

  def _simple_solve(self):
    """Solve a sudoku with simple recursive algorithm.

    This function uses simple recursive algorithm without run time optimization.
    but it can still solve a sudoku within a second. It can be used for solving
    a single sudoku, but will be too slow for solving a lot of sudokus or
    generating a lot of random sudoku problems.
    """
    if not self._sudoku.is_valid():
      return None
    solution = []
    for row in range(9):
      for col in range(9):
        if self._sudoku.get(row, col) == ' ':
          possible_values = []
          for i in range(9):
            value = chr(i + ord('1'))
            if self._sudoku.is_valid_value(row, col, value):
              possible_values.append(value)
          if not possible_values:
            return None
          try_solution = None
          for value in possible_values:
            self._sudoku.set(row, col, value)
            try_solution = self._simple_solve()
            if try_solution is None:
              self._sudoku.set(row, col, ' ')
            else:
              solution.append((row, col, value))
              solution.extend(try_solution)
              break
          if try_solution is None:
            return None
          return solution
    return solution

  def solve(self, fast=False, simple=False):
    """Solves a sudoku.

    Args:
      simple: If true, use simple solver, otherwise use other solvers.
      fast: If true, use fast solver, otherwise use full solver.

    Returns:
      A list of solutions with each solution as a tuple of row, column and
        value, where value is a character between '1' and '9'.
    """
    if simple:
      return self._simple_solve()
    self._initialize_possible_values()
    self._initialize_possible_locations()
    if fast:
      return self._fast_solve()
    return self._full_solve()
