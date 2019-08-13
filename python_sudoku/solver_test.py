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
        expected_solutions.append(lines[i + 10])
  if expected_solutions is None:
    sorted_solutions = None
  else:
    sorted_solutions = sorted(expected_solutions)
  return sudoku, sorted_solutions


def compare_solutions(file_name, solutions, expected_solutions):
  if solutions is None:
    sorted_solutions = None
  else:
    sorted_solutions = sorted(
        ['{},{},{}'.format(i, j, c) for i, j, c in solutions])
  if sorted_solutions != expected_solutions:
    print('Mismtach found for {}.'.format(file_name))
    print('Expected solutions: {}'.format(expected_solutions))
    print('Actual solutions: {}'.format(sorted_solutions))
    raise RuntimeError('Testing failed.')


def test_solver(path, fast_solve=False):
  for file_name in os.listdir(path):
    full_name = os.path.join(path, file_name)
    sudoku, expected_solutions = read_data_file(full_name)
    solutions = sudoku_solver.SudokuSolver(sudoku).solve(fast_solve=fast_solve)
    compare_solutions(full_name, solutions, expected_solutions)
  print('Tests in {} passed.'.format(path))


def main():
  data_path = 'python_sudoku/test_data'
  if not os.path.exists(data_path):
    data_path = 'test_data'
    if not os.path.exists(data_path):
      raise RuntimeError('No test_data directory found.')
  test_solver(os.path.join(data_path, 'fast_solver'), fast_solve=True)
  test_solver(os.path.join(data_path, 'full_solver'))
  print('Tests passed.')


if __name__ == '__main__':
  main()
