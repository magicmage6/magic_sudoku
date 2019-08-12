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
  return sudoku, sorted(expected_solutions)


def compare_solutions(file_name, solutions, expected_solutions):
  sorted_solutions = sorted(
      ['{},{},{}'.format(i, j, c) for i, j, c in solutions])
  if sorted_solutions != expected_solutions:
    print('Mismtach found for {}.'.format(file_name))
    print('Expected solutions: {}'.format(expected_solutions))
    print('Actual solutions: {}'.format(sorted_solutions))
    raise RuntimeError('Testing failed.')


def test_fast_solver():
  path = 'test_data/fast_solver'
  for file_name in os.listdir(path):
    full_name = os.path.join(path, file_name)
    sudoku, expected_solutions = read_data_file(full_name)
    solver = sudoku_solver.SudokuSolver(sudoku)
    solutions = solver.solve(fast_solve=True)
    compare_solutions(full_name, solutions, expected_solutions)
  print('Fast solver tests passed.')


def test_full_solver():
  path = 'test_data/full_solver'
  for file_name in os.listdir(path):
    full_name = os.path.join(path, file_name)
    sudoku, expected_solutions = read_data_file(full_name)
    solver = sudoku_solver.SudokuSolver(sudoku)
    solutions = solver.solve()
    compare_solutions(full_name, solutions, expected_solutions)
  print('Full solver tests passed.')


def main():
  test_fast_solver()
  test_full_solver()
  print('Tests passed.')


if __name__ == '__main__':
  main()
