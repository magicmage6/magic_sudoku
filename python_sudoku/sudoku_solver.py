"""Sudoku Solver."""

import copy
import random
import sudoku_data

# A region is a row, column, or a box where each number 1-9 will appear once and
# only once.
# A region represent a row.
_ROW_REGION = 0
# A region represent a column.
_COLUMN_REGION = 1
# A region represent a box.
_BOX_REGION = 2


def _get_randomized_list(data):
  """Returns a randomized list."""
  randomized_data = list(data)
  nr_values = len(randomized_data)
  for i in range(nr_values):
    upper = nr_values - i
    # Randomly choosing an index between 0 and upper.
    index = random.randrange(upper)
    if index != upper - 1:
      # Swap index and the last element.
      tmp = randomized_data[index]
      randomized_data[index] = randomized_data[upper - 1]
      randomized_data[upper - 1] = tmp
  return randomized_data


class SudokuSolver:
  """Class for sudoku solver."""

  def __init__(self):
    self._sudoku = sudoku_data.SudokuData()
    self._possible_values = [[{}] * 9 for _ in range(9)]
    # A list grouping locations by the number of possible values.
    self._location_groups = [{}] * 10
    # A dictionary mapping the possible locations of a number in a region.
    self._possible_locations = {}
    # A dictionary of unique locations for a number in a region.
    # The key is a tupe of the region type, region number, the value (number),
    # and the value is the only possible location.
    self._unique_locations = {}

  def _get_region_keys(self, row, col, value):
    """Gets the key for the possible location dictionary that a particular location and value impacts.

    This function is used to help update the possible locations when a new
    number is filled in.
    """
    return [(_ROW_REGION, row, value), (_COLUMN_REGION, col, value),
            (_BOX_REGION, int(row / 3) * 3 + int(col / 3), value)]

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
      # Update the dictionary grouping the location by number of possible values.
      if (row, col) in self._location_groups[orig_len]:
        self._location_groups[orig_len].remove((row, col))
        self._location_groups[orig_len - 1].add((row, col))
      # Update the possible locations for the regions this location impacts.
      for key in self._get_region_keys(row, col, value):
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
    # Remove possible locations as this location is filled in.
    for key in self._get_region_keys(row, col, value):
      if key in self._possible_locations:
        del self._possible_locations[key]
      if key in self._unique_locations:
        del self._unique_locations[key]

  def _initialize_possible_values(self):
    """Initializes possible values at every location."""
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
    """Initializes the possible locations of a number in each region.

    A region is a row, column, or a box where each number 1-9 will appear once
    and only once.
    """
    self._possible_locations = {}
    for row in range(9):
      for col in range(9):
        if self._sudoku.get(row, col) == ' ':
          for value in self._possible_values[row][col]:
            for key in self._get_region_keys(row, col, value):
              self._possible_locations.setdefault(key, set()).add((row, col))
    self._unique_locations = {}
    for key, possible_locations in self._possible_locations.items():
      if len(possible_locations) == 1:
        for location in possible_locations:
          self._unique_locations[key] = location

  def _initialize_data(self):
    """Initializes possible values and possible locations."""
    self._initialize_possible_values()
    self._initialize_possible_locations()

  def _partial_solve(self):
    """Solves a sudoku with approaches similar to human strategies.

    This function mimics the common strategies that human uses to solve sudoku
    without guessing any numbers. It can solve many easy sudokus, but may not
    be able to solve difficult sudokus. Can be used for giving hints of
    solution.

    Returns:
      A solution as a list of moves with each move as a tuple of row, column and
        value, where value is a character between '1' and '9'. Returns None if
        the sudoku becomes invalid after partial solve.
    """
    # If some location can't have any possible values, there is no solution.
    if self._location_groups[0]:
      return None
    solution = []
    move_set = set()
    # Fill in numbers in the location where only one value is possible.
    unique_group = self._location_groups[1]
    conflict_found = False
    if unique_group:
      for row, col in unique_group:
        for value in self._possible_values[row][col]:
          move = (row, col, value)
          if move not in move_set:
            if self._sudoku.get(row, col) == ' ':
              move_set.add(move)
              solution.append(move)
              self._sudoku.set(row, col, value)
            else:
              conflict_found = True
              break
          break

    # Fill in the numbers in a region where only one location is possible.
    for (_, _, value), (row, col) in self._unique_locations.items():
      move = (row, col, value)
      if move not in move_set:
        if self._sudoku.get(row, col) == ' ':
          move_set.add(move)
          solution.append(move)
          self._sudoku.set(row, col, value)
        else:
          conflict_found = True
          break

    # Check if the sudoku is still valid after all the above changes.
    if conflict_found or not self._sudoku.is_valid():
      # Revert the changes.
      for row, col, value in solution:
        self._sudoku.set(row, col, ' ')
      return None
    for row, col, value in solution:
      self._update_possible_values(row, col, value)
    return solution

  def _fast_solve(self):
    """Solves a sudoku combining human strategies and guessing numbers.

    This function combines the common approaches that human uses with number
    guessing when those approaches are not able to solve the problems. It can
    solve any solvable sudokus.

    Returns:
      A solution as a list of moves with each move as a tuple of row, column and
        value, where value is a character between '1' and '9'. Returns None if
        the sudoku is not solvable.
    """
    solution = []
    # Apply human strategies.
    for _ in range(81):
      partial_solution = self._partial_solve()
      if partial_solution is None:
        for row, col, _ in solution:
          self._sudoku.set(row, col, ' ')
        return None
      elif not partial_solution:
        break
      else:
        solution.extend(partial_solution)

    # Try it from the location where has the least number of possible values.
    for i in range(10):
      group = self._location_groups[i]
      if not group:
        continue
      for row, col in group:
        # This is the location with the least number of possible values, try it
        # here.
        possible_values = _get_randomized_list(self._possible_values[row][col])
        try_solution = None
        # Try for every possible values.
        for value in possible_values:
          self._sudoku.set(row, col, value)
          self._update_possible_values(row, col, value)
          try_solution = self._fast_solve()
          if try_solution is None:
            # Fail to get valid solution, revert the try.
            self._sudoku.set(row, col, ' ')
            # We can incrementally update, but just reinitialize it seems to be fast enough.
            self._initialize_data()
          else:
            # Get a valid solution.
            solution.append((row, col, value))
            solution.extend(try_solution)
            break
        if try_solution is None:
          # Can't find valid solution. Revert pervious moves.
          for row, col, _ in solution:
            self._sudoku.set(row, col, ' ')
          # We can incrementally update, but just reinitialize it seems to be fast enough.
          self._initialize_data()
          return None
        break
      break
    return solution

  def _simple_solve(self):
    """Solves a sudoku with simple recursive algorithm.

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

  def solve(self, sudoku, partial=False, simple=False):
    """Solves a sudoku.

    Args:
      sudoku: A sudoku to solve. An object of sudoku_data.SudokuData.
      simple: If true, use simple solver, otherwise use other solvers.
      partial: If true, use partial solver, otherwise use fast solver.

    Returns:
      A list of solutions with each solution as a tuple of row, column and
        value, where value is a character between '1' and '9'. Returns None
        if the sudoku is not solvable.
    """
    self._sudoku = sudoku
    if simple:
      return self._simple_solve()
    self._initialize_data()
    if partial:
      return self._partial_solve()
    return self._fast_solve()
