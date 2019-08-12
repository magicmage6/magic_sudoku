
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
    # A set of unique locations for a number in a region.
    self._unique_locations = {}

  def _remove_possible_values(self, row, col, value):
    if value in self._possible_values[row][col]:
      orig_len = len(self._possible_values[row][col])
      self._possible_values[row][col].remove(value)
      if (row, col) in self._location_groups[orig_len]:
        self._location_groups[orig_len].remove((row, col))
        self._location_groups[orig_len - 1].add((row, col))

  def _update_possible_values(self, row, col, value):
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
    solutions = []
    # for i in range(9):
      # for j in range(9):
        # print(i, j, self._possible_values[i][j])
    unique_group = self._location_groups[1]
    if unique_group:
      for i, j in unique_group:
        for c in self._possible_values[i][j]:
          # print('solutions append ', i, j, c)
          solutions.append((i, j, c))
          self._sudoku.set(i, j, c)
          break
    # for key, value in self._possible_locations.items():
      # print(key, value)
    # for key, value in self._unique_locations.items():
      # print(key, value)
    
    unique_locations_solutions = set()
    for key, value in self._unique_locations.items():
      _, _, c = key
      row, col = value
      if (row, col, c) not in unique_locations_solutions:
        # print('solutions append row col c ', row, col, c)
        unique_locations_solutions.add((row, col, c))
        solutions.append((row, col, c))
      self._sudoku.set(row, col, c)
    for row, column, c in solutions:
      self._update_possible_values(row, column, c)
    return solutions
  
  def _recursive_solve(self):
    return self._fast_solve()

  def solve(self, fast_solve = False):
    """Solve a sudoku."""
    self._initialize_possible_values()
    self._initialize_possible_locations()
    if fast_solve:
      return self._fast_solve()
    else:
      return self._recursive_solve()

