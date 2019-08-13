"""Sudoku data."""


class SudokuData:
  """Class for sudoku data."""

  def __init__(self):
    self.data = [[' '] * 9 for _ in range(9)]

  def from_lines(self, lines):
    """Load data from a list of lines.

    Args:
      lines: A list of lines with numbers or space separated by common. Only the
        first 9 lines will be used.

    Raises:
      If the lines doesn't have correct format.
    """
    if len(lines) < 9:
      raise RuntimeError('The number of lines is less than 9.')
    for i in range(9):
      self.data[i] = lines[i].split(',')
      if len(self.data[i]) != 9:
        raise RuntimeError('The line does not contain 9 values. {}'.format(
            lines[i]))

  def set(self, row, col, value):
    self.data[row][col] = value

  def get(self, row, col):
    return self.data[row][col]

  def print(self):
    for row in range(9):
      print(','.join(self.data[row]))

  def is_valid(self):
    """Check if this is valid sudoku.

    A valid sudoku is one that doesn't have conflict at the this time, it
    does not mean it is solvable.

    Returns:
      True if the sudoku is valid.
    """
    # Check if every row is valid.
    for row in range(9):
      value_set = set()
      for col in range(9):
        value = self.data[row][col]
        if value == ' ':
          continue
        if value in value_set:
          return False
        value_set.add(value)
    # Check if every column is valid.
    for col in range(9):
      value_set = set()
      for row in range(9):
        value = self.data[row][col]
        if value == ' ':
          continue
        if value in value_set:
          return False
        value_set.add(value)
    # Check if every box is valid.
    for low in [0, 3, 6]:
      for left in [0, 3, 6]:
        value_set = set()
        for row in range(low, low + 3):
          for col in range(left, left + 3):
            value = self.data[row][col]
            if value == ' ':
              continue
            if value in value_set:
              return False
            value_set.add(value)
    return True

  def is_valid_value(self, row, col, value):
    """Check if a value is valid in a particular location.

    Args:
      row: Row of the location.
      col: Column of the location.
      value: The value to check.

    Returns:
      True if the value is valid in the location.
    """
    if value == ' ':
      return True
    for i in range(9):
      if i != row:
        if self.data[i][col] == value:
          return False
    for i in range(9):
      if i != col:
        if self.data[row][i] == value:
          return False
    low = int(row / 3) * 3
    left = int(col / 3) * 3
    for i in range(low, low + 3):
      for j in range(left, left + 3):
        if i != row and j != col:
          if self.data[i][j] == value:
            return False
    return True
