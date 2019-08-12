import os
import sudoku_data
import sudoku_solver

def read_data_file(file_name):
  expected_solutions = []
  sudoku = sudoku_data.SudokuData()
  with open(file_name, 'r') as f:
    lines = f.read().split('\n')
    sudoku.from_lines(lines)
    nr_solutions = int(lines[9])
    if nr_solutions == -1:
      expected_solutions = None
    else:
      for i in range(nr_solutions):
        expected_solutions.append(lines[i+10])
  return sudoku, sorted(expected_solutions)

def test_fast_solver():
  path = 'test_data/fast_solver'
  for file_name in os.listdir(path):
    full_name = os.path.join(path, file_name)
    sudoku, expected_solutions = read_data_file(full_name)
    solver = sudoku_solver.SudokuSolver(sudoku)
    solutions = sorted(['{},{},{}'.format(i, j, c) for i, j, c in solver.solve()])
    if solutions != expected_solutions:
      print('Mismtach found for {}.'.format(full_name))
      print('Expected solutions: {}'.format(expected_solutions))
      print('Actual solutions: {}'.format(solutions))
      raise RuntimeError('Testing failed.')
  print('Fast solver tests passed.')


def main():
  test_fast_solver()
  print('Tests passed.')


if __name__ == "__main__":
  main()
