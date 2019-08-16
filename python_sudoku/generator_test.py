import sudoku_generator
import sudoku_solver


def test_generator(generator, level):
  sudoku = generator.get_sudoku(level=level)
  passed = True
  actual_level = generator.get_sudoku_level(sudoku)
  if level != actual_level:
    print('Level does not match. Expected {}. Actual {}'.format(
        level, actual_level))
    passed = False
  solver = sudoku_solver.SudokuSolver()
  solution = solver.solve(sudoku)
  if not solution:
    print('Can not solve the generated sudoku.')
    passed = False
  if not passed:
    raise RuntimeError('Test for {} level failed.'.format(level))


def test_generators():
  generator = sudoku_generator.SudokuGenerator()
  for _ in range(40):
    test_generator(generator, 'MEDIUM')
  print('Tests for MEDIUM level passed.')
  for _ in range(100):
    test_generator(generator, 'EASY')
  print('Tests for EASY level passed.')
  for _ in range(20):
    test_generator(generator, 'HARD')
  print('Tests for HARD level passed.')
  for _ in range(3):
    test_generator(generator, 'CHALLENGER')
  print('Tests for CHALLENGER level passed.')
  print('All tests passed.')
