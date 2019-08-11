import curses


class Sudoku:

  def __init__(self):
    self.data = [[' ' for x in range(9)] for y in range(9)]
    self.colors = [[1 for x in range(9)] for y in range(9)]
    self.data_file = '/tmp/magic_sudoku.data'

  def set(self, row, col, value, color):
    self.data[row][col] = value
    self.colors[row][col] = color

  def get(self, row, col):
    return self.data[row][col], self.colors[row][col]

  def valid(self, row, col, value):
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

  def save(self):
    with open(self.data_file, 'w') as f:
      for i in range(9):
        f.write(','.join(self.data[i]) + '\n')
      for i in range(9):
        f.write(','.join([str(c) for c in self.colors[i]]) + '\n')
  
  def load(self):
    with open(self.data_file, 'r') as f:
      contents = f.read().split('\n')
      for i in range(9):
        self.data[i] = contents[i].split(',')
        self.colors[i] = [int(c) for c in contents[i + 9].split(',')]


class SudokuUI:

  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.height = 18
    self.width = 36
    self.curr_row = 4
    self.curr_col = 4
    self.curr_color = 1
    self.mouse_x = None
    self.mouse_y = None
    self.sudoku = Sudoku()
    self._setup_colors()

  def _setup_colors(self):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
    self.num_colors = 7

  def _draw_board(self):
    max_y, max_x = self.stdscr.getmaxyx()
    
    if max_y <= 20:
      raise RuntimeError('Window height must be greater than 20.')
    if max_x <= 27:
      raise RuntimeError('Window width must be greater than 27.')
    if self.width >= max_x:
      self.height -= 9
      self.width -= 18
    # Leaving space for title.
    if self.height >= max_y - 2:
      self.height -= 9
      self.width -= 18

    left = int((max_x - self.width) / 2)
    right = left + self.width
    up = int((max_y - self.height) /2 )
    down = up + self.height
    delta_x = self.width / 9
    delta_y = self.height / 9

    if self.mouse_x is not None and self.mouse_y is not None:
      row = int((self.mouse_y - up) / delta_y)
      col = int((self.mouse_x - left) / delta_x)
      self.curr_row = min(8, max(0, row))
      self.curr_col = min(8, max(0, col))
      self.mouse_x = None
      self.mouse_y = None

    title = 'Magic Sudoku'
    self.stdscr.attron(curses.color_pair(self.curr_color))
    self.stdscr.addstr(int(up / 2), int((max_x - len(title)) / 2), title)
    self.stdscr.attroff(curses.color_pair(self.curr_color))

    boards = [['' for x in range(left, right + 1)] for y in range(up, down + 1)]
    for i in range(10):
      for j in range(left, right + 1):
        boards[int(i * delta_y)][j - left] = curses.ACS_HLINE
    
    for i in range(10):
      col = int(left + i * delta_x)
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
    colors = [[inner_color for x in range(left, right + 1)] for y in range(up, down + 1)]
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

    for i in range(9):
      for j in range(9):
        number, color = self.sudoku.get(i,j)
        self.stdscr.attron(curses.color_pair(color))
        self.stdscr.addch(int(up + (i + 0.5) * delta_y), int(left + (j + 0.5) * delta_x), number)
        self.stdscr.attroff(curses.color_pair(color))

    self.stdscr.move(int(up + (self.curr_row + 0.5) * delta_y), int(left + (self.curr_col + 0.5) * delta_x))

  def _process_key(self, key):
    if key == ord('-'):
      if self.height > 18:
        self.height -= 9
        self.width -= 18
    elif key == ord('+'):
      self.height += 9
      self.width += 18
    elif key == curses.KEY_DOWN:
      self.curr_row = min(8, self.curr_row + 1)
    elif key == curses.KEY_UP:
      self.curr_row = max(0, self.curr_row - 1)
    elif key == curses.KEY_RIGHT:
      self.curr_col = min(8, self.curr_col + 1)
    elif key == curses.KEY_LEFT:
      self.curr_col = max(0, self.curr_col - 1)
    elif key == curses.KEY_MOUSE:
      _, self.mouse_x, self.mouse_y, _, _ = curses.getmouse()
    elif key == ord('c'):
      self.curr_color = (self.curr_color + 1) % self.num_colors
    elif key == ord('s'):
      self.sudoku.save()
    elif key == ord('l'):
      self.sudoku.load()
    elif key >= ord('1') and key <= ord('9') or key == ord(' '):
      if self.sudoku.valid(self.curr_row, self.curr_col, chr(key)):
        self.sudoku.set(self.curr_row, self.curr_col, chr(key), self.curr_color)
      else:
        curses.beep()


  def run(self):
    key = 0
    curses.mousemask(1)

    while key != ord('q'):
      self.stdscr.clear()

      self._process_key(key)
      self._draw_board()

      self.stdscr.refresh()

      # Get the input key.
      key = self.stdscr.getch()


def run_sudoku(stdscr):
  SudokuUI(stdscr).run()


def main():
  curses.wrapper(run_sudoku)

if __name__ == "__main__":
  main()
