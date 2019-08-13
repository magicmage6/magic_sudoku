"""Sudoku data."""


class SudokuData:
  """Class for sudoku data."""

  def __init__(self):
    self.data = [[' '] * 9 for _ in range(9)]
    self._regions = None

  def from_lines(self, lines):
    """Load data from a list of lines.

    Args:
      lines: A list of lines with numbers or space separated by common. Only the
        first 9 lines will be used.

    Raises:
      RuntimeError: If the lines doesn't have correct format.
    """
    if len(lines) < 9:
      raise RuntimeError('The number of lines is less than 9.')
    for i in range(9):
      self.data[i] = lines[i].split(',')
      if len(self.data[i]) != 9:
        raise RuntimeError('The line does not contain 9 values. {}'.format(
            lines[i]))

  def copy(self, other):
    """Copy another sudoku."""
    for row in range(9):
      for col in range(9):
        self.data[row][col] = other.data[row][col]

  def set(self, row, col, value):
    self.data[row][col] = value

  def get(self, row, col):
    return self.data[row][col]

  def print_data(self):
    for row in range(9):
      print(','.join(self.data[row]))

  def _calculate_regions(self):
    """Calculate all the regions of a sukoku.

    A region is a row, a column, or a box. Each region is a list of all the
    locations (a tuple of row, column) in that region. As the regions are
    independent of the numbers, this only needs to be calculated once.
    """

    # Calculate all the regions, which is either a row, a column, or a box.
    # Regions for all rows.
    self._regions = [[(row, col) for col in range(9)] for row in range(9)]
    # Regions for all columns.
    self._regions.extend([[(row, col) for row in range(9)] for col in range(9)])
    # Regions for all boxes.
    for low in [0, 3, 6]:
      for left in [0, 3, 6]:
        box = []
        for row in range(low, low + 3):
          box.extend([(row, col) for col in range(left, left + 3)])
        self._regions.append(box)

  def is_valid(self):
    """Check if this is valid sudoku.

    A valid sudoku is one that doesn't have conflict at the this time, it
    does not mean it is solvable.

    Returns:
      True if the sudoku is valid.
    """
    # Get all the regions, which is either a row, a column, or a box.
    if self._regions is None:
      self._calculate_regions()
    # Check if it is valid in every region.
    for region in self._regions:
      value_set = set()
      for row, col in region:
        value = self.data[row][col]
        if value == ' ':
          continue
        if len(value) != 1 or ord(value) < ord('1') or ord(value) > ord('9'):
          return False
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
