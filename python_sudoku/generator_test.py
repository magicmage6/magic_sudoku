import sudoku_generator
import sudoku_solver


def test_generator(generator, level):
  sudoku = generator.get_sudoku(level=level)
  solver = sudoku_solver.SudokuSolver()
  solution = solver.solve(sudoku)
  if not solution:
    print('Can not solve the generated sudoku.')
    raise RuntimeError('Test for {} level failed.'.format(level))

def test_generators():
  generator = sudoku_generator.SudokuGenerator()
  for _ in range(10):
    test_generator(generator, 'EASY')
    test_generator(generator, 'MEDIUM')
    test_generator(generator, 'HARD')
    test_generator(generator, 'CHALLENGER')
  print('Tests passed.')
