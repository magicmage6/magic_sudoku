import curses

class SudokuUI:

  def __init__(self, stdscr):
    self.stdscr = stdscr

  def run(self):
    key = 0

    self.stdscr.clear()
    self.stdscr.refresh()

    while key != ord('q'):
      # Get the input key.
      key = self.stdscr.getch()

def run_sudoku(stdscr):
  SudokuUI(stdscr).run()

def main():
  curses.wrapper(run_sudoku)

if __name__ == "__main__":
  main()
