import curses


class Sudoku:

  def __init__(self):
    self.data = [[' ' for x in range(9)] for y in range(9)]
    self.colors = [[1 for x in range(9)] for y in range(9)]

  def set(self, row, col, value, color):
    self.data[col][row] = value
    self.colors[col][row] = color

  def get(self, row, col):
    return self.data[col][row], self.colors[col][row]

  def valid(self, row, col, value):
    if value == ' ':
      return True
    for i in range(9):
      if i != row:
        if self.data[col][i] == value:
          return False
    for i in range(9):
      if i != col:
        if self.data[i][row] == value:
          return False
    low = int(row / 3) * 3
    left = int(col / 3) * 3
    for i in range(low, low + 3):
      for j in range(left, left + 3):
        if i != row and j != col:
          if self.data[j][i] == value:
            return False
    return True


class SudokuUI:

  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.height = 18
    self.width = 36
    self.curr_row = 4
    self.curr_col = 4
    self.curr_color = 1
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

    title = 'Magic Sudoku'
    self.stdscr.attron(curses.color_pair(self.curr_color))
    self.stdscr.addstr(int(up / 2), int((max_x - len(title)) / 2), title)
    self.stdscr.attroff(curses.color_pair(self.curr_color))

    for i in range(10):
      self.stdscr.hline(int(up + i * delta_y), left, curses.ACS_HLINE, self.width)
    
    for i in range(10):
      self.stdscr.vline(up, int(round(left + i * delta_x)), curses.ACS_VLINE, self.height)
    
    for i in range(10):
      self.stdscr.addch(up, int(left + i * delta_x), curses.ACS_TTEE)
      self.stdscr.addch(down, int(left + i * delta_x), curses.ACS_BTEE)

    self.stdscr.addch(up, left, curses.ACS_ULCORNER)
    self.stdscr.addch(up, right, curses.ACS_URCORNER)
    self.stdscr.addch(down, left, curses.ACS_LLCORNER)
    self.stdscr.addch(down, right, curses.ACS_LRCORNER)

    for i in range(9):
      for j in range(9):
        number, color = self.sudoku.get(i,j)
        self.stdscr.attron(curses.color_pair(color))
        self.stdscr.addch(int(up + i * delta_y) + 1, int(left + j * delta_x) + 2, number)
        self.stdscr.attroff(curses.color_pair(color))

    self.stdscr.move(int(up + self.curr_row * delta_y) + 1, int(left + self.curr_col * delta_x) + 2)

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
    elif key == ord('c'):
      self.curr_color = (self.curr_color + 1) % self.num_colors
    elif key >= ord('1') and key <= ord('9') or key == ord(' '):
      if self.sudoku.valid(self.curr_row, self.curr_col, chr(key)):
        self.sudoku.set(self.curr_row, self.curr_col, chr(key), self.curr_color)
      else:
        curses.beep()


  def run(self):
    key = 0

    self.stdscr.clear()
    self.stdscr.refresh()

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
