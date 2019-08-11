class SudokuData:

  def __init__(self):
    self.data = [[' ' for x in range(9)] for y in range(9)]

  def set(self, row, col, value):
    self.data[row][col] = value

  def get(self, row, col):
    return self.data[row][col]

  def valid(self, row, col, value):
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

