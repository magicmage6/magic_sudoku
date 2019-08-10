import curses


class Sudoku:

  def __init__(self):
    self.data = [[' ' for x in range(9)] for y in range(9)]

  def set(self, row, col, value):
    self.data[col][row] = value

  def get(self, row, col):
    return self.data[col][row]

class SudokuUI:

  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.height = 18
    self.width = 36
    self.curr_row = 4
    self.curr_col = 4
    self.sudoku = Sudoku()

  def _draw_board(self):
    max_y, max_x = self.stdscr.getmaxyx()
    
    if max_y <= 18:
      raise RuntimeError('Window height must be greater than 18.')
    if max_x <= 27:
      raise RuntimeError('Window width must be greater than 27.')
    if self.width >= max_x:
      self.height -= 9
      self.width -= 18
    if self.height >= max_y:
      self.height -= 9
      self.width -= 18

    left = int((max_x - self.width) / 2)
    right = left + self.width
    up = int((max_y - self.height) /2 )
    down = up + self.height
    delta_x = self.width / 9
    delta_y = self.height / 9

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
        self.stdscr.addch(int(up + i * delta_y) + 1, int(left + j * delta_x) + 2, self.sudoku.get(i,j))

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
    elif key >= ord('1') and key <= ord('9') or key == ord(' '):
      self.sudoku.set(self.curr_row, self.curr_col, chr(key))

  def run(self):
    key = 0

    self.stdscr.clear()
    self.stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)


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
