"""Sudoku UI."""

import curses
import os
import sudoku_data
import sudoku_generator
import sudoku_solver

_MENU = """
q       Quit
m       Show menu
n       New sudoku
Up      Cursor up
Down    Cursor down
Left    Cursor left
Right   Cursor right
1 - 9   Fill in a number
Space   Erase a number
+       Increase size
-       Decrease size
c       Change color
b       Change color back
a       Auto solve
h       Hint
u       Undo changes
r       Redo changes
Mouse   Move cursor
Any     Dismiss menu
"""

_NEW_SUDOKU_MSG = """
A new sudoku?
0       Empty
1       Easy
2       Medium
3       Hard
4       Challenger
Other   Back
"""

_WIN_MSG = """
**********************
*                    *
*  Congratulations!  *
*                    *
**********************
"""

# change type.
_NUMBER_CHANGE = 1
_COLOR_CHANGE = 2
_SUDOKU_CHANGE = 3

# Confirmation type
_NEW_SUDOKU_CONFIRM = 1


class SudokuUI(object):
  """Class for sudoku UI with curses."""

  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.height = 18
    self.width = 36
    self.curr_row = 4
    self.curr_col = 4
    self.curr_color = 1
    self.message = None
    self.confirm = None
    self.mouse_x = None
    self.mouse_y = None
    self.level = 'Easy'
    self.sudoku = sudoku_data.SudokuData()
    self.solver = sudoku_solver.SudokuSolver()
    self.generator = sudoku_generator.SudokuGenerator()
    self._setup_colors()
    self.data_file = '/tmp/magic_sudoku.data'
    self.changes = []
    self.redo_changes = []

  def _setup_colors(self):
    """Setup curses colors."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
    self.num_colors = 7
    self.colors = [[0] * 9 for _ in range(9)]

  def _save(self, file_name):
    """Save sudoku to a file."""
    with open(file_name, 'w') as f:
      for i in range(9):
        f.write(','.join(self.sudoku.data[i]) + '\n')
      for i in range(9):
        f.write(','.join([str(c) for c in self.colors[i]]) + '\n')
      f.write(self.level)

  def _auto_save(self):
    """Automatically save sudoku to data file."""
    if self.data_file is None:
      return
    try:
      self._save(self.data_file)
    except IOError:
      self.message = 'Auto save failed'

  def _load(self):
    """Load sudoku from date file."""
    try:
      with open(self.data_file, 'r') as f:
        contents = f.read().split('\n')
        self.sudoku.from_lines(contents)
        if len(contents) >= 18:
          for i in range(9):
            self.colors[i] = [int(c) for c in contents[i + 9].split(',')]
        if len(contents) > 18:
          level = contents[18]
          if level in {'Easy', 'Medium', 'Hard', 'Challenger'}:
            self.level = contents[18]
    except IOError:
      curses.beep()

  def _draw_board(self):
    """Draw sudoku board."""
    self.stdscr.clear()
    # Check the screen size.
    max_y, max_x = self.stdscr.getmaxyx()
    if max_y <= 20 or max_x <= 27:
      self.stdscr.addstr(0, 0, 'Terminal is too small.')
      return

    # Adjust sudoku board based on the screen size.
    if self.width >= max_x:
      self.height -= 9
      self.width -= 18
    # -4 to Leaving space for title and subtitle.
    if self.height >= max_y - 4:
      self.height -= 9
      self.width -= 18

    # Calculate the boundary of the sudoku board.
    left = int(round(max(0, int((max_x - self.width) / 2))))
    right = int(round(left + self.width))
    up = int(round(max(0, int((max_y - self.height) / 2))))
    down = int(round(up + self.height))
    delta_x = self.width / 9
    delta_y = self.height / 9

    # Move the current position to the mouse click location.
    if self.mouse_x is not None and self.mouse_y is not None:
      row = int((self.mouse_y - up) / delta_y)
      col = int((self.mouse_x - left) / delta_x)
      self.curr_row = min(8, max(0, row))
      self.curr_col = min(8, max(0, col))
      self.mouse_x = None
      self.mouse_y = None

    # Show title.
    title = 'Magic Sudoku ({})'.format(self.level)
    title_y = int(up / 2)
    self.stdscr.attron(curses.color_pair(self.curr_color))
    self.stdscr.addstr(title_y, max(0, int((max_x - len(title)) / 2)), title)
    subtitle = 'Press m for menu'
    self.stdscr.addstr(title_y + 1, max(0, int((max_x - len(subtitle)) / 2)),
                       subtitle)
    self.stdscr.attroff(curses.color_pair(self.curr_color))

    # Draw lines of the board.
    boards = [[''] * (right - left + 1) for _ in range(up, down + 1)]
    # Horizontal lines.
    for i in range(10):
      for j in range(left, right + 1):
        boards[int(round(i * delta_y))][j - left] = curses.ACS_HLINE
    # Vertical lines, and handle corners, edges, and crosses.
    for i in range(10):
      col = int(round(left + i * delta_x))
      for row in range(up, down + 1):
        c = boards[row - up][col - left]
        if c != curses.ACS_HLINE:
          c = curses.ACS_VLINE
        elif row == up and col == left:
          c = curses.ACS_ULCORNER
        elif row == up and col == right:
          c = curses.ACS_URCORNER
        elif row == down and col == left:
          c = curses.ACS_LLCORNER
        elif row == down and col == right:
          c = curses.ACS_LRCORNER
        elif row == up:
          c = curses.ACS_TTEE
        elif row == down:
          c = curses.ACS_BTEE
        elif col == left:
          c = curses.ACS_LTEE
        elif col == right:
          c = curses.ACS_RTEE
        else:
          c = curses.ACS_PLUS
        boards[row - up][col - left] = c

    # Set different color for border lines and inner lines.
    border_color = 0
    inner_color = 7
    colors = [[inner_color] * (right - left + 1) for _ in range(up, down + 1)]
    for i in range(4):
      col = int(left + i * delta_x * 3)
      for row in range(up, down + 1):
        colors[row - up][col - left] = border_color

    for i in range(4):
      row = int(up + i * delta_y * 3)
      for col in range(left, right + 1):
        colors[row - up][col - left] = border_color

    for i in range(up, down + 1):
      for j in range(left, right + 1):
        c = boards[i - up][j - left]
        color = colors[i - up][j - left]
        if c:
          if color != 0:
            self.stdscr.attron(curses.color_pair(color))
          self.stdscr.addch(i, j, c)
          if color != 0:
            self.stdscr.attroff(curses.color_pair(color))

    # Draw numbers of the sudoku.
    for i in range(9):
      for j in range(9):
        number = self.sudoku.get(i, j)
        color = self.colors[i][j]
        if color != 0:
          self.stdscr.attron(curses.color_pair(color))
        self.stdscr.addch(
            int(up + (i + 0.5) * delta_y), int(left + (j + 0.5) * delta_x),
            number)
        if color != 0:
          self.stdscr.attroff(curses.color_pair(color))

    self.stdscr.move(
        int(up + (self.curr_row + 0.5) * delta_y),
        int(left + (self.curr_col + 0.5) * delta_x))

    self.stdscr.refresh()

    # Show messages.
    if self.message:
      message_lines = self.message.strip().split('\n')
      message_width = max([len(m) for m in message_lines]) + 2
      message_height = len(message_lines)
      window_left = int(round((max_x - message_width) / 2))
      window_up = int(round((max_y - message_height) / 2))
      message_window = curses.newwin(message_height, message_width + 1,
                                     window_up, window_left)
      for i in range(message_height):
        line = message_lines[i]
        padded_line = ' {}{}'.format(line,
                                     ' ' * (message_width - len(line) - 1))
        message_window.addstr(i, 0, padded_line, curses.A_REVERSE)
      curses.curs_set(0)
      message_window.refresh()

  def _change_number(self, row, col, new_value):
    """Change a number in a location.

    Args:
      row: The row of the location.
      col: The column of the location.
      new_value: The number to fill in.

    Returns:
      True if the number is changed, false if the change is not valid.
    """
    original_value = self.sudoku.get(row, col)
    if new_value == original_value:
      return False
    if original_value != ' ' and self.colors[row][col] == 0:
      self.message = 'Can not change fixed number'
      return False
    if self.sudoku.is_valid_value(row, col, new_value):
      self.curr_row = row
      self.curr_col = col
      self.sudoku.set(self.curr_row, self.curr_col, new_value)
      self.colors[self.curr_row][self.curr_col] = self.curr_color
      self.changes.append((_NUMBER_CHANGE, (self.curr_row, self.curr_col,
                                            original_value, new_value)))
      self.redo_changes = []
      self._auto_save()
      return True
    else:
      self.message = '{} is not valid here'.format(new_value)
      return False

  def _change_color(self, new_color):
    """Change the current color."""
    original_color = self.curr_color
    new_color = (new_color - 1) % self.num_colors + 1
    self.curr_color = new_color
    self.changes.append((_COLOR_CHANGE, (original_color, new_color)))
    self.redo_changes = []
    self._auto_save()

  def _change_sudoku(self, new_sudoku):
    """Change the current sudoku."""
    original_sudoku = self.sudoku
    original_colors = self.colors
    original_curr_color = self.curr_color
    self.colors = [[0] * 9 for _ in range(9)]
    self.sudoku = new_sudoku
    self.changes.append(
        (_SUDOKU_CHANGE, ((original_sudoku, original_colors,
                           original_curr_color), (self.sudoku, self.colors,
                                                  self.curr_color))))
    self.redo_changes = []
    self._auto_save()

  def _process_key(self, key):
    """Process the key and mouse events."""
    if self.message:
      if self.message == _WIN_MSG:
        self.message = _NEW_SUDOKU_MSG
        self.confirm = _NEW_SUDOKU_CONFIRM
        return
      self.message = None
      curses.curs_set(1)
      if self.confirm is not None:
        if self.confirm == _NEW_SUDOKU_CONFIRM:
          self.confirm = None
          if key == ord('0'):
            self.level = 'Easy'
          elif key == ord('1'):
            self.level = 'Easy'
          elif key == ord('2'):
            self.level = 'Medium'
          elif key == ord('3'):
            self.level = 'Hard'
          elif key == ord('4'):
            self.level = 'Challenger'
          else:
            return
          if key == ord('0'):
            self._change_sudoku(sudoku_data.SudokuData())
          else:
            self._change_sudoku(self.generator.get_sudoku(level=self.level))
    elif key == ord('-') or key == ord('_'):
      # Reduce size of the sudoku board.
      if self.height > 18:
        self.height -= 9
        self.width -= 18
    elif key == ord('+') or key == ord('='):
      # Increase size of the sudoku board.
      self.height += 9
      self.width += 18
    elif key == curses.KEY_DOWN:
      # Move cursor down.
      self.curr_row = min(8, self.curr_row + 1)
    elif key == curses.KEY_UP:
      # Move cursor up.
      self.curr_row = max(0, self.curr_row - 1)
    elif key == curses.KEY_RIGHT:
      # Move cursor right.
      self.curr_col = min(8, self.curr_col + 1)
    elif key == curses.KEY_LEFT:
      # Move cursor left.
      self.curr_col = max(0, self.curr_col - 1)
    elif key == curses.KEY_MOUSE:
      # Move cursor to the location of the mouse.
      try:
        _, self.mouse_x, self.mouse_y, _, _ = curses.getmouse()
      except Exception:
        curses.beep()
    elif key == ord('a') or key == ord('A'):
      # Automatically solve the sudoku.
      clone = sudoku_data.SudokuData()
      clone.copy(self.sudoku)
      solution = self.solver.solve(clone)
      if solution:
        self._change_color(self.curr_color + 1)
        for row, col, value in solution:
          self._change_number(row, col, value)
      else:
        self.message = 'Not solvable'
    elif key == ord('h') or key == ord('H'):
      # Give hint of the next move.
      clone = sudoku_data.SudokuData()
      clone.copy(self.sudoku)
      solution = self.solver.solve(clone, partial=True)
      if not solution:
        solution = self.solver.solve(clone)
      if solution:
        for row, col, value in solution:
          self._change_number(row, col, value)
          break
      else:
        self.message = 'Not solvable'
    elif key == ord('n') or key == ord('N'):
      # Generates a new sudoku.
      self.message = _NEW_SUDOKU_MSG
      self.confirm = _NEW_SUDOKU_CONFIRM
    elif key == ord('c') or key == ord('C'):
      # Change current color use for new numbers fill in the board.
      self._change_color(self.curr_color + 1)
    elif key == ord('b') or key == ord('B'):
      # Change current color to previous one.
      self._change_color(self.curr_color - 1)
    elif key == ord('m') or key == ord('M'):
      # Show or hide menu.
      self.message = _MENU
    elif key == ord('u') or key == ord('U'):
      # Undo changes.
      if self.changes:
        change_type, content = self.changes[-1]
        if change_type == _NUMBER_CHANGE:
          row, col, original_value, _ = content
          self.sudoku.set(row, col, original_value)
          self.curr_row = row
          self.curr_col = col
        elif change_type == _COLOR_CHANGE:
          original_color, _ = content
          self.curr_color = original_color
        else:
          (original_sudoku, original_colors, original_curr_color), _ = content
          self.sudoku = original_sudoku
          self.colors = original_colors
          self.curr_color = original_curr_color
        del self.changes[-1]
        self.redo_changes.append((change_type, content))
        self._auto_save()
      else:
        self.message = 'Nothing to undo'
    elif key == ord('r') or key == ord('R'):
      # Redo changes.
      if self.redo_changes:
        change_type, content = self.redo_changes[-1]
        if change_type == _NUMBER_CHANGE:
          row, col, _, new_value = content
          self.sudoku.set(row, col, new_value)
          self.curr_row = row
          self.curr_col = col
        elif change_type == _COLOR_CHANGE:
          _, new_color = content
          self.curr_color = new_color
        else:
          _, (new_sudoku, new_colors, new_curr_color) = content
          self.sudoku = new_sudoku
          self.colors = new_colors
          self.curr_color = new_curr_color
        del self.redo_changes[-1]
        self.changes.append((change_type, content))
        self._auto_save()
      else:
        self.message = 'Nothing to redo'
    elif key >= ord('1') and key <= ord('9') or key == ord(' '):
      # Fill in a new number in the board. Space erases existing number.
      if self._change_number(self.curr_row, self.curr_col,
                             chr(key)) and self.sudoku.is_solved():
        self.message = _WIN_MSG

  def _initialize_sudoku(self):
    """Try to load sudo from auto save file.

    If the auto save file does not exist, generates a random sudoku with Easy
    level.
    """
    self.data_file = '/tmp/.magic_sudoku_autosave.data'
    if os.path.exists(self.data_file):
      self._load()
    else:
      self.data_file = '.magic_sudoku_autosave.data'
      if os.path.exists(self.data_file):
        self._load()
      else:
        self.sudoku = self.generator.get_sudoku()
        self.data_file = '/tmp/.magic_sudoku_autosave.data'
        try:
          self._save(self.data_file)
        except IOError:
          self.data_file = '.magic_sudoku_autosave.data'
          try:
            self._save(self.data_file)
          except IOError:
            self.data_file = None
            self.message = 'Failed to save'

  def run(self):
    """Run sudoku UI."""
    key = 0
    # Enable mouse click.
    curses.mousemask(1)
    self._initialize_sudoku()

    while key != ord('q'):
      self._process_key(key)
      self._draw_board()
      # Generates a sudoku every turn in the background and cache them to make
      # it faster when a new sudoku is really needed.
      self.generator.generate_sudoku()
      # Get the input key.
      key = self.stdscr.getch()


def _run_sudoku(stdscr):
  SudokuUI(stdscr).run()


def start_ui():
  curses.wrapper(_run_sudoku)
