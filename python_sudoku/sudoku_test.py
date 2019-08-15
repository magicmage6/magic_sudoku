import generator_test
import solver_test


def main():
  print('Testing sudoku solver.')
  solver_test.test_solvers()
  print('Testing sudoku generator.')
  generator_test.test_generators()


if __name__ == '__main__':
  main()
