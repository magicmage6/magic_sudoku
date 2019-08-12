import collections
import copy

# A region is a row, column, or a box where each number 1-9 will appear once and only once.
# A region represent a row.
_ROW_REGION = 0
# A region represent a column.
_COLUMN_REGION = 1
# A region represent a box.
_BOX_REGION = 2

class SudokuSolver:

  def __init__(self, sudoku):
    self._sudoku = sudoku
    self._possible_values = [[{} for i in range(9)] for j in range(9)]
    # A list grouping locations by the number of possible values.
    self._location_groups = [{} for i in range(10)]
    # A dictionary mapping the possible locations of a number in a region.
    self._possible_locations = {}
    # A dictionary of unique locations for a number in a region.
    # The key is a tupe of the region type, region number, the value (number), and the value
    # is the only possible location.
    self._unique_locations = {}

  def _remove_possible_values(self, row, col, value):
    if value in self._possible_values[row][col]:
      orig_len = len(self._possible_values[row][col])
      self._possible_values[row][col].remove(value)
      if (row, col) in self._location_groups[orig_len]:
        self._location_groups[orig_len].remove((row, col))
        self._location_groups[orig_len - 1].add((row, col))
      keys = [(_ROW_REGION, row, value), (_COLUMN_REGION, col, value), (_BOX_REGION, int (row / 3) * 3 + int (col / 3), value)]
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
    keys = [(_ROW_REGION, row, value), (_COLUMN_REGION, col, value), (_BOX_REGION, int (row / 3) * 3 + int (col / 3), value)]
    for key in keys:
      # print('key', key)
      if key in self._possible_locations:
        # print('delete')
        del self._possible_locations[key]
      if key in self._unique_locations:
        # print('delete unique')
        del self._unique_locations[key]


  def _initialize_possible_values(self):
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
    self._possible_locations = {}
    for i in range(9):
      for j in range(9):
        if self._sudoku.get(i, j) == ' ':
          for value in self._possible_values[i][j]:
            key = (_ROW_REGION, i, value)
            self._possible_locations.setdefault(key, set()).add((i, j))
            key = (_COLUMN_REGION, j, value)
            self._possible_locations.setdefault(key, set()).add((i, j))
            key = (_BOX_REGION, int (i / 3) * 3 + int (j / 3), value)
            self._possible_locations.setdefault(key, set()).add((i, j))
    self._unique_locations = {}
    for key, value in self._possible_locations.items():
      if len(value) == 1:
        for c in value:
          self._unique_locations[key] = c

  def _fast_solve(self):
    """Sovling it with fast approaches."""
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
    for row, column, c in solutions:
      self._update_possible_values(row, column, c)
    return solutions
  
  def _recursive_solve(self):
    solutions = []
    for _ in range(81):
      fast_solutions = self._fast_solve()
      # print(fast_solutions)
      if not fast_solutions:
        break
      else:
        solutions.extend(fast_solutions)
    return solutions

  def solve(self, fast_solve = False):
    """Solve a sudoku."""
    self._initialize_possible_values()
    self._initialize_possible_locations()
    if fast_solve:
      return self._fast_solve()
    else:
      return self._recursive_solve()

