import os
import sudoku_data
import sudoku_solver


def test_fast_solver():
  path = 'test_data/fast_solver'
  for file_name in os.listdir(path):
    sudoku = sudoku_data.SudokuData()
    solver = sudoku_solver.SudokuSolver(sudoku)
    full_name = os.path.join(path, file_name)
    with open(full_name, 'r') as f:
      lines = f.read().split('\n')
      sudoku.from_lines(lines)
      expected_solutions = [line.split(',') for line in lines[9:] if line]
    solutions = [[str(i), str(j), c ]for i, j, c in solver.solve()]
    if solutions != expected_solutions:
      print('Mismtach found for {}.'.format(full_name))
      print('Expected solutions: {}'.format(expected_solutions))
      print('Actual solutions: {}'.format(solutions))
      raise RuntimeError('Testing failed.')


def main():
  test_fast_solver()


if __name__ == "__main__":
  main()
