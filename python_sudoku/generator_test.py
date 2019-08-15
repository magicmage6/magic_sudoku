import sudoku_generator
import sudoku_solver


def test_generator(level, nr_tests):
  for _ in range(nr_tests):
    generator = sudoku_generator.SudokuGenerator()
    sudoku = generator.get_sudoku(level=level)
    solver = sudoku_solver.SudokuSolver()
    solution = solver.solve(sudoku)
    passed = True
    if not solution:
      print('Can not solve the generated sudoku.')
      passed = False
    expected_nr_spaces = sudoku_generator._NR_SPACES_DICT[level]
    if len(solution) != expected_nr_spaces:
      print('Expected nr spaces {}. Actual {}'.format(expected_nr_spaces,
                                                      len(solution)))
      passed = False
    if not passed:
      raise RuntimeError('Test for {} level failed.'.format(level))
  print('Tests passed for {} level.'.format(level))


def test_generators():
  test_generator('EASY', 100)
  test_generator('MEDIUM', 50)
  test_generator('HARD', 10)
  test_generator('CHALLENGER', 10)
  print('Tests passed.')
